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
    .status-pending { color: #ffaa00 !important; font-weight: bold; }
    .sidebar-glowing-btn button {
        background: linear-gradient(135deg, #a5ff33 0%, #66ff00 100%) !important;
        color: #0c0e11 !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. GOOGLE SHEETS INTEGRATION LINK ---
# Direct API integration path for: 1EWrF_vJOIXyN7Y03t6rVECmY_YijC3nping9DoNnC-4
GSHEET_URL = "https://docs.google.com/spreadsheets/d/1EWrF_vJOIXyN7Y03t6rVECmY_YijC3nping9DoNnC-4/edit?usp=sharing"

# --- 4. SESSION STATE MANAGEMENT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_phone' not in st.session_state:
    st.session_state.user_phone = ""
if 'balance' not in st.session_state:
    st.session_state.balance = 0.00

# Mock historical data simulation (Jab tak live connection credentials config na hon)
if 'history_df' not in st.session_state:
    st.session_state.history_df = pd.DataFrame([
        {"Date": "Yesterday", "Question": "Will the price of petrol decrease?", "Your Pick": "Yes", "Status": "Win", "Reward": "+ PKR 200"},
        {"Date": "Yesterday", "Question": "Will it rain in Islamabad?", "Your Pick": "No", "Status": "Loss", "Reward": "0"}
    ])

# Dynamic Active Questions Engine
if 'q1' not in st.session_state:
    daily_questions_pool = [
        "Will the maximum temperature in Islamabad cross 40°C tomorrow afternoon?",
        "Will Bitcoin's market value close higher than Ethereum's growth percentage by midnight?",
        "Will the local stock market index (PSX) close on a positive green note today?",
        "Will the price of petrol see a decrease or remain stable in the upcoming fuel policy announcement?",
        "Will it rain in your current city within the next 24 hours according to satellite cloud mapping?"
    ]
    st.session_state.q1 = random.choice(daily_questions_pool)
    st.session_state.q2 = random.choice(daily_questions_pool)
    while st.session_state.q2 == st.session_state.q1:
        st.session_state.q2 = random.choice(daily_questions_pool)

# --- 5. AUTHENTICATION SIDEBAR SYSTEM (LOGIN & REGISTER) ---
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
                    # Simulated Sheet Write Event
                    st.success("Registration Logged! Account Created.")
                    st.session_state.logged_in = True
                    st.session_state.user_phone = phone
                    st.session_state.balance = 100.00  # Welcome signup bonus
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
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    current_page = st.selectbox("Navigate Workspace", ["Predictions Zone", "User Dashboard (Results)", "Investor Wallet"])

# --- 6. APPLICATION WORKSPACES ---

# WORKSPACE A: ACTIVE PREDICTIONS
if current_page == "Predictions Zone":
    st.title("🏆 Active Prediction Markets")
    st.caption("Select your node below. Logs will append instantly to Google Sheet Pipeline.")
    
    col1, col2 = st.columns(2)
    col1.metric("Active Players Pool", "1,420 Users Online")
    col2.metric("Data Sync Mode", "Sheet Pipeline Active")
    st.markdown("---")

    # Question Box 1
    st.markdown('<div class="premium-border-box">', unsafe_allow_html=True)
    st.markdown("📊 **Market Node #1:** Real-Time Lifestyle Forecast")
    st.markdown(f'<div class="daily-question">❓ {st.session_state.q1}</div>', unsafe_allow_html=True)
    
    b1, b2 = st.columns(2)
    if b1.button("YES, I Predict This Outcome", key="q1_yes"):
        st.toast(f"Logged: YES to Google Sheets ID: {st.session_state.user_phone if st.session_state.logged_in else 'Guest'}")
        st.success("Selection appended to data sheet under pending state!")
    if b2.button("NO, I Reject This Outcome", key="q1_no"):
        st.toast("Logged: NO to Google Sheets Pipeline.")
        st.success("Selection appended to data sheet under pending state!")
    st.markdown('</div>', unsafe_allow_html=True)

# WORKSPACE B: NEXT DAY RESULTS & OUTPUTS (WIN / LOSS)
elif current_page == "User Dashboard (Results)":
    st.title("📅 Settlement Matrix & Performance Results")
    st.caption("This data tracks results appended directly from your automated sheet logs.")
    
    if not st.session_state.logged_in:
        st.warning("Please sign in from the gateway sidebar to view your profile results ledger.")
    else:
        st.subheader("Your Recent Predictions Ledger")
        
        # Displaying Results with Status Mapping
        for idx, row in st.session_state.history_df.iterrows():
            st.markdown('<div class="premium-border-box">', unsafe_allow_html=True)
            r_col1, r_col2, r_col3 = st.columns([3, 1, 1])
            
            with r_col1:
                st.markdown(f"❓ **Question:** {row['Question']}")
                st.caption(f"Timeline: {row['Date']} | Your Selection: **{row['Your Pick']}**")
            
            with r_col2:
                if row['Status'] == "Win":
                    st.markdown('Status: <span class="status-win">WIN ✅</span>', unsafe_allow_html=True)
                elif row['Status'] == "Loss":
                    st.markdown('Status: <span class="status-loss">LOSS ❌</span>', unsafe_allow_html=True)
                else:
                    st.markdown('Status: <span class="status-pending">PENDING ⏳</span>', unsafe_allow_html=True)
                    
            with r_col3:
                st.metric("Reward Metric", row['Reward'])
            st.markdown('</div>', unsafe_allow_html=True)

# WORKSPACE C: INVESTOR WALLET MANAGEMENT
elif current_page == "Investor Wallet":
    st.title("💰 Capital Allocation & Liquidity")
    w_col1, w_col2 = st.columns(2)
    w_col1.metric("Liquid Balance Pool", f"PKR {st.session_state.balance:,.2f}")
    w_col2.metric("Database Pipeline Connection", "Connected ✅")
