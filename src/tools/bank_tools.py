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


def get_mock_recent_transactions(customer_id: str, limit: int = 4):
    return [
        {"date": "2026-08-31", "merchant": "Northstar Market", "amount": 64.20, "status": "Completed"},
        {"date": "2026-08-30", "merchant": "Metro Transit", "amount": 18.50, "status": "Completed"},
        {"date": "2026-08-29", "merchant": "Cloudline Utilities", "amount": 92.00, "status": "Completed"},
        {"date": "2026-08-28", "merchant": "Harbor Coffee", "amount": 7.80, "status": "Completed"},
        {"date": "2026-08-27", "merchant": "Greenfield Pharmacy", "amount": 31.45, "status": "Completed"},
        {"date": "2026-08-26", "merchant": "City Bikes", "amount": 12.00, "status": "Completed"},
        {"date": "2026-08-25", "merchant": "Pine Telecom", "amount": 45.00, "status": "Completed"},
        {"date": "2026-08-24", "merchant": "Lighthouse Books", "amount": 27.90, "status": "Completed"},
        {"date": "2026-08-23", "merchant": "Oak Street Bakery", "amount": 9.60, "status": "Completed"},
        {"date": "2026-08-22", "merchant": "River Fuel", "amount": 58.30, "status": "Completed"},
    ][:limit]
