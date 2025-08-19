# Debug script to identify the empty messages issue
from typing import Dict, Any, List
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
import time

def create_simple_guardrails_agent(simple_agent, guardrails_available=True):
    """Create a simplified guardrails agent that avoids API issues."""
    
    if not guardrails_available or not simple_agent:
        print("⚠ Guardrails not available or simple_agent missing")
        return simple_agent
    
    class SafeState(dict):
        """Simple state for guardrails agent."""
        pass
    
    def validate_and_process(state: SafeState) -> Dict[str, Any]:
        """Combined validation and processing to avoid state issues."""
        messages = state.get("messages", [])
        if not messages:
            return {"messages": [AIMessage(content="Error: No input provided")]}
            
        user_message = messages[-1]
        if not hasattr(user_message, 'content'):
            return {"messages": [AIMessage(content="Error: Invalid message format")]}
            
        user_input = user_message.content
        
        # Simple validation checks (avoid external API calls)
        blocked_keywords = ["crypto", "investment", "gambling", "politics"]
        if any(keyword in user_input.lower() for keyword in blocked_keywords):
            return {"messages": messages + [AIMessage(content="Request blocked: Off-topic. Please ask about student loans or financial aid.")]}
        
        # Check for obvious jailbreak attempts
        jailbreak_patterns = ["ignore", "instructions", "system", "prompt"]
        if len([p for p in jailbreak_patterns if p in user_input.lower()]) >= 2:
            return {"messages": messages + [AIMessage(content="Request blocked: Invalid request pattern. Please ask about student loans or financial aid.")]}
        
        # Call the underlying agent safely
        try:
            response = simple_agent.invoke({"messages": messages})
            
            # Simple output validation
            if "messages" in response and response["messages"]:
                last_response = response["messages"][-1]
                if hasattr(last_response, 'content'):
                    content = last_response.content
                    
                    # Simple PII redaction
                    import re
                    # Redact SSN patterns
                    content = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '<SSN_REDACTED>', content)
                    # Redact phone patterns  
                    content = re.sub(r'\b\d{3}-\d{3}-\d{4}\b', '<PHONE_REDACTED>', content)
                    
                    # Update response
                    response["messages"][-1] = AIMessage(content=content)
            
            return response
            
        except Exception as e:
            print(f"Agent error: {e}")
            return {"messages": messages + [AIMessage(content="I apologize, but I encountered an error. Please try rephrasing your question about student loans or financial aid.")]}
    
    # Build simple graph
    graph = StateGraph(SafeState)
    graph.add_node("process", validate_and_process)
    graph.set_entry_point("process")
    graph.add_edge("process", END)
    
    return graph.compile()

# Test the simple version
print("🔧 Creating simplified guardrails agent...")
