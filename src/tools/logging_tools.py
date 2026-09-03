import datetime
import re
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parents[2] / "binarybucks_audit.log"
SENSITIVE_PATTERNS = [
    (re.compile(r"(?i)\b(?:pin|password|passcode|otp|one[- ]time password)\b\s*[:=]?\s*\S+"), "[REDACTED_SECRET]"),
    (re.compile(r"\b\d{12,19}\b"), "[REDACTED_ACCOUNT_NUMBER]"),
]


def _redact(value: str) -> str:
    for pattern, replacement in SENSITIVE_PATTERNS:
        value = pattern.sub(replacement, value)
    return value.replace("\r", " ").replace("\n", " ").replace("|", "/")

def log_interaction(agent_name: str, user_query: str, answer: str):
    timestamp = datetime.datetime.utcnow().isoformat()
    line = f"{timestamp} | {_redact(agent_name)} | {_redact(user_query)} | {_redact(answer)}\n"
    try:
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(line)
    except OSError:
        pass
