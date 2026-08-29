from src.agents.account_agent import handle_account_query
from src.agents.card_agent import handle_card_query
from src.agents.risk_agent import handle_risk_query
from src.tools.logging_tools import log_interaction
from src.config.policy import is_transfer_request, is_fraud_request


def route_request(user_query: str, customer_id: str, memory_text: str) -> str:
    q = user_query.lower()

    # Guardrail: transfers and money movement
    if is_transfer_request(q):
        answer = (
            "For safety reasons, BinaryBucks cannot perform or simulate real money transfers. "
            "Please contact your bank directly using official channels."
        )
        log_interaction("GUARDRAIL", user_query, answer)
        return answer

    # Fraud / risk routing
    if is_fraud_request(q):
        answer = handle_risk_query(user_query, customer_id, memory_text)
        log_interaction("RISK", user_query, answer)
        return answer

    # Card-related routing
    if any(word in q for word in ["card", "credit", "debit", "lost card", "block card", "atm"]):
        answer = handle_card_query(user_query, customer_id, memory_text)
        log_interaction("CARD", user_query, answer)
        return answer

    # Default: account agent
    answer = handle_account_query(user_query, customer_id, memory_text)
    log_interaction("ACCOUNT", user_query, answer)
    return answer
