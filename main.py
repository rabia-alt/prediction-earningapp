import streamlit as st
import pandas as pd
import numpy as np

# --- 1. PAGE SETUP & NATIVE CONFIG ---
st.set_page_config(page_title="Nerdy Earners | AI Predictions", layout="wide", initial_siimport streamlit as st
import pandas as pd
import numpy as np

# --- 1. PAGE SETUP & NATIVE CONFIG ---
st.set_page_config(page_title="Nerdy Earners | AI Predictions", layout="wide", initial_sidebar_state="expanded")

# --- 2. GLOBAL CUSTOM CSS (NERDYTIPS STYLE) ---
# We use custom CSS to create the dark theme, neon glows, and table stylings.
# In a real environment, you might load this from a .css file.
st.markdown("""
<style>
    /* Global Background and Colors */
    .stApp {
        background-color: #0c0e11;
        color: #e6e8eb;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling */
    .css-1d391kg { /* This may change in different Streamlit versions */
        background-color: #111417 !important;
    }
    .css-1d391kg .st-df {
        color: #66ff00;
    }
    .sidebar .stButton > button {
        color: #e6e8eb;
        background-color: transparent;
        border: none;
        text-align: left;
    }
    
    /* Prediction Cards (like 'Bankers', 'Upcoming' in screenshot) */
    .nerdy-card {
        background-color: rgba(20, 24, 28, 0.7);
        border: 1px solid #2a2f36;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: transform 0.2s;
    }
    .nerdy-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 15px rgba(102, 255, 0, 0.2);
    }
    .nerdy-card h3 {
        color: #e6e8eb;
        margin-bottom: 5px;
    }
    .nerdy-card p {
        color: #9299a3;
        font-size: 0.9em;
    }
    .nerdy-card .neon-text {
        color: #66ff00;
        font-weight: bold;
    }

    /* Custom Custom Match Table (inspired by screenshot) */
    .nerdy-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
        border-radius: 12px;
        overflow: hidden;
        background-color: #14181c;
        border: 1px solid #2a2f36;
    }
    .nerdy-table th {
        background-color: #1a1e23;
        color: #9299a3;
        padding: 15px;
        text-align: center;
        font-weight: 500;
        font-size: 0.9em;
    }
    .nerdy-table td {
        padding: 20px 15px;
        text-align: center;
        border-bottom: 1px solid #1c2126;
        color: #e6e8eb;
    }
    .nerdy-table tr:last-child td {
        border-bottom: none;
    }
    .team-info {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .team-logo {
        width: 30px;
        height: 30px;
        margin: 0 10px;
    }
    .match-row-details {
        color: #9299a3;
        font-size: 0.8em;
    }
    
    /* Action Buttons (like 'Bet of the Day') */
    .neon-button {
        color: #0c0e11 !important;
        background: linear-gradient(135deg, #a5ff33 0%, #66ff00 100%) !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        border: none !important;
        font-weight: bold !important;
    }
    .secondary-button {
        color: #9299a3 !important;
        background-color: transparent !important;
        border: 1px solid #2a2f36 !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
    }
    
    /* Wallet & History Cards */
    .info-panel {
        background-color: #14181c;
        border: 1px solid #2a2f36;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE FOR MOCK DATA ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = "GuestUser"
if 'balance' not in st.session_state:
    st.session_state.balance = 1000.00
if 'deposit_requests' not in st.session_state:
    st.session_state.deposit_requests = []
if 'withdraw_requests' not in st.session_state:
    st.session_state.withdraw_requests = []
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

# Mock data for active matches (like the ones in the screenshot)
active_matches_data = [
    {
        'id': 1, 'date': '00:30', 'match': ('FC Cincinnati', 'Toronto FC'), 'logos': ('https://raw.githubusercontent.com/davide-neri/logos/master/cincinnati.png', 'https://raw.githubusercontent.com/davide-neri/logos/master/toronto_fc.png'),
        'tip': '1', 'odds': (1.85, 3.80, 4.00), 'goals': '2-3', 'gg': 'No', 'best_tip': '1', 'trust': '4/10'
    },
    {
        'id': 2, 'date': '01:00', 'match': ('Cuiaba Esporte Clube MT', 'EC Bahia BA'), 'logos': ('https://raw.githubusercontent.com/davide-neri/logos/master/cuiaba.png', 'https://raw.githubusercontent.com/davide-neri/logos/master/bahia.png'),
        'tip': 'GG', 'odds': (2.30, 3.20, 3.30), 'goals': 'GG', 'gg': 'Yes', 'best_tip': 'GG', 'trust': '6/10'
    },
    {
        'id': 3, 'date': '02:00', 'match': ('Goiás', 'Corinthians'), 'logos': ('https://raw.githubusercontent.com/davide-neri/logos/master/goias.png', 'https://raw.githubusercontent.com/davide-neri/logos/master/corinthians.png'),
        'tip': 'X', 'odds': (2.10, 3.10, 3.70), 'goals': '1-2', 'gg': 'No', 'best_tip': '2', 'trust': '5/10'
    }
]

# --- 4. SIDEBAR LOGIC & NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/5973/5973685.png", width=60) # Substitute with your 'NT' logo
    st.title("Nerdy Earners")
    st.caption("AI-Powered AI Predictions")

    if st.session_state.logged_in:
        st.success(f"Welcome, {st.session_state.user_name}!")
        st.caption(f"Member Since: 2024")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    else:
        st.subheader("Account Login")
        st.text_input("Mobile Number", key="login_phone")
        st.text_input("Password", type="password", key="login_pass")
        if st.button("Sign In Securely", key="sidebar_login_btn", help="Click to Login", args=None, kwargs=None, type="primary"):
            # Simple mock login for design purpose
            if st.session_state.login_phone == "1234567890" and st.session_state.login_pass == "password":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials.")

    st.markdown("---")
    # Native Sidebar Navigation (to align with Nerdytips structure)
    current_page = st.selectbox("Navigate", ["Predictions Zone", "My Wallet", "Predictions History", "Member Profile", "AI Leagues"], index=0)

# --- 5. MAIN CONTENT AREA ---
if current_page == "Predictions Zone":
    # 5.1 HEADER AREA
    st.title("🏆 AI Match Center")
    st.caption("Updated Every 5 Minutes | Confidence Score Engine v3.1")
    
    # 5.2 TOP CARDS (BANKERS, UPCOMING, SUCCESS RATE)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="nerdy-card"><h3>Bankers</h3><p class="neon-text">4/4 Tips Won Today</p><p>Low Risk Matches</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="nerdy-card"><h3>Upcoming Matches</h3><p>Next Match in</p><p class="neon-text">01:15:30</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="nerdy-card"><h3>Match Success Rate</h3><p class="neon-text">82% Success Rate</p><p>Last 30 Days</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # 5.3 MATCH PREDICTION TABLE (The main feature)
    st.subheader("Featured AI Predictions")
    
    # Create the HTML table with NerdyTips styling
    html_table = """
    <table class="nerdy-table">
        <thead>
            <tr>
                <th>Date</th>
                <th>Match Details</th>
                <th>1</th>
                <th>X</th>
                <th>2</th>
                <th>TIP</th>
                <th>Goals</th>
                <th>GG</th>
                <th>Best TIP</th>
                <th>Trust</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for match in active_matches_data:
        html_table += f"""
        <tr>
            <td>
                <div>{match['date']}</div>
                <div class="match-row-details">Finished</div>
            </td>
            <td>
                <div class="team-info">
                    {match['match'][0]} <img src="{match['logos'][0]}" class="team-logo">
                    vs
                    <img src="{match['logos'][1]}" class="team-logo"> {match['match'][1]}
                </div>
            </td>
            <td>{match['odds'][0]}</td>
            <td>{match['odds'][1]}</td>
            <td>{match['odds'][2]}</td>
            <td><span class="neon-text">{match['tip']}</span></td>
            <td>{match['goals']}</td>
            <td>{match['gg']}</td>
            <td><span class="neon-text">{match['best_tip']}</span></td>
            <td>{match['trust']}</td>
        </tr>
        """
        
    html_table += "</tbody></table>"
    
    # Use st.markdown with unsafe_allow_html=True to render the HTML table
    st.markdown(html_table, unsafe_allow_html=True)

elif current_page == "My Wallet":
    st.title("💰 AI Investor Wallet")
    
    col1, col2 = st.columns([1, 1])
    
    # Wallet Info Panel
    with col1:
        st.markdown(f"""
        <div class="info-panel">
            <h3>Account Balance</h3>
            <p style="font-size: 2.5em; color: #66ff00; font-weight: bold;">PKR {st.session_state.balance:,.2f}</p>
            <p style="color: #9299a3;">Withdrawal Pending: <span style="color: #FF5353;">PKR 500.00</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-panel">
            <h3>Account Status</h3>
            <p>Verification: <span style="color: #66ff00;">Verified</span></p>
            <p>Current Tier: Bronze Investor</p>
            <p>Active Predictions: 0</p>
        </div>
        """, unsafe_allow_html=True)

    # Deposit/Investment Panel
    st.markdown("---")
    dep_col, with_col = st.columns(2)
    with dep_col:
        st.subheader("New Investment (Deposit)")
        with st.expander("Deposit via EasyPaisa / JazzCash", expanded=False):
            st.info("ℹ️ Account Title: Rabia Hafeez\nPhone: 03415687754")
            dep_amount = st.number_input("Enter Amount (PKR)", min_value=100)
            trx_id = st.text_input("Enter Transaction ID (Trx ID)")
            if st.button("Submit Investment Request", key="submit_deposit_btn", type="primary"):
                if dep_amount and trx_id:
                    st.session_state.deposit_requests.append({'amount': dep_amount, 'trx_id': trx_id, 'status': 'Pending Verification'})
                    st.success("Investment Request received! Please wait for AI verification.")
                else:
                    st.error("Please fill in both the amount and Transaction ID.")

        st.subheader("Investment History")
        if not st.session_state.deposit_requests:
            st.caption("No recent investments.")
        else:
            dep_df = pd.DataFrame(st.session_state.deposit_requests)
            st.dataframe(dep_df)

    with with_col:
        st.subheader("Withdraw Rewards")
        with st.expander("Request Withdrawal", expanded=False):
            with_amount = st.number_input("Enter Amount (PKR)", min_value=100)
            with_method = st.selectbox("Withdrawal Method", ["EasyPaisa", "JazzCash", "UBL Omni"])
            with_acc = st.text_input("Account Number (without leading 0)", placeholder="e.g. 341...")
            
            if st.button("Request Withdrawal", key="request_withdraw_btn", type="primary"):
                if with_amount <= st.session_state.balance:
                    if with_amount >= 100:
                        st.session_state.withdraw_requests.append({'amount': with_amount, 'method': with_method, 'account': with_acc, 'status': 'Pending Approval'})
                        st.session_state.balance -= with_amount # Update balance mockingly
                        st.success("Withdrawal request submitted! Processing typically takes 24-48 hours.")
                        st.rerun()
                    else:
                        st.error("Minimum withdrawal amount is PKR 100.")
                else:
                    st.error("Insufficient balance.")

        st.subheader("Withdrawal History")
        if not st.session_state.withdraw_requests:
            st.caption("No recent withdrawals.")
        else:
            with_df = pd.DataFrame(st.session_state.withdraw_requests)
            st.dataframe(with_df)

elif current_page == "Predictions History":
    st.title("📋 Predictions History")
    # Mock data for past predictions
    prediction_history_mock = [
        {'id': 101, 'match': ('Manchester United', 'Liverpool'), 'type': 'Bet', 'predicted': 'Yes', 'result': 'Lost'},
        {'id': 102, 'match': ('Real Madrid', 'Barcelona'), 'type': 'Tip', 'predicted': 'GG', 'result': 'GG'},
        {'id': 103, 'match': ('PSG', 'Marseille'), 'type': 'AI Prediction', 'predicted': '1', 'result': '1'},
    ]
    
    st.subheader("AI Prediction History")
    
    # Create the HTML table for history
    html_history_table = """
    <table class="nerdy-table">
        <thead>
            <tr>
                <th>Prediction ID</th>
                <th>Match</th>
                <th>Type</th>
                <th>Predicted</th>
                <th>Result</th>
            </tr>
        </thead>
        <tbody>
    """
    for pred in prediction_history_mock:
        result_color = "#66ff00" if pred['result'] == 'GG' or pred['result'] == '1' else "#FF5353"
        html_history_table += f"""
        <tr>
            <td>{pred['id']}</td>
            <td>{pred['match'][0]} vs {pred['match'][1]}</td>
            <td>{pred['type']}</td>
            <td>{pred['predicted']}</td>
            <td><span style="color: {result_color}; font-weight: bold;">{pred['result']}</span></td>
        </tr>
        """
    html_history_table += "</tbody></table>"
    st.markdown(html_history_table, unsafe_allow_html=True)debar_state="expanded")

# --- 2. GLOBAL CUSTOM CSS (NERDYTIPS STYLE) ---
# We use custom CSS to create the dark theme, neon glows, and table stylings.
# In a real environment, you might load this from a .css file.
st.markdown("""
<style>
    /* Global Background and Colors */
    .stApp {
        background-color: #0c0e11;
        color: #e6e8eb;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling */
    .css-1d391kg { /* This may change in different Streamlit versions */
        background-color: #111417 !important;
    }
    .css-1d391kg .st-df {
        color: #66ff00;
    }
    .sidebar .stButton > button {
        color: #e6e8eb;
        background-color: transparent;
        border: none;
        text-align: left;
    }
    
    /* Prediction Cards (like 'Bankers', 'Upcoming' in screenshot) */
    .nerdy-card {
        background-color: rgba(20, 24, 28, 0.7);
        border: 1px solid #2a2f36;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: transform 0.2s;
    }
    .nerdy-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 15px rgba(102, 255, 0, 0.2);
    }
    .nerdy-card h3 {
        color: #e6e8eb;
        margin-bottom: 5px;
    }
    .nerdy-card p {
        color: #9299a3;
        font-size: 0.9em;
    }
    .nerdy-card .neon-text {
        color: #66ff00;
        font-weight: bold;
    }

    /* Custom Custom Match Table (inspired by screenshot) */
    .nerdy-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
        border-radius: 12px;
        overflow: hidden;
        background-color: #14181c;
        border: 1px solid #2a2f36;
    }
    .nerdy-table th {
        background-color: #1a1e23;
        color: #9299a3;
        padding: 15px;
        text-align: center;
        font-weight: 500;
        font-size: 0.9em;
    }
    .nerdy-table td {
        padding: 20px 15px;
        text-align: center;
        border-bottom: 1px solid #1c2126;
        color: #e6e8eb;
    }
    .nerdy-table tr:last-child td {
        border-bottom: none;
    }
    .team-info {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .team-logo {
        width: 30px;
        height: 30px;
        margin: 0 10px;
    }
    .match-row-details {
        color: #9299a3;
        font-size: 0.8em;
    }
    
    /* Action Buttons (like 'Bet of the Day') */
    .neon-button {
        color: #0c0e11 !important;
        background: linear-gradient(135deg, #a5ff33 0%, #66ff00 100%) !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        border: none !important;
        font-weight: bold !important;
    }
    .secondary-button {
        color: #9299a3 !important;
        background-color: transparent !important;
        border: 1px solid #2a2f36 !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
    }
    
    /* Wallet & History Cards */
    .info-panel {
        background-color: #14181c;
        border: 1px solid #2a2f36;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE FOR MOCK DATA ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = "GuestUser"
if 'balance' not in st.session_state:
    st.session_state.balance = 1000.00
if 'deposit_requests' not in st.session_state:
    st.session_state.deposit_requests = []
if 'withdraw_requests' not in st.session_state:
    st.session_state.withdraw_requests = []
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

# Mock data for active matches (like the ones in the screenshot)
active_matches_data = [
    {
        'id': 1, 'date': '00:30', 'match': ('FC Cincinnati', 'Toronto FC'), 'logos': ('https://raw.githubusercontent.com/davide-neri/logos/master/cincinnati.png', 'https://raw.githubusercontent.com/davide-neri/logos/master/toronto_fc.png'),
        'tip': '1', 'odds': (1.85, 3.80, 4.00), 'goals': '2-3', 'gg': 'No', 'best_tip': '1', 'trust': '4/10'
    },
    {
        'id': 2, 'date': '01:00', 'match': ('Cuiaba Esporte Clube MT', 'EC Bahia BA'), 'logos': ('https://raw.githubusercontent.com/davide-neri/logos/master/cuiaba.png', 'https://raw.githubusercontent.com/davide-neri/logos/master/bahia.png'),
        'tip': 'GG', 'odds': (2.30, 3.20, 3.30), 'goals': 'GG', 'gg': 'Yes', 'best_tip': 'GG', 'trust': '6/10'
    },
    {
        'id': 3, 'date': '02:00', 'match': ('Goiás', 'Corinthians'), 'logos': ('https://raw.githubusercontent.com/davide-neri/logos/master/goias.png', 'https://raw.githubusercontent.com/davide-neri/logos/master/corinthians.png'),
        'tip': 'X', 'odds': (2.10, 3.10, 3.70), 'goals': '1-2', 'gg': 'No', 'best_tip': '2', 'trust': '5/10'
    }
]

# --- 4. SIDEBAR LOGIC & NAVIGATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/5973/5973685.png", width=60) # Substitute with your 'NT' logo
    st.title("Nerdy Earners")
    st.caption("AI-Powered AI Predictions")

    if st.session_state.logged_in:
        st.success(f"Welcome, {st.session_state.user_name}!")
        st.caption(f"Member Since: 2024")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    else:
        st.subheader("Account Login")
        st.text_input("Mobile Number", key="login_phone")
        st.text_input("Password", type="password", key="login_pass")
        if st.button("Sign In Securely", key="sidebar_login_btn", help="Click to Login", args=None, kwargs=None, type="primary"):
            # Simple mock login for design purpose
            if st.session_state.login_phone == "1234567890" and st.session_state.login_pass == "password":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid credentials.")

    st.markdown("---")
    # Native Sidebar Navigation (to align with Nerdytips structure)
    current_page = st.selectbox("Navigate", ["Predictions Zone", "My Wallet", "Predictions History", "Member Profile", "AI Leagues"], index=0)

# --- 5. MAIN CONTENT AREA ---
if current_page == "Predictions Zone":
    # 5.1 HEADER AREA
    st.title("🏆 AI Match Center")
    st.caption("Updated Every 5 Minutes | Confidence Score Engine v3.1")
    
    # 5.2 TOP CARDS (BANKERS, UPCOMING, SUCCESS RATE)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="nerdy-card"><h3>Bankers</h3><p class="neon-text">4/4 Tips Won Today</p><p>Low Risk Matches</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="nerdy-card"><h3>Upcoming Matches</h3><p>Next Match in</p><p class="neon-text">01:15:30</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="nerdy-card"><h3>Match Success Rate</h3><p class="neon-text">82% Success Rate</p><p>Last 30 Days</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # 5.3 MATCH PREDICTION TABLE (The main feature)
    st.subheader("Featured AI Predictions")
    
    # Create the HTML table with NerdyTips styling
    html_table = """
    <table class="nerdy-table">
        <thead>
            <tr>
                <th>Date</th>
                <th>Match Details</th>
                <th>1</th>
                <th>X</th>
                <th>2</th>
                <th>TIP</th>
                <th>Goals</th>
                <th>GG</th>
                <th>Best TIP</th>
                <th>Trust</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for match in active_matches_data:
        html_table += f"""
        <tr>
            <td>
                <div>{match['date']}</div>
                <div class="match-row-details">Finished</div>
            </td>
            <td>
                <div class="team-info">
                    {match['match'][0]} <img src="{match['logos'][0]}" class="team-logo">
                    vs
                    <img src="{match['logos'][1]}" class="team-logo"> {match['match'][1]}
                </div>
            </td>
            <td>{match['odds'][0]}</td>
            <td>{match['odds'][1]}</td>
            <td>{match['odds'][2]}</td>
            <td><span class="neon-text">{match['tip']}</span></td>
            <td>{match['goals']}</td>
            <td>{match['gg']}</td>
            <td><span class="neon-text">{match['best_tip']}</span></td>
            <td>{match['trust']}</td>
        </tr>
        """
        
    html_table += "</tbody></table>"
    
    # Use st.markdown with unsafe_allow_html=True to render the HTML table
    st.markdown(html_table, unsafe_allow_html=True)

elif current_page == "My Wallet":
    st.title("💰 AI Investor Wallet")
    
    col1, col2 = st.columns([1, 1])
    
    # Wallet Info Panel
    with col1:
        st.markdown(f"""
        <div class="info-panel">
            <h3>Account Balance</h3>
            <p style="font-size: 2.5em; color: #66ff00; font-weight: bold;">PKR {st.session_state.balance:,.2f}</p>
            <p style="color: #9299a3;">Withdrawal Pending: <span style="color: #FF5353;">PKR 500.00</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-panel">
            <h3>Account Status</h3>
            <p>Verification: <span style="color: #66ff00;">Verified</span></p>
            <p>Current Tier: Bronze Investor</p>
            <p>Active Predictions: 0</p>
        </div>
        """, unsafe_allow_html=True)

    # Deposit/Investment Panel
    st.markdown("---")
    dep_col, with_col = st.columns(2)
    with dep_col:
        st.subheader("New Investment (Deposit)")
        with st.expander("Deposit via EasyPaisa / JazzCash", expanded=False):
            st.info("ℹ️ Account Title: Rabia Hafeez\nPhone: 03415687754")
            dep_amount = st.number_input("Enter Amount (PKR)", min_value=100)
            trx_id = st.text_input("Enter Transaction ID (Trx ID)")
            if st.button("Submit Investment Request", key="submit_deposit_btn", type="primary"):
                if dep_amount and trx_id:
                    st.session_state.deposit_requests.append({'amount': dep_amount, 'trx_id': trx_id, 'status': 'Pending Verification'})
                    st.success("Investment Request received! Please wait for AI verification.")
                else:
                    st.error("Please fill in both the amount and Transaction ID.")

        st.subheader("Investment History")
        if not st.session_state.deposit_requests:
            st.caption("No recent investments.")
        else:
            dep_df = pd.DataFrame(st.session_state.deposit_requests)
            st.dataframe(dep_df)

    with with_col:
        st.subheader("Withdraw Rewards")
        with st.expander("Request Withdrawal", expanded=False):
            with_amount = st.number_input("Enter Amount (PKR)", min_value=100)
            with_method = st.selectbox("Withdrawal Method", ["EasyPaisa", "JazzCash", "UBL Omni"])
            with_acc = st.text_input("Account Number (without leading 0)", placeholder="e.g. 341...")
            
            if st.button("Request Withdrawal", key="request_withdraw_btn", type="primary"):
                if with_amount <= st.session_state.balance:
                    if with_amount >= 100:
                        st.session_state.withdraw_requests.append({'amount': with_amount, 'method': with_method, 'account': with_acc, 'status': 'Pending Approval'})
                        st.session_state.balance -= with_amount # Update balance mockingly
                        st.success("Withdrawal request submitted! Processing typically takes 24-48 hours.")
                        st.rerun()
                    else:
                        st.error("Minimum withdrawal amount is PKR 100.")
                else:
                    st.error("Insufficient balance.")

        st.subheader("Withdrawal History")
        if not st.session_state.withdraw_requests:
            st.caption("No recent withdrawals.")
        else:
            with_df = pd.DataFrame(st.session_state.withdraw_requests)
            st.dataframe(with_df)

elif current_page == "Predictions History":
    st.title("📋 Predictions History")
    # Mock data for past predictions
    prediction_history_mock = [
        {'id': 101, 'match': ('Manchester United', 'Liverpool'), 'type': 'Bet', 'predicted': 'Yes', 'result': 'Lost'},
        {'id': 102, 'match': ('Real Madrid', 'Barcelona'), 'type': 'Tip', 'predicted': 'GG', 'result': 'GG'},
        {'id': 103, 'match': ('PSG', 'Marseille'), 'type': 'AI Prediction', 'predicted': '1', 'result': '1'},
    ]
    
    st.subheader("AI Prediction History")
    
    # Create the HTML table for history
    html_history_table = """
    <table class="nerdy-table">
        <thead>
            <tr>
                <th>Prediction ID</th>
                <th>Match</th>
                <th>Type</th>
                <th>Predicted</th>
                <th>Result</th>
            </tr>
        </thead>
        <tbody>
    """
    for pred in prediction_history_mock:
        result_color = "#66ff00" if pred['result'] == 'GG' or pred['result'] == '1' else "#FF5353"
        html_history_table += f"""
        <tr>
            <td>{pred['id']}</td>
            <td>{pred['match'][0]} vs {pred['match'][1]}</td>
            <td>{pred['type']}</td>
            <td>{pred['predicted']}</td>
            <td><span style="color: {result_color}; font-weight: bold;">{pred['result']}</span></td>
        </tr>
        """
    html_history_table += "</tbody></table>"
    st.markdown(html_history_table, unsafe_allow_html=True)
