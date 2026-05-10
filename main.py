import streamlit as st
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="Prediction & Win", page_icon="💰")

# --- INITIALIZE SESSION STATE ---
# Yeh user ka data temporary save karne ke liye hai (Jab tak database connect nahi hota)
if 'balance' not in st.session_state:
    st.session_state.balance = 0
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- HEADER ---
st.title("🎯 Prediction & Reward App")
st.write("Rozana sawalat ke jawab den aur paise jeetain!")

# --- SIDEBAR (Login & Deposit) ---
st.sidebar.header("User Panel")

if not st.session_state.logged_in:
    st.sidebar.subheader("Login / Sign Up")
    name = st.sidebar.text_input("Apna Naam")
    phone = st.sidebar.text_input("Mobile Number (EasyPaisa)")
    
    if st.sidebar.button("Register & Get 30 RS"):
        if name and phone:
            st.session_state.logged_in = True
            st.session_state.user_name = name
            st.session_state.balance = 30  # Login bonus
            st.sidebar.success(f"Khush Amdeed {name}!")
            st.rerun()
        else:
            st.sidebar.error("Naam aur Number lazmi hai!")
else:
    st.sidebar.write(f"👤 **User:** {st.session_state.user_name}")
    st.sidebar.write(f"💰 **Balance:** RS {st.session_state.balance}")
    
    st.sidebar.divider()
    st.sidebar.write("💳 **Deposit Money**")
    st.sidebar.info("EasyPaisa: 03xx-xxxxxxx\n(Bhejne ke baad TID likhen)")
    tid = st.sidebar.text_input("Transaction ID (TID)")
    if st.sidebar.button("Verify Payment"):
        st.sidebar.warning("TID bhej di gayi hai. Admin verify karega.")

# --- MAIN INTERFACE ---
if st.session_state.logged_in:
    st.header("🔥 Aaj ka Sawal")
    
    # Sawal aur Options
    question = "Kya kal Pakistan Cricket Match jitega?"
    st.subheader(question)
    
    bet_amount = st.radio("Kitni raqam lagani hai?", [10, 20, 50, 100], horizontal=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("YES ✅"):
            if st.session_state.balance >= bet_amount:
                st.session_state.balance -= bet_amount
                st.success(f"Aapne YES par RS {bet_amount} laga diye. Result ka intezar karen!")
            else:
                st.error("Balance kam hai! Please deposit karen.")
                
    with col2:
        if st.button("NO ❌"):
            if st.session_state.balance >= bet_amount:
                st.session_state.balance -= bet_amount
                st.error(f"Aapne NO par RS {bet_amount} laga diye. Result ka intezar karen!")
            else:
                st.error("Balance kam hai! Please deposit karen.")

    # Rules Section
    st.divider()
    with st.expander("App ke Rules Parhein"):
        st.write("""
        1. Login karne par 30 Rupees bonus milega.
        2. Har sahi prediction par aapko lagayi hui raqam ka double milega (minus 10% commission).
        3. Paise nikalne (Withdraw) ke liye kam az kam 500 balance hona chahiye.
        """)
else:
    st.info("App use karne ke liye pehle Sidebar se Login/Register karen.")
    st.image("https://img.freepik.com/free-vector/sport-game-prediction-concept_23-2148496468.jpg", caption="Predict & Win Big!")
