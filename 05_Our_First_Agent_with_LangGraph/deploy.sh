#!/bin/bash

# Space Exploration Agent - Cloud Run Deployment Script

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
FRONTEND_SERVICE="space-agent-frontend"

echo -e "${BLUE}🚀 Starting Space Exploration Agent deployment to Cloud Run${NC}"
echo -e "${BLUE}Project ID: ${PROJECT_ID}${NC}"
echo -e "${BLUE}Region: ${REGION}${NC}"

# Check if gcloud is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo -e "${RED}❌ Error: Not authenticated with gcloud. Please run: gcloud auth login${NC}"
    exit 1
fi

# Check if required APIs are enabled
echo -e "${YELLOW}🔧 Enabling required APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and deploy using Cloud Build
echo -e "${YELLOW}🔨 Building and deploying services...${NC}"
gcloud builds submit --config cloudbuild.yaml .

# Get service URLs
echo -e "${YELLOW}📡 Getting service URLs...${NC}"
BACKEND_URL=$(gcloud run services describe $BACKEND_SERVICE --region=$REGION --format="value(status.url)")
FRONTEND_URL=$(gcloud run services describe $FRONTEND_SERVICE --region=$REGION --format="value(status.url)")

# Update frontend with backend URL
echo -e "${YELLOW}🔗 Updating frontend with backend URL...${NC}"
gcloud run services update $FRONTEND_SERVICE \
    --region=$REGION \
    --set-env-vars="API_URL=${BACKEND_URL}"

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo -e "${GREEN}🌐 Frontend URL: ${FRONTEND_URL}${NC}"
echo -e "${GREEN}🔧 Backend URL: ${BACKEND_URL}${NC}"

echo -e "\n${BLUE}📋 Next steps:${NC}"
echo -e "1. Set your API keys as environment variables in Cloud Run:"
echo -e "   ${YELLOW}gcloud run services update $BACKEND_SERVICE --region=$REGION --set-env-vars=\"OPENAI_API_KEY=your-key,TAVILY_API_KEY=your-key,NASA_API_KEY=your-key\"${NC}"
echo -e "2. Visit your application at: ${GREEN}${FRONTEND_URL}${NC}"
echo -e "3. Configure your API keys in the UI or set them as environment variables"

echo -e "\n${BLUE}🔐 Security Note:${NC}"
echo -e "Remember to set your API keys as environment variables for production use!" 