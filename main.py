import streamlit as st
import pandas as pd
import requests
from io import StringIO

# --- 1. PAGE SETUP & CONFIG ---
st.set_page_config(page_title="Nerdy Earners | AI Predictions", layout="wide")

# --- 2. GLOBAL CUSTOM CSS (NERDYTIPS STYLE) ---
st.markdown("""
<style>
    /* Global Background and Colors */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0c0e11 !important;
        color: #e6e8eb !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #111417 !important;
    }
    
    /* Prediction Cards (like 'Bankers', 'Upcoming' in screenshot) */
    .nerdy-card {
        background-color: rgba(20, 24, 28, 0.7);
        border: 1px solid #2a2f36;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: transform 0.2s;
        margin-bottom: 10px;
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
    .neon-text {
        color: #66ff00 !important;
        font-weight: bold;
    }

    /* Custom Match Table (inspired by screenshot) */
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
    
    /* Native Button Overrides to make them Neon Green */
    .stButton>button {
        background: linear-gradient(135deg, #a5ff33 0%, #66ff00 100%) !important;
        color: #0c0e11 !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
    }
    
    /* Wallet Info Panels */
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

active_matches_data = [
    {
        'date': '00:30', 'match': ('FC Cincinnati', 'Toronto FC'), 'logos': ('https://raw.githubusercontent.com/davide-neri/logos/master/cincinnati.png', 'https://raw.githubusercontent.com/davide-neri/logos/master/toronto_fc.png'),
        'odds': (1.85, 3.80, 4.00), 'tip': '1', 'goals': '2-3', 'gg': 'No', 'best_tip': '1', 'trust': '4/10'
    },
    {
        'date': '01:00', 'match': ('Cuiaba Esporte MT', 'EC Bahia BA'), 'logos': ('https://raw.githubusercontent.com/davide-neri/logos/master/cuiaba.png', 'https://raw.githubusercontent.com/davide-neri/logos/master/bahia.png'),
        'odds': (2.30, 3.20, 3.30), 'tip': 'GG', 'goals': 'GG', 'gg': 'Yes', 'best_tip': 'GG', 'trust': '6/10'
    }
]

# --- 4. SIDEBAR & NAVIGATION ---
with st.sidebar:
    st.title("Nerdy Earners")
    st.caption("AI-Powered Predictions")

    if st.session_state.logged_in:
        st.success(f"Welcome, {st.session_state.user_name}!")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    else:
        st.subheader("Account Login")
        st.text_input("Mobile Number", key="login_phone")
        st.text_input("Password", type="password", key="login_pass")
        if st.button("Sign In Securely", type="primary"):
            st.session_state.logged_in = True
            st.session_state.user_name = "Rabia"
            st.rerun()

    st.markdown("---")
    current_page = st.selectbox("Navigate", ["Predictions Zone", "My Wallet"])

# --- 5. MAIN CONTENT ---
if current_page == "Predictions Zone":
    st.title("🏆 AI Match Center")
    st.caption("Updated Every 5 Minutes")
    
    # Cards layout
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="nerdy-card"><h3>Bankers</h3><p class="neon-text">4/4 Tips Won Today</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="nerdy-card"><h3>Upcoming</h3><p>Next Match in <span class="neon-text">01:15</span></p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="nerdy-card"><h3>Success Rate</h3><p class="neon-text">82% Last 30 Days</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Featured AI Predictions")
    
    # Custom Rendered Table
    html_table = """
    <table class="nerdy-table">
        <thead>
            <tr>
                <th>Date</th><th>Match Details</th><th>1</th><th>X</th><th>2</th><th>TIP</th><th>Goals</th><th>GG</th><th>Best TIP</th><th>Trust</th>
            </tr>
        </thead>
        <tbody>
    """
    for match in active_matches_data:
        html_table += f"""
        <tr>
            <td>{match['date']}<br><span class="match-row-details">Finished</span></td>
            <td><div class="team-info">{match['match'][0]} vs {match['match'][1]}</div></td>
            <td>{match['odds'][0]}</td><td>{match['odds'][1]}</td><td>{match['odds'][2]}</td>
            <td><span class="neon-text">{match['tip']}</span></td><td>{match['goals']}</td><td>{match['gg']}</td>
            <td><span class="neon-text">{match['best_tip']}</span></td><td>{match['trust']}</td>
        </tr>
        """
    html_table += "</tbody></table>"
    st.markdown(html_table, unsafe_allow_html=True)

elif current_page == "My Wallet":
    st.title("💰 AI Investor Wallet")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="info-panel">
            <h3>Account Balance</h3>
            <p style="font-size: 2em; color: #66ff00; font-weight: bold;">PKR {st.session_state.balance:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="info-panel">
            <h3>Account Status</h3>
            <p>Verification: <span class="neon-text">Verified</span></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    dep_col, with_col = st.columns(2)
    with dep_col:
        st.subheader("Deposit (Investment)")
        dep_amount = st.number_input("Enter Amount (PKR)", min_value=100)
        trx_id = st.text_input("Transaction ID")
        if st.button("Submit Deposit"):
            st.success("Request sent for verification!")
            
    with with_col:
        st.subheader("Withdraw Rewards")
        with_amount = st.number_input("Withdraw Amount (PKR)", min_value=100)
        if st.button("Request Withdrawal"):
            if with_amount <= st.session_state.balance:
                st.session_state.balance -= with_amount
                st.success("Withdrawal request submitted!")
                st.rerun()
            else:
                st.error("Insufficient balance.")
# Dhundiye jahan "if current_page == "Predictions Zone":" likha hai, uske neeche cards ke baad ye paste karein:

    st.markdown("---")
    st.subheader("Featured AI Predictions")
    
    # Aapka HTML code yahan st.markdown ke andar aayega:
    html_table = """
    <table class="nerdy-table">
        <thead>
            <tr>
                <th>Date</th><th>Match Details</th><th>1</th><th>X</th><th>2</th><th>TIP</th><th>Goals</th><th>GG</th><th>Best TIP</th><th>Trust</th>
            </tr>
        </thead>
        <tbody>
            <tr>    
                <td>00:30<br><span class="match-row-details">Finished</span></td>    
                <td><div class="team-info">FC Cincinnati vs Toronto FC</div></td>    
                <td>1.85</td><td>3.8</td><td>4.0</td>    
                <td><span class="neon-text">1</span></td><td>2-3</td><td>No</td>    
                <td><span class="neon-text">1</span></td><td>4/10</td>
            </tr>
            <tr>    
                <td>01:00<br><span class="match-row-details">Finished</span></td>    
                <td><div class="team-info">Cuiaba Esporte MT vs EC Bahia BA</div></td>    
                <td>2.3</td><td>3.2</td><td>3.3</td>    
                <td><span class="neon-text">GG</span></td><td>GG</td><td>Yes</td>    
                <td><span class="neon-text">GG</span></td><td>6/10</td>
            </tr>
        </tbody>
    </table>
    """
    
    # Is line ke zariye ye website par show hoga:
    st.markdown(html_table, unsafe_allow_html=True)
