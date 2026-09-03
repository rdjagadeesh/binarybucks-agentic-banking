import streamlit as st
from src.agents.orchestrator import route_request

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="BinaryBucks Support", page_icon=":material/account_balance:", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root { --ink:#24170f; --muted:#77685f; --navy:#102a43; --orange:#e85d04; --orange-dark:#bd4600; --paper:#fffaf5; --line:#eadfd6; }
.stApp { background:var(--paper); color:var(--ink); }
[data-testid="stMainBlockContainer"] { max-width:1440px; padding-top:2rem; }
h1,h2,h3,h4,[data-testid="stChatMessage"] p { font-family:'DM Sans',sans-serif; }
h1,h2,h3,h4 { color:var(--ink); }
.brand-mark,.panel-label { color:var(--orange-dark); font-family:'Space Grotesk',sans-serif; font-weight:700; letter-spacing:.1em; text-transform:uppercase; }
.brand-mark { font-size:.74rem; }
.hero-title { color:var(--navy); font-family:'Space Grotesk',sans-serif; font-size:clamp(2rem,4vw,3.6rem); line-height:1.02; margin:.25rem 0 .5rem; }
.hero-copy { color:var(--muted); font-size:1rem; margin-bottom:1.5rem; }
.panel-label { font-size:.73rem; }
.console { background:#fff; border:1px solid var(--line); border-top:5px solid var(--orange); border-radius:10px; padding:1.4rem 1.5rem .7rem; box-shadow:0 12px 30px rgba(92, 52, 24, .06); }
.console-header { display:flex; align-items:center; justify-content:space-between; border-bottom:1px solid #f0e8e1; padding-bottom:1rem; margin-bottom:1rem; }
.bank-name { color:var(--navy); font-family:'Space Grotesk',sans-serif; font-size:1.25rem; font-weight:700; }
.bank-status { color:#277a4d; font-size:.78rem; font-weight:600; }
.bank-status::before { content:' '; display:inline-block; width:8px; height:8px; margin-right:6px; border-radius:50%; background:#3aa76d; }
[data-testid="stChatMessage"] { border:1px solid var(--line); border-left:4px solid var(--orange); border-radius:8px; margin:.65rem 0; padding:.85rem 1rem; background:#fff; }
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p { line-height:1.55; }
[data-testid="stChatInput"] { border-color:var(--orange); }
div.stButton > button { border-radius:6px; border-color:var(--line); color:var(--navy); font-weight:600; }
div.stButton > button:hover { border-color:var(--orange); color:var(--orange-dark); }
div.stButton > button[kind="primary"] { background:var(--orange); border-color:var(--orange); color:#fff; }
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state["history"] = []

def clean_answer(answer):
    markers = ["[Agent: ACCOUNT]", "[Agent: CARD]", "[Agent: RISK]",
               "[Tool: PROFILE]", "[Tool: RISK]", "[LLM: BEGIN]"]
    for marker in markers:
        answer = answer.replace(marker, "")
    return answer.strip()


def submit_query(user_query, customer_id):
    history_text = "\n".join(
        f"{msg['role']}: {msg['content']}" for msg in st.session_state["history"]
    )
    with st.spinner("Reviewing your request..."):
        answer = route_request(user_query, customer_id, history_text)
    st.session_state["history"].extend([
        {"role": "user", "content": user_query},
        {"role": "assistant", "content": clean_answer(answer)},
    ])


st.markdown('<div class="brand-mark">BinaryBucks Bank / digital support</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">How can we help<br>with your banking today?</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-copy">Secure customer support for accounts, cards, and transactions.</div>', unsafe_allow_html=True)

customer_id = "CUST001"

st.markdown('<div class="console">', unsafe_allow_html=True)
st.markdown('<div class="console-header"><span class="bank-name">BinaryBucks Bank</span><span class="bank-status">Support online</span></div>', unsafe_allow_html=True)
st.markdown('<div class="panel-label">Secure conversation</div>', unsafe_allow_html=True)

if not st.session_state["history"]:
    with st.chat_message("assistant", avatar=":material/account_balance:"):
        st.markdown("Welcome to **BinaryBucks Bank support**. Tell me what you need help with, and I’ll guide you through the next step.")
        st.caption("For your security, never share passwords, PINs, or one-time passcodes here.")

for message in st.session_state["history"]:
    role = "user" if message["role"] == "user" else "assistant"
    avatar = ":material/person:" if role == "user" else ":material/account_balance:"
    with st.chat_message(role, avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message to BinaryBucks Bank..."):
    submit_query(prompt, customer_id)
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

if st.session_state["history"] and st.button("Clear conversation", icon=":material/delete_sweep:"):
    st.session_state["history"] = []
    st.rerun()
