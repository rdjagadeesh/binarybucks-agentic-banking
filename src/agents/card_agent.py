import os
from dotenv import load_dotenv
from src.config.llm_config import get_llm_client, MODEL_NAME
from src.prompts.system_prompts import BINARYBUCKS_SYSTEM_PROMPT

load_dotenv()
client = get_llm_client()


def handle_card_query(user_query: str, customer_id: str, memory_text: str) -> str:
    # Load FAQ / RAG-style knowledge
    try:
        with open("docs/banking_faq.md", "r", encoding="utf-8") as f:
            faq_text = f.read()
    except Exception:
        faq_text = "FAQ data not available in this simulated environment."

    contents = [
        {
            "role": "user",
            "parts": [
                {"text": BINARYBUCKS_SYSTEM_PROMPT},
                {"text": "[Agent: CARD]"},
                {"text": f"[CustomerID] {customer_id}"},
                {"text": f"[Memory]\n{memory_text}"},
                {"text": f"[Knowledge]\n{faq_text[:3000]}"},
                {"text": "[LLM: BEGIN]"},
                {"text": f"Card issue: {user_query}"}
            ]
        }
    ]

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents
        )
        return response.text
    except Exception:
        return (
            "BinaryBucks encountered an issue while generating a card-related response. "
            "This is a simulated environment; please try again later."
        )
