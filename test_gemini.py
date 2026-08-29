import os

from google import genai

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")


def build_client():
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "API key is missing. Set GOOGLE_API_KEY or GEMINI_API_KEY in your environment "
            "or in a .env file before running this demo."
        )
    return genai.Client(api_key=api_key)


def ask_gemini(question: str) -> str:
    client = build_client()
    prompt = f"""
    You are a beginner-friendly banking assistant for a fictional bank named BinaryBucks.
    Use only the information provided in the request and do not invent account details.
    Keep the answer concise, professional, and safe.

    User request:
    {question}
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )
    return response.text


if __name__ == "__main__":
    print("BinaryBucks AI test is starting...")
    try:
        answer = ask_gemini("Customer says: My card payment was declined. Give a calm first response.")
        print(answer)
    except RuntimeError as exc:
        print(f"Setup needed: {exc}")
        raise SystemExit(1)
