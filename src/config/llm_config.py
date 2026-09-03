import os
import logging
from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

_client = None
logger = logging.getLogger(__name__)

def get_llm_client():
    global _client
    if _client is None:
        if not API_KEY:
            logger.warning("Gemini client unavailable: API key is not configured")
            return None
        _client = genai.Client(api_key=API_KEY)
    return _client

def safe_generate(contents, fallback: str) -> str:
    try:
        client = get_llm_client()
        if client is None:
            return fallback
        resp = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents
        )
        return (resp.text or "").strip() or fallback
    except Exception as exc:
        logger.warning("Gemini request failed (%s): %s", type(exc).__name__, str(exc)[:300])
        return fallback
