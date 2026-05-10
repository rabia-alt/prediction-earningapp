import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Page Config
st.set_page_config(page_title="Predict & Earn | Pro", page_icon="💰", layout="wide")

# 2. Establish Connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Function to load data
def load_data():
    return conn.read(worksheet="Sheet1", ttl=0)

# Load existing data
try:
    df = load_data()
    # Clean column names
    df.columns = [c.strip().lower() for c in df.columns]
except Exception as e:
    st.error("Database connection failed. Please check your Secrets and Sheet permissions.")
    st.stop()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- App Interface ---
st.title("🎯 Predict & Earn Rewards")

# Sidebar
st.sidebar.header("Member Access")

if not st.session_state.logged_in:
    tab_login, tab_reg = st.sidebar.tabs(["Login", "Register"])
    
    with tab_reg: # --- AUTOMATIC REGISTRATION ---
        st.subheader("Create Account")
        new_name = st.text_input("Full Name", key="reg_name")
        new_phone = st.text_input("Mobile Number", key="reg_phone")
        new_pass = st.text_input("Create Password", type="password", key="reg_pass")
        
        if st.button("Register & Get PKR 30", use_container_width=True):
            if new_phone in df['phone'].astype(str).values:
                st.warning("This number is already registered. Please Login.")
            elif new_name and new_phone and new_pass:
                # Add new user to the list
                new_data = pd.DataFrame([{
                    "name": new_name,
                    "phone": str(new_phone),
                    "password": str(new_pass),
                    "balance": 30
                }])
                updated_df = pd.concat([df, new_data], ignore_index=True)
                
                # Save back to Google Sheets
                conn.update(worksheet="Sheet1", data=updated_df)
                st.success("Registration Successful! You can now Login.")
                st.balloons()
            else:
                st.error("Please fill all details correctly.")

    with tab_login: # --- DIRECT LOGIN ---
        st.subheader("Login")
        l_phone = st.text_input("Mobile Number", key="login_phone")
        l_pass = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Sign In", type="primary", use_container_width=True):
            # Clean data for matching
            df['phone'] = df['phone'].astype(str).str.strip()
            df['password'] = df['password'].astype(str).str.strip()
            
            user = df[(df['phone'] == str(l_phone).strip()) & (df['password'] == str(l_pass).strip())]
            
            if not user.empty:
                st.session_state.logged_in = True
                st.session_state.user_name = user.iloc[0]['name']
                st.session_state.balance = user.iloc[0]['balance']
                st.session_state.user_phone = str(l_phone)
                st.rerun()
            else:
                st.error("Invalid credentials. Try again.")

else: # --- DASHBOARD ---
    st.sidebar.success(f"Welcome, {st.session_state.user_name}!")
    st.sidebar.metric("Wallet Balance", f"PKR {st.session_state.balance}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.header("Today's Prediction")
    st.image("https://img.freepik.com/free-vector/data-analysis-concept-illustration_114360-1288.jpg", width=400)
    
    st.subheader("Will Gold price increase today?")
    stake = st.select_slider("Stake Amount (PKR):", options=[10, 20, 50, 100])
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("YES - Increase", use_container_width=True, type="primary"):
            st.success(f"Prediction Recorded: YES (PKR {stake})")
    with c2:
        if st.button("NO - Decrease", use_container_width=True):
            st.warning(f"Prediction Recorded: NO (PKR {stake})")
