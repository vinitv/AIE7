# Unified Space Exploration Agent Deployment

This guide shows how to deploy both the Next.js frontend and FastAPI backend as a **single Cloud Run service**.

## 🌟 Benefits of Unified Deployment

- **Simplified Architecture**: One service instead of two
- **Lower Costs**: Single Cloud Run instance
- **No CORS Issues**: Frontend and API on same domain
- **Easier Management**: One deployment, one URL
- **Better Performance**: No cross-service network calls

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│          Cloud Run Service          │
├─────────────────────────────────────┤
│  FastAPI Backend                    │
│  ├── API endpoints (/api/*, /ask)   │
│  ├── Health check (/health)         │
│  └── Static file serving (/)        │
├─────────────────────────────────────┤
│  Next.js Frontend (Static Export)   │
│  ├── Built to /static directory     │
│  ├── React SPA                      │
│  └── Served by FastAPI              │
└─────────────────────────────────────┘
```

## 🚀 Quick Deployment

### Prerequisites
- Google Cloud Project with billing enabled
- gcloud CLI installed and authenticated
- Docker (for local testing, optional)

### Deploy to Cloud Run

1. **Set your Google Cloud project:**
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Deploy the unified service:**
   ```bash
   ./deploy-unified.sh
   ```

3. **Access your application:**
   - The script will output your service URL
   - Visit the URL to access the frontend
   - API endpoints are available at the same domain

## 📁 File Structure

```
space-exploration-agent/
├── Dockerfile                 # Unified Docker build
├── cloudbuild-unified.yaml   # Cloud Build config
├── deploy-unified.sh          # Deployment script
├── api/                       # Backend code
│   ├── main.py               # FastAPI app (now serves static files)
│   ├── requirements.txt      # Python dependencies
│   └── ...
├── frontend/                 # Frontend code
│   ├── next.config.js        # Next.js config (export mode)
│   ├── package.json          # Node.js dependencies
│   └── ...
└── space_exploration_agent.py # Agent logic
```

## 🔧 How It Works

1. **Build Process:**
   - Next.js frontend is built to static files
   - Python backend is set up with FastAPI
   - Static files are copied to `/static` directory

2. **Runtime:**
   - FastAPI serves API endpoints (`/api/*`, `/ask`, `/health`)
   - FastAPI serves static frontend files for all other routes
   - Single port (8080) handles all traffic

3. **Routing:**
   ```
   /health          → FastAPI health check
   /api/test-keys   → FastAPI API endpoint
   /ask             → FastAPI API endpoint
   /setup           → Static frontend file
   /                → Static frontend (index.html)
   /*               → Static frontend files or index.html
   ```

## 🔑 API Keys Setup

After deployment:
1. Visit `YOUR_SERVICE_URL/setup`
2. Enter your API keys:
   - OpenAI API Key (required)
   - Tavily API Key (for web search)
   - NASA API Key (optional, DEMO_KEY works)

## 🧪 Local Testing

To test the unified build locally:

```bash
# Build the Docker image
docker build -t space-agent-unified .

# Run locally
docker run -p 8080:8080 space-agent-unified
```

Visit `http://localhost:8080` to test the full application.

## 🔄 Comparison with Two-Service Deployment

| Aspect | Unified Service | Two Services |
|--------|----------------|--------------|
| Services | 1 Cloud Run service | 2 Cloud Run services |
| Cost | Lower (1 instance) | Higher (2 instances) |
| Complexity | Simpler | More complex |
| CORS | No issues | Requires configuration |
| Scaling | Single service scaling | Independent scaling |
| URLs | 1 URL for everything | Separate URLs |

## 🛠️ Customization

### Environment Variables
Set in Cloud Run service:
- `NODE_ENV=production`
- Add your own env vars as needed

### Memory and CPU
Adjust in `cloudbuild-unified.yaml`:
```yaml
- '--memory=2Gi'     # Increase if needed
- '--cpu=1'          # Increase for more power
```

### Build Configuration
Modify `Dockerfile` to:
- Change Python or Node.js versions
- Add additional dependencies
- Customize build process

## 🚨 Troubleshooting

**Build fails:**
- Check Docker syntax in `Dockerfile`
- Verify all file paths are correct
- Check Cloud Build logs

**Static files not loading:**
- Ensure `next.config.js` has `output: 'export'`
- Check static file paths in FastAPI

**API calls failing:**
- Verify API routes in `main.py`
- Check frontend API base URL configuration

## 📚 Next Steps

- Set up monitoring and logging
- Configure custom domain
- Add environment-specific configurations
- Set up CI/CD pipeline with GitHub Actions 