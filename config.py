"""
Centralized Configuration
All agents must import MODEL_NAME and API configuration from this file
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration - Switch between OpenAI and OpenRouter
USE_OPENROUTER = True  # Set to True to use OpenRouter (free), False for OpenAI

if USE_OPENROUTER:
    # OpenRouter Configuration (FREE)
    API_KEY = os.getenv('OPENROUTER_API_KEY')
    API_BASE = "https://openrouter.ai/api/v1"
    MODEL_NAME = "google/gemini-flash-1.5-8b"  # Free model on OpenRouter
    
    if not API_KEY:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables. Get one free at https://openrouter.ai/keys")
else:
    # OpenAI Configuration (PAID)
    API_KEY = os.getenv('OPENAI_API_KEY')
    API_BASE = "https://api.openai.com/v1"
    MODEL_NAME = "gpt-4o-mini"
    
    if not API_KEY:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

# Model Parameters
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 500

# Legacy support (for backward compatibility)
OPENAI_API_KEY = API_KEY
