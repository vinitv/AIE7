"""LangGraph agent integration with production features."""

from typing import Dict, Any, List, Optional
import os

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_core.tools import tool
from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages

from .models import get_openai_model
from .rag import ProductionRAGChain


class AgentState(TypedDict):
    """State schema for agent graphs."""
    messages: Annotated[List[BaseMessage], add_messages]


def create_rag_tool(rag_chain: ProductionRAGChain):
    """Create a RAG tool from a ProductionRAGChain."""
    
    @tool
    def retrieve_information(query: str) -> str:
        """Use Retrieval Augmented Generation to retrieve information from the student loan documents."""
        try:
            result = rag_chain.invoke(query)
            return result.content if hasattr(result, 'content') else str(result)
        except Exception as e:
            return f"Error retrieving information: {str(e)}"
    
    return retrieve_information


def get_default_tools(rag_chain: Optional[ProductionRAGChain] = None) -> List:
    """Get default tools for the agent.
    
    Args:
        rag_chain: Optional RAG chain to include as a tool
        
    Returns:
        List of tools
    """
    tools = []
    
    # Add Tavily search if API key is available
    if os.getenv("TAVILY_API_KEY"):
        tools.append(TavilySearchResults(max_results=5))
    
    # Add Arxiv tool
    tools.append(ArxivQueryRun())
    
    # Add RAG tool if provided
    if rag_chain:
        tools.append(create_rag_tool(rag_chain))
    
    return tools


def create_langgraph_agent(
    model_name: str = "gpt-4",
    temperature: float = 0.1,
    tools: Optional[List] = None,
    rag_chain: Optional[ProductionRAGChain] = None
):
    """Create a simple LangGraph agent.
    
    Args:
        model_name: OpenAI model name
        temperature: Model temperature
        tools: List of tools to bind to the model
        rag_chain: Optional RAG chain to include as a tool
        
    Returns:
        Compiled LangGraph agent
    """
    if tools is None:
        tools = get_default_tools(rag_chain)
    
    # Get model and bind tools
    model = get_openai_model(model_name=model_name, temperature=temperature)
    model_with_tools = model.bind_tools(tools)
    
    def call_model(state: AgentState) -> Dict[str, Any]:
        """Invoke the model with messages."""
        messages = state["messages"]
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}
    
    def should_continue(state: AgentState):
        """Route to tools if the last message has tool calls."""
        last_message = state["messages"][-1]
        if getattr(last_message, "tool_calls", None):
            return "action"
        return END
    
    # Build graph
    graph = StateGraph(AgentState)
    tool_node = ToolNode(tools)
    
    graph.add_node("agent", call_model)
    graph.add_node("action", tool_node)
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue, {"action": "action", END: END})
    graph.add_edge("action", "agent")
    
    return graph.compile()


def create_helpfulness_agent(
    model_name: str = "gpt-4",
    temperature: float = 0.1,
    tools: Optional[List] = None,
    rag_chain: Optional[ProductionRAGChain] = None,
    max_iterations: int = 2
):
    """Create a helpfulness agent with evaluation and refinement capabilities.
    
    Args:
        model_name: OpenAI model name
        temperature: Model temperature
        tools: List of tools to bind to the model
        rag_chain: Optional RAG chain to include as a tool
        max_iterations: Maximum refinement iterations
        
    Returns:
        Compiled LangGraph agent with helpfulness evaluation
    """
    if tools is None:
        tools = get_default_tools(rag_chain)
    
    # Get model and bind tools
    model = get_openai_model(model_name=model_name, temperature=temperature)
    model_with_tools = model.bind_tools(tools)
    
    # Evaluation model (can be cheaper)
    eval_model = get_openai_model(model_name="gpt-3.5-turbo", temperature=0.1)
    
    class HelpfulnessState(TypedDict):
        """Extended state for helpfulness agent."""
        messages: Annotated[List[BaseMessage], add_messages]
        iteration_count: int
        evaluation_scores: List[float]
        
    def call_model(state: HelpfulnessState) -> Dict[str, Any]:
        """Invoke the model with messages."""
        messages = state["messages"]
        response = model_with_tools.invoke(messages)
        return {"messages": [response]}
    
    def evaluate_helpfulness(state: HelpfulnessState) -> Dict[str, Any]:
        """Evaluate the helpfulness of the last response."""
        messages = state.get("messages", [])
        if not messages:
            return {"evaluation_scores": state.get("evaluation_scores", [])}
            
        last_message = messages[-1]
        if not isinstance(last_message, AIMessage):
            return {"evaluation_scores": state.get("evaluation_scores", [])}
            
        # Get the original question
        human_messages = [msg for msg in messages if hasattr(msg, 'type') and msg.type == "human"]
        if not human_messages:
            return {"evaluation_scores": state.get("evaluation_scores", [])}
            
        original_question = human_messages[0].content
        response_content = last_message.content
        
        # Simple scoring without LLM call to avoid API issues
        # Basic heuristic: longer responses with question words get higher scores
        score = 5.0  # Default score
        if len(response_content) > 100:
            score += 1.0
        if any(word in response_content.lower() for word in ['loan', 'student', 'financial', 'aid']):
            score += 1.0
        if len(response_content.split()) > 20:
            score += 1.0
        
        score = min(10.0, max(1.0, score))  # Clamp between 1-10
        
        scores = state.get("evaluation_scores", [])
        scores.append(score)
        return {"evaluation_scores": scores}
    
    def should_continue_or_refine(state: HelpfulnessState):
        """Decide whether to continue with tools, refine, or end."""
        last_message = state["messages"][-1]
        iteration_count = state.get("iteration_count", 0)
        scores = state.get("evaluation_scores", [])
        
        # Check for tool calls first
        if getattr(last_message, "tool_calls", None):
            return "action"
            
        # Check if we should refine
        if scores and iteration_count < max_iterations:
            latest_score = scores[-1]
            if latest_score < 7.0:  # Threshold for refinement
                return "refine"
                
        return END
    
    def refine_response(state: HelpfulnessState) -> Dict[str, Any]:
        """Refine the response based on evaluation."""
        iteration_count = state.get("iteration_count", 0)
        scores = state.get("evaluation_scores", [])
        
        if not scores:
            return {"iteration_count": iteration_count + 1}
            
        # Simple refinement: add more detail if score is low
        last_message = state["messages"][-1]
        last_response = last_message.content
        
        # Get original question
        human_messages = [msg for msg in state["messages"] if hasattr(msg, 'type') and msg.type == "human"]
        original_question = human_messages[0].content if human_messages else ""
        
        # Simple refinement: add clarification
        refined_content = f"{last_response}\n\nTo provide more specific information about {original_question.lower()}, please let me know if you need details about eligibility, application process, or repayment options."
        
        refined_message = AIMessage(content=refined_content)
        return {
            "messages": [refined_message],
            "iteration_count": iteration_count + 1
        }
    
    # Build graph
    graph = StateGraph(HelpfulnessState)
    tool_node = ToolNode(tools)
    
    graph.add_node("agent", call_model)
    graph.add_node("action", tool_node)
    graph.add_node("evaluate", evaluate_helpfulness)
    graph.add_node("refine", refine_response)
    
    graph.set_entry_point("agent")
    graph.add_edge("agent", "evaluate")
    graph.add_conditional_edges("evaluate", should_continue_or_refine, {
        "action": "action", 
        "refine": "refine",
        END: END
    })
    graph.add_edge("action", "agent")
    graph.add_edge("refine", "evaluate")
    
    return graph.compile()
