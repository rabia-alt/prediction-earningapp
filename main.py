import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Page Config
st.set_page_config(page_title="Predict & Earn | Pro", page_icon="💰", layout="wide")

# 2. Connection
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    # TTL=0 taake har baar naya data aaye
    return conn.read(worksheet="Sheet1", ttl=0)

try:
    df = load_data()
    df.columns = [c.strip().lower() for c in df.columns]
except:
    st.error("Database connection failed. Check your Secrets.")
    st.stop()

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
                # Phone check as string
                if str(new_phone).strip() in df['phone'].astype(str).str.strip().values:
                    st.warning("This number is already registered.")
                else:
                    new_data = pd.DataFrame([{
                        "name": new_name,
                        "phone": str(new_phone).strip(),
                        "password": str(new_pass).strip(),
                        "balance": 30
                    }])
                    updated_df = pd.concat([df, new_data], ignore_index=True)
                    conn.update(worksheet="Sheet1", data=updated_df)
                    st.success("Registered! Now go to Login tab.")
            else:
                st.error("Fill all fields.")

    with tab_login:
        st.subheader("Login")
        l_phone = st.text_input("Mobile Number", key="login_phone")
        l_pass = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Sign In", type="primary", use_container_width=True):
            # --- IMPROVED LOGIN LOGIC ---
            # 1. Convert everything to string
            # 2. Remove any extra spaces (strip)
            # 3. Ensure '0' at the start doesn't cause issues
            
            input_phone = str(l_phone).strip()
            input_pass = str(l_pass).strip()
            
            temp_df = df.copy()
            temp_df['phone'] = temp_df['phone'].astype(str).str.strip()
            temp_df['password'] = temp_df['password'].astype(str).str.strip()
            
            user = temp_df[(temp_df['phone'] == input_phone) & (temp_df['password'] == input_pass)]
            
            if not user.empty:
                st.session_state.logged_in = True
                st.session_state.user_name = user.iloc[0]['name']
                st.session_state.balance = user.iloc[0]['balance']
                st.rerun()
            else:
                st.error("Invalid credentials. Check your number/password or Register again.")

else:
    st.sidebar.success(f"Welcome, {st.session_state.user_name}!")
    st.sidebar.metric("Balance", f"PKR {st.session_state.balance}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.header("Today's Prediction")
    st.subheader("Will the Bitcoin price stay above $62,000?")
    stake = st.select_slider("Stake (PKR):", options=[10, 20, 50, 100])
    
    if st.button("Submit Prediction", type="primary"):
        st.success(f"Prediction locked for PKR {stake}!")
