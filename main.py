import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Page Title
st.set_page_config(page_title="Predict & Earn", page_icon="💰")

# 2. Google Sheet Link (Short format for better connection)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1EWrF_vJOIXyN7Y03t6rVECmY_YijC3nping9DoNnC-4/edit"

# 3. Connection Setup
conn = st.connection("gsheets", type=GSheetsConnection)

# 4. Data Load Karne ka Function
def get_data():
    # ttl=0 ka matlab hai har baar fresh data uthaye
    return conn.read(spreadsheet=SHEET_URL, worksheet="Sheet1", ttl=0)

# Load data initially
try:
    df = get_data()
    # Cleaning data: Ensure columns are strings to avoid errors
    df['phone'] = df['phone'].astype(str)
    df['password'] = df['password'].astype(str)
except Exception as e:
    st.error(f"Database Connect Nahi Ho Raha! Error: {e}")
    st.stop()

# --- APP INTERFACE ---
st.title("🎯 Prediction & Reward App")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Sidebar
st.sidebar.header("User Panel")

if not st.session_state.logged_in:
    tab1, tab2 = st.sidebar.tabs(["Login", "Sign Up"])
    
    with tab2: # --- SIGN UP SECTION ---
        st.subheader("Naya Account")
        new_name = st.text_input("Apna Naam")
        new_phone = st.text_input("Mobile Number")
        new_pass = st.text_input("Password", type="password")
        
        if st.button("Register & Get 30 RS"):
            if new_phone in df['phone'].values:
                st.error("Ye number pehle se mojood hai!")
            elif new_name and new_phone and new_pass:
                # Naya data banana
                new_row = pd.DataFrame([{
                    "name": new_name, 
                    "phone": str(new_phone), 
                    "password": str(new_pass), 
                    "balance": 30
                }])
                # Sheet update karna
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(spreadsheet=SHEET_URL, worksheet="Sheet1", data=updated_df)
                st.success("Registration Kamyab! Ab Login tab par jayein.")
                st.cache_data.clear() # Data refresh karein
            else:
                st.error("Sari malomat bharein!")

    with tab1: # --- LOGIN SECTION ---
        st.subheader("Login Karen")
        l_phone = st.text_input("Mobile No", key="login_phone")
        l_pass = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login"):
            user = df[(df['phone'] == str(l_phone)) & (df['password'] == str(l_pass))]
            if not user.empty:
                st.session_state.logged_in = True
                st.session_state.user_phone = str(l_phone)
                st.session_state.user_name = user.iloc[0]['name']
                st.rerun()
            else:
                st.error("Number ya Password galat hai!")

else: # --- LOGGED IN USER DASHBOARD ---
    # Refresh user data to get latest balance
    current_df = get_data()
    user_row = current_df[current_df['phone'] == st.session_state.user_phone].iloc[0]
    balance = user_row['balance']
    
    st.sidebar.success(f"Khush Amdeed, {st.session_state.user_name}!")
    st.sidebar.metric("Aapka Balance", f"RS {balance}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # Prediction Area
    st.header("🔥 Aaj ka Sawal")
    st.subheader("Kya kal Gold ka rate sasta hoga?")
    
    bet = st.radio("Kitne paise lagane hain?", [10, 20, 50, 100], horizontal=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("YES ✅"):
            if balance >= bet:
                # Update balance in dataframe
                current_df.loc[current_df['phone'] == st.session_state.user_phone, 'balance'] = balance - bet
                conn.update(spreadsheet=SHEET_URL, worksheet="Sheet1", data=current_df)
                st.success(f"RS {bet} lag gaye! Dua karein.")
                st.cache_data.clear()
                st.rerun()
            else:
                st.error("Balance kam hai! Recharge karein.")

    with col2:
        if st.button("NO ❌"):
            if balance >= bet:
                current_df.loc[current_df['phone'] == st.session_state.user_phone, 'balance'] = balance - bet
                conn.update(spreadsheet=SHEET_URL, worksheet="Sheet1", data=current_df)
                st.warning(f"RS {bet} lag gaye! Result ka intezar karein.")
                st.cache_data.clear()
                st.rerun()
            else:
                st.error("Balance kam hai!")
