import streamlit as st

# --- 1. PAGE SETUP & INITIAL CONFIG ---
st.set_page_config(page_title="Nerdy Earners | AI Predictions", layout="wide")

# --- 2. PREMIUM NERDYTIPS STYLE ENGINE (CSS) ---
st.markdown("""
<style>
    /* Pure Dark Theme Background */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0c0e11 !important;
        color: #e6e8eb !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Layout Customization */
    [data-testid="stSidebar"] {
        background-color: #111417 !important;
    }
    
    /* Neon Glowing Buttons Override */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #a5ff33 0%, #66ff00 100%) !important;
        color: #0c0e11 !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
        width: 100%;
        box-shadow: 0 4px 15px rgba(102, 255, 0, 0.2);
    }
    
    /* Global Neon Text Utility */
    .neon-text {
        color: #66ff00 !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE FOR PERSISTENT DATA ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'balance' not in st.session_state:
    st.session_state.balance = 1250.00

# --- 4. NAVIGATION CONTROL PANEL (SIDEBAR) ---
with st.sidebar:
    st.title("🔋 Nerdy Earners")
    st.caption("AI-Powered Match Analytics Engine")

    if st.session_state.logged_in:
        st.success("Active User: Rabia")
        st.metric("Wallet Balance", f"PKR {st.session_state.balance:,.2f}")
        if st.button("Secure Logout"):
            st.session_state.logged_in = False
            st.rerun()
    else:
        st.subheader("Account Login Gateway")
        phone = st.text_input("Mobile Number", placeholder="e.g. 3415687754")
        st.caption("⚠️ Start se '0' remove kar ke enter karein.")
        password = st.text_input("Secure Password", type="password")
        if st.button("Sign In Securely"):
            if phone and password:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Fields cannot be left blank.")

    st.markdown("---")
    current_page = st.selectbox("Navigate Workspace", ["Predictions Zone", "Investor Wallet"])

# --- 5. APPLICATION CORE WORKSPACES ---

# WORKSPACE A: PREDICTIONS ZONE
if current_page == "Predictions Zone":
    st.title("🏆 AI Match Center")
    st.caption("Updated Every 5 Minutes")
    
    # Analytical Header Row Cards (Using Streamlit Native Metrics for 100% Stability)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Bankers", value="4/4 Tips Won Today")
    with col2:
        st.metric(label="Upcoming", value="Next Match in 01:15")
    with col3:
        st.metric(label="Success Rate", value="82% Last 30 Days")

    st.markdown("---")
    st.subheader("Featured AI Predictions")
    
    # Match Row 1 - Clean Container Grid Layout
    with st.container(border=True):
        m1_c1, m1_c2, m1_c3, m1_c4 = st.columns([1, 2, 2, 2])
        with m1_c1:
            st.markdown("⏰ **00:30**\n\n🟢 *Finished*")
        with m1_c2:
            st.markdown("⚽ **FC Cincinnati** vs **Toronto FC**")
            st.caption("Goals: **2-3** | GG: **No**")
        with m1_c3:
            st.markdown("**Odds Matrix (1-X-2)**")
            st.code("1.85  |  3.80  |  4.00", language="")
        with m1_c4:
            st.markdown("🎯 **AI Best TIP**")
            st.success("TIP: 1 (Trust: 4/10)")
            
    st.markdown("")  # Spacing element

    # Match Row 2 - Clean Container Grid Layout
    with st.container(border=True):
        m2_c1, m2_c2, m2_c3, m2_c4 = st.columns([1, 2, 2, 2])
        with m2_c1:
            st.markdown("⏰ **01:00**\n\n🟢 *Finished*")
        with m2_c2:
            st.markdown("⚽ **Cuiaba Esporte** vs **EC Bahia BA**")
            st.caption("Goals: **GG** | GG: **Yes**")
        with m2_c3:
            st.markdown("**Odds Matrix (1-X-2)**")
            st.code("2.30  |  3.20  |  3.30", language="")
        with m2_c4:
            st.markdown("🎯 **AI Best TIP**")
            st.success("TIP: GG (Trust: 6/10)")

# WORKSPACE B: INVESTOR WALLET MANAGEMENT
elif current_page == "Investor Wallet":
    st.title("💰 Capital Allocation & Liquidity")
    
    w_col1, w_col2 = st.columns(2)
    w_col1.metric("Liquid Balance Pool", f"PKR {st.session_state.balance:,.2f}")
    w_col2.metric("Verification State", "Fully Verified ✅")

    st.markdown("---")
    dep_panel, with_panel = st.columns(2)
    
    with dep_panel:
        st.subheader("Investment Deposit")
        st.info("⚡ **EasyPaisa / JazzCash:** 03415687754\n\n**Title:** Rabia Hafeez")
        dep_amount = st.number_input("Transfer Amount (PKR)", min_value=100, step=50, key="wallet_dep_amt")
        trx_id = st.text_input("Transaction ID (TrxID)", placeholder="e.g. 8945729104", key="wallet_trx")
        if st.button("Submit Deposit Log"):
            if trx_id:
                st.success("Log submitted! Data queued for verification.")
            else:
                st.error("Transaction ID is required.")
                
    with with_panel:
        st.subheader("Withdraw Rewards")
        with_amount = st.number_input("Withdraw Amount (PKR)", min_value=100, step=50, key="wallet_with_amt")
        if st.button("Authorize Liquidation"):
            if with_amount <= st.session_state.balance:
                st.session_state.balance -= with_amount
                st.success("Liquidation authorized successfully!")
                st.rerun()
            else:
                st.error("Insufficient balance pool.")
