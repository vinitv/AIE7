"""
Demo script showing the LangGraph A2A Client structure without API calls.

This demonstrates the graph structure and flow without requiring API keys.
"""
import json
from typing import Dict, Any, List, TypedDict, Annotated

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage


class AgentState(TypedDict):
    messages: Annotated[List, add_messages]


def build_demo_agent():
    """Build a demo LangGraph agent showing A2A communication structure."""
    
    def agent_node(state: AgentState) -> Dict[str, Any]:
        """Mock agent node that decides whether to call A2A agent."""
        last_message = state["messages"][-1]
        user_input = last_message.content
        
        # Simple rule: if user asks about complex topics, simulate tool call
        complex_keywords = ["search", "research", "find", "latest", "papers", "news"]
        needs_a2a = any(keyword in user_input.lower() for keyword in complex_keywords)
        
        if needs_a2a:
            # Simulate tool call decision
            mock_response = AIMessage(
                content="I need to search for that information.",
                tool_calls=[{
                    "id": "call_123",
                    "name": "query_a2a_agent", 
                    "args": {"question": user_input}
                }]
            )
            print(f"🔄 Agent decided to call A2A agent for: '{user_input}'")
        else:
            # Direct response
            mock_response = AIMessage(
                content=f"I can help with that directly. You asked: {user_input}"
            )
            print(f"💬 Agent responding directly to: '{user_input}'")
        
        return {"messages": [mock_response]}
    
    def tool_node(state: AgentState) -> Dict[str, Any]:
        """Mock tool node that simulates A2A agent call."""
        last_message = state["messages"][-1]
        tool_call = last_message.tool_calls[0]
        question = tool_call["args"]["question"]
        
        print(f"📡 Calling A2A Agent with: '{question}'")
        print("   → Fetching agent card from localhost:10000")
        print("   → Sending A2A protocol message")
        print("   → A2A agent processing with tools (Tavily, ArXiv, RAG)")
        print("   → Receiving A2A protocol response")
        
        # Simulate A2A response
        mock_tool_response = ToolMessage(
            content=f"A2A Agent found: [Simulated response for '{question}']",
            tool_call_id="call_123"
        )
        
        return {"messages": [mock_tool_response]}
    
    def should_continue(state: AgentState) -> str:
        """Route to tool node or end based on tool calls."""
        last_message = state["messages"][-1]
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "tools"
        return END
    
    # Build the graph
    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)
    graph.set_entry_point("agent")
    graph.add_conditional_edges(
        "agent", 
        should_continue, 
        {"tools": "tools", END: END}
    )
    graph.add_edge("tools", "agent")
    
    return graph.compile()


def demo_workflow():
    """Demonstrate the A2A client workflow."""
    print("🤖 LangGraph A2A Client Structure Demo")
    print("=" * 50)
    
    agent = build_demo_agent()
    
    test_cases = [
        "Hello, how are you?",  # Direct response
        "Search for latest AI news",  # Should trigger A2A call
        "Find papers on transformers",  # Should trigger A2A call
        "What's 2+2?",  # Direct response
    ]
    
    for i, query in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: '{query}'")
        print("-" * 30)
        
        inputs = {"messages": [HumanMessage(content=query)]}
        
        for event in agent.stream(inputs):
            for node_name, output in event.items():
                if node_name == "agent":
                    pass  # Agent processing logged in node
                elif node_name == "tools":
                    pass  # Tool processing logged in node
    
    print("\n" + "=" * 50)
    print("🎯 Key Architecture Points:")
    print("1. LangGraph routes user queries intelligently")
    print("2. Complex queries trigger A2A protocol calls")
    print("3. A2A agent acts as a specialized tool")
    print("4. Responses flow back through the graph")
    print("5. The system is composable and extensible")


def show_graph_structure():
    """Show the LangGraph structure."""
    print("\n📊 LangGraph Structure:")
    print("""
    ┌─────────────┐
    │ User Input  │
    └─────┬───────┘
          │
          ▼
    ┌─────────────┐
    │ Agent Node  │ ◄─── Main LLM Decision Point
    └─────┬───────┘
          │
          ▼
    ┌─────────────┐
    │Should Call  │ ◄─── Conditional Router
    │   A2A?      │
    └─────┬───────┘
          │
     ┌────┴────┐
     │         │
     ▼         ▼
┌─────────┐ ┌─────────────┐
│Direct   │ │ Tool Node   │ ◄─── A2A Protocol Call
│Response │ │ (A2A Agent) │
└─────────┘ └─────┬───────┘
     │            │
     │            ▼
     │       ┌─────────────┐
     │       │ Agent Node  │ ◄─── Process A2A Response
     │       │ (Final)     │
     │       └─────┬───────┘
     │             │
     ▼             ▼
    ┌─────────────┐
    │    END      │
    └─────────────┘
    """)


if __name__ == "__main__":
    demo_workflow()
    show_graph_structure()
    
    print("\n🚀 To test with real A2A calls:")
    print("1. Set OPENAI_API_KEY in .env")
    print("2. Start A2A server: uv run python -m app")
    print("3. Run: uv run python minimal_a2a_client.py")
