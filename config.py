import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenRouter API configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Default model to use
DEFAULT_MODEL = "google/gemini-2.0-pro-exp-02-05:free"

# Application settings
DEBUG = True