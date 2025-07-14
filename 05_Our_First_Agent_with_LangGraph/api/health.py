#!/usr/bin/env python3
"""
Health check endpoint for Vercel serverless function
"""

import json

def handler(request, context):
    """Simple health check handler"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        },
        'body': json.dumps({
            'status': 'healthy',
            'message': 'Space Exploration Agent API is running'
        })
    } 