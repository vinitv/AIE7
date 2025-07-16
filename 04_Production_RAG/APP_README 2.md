# RAG Application with LangSmith

This is a production-ready RAG (Retrieval-Augmented Generation) application that processes student loan documents and answers questions using LangGraph and LangSmith for monitoring.

## Features

- **Document Processing**: Loads PDF documents from the `data/` directory
- **Intelligent Chunking**: Uses tiktoken-based chunking for optimal token management
- **Vector Storage**: Uses Qdrant for efficient document retrieval
- **LangGraph Pipeline**: Implements a graph-based RAG architecture
- **Enhanced Prompt Engineering**: Includes Activity #2 improvements for better context handling
- **LangSmith Integration**: Full tracing and monitoring capabilities

## Setup

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Prepare Data**:
   - Make sure you have a `data/` directory with PDF files
   - The application expects student loan-related documents

3. **API Keys**:
   - You'll need an OpenAI API key
   - You'll need a LangSmith API key (free account at https://www.langchain.com/langsmith)

## Usage

Run the application:
```bash
python app.py
```

The application will:
1. Prompt you for your OpenAI API key
2. Prompt you for your LangSmith API key
3. Load and process documents from the `data/` directory
4. Create embeddings and vector store
5. Set up the LangGraph RAG pipeline
6. Run test queries to demonstrate functionality
7. Enable LangSmith tracing for monitoring

## What's Included

### From LangSmith Notebook (Tasks 1-4):
- ✅ **Task 1**: Dependencies and OpenAI API Key setup
- ✅ **Task 2**: LangGraph RAG implementation
- ✅ **Activity #2**: Enhanced prompt template for better context handling
- ✅ **Task 3**: LangSmith setup and configuration
- ✅ **Task 4**: Testing and trace generation

### Key Components:
- **Enhanced Prompt Template**: Implements Activity #2 requirements for better context relevance checking
- **Robust Error Handling**: Graceful error handling throughout the pipeline
- **Comprehensive Testing**: Tests both relevant and irrelevant questions
- **LangSmith Integration**: Full tracing with unique project IDs

## LangSmith Monitoring

After running the application, you can:
1. Go to your LangSmith dashboard
2. Find your project (named "LangSmith - [unique_id]")
3. View traces for all the test queries
4. Analyze performance, token usage, and system behavior

## Expected Output

The application will test three scenarios:
1. **Relevant Question**: "What is the maximum loan amount I can get from the government to go to school these days?"
2. **Irrelevant Question**: "What is the airspeed velocity of an unladen swallow?"
3. **Another Relevant Question**: "Is applying for and securing a student loan in 2025 a terrible idea?"

The enhanced prompt should provide accurate answers for relevant questions and respond with "I don't know" for irrelevant questions.

## Notes

- The application uses `gpt-4o-mini` instead of `gpt-4.1-nano` for better reliability
- Vector store is created in memory for quick setup
- All traces are automatically sent to LangSmith for monitoring
- The application includes comprehensive logging for debugging 