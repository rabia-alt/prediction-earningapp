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
        font-size: 1rem;
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

# --- 3. GOOGLE SHEETS INTEGRATION LINK ---
GSHEET_URL = "https://docs.google.com/spreadsheets/d/1EWrF_vJOIXyN7Y03t6rVECmY_YijC3nping9DoNnC-4/edit?usp=sharing"

# Establish Cloud Connection
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
    st.session_state.balance = 0.00

if 'm1_selection' not in st.session_state: st.session_state.m1_selection = None
if 'm1_bet_placed' not in st.session_state: st.session_state.m1_bet_placed = False
if 'm2_selection' not in st.session_state: st.session_state.m2_selection = None
if 'm2_bet_placed' not in st.session_state: st.session_state.m2_bet_placed = False

if 'q1' not in st.session_state:
    st.session_state.q1 = "Will the price of petrol see a decrease or remain stable in the upcoming fuel policy announcement?"
    st.session_state.q2 = "Will the local stock market index (PSX) close on a positive green note today?"

# --- HELPER DATABASE FUNCTIONS (LIVE SYNC) ---
def fetch_users_db():
    if conn:
        try:
            # Clear cache to get fresh data directly from Google Sheet
            st.cache_data.clear()
            df = conn.read(spreadsheet=GSHEET_URL, worksheet="Users", ttl=0)
            df['Mobile Number'] = df['Mobile Number'].astype(str).str.strip()
            return df
        except:
            return pd.DataFrame(columns=["Mobile Number", "Password", "Balance"])
    return pd.DataFrame(columns=["Mobile Number", "Password", "Balance"])

def sync_user_balance_from_sheet(phone_num):
    df = fetch_users_db()
    user_row = df[df['Mobile Number'] == str(phone_num).strip()]
    if not user_row.empty:
        st.session_state.balance = float(user_row.iloc[0]['Balance'])

# Live balance update on every action if user is logged in
if st.session_state.logged_in:
    sync_user_balance_from_sheet(st.session_state.user_phone)

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
        phone = st.text_input("Mobile Number", placeholder="e.g. 03415687754").strip()
        password = st.text_input("Secure Password", type="password")
        
        if auth_mode == "Register (New User)":
            confirm_pass = st.text_input("Confirm Password", type="password")
            st.markdown('<div class="sidebar-glowing-btn">', unsafe_allow_html=True)
            if st.button("Create Account & Join"):
                if phone and password == confirm_pass:
                    # Check if user already exists in Sheet database
                    users_df = fetch_users_db()
                    if phone in users_df['Mobile Number'].values:
                        st.error("This mobile number is already registered! Please Sign In.")
                    else:
                        if conn:
                            try:
                                new_user = pd.DataFrame([{"Mobile Number": str(phone), "Password": str(password), "Balance": 20.00}])
                                conn.create(spreadsheet=GSHEET_URL, worksheet="Users", data=new_user)
                                st.session_state.logged_in = True
                                st.session_state.user_phone = phone
                                st.session_state.balance = 20.00
                                st.success("Registered Successfully! PKR 20 Bonus Added.")
                                st.rerun()
                            except Exception as e:
                                st.error("Database connection busy. Please try again.")
                else:
                    st.error("Passwords do not match or fields are empty.")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="sidebar-glowing-btn">', unsafe_allow_html=True)
            if st.button("Sign In Securely"):
                if phone and password:
                    users_df = fetch_users_db()
                    # Validate credentials directly from Google Sheet rows
                    matched_user = users_df[(users_df['Mobile Number'] == str(phone)) & (users_df['Password'].astype(str) == str(password))]
                    if not matched_user.empty:
                        st.session_state.logged_in = True
                        st.session_state.user_phone = phone
                        st.session_state.balance = float(matched_user.iloc[0]['Balance'])
                        st.success("Access Granted!")
                        st.rerun()
                    else:
                        st.error("Invalid Mobile Number or Password combination.")
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
        bet_amt_1 = st.number_input("Enter Bet Amount (PKR) for Node 1", min_value=30, max_value=int(st.session_state.balance) if st.session_state.balance >= 30 else 30, step=10, key="amt_1", disabled=st.session_state.m1_bet_placed)
    with bet_col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔥 PLACE & LOCK BET", key="confirm_m1", disabled=st.session_state.m1_bet_placed or not st.session_state.m1_selection):
            if st.session_state.balance >= bet_amt_1 and bet_amt_1 >= 30:
                # Update local and cloud balance
                new_bal = st.session_state.balance - bet_amt_1
                st.session_state.m1_bet_placed = True
                
                if conn:
                    try:
                        # 1. Log Bet Details
                        new_bet = pd.DataFrame([{"Mobile Number": st.session_state.user_phone, "Question": st.session_state.q1, "Selection": st.session_state.m1_selection, "Amount": bet_amt_1, "Status": "Pending"}])
                        conn.create(spreadsheet=GSHEET_URL, worksheet="Bets", data=new_bet)
                        
                        # 2. Update User's Balance row on Sheet
                        all_users = fetch_users_db()
                        all_users.loc[all_users['Mobile Number'] == str(st.session_state.user_phone), 'Balance'] = new_bal
                        conn.update(spreadsheet=GSHEET_URL, worksheet="Users", data=all_users)
                        
                        st.session_state.balance = new_bal
                        st.success(f"Bet Locked! Data pushed to Sheet.")
                        st.rerun()
                    except:
                        st.error("Database was busy. Bet not recorded.")
            else:
                st.error("❌ Insufficient Balance! Minimum PKR 30 required. Please go to 'Investor Wallet' to add money via EasyPaisa.")
                
    if st.session_state.m1_bet_placed:
        st.markdown(f'<p style="color:#66ff00; font-weight:bold;">✅ Active Position Locked on "{st.session_state.m1_selection}"</p>', unsafe_allow_html=True)
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
        bet_amt_2 = st.number_input("Enter Bet Amount (PKR) for Node 2", min_value=30, max_value=int(st.session_state.balance) if st.session_state.balance >= 30 else 30, step=10, key="amt_2", disabled=st.session_state.m2_bet_placed)
    with bet_col4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔥 PLACE & LOCK BET", key="confirm_m2", disabled=st.session_state.m2_bet_placed or not st.session_state.m2_selection):
            if st.session_state.balance >= bet_amt_2 and bet_amt_2 >= 30:
                new_bal = st.session_state.balance - bet_amt_2
                st.session_state.m2_bet_placed = True
                
                if conn:
                    try:
                        new_bet = pd.DataFrame([{"Mobile Number": st.session_state.user_phone, "Question": st.session_state.q2, "Selection": st.session_state.m2_selection, "Amount": bet_amt_2, "Status": "Pending"}])
                        conn.create(spreadsheet=GSHEET_URL, worksheet="Bets", data=new_bet)
                        
                        all_users = fetch_users_db()
                        all_users.loc[all_users['Mobile Number'] == str(st.session_state.user_phone), 'Balance'] = new_bal
                        conn.update(spreadsheet=GSHEET_URL, worksheet="Users", data=all_users)
                        
                        st.session_state.balance = new_bal
                        st.success(f"Bet Locked! Data pushed to Sheet.")
                        st.rerun()
                    except:
                        st.error("Database was busy.")
            else:
                st.error("❌ Insufficient Balance! Minimum PKR 30 required. Please go to 'Investor Wallet' to add money via EasyPaisa.")
    st.markdown('</div>', unsafe_allow_html=True)

# WORKSPACE B: RESULTS LEDGER
elif current_page == "User Dashboard (Results)":
    st.title("📅 Settlement Matrix & Performance Results")
    st.caption("Peeche Google Sheet se results change hote hi yahan dashboard automatically update ho jata hai.")
    
    if not st.session_state.logged_in:
        st.warning("Please sign in from the gateway sidebar to view your profile results ledger.")
    else:
        st.subheader("Live History Log Tracking")
        if conn:
            try:
                st.cache_data.clear()
                all_bets = conn.read(spreadsheet=GSHEET_URL, worksheet="Bets", ttl=0)
                user_bets = all_bets[all_bets['Mobile Number'].astype(str).str.strip() == str(st.session_state.user_phone).strip()]
                
                if user_bets.empty:
                    st.info("Aapne abhi tak koi bet lock nahi ki.")
                else:
                    for idx, row in user_bets.iterrows():
                        st.markdown('<div class="premium-border-box">', unsafe_allow_html=True)
                        st.markdown(f"❓ **Question:** {row['Question']}")
                        st.markdown(f"Your Prediction: **{row['Selection']}** | Amount Staked: **PKR {row['Amount']}** | Status: `{row['Status']}`")
                        st.markdown('</div>', unsafe_allow_html=True)
            except:
                st.info("History display pipeline is sleeping. Add a 'Bets' worksheet tab to active.")

# WORKSPACE C: INVESTOR WALLET MANAGEMENT
elif current_page == "Investor Wallet":
    st.title("💰 Capital Allocation & Liquidity")
    
    w_col1, w_col2 = st.columns(2)
    w_col1.metric("Liquid Balance Pool", f"PKR {st.session_state.balance:,.2f}")
    w_col2.metric("Database Pipeline Connection", "Live Sync Active ✅")

    st.markdown("---")
    dep_panel, with_panel = st.columns(2)
    
    with dep_panel:
        st.subheader("💳 Deposit Funds")
        
        st.markdown("""
        <div class="admin-account-box">
            <p style="color:#66ff00; font-weight:bold; margin-bottom:5px;">⚠️ OFFICIAL EASYPAISA DEPOSIT SLOT:</p>
            <p style="margin:2px 0; font-size:1.2rem;"><b>EasyPaisa Account:</b> 03415687754</p>
            <p style="margin:2px 0; color:#aaa; font-size:0.9rem;">Account Title: <b>Rabia Hafeez</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        wallet_number = st.text_input("Your Account Mobile Number", placeholder="e.g. 03415687754")
        account_title = st.text_input("Your Account Title Name", placeholder="e.g. Ali Khan")
        dep_amount = st.number_input("Transfer Amount (PKR)", min_value=30, step=50, key="wallet_dep_amt")
        trx_id = st.text_input("Transaction ID (TrxID)", placeholder="e.g. 8945729104", key="wallet_trx")
        
        st.markdown('<div class="sidebar-glowing-btn">', unsafe_allow_html=True)
        if st.button("Submit Deposit Proof"):
            if trx_id and wallet_number and account_title and dep_amount >= 30:
                if conn:
                    try:
                        # Append to Deposits Worksheet tab
                        new_dep = pd.DataFrame([{"Mobile Number": st.session_state.user_phone, "Network": "EasyPaisa", "Account Title": account_title, "Amount": dep_amount, "TrxID": trx_id, "Status": "Pending"}])
                        conn.create(spreadsheet=GSHEET_URL, worksheet="Deposits", data=new_dep)
                        st.success(f"Deposit proof pushed to Sheet! Admin (Rabia Hafeez) verifies it soon.")
                    except:
                        st.error("Database connection issue. Proof not saved.")
            else:
                st.error("Please fill out all credentials correctly (Min Rs. 30).")
        st.markdown('</div>', unsafe_allow_html=True)
                
    with with_panel:
        st.subheader("Withdraw Rewards")
        with_number = st.text_input("Withdrawal EasyPaisa Number", placeholder="e.g. 03415687754", key="w_num")
        with_amount = st.number_input("Withdraw Amount (PKR)", min_value=0, step=50, key="wallet_with_amt")
        
        st.markdown('<div class="sidebar-glowing-btn">', unsafe_allow_html=True)
        if st.button("Authorize Liquidation"):
            if with_amount > 0 and with_amount <= st.session_state.balance:
                if conn:
                    try:
                        new_with = pd.DataFrame([{"Mobile Number": st.session_state.user_phone, "Network": "EasyPaisa", "Account Number": with_number, "Amount": with_amount, "Status": "Pending"}])
                        conn.create(spreadsheet=GSHEET_URL, worksheet="Withdrawals", data=new_with)
                        st.success(f"Liquidation request dispatched to Sheet.")
                    except:
                        st.error("Failed to post withdrawal log.")
            else:
                st.error("Insufficient balance pool.")
        st.markdown('</div>', unsafe_allow_html=True)
