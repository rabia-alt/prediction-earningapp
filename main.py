import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Page Configuration
st.set_page_config(page_title="Predict & Earn | Official", page_icon="💰", layout="wide")

# 2. Database Connection Settings
SHEET_ID = "1EWrF_vJOIXyN7Y03t6rVECmY_YijC3nping9DoNnC-4"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=5) # Refresh every 5 seconds for fast updates
def fetch_database():
    try:
        response = requests.get(SHEET_URL)
        if response.status_code == 200:
            data = pd.read_csv(StringIO(response.text))
            # FIX: Convert all column names to lowercase automatically
            data.columns = [c.strip().lower() for c in data.columns]
            return data
        return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

# Load data
df = fetch_database()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- App Interface ---
st.title("🎯 Predict & Earn Rewards")
st.write("Professional English Interface | High Security")

# Sidebar
st.sidebar.header("Member Access")

if not st.session_state.logged_in:
    tab_login, tab_reg = st.sidebar.tabs(["Login", "Register"])
    
    with tab_reg:
        st.subheader("Join Now")
        st.image("https://img.freepik.com/free-vector/sign-up-concept-illustration_114360-7885.jpg", width=150)
        st.info("Registration is handled by Admin via WhatsApp.")

    with tab_login:
        st.subheader("Login")
        l_phone = st.text_input("Mobile Number", key="login_phone")
        l_pass = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Sign In Securely", type="primary", use_container_width=True):
            if not df.empty:
                # Making sure all types match (String to String comparison)
                df['phone'] = df['phone'].astype(str).str.strip()
                df['password'] = df['password'].astype(str).str.strip()
                
                # Check login
                user_match = df[(df['phone'] == str(l_phone).strip()) & (df['password'] == str(l_pass).strip())]
                
                if not user_match.empty:
                    st.session_state.logged_in = True
                    st.session_state.user_name = user_match.iloc[0]['name']
                    st.session_state.balance = user_match.iloc[0]['balance']
                    st.rerun()
                else:
                    st.error("Invalid credentials. Check your Mobile No or Password.")
            else:
                st.error("Database connection failed. Please check your internet or Sheet settings.")

else: # --- DASHBOARD ---
    st.sidebar.success(f"Welcome, {st.session_state.user_name}!")
    st.sidebar.metric("Your Balance", f"PKR {st.session_state.balance}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.header("Today's Prediction")
    st.image("https://img.freepik.com/free-vector/data-analysis-concept-illustration_114360-1288.jpg", width=400)
    
    st.subheader("Will Bitcoin price increase in next 1 hour?")
    stake = st.select_slider("Stake Amount (PKR):", options=[10, 20, 50, 100])
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("YES - Increase", use_container_width=True, type="primary"):
            st.success(f"Predicted YES (PKR {stake})")
    with c2:
        if st.button("NO - Decrease", use_container_width=True):
            st.warning(f"Predicted NO (PKR {stake})")
