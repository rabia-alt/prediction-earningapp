import streamlit as st
import pandas as pd
import requests
from io import StringIO

# --- 1. PAGE SETUP & INITIAL CONFIG ---
st.set_page_config(page_title="Nerdy Earners | AI Predictions", layout="wide")

# --- 2. PREMIUM NERDYTIPS STYLING ENGINE (CSS INJECTION) ---
st.markdown("""
<style>
    /* Pure Dark Theme Background & Text */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #0c0e11 !important;
        color: #e6e8eb !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Dark Profile Styling */
    [data-testid="stSidebar"] {
        background-color: #111417 !important;
    }
    
    /* Top Analytical Dashboard Cards */
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
        font-size: 1.2em;
    }
    
    /* Custom HTML Match Layout Styling */
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
        padding: 18px 12px;
        text-align: center;
        border-bottom: 1px solid #1c2126;
        color: #e6e8eb;
        font-size: 0.95em;
    }
    .match-row-details {
        color: #6c757d;
        font-size: 0.8em;
    }
    
    /* Global Neon Glowing Text */
    .neon-text {
        color: #66ff00 !important;
        font-weight: bold;
    }
    
    /* Native App Buttons Overrides to Neon Glow */
    .stButton>button {
        background: linear-gradient(135deg, #a5ff33 0%, #66ff00 100%) !important;
        color: #0c0e11 !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
        width: 100%;
    }
    
    /* Wallet Interface Blocks */
    .info-panel {
        background-color: #14181c;
        border: 1px solid #2a2f36;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. PERSISTENT STORAGE MANAGEMENT (SESSION STATE) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = "GuestUser"
if 'balance' not in st.session_state:
    st.session_state.balance = 1250.00  # Default initial mock value
if 'deposit_requests' not in st.session_state:
    st.session_state.deposit_requests = []
if 'withdraw_requests' not in st.session_state:
    st.session_state.withdraw_requests = []

# --- 4. NAVIGATION CONTROL PANEL (SIDEBAR) ---
with st.sidebar:
    st.title("🔋 Nerdy Earners")
    st.caption("AI-Powered Match Analytics Engine")

    if st.session_state.logged_in:
        st.success(f"Active User: {st.session_state.user_name}")
        st.metric("Wallet Balance", f"PKR {st.session_state.balance:,.2f}")
        if st.button("Secure Logout"):
            st.session_state.logged_in = False
            st.rerun()
    else:
        st.subheader("Account Login Gateway")
        st.text_input("Mobile Number", key="login_phone", placeholder="e.g. 3415687754")
        st.caption("⚠️ **Hint:** Agar access issue ho toh start se '0' remove kar ke try karein.")
        st.text_input("Secure Password", type="password", key="login_pass")
        if st.button("Sign In Securely"):
            # Simple design validation toggle
            if st.session_state.login_phone and st.session_state.login_pass:
                st.session_state.logged_in = True
                st.session_state.user_name = "Rabia"
                st.rerun()
            else:
                st.error("Fields cannot be left blank.")

    st.markdown("---")
    current_page = st.selectbox("Navigate Workspace", ["Predictions Center", "Investor Wallet"])

# --- 5. APPLICATION CORE WORKSPACES ---

# WORKSPACE A: PREDICTIONS ZONE
if current_page == "Predictions Center":
    st.title("🏆 AI Match Matrix")
    st.caption("Real-Time Probabilities Engine (v3.2 Active)")
    
    # Core Analytic Analytical Cards Header Layer
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="nerdy-card"><h3>🔒 Bankers Performance</h3><p class="neon-text">4 / 4 Clear Slates Today</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="nerdy-card"><h3>⏳ Queue Horizon</h3><p>Next AI Calculation in <span class="neon-text">01:12:45</span></p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="nerdy-card"><h3>📈 Historical Matrix</h3><p class="neon-text">82% Weighted Win Ratio</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Featured AI Predictions")
    
    # Highly Optimized HTML Structural Injection Container
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
                    <div style="display: flex; align-items: center; justify-content: center; gap: 8px;">
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
                    <div style="display: flex; align-items: center; justify-content: center; gap: 8px;">
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
    # Raw HTML execution logic block
    st.markdown(html_table, unsafe_allow_html=True)

# WORKSPACE B: INVESTOR WALLET MANAGEMENT
elif current_page == "Investor Wallet":
    st.title("💰 Capital Allocation & Liquidity")
    
    col_bal, col_stat = st.columns(2)
    with col_bal:
        st.markdown(f"""
        <div class="info-panel">
            <h3>Liquid Balance Pool</h3>
            <p style="font-size: 2.2em; color: #66ff00; font-weight: bold; margin: 0;">PKR {st.session_state.balance:,.2f}</p>
        </div>
        """, unsafe_allow_html=True)
    with col_stat:
        st.markdown("""
        <div class="info-panel">
            <h3>Verification State</h3>
            <p style="margin: 0; font-size: 1.1em;">Status: <span class="neon-text">Fully Cryptographically Verified ✅</span></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    dep_panel, with_panel = st.columns(2)
    
    with dep_panel:
        st.subheader("Inbound Investment (Deposit)")
        with st.expander("Show Inbound Gateway Info", expanded=True):
            st.info("⚡ **EasyPaisa / JazzCash Account:** 03415687754\\n\\n**Account Title:** Rabia Hafeez")
        dep_amount = st.number_input("Transfer Capital Amount (PKR)", min_value=100, step=50, key="inp_dep_amt")
        trx_id = st.text_input("Electronic Transaction ID (TrxID)", placeholder="e.g. 8945729104", key="inp_trx")
        
        if st.button("Transmit Deposit Log"):
            if trx_id:
                st.session_state.deposit_requests.append({'Amount': dep_amount, 'Transaction ID': trx_id, 'Status': 'Pending Manual Sync'})
                st.success("Log submitted! Data queued for processing.")
            else:
                st.error("Transaction ID required for backend ledger verification.")
                
    with with_panel:
        st.subheader("Outbound Liquidations (Withdraw)")
        with_amount = st.number_input("Request Liquidation Volume (PKR)", min_value=100, step=50, key="inp_with_amt")
        
        if st.button("Authorize Liquidation"):
            if with_amount <= st.session_state.balance:
                st.session_state.balance -= with_amount
                st.session_state.withdraw_requests.append({'Amount': with_amount, 'Status': 'Disbursing'})
                st.success("Liquidation event authorized successfully!")
                st.rerun()
            else:
                st.error("Insufficient capitalization pool available.")
