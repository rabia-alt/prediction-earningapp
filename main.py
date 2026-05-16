import streamlit as st

# --- 1. PAGE SETUP & INITIAL CONFIG ---
st.set_page_config(page_title="Nerdy Earners | AI Predictions", layout="wide")

# --- 2. ADVANCED PREMIUM LAYOUT STYLING ENGINE (CSS) ---
st.markdown("""
<style>
    /* Pure Dark Premium Background */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0c0e11 !important;
        color: #e6e8eb !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Design Customization */
    [data-testid="stSidebar"] {
        background-color: #111417 !important;
    }
    
    /* Metrics Component Stability Style */
    [data-testid="stMetricValue"] {
        color: #66ff00 !important;
        font-weight: bold !important;
        font-size: 1.8rem !important;
    }
    [data-testid="stMetricLabel"] {
        color: #9299a3 !important;
    }
    
    /* Custom Responsive Match Row Cards */
    .match-container {
        background-color: #14181c;
        border: 1px solid #2a2f36;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Odd Selection Betting Block Buttons Styling */
    div.stButton > button {
        background-color: #1e222b !important;
        color: #e6e8eb !important;
        border: 1px solid #2d323f !important;
        border-radius: 8px !important;
        padding: 10px !important;
        font-weight: bold !important;
        font-size: 1.05rem !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
    }
    
    /* Odd Buttons Hover & Active States */
    div.stButton > button:hover {
        border-color: #66ff00 !important;
        color: #66ff00 !important;
        background-color: rgba(102, 255, 0, 0.05) !important;
        transform: translateY(-2px);
    }
    
    /* Main Call-to-Action (Login/Submit) Glowing Green Overrides */
    .sidebar-glowing-btn button {
        background: linear-gradient(135deg, #a5ff33 0%, #66ff00 100%) !important;
        color: #0c0e11 !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(102, 255, 0, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE FOR BALANCE & INTERACTION TRACKING ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'balance' not in st.session_state:
    st.session_state.balance = 1250.00

# --- 4. NAVIGATION CONTROL PANEL (SIDEBAR) ---
with st.sidebar:
    st.title("🔋 Nerdy Earners")
    st.caption("AI-Powered Match Analytics Engine")

    if st.session_state.logged_in:
        st.success("Active User: Rabia")
        st.metric("Wallet Balance", f"PKR {st.session_state.balance:,.2f}")
        st.markdown('<div class="sidebar-glowing-btn">', unsafe_allow_html=True)
        if st.button("Secure Logout", key="logout_btn"):
            st.session_state.logged_in = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.subheader("Account Login Gateway")
        phone = st.text_input("Mobile Number", placeholder="e.g. 3415687754")
        st.caption("⚠️ Start se '0' remove kar ke enter karein.")
        password = st.text_input("Secure Password", type="password")
        st.markdown('<div class="sidebar-glowing-btn">', unsafe_allow_html=True)
        if st.button("Sign In Securely", key="login_submit_btn"):
            if phone and password:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Fields cannot be left blank.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    current_page = st.selectbox("Navigate Workspace", ["Predictions Zone", "Investor Wallet"])

# --- 5. APPLICATION CORE WORKSPACES ---

# WORKSPACE A: PREDICTIONS ZONE
if current_page == "Predictions Zone":
    st.title("🏆 AI Match Matrix Center")
    st.caption("Select your prediction odds below to stake tokens.")
    
    # Analytical Top Header Row Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Bankers Track", value="4/4 Absolute Wins Today")
    with col2:
        st.metric(label="Queue Horizon", value="Next AI Refresh: 01:15")
    with col3:
        st.metric(label="Historical Performance Matrix", value="82% Average Accuracy")

    st.markdown("---")
    st.subheader("Active Markets & AI Recommendations")
    
    # --- MATCH CARD #1 ---
    st.markdown('<div class="match-container">', unsafe_allow_html=True)
    m1_r1_c1, m1_r1_c2 = st.columns([3, 1])
    with m1_r1_c1:
        st.markdown("⚽ **FC Cincinnati** vs **Toronto FC** &nbsp;|&nbsp; ⏰ *Today 00:30* &nbsp;|&nbsp; 🟢 **Live Market**")
    with m1_r1_c2:
        st.markdown("<span style='float:right;'>AI Best Tip: <b style='color:#66ff00;'>1 (Trust 4/10)</b></span>", unsafe_allow_html=True)
    
    st.markdown("<p style='color:#9299a3; font-size:0.9rem; margin-top:-5px;'>Question: Which outcome will manifest at full-time whistle?</p>", unsafe_allow_html=True)
    
    # Interactive Clickable Odds Row (The Betting Question Blocks)
    m1_o1, m1_o2, m1_o3 = st.columns(3)
    if m1_o1.button("Home (1) @ 1.85", key="m1_odd_1"):
        st.toast("Selected Home Team win for FC Cincinnati!")
    if m1_o2.button("Draw (X) @ 3.80", key="m1_odd_x"):
        st.toast("Selected Draw Match outcome!")
    if m1_o3.button("Away (2) @ 4.00", key="m1_odd_2"):
        st.toast("Selected Away Team win for Toronto FC!")
    st.markdown('</div>', unsafe_allow_html=True)


    # --- MATCH CARD #2 ---
    st.markdown('<div class="match-container">', unsafe_allow_html=True)
    m2_r1_c1, m2_r1_c2 = st.columns([3, 1])
    with m2_r1_c1:
        st.markdown("⚽ **Cuiabá Esporte** vs **EC Bahia BA** &nbsp;|&nbsp; ⏰ *Today 01:00* &nbsp;|&nbsp; 🟢 **Live Market**")
    with m2_r1_c2:
        st.markdown("<span style='float:right;'>AI Best Tip: <b style='color:#66ff00;'>GG (Trust 6/10)</b></span>", unsafe_allow_html=True)
        
    st.markdown("<p style='color:#9299a3; font-size:0.9rem; margin-top:-5px;'>Question: Will both teams secure goals within normal match duration?</p>", unsafe_allow_html=True)
    
    # Interactive Clickable Odds Row
    m2_o1, m2_o2, m2_o3 = st.columns(3)
    if m2_o1.button("Yes (GG) @ 2.30", key="m2_odd_gg"):
        st.toast("Selected Goal-Goal option!")
    if m2_o2.button("No @ 1.65", key="m2_odd_no"):
        st.toast("Selected clean-sheet prediction!")
    if m2_o3.button("Over 2.5 Goals @ 3.30", key="m2_odd_o25"):
        st.toast("Selected aggressive goal threshold prediction!")
    st.markdown('</div>', unsafe_allow_html=True)

# WORKSPACE B: INVESTOR WALLET MANAGEMENT
elif current_page == "Investor Wallet":
    st.title("💰 Capital Allocation & Liquidity")
    
    w_col1, w_col2 = st.columns(2)
    w_col1.metric("Liquid Balance Pool", f"PKR {st.session_state.balance:,.2f}")
    w_col2.metric("Verification State", "Fully Verified ✅")

    st.markdown("---")
    dep_panel, with_panel = st.columns(2)
    
    with dep_panel:
        st.subheader("Investment Deposit")
        st.info("⚡ **EasyPaisa / JazzCash:** 03415687754\n\n**Title:** Rabia Hafeez")
        dep_amount = st.number_input("Transfer Amount (PKR)", min_value=100, step=50, key="wallet_dep_amt")
        trx_id = st.text_input("Transaction ID (TrxID)", placeholder="e.g. 8945729104", key="wallet_trx")
        st.markdown('<div class="sidebar-glowing-btn">', unsafe_allow_html=True)
        if st.button("Submit Deposit Log", key="submit_dep_btn"):
            if trx_id:
                st.success("Log submitted! Data queued for verification.")
            else:
                st.error("Transaction ID is required.")
        st.markdown('</div>', unsafe_allow_html=True)
                
    with with_panel:
        st.subheader("Withdraw Rewards")
        with_amount = st.number_input("Withdraw Amount (PKR)", min_value=100, step=50, key="wallet_with_amt")
        st.markdown('<div class="sidebar-glowing-btn">', unsafe_allow_html=True)
        if st.button("Authorize Liquidation", key="auth_with_btn"):
            if with_amount <= st.session_state.balance:
                st.session_state.balance -= with_amount
                st.success("Liquidation authorized successfully!")
                st.rerun()
            else:
                st.error("Insufficient balance pool.")
        st.markdown('</div>', unsafe_allow_html=True)
