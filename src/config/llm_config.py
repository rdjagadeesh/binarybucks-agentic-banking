import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL_NAME = "gemini-3.6-flash"  # change once, used everywhere
API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

_client = None

def get_llm_client():
    global _client
    if _client is None:
        _client = genai.Client(api_key=API_KEY)
    return _client
