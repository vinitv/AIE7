import os
import getpass
from uuid import uuid4
import tiktoken
import nest_asyncio

# Apply asyncio bug handling
nest_asyncio.apply()

# Dependencies
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Qdrant
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph
from typing_extensions import TypedDict
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser

def setup_api_keys():
    """Setup OpenAI and LangSmith API keys"""
    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API Key: ")
    
    if "LANGSMITH_API_KEY" not in os.environ:
        os.environ["LANGSMITH_API_KEY"] = getpass.getpass("Enter your LangSmith API Key: ")

def setup_langsmith():
    """Setup LangSmith tracing"""
    unique_id = uuid4().hex[0:8]
    
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com/"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com/"
    os.environ["LANGSMITH_PROJECT"] = f"LangSmith - {unique_id}"
    
    print(f"LangSmith project created: LangSmith - {unique_id}")

def load_documents():
    """Load PDF documents from data directory"""
    print("Loading documents...")
    directory_loader = DirectoryLoader("data", glob="**/*.pdf", loader_cls=PyMuPDFLoader)
    loan_knowledge_resources = directory_loader.load()
    print(f"Loaded {len(loan_knowledge_resources)} documents")
    return loan_knowledge_resources

def tiktoken_len(text):
    """Calculate token length using tiktoken"""
    tokens = tiktoken.encoding_for_model("gpt-4o").encode(text)
    return len(tokens)

def chunk_documents(documents):
    """Split documents into chunks"""
    print("Chunking documents...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=750,
        chunk_overlap=0,
        length_function=tiktoken_len,
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")
    
    # Verify max chunk length
    max_chunk_length = max(tiktoken_len(chunk.page_content) for chunk in chunks)
    print(f"Maximum chunk length: {max_chunk_length} tokens")
    
    return chunks

def create_vectorstore(chunks):
    """Create Qdrant vectorstore with embeddings"""
    print("Creating vectorstore...")
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
    
    qdrant_vectorstore = Qdrant.from_documents(
        documents=chunks,
        embedding=embedding_model,
        location=":memory:"
    )
    
    print("Vectorstore created successfully")
    return qdrant_vectorstore

def create_enhanced_prompt():
    """Create enhanced prompt template for Activity #2"""
    HUMAN_TEMPLATE = """
You are a helpful assistant that answers questions about student loans and financial aid based on provided context.

#CONTEXT:
{context}

#QUERY:
{query}

#INSTRUCTIONS:
1. Carefully read the provided context above
2. Analyze if the context is relevant to answering the user's query
3. If the context contains relevant information to answer the query:
   - Provide a clear, accurate answer based ONLY on the information in the context
   - Do not add information that is not explicitly stated in the context
4. If the context is not relevant or does not contain enough information to answer the query:
   - Respond with "I don't know" or "I don't have enough information to answer that question"
5. Do not make up information or use knowledge outside of the provided context

#RESPONSE:
"""
    
    return ChatPromptTemplate.from_messages([
        ("human", HUMAN_TEMPLATE)
    ])

# Define State for LangGraph
class State(TypedDict):
    question: str
    context: list[Document]
    response: str

def create_rag_graph(retriever, chat_prompt, openai_chat_model):
    """Create LangGraph RAG pipeline"""
    
    def retrieve(state: State) -> State:
        retrieved_docs = retriever.invoke(state["question"])
        return {"context": retrieved_docs}
    
    def generate(state: State) -> State:
        generator_chain = chat_prompt | openai_chat_model | StrOutputParser()
        response = generator_chain.invoke({
            "query": state["question"], 
            "context": state["context"]
        })
        return {"response": response}
    
    # Build the graph
    graph_builder = StateGraph(State)
    graph_builder = graph_builder.add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    
    return graph_builder.compile()

def test_rag_system(rag_graph):
    """Test the RAG system with sample questions"""
    print("\n" + "="*50)
    print("TESTING RAG SYSTEM")
    print("="*50)
    
    # Test 1: Relevant question
    print("\nTest 1: Relevant question")
    question1 = "What is the maximum loan amount I can get from the government to go to school these days?"
    response1 = rag_graph.invoke({"question": question1}, {"tags": ["Demo Run"]})
    print(f"Question: {question1}")
    print(f"Response: {response1['response']}")
    
    print("\nRetrieved Context:")
    for i, context in enumerate(response1["context"], 1):
        print(f"Context {i}: {context.page_content[:100]}...")
    
    # Test 2: Irrelevant question
    print("\n" + "-"*50)
    print("Test 2: Irrelevant question")
    question2 = "What is the airspeed velocity of an unladen swallow?"
    response2 = rag_graph.invoke({"question": question2})
    print(f"Question: {question2}")
    print(f"Response: {response2['response']}")
    
    # Test 3: Another relevant question
    print("\n" + "-"*50)
    print("Test 3: Another relevant question")
    question3 = "Is applying for and securing a student loan in 2025 a terrible idea?"
    response3 = rag_graph.invoke({"question": question3})
    print(f"Question: {question3}")
    print(f"Response: {response3['response']}")
    
    print("\n" + "="*50)

def main():
    """Main function to run the RAG application"""
    print("Starting RAG Application Setup...")
    
    try:
        # Setup API keys
        setup_api_keys()
        
        # Setup LangSmith
        setup_langsmith()
        
        # Load and process documents
        documents = load_documents()
        chunks = chunk_documents(documents)
        
        # Create vectorstore
        vectorstore = create_vectorstore(chunks)
        retriever = vectorstore.as_retriever()
        
        # Setup LLM and prompt
        openai_chat_model = ChatOpenAI(model="gpt-4o-mini")  # Using gpt-4o-mini as it's more reliable
        chat_prompt = create_enhanced_prompt()
        
        # Create RAG graph
        print("Creating RAG graph...")
        rag_graph = create_rag_graph(retriever, chat_prompt, openai_chat_model)
        
        print("RAG system setup complete!")
        
        # Test the system
        test_rag_system(rag_graph)
        
        print("\nRAG system is ready! You can now check your LangSmith dashboard for traces.")
        print("The system has been tested with sample questions.")
        
        return rag_graph
        
    except Exception as e:
        print(f"Error setting up RAG system: {e}")
        return None

if __name__ == "__main__":
    rag_graph = main() 