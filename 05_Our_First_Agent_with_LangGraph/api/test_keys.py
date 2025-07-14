#!/usr/bin/env python3
"""
API endpoint to test API keys
"""

import os
import sys
from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

router = APIRouter()

class APIKeysRequest(BaseModel):
    openai: str
    tavily: str
    nasa: str = "DEMO_KEY"

class APIKeysResponse(BaseModel):
    status: str
    message: str
    details: Dict[str, Any] = {}

@router.post("/test-keys", response_model=APIKeysResponse)
async def test_api_keys(request: APIKeysRequest):
    """Test the provided API keys"""
    
    results = {
        "openai": {"valid": False, "message": ""},
        "tavily": {"valid": False, "message": ""},
        "nasa": {"valid": False, "message": ""}
    }
    
    # Test OpenAI API key
    try:
        headers = {
            "Authorization": f"Bearer {request.openai}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 5
            },
            timeout=10
        )
        
        if response.status_code == 200:
            results["openai"]["valid"] = True
            results["openai"]["message"] = "OpenAI API key is valid"
        else:
            results["openai"]["message"] = f"OpenAI API error: {response.status_code}"
            
    except Exception as e:
        results["openai"]["message"] = f"OpenAI API test failed: {str(e)}"
    
    # Test Tavily API key
    try:
        headers = {
            "api-key": request.tavily,
            "content-type": "application/json"
        }
        response = requests.post(
            "https://api.tavily.com/search",
            headers=headers,
            json={
                "query": "test",
                "search_depth": "basic",
                "max_results": 1
            },
            timeout=10
        )
        
        if response.status_code == 200:
            results["tavily"]["valid"] = True
            results["tavily"]["message"] = "Tavily API key is valid"
        else:
            results["tavily"]["message"] = f"Tavily API error: {response.status_code}"
            
    except Exception as e:
        results["tavily"]["message"] = f"Tavily API test failed: {str(e)}"
    
    # Test NASA API key
    try:
        response = requests.get(
            "https://api.nasa.gov/planetary/apod",
            params={"api_key": request.nasa, "count": 1},
            timeout=10
        )
        
        if response.status_code == 200:
            results["nasa"]["valid"] = True
            results["nasa"]["message"] = "NASA API key is valid"
        else:
            results["nasa"]["message"] = f"NASA API error: {response.status_code}"
            
    except Exception as e:
        results["nasa"]["message"] = f"NASA API test failed: {str(e)}"
    
    # Check if required keys are valid
    required_keys_valid = results["openai"]["valid"] and results["tavily"]["valid"]
    
    if required_keys_valid:
        return APIKeysResponse(
            status="success",
            message="All required API keys are valid!",
            details=results
        )
    else:
        # Find which required keys failed
        failed_keys = []
        if not results["openai"]["valid"]:
            failed_keys.append("OpenAI")
        if not results["tavily"]["valid"]:
            failed_keys.append("Tavily")
        
        raise HTTPException(
            status_code=400,
            detail=f"Invalid API keys: {', '.join(failed_keys)}. Please check your keys and try again."
        ) 