import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Page setup
st.set_page_config(page_title="Predict & Earn", page_icon="💰")

# Google Sheet Direct Link (Secrets ke baghair)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1EWrF_vJOIXyN7Y03t6rVECmY_YijC3nping9DoNnC-4/edit?usp=sharing"

# Connection setup
conn = st.connection("gsheets", type=GSheetsConnection)

def get_data():
    # Direct link se data read karne ke liye spreadsheet parameter use kiya hai
    return conn.read(spreadsheet=SHEET_URL, worksheet="Sheet1", ttl=0)

# Load data
try:
    df = get_data()
except Exception as e:
    st.error(f"Data load nahi ho raha. Error: {e}")
    st.stop()

# --- Baki Sara App Code ---
st.title("🎯 Prediction & Reward App")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Sidebar logic
st.sidebar.header("User Panel")

if not st.session_state.logged_in:
    tab1, tab2 = st.sidebar.tabs(["Login", "Sign Up"])
    
    with tab2: # Sign Up
        new_name = st.text_input("Naam")
        new_phone = st.text_input("Mobile Number")
        new_pass = st.text_input("Password", type="password")
        if st.button("Register & Get 30 RS"):
            if new_phone in df['phone'].astype(str).values:
                st.error("Ye number pehle se majood hai!")
            elif new_name and new_phone and new_pass:
                new_row = pd.DataFrame([{"name": new_name, "phone": new_phone, "password": new_pass, "balance": 30}])
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(spreadsheet=SHEET_URL, worksheet="Sheet1", data=updated_df)
                st.success("Account ban gaya! Ab Login karen.")
                st.cache_data.clear() # Refresh data
            else:
                st.error("Sari details likhen!")

    with tab1: # Login
        l_phone = st.text_input("Mobile No")
        l_pass = st.text_input("Password", type="password")
        if st.button("Login"):
            user = df[(df['phone'].astype(str) == l_phone) & (df['password'].astype(str) == l_pass)]
            if not user.empty:
                st.session_state.logged_in = True
                st.session_state.user_phone = l_phone
                st.session_state.user_name = user.iloc[0]['name']
                st.rerun()
            else:
                st.error("Galat Number ya Password!")
else:
    # User Dashboard
    user_row = df[df['phone'].astype(str) == st.session_state.user_phone].iloc[0]
    balance = user_row['balance']
    
    st.sidebar.write(f"👤 **User:** {st.session_state.user_name}")
    st.sidebar.subheader(f"💰 Balance: RS {balance}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.header("🔥 Aaj ka Sawal")
    st.subheader("Kya aaj Pakistan match jitega?")
    bet = st.radio("Bet lagayein:", [10, 20, 50, 100], horizontal=True)
    
    if st.button("Submit Prediction"):
        if balance >= bet:
            df.loc[df['phone'].astype(str) == st.session_state.user_phone, 'balance'] = balance - bet
            conn.update(spreadsheet=SHEET_URL, worksheet="Sheet1", data=df)
            st.success(f"RS {bet} lag gaye!")
            st.cache_data.clear()
            st.rerun()
        else:
            st.error("Balance kam hai!")
