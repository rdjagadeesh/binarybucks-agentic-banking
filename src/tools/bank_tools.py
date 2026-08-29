def get_mock_customer_profile(customer_id: str):
    return {
        "customer_id": customer_id,
        "segment": "retail",
        "risk_rating": "low",
        "accounts": [
            {"type": "current", "balance": 2500},
            {"type": "savings", "balance": 12000}
        ]
    }

def assess_mock_risk(amount: float, country: str):
    if amount > 5000 and country not in ["nl", "de", "fr"]:
        return "high"
    if amount > 1000:
        return "medium"
    return "low"
