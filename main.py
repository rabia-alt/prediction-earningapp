import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page setup
st.set_page_config(page_title="Predict & Earn", page_icon="💰")

# Google Sheets Connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Function to get data
def get_data():
    return conn.read(worksheet="Sheet1", ttl=0)

# Main App
st.title("🎯 Prediction & Reward App")

# Sidebar for Login/Signup
st.sidebar.header("User Panel")

# Load existing users
df = get_data()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    tab1, tab2 = st.sidebar.tabs(["Login", "Sign Up"])
    
    with tab2: # Sign Up Logic
        new_name = st.text_input("Naam")
        new_phone = st.text_input("Mobile Number")
        new_pass = st.text_input("Password", type="password")
        if st.button("Register & Get 30 RS"):
            if new_phone in df['phone'].values:
                st.error("Ye number pehle se majood hai!")
            elif new_name and new_phone and new_pass:
                new_data = pd.DataFrame([{"name": new_name, "phone": new_phone, "password": new_pass, "balance": 30}])
                updated_df = pd.concat([df, new_data], ignore_index=True)
                conn.update(worksheet="Sheet1", data=updated_df)
                st.success("Account ban gaya! Ab Login karen.")
            else:
                st.error("Sari details likhen!")

    with tab1: # Login Logic
        l_phone = st.text_input("Mobile No", key="l_phone")
        l_pass = st.text_input("Password", type="password", key="l_pass")
        if st.button("Login"):
            user = df[(df['phone'] == l_phone) & (df['password'] == l_pass)]
            if not user.empty:
                st.session_state.logged_in = True
                st.session_state.user_phone = l_phone
                st.session_state.user_name = user.iloc[0]['name']
                st.rerun()
            else:
                st.error("Galat Number ya Password!")

else:
    # User is Logged In
    user_row = df[df['phone'] == st.session_state.user_phone].iloc[0]
    balance = user_row['balance']
    
    st.sidebar.write(f"👤 **Khush Amdeed:** {st.session_state.user_name}")
    st.sidebar.subheader(f"💰 Balance: RS {balance}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # Prediction Section
    st.header("🔥 Aaj ka Sawal")
    st.subheader("Kya aaj Pakistan match jitega?")
    
    bet = st.radio("Bet lagayein:", [10, 20, 50, 100], horizontal=True)
    
    if st.button("Submit Prediction"):
        if balance >= bet:
            # Update balance in Sheet
            df.loc[df['phone'] == st.session_state.user_phone, 'balance'] = balance - bet
            conn.update(worksheet="Sheet1", data=df)
            st.success(f"RS {bet} lag gaye! Result ka intezar karen.")
            st.rerun()
        else:
            st.error("Balance kam hai! Deposit karen.")

    # Deposit Info
    st.divider()
    st.info("💳 **Deposit:** Paisay 03xx-xxxxxxx par bhej kar admin ko WhatsApp karen.")
