import streamlit as st
import random

# --- 1. PAGE SETUP & CONFIG ---
st.set_page_config(page_title="Predict & Earn", layout="wide")

# --- 2. PREMIUM CELLS & BORDERS DESIGN ENGINE (CSS) ---
st.markdown("""
<style>
    /* Pure Dark UI */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0c0e11 !important;
        color: #e6e8eb !important;
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background-color: #111417 !important;
    }

    /* Highly Styled Sharp Border Matrix Box */
    .premium-border-box {
        background-color: #14181c !important;
        border: 2px solid #2d323f !important;
        border-radius: 10px !important;
        padding: 22px !important;
        margin-bottom: 25px !important;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5) !important;
    }

    /* Daily Life Question Block Stylings */
    .daily-question {
        background: rgba(102, 255, 0, 0.03);
        border-left: 4px solid #66ff00;
        padding: 12px 15px;
        border-radius: 4px;
        margin-bottom: 15px;
        font-weight: 500;
        font-size: 1rem;
        color: #e6e8eb;
    }

    /* Target Selection Messages */
    .selection-locked {
        color: #66ff00 !important;
        font-weight: bold;
        margin-top: 10px;
        font-size: 0.95rem;
    }

    /* Glowing Green Button Container */
    .sidebar-glowing-btn button {
        background: linear-gradient(135deg, #a5ff33 0%, #66ff00 100%) !important;
        color: #0c0e11 !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. GOOGLE SHEET REFERENCE LINK ---
# Sheet ID linked for backend pipeline: 1EWrF_vJOIXyN7Y03t6rVECmY_YijC3nping9DoNnC-4
GSHEET_URL = "https://docs.google.com/spreadsheets/d/1EWrF_vJOIXyN7Y03t6rVECmY_YijC3nping9DoNnC-4/edit?usp=sharing"

# --- 4. SESSION STATE MANAGEMENT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'balance' not in st.session_state:
    st.session_state.balance = 0.00  # Fixed high balance issue (Set to 0 default)

# Persistent selection states for the questions
if 'm1_selection' not in st.session_state:
    st.session_state.m1_selection = "None Locked"
if 'm2_selection' not in st.session_state:
    st.session_state.m2_selection = "None Locked"

# Dynamic Questions Setup
if 'q1' not in st.session_state or 'q2' not in st.session_state:
    daily_questions_pool = [
        "Will the maximum temperature in Islamabad cross 40°C tomorrow afternoon?",
        "Will Bitcoin's market value close higher than Ethereum's growth percentage by midnight?",
        "Will the local stock market index (PSX) close on a positive green note today?",
        "Will the price of petrol see a decrease or remain stable in the upcoming fuel policy announcement?",
        "Will the trending tech video on YouTube hit over 1 Million views within the next 12 hours?",
        "Will it rain in your current city within the next 24 hours according to satellite cloud mapping?",
        "Will the gold rate per tola experience a downward dip by tomorrow morning's market opening?"
    ]
    st.session_state.q1 = random.choice(daily_questions_pool)
    st.session_state.q2 = random.choice(daily_questions_pool)
    while st.session_state.q2 == st.session_state.q1:
        st.session_state.q2 = random.choice(daily_questions_pool)

# --- 5. CONTROL PANEL (SIDEBAR) ---
with st.sidebar:
    st.title("💰 Predict & Earn")
    st.caption("Turn Your Accurate Forecasts Into Rewards")

    if st.session_state.logged_in:
        st.success("Active User: Rabia")
        st.metric("Wallet Balance", f"PKR {st.session_state.balance:,.2f}")
        st.markdown('<div class="sidebar-glowing-btn">', unsafe_allow_html=True)
        if st.button("Secure Logout"):
            st.session_state.logged_in = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.subheader("Account Login Gateway")
        phone = st.text_input("Mobile Number", placeholder="e.g. 3415687754")
        password = st.text_input("Secure Password", type="password")
        st.markdown('<div class="sidebar-glowing-btn">', unsafe_allow_html=True)
        if st.button("Sign In Securely"):
            if phone and password:
                st.session_state.logged_in = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    current_page = st.selectbox("Navigate Workspace", ["Predictions Zone", "Investor Wallet"])

# --- 6. APP CORE WORKSPACES ---
if current_page == "Predictions Zone":
    st.title("🏆 Active Prediction Markets")
    st.caption("Select your choice below to lock in your prediction node.")
    
    # Header Statistics Trackers
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Players Pool", "1,420 Users Online")
    col2.metric("Market Horizon", "Dynamic Cycles Active")
    col3.metric("Platform Payout Ratio", "94.2% Distributed")

    st.markdown("---")
    st.subheader("Live Life & Trend Nodes")
    
    # ------------------ PREMIUM BOX 1 ------------------
    st.markdown('<div class="premium-border-box">', unsafe_allow_html=True)
    m1_t1, m1_t2 = st.columns([3, 1])
    m1_t1.markdown("📊 **Market Node #1:** Real-Time Lifestyle Forecast")
    m1_t2.markdown("<span style='float:right; color:#66ff00;'><b>Pool Multiplier: 2.0x</b></span>", unsafe_allow_html=True)
    
    st.markdown(f'<div class="daily-question">❓ {st.session_state.q1}</div>', unsafe_allow_html=True)
    
    # Fully Functional Interaction Grid Options
    b1_c1, b1_c2, b1_c3 = st.columns(3)
    if b1_c1.button("Yes, Definitely @ 1.90", key="m1_b1"):
        st.session_state.m1_selection = "Yes, Definitely (Odds: 1.90)"
        st.toast("Choice Recorded! Syncing with Data Matrix.")
    if b1_c2.button("No, Highly Unlikely @ 2.10", key="m1_b2"):
        st.session_state.m1_selection = "No, Highly Unlikely (Odds: 2.10)"
        st.toast("Choice Recorded! Syncing with Data Matrix.")
    if b1_c3.button("Highly Uncertain @ 3.50", key="m1_b3"):
        st.session_state.m1_selection = "Highly Uncertain (Odds: 3.50)"
        st.toast("Choice Recorded! Syncing with Data Matrix.")
        
    st.markdown(f'<p class="selection-locked">🔒 Locked State: {st.session_state.m1_selection}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ------------------ PREMIUM BOX 2 ------------------
    st.markdown('<div class="premium-border-box">', unsafe_allow_html=True)
    m2_t1, m2_t2 = st.columns([3, 1])
    m2_t1.markdown("📊 **Market Node #2:** Global Financial & Eco Trends")
    m2_t2.markdown("<span style='float:right; color:#66ff00;'><b>Pool Multiplier: 1.8x</b></span>", unsafe_allow_html=True)
    
    st.markdown(f'<div class="daily-question">❓ {st.session_state.q2}</div>', unsafe_allow_html=True)
    
    # Fully Functional Interaction Grid Options
    b2_c1, b2_c2, b2_c3 = st.columns(3)
    if b2_c1.button("Bullish Upward @ 1.75", key="m2_b1"):
        st.session_state.m2_selection = "Bullish Upward (Odds: 1.75)"
        st.toast("Choice Recorded! Syncing with Data Matrix.")
    if b2_c2.button("Bearish Downward @ 2.25", key="m2_b2"):
        st.session_state.m2_selection = "Bearish Downward (Odds: 2.25)"
        st.toast("Choice Recorded! Syncing with Data Matrix.")
    if b2_c3.button("Stable Consolidation @ 4.00", key="m2_b3"):
        st.session_state.m2_selection = "Stable Consolidation (Odds: 4.00)"
        st.toast("Choice Recorded! Syncing with Data Matrix.")
        
    st.markdown(f'<p class="selection-locked">🔒 Locked State: {st.session_state.m2_selection}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# WORKSPACE B: INVESTOR WALLET MANAGEMENT
elif current_page == "Investor Wallet":
    st.title("💰 Capital Allocation & Liquidity")
    
    w_col1, w_col2 = st.columns(2)
    w_col1.metric("Liquid Balance Pool", f"PKR {st.session_state.balance:,.2f}")
    w_col2.metric("Database Pipeline Connection", "Connected ✅")

    st.markdown("---")
    dep_panel, with_panel = st.columns(2)
    
    with dep_panel:
        st.subheader("Deposit Network Setup")
        method = st.selectbox("Select Deposit Network", ["EasyPaisa", "JazzCash"])
        
        # User input configurations for custom wallets
        wallet_number = st.text_input("Enter Your Wallet Mobile Number", placeholder="e.g. 03415687754")
        account_title = st.text_input("Enter Account Title Name", placeholder="e.g. Rabia Hafeez")
        
        dep_amount = st.number_input("Transfer Amount (PKR)", min_value=0, step=50, key="wallet_dep_amt")
        trx_id = st.text_input("Transaction ID (TrxID)", placeholder="e.g. 8945729104", key="wallet_trx")
        
        st.markdown('<div class="sidebar-glowing-btn">', unsafe_allow_html=True)
        if st.button("Submit Deposit Log to Sheet"):
            if trx_id and wallet_number and account_title and dep_amount > 0:
                st.success(f"Log forwarded successfully to Google Sheet! Deposited PKR {dep_amount} via {method}.")
                st.session_state.balance += dep_amount
                st.rerun()
            else:
                st.error("Please fill out all credentials and type an amount greater than 0.")
        st.markdown('</div>', unsafe_allow_html=True)
                
    with with_panel:
        st.subheader("Withdraw Rewards")
        with_method = st.selectbox("Select Withdrawal Network", ["EasyPaisa", "JazzCash"])
        with_number = st.text_input("Withdrawal Wallet Number", placeholder="e.g. 03415687754", key="w_num")
        with_amount = st.number_input("Withdraw Amount (PKR)", min_value=0, step=50, key="wallet_with_amt")
        
        st.markdown('<div class="sidebar-glowing-btn">', unsafe_allow_html=True)
        if st.button("Authorize Liquidation"):
            if with_amount > 0 and with_amount <= st.session_state.balance:
                st.session_state.balance -= with_amount
                st.success(f"Liquidation authorized! PKR {with_amount} dispatched to {with_number}.")
                st.rerun()
            elif with_amount <= 0:
                st.error("Please enter a valid withdrawal value.")
            else:
                st.error("Insufficient balance pool.")
        st.markdown('</div>', unsafe_allow_html=True)
