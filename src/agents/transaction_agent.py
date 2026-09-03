from pathlib import Path
import re

from src.config.llm_config import safe_generate
from src.prompts.system_prompts import BINARYBUCKS_SYSTEM_PROMPT
from src.tools.bank_tools import get_mock_recent_transactions


def handle_transaction_query(user_query: str, customer_id: str, memory_text: str) -> str:
    try:
        faq_path = Path(__file__).resolve().parents[2] / "docs" / "banking_faq.md"
        faq_text = faq_path.read_text(encoding="utf-8")[:600]
    except OSError:
        faq_text = "FAQ unavailable."

    count_match = re.search(r"\b(?:last|recent)\s+(\d+)\b", user_query.lower())
    requested_count = int(count_match.group(1)) if count_match else 4
    requested_count = max(1, min(requested_count, 10))
    transactions = get_mock_recent_transactions(customer_id, limit=requested_count)
    transaction_text = "\n".join(
        f"{item['date']} | {item['merchant']} | EUR {item['amount']:.2f} | {item['status']}"
        for item in transactions
    )
    contents = [
        {
            "role": "user",
            "parts": [
                {"text": BINARYBUCKS_SYSTEM_PROMPT},
                {"text": "[Agent: TRANSACTION]"},
                {"text": f"[CustomerID] {customer_id}"},
                {"text": f"[Memory]\n{memory_text[-400:]}"},
                {"text": f"[Knowledge]\n{faq_text}"},
                {"text": f"[Tool: TRANSACTIONS]\n{transaction_text}"},
                {"text": f"Transaction request: {user_query}"},
                {"text": "Answer the exact transaction request using the supplied records. Do not invent records."},
            ],
        }
    ]
    formatted_transactions = "\n".join(
        f"- {item['date']}: {item['merchant']} - EUR {item['amount']:.2f} ({item['status']})"
        for item in transactions
    )
    fallback = (
        f"Here are the {len(transactions)} most recent simulated transactions:\n\n"
        f"{formatted_transactions}\n\n"
        "These records are fictional. For an unfamiliar transaction, contact official "
        "bank channels immediately and request human review."
    )
    return safe_generate(contents, fallback)
