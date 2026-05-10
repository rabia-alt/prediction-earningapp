import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Page Config
st.set_page_config(page_title="Predict & Earn | Official App", page_icon="💰", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .big-font { font-size:24px !important; font-weight: 700; color: #2c3e50; }
    .metric-card { background-color: #f8f9fa; border-radius: 10px; padding: 20px; border: 1px solid #e9ecef; }
</style>
""", unsafe_allow_html=True)

# 2. Google Sheet CSV Export Link
SHEET_ID = "1EWrF_vJOIXyN7Y03t6rVECmY_YijC3nping9DoNnC-4"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=60) # Cache data for 60 seconds
def get_data():
    try:
        response = requests.get(SHEET_URL)
        if response.status_code == 200:
            return pd.read_csv(StringIO(response.text))
        return pd.DataFrame()
    except:
        return pd.DataFrame()

# Load Data
df = get_data()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- Main App Header ---
col_header1, col_header2 = st.columns([1, 6])
with col_header1:
    # High-quality related icon
    st.image("https://cdn-icons-png.flaticon.com/512/3209/3209935.png", width=100)
with col_header2:
    st.markdown('<p class="big-font">Predict & Earn | Daily Rewards</p>', unsafe_allow_html=True)
    st.write("Analyze, Predict, and Win Rewards Daily!")

# --- Sidebar Panel ---
st.sidebar.header("Control Panel")

if not st.session_state.logged_in:
    auth_tab1, auth_tab2 = st.sidebar.tabs(["🔒 Secure Login", "📝 New Account"])
    
    with auth_tab2: # --- REGISTRATION ---
        st.subheader("Register with EasyPaisa")
        reg_name = st.text_input("Full Name", key="signup_name", help="Enter your legal name")
        reg_phone = st.text_input("Mobile Number", key="signup_phone", help="EasyPaisa/JazzCash number")
        reg_pass = st.text_input("Password", type="password", key="signup_pass")
        
        if st.button("Create Account & Claim PKR 30", key="signup_btn", use_container_width=True):
            # Professional Registration Image
            st.image("https://img.freepik.com/free-vector/sign-up-concept-illustration_114360-7885.jpg?t=st=1715363400~exp=1715367000~hmac=a40498b58a1005d76d4984f475f4585c575005d54a2a222c1d3550e69b596281", caption="Almost there!")
            st.info("Registration is currently managed by Support. Contact us with your details for quick activation.")
            st.markdown(f"**Your Submitted Number:** `{reg_phone}`")

    with auth_tab1: # --- LOGIN ---
        st.subheader("Login to Your Dashboard")
        login_phone = st.text_input("Mobile Number", key="login_phone")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login Securely", key="login_btn", use_container_width=True):
            if not df.empty and 'phone' in df.columns:
                # Standardizing data for comparison
                df['phone'] = df['phone'].astype(str)
                df['password'] = df['password'].astype(str)
                
                user = df[(df['phone'] == str(login_phone)) & (df['password'] == str(login_pass))]
                if not user.empty:
                    st.session_state.logged_in = True
                    st.session_state.user_name = user.iloc[0]['name']
                    st.session_state.balance = user.iloc[0]['balance']
                    st.session_state.user_phone = str(login_phone)
                    st.rerun()
                else:
                    st.error("Access Denied: Invalid Number or Password.")
            else:
                st.error("Service Error: Unable to connect to the database. Try again later.")

else: # --- LOGGED IN DASHBOARD ---
    st.sidebar.success(f"Welcome, {st.session_state.user_name}!")
    
    # Professional metric inside a container
    with st.sidebar.container():
        st.metric("Wallet Balance", f"PKR {st.session_state.balance}")
    
    if st.sidebar.button("Log Out Securely", key="logout_btn", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    # --- Main App Content (Dashboard) ---
    st.image("https://img.freepik.com/free-vector/data-analysis-concept-illustration_114360-1288.jpg", caption="Analyze the Data Before You Predict!")
    
    st.header("🔥 Today's Hot Prediction")
    st.subheader("Will the Bitcoin price close above $65,000 tonight?")
    
    bet_amount = st.radio("Select Your Stake (PKR):", [10, 20, 50, 100], horizontal=True)
    
    col_bet1, col_bet2 = st.columns(2)
    with col_bet1:
        if st.button("YES - Above $65k", key="bet_yes", use_container_width=True, type="primary"):
            st.success(f"✅ Prediction locked: YES. PKR {bet_amount} staked.")
            
    with col_bet2:
        if st.button("NO - Below $65k", key="bet_no", use_container_width=True):
            st.warning(f"✅ Prediction locked: NO. PKR {bet_amount} staked.")

    st.divider()
    # Relevant Rules/Info Image
    with st.expander("📌 Official Rules & Guidelines", expanded=True):
        col_rules1, col_rules2 = st.columns([1, 3])
        with col_rules1:
            st.image("https://img.freepik.com/free-vector/rules-concept-illustration_114360-1926.jpg", caption="Play Fair")
        with col_rules2:
            st.markdown("""
            * One prediction per account daily.
            * Staked amount is deducted instantly.
            * Correct prediction doubles your stake (minus 5% commission).
            * Minimum Withdrawal: PKR 500.
            * Results are announced daily at 12:00 AM.
            """)
