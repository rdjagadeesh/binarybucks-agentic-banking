import os
from dotenv import load_dotenv
from src.config.llm_config import get_llm_client, MODEL_NAME
from src.prompts.system_prompts import BINARYBUCKS_SYSTEM_PROMPT
from src.tools.bank_tools import assess_mock_risk

load_dotenv()
client = get_llm_client()


def handle_risk_query(user_query: str, customer_id: str, memory_text: str) -> str:
    # Load FAQ / RAG-style knowledge
    try:
        with open("docs/banking_faq.md", "r", encoding="utf-8") as f:
            faq_text = f.read()
    except Exception:
        faq_text = "FAQ data not available in this simulated environment."

    # Tool: simulated risk scoring
    amount = 6000  # demo value; could be parsed from text later
    country = "us"
    risk_level = assess_mock_risk(amount, country)

    tool_output_text = f"""
    [Tool: RISK]
    - Transaction Amount: {amount}
    - Country: {country}
    - Assessed Risk Level: {risk_level}
    """

    if risk_level == "high":
        human_message = (
            "This case is assessed as HIGH RISK in the simulated model. "
            "BinaryBucks cannot make final fraud or liability decisions. "
            "This must be escalated to a human fraud specialist in a real banking environment."
        )
    else:
        human_message = (
            "This case is not classified as high risk in the simulated model, "
            "but BinaryBucks still recommends contacting your bank for confirmation."
        )

    contents = [
        {
            "role": "user",
            "parts": [
                {"text": BINARYBUCKS_SYSTEM_PROMPT},
                {"text": "[Agent: RISK]"},
                {"text": f"[CustomerID] {customer_id}"},
                {"text": f"[Memory]\n{memory_text}"},
                {"text": f"[Knowledge]\n{faq_text[:3000]}"},
                {"text": tool_output_text},
                {"text": human_message},
                {"text": "[LLM: BEGIN]"},
                {"text": f"Risk issue: {user_query}"}
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
            "BinaryBucks encountered an issue while generating a risk-related response. "
            "This is a simulated environment; please try again later."
        )
