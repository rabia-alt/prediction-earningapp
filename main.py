import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Page Configuration
st.set_page_config(page_title="Predict & Earn | Official", page_icon="💰", layout="wide")

# 2. Direct Database Connection (Replacing Secrets)
SHEET_ID = "1EWrF_vJOIXyN7Y03t6rVECmY_YijC3nping9DoNnC-4"
# Export URL for reading data
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=5)
def fetch_database():
    try:
        response = requests.get(READ_URL)
        if response.status_code == 200:
            data = pd.read_csv(StringIO(response.text))
            # Automatically convert column headers to lowercase
            data.columns = [c.strip().lower() for c in data.columns]
            return data
        return pd.DataFrame()
    except Exception:
        return pd.DataFrame()

# Load data
df = fetch_database()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- App Header ---
st.title("🎯 Predict & Earn Rewards")
st.markdown("---")

# --- Sidebar Controls ---
st.sidebar.header("Member Access")

if not st.session_state.logged_in:
    tab_login, tab_reg = st.sidebar.tabs(["Login", "Register"])
    
    with tab_reg:
        st.subheader("Join the Platform")
        st.image("https://img.freepik.com/free-vector/sign-up-concept-illustration_114360-7885.jpg", width=200)
        st.info("Registration is currently managed by Admin for security. Please send your details via WhatsApp.")

    with tab_login:
        st.subheader("Account Login")
        l_phone = st.text_input("Mobile Number", key="login_phone")
        l_pass = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Sign In Now", type="primary", use_container_width=True):
            if not df.empty and 'phone' in df.columns:
                # Clean strings for exact matching
                df['phone'] = df['phone'].astype(str).str.strip()
                df['password'] = df['password'].astype(str).str.strip()
                
                user_match = df[(df['phone'] == str(l_phone).strip()) & (df['password'] == str(l_pass).strip())]
                
                if not user_match.empty:
                    st.session_state.logged_in = True
                    st.session_state.user_name = user_match.iloc[0]['name']
                    st.session_state.balance = user_match.iloc[0]['balance']
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please check your number or password.")
            else:
                st.error("Database connection issue. Please ensure your Sheet has headers.")

else: # --- DASHBOARD ---
    st.sidebar.success(f"Welcome, {st.session_state.user_name}!")
    st.sidebar.metric("Your Balance", f"PKR {st.session_state.balance}")
    
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    st.header("🔥 Today's Prediction")
    st.image("https://img.freepik.com/free-vector/data-analysis-concept-illustration_114360-1288.jpg", width=400)
    
    st.subheader("Will the Bitcoin price cross $65,000 tonight?")
    stake = st.select_slider("Select Stake (PKR):", options=[10, 20, 50, 100])
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("YES", use_container_width=True, type="primary"):
            st.success(f"Prediction Locked: YES (PKR {stake})")
    with c2:
        if st.button("NO", use_container_width=True):
            st.warning(f"Prediction Locked: NO (PKR {stake})")
