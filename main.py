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
# --- MAIN CODE MEIN YAHAN REPLACE KAREIN ---
if current_page == "Predictions Zone":
    st.title("🏆 AI Match Center")
    st.caption("Updated Every 5 Minutes")
    
    # 1. Top Cards Section
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="nerdy-card"><h3>Bankers</h3><p class="neon-text">4/4 Tips Won Today</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="nerdy-card"><h3>Upcoming</h3><p>Next Match in <span class="neon-text">01:15</span></p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="nerdy-card"><h3>Success Rate</h3><p class="neon-text">82% Last 30 Days</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Featured AI Predictions")
    
    # 2. Aapka HTML Table Code Yahan Ayega (Ham ne isme styling aur logos bhi add kar diye hain)
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
            <tr>
                <td>00:30<br><span class="match-row-details">Finished</span></td>
                <td>
                    <div class="team-info" style="display: flex; align-items: center; justify-content: center; gap: 8px;">
                        FC Cincinnati <img src="https://img.asmedia.epimg.net/resizer/v2/https%3A%2F%2Fas.com%2Fimg%2Fcomunes%2Fdeporte%2Ff%2Fv1.0%2F60x60%2F4284.png?width=30&height=30" width="22"> 
                        <span style="color: #555;">vs</span> 
                        <img src="https://img.asmedia.epimg.net/resizer/v2/https%3A%2F%2Fas.com%2Fimg%2Fcomunes%2Fdeporte%2Ff%2Fv1.0%2F60x60%2F2459.png?width=30&height=30" width="22"> Toronto FC
                    </div>
                </td>
                <td><span style="background: #1e222b; padding: 4px 8px; border-radius: 4px; border: 1px solid #2d323f;">1.85</span></td>
                <td><span style="background: #1e222b; padding: 4px 8px; border-radius: 4px; border: 1px solid #2d323f;">3.80</span></td>
                <td><span style="background: #1e222b; padding: 4px 8px; border-radius: 4px; border: 1px solid #2d323f;">4.00</span></td>
                <td><span class="neon-text" style="background: rgba(102, 255, 0, 0.1); padding: 4px 10px; border-radius: 6px; border: 1px solid #66ff00;">1</span></td>
                <td>2-3</td>
                <td>No</td>
                <td><span class="neon-text">1</span></td>
                <td><span style="color: #66ff00;">4/10</span></td>
            </tr>
            <tr>
                <td>01:00<br><span class="match-row-details">Finished</span></td>
                <td>
                    <div class="team-info" style="display: flex; align-items: center; justify-content: center; gap: 8px;">
                        Cuiabá <img src="https://ssl.gstatic.com/onebox/media/sports/logos/w47S66f_S_VvKsuVw7Wv8g_48x48.png" width="22"> 
                        <span style="color: #555;">vs</span> 
                        <img src="https://ssl.gstatic.com/onebox/media/sports/logos/96m_9un6BOv77Z_A93CqXw_48x48.png" width="22"> EC Bahia BA
                    </div>
                </td>
                <td><span style="background: #1e222b; padding: 4px 8px; border-radius: 4px; border: 1px solid #2d323f;">2.30</span></td>
                <td><span style="background: #1e222b; padding: 4px 8px; border-radius: 4px; border: 1px solid #2d323f;">3.20</span></td>
                <td><span style="background: #1e222b; padding: 4px 8px; border-radius: 4px; border: 1px solid #2d323f;">3.30</span></td>
                <td><span class="neon-text" style="background: rgba(102, 255, 0, 0.1); padding: 4px 10px; border-radius: 6px; border: 1px solid #66ff00;">GG</span></td>
                <td>GG</td>
                <td>Yes</td>
                <td><span class="neon-text">GG</span></td>
                <td><span style="color: #66ff00;">6/10</span></td>
            </tr>
        </tbody>
    </table>
    """
    
    # 3. Table Render Line
    st.markdown(html_table, unsafe_allow_html=True)llow_html=True)
