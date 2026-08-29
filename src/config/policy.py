GUARDRAIL_TRANSFER_KEYWORDS = [
    "transfer", "send money", "move funds", "wire", "swift"
]

GUARDRAIL_FRAUD_KEYWORDS = [
    "fraud", "unauthorized", "suspicious", "risk", "chargeback",
    "illegal", "scam", "dispute", "stolen", "hacked"
]

def is_transfer_request(text: str) -> bool:
    q = text.lower()
    return any(word in q for word in GUARDRAIL_TRANSFER_KEYWORDS)

def is_fraud_request(text: str) -> bool:
    q = text.lower()
    return any(word in q for word in GUARDRAIL_FRAUD_KEYWORDS)
