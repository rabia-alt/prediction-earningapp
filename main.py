import streamlit as st
import random

# --- 1. PAGE SETUP & CONFIG ---
st.set_page_config(page_title="Predict & Earn | Sports & Life Matrix", layout="wide")

# --- 2. PREMIUM CELLS & BORDERS DESIGN ENGINE (CSS) ---
st.markdown("""
<style>
    /* Pure Matrix Dark UI */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0c0e11 !important;
        color: #e6e8eb !important;
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background-color: #111417 !important;
    }

    /* Highly Styled Sharp Border Matrix Box */
    .premium-border-box {
        background-color: #14181c !important;
        border: 2px solid #2d323f !important;
        border-radius: 10px !important;
        padding: 22px !important;
        margin-bottom: 25px !important;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5) !important;
        transition: border-color 0.3s ease;
    }
    .premium-border-box:hover {
        border-color: #66ff00 !important;
    }

    /* Daily Life Question Block Stylings */
    .daily-question {
        background: rgba(102, 255, 0, 0.03);
        border-left: 4px solid #66ff00;
        padding: 12px 15px;
        border-radius: 4px;
        margin-bottom: 15px;
        font-weight: 500;
        font-size: 1rem;
        color: #e6e8eb;
    }

    /* Betting Odd Box Selectors */
    div.stButton > button {
        background-color: #1e222b !important;
        color: #e6e8eb !important;
        border: 1px solid #2d323f !important;
        border-radius: 6px !important;
        padding: 12px !important;
        font-weight: bold !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    div.stButton > button:hover {
        border-color: #66ff00 !important;
        color: #66ff00 !important;
        background-color: rgba(102, 255, 0, 0.04) !important;
    }

    /* Glowing Green Button Container */
    .sidebar-glowing-btn button {
        background: linear-gradient(135deg, #a5ff33 0%, #66ff00 100%) !important;
        color: #0c0e11 !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE MANAGEMENT ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'balance' not in st.session_state:
    st.session_state.balance = 1250.00

# Daily Life Questions Pool (Automatic Random Changer)
daily_questions_pool = [
    "Will the maximum temperature in Islamabad cross 40°C tomorrow afternoon?",
    "Will Bitcoin's market value close higher than Ethereum's growth percentage by midnight?",
    "Will the local stock market index (PSX) close on a positive green note today?",
    "Will the price of petrol see a decrease or remain stable in the upcoming fuel policy announcement?",
    "Will the trending tech video on YouTube hit over 1 Million views within the next 12 hours?",
    "Will it rain in your current city within the next 24 hours according to satellite cloud mapping?",
    "Will the gold rate per tola experience a downward dip by tomorrow morning's market opening?"
]

# Randomize unique questions automatically on run
q1 = random.choice(daily_questions_pool)
q2 = random.choice(daily_questions_pool)
while q2 == q1:
    q2 = random.choice(daily_questions_pool)

# --- 4. CONTROL PANEL (SIDEBAR) ---
with st.sidebar:
    st.title("💰 Predict & Earn")
    st.caption("Turn Your Accurate Forecasts Into Rewards")

    if st.session_state.logged_in:
        st.success("Active User: Rabia")
        st.metric("Wallet Balance", f"PKR {st.session_state.balance:,.2f}")
        st.markdown('<div class="sidebar-glowing-btn">', unsafe_allow_html=True)
        if st.button("Secure Logout"):
            st.session_state.logged_in = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.subheader("Account Login Gateway")
        phone = st.text_input("Mobile Number", placeholder="e.g. 3415687754")
        password = st.text_input("Secure Password", type="password")
        st.markdown('<div class="sidebar-glowing-btn">', unsafe_allow_html=True)
        if st.button("Sign In Securely"):
            if phone and password:
                st.session_state.logged_in = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    current_page = st.selectbox("Navigate Workspace", ["Predictions Zone", "Investor Wallet"])

# --- 5. APP CORE WORKSPACES ---
if current_page == "Predictions Zone":
    st.title("🏆 Active Prediction Markets")
    st.caption("Select your choice below to lock in your stake pool.")
    
    # Header Statistics Trackers
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Players Pool", "1,420 Users Online")
    col2.metric("Market Horizon", "Dynamic Cycles Active")
    col3.metric("Platform Payout Ratio", "94.2% Distributed")

    st.markdown("---")
    st.subheader("Live Life & Trend Nodes")
    
    # ------------------ PREMIUM BOX 1 ------------------
    st.markdown('<div class="premium-border-box">', unsafe_allow_html=True)
    m1_t1, m1_t2 = st.columns([3, 1])
    m1_t1.markdown("📊 **Market Node #1:** Real-Time Lifestyle Forecast")
    m1_t2.markdown("<span style='float:right; color:#66ff00;'><b>Pool Multiplier: 2.0x</b></span>", unsafe_allow_html=True)
    
    # Dynamic Daily Life Question 1
    st.markdown(f'<div class="daily-question">❓ {q1}</div>', unsafe_allow_html=True)
    
    # Interaction Grid Options
    b1_c1, b1_c2, b1_c3 = st.columns(3)
    if b1_c1.button("Yes, Definitely @ 1.90", key="m1_b1"):
        st.toast("Stake allocated to affirmative target node!")
    if b1_c2.button("No, Highly Unlikely @ 2.10", key="m1_b2"):
        st.toast("Stake allocated to negative target node!")
    if b1_c3.button("Highly Uncertain (Draw) @ 3.50", key="m1_b3"):
        st.toast("Stake allocated to uncertainty bracket!")
    st.markdown('</div>', unsafe_allow_html=True)

    # ------------------ PREMIUM BOX 2 ------------------
    st.markdown('<div class="premium-border-box">', unsafe_allow_html=True)
    m2_t1, m2_t2 = st.columns([3, 1])
    m2_t1.markdown("📊 **Market Node #2:** Global Financial & Eco Trends")
    m2_t2.markdown("<span style='float:right; color:#66ff00;'><b>Pool Multiplier: 1.8x</b></span>", unsafe_allow_html=True)
    
    # Dynamic Daily Life Question 2
    st.markdown(f'<div class="daily-question">❓ {q2}</div>', unsafe_allow_html=True)
    
    # Interaction Grid Options
    b2_c1, b2_c2, b2_c3 = st.columns(3)
    if b2_c1.button("Bullish Upward (Yes) @ 1.75", key="m2_b1"):
        st.toast("Stake allocated to upward trend line!")
    if b2_c2.button("Bearish Downward (No) @ 2.25", key="m2_b2"):
        st.toast("Stake allocated to downward trend line!")
    if b2_c3.button("Stable Consolidation @ 4.00", key="m2_b3"):
        st.toast("Stake allocated to flat market equilibrium!")
    st.markdown('</div>', unsafe_allow_html=True)

elif current_page == "Investor Wallet":
    st.title("💰 Capital Allocation & Liquidity")
    w_col1, w_col2 = st.columns(2)
    w_col1.metric("Liquid Balance Pool", f"PKR {st.session_state.balance:,.2f}")
    w_col2.metric("Verification State", "Fully Verified ✅")
