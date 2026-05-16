import streamlit as st
import random

# --- 1. PAGE SETUP & CONFIG ---
st.set_page_config(page_title="Nerdy Earners | AI Predictions", layout="wide")

# --- 2. PREMIUM CELLULAR BORDER DESIGN ENGINE (CSS) ---
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

    /* Target Question Block Stylings */
    .mushkil-question {
        background: rgba(255, 75, 75, 0.05);
        border-left: 4px solid #ff4b4b;
        padding: 10px 15px;
        border-radius: 4px;
        margin-bottom: 15px;
        font-weight: 500;
        font-size: 0.95rem;
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

    /* Green System Confirm Overrides */
    .sidebar-glowing-btn button {
        background: linear-gradient(135deg, #a5ff33 0%, #66ff00 100%) !important;
        color: #0c0e11 !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE FOR BALANCE & DYNAMIC QUESTIONS ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'balance' not in st.session_state:
    st.session_state.balance = 1250.00

# Hardcore/Mushkil Betting Questions Pool (Automatic Random Rotator)
questions_pool = [
    "Will Asian Handicap Threshold alternative (+1.75) collapse before the 75th minute interval?",
    "Will Expected Goals (xG) matrix divergence exceed a differential margin of >1.42 at full-time?",
    "Will tactical operational shifts trigger consecutive booking events within a compressed 10-min window?",
    "Will counter-pressing conversion rate surpass defensive recovery threshold parameters (Over 64.5%)?",
    "Will structural defensive shape break down resulting in direct box entry events exceeding 14.5?"
]

# Randomize questions automatically on run
q1 = random.choice(questions_pool)
q2 = random.choice(questions_pool)
while q2 == q1:
    q2 = random.choice(questions_pool)

# --- 4. CONTROL PANEL (SIDEBAR) ---
with st.sidebar:
    st.title("🔋 Nerdy Earners")
    st.caption("AI-Powered Match Analytics Engine")

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
    st.title("🏆 AI Match Matrix Center")
    st.caption("Select your dynamic edge targets below to authorize stakes.")
    
    # Header Technical Analytics Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Bankers Track", "4/4 Active Slates")
    col2.metric("Queue Horizon", "Auto-Cycling Active")
    col3.metric("Historical Ratio", "82% Confidence Index")

    st.markdown("---")
    
    # ------------------ PREMIUM BOX 1 ------------------
    st.markdown('<div class="premium-border-box">', unsafe_allow_html=True)
    m1_t1, m1_t2 = st.columns([3, 1])
    m1_t1.markdown("⚽ **FC Cincinnati** vs **Toronto FC** &nbsp;|&nbsp; ⏰ *Live Aggregation*")
    m1_t2.markdown("<span style='float:right; color:#66ff00;'><b>AI Target: 1 (Trust 4/10)</b></span>", unsafe_allow_html=True)
    
    # The Automatic Changing Advanced Question
    st.markdown(f'<div class="mushkil-question">🔥 Complex Market Node: {q1}</div>', unsafe_allow_html=True)
    
    # Clean Grid Button Layout Inside Border
    b1_c1, b1_c2, b1_c3 = st.columns(3)
    if b1_c1.button("Bullish Edge (Yes) @ 2.15", key="m1_b1"):
        st.toast("Executing Capital Allocation on Bullish Target Node.")
    if b1_c2.button("Neutral Matrix (Draw) @ 3.40", key="m1_b2"):
        st.toast("Executing Capital Allocation on Neutral Target Node.")
    if b1_c3.button("Bearish Hedge (No) @ 1.95", key="m1_b3"):
        st.toast("Executing Capital Allocation on Bearish Target Node.")
    st.markdown('</div>', unsafe_allow_html=True)

    # ------------------ PREMIUM BOX 2 ------------------
    st.markdown('<div class="premium-border-box">', unsafe_allow_html=True)
    m2_t1, m2_t2 = st.columns([3, 1])
    m2_t1.markdown("⚽ **Cuiabá Esporte** vs **EC Bahia BA** &nbsp;|&nbsp; ⏰ *Live Aggregation*")
    m2_t2.markdown("<span style='float:right; color:#66ff00;'><b>AI Target: GG (Trust 6/10)</b></span>", unsafe_allow_html=True)
    
    # The Automatic Changing Advanced Question
    st.markdown(f'<div class="mushkil-question">🔥 Complex Market Node: {q2}</div>', unsafe_allow_html=True)
    
    # Clean Grid Button Layout Inside Border
    b2_c1, b2_c2, b2_c3 = st.columns(3)
    if b2_c1.button("Over 2.5 Alternative @ 2.45", key="m2_b1"):
        st.toast("Executing Capital Allocation on Over Alternative.")
    if b2_c2.button("Both Score Target @ 1.80", key="m2_b2"):
        st.toast("Executing Capital Allocation on Dual Scoring Core.")
    if b2_c3.button("Under 1.5 Alternative @ 3.10", key="m2_b3"):
        st.toast("Executing Capital Allocation on Under Alternative.")
    st.markdown('</div>', unsafe_allow_html=True)

elif current_page == "Investor Wallet":
    st.title("💰 Capital Allocation & Liquidity")
    w_col1, w_col2 = st.columns(2)
    w_col1.metric("Liquid Balance Pool", f"PKR {st.session_state.balance:,.2f}")
    w_col2.metric("Verification State", "Fully Verified ✅")
