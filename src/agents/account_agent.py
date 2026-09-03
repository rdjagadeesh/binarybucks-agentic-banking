import os
from pathlib import Path
from dotenv import load_dotenv
from src.config.llm_config import safe_generate
from src.prompts.system_prompts import BINARYBUCKS_SYSTEM_PROMPT
from src.tools.bank_tools import get_mock_customer_profile

load_dotenv()

def handle_account_query(user_query: str, customer_id: str, memory_text: str) -> str:
    try:
        faq_path = Path(__file__).resolve().parents[2] / "docs" / "banking_faq.md"
        with faq_path.open("r", encoding="utf-8") as f:
            faq_text = f.read()[:600]
    except Exception:
        faq_text = "FAQ unavailable."

    profile = get_mock_customer_profile(customer_id)

    tool_output_text = (
        f"[Tool: PROFILE]\n"
        f"ID: {profile.get('customer_id')}\n"
        f"Segment: {profile.get('segment')}\n"
        f"Risk: {profile.get('risk_rating')}\n"
    )

    contents = [
        {
            "role": "user",
            "parts": [
                {"text": BINARYBUCKS_SYSTEM_PROMPT},
                {"text": "[Agent: ACCOUNT]"},
                {"text": f"[CustomerID] {customer_id}"},
                {"text": f"[Memory]\n{memory_text[-400:]}"},
                {"text": f"[Knowledge]\n{faq_text}"},
                {"text": tool_output_text},
                {"text": "Write a direct, helpful answer to the customer's account question."},
                {"text": f"Account issue: {user_query}"}
            ]
        }
    ]

    query = user_query.lower()
    if "open" in query and "account" in query:
        fallback = (
            "You can open a simulated current or savings account in this demo with no "
            "minimum balance and no KYC verification. In a real bank, use its official app "
            "or branch and complete the required identity checks."
        )
    elif "balance" in query:
        fallback = (
            f"Your simulated current account balance is EUR {profile['accounts'][0]['balance']:,.2f}, "
            f"and your savings balance is EUR {profile['accounts'][1]['balance']:,.2f}. "
            "This is fictional information only."
        )
    else:
        fallback = (
            "I can help with simulated account opening, balances, and account details. "
            "Tell me what you need, and contact official bank channels for real account support."
        )
    return safe_generate(contents, fallback)
