#!/usr/bin/env python3
"""
Vercel entry point for the Space Exploration Agent API
"""

import sys
import os

# Add both the parent directory and current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, current_dir)

# Import the FastAPI app and Mangum handler from main.py
from main import handler

# Export the Mangum-wrapped handler for Vercel
# This is the proper ASGI handler that Vercel expects
handler = handler 