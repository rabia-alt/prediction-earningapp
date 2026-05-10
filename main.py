import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Page Title
st.set_page_config(page_title="Predict & Earn", page_icon="💰")

# 2. Google Sheet Link (CLEAN FORMAT)
# Agar niche wala link masla kare, toh bas "/edit" tak hi rehne den
SHEET_URL = "https://docs.google.com/spreadsheets/d/1EWrF_vJOIXyN7Y03t6rVECmY_YijC3nping9DoNnC-4/edit#gid=0"

# 3. Connection Setup
conn = st.connection("gsheets", type=GSheetsConnection)

# 4. Data Load Karne ka Function
def get_data():
    # Hum yahan spreadsheet aur worksheet dono specify kar rahe hain
    return conn.read(spreadsheet=SHEET_URL, worksheet="Sheet1", ttl="0")

# Load data initially
try:
    df = get_data()
    # Ensure columns exist even if sheet is empty
    if df.empty:
        df = pd.DataFrame(columns=['name', 'phone', 'password', 'balance'])
    
    df['phone'] = df['phone'].astype(str)
    df['password'] = df['password'].astype(str)
except Exception as e:
    st.error(f"Database Error: {e}")
    st.info("Pehli Row (Header) mein 'name', 'phone', 'password', 'balance' hona lazmi hai.")
    st.stop()

# --- APP INTERFACE ---
st.title("🎯 Prediction & Reward App")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Sidebar
st.sidebar.header("User Panel")

if not st.session_state.logged_in:
    tab1, tab2 = st.sidebar.tabs(["Login", "Sign Up"])
    
    with tab2: # --- SIGN UP ---
        new_name = st.text_input("Apna Naam")
        new_phone = st.text_input("Mobile Number")
        new_pass = st.text_input("Password", type="password")
        
        if st.button("Register & Get 30 RS"):
            if new_phone in df['phone'].values:
                st.error("Ye number pehle se mojood hai!")
            elif new_name and new_phone and new_pass:
                new_row = pd.DataFrame([{
                    "name": new_name, 
                    "phone": str(new_phone), 
                    "password": str(new_pass), 
                    "balance": 30
                }])
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(spreadsheet=SHEET_URL, worksheet="Sheet1", data=updated_df)
                st.success("Account Ban Gaya! Ab Login Karen.")
                st.cache_data.clear()
            else:
                st.error("Sari detail likhen!")

    with tab1: # --- LOGIN ---
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
                st.error("Ghalat Password!")

else: # --- DASHBOARD ---
    user_row = df[df['phone'] == st.session_state.user_phone].iloc[0]
    balance = user_row['balance']
    
    st.sidebar.success(f"Khush Amdeed, {st.session_state.user_name}!")
    st.sidebar.metric("Aapka Balance", f"RS {balance}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.header("🔥 Aaj ka Sawal")
    st.subheader("Kya Pakistan kal jeetay ga?")
    bet = st.radio("Bet Amount:", [10, 20, 50, 100], horizontal=True)
    
    if st.button("Submit Prediction"):
        if balance >= bet:
            df.loc[df['phone'] == st.session_state.user_phone, 'balance'] = balance - bet
            conn.update(spreadsheet=SHEET_URL, worksheet="Sheet1", data=df)
            st.success("Lag Gaye!")
            st.cache_data.clear()
            st.rerun()
        else:
            st.error("Paisa Kam Hai!")
