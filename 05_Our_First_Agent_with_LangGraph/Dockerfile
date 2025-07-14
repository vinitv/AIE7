# Multi-stage build for unified Next.js + FastAPI service
FROM node:18-alpine AS frontend-builder

# Build the Next.js frontend for static export
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci

# Copy frontend source and build for static export
COPY frontend/ ./
RUN npm run build

# Python backend stage
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies for Python
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements
COPY api/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY api/ ./
COPY space_exploration_agent.py ./

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/out ./static

# Expose port
EXPOSE 8080

# Set environment variables for Cloud Run
ENV HOST=0.0.0.0
ENV PORT=8080
ENV NODE_ENV=production

# Run the unified application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"] 