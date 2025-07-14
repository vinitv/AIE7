#!/usr/bin/env python3
"""
Vercel serverless function for the /ask endpoint
"""

import os
import sys
import json
from typing import Optional

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, current_dir)

# Import agent functions
from space_exploration_agent import create_agent_with_keys, convert_inputs, parse_output, get_tools_used, reset_tools_tracking

def handler(request, context):
    """Handle /ask endpoint requests"""
    
    # Handle CORS preflight
    if request.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            },
            'body': ''
        }
    
    try:
        # Parse request body
        if isinstance(request.get('body'), str):
            body = json.loads(request['body'])
        else:
            body = request.get('body', {})
        
        question = body.get('question', '')
        if not question:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({
                    'response': 'Question is required',
                    'status': 'error',
                    'tool_used': 'none'
                })
            }
        
        # Reset tools tracking for this request
        reset_tools_tracking()
        
        # Get API keys from request or environment
        openai_key = body.get('openai_api_key') or os.getenv("OPENAI_API_KEY")
        tavily_key = body.get('tavily_api_key') or os.getenv("TAVILY_API_KEY") or "DEMO_KEY"
        nasa_key = body.get('nasa_api_key') or os.getenv("NASA_API_KEY") or "DEMO_KEY"
        
        if not openai_key:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps({
                    'response': 'OpenAI API key is required',
                    'status': 'error',
                    'tool_used': 'none'
                })
            }
        
        # Create agent with provided API keys - returns (workflow, tools)
        workflow, tools = create_agent_with_keys(
            openai_api_key=openai_key,
            tavily_api_key=tavily_key,
            nasa_api_key=nasa_key
        )
        
        # Convert inputs and process question
        converted_input = convert_inputs({"question": question})
        
        # Run the agent workflow
        result = workflow.invoke(converted_input)
        
        # Parse the output
        parsed_result = parse_output(result)
        
        # Get actual tools used from workflow tracking
        tools_used = get_tools_used()
        if not tools_used:
            tool_used = "No tools used"
        elif len(tools_used) == 1:
            tool_used = tools_used[0]
        else:
            tool_used = ", ".join(tools_used)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({
                'response': parsed_result,
                'status': 'success',
                'tool_used': tool_used
            })
        }
        
    except Exception as e:
        print(f"Error processing question: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            'body': json.dumps({
                'response': f'Sorry, I encountered an error: {str(e)}',
                'status': 'error',
                'tool_used': 'none'
            })
        } 