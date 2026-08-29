import os
from dotenv import load_dotenv
from src.config.llm_config import get_llm_client, MODEL_NAME
from src.prompts.system_prompts import BINARYBUCKS_SYSTEM_PROMPT
from src.tools.bank_tools import get_mock_customer_profile

load_dotenv()
client = get_llm_client()


def handle_account_query(user_query: str, customer_id: str, memory_text: str) -> str:
    # Load FAQ / RAG-style knowledge
    try:
        with open("docs/banking_faq.md", "r", encoding="utf-8") as f:
            faq_text = f.read()
    except Exception:
        faq_text = "FAQ data not available in this simulated environment."

    # Tool: simulated customer profile
    profile = get_mock_customer_profile(customer_id)

    tool_output_text = f"""
    [Tool: PROFILE]
    - ID: {profile.get('customer_id')}
    - Segment: {profile.get('segment')}
    - Risk Rating: {profile.get('risk_rating')}
    - Accounts: {profile.get('accounts')}
    """

    contents = [
        {
            "role": "user",
            "parts": [
                {"text": BINARYBUCKS_SYSTEM_PROMPT},
                {"text": "[Agent: ACCOUNT]"},
                {"text": f"[CustomerID] {customer_id}"},
                {"text": f"[Memory]\n{memory_text}"},
                {"text": f"[Knowledge]\n{faq_text[:3000]}"},
                {"text": tool_output_text},
                {"text": "[LLM: BEGIN]"},
                {"text": f"Account issue: {user_query}"}
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
            "BinaryBucks encountered an issue while generating a response. "
            "This is a simulated environment; please try again later."
        )
