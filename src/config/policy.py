from src.config.llm_config import get_llm_client, MODEL_NAME

GUARDRAIL_TRANSFER_KEYWORDS = [
    "transfer", "send money", "move funds", "wire", "swift"
]

GUARDRAIL_FRAUD_KEYWORDS = [
    "fraud", "unauthorized", "suspicious", "risk", "chargeback",
    "illegal", "scam", "dispute", "stolen", "hacked"
]

SENSITIVE_INFO_KEYWORDS = [
    "pin", "password", "otp", "one-time", "passcode"
]

UNSUPPORTED_TOPIC_KEYWORDS = [
    "share market", "stock market", "stocks", "shares", "mutual fund",
    "mutual funds", "investing", "investment", "trading", "forex",
    "crypto", "cryptocurrency", "ipo"
]

def is_transfer_request(text: str) -> bool:
    q = text.lower()
    return any(word in q for word in GUARDRAIL_TRANSFER_KEYWORDS)

def is_fraud_request(text: str) -> bool:
    q = text.lower()
    return any(word in q for word in GUARDRAIL_FRAUD_KEYWORDS)


def authenticate_customer(customer_id: str) -> bool:
    """Simulated identity provider: only the demo customer is authenticated."""
    return customer_id == "CUST001"


def authorize_customer(requested_customer_id: str, authenticated_customer_id: str) -> bool:
    """Simulated ownership check at the tool boundary."""
    return requested_customer_id == authenticated_customer_id

def apply_guardrails(text: str) -> str | None:
    q = text.lower()

    if any(w in q for w in SENSITIVE_INFO_KEYWORDS):
        return "For your security, please do not share PINs, passwords, or one‑time passcodes."

    if is_transfer_request(q):
        return (
            "For safety reasons, BinaryBucks cannot perform or simulate real money transfers. "
            "Please contact your bank directly using official channels."
        )

    if any(word in q for word in UNSUPPORTED_TOPIC_KEYWORDS):
        return (
            "That topic is outside BinaryBucks support. I can help with simulated accounts, "
            "cards, transactions, KYC requests, and suspicious activity. For investment or "
            "share-market guidance, use a regulated financial adviser or official provider."
        )

    return None


def validate_model_response(response: str) -> str | None:
    """Reject model output that claims an unsafe action or exposes internals."""
    lowered = response.lower()
    forbidden = [
        "[customer context]", "[recent simulated transactions]", "[faq knowledge]",
        "[conversation memory]", "[customer question]", "api key", "system prompt",
    ]
    if any(marker in lowered for marker in forbidden):
        return "I cannot provide that response safely. Please contact official bank channels."
    if any(phrase in lowered for phrase in [
        "i have transferred", "transfer completed", "your card has been blocked",
        "refund has been issued", "chargeback has been processed",
    ]):
        return "I cannot perform financial actions in this simulated environment. Please contact official bank channels."
    return None

def classify_intent(query: str) -> str:
    q = query.lower()
    if any(word in q for word in ["kyc", "know your customer", "demat", "service request", "change my details", "change my information"]):
        return "service"
    if any(word in q for word in ["fraud", "unauthorized", "suspicious", "invalid transaction", "unrecognized", "scam", "stolen", "hacked"]):
        return "risk"
    if any(word in q for word in ["card", "credit", "debit", "atm", "cash withdrawal"]):
        return "card"
    if any(word in q for word in ["transaction", "transactions", "transcation", "transcations", "statement", "payment history", "purchase history"]):
        return "transaction"
    if any(word in q for word in ["balance", "account", "savings", "savings account", "current account", "open an account"]):
        return "account"

    client = get_llm_client()
    if client is None:
        return "account"
    prompt = (
        "Classify this request as exactly one of: account, card, transaction, risk, service, "
        "or unknown. Use unknown when it is outside simulated banking support.\n"
        f"User: {query}\nAnswer with one word."
    )
    try:
        resp = client.models.generate_content(
            model=MODEL_NAME,
            contents=[{"text": prompt}]
        )
        intent = resp.text.strip().lower()
    except Exception:
        return "unknown"

    if intent not in ["account", "card", "transaction", "risk", "service", "unknown"]:
        return "unknown"
    return intent
