import streamlit as st
from src.agents.orchestrator import route_request

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="BinaryBucks Support", layout="wide")

# ---------------------------------------------------------
# BRANDING HEADER
# ---------------------------------------------------------
st.markdown("""
    <div style='text-align:center; padding:20px;'>
        <h1 style='color:#0047AB; font-family:Arial;'>BinaryBucks Virtual Banking Assistant</h1>
        <p style='color:#555;'>Smart. Secure. Simulated Banking Support</p>
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SESSION MEMORY
# ---------------------------------------------------------
if "history" not in st.session_state:
    st.session_state["history"] = []

# ---------------------------------------------------------
# LAYOUT: CHAT LEFT, DASHBOARD RIGHT
# ---------------------------------------------------------
chat_col, profile_col = st.columns([2, 1])

# ---------------------------------------------------------
# CUSTOMER PROFILE DASHBOARD (RIGHT SIDE)
# ---------------------------------------------------------
with profile_col:
    st.markdown("<h3 style='color:#0047AB;'>Customer Overview</h3>", unsafe_allow_html=True)

    customer_id = st.text_input("Customer ID (simulated):", value="CUST001")

    segment = st.selectbox("Segment", ["Retail Banking", "Private Banking", "SME"])
    risk_rating = st.selectbox("Risk Rating", ["Low", "Medium", "High"])
    current_balance = st.number_input("Current Account Balance (€)", value=2500)
    savings_balance = st.number_input("Savings Account Balance (€)", value=12000)

    st.markdown(f"""
        <div style='background-color:#F0F8FF; padding:15px; border-radius:10px; margin-top:10px;'>
            <h4 style='color:#0047AB;'>Profile Snapshot</h4>
            <p><strong>ID:</strong> {customer_id}</p>
            <p><strong>Segment:</strong> {segment}</p>
            <p><strong>Risk Rating:</strong> {risk_rating}</p>
            <p><strong>Current Account:</strong> €{current_balance}</p>
            <p><strong>Savings Account:</strong> €{savings_balance}</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div style='background-color:#FFF8DC; padding:15px; border-radius:10px; margin-top:10px;'>
            <h4 style='color:#0047AB;'>Card Status</h4>
            <p><strong>Debit Card:</strong> Active</p>
            <p><strong>Credit Card:</strong> Active</p>
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# CHAT WINDOW (LEFT SIDE)
# ---------------------------------------------------------
with chat_col:
    st.markdown("<h3 style='color:#0047AB;'>Chat with BinaryBucks</h3>", unsafe_allow_html=True)

    # QUICK ACTION BUTTONS
    st.markdown("**Quick Actions:**")
    col1, col2, col3 = st.columns(3)

    quick_action = None
    if col1.button("Card Issue"):
        quick_action = "I have an issue with my debit or credit card."
    if col2.button("Fraud / Suspicious"):
        quick_action = "I see a suspicious or unauthorized transaction."
    if col3.button("Account Help"):
        quick_action = "I need help with my bank account."

    # USER INPUT
    if quick_action:
        user_query = quick_action
    else:
        user_query = st.text_input("Type your message:")

    # SEND BUTTON
    if st.button("Send"):
        if user_query.strip():
            with st.spinner("BinaryBucks is thinking..."):
                # Build memory text for LLM
                history_text = "\n".join(
                    [f"{msg['role']}: {msg['content']}" for msg in st.session_state["history"]]
                )

                # Call orchestrator with memory + customer ID
                answer = route_request(
                    user_query,
                    customer_id,
                    history_text
                )

                # Clean answer (remove internal markers)
                clean_answer = (
                    answer.replace("[Agent: ACCOUNT]", "")
                          .replace("[Agent: CARD]", "")
                          .replace("[Agent: RISK]", "")
                          .replace("[Tool: PROFILE]", "")
                          .replace("[Tool: RISK]", "")
                          .replace("[LLM: BEGIN]", "")
                )

                # Save memory
                st.session_state["history"].append({"role": "user", "content": user_query})
                st.session_state["history"].append({"role": "agent", "content": clean_answer})

    # DISPLAY CHAT HISTORY
    for msg in st.session_state["history"]:
        if msg["role"] == "user":
            st.markdown(f"""
                <div style='background-color:#E3F2FD; padding:10px; border-radius:10px; margin:5px 0;'>
                    <strong>You:</strong> {msg['content']}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style='background-color:#E8F5E9; padding:10px; border-radius:10px; margin:5px 0;'>
                    <strong>BinaryBucks:</strong> {msg['content']}
                </div>
            """, unsafe_allow_html=True)
