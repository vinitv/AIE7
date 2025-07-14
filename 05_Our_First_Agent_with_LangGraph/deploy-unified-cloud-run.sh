#!/bin/bash

# Deploy Unified Space Exploration Agent to Cloud Run
# This script builds and deploys both frontend and backend as a single service

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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
    print_error "No Google Cloud project configured. Please run 'gcloud config set project YOUR_PROJECT_ID'"
    exit 1
fi

print_status "Using project: $PROJECT_ID"

# Build the frontend first
print_status "Building frontend..."
cd frontend
npm run build
cd ..

# Copy static files to backend (for local testing)
print_status "Copying static files to backend..."
rm -rf api/static
cp -r frontend/out api/static

# Build and deploy using Cloud Build
print_status "Building and deploying to Cloud Run..."
gcloud builds submit --config cloudbuild-unified.yaml .

print_success "Deployment completed!"
print_status "Your unified service should be available at the URL shown above."
print_status "The service serves both the frontend and API from a single Cloud Run instance." 