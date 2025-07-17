#!/usr/bin/env python3
"""
Teambee Application Entry Point

This is the main entry point for the Teambee application.
"""

import logging
from main import app
from app.config import config
from fasthtml.common import serve

def configure_logging():
    """Configure logging levels to reduce noise while keeping important information."""
    
    # Keep uvicorn logs at INFO level (for request logs)
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    
    # Keep other FastHTML related logs at INFO
    logging.getLogger("fasthtml").setLevel(logging.INFO)

if __name__ == "__main__":
    # Configure logging to reduce noise
    configure_logging()
    
    # Start the FastHTML server
    serve(host=config.HOST, port=config.PORT) 