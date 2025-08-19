# Simple A2A LangGraph Client

This directory contains two implementations of a Simple LangGraph Agent that communicates with the A2A Agent Node through the A2A protocol.

## Files Created

1. **`simple_agent_client.py`** - Full-featured interactive client with conversation flow
2. **`minimal_a2a_client.py`** - Minimal, non-chatty demonstration client

## What These Agents Do

Both agents demonstrate how to:
- Create a LangGraph agent with A2A protocol communication
- Use the existing A2A Agent Node as a tool within a new LangGraph workflow
- Handle the A2A message protocol for agent-to-agent communication

## Key Features

### Simple Agent Client (`simple_agent_client.py`)
- **Interactive CLI**: Chat-based interface for testing
- **Tool Integration**: Uses A2A agent as a LangGraph tool
- **Error Handling**: Robust error handling and user feedback
- **Conversation Memory**: Maintains conversation context

### Minimal A2A Client (`minimal_a2a_client.py`)
- **Non-chatty**: Minimal output, focused on functionality
- **Demo Mode**: Runs predefined test queries
- **Clean Code**: Simplified structure for easy understanding
- **A2A Core**: Pure focus on A2A protocol communication

## Setup & Usage

### 1. Start the A2A Agent Server
```bash
# In one terminal
uv run python -m app
```
This starts your existing A2A agent on `localhost:10000`

### 2. Run the Simple Agent Client

**Interactive Client:**
```bash
uv run python simple_agent_client.py
```

**Minimal Demo:**
```bash
uv run python minimal_a2a_client.py
```

## How It Works

### LangGraph Structure
```
[User Input] → [Agent Node] → [Should Call A2A?] 
                     ↓              ↓
                [Direct Response]  [A2A Tool Call]
                     ↓              ↓
                   [END]         [Tool Node] → [Agent Node] → [END]
```

### A2A Communication Flow
1. User asks a question
2. LangGraph agent decides if it needs the A2A agent's capabilities
3. If yes, calls `query_a2a_agent` tool
4. Tool makes HTTP request to A2A server (`localhost:10000`)
5. A2A server processes with its tools (Tavily, ArXiv, RAG)
6. Response flows back through the chain

## Test Queries

Try these to see A2A communication in action:

**Web Search:**
- "What are the latest AI developments in 2024?"
- "Current news about large language models"

**Academic Research:**
- "Find recent papers on transformer architectures"
- "Research on multimodal AI models"

**Document Retrieval (if you have docs in `data/`):**
- "What do the documents say about requirements?"

## Architecture Benefits

This approach demonstrates:
- **Modularity**: Your existing A2A agent becomes a reusable component
- **Composability**: New agents can leverage existing agent capabilities
- **Protocol Compliance**: Proper A2A message format handling
- **Scalability**: Easy to add more A2A agents as tools

## Code Structure

### Core Components

**Tool Definition:**
```python
@tool
async def query_a2a_agent(question: str) -> str:
    """Query the A2A Agent Node through HTTP."""
```

**LangGraph Nodes:**
- `agent_node`: Main LLM decision maker
- `tool_node`: Executes A2A calls
- Conditional routing based on tool calls

**A2A Protocol:**
- Uses `A2ACardResolver` to discover agent capabilities
- Formats messages according to A2A standards
- Handles response parsing

This implementation showcases how LangGraph can orchestrate agent-to-agent communication through standardized protocols like A2A.
