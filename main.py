import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Page Config
st.set_page_config(page_title="Predict & Earn | Pro", page_icon="💰", layout="wide")

# 2. Database Read Link
SHEET_ID = "1EWrF_vJOIXyN7Y03t6rVECmY_YijC3nping9DoNnC-4"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=2)
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
        r_name = st.text_input("Full Name", key="r_name")
        r_phone = st.text_input("Mobile Number", key="r_phone", help="Enter number without starting 0 if you face issues.")
        r_pass = st.text_input("Password", type="password", key="r_pass")
        
        if st.button("Submit Registration", use_container_width=True, type="primary"):
            if r_name and r_phone and r_pass:
                st.success("Request received!")
                whatsapp_msg = f"Hi Admin, Register me: {r_name}, {r_phone}, {r_pass}"
                st.markdown(f"[Click to Activate via WhatsApp](https://wa.me/923415687754?text={whatsapp_msg})")
            else:
                st.error("Fill all fields.")

    with tab_login:
        st.subheader("Login")
        l_phone = st.text_input("Mobile Number", key="l_phone", placeholder="e.g. 3415687754")
        
        # --- HINT FOR USER ---
        st.caption("⚠️ **Hint:** Agar aapka login nahi ho raha, toh number ke shuru mein **'0'** lagaye baghair koshish karein (e.g., 341...).")
        
        l_pass = st.text_input("Password", type="password", key="l_pass")
        
        if st.button("Sign In Securely", type="primary", use_container_width=True):
            if not df.empty:
                # Cleaning database values (Removing spaces and converting to string)
                df['phone'] = df['phone'].astype(str).str.strip()
                df['password'] = df['password'].astype(str).str.strip()
                
                # Check 1: Direct Match
                input_phone = str(l_phone).strip()
                input_pass = str(l_pass).strip()
                
                # Check 2: Match without leading zero (if database stripped it)
                phone_no_zero = input_phone[1:] if input_phone.startswith('0') else input_phone
                
                user = df[((df['phone'] == input_phone) | (df['phone'] == phone_no_zero)) & 
                          (df['password'] == input_pass)]
                
                if not user.empty:
                    st.session_state.logged_in = True
                    st.session_state.user_name = user.iloc[0]['name']
                    st.session_state.balance = user.iloc[0]['balance']
                    st.rerun()
                else:
                    st.error("Login Fail: Number ya Password ghalat hai.")
            else:
                st.error("Database khali hai.")

else: # --- DASHBOARD ---
    st.sidebar.success(f"Welcome, {st.session_state.user_name}!")
    st.sidebar.metric("Balance", f"PKR {st.session_state.balance}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.header("Today's Prediction")
    st.image("https://img.freepik.com/free-vector/data-analysis-concept-illustration_114360-1288.jpg", width=400)
    st.subheader("Will the Bitcoin price stay above $62,000?")
    
    if st.button("Submit Prediction", type="primary"):
        st.success("Prediction Locked!")
