import streamlit as st

# --- 1. INITIAL CONFIG (Keep this at the absolute top) ---
st.set_page_config(page_title="Nerdy Earners", layout="wide")

# --- 2. DARK STYLE INJECTION ---
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0c0e11 !important;
        color: #e6e8eb !important;
    }
    [data-testid="stSidebar"] {
        background-color: #111417 !important;
    }
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #a5ff33 0%, #66ff00 100%) !important;
        color: #0c0e11 !important;
        font-weight: bold !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'balance' not in st.session_state:
    st.session_state.balance = 1250.00

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🔋 Nerdy Earners")
    
    if st.session_state.logged_in:
        st.success("Active: Rabia")
        st.metric("Balance", f"PKR {st.session_state.balance:,.2f}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    else:
        st.subheader("Login Gateway")
        phone = st.text_input("Mobile Number")
        password = st.text_input("Password", type="password")
        if st.button("Sign In Securely"):
            if phone and password:
                st.session_state.logged_in = True
                st.rerun()

    st.markdown("---")
    page = st.selectbox("Navigation", ["Predictions Center", "Investor Wallet"])

# --- 5. MAIN WORKSPACES ---
if page == "Predictions Center":
    st.title("🏆 AI Match Matrix")
    st.caption("Real-Time Probabilities Engine")
    
    # Top Cards
    c1, c2, c3 = st.columns(3)
    c1.metric("Bankers Performance", "4/4 Won Today")
    c2.metric("Queue Horizon", "01:12:45")
    c3.metric("Historical Matrix", "82% Win Rate")
    
    st.markdown("---")
    st.subheader("Featured AI Predictions")
    
    # Match 1 Display Box
    with st.container(border=True):
        m1_col1, m1_col2, m1_col3 = st.columns([1, 2, 1])
        m1_col1.markdown("**00:30** \n*Finished*")
        m1_col2.markdown("⚽ **FC Cincinnati** vs **Toronto FC**")
        m1_col3.markdown("🏆 TIP: **1** \n🎯 Goals: **2-3**")
        
    # Match 2 Display Box
    with st.container(border=True):
        m2_col1, m2_col2, m2_col3 = st.columns([1, 2, 1])
        m2_col1.markdown("**01:00** \n*Finished*")
        m2_col2.markdown("⚽ **Cuiabá** vs **EC Bahia BA**")
        m2_col3.markdown("🏆 TIP: **GG** \n🎯 Goals: **GG**")

elif page == "Investor Wallet":
    st.title("💰 Capital Allocation & Liquidity")
    
    w1, w2 = st.columns(2)
    w1.metric("Liquid Balance Pool", f"PKR {st.session_state.balance:,.2f}")
    w2.metric("Verification State", "Fully Verified ✅")
    
    st.markdown("---")
    dep_col, with_col = st.columns(2)
    
    with dep_col:
        st.subheader("Investment Deposit")
        st.info("Easypaisa/JazzCash: **03415687754** (Rabia Hafeez)")
        st.number_input("Amount (PKR)", min_value=100, step=50, key="d_amt")
        st.text_input("Transaction ID", key="d_trx")
        if st.button("Submit Deposit Log"):
            st.success("Log submitted for ledger verification!")
            
    with with_col:
        st.subheader("Withdraw Rewards")
        w_amt = st.number_input("Withdraw Amount (PKR)", min_value=100, step=50, key="w_amt")
        if st.button("Authorize Liquidation"):
            if w_amt <= st.session_state.balance:
                st.session_state.balance -= w_amt
                st.success("Liquidation event authorized!")
                st.rerun()
            else:
                st.error("Insufficient pool capitalization.")
