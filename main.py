import streamlit as st
import random
import pandas as pd

# --- 1. PAGE SETUP & CONFIG ---
st.set_page_config(page_title="Predict & Earn", layout="wide")

# --- 2. PREMIUM DARK UI DESIGN ENGINE (CSS) ---
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0c0e11 !important;
        color: #e6e8eb !important;
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #111417 !important;
    }
    .premium-border-box {
        background-color: #14181c !important;
        border: 2px solid #2d323f !important;
        border-radius: 10px !important;
        padding: 22px !important;
        margin-bottom: 25px !important;
    }
    .daily-question {
        background: rgba(102, 255, 0, 0.03);
        border-left: 4px solid #66ff00;
        padding: 12px 15px;
        border-radius: 4px;
        margin-bottom: 15px;
        font-size: 1rem;
    }
    .status-win { color: #66ff00 !important; font-weight: bold; }
    .status-loss { color: #ff4b4b !important; font-weight: bold; }
    
    /* Glowing Green Button Container */
    .sidebar-glowing-btn button {
        background: linear-gradient(135deg, #a5ff33 0%, #66ff00 100%) !important;
        color: #0c0e11 !important;
        border: none !important;
    }
    
    /* Bet Submit Special Button styling */
    div.stButton > button[key^="confirm_"] {
        background: #66ff00 !important;
        color: #0c0e11 !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. GOOGLE SHEETS INTEGRATION LINK ---
GSHEET_URL = "https://docs.google.com/spreadsheets/d/1EWrF_vJOIXyN7Y03t6rVECmY_YijC3nping9DoNnC-4/edit?usp=sharing"

# --- 4. SESSION STATE MANAGEMENT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_phone' not in st.session_state:
    st.session_state.user_phone = ""
if 'balance' not in st.session_state:
    st.session_state.balance = 0.00  

# Persistent selection and bet storage
if 'm1_selection' not in st.session_state:
    st.session_state.m1_selection = None
if 'm1_bet_placed' not in st.session_state:
    st.session_state.m1_bet_placed = False
if 'm1_bet_amount' not in st.session_state:
    st.session_state.m1_bet_amount = 0

if 'm2_selection' not in st.session_state:
    st.session_state.m2_selection = None
if 'm2_bet_placed' not in st.session_state:
    st.session_state.m2_bet_placed = False
if 'm2_bet_amount' not in st.session_state:
    st.session_state.m2_bet_amount = 0

# Mock history data simulation for testing next-day output UI
if 'history_df' not in st.session_state:
    st.session_state.history_df = pd.DataFrame([
        {"Date": "16-05-2026", "Question": "Will Bitcoin value close higher than Ethereum today?", "Your Pick": "YES", "Bet Amount": "PKR 30", "Status": "Win", "Reward": "+ PKR 60"},
        {"Date": "16-05-2026", "Question": "Will maximum temperature cross 40°C?", "Your Pick": "NO", "Bet Amount": "PKR 50", "Status": "Loss", "Reward": "0"}
    ])

if 'q1' not in st.session_state:
    st.session_state.q1 = "Will the price of petrol see a decrease or remain stable in the upcoming fuel policy announcement?"
    st.session_state.q2 = "Will the local stock market index (PSX) close on a positive green note today?"

# --- 5. SIDEBAR AUTHENTICATION CONTAINER ---
with st.sidebar:
    st.title("💰 Predict & Earn")
    st.caption("Turn Accurate Forecasts Into Daily Rewards")

    if st.session_state.logged_in:
        st.success(f"Welcome: {st.session_state.user_phone}")
        st.metric("Wallet Balance", f"PKR {st.session_state.balance:,.2f}")
        st.markdown('<div class="sidebar-glowing-btn">', unsafe_allow_html=True)
        if st.button("Secure Logout"):
            st.session_state.logged_in = False
            st.session_state.user_phone = ""
            st.session_state.balance = 0.00
            st.session_state.m1_bet_placed = False
            st.session_state.m2_bet_placed = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        auth_mode = st.radio("Account Gateway", ["Sign In (Existing)", "Register (New User)"])
        phone = st.text_input("Mobile Number", placeholder="e.g. 3415687754")
        password = st.text_input("Secure Password", type="password")
        
        if auth_mode == "Register (New User)":
            confirm_pass = st.text_input("Confirm Password", type="password")
            st.markdown('<div class="sidebar-glowing-btn">', unsafe_allow_html=True)
            if st.button("Create Account & Join"):
                if phone and password == confirm_pass:
                    st.success("Registration Logged! PKR 100 Welcome Bonus Credited.")
                    st.session_state.logged_in = True
                    st.session_state.user_phone = phone
                    st.session_state.balance = 100.00  # Bonus set to 100 so user can play multiple Rs. 30 bets
                    st.rerun()
                else:
                    st.error("Passwords do not match or fields are empty.")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="sidebar-glowing-btn">', unsafe_allow_html=True)
            if st.button("Sign In Securely"):
                if phone and password:
                    st.session_state.logged_in = True
                    st.session_state.user_phone = phone
                    st.session_state.balance = 100.00  
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    current_page = st.selectbox("Navigate Workspace", ["Predictions Zone", "User Dashboard (Results)", "Investor Wallet"])

# --- 6. CORE WORKSPACES ---

# WORKSPACE A: ACTIVE PREDICTIONS & INPUT SLOTS
if current_page == "Predictions Zone":
    st.title("🏆 Active Prediction Markets")
    st.caption("Step 1: Choose Answer | Step 2: Enter Bet Amount (Min: PKR 30) | Step 3: Lock Bet")
    st.markdown("---")

    if not st.session_state.logged_in:
        st.warning("⚠️ Please Login or Register from the sidebar to place amounts and lock bets.")

    # ------------------ MARKET CARD #1 ------------------
    st.markdown('<div class="premium-border-box">', unsafe_allow_html=True)
    st.markdown("📊 **Market Node #1:** Real-Time Lifestyle Forecast")
    st.markdown(f'<div class="daily-question">❓ {st.session_state.q1}</div>', unsafe_allow_html=True)
    
    b1, b2 = st.columns(2)
    if b1.button("🟢 YES, I Predict This", key="btn_q1_yes", disabled=st.session_state.m1_bet_placed):
        st.session_state.m1_selection = "YES"
    if b2.button("🔴 NO, I Reject This", key="btn_q1_no", disabled=st.session_state.m1_bet_placed):
        st.session_state.m1_selection = "NO"
        
    if st.session_state.m1_selection:
        st.info(f"Selected Option: **{st.session_state.m1_selection}**")
    
    st.markdown("---")
    bet_col1, bet_col2 = st.columns([2, 1])
    with bet_col1:
        # FIXED: min_value is set to 30 now
        bet_amt_1 = st.number_input("Enter Bet Amount (PKR) for Node 1", min_value=30, max_value=int(st.session_state.balance) if st.session_state.balance >= 30 else 30, step=10, key="amt_1", disabled=st.session_state.m1_bet_placed)
    with bet_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔥 PLACE & LOCK BET", key="confirm_m1", disabled=st.session_state.m1_bet_placed or not st.session_state.m1_selection):
            if st.session_state.balance >= bet_amt_1:
                st.session_state.balance -= bet_amt_1
                st.session_state.m1_bet_placed = True
                st.session_state.m1_bet_amount = bet_amt_1
                st.success(f"Bet Locked! PKR {bet_amt_1} deducted and tracked.")
                st.rerun()
            else:
                st.error("Insufficient Balance! Minimum PKR 30 required.")
                
    if st.session_state.m1_bet_placed:
        st.markdown(f'<p style="color:#66ff00; font-weight:bold;">✅ Active Position: Bet of PKR {st.session_state.m1_bet_amount} locked on "{st.session_state.m1_selection}"</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


    # ------------------ MARKET CARD #2 ------------------
    st.markdown('<div class="premium-border-box">', unsafe_allow_html=True)
    st.markdown("📊 **Market Node #2:** Global Financial & Eco Trends")
    st.markdown(f'<div class="daily-question">❓ {st.session_state.q2}</div>', unsafe_allow_html=True)
    
    b3, b4 = st.columns(2)
    if b3.button("🟢 YES, I Predict This", key="btn_q2_yes", disabled=st.session_state.m2_bet_placed):
        st.session_state.m2_selection = "YES"
    if b4.button("🔴 NO, I Reject This", key="btn_q2_no", disabled=st.session_state.m2_bet_placed):
        st.session_state.m2_selection = "NO"
        
    if st.session_state.m2_selection:
        st.info(f"Selected Option: **{st.session_state.m2_selection}**")
        
    st.markdown("---")
    bet_col3, bet_col4 = st.columns([2, 1])
    with bet_col3:
        # FIXED: min_value is set to 30 now
        bet_amt_2 = st.number_input("Enter Bet Amount (PKR) for Node 2", min_value=30, max_value=int(st.session_state.balance) if st.session_state.balance >= 30 else 30, step=10, key="amt_2", disabled=st.session_state.m2_bet_placed)
    with bet_col4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔥 PLACE & LOCK BET", key="confirm_m2", disabled=st.session_state.m2_bet_placed or not st.session_state.m2_selection):
            if st.session_state.balance >= bet_amt_2:
                st.session_state.balance -= bet_amt_2
                st.session_state.m2_bet_placed = True
                st.session_state.m2_bet_amount = bet_amt_2
                st.success(f"Bet Locked! PKR {bet_amt_2} deducted and tracked.")
                st.rerun()
            else:
                st.error("Insufficient Balance! Minimum PKR 30 required.")
                
    if st.session_state.m2_bet_placed:
        st.markdown(f'<p style="color:#66ff00; font-weight:bold;">✅ Active Position: Bet of PKR {st.session_state.m2_bet_amount} locked on "{st.session_state.m2_selection}"</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# WORKSPACE B: RESULTS LEDGER
elif current_page == "User Dashboard (Results)":
    st.title("📅 Settlement Matrix & Performance Results")
    st.caption("Peeche Google Sheet se results change hote hi yahan dashboard automatically update ho jata hai.")
    
    if not st.session_state.logged_in:
        st.warning("Please sign in from the gateway sidebar to view your profile results ledger.")
    else:
        st.subheader("Your Recent Predictions Log")
        
        for idx, row in st.session_state.history_df.iterrows():
            st.markdown('<div class="premium-border-box">', unsafe_allow_html=True)
            r_col1, r_col2, r_col3 = st.columns([3, 1, 1])
            with r_col1:
                st.markdown(f"❓ **Question:** {row['Question']}")
                st.caption(f"Your Pick: **{row['Your Pick']}** | Amount Staked: **{row['Bet Amount']}**")
            with r_col2:
                if row['Status'] == "Win":
                    st.markdown('Status: <span class="status-win">WIN ✅</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="status-loss">LOSS ❌</span>', unsafe_allow_html=True)
            with r_col3:
                st.metric("Profit Multiplier", row['Reward'])
            st.markdown('</div>', unsafe_allow_html=True)

# WORKSPACE C: INVESTOR WALLET MANAGEMENT
elif current_page == "Investor Wallet":
    st.title("💰 Capital Allocation & Liquidity")
    w_col1, w_col2 = st.columns(2)
    w_col1.metric("Liquid Balance Pool", f"PKR {st.session_state.balance:,.2f}")
    w_col2.metric("Database Pipeline Connection", "Connected ✅")
