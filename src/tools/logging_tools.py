import datetime

def log_interaction(agent_name: str, user_query: str, answer: str):
    timestamp = datetime.datetime.utcnow().isoformat()
    line = f"{timestamp} | {agent_name} | {user_query} | {answer}\n"

    with open("binarybucks_audit.log", "a", encoding="utf-8") as f:
        f.write(line)

