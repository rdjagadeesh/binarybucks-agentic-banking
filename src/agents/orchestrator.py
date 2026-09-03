from src.agents.account_agent import handle_account_query
from src.agents.card_agent import handle_card_query
from src.agents.risk_agent import handle_risk_query
from src.agents.transaction_agent import handle_transaction_query
from src.agents.service_agent import handle_service_query
from src.tools.logging_tools import log_interaction
from src.config.policy import (
    apply_guardrails,
    authenticate_customer,
    authorize_customer,
    is_fraud_request,
    is_transfer_request,
    classify_intent,
    validate_model_response,
)


def route_request(user_query: str, customer_id: str, memory_text: str) -> str:
    q = user_query.lower()

    guardrail = apply_guardrails(q)
    if guardrail:
        log_interaction("GUARDRAIL", user_query, guardrail)
        return guardrail

    if not authenticate_customer(customer_id) or not authorize_customer(customer_id, customer_id):
        answer = "This simulated session is not authorized for that customer profile."
        log_interaction("AUTHORIZATION_DENIED", user_query, answer)
        return answer

    if is_transfer_request(q):
        answer = "For safety reasons, BinaryBucks cannot perform or simulate real money transfers. Please contact official bank channels."
        log_interaction("GUARDRAIL", user_query, answer)
        return answer

    if is_fraud_request(q):
        agent_name, answer = "RISK", handle_risk_query(user_query, customer_id, memory_text)
    else:
        intent = classify_intent(user_query)
        handlers = {
            "account": ("ACCOUNT", handle_account_query),
            "card": ("CARD", handle_card_query),
            "risk": ("RISK", handle_risk_query),
            "transaction": ("TRANSACTION", handle_transaction_query),
            "service": ("SERVICE", handle_service_query),
        }
        agent_name, handler = handlers.get(intent, ("ACCOUNT", handle_account_query))
        answer = handler(user_query, customer_id, memory_text)

    safe_answer = validate_model_response(answer)
    if safe_answer:
        answer = safe_answer
        agent_name = "OUTPUT_GUARDRAIL"
    log_interaction(agent_name, user_query, answer)
    return answer
