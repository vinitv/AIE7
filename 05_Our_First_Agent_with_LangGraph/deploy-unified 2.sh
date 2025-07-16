#!/bin/bash

# Deploy script for unified Space Exploration Agent
# Deploys both frontend and backend as a single Cloud Run service

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    print_error "gcloud CLI is not installed. Please install it first."
    exit 1
fi

# Get project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    print_error "No Google Cloud project set. Run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

print_status "Using Google Cloud Project: $PROJECT_ID"

# Enable required APIs
print_status "Enabling required Google Cloud APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and deploy using Cloud Build
print_status "Starting Cloud Build for unified service..."
gcloud builds submit --config=cloudbuild-unified.yaml .

# Get the service URL
SERVICE_URL=$(gcloud run services describe space-agent-unified --region=us-central1 --format="value(status.url)")

if [ ! -z "$SERVICE_URL" ]; then
    print_success "Deployment completed successfully!"
    print_success "Your Space Exploration Agent is available at:"
    echo -e "${BLUE}${SERVICE_URL}${NC}"
    echo ""
    print_status "API endpoints available at:"
    echo -e "  Health Check: ${SERVICE_URL}/health"
    echo -e "  Test Keys: ${SERVICE_URL}/api/test-keys"
    echo -e "  Ask Question: ${SERVICE_URL}/ask"
    echo ""
    print_warning "Don't forget to set your API keys in the frontend at:"
    echo -e "  ${SERVICE_URL}/setup"
else
    print_error "Failed to get service URL. Please check the Cloud Build logs."
    exit 1
fi 