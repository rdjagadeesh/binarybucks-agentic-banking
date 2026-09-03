import os
from pathlib import Path
from dotenv import load_dotenv
from src.config.llm_config import safe_generate
from src.prompts.system_prompts import BINARYBUCKS_SYSTEM_PROMPT

load_dotenv()

def handle_card_query(user_query: str, customer_id: str, memory_text: str) -> str:
    try:
        faq_path = Path(__file__).resolve().parents[2] / "docs" / "banking_faq.md"
        with faq_path.open("r", encoding="utf-8") as f:
            faq_text = f.read()[:600]
    except Exception:
        faq_text = "FAQ unavailable."

    contents = [
        {
            "role": "user",
            "parts": [
                {"text": BINARYBUCKS_SYSTEM_PROMPT},
                {"text": "[Agent: CARD]"},
                {"text": f"[CustomerID] {customer_id}"},
                {"text": f"[Memory]\n{memory_text[-400:]}"},
                {"text": f"[Knowledge]\n{faq_text}"},
                {"text": f"Card issue: {user_query}"},
                {"text": "Write a direct, empathetic answer with practical next steps."}
            ]
        }
    ]

    query = user_query.lower()
    if "limit" in query or "increase" in query or "increased" in query:
        fallback = (
            "Your simulated card has a current credit limit of EUR 5,000. A higher limit "
            "requires an eligibility review, and this demo cannot change or approve it. "
            "Contact official bank channels to submit a real request."
        )
    elif "declined" in query or "decline" in query:
        fallback = (
            "I’m sorry your card payment was declined. Please check the available balance, "
            "card expiry, and whether the merchant supports this card. If it continues, "
            "contact official bank channels for a review."
        )
    else:
        fallback = (
            "I can help with a simulated card issue. Tell me whether the card was declined, "
            "lost, or charged unexpectedly. Never share your PIN or passcodes, and contact "
            "official bank channels for a real card issue."
        )
    return safe_generate(contents, fallback)
