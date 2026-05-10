import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Page Config
st.set_page_config(page_title="Predict & Earn | Pro", page_icon="💰", layout="wide")

# 2. Database Read Link (Stable Method)
SHEET_ID = "1EWrF_vJOIXyN7Y03t6rVECmY_YijC3nping9DoNnC-4"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=5)
def fetch_data():
    try:
        response = requests.get(READ_URL)
        if response.status_code == 200:
            data = pd.read_csv(StringIO(response.text))
            data.columns = [c.strip().lower() for c in data.columns]
            return data
        return pd.DataFrame()
    except:
        return pd.DataFrame()

df = fetch_data()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- UI Interface ---
st.title("🎯 Predict & Earn Rewards")

st.sidebar.header("Member Access")

if not st.session_state.logged_in:
    tab_login, tab_reg = st.sidebar.tabs(["Login", "Register"])
    
    with tab_reg:
        st.subheader("Create Account")
        st.image("https://img.freepik.com/free-vector/sign-up-concept-illustration_114360-7885.jpg", width=200)
        
        r_name = st.text_input("Full Name", key="r_name")
        r_phone = st.text_input("Mobile Number", key="r_phone")
        r_pass = st.text_input("Password", type="password", key="r_pass")
        
        if st.button("Submit Registration", use_container_width=True, type="primary"):
            if r_name and r_phone and r_pass:
                st.success("Registration request received!")
                # WhatsApp link for instant registration support
                whatsapp_msg = f"Hi Admin, please register me: Name: {r_name}, Phone: {r_phone}, Pass: {r_pass}"
                st.markdown(f"[Click here to Activate via WhatsApp](https://wa.me/923415687754?text={whatsapp_msg})")
                st.info("Once Admin adds you to the sheet, you can Login instantly.")
            else:
                st.error("Please fill all fields.")

    with tab_login:
        st.subheader("Login")
        l_phone = st.text_input("Mobile Number", key="l_phone")
        l_pass = st.text_input("Password", type="password", key="l_pass")
        
        if st.button("Sign In Securely", type="primary", use_container_width=True):
            if not df.empty:
                # Force string matching to avoid leading zero issues
                df['phone'] = df['phone'].astype(str).str.strip()
                df['password'] = df['password'].astype(str).str.strip()
                
                user = df[(df['phone'] == str(l_phone).strip()) & (df['password'] == str(l_pass).strip())]
                
                if not user.empty:
                    st.session_state.logged_in = True
                    st.session_state.user_name = user.iloc[0]['name']
                    st.session_state.balance = user.iloc[0]['balance']
                    st.rerun()
                else:
                    st.error("User not found or Password incorrect.")
            else:
                st.error("Database is empty. Please add users to the Sheet.")

else: # --- DASHBOARD ---
    st.sidebar.success(f"Welcome, {st.session_state.user_name}!")
    st.sidebar.metric("Balance", f"PKR {st.session_state.balance}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.header("Today's Prediction")
    st.subheader("Will the Bitcoin price stay above $62,000?")
    stake = st.select_slider("Stake (PKR):", options=[10, 20, 50, 100])
    
    if st.button("Place Bet", type="primary"):
        st.success(f"Prediction locked for PKR {stake}!")
