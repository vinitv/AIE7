<p align = "center" draggable=”false” ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719" 
     width="200px"
     height="auto"/>
</p>

# Space Exploration Agent

An AI-powered research assistant for space exploration and astronomy, built with LangGraph and featuring DALL-E image generation.

## 🌟 Features

- **Web Search**: Get the latest space news, research papers, and current developments
- **DALL-E Image Generation**: Create stunning space-themed images and visualizations
- **NASA API Integration**: Access official NASA data, astronomy pictures, and Mars rover photos
- **Beautiful React Frontend**: Modern, responsive interface with space-themed design
- **LangGraph Workflow**: Intelligent agent that can use multiple tools in sequence

## 🛠️ Tech Stack

### Backend
- **LangGraph**: For building the agent workflow
- **LangChain**: For tool integration and model management
- **OpenAI**: GPT-4o-mini for reasoning and DALL-E for image generation
- **Tavily**: For web search capabilities
- **NASA API**: For official space data
- **FastAPI**: For the REST API
- **Uvicorn**: ASGI server

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Lucide React**: Beautiful icons
- **Axios**: HTTP client

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Node.js 18+
- API keys for:
  - OpenAI (for GPT and DALL-E)
  - Tavily (for web search)
  - NASA (optional, uses demo key by default)

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd 05_Our_First_Agent_with_LangGraph
```

### 2. Backend Setup

```bash
# Navigate to the API directory
cd api

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (replace with your actual keys)
export OPENAI_API_KEY="your-openai-api-key"
export TAVILY_API_KEY="your-tavily-api-key"
export NASA_API_KEY="your-nasa-api-key"  # Optional

# Run the backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
# In a new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 4. Configure API Keys

**Option A: UI Setup (Recommended)**
1. Open your browser and go to `http://localhost:3000`
2. You'll be redirected to the setup page
3. Enter your API keys in the beautiful setup interface
4. Click "Validate & Continue"

**Option B: Environment Variables**
Set the environment variables before starting the backend (as shown in step 2).

## 🌌 Usage Examples

The agent can handle various types of space exploration queries:

### Research Questions
- "What are the latest developments in Mars exploration?"
- "Tell me about the James Webb Space Telescope discoveries"
- "What's happening with SpaceX's Starship program?"

### Image Generation
- "Generate an image of a futuristic space station orbiting Earth"
- "Create an image of a black hole with accretion disk"
- "Show me a visualization of the solar system"

### NASA Data
- "What's the latest astronomy picture of the day from NASA?"
- "Show me recent Mars rover photos"
- "What asteroids are near Earth right now?"

## 🚀 Deployment

### Frontend (Vercel)

The frontend is optimized for Vercel deployment:

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Set the **Root Directory** to `frontend`
4. Deploy!

The frontend will work with your local backend during development, and you can point it to any deployed backend by updating the API configuration.

### Backend (Local/Cloud)

For production, deploy the backend to a Python-friendly platform:

**Option 1: Railway**
```bash
# Deploy the api/ directory to Railway
# Set environment variables in Railway dashboard
```

**Option 2: Render**
```bash
# Deploy the api/ directory to Render
# Set environment variables in Render dashboard
```

**Option 3: Local Development**
The easiest approach is to keep the backend running locally while deploying only the frontend to Vercel.

### Environment Variables

For backend deployment, set these environment variables:

```bash
OPENAI_API_KEY=your-openai-api-key
TAVILY_API_KEY=your-tavily-api-key
NASA_API_KEY=your-nasa-api-key  # Optional
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=space-exploration-agent
LANGCHAIN_API_KEY=your-langsmith-api-key
```

## 🔧 Development

### Project Structure
```
├── space_exploration_agent.py    # Main agent logic
├── api/
│   ├── main.py                   # FastAPI backend
│   ├── requirements.txt          # Python dependencies
│   └── venv/                     # Virtual environment
├── frontend/
│   ├── app/
│   │   ├── page.tsx             # Main page component
│   │   ├── layout.tsx           # Root layout
│   │   └── globals.css          # Global styles
│   ├── lib/
│   │   └── config.ts            # API configuration
│   ├── package.json             # Frontend dependencies
│   └── tailwind.config.js       # Tailwind configuration
├── vercel.json                  # Vercel configuration (frontend only)
├── pyproject.toml               # Python dependencies
└── README.md                    # This file
```

### Running Both Services

**Terminal 1 (Backend):**
```bash
cd api
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

### Adding New Tools

1. Create a new tool function in `space_exploration_agent.py`
2. Add it to the `get_tools()` function
3. Test with the agent

### Customizing the Frontend

1. Modify components in `frontend/app/`
2. Update styles in `frontend/app/globals.css`
3. Add new pages in the `frontend/app/` directory

## ⚠️ Deployment Notes

- **Vercel Limitations**: Due to Vercel's serverless function limitations and the size of LangChain dependencies, we deploy only the frontend to Vercel
- **Backend Deployment**: The backend requires a more traditional server environment for optimal performance
- **Local Development**: The easiest setup is running the backend locally while developing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- LangChain team for the amazing framework
- OpenAI for GPT and DALL-E
- NASA for their public APIs
- The space exploration community for inspiration

---

**Explore the final frontier with AI! 🚀✨**
