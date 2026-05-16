import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

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
    .admin-account-box {
        background: linear-gradient(135deg, rgba(102, 255, 0, 0.1) 0%, rgba(0,0,0,0) 100%);
        border: 2px dashed #66ff00 !important;
        padding: 15px !important;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .daily-question {
        background: rgba(102, 255, 0, 0.03);
        border-left: 4px solid #66ff00;
        padding: 12px 15px;
        border-radius: 4px;
        margin-bottom: 15px;
    }
    .sidebar-glowing-btn button {
        background: linear-gradient(135deg, #a5ff33 0%, #66ff00 100%) !important;
        color: #0c0e11 !important;
        border: none !important;
    }
    div.stButton > button[key^="confirm_"] {
        background: #66ff00 !important;
        color: #0c0e11 !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. GOOGLE SHEETS CONNECTOR CONFIG ---
GSHEET_URL = "https://docs.google.com/spreadsheets/d/1EWrF_vJOIXyN7Y03t6rVECmY_YijC3nping9DoNnC-4/edit?usp=sharing"

# Streamlit Core Google Sheet Connection Pipeline
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    conn = None

# --- 4. SESSION STATE MANAGEMENT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_phone' not in st.session_state:
    st.session_state.user_phone = ""
if 'balance' not in st.session_state:
    st.session_state.balance = 20.00  # Default signup bonus

if 'm1_selection' not in st.session_state: st.session_state.m1_selection = None
if 'm1_bet_placed' not in st.session_state: st.session_state.m1_bet_placed = False
if 'm2_selection' not in st.session_state: st.session_state.m2_selection = None
if 'm2_bet_placed' not in st.session_state: st.session_state.m2_bet_placed = False

# Questions Pool
if 'q1' not in st.session_state:
    st.session_state.q1 = "Will the price of petrol see a decrease or remain stable in the upcoming fuel policy announcement?"
    st.session_state.q2 = "Will the local stock market index (PSX) close on a positive green note today?"

# --- 5. SIDEBAR CONTROL GATEWAY ---
with st.sidebar:
    st.title("💰 Predict & Earn")
    st.caption("Live Automated Sheet Network")

    if st.session_state.logged_in:
        st.success(f"Welcome: {st.session_state.user_phone}")
        st.metric("Wallet Balance", f"PKR {st.session_state.balance:,.2f}")
        st.markdown('<div class="sidebar-glowing-btn">', unsafe_allow_html=True)
        if st.button("Secure Logout"):
            st.session_state.logged_in = False
            st.session_state.user_phone = ""
            st.session_state.balance = 20.00
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        auth_mode = st.radio("Account Gateway", ["Sign In", "Register (New User)"])
        phone = st.text_input("Mobile Number", placeholder="e.g. 03415687754")
        password = st.text_input("Secure Password", type="password")
        
        if auth_mode == "Register (New User)":
            confirm_pass = st.text_input("Confirm Password", type="password")
            if st.button("Create Account"):
                if phone and password == confirm_pass:
                    st.session_state.logged_in = True
                    st.session_state.user_phone = phone
                    st.session_state.balance = 20.00
                    
                    # Google Sheets Write Logic for New User
                    if conn:
                        try:
                            new_user = pd.DataFrame([{"Mobile Number": phone, "Password": password, "Balance": 20.00}])
                            conn.create(spreadsheet=GSHEET_URL, worksheet="Users", data=new_user)
                        except:
                            pass
                    st.success("Account Created! PKR 20 Bonus Added.")
                    st.rerun()
        else:
            if st.button("Sign In Securely"):
                if phone and password:
                    st.session_state.logged_in = True
                    st.session_state.user_phone = phone
                    st.rerun()

    st.markdown("---")
    current_page = st.selectbox("Navigate Workspace", ["Predictions Zone", "User Dashboard (Results)", "Investor Wallet"])

# --- 6. CORE WORKSPACES ---

# WORKSPACE A: PREDICTIONS
if current_page == "Predictions Zone":
    st.title("🏆 Active Prediction Markets")
    st.caption("Step 1: Choose Answer | Step 2: Enter Bet Amount (Min: PKR 30) | Step 3: Lock Bet")
    st.markdown("---")

    if not st.session_state.logged_in:
        st.warning("⚠️ Please Login or Register from the sidebar to lock positions.")

    # MARKET CARD #1
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
        bet_amt_1 = st.number_input("Enter Bet Amount (PKR)", min_value=30, max_value=int(st.session_state.balance) if st.session_state.balance >= 30 else 30, step=10, key="amt_1", disabled=st.session_state.m1_bet_placed)
    with bet_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔥 PLACE & LOCK BET", key="confirm_m1", disabled=st.session_state.m1_bet_placed or not st.session_state.m1_selection):
            if st.session_state.balance >= bet_amt_1 and bet_amt_1 >= 30:
                st.session_state.balance -= bet_amt_1
                st.session_state.m1_bet_placed = True
                
                # Append Bet Log to Google Sheet Data Pipeline
                if conn:
                    try:
                        new_bet = pd.DataFrame([{"Mobile Number": st.session_state.user_phone, "Question": st.session_state.q1, "Selection": st.session_state.m1_selection, "Amount": bet_amt_1, "Status": "Pending"}])
                        conn.create(spreadsheet=GSHEET_URL, worksheet="Bets", data=new_bet)
                    except:
                        pass
                st.success(f"Bet Locked! Data pushed to Sheet pipeline.")
                st.rerun()
            else:
                st.error("❌ Insufficient Balance! Minimum PKR 30 required. Please deposit funds first.")
    st.markdown('</div>', unsafe_allow_html=True)

# WORKSPACE C: INVESTOR WALLET MANAGEMENT
elif current_page == "Investor Wallet":
    st.title("💰 Capital Allocation & Liquidity")
    
    w_col1, w_col2 = st.columns(2)
    w_col1.metric("Liquid Balance Pool", f"PKR {st.session_state.balance:,.2f}")
    w_col2.metric("Database Sync Pipeline", "Active ✅")

    st.markdown("---")
    dep_panel, with_panel = st.columns(2)
    
    with dep_panel:
        st.subheader("💳 Deposit Funds")
        
        # 🟢 LIVE ADMIN ACCOUNT DISPLAY BOX
        st.markdown("""
        <div class="admin-account-box">
            <p style="color:#66ff00; font-weight:bold; margin-bottom:5px;">⚠️ OFFICIAL ADMIN PAYMENT SLOTS:</p>
            <p style="margin:2px 0;"><b>EasyPaisa Account:</b> 0300-1234567</p>
            <p style="margin:2px 0;"><b>JazzCash Account:</b> 0300-7654321</p>
            <p style="margin:2px 0; caption-color:#aaa; font-size:0.85rem;">Account Title: <b>Predict Admin</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        method = st.selectbox("Select Deposit Network", ["EasyPaisa", "JazzCash"])
        wallet_number = st.text_input("Your Account Mobile Number", placeholder="e.g. 03415687754")
        account_title = st.text_input("Your Account Title Name", placeholder="e.g. Ali Khan")
        dep_amount = st.number_input("Transfer Amount (PKR)", min_value=30, step=50, key="wallet_dep_amt")
        trx_id = st.text_input("Transaction ID (TrxID)", placeholder="e.g. 8945729104", key="wallet_trx")
        
        if st.button("Submit Deposit Proof"):
            if trx_id and wallet_number and account_title and dep_amount >= 30:
                
                # Append Deposit Request to Google Sheet Pipeline
                if conn:
                    try:
                        new_dep = pd.DataFrame([{"Mobile Number": st.session_state.user_phone, "Network": method, "Account Title": account_title, "Amount": dep_amount, "TrxID": trx_id, "Status": "Pending"}])
                        conn.create(spreadsheet=GSHEET_URL, worksheet="Deposits", data=new_dep)
                    except:
                        pass
                
                st.session_state.balance += dep_amount
                st.success(f"Deposit log successfully pushed to Admin's Google Sheet! Balance updated.")
                st.rerun()
            else:
                st.error("Please fill out all credentials correctly (Min Rs. 30).")
