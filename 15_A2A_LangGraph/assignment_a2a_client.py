
import os
import asyncio
from typing import Dict, Any, List, TypedDict, Annotated
from uuid import uuid4

import httpx
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

from a2a.client import A2ACardResolver, A2AClient
from a2a.types import MessageSendParams, SendMessageRequest

load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[List, add_messages]


@tool
async def query_a2a_agent(question: str) -> str:
    """Query the A2A Agent Node."""
    async with httpx.AsyncClient(timeout=60.0) as client:
        resolver = A2ACardResolver(client, 'http://localhost:10000')
        card = await resolver.get_agent_card()
        a2a_client = A2AClient(client, card)
        
        request = SendMessageRequest(
            id=str(uuid4()),
            params=MessageSendParams(
                message={
                    'role': 'user',
                    'parts': [{'kind': 'text', 'text': question}],
                    'message_id': uuid4().hex,
                }
            )
        )
        
        response = await a2a_client.send_message(request)
        
        # Extract response text
        if response.root and response.root.result and response.root.result.artifacts:
            for artifact in response.root.result.artifacts:
                if artifact.parts:
                    for part in artifact.parts:
                        if hasattr(part.root, 'text'):
                            return part.root.text
        
        return "No response from A2A agent"


def build_simple_agent():
    """Build LangGraph agent."""
    model = ChatOpenAI(
        model=os.getenv('TOOL_LLM_NAME', 'gpt-4o-mini'),
        openai_api_key=os.getenv('OPENAI_API_KEY'),
        temperature=0
    ).bind_tools([query_a2a_agent])
    
    def agent_node(state: AgentState) -> Dict[str, Any]:
        return {"messages": [model.invoke(state["messages"])]}
    
    async def tool_node(state: AgentState) -> Dict[str, Any]:
        last_message = state["messages"][-1]
        responses = []
        
        for tool_call in last_message.tool_calls:
            result = await query_a2a_agent.ainvoke(tool_call["args"])
            responses.append(ToolMessage(
                content=result,
                tool_call_id=tool_call["id"],
                name=tool_call["name"]
            ))
        
        return {"messages": responses}
    
    def should_continue(state: AgentState) -> str:
        return "tools" if state["messages"][-1].tool_calls else END
    
    # Build graph
    graph = StateGraph(AgentState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")
    
    return graph.compile()


async def demo():
    """Demo the minimal A2A client."""
    agent = build_simple_agent()
    
    test_queries = [
        "What are the latest AI developments?",
        "Find papers on transformer architectures",
        "What's 2 plus 2"
    ]
    
    print("A2A Client Demo")
    print("=" * 40)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 30)
        
        try:
            inputs = {"messages": [HumanMessage(content=query)]}
            
            async for event in agent.astream(inputs):
                for node, output in event.items():
                    if node == "agent" and "messages" in output:
                        msg = output["messages"][-1]
                        if isinstance(msg, AIMessage) and not msg.tool_calls:
                            print(f"Response: {msg.content}")
                    elif node == "tools":
                        print("✓ A2A agent called")
        
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: Set OPENAI_API_KEY in .env file")
        exit(1)
    
    print("Ensure A2A server is running: uv run python -m app")
    asyncio.run(demo())
