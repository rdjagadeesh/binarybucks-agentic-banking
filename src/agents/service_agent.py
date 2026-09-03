from pathlib import Path

from src.config.llm_config import safe_generate
from src.prompts.system_prompts import BINARYBUCKS_SYSTEM_PROMPT


def handle_service_query(user_query: str, customer_id: str, memory_text: str) -> str:
    try:
        faq_path = Path(__file__).resolve().parents[2] / "docs" / "banking_faq.md"
        faq_text = faq_path.read_text(encoding="utf-8")[:600]
    except OSError:
        faq_text = "FAQ unavailable."

    contents = [
        {
            "role": "user",
            "parts": [
                {"text": BINARYBUCKS_SYSTEM_PROMPT},
                {"text": "[Agent: SERVICE]"},
                {"text": f"[CustomerID] {customer_id}"},
                {"text": f"[Memory]\n{memory_text[-400:]}"},
                {"text": f"[Knowledge]\n{faq_text}"},
                {"text": f"Service request: {user_query}"},
                {"text": "Answer the exact service question directly and provide the safest next step."},
            ],
        }
    ]
    query = user_query.lower()
    if "demat" in query:
        fallback = (
            "Your CUST001 simulated profile has no demat account, so there is no demat "
            "account number to display. BinaryBucks cannot access a real brokerage account. "
            "For a real demat account, use the official website or app of a regulated broker "
            "or bank and complete its identity-verification process."
        )
    else:
        fallback = (
            "In this simulated demo, KYC verification is not required. For a real change to "
            "your KYC details, use your bank's official app or branch process and provide "
            "the requested identity documents. Never share passwords or one-time passcodes."
        )
    return safe_generate(contents, fallback)
