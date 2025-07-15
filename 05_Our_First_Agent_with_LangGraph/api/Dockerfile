# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY api/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the API code (including space_exploration_agent.py)
COPY api/ .

# Expose port
EXPOSE 8080

# Set environment variables for Cloud Run
ENV HOST=0.0.0.0
ENV PORT=8080

# Run the application
CMD exec uvicorn main:app --host $HOST --port $PORT --workers 1 