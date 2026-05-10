import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Page Configuration
st.set_page_config(page_title="Predict & Earn | Official", page_icon="💰", layout="wide")

# 2. Database Connection Settings
# Make sure the Sheet is set to "Anyone with the link" -> "Editor/Viewer"
SHEET_ID = "1EWrF_vJOIXyN7Y03t6rVECmY_YijC3nping9DoNnC-4"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=10) # Refresh data every 10 seconds
def fetch_database():
    try:
        response = requests.get(SHEET_URL)
        if response.status_code == 200:
            data = pd.read_csv(StringIO(response.text))
            # Clean column names to prevent matching errors
            data.columns = data.columns.str.strip().str.lower()
            return data
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

# Load initial data
df = fetch_database()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- App Header & Visuals ---
col_logo, col_text = st.columns([1, 5])
with col_logo:
    st.image("https://cdn-icons-png.flaticon.com/512/3209/3209935.png", width=80)
with col_text:
    st.title("Predict & Earn Rewards")
    st.write("The most trusted prediction platform.")

# --- Sidebar Authentication ---
st.sidebar.header("Member Access")

if not st.session_state.logged_in:
    tab_login, tab_reg = st.sidebar.tabs(["Login", "Register"])
    
    with tab_reg:
        st.subheader("Join the Platform")
        st.image("https://img.freepik.com/free-vector/sign-up-concept-illustration_114360-7885.jpg", width=150)
        reg_name = st.text_input("Full Name", key="reg_name")
        reg_phone = st.text_input("Mobile No (EasyPaisa)", key="reg_phone")
        
        if st.button("Get Started", use_container_width=True):
            st.info("Registration is handled by Admin. Contact us on WhatsApp to activate.")

    with tab_login:
        st.subheader("Welcome Back")
        l_phone = st.text_input("Mobile Number", key="login_phone")
        l_pass = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Sign In", type="primary", use_container_width=True):
            if not df.empty and 'phone' in df.columns:
                # Standardizing for login check
                df['phone'] = df['phone'].astype(str)
                df['password'] = df['password'].astype(str)
                
                user_match = df[(df['phone'] == str(l_phone)) & (df['password'] == str(l_pass))]
                
                if not user_match.empty:
                    st.session_state.logged_in = True
                    st.session_state.user_name = user_match.iloc[0]['name']
                    st.session_state.balance = user_match.iloc[0]['balance']
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please check your number/password.")
            else:
                st.error("Database connection failed. Check your Sheet headers.")

else: # --- DASHBOARD ---
    st.sidebar.success(f"Hello, {st.session_state.user_name}!")
    st.sidebar.metric("Wallet Balance", f"PKR {st.session_state.balance}")
    
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    st.header("Today's Prediction Challenge")
    st.image("https://img.freepik.com/free-vector/data-analysis-concept-illustration_114360-1288.jpg", width=400)
    
    st.subheader("Will it rain in Lahore tonight?")
    stake = st.select_slider("Select Stake Amount (PKR):", options=[10, 20, 50, 100, 500])
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("YES - It will rain", use_container_width=True, type="primary"):
            st.success(f"Prediction Recorded: YES (PKR {stake})")
    with c2:
        if st.button("NO - Clear Sky", use_container_width=True):
            st.warning(f"Prediction Recorded: NO (PKR {stake})")

    with st.expander("View Platform Guidelines"):
        st.write("1. Results are updated every 24 hours.")
        st.write("2. Double your reward on correct predictions.")
