import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. Page Config
st.set_page_config(page_title="Predict & Earn", page_icon="💰")

# 2. Google Sheet CSV Export Link
# Hum Sheet ko as a CSV parhen ge, is se error nahi ata
SHEET_ID = "1EWrF_vJOIXyN7Y03t6rVECmY_YijC3nping9DoNnC-4"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# Function to get data
def get_data():
    response = requests.get(SHEET_URL)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        st.error("Google Sheet se data nahi mil raha!")
        return pd.DataFrame()

# Load Data
df = get_data()

# Basic Setup
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

st.title("🎯 Prediction & Reward App")

# Sidebar
st.sidebar.header("User Panel")

if not st.session_state.logged_in:
    tab1, tab2 = st.sidebar.tabs(["Login", "Sign Up"])
    
    with tab2:
        st.subheader("Naya Account")
        n_name = st.text_input("Naam")
        n_phone = st.text_input("Mobile No")
        n_pass = st.text_input("Password", type="password")
        
        if st.button("Register Now"):
            st.info("Note: Registration ke liye Admin ko WhatsApp karen taake wo aapka data sheet mein add karde.")
            st.write("Aapka Number:", n_phone)

    with tab1:
        st.subheader("Login")
        l_phone = st.text_input("Mobile No")
        l_pass = st.text_input("Password", type="password")
        
        if st.button("Login"):
            # Check if user exists in Sheet
            if not df.empty and 'phone' in df.columns:
                user = df[(df['phone'].astype(str) == str(l_phone)) & (df['password'].astype(str) == str(l_pass))]
                if not user.empty:
                    st.session_state.logged_in = True
                    st.session_state.user_name = user.iloc[0]['name']
                    st.session_state.balance = user.iloc[0]['balance']
                    st.rerun()
                else:
                    st.error("Ghalat Password ya Number!")
            else:
                st.error("Sheet khali hai ya data format ghalat hai!")

else:
    st.sidebar.success(f"Welcome {st.session_state.user_name}")
    st.sidebar.write(f"💰 Balance: RS {st.session_state.balance}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.header("Aaj ka Sawal")
    st.write("Kya aaj baarish hogi?")
    if st.button("YES"):
        st.success("Bet Lag Gayi!")
