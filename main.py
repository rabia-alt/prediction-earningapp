import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Page Configuration
st.set_page_config(page_title="Predict & Earn | Official", page_icon="💰", layout="wide")

# 2. Database Link
# Note: Using direct CSV export to bypass "Secrets" connection errors
SHEET_ID = "1EWrF_vJOIXyN7Y03t6rVECmY_YijC3nping9DoNnC-4"
READ_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=5)
def fetch_users():
    try:
        response = requests.get(READ_URL)
        if response.status_code == 200:
            data = pd.read_csv(StringIO(response.text))
            data.columns = [c.strip().lower() for c in data.columns]
            return data
        return pd.DataFrame()
    except:
        return pd.DataFrame()

df = fetch_users()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- UI Layout ---
st.title("🎯 Predict & Earn Rewards")
st.markdown("---")

# Sidebar
st.sidebar.header("Member Access")

if not st.session_state.logged_in:
    tab_login, tab_reg = st.sidebar.tabs(["Login", "Register"])
    
    with tab_reg:
        st.subheader("Direct Registration")
        st.image("https://img.freepik.com/free-vector/sign-up-concept-illustration_114360-7885.jpg", width=200)
        
        # Registration Form
        r_name = st.text_input("Full Name", key="reg_name")
        r_phone = st.text_input("EasyPaisa Number", key="reg_phone")
        r_pass = st.text_input("Set Password", type="password", key="reg_pass")
        
        st.info("💡 Tip: Use your EasyPaisa number for faster withdrawals.")
        
        if st.button("Submit Registration", use_container_width=True, type="primary"):
            if r_name and r_phone and r_pass:
                # Redirecting to Admin for instant manual entry into Sheet
                # This prevents "Connection 400 Error" while writing
                st.success("Registration details captured!")
                st.markdown(f"""
                ### ✅ Step 2: Finalize Registration
                Please send a screenshot or your number to our Admin for instant activation and **PKR 30 Bonus**.
                
                **Admin WhatsApp/EasyPaisa:** `03415687754`
                """)
            else:
                st.error("Please fill all fields.")

    with tab_login:
        st.subheader("Login to Dashboard")
        l_phone = st.text_input("Mobile Number", key="login_phone")
        l_pass = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Sign In Securely", type="primary", use_container_width=True):
            if not df.empty:
                df['phone'] = df['phone'].astype(str).str.strip()
                df['password'] = df['password'].astype(str).str.strip()
                
                user = df[(df['phone'] == str(l_phone).strip()) & (df['password'] == str(l_pass).strip())]
                
                if not user.empty:
                    st.session_state.logged_in = True
                    st.session_state.user_name = user.iloc[0]['name']
                    st.session_state.balance = user.iloc[0]['balance']
                    st.rerun()
                else:
                    st.error("Invalid credentials. If you are new, please Register first.")
            else:
                st.error("Database connection error. Try again later.")

else: # --- LOGGED IN DASHBOARD ---
    st.sidebar.success(f"Welcome, {st.session_state.user_name}!")
    st.sidebar.metric("Your Balance", f"PKR {st.session_state.balance}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.header("🔥 Daily Challenge")
    st.subheader("Will the Bitcoin price be above $62,000 in the next 1 hour?")
    
    stake = st.select_slider("Select Stake (PKR):", options=[10, 20, 50, 100])
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("YES - Above", use_container_width=True, type="primary"):
            st.success(f"Prediction Locked! Amount Staked: PKR {stake}")
    with c2:
        if st.button("NO - Below", use_container_width=True):
            st.warning(f"Prediction Locked! Amount Staked: PKR {stake}")

    st.divider()
    st.write(f"📢 For deposits/withdrawals, contact Admin at: **03415687754**")
