"""
Centralized Configuration
All agents must import MODEL_NAME from this file
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MODEL_NAME = "gpt-4o-mini"  # Centralized model configuration

# Model Parameters
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 500

# Validation
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")
