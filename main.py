import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Page Config
st.set_page_config(page_title="Predict & Earn | Pro", page_icon="💰", layout="wide")

# 2. Connection
conn = st.connection("gsheets", type=GSheetsConnection)

# We use ttl=0 to ensure we always get the latest data from the sheet
def load_data():
    try:
        return conn.read(worksheet="Sheet1", ttl=0)
    except Exception as e:
        st.error("Connection Error: Please check if your Google Sheet is Shared as 'Editor'.")
        return pd.DataFrame()

df = load_data()

# Standardizing column names
if not df.empty:
    df.columns = [c.strip().lower() for c in df.columns]

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- UI ---
st.title("🎯 Predict & Earn Rewards")

st.sidebar.header("Member Access")

if not st.session_state.logged_in:
    tab_login, tab_reg = st.sidebar.tabs(["Login", "Register"])
    
    with tab_reg:
        st.subheader("Create Account")
        new_name = st.text_input("Full Name", key="reg_name")
        new_phone = st.text_input("Mobile Number", key="reg_phone")
        new_pass = st.text_input("Create Password", type="password", key="reg_pass")
        
        if st.button("Register Now", use_container_width=True):
            if new_name and new_phone and new_pass:
                # Clean checks
                existing_phones = df['phone'].astype(str).str.strip().values if not df.empty else []
                if str(new_phone).strip() in existing_phones:
                    st.warning("This number is already registered.")
                else:
                    new_user = pd.DataFrame([{
                        "name": new_name,
                        "phone": str(new_phone).strip(),
                        "password": str(new_pass).strip(),
                        "balance": 30
                    }])
                    updated_df = pd.concat([df, new_user], ignore_index=True)
                    conn.update(worksheet="Sheet1", data=updated_df)
                    st.success("Registration Successful! Please switch to Login tab.")
            else:
                st.error("Please fill all fields.")

    with tab_login:
        st.subheader("Login")
        l_phone = st.text_input("Mobile Number", key="login_phone")
        l_pass = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Sign In", type="primary", use_container_width=True):
            if not df.empty:
                # Force clean matching
                search_phone = str(l_phone).strip()
                search_pass = str(l_pass).strip()
                
                # Matching logic that ignores leading zeros or formatting issues
                match = df[
                    (df['phone'].astype(str).str.strip() == search_phone) & 
                    (df['password'].astype(str).str.strip() == search_pass)
                ]
                
                if not match.empty:
                    st.session_state.logged_in = True
                    st.session_state.user_name = match.iloc[0]['name']
                    st.session_state.balance = match.iloc[0]['balance']
                    st.rerun()
                else:
                    st.error("User not found or Password incorrect.")
            else:
                st.error("No user data found in database.")

else:
    st.sidebar.success(f"Welcome, {st.session_state.user_name}!")
    st.sidebar.metric("Your Balance", f"PKR {st.session_state.balance}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.header("Today's Prediction")
    st.image("https://img.freepik.com/free-vector/data-analysis-concept-illustration_114360-1288.jpg", width=400)
    st.subheader("Will Bitcoin price be above $65,000 tonight?")
    
    stake = st.select_slider("Select Stake (PKR):", options=[10, 20, 50, 100])
    if st.button("Place Prediction", type="primary"):
        st.success(f"Success! PKR {stake} bet has been placed.")
