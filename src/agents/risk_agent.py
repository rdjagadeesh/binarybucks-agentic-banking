import os
from pathlib import Path
from dotenv import load_dotenv
from src.config.llm_config import safe_generate
from src.prompts.system_prompts import BINARYBUCKS_SYSTEM_PROMPT
from src.tools.bank_tools import assess_mock_risk

load_dotenv()

def handle_risk_query(user_query: str, customer_id: str, memory_text: str) -> str:
    try:
        faq_path = Path(__file__).resolve().parents[2] / "docs" / "banking_faq.md"
        with faq_path.open("r", encoding="utf-8") as f:
            faq_text = f.read()[:600]
    except Exception:
        faq_text = "FAQ unavailable."

    amount = 6000
    country = "us"
    risk_level = assess_mock_risk(amount, country)

    tool_output_text = (
        f"[Tool: RISK]\n"
        f"Amount: {amount}\n"
        f"Country: {country}\n"
        f"RiskLevel: {risk_level}"
    )

    human_message = (
        "High risk detected. Escalation recommended."
        if risk_level == "high"
        else "Not high risk, but verification recommended."
    )

    contents = [
        {
            "role": "user",
            "parts": [
                {"text": BINARYBUCKS_SYSTEM_PROMPT},
                {"text": "[Agent: RISK]"},
                {"text": f"[CustomerID] {customer_id}"},
                {"text": f"[Memory]\n{memory_text[-400:]}"},
                {"text": f"[Knowledge]\n{faq_text}"},
                {"text": tool_output_text},
                {"text": human_message},
                {"text": f"Risk issue: {user_query}"},
                {"text": "Write a calm, urgent answer and clearly explain the human-review next step."}
            ]
        }
    ]

    fallback = (
        f"This simulated review classified the example as {risk_level} risk. "
        "Because the request involves suspicious or potentially unauthorized activity, "
        "please contact official bank channels immediately and ask for human review. "
        "Do not share passwords, PINs, or one-time passcodes."
    )
    return safe_generate(contents, fallback)
