import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Directory to store generated images
IMAGE_IA_DIR = os.getenv("IMAGE_IA_DIR", "/app/files/ia/")

IMAGE_WORDCLOUD_DIR = os.getenv("IMAGE_WORDCLOUD_DIR", "/app/files/wordcloud/")

STATE_DIR = os.getenv("STATE_DIR", "/app/files/state.txt")

SERVE_IMAGE = os.getenv("SERVE_IMAGE", "http://localhost:8000")