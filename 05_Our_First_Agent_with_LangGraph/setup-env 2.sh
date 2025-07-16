#!/bin/bash

# Space Exploration Agent - Environment Setup Script for Cloud Run

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID="${GOOGLE_CLOUD_PROJECT:-$(gcloud config get-value project)}"
REGION="us-central1"
BACKEND_SERVICE="space-agent-backend"

echo -e "${BLUE}🔐 Space Exploration Agent - Environment Setup${NC}"
echo -e "${BLUE}This script will help you set up API keys for your Cloud Run deployment${NC}"

# Function to prompt for API key
prompt_for_key() {
    local key_name=$1
    local key_description=$2
    local is_optional=$3
    
    echo -e "\n${YELLOW}Setting up ${key_name}${NC}"
    echo -e "${BLUE}${key_description}${NC}"
    
    if [ "$is_optional" = "true" ]; then
        echo -e "${YELLOW}(Optional - press Enter to skip)${NC}"
    fi
    
    read -p "Enter your ${key_name}: " key_value
    
    if [ -n "$key_value" ]; then
        echo "$key_value"
    elif [ "$is_optional" = "true" ]; then
        echo "DEMO_KEY"
    else
        echo ""
    fi
}

# Collect API keys
echo -e "\n${BLUE}📝 Please provide your API keys:${NC}"

OPENAI_KEY=$(prompt_for_key "OpenAI API Key" "Required for GPT-4 and DALL-E image generation. Get it from: https://platform.openai.com/api-keys" "false")

if [ -z "$OPENAI_KEY" ]; then
    echo -e "${RED}❌ OpenAI API Key is required. Exiting.${NC}"
    exit 1
fi

TAVILY_KEY=$(prompt_for_key "Tavily API Key" "Required for web search functionality. Get it from: https://tavily.com" "false")

if [ -z "$TAVILY_KEY" ]; then
    echo -e "${RED}❌ Tavily API Key is required. Exiting.${NC}"
    exit 1
fi

NASA_KEY=$(prompt_for_key "NASA API Key" "Optional for NASA data access. Get it from: https://api.nasa.gov/" "true")

LANGSMITH_KEY=$(prompt_for_key "LangSmith API Key" "Optional for tracing and monitoring. Get it from: https://smith.langchain.com/" "true")

# Set environment variables in Cloud Run
echo -e "\n${YELLOW}🚀 Setting environment variables in Cloud Run...${NC}"

ENV_VARS="OPENAI_API_KEY=${OPENAI_KEY},TAVILY_API_KEY=${TAVILY_KEY},NASA_API_KEY=${NASA_KEY}"

if [ "$LANGSMITH_KEY" != "DEMO_KEY" ] && [ -n "$LANGSMITH_KEY" ]; then
    ENV_VARS="${ENV_VARS},LANGCHAIN_API_KEY=${LANGSMITH_KEY}"
fi

gcloud run services update $BACKEND_SERVICE \
    --region=$REGION \
    --set-env-vars="$ENV_VARS" \
    --quiet

echo -e "${GREEN}✅ Environment variables updated successfully!${NC}"

# Get service URL
FRONTEND_URL=$(gcloud run services describe space-agent-frontend --region=$REGION --format="value(status.url)" 2>/dev/null || echo "Not deployed yet")

echo -e "\n${GREEN}🎉 Setup completed!${NC}"
if [ "$FRONTEND_URL" != "Not deployed yet" ]; then
    echo -e "${GREEN}🌐 Your Space Exploration Agent is ready at: ${FRONTEND_URL}${NC}"
else
    echo -e "${YELLOW}📋 Run ./deploy.sh to deploy your application${NC}"
fi

echo -e "\n${BLUE}💡 Pro Tips:${NC}"
echo -e "• You can update environment variables anytime using this script"
echo -e "• For production, consider using Google Secret Manager for sensitive keys"
echo -e "• Monitor your usage and costs in the Google Cloud Console" 