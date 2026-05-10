import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Page Config
st.set_page_config(page_title="Predict & Earn", page_icon="💰")

# 2. Google Sheet CSV Export Link
SHEET_ID = "1EWrF_vJOIXyN7Y03t6rVECmY_YijC3nping9DoNnC-4"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

def get_data():
    try:
        response = requests.get(SHEET_URL)
        if response.status_code == 200:
            return pd.read_csv(StringIO(response.text))
        return pd.DataFrame()
    except:
        return pd.DataFrame()

df = get_data()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

st.title("🎯 Prediction & Reward App")

st.sidebar.header("User Panel")

if not st.session_state.logged_in:
    tab1, tab2 = st.sidebar.tabs(["Login", "Sign Up"])
    
    with tab2: # --- SIGN UP ---
        st.subheader("Naya Account")
        n_name = st.text_input("Naam", key="signup_name")
        # Yahan humne key badal di hai
        n_phone = st.text_input("Mobile No", key="signup_phone")
        n_pass = st.text_input("Password", type="password", key="signup_pass")
        
        if st.button("Register Now", key="signup_btn"):
            st.info("Registration ke liye Admin se rabta karen.")

    with tab1: # --- LOGIN ---
        st.subheader("Login")
        # Yahan bhi unique key laga di hai
        l_phone = st.text_input("Mobile No", key="login_phone")
        l_pass = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login", key="login_btn"):
            if not df.empty and 'phone' in df.columns:
                # Convert to string for matching
                df['phone'] = df['phone'].astype(str)
                df['password'] = df['password'].astype(str)
                
                user = df[(df['phone'] == str(l_phone)) & (df['password'] == str(l_pass))]
                if not user.empty:
                    st.session_state.logged_in = True
                    st.session_state.user_name = user.iloc[0]['name']
                    st.session_state.balance = user.iloc[0]['balance']
                    st.rerun()
                else:
                    st.error("Ghalat Password ya Number!")
            else:
                st.error("Data load nahi ho raha!")

else:
    st.sidebar.success(f"Welcome {st.session_state.user_name}")
    st.sidebar.write(f"💰 Balance: RS {st.session_state.balance}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.header("Aaj ka Sawal")
    st.write("Kya aaj Pakistan match jeetay ga?")
    if st.button("YES"):
        st.success("Bet Lag Gayi!")
