import streamlit as st
import base64
from pathlib import Path

# SOVEREIGN CONFIGURATION
st.set_page_config(page_title="GCSLC Sovereign Gateway", layout="wide")

# Asset folder: same directory as this script
_ASSETS = Path(__file__).resolve().parent

# BASE64 ENCODER FOR LOCAL ASSETS
def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# CUSTOM CSS: THE NAVY VOID & SHIMMER (class names must not start with a digit)
st.markdown("""
    <style>
    @keyframes shimmer-white {
        0% { color: #FFFFFF; text-shadow: 0 0 5px #FFFFFF; }
        50% { color: #FFD700; text-shadow: 0 0 20px #FFD700; }
        100% { color: #FFFFFF; text-shadow: 0 0 5px #FFFFFF; }
    }
    .stApp {
        background-color: #000814; /* Deep Navy Base */
        color: #FFFFFF;
    }
    .medallion-header {
        text-align: center;
        padding: 40px;
        border-bottom: 2px solid #FFD700;
        background: radial-gradient(circle, #001d3d 0%, #000814 100%);
    }
    .shimmer-text {
        animation: shimmer-white 3s infinite;
        font-weight: 800;
        text-transform: uppercase;
    }
    .eightr-card {
        background: rgba(0, 29, 61, 0.7);
        border: 1px solid #FFD700;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    @keyframes navy-shimmer {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    div[data-testid="stVideo"] {
        width: 100% !important;
        max-width: 100%;
        background: linear-gradient(135deg, #001d3d 0%, #000814 50%, #001d3d 100%);
        background-size: 200% 200%;
        animation: navy-shimmer 4s ease infinite;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid rgba(255, 215, 0, 0.3);
    }
    div[data-testid="stVideo"] video {
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

# THE HEADER: MEDALLION & SIGNATURE
_logo_path = _ASSETS / "gcslc_logo.png"
logo_b64 = get_base64(_logo_path)
st.markdown(f"""
    <div class="medallion-header">
        <img src="data:image/png;base64,{logo_b64}" width="150" style="border-radius:50%; border:3px solid #FFD700; box-shadow: 0 0 20px #FFD700;">
        <h1 class="shimmer-text">Galadiman Ruwa Center for Strategic Leadership and Communication</h1>
        <h2 style="color: #FFD700;">GCSLC LTD/GTE</h2>
        <p style="font-style: italic; color: #a3a3a3;">Proponent of the 8R Stealth Paradigm Convergence and its Determinants</p>
    </div>
    """, unsafe_allow_html=True)

st.success("⚡ HIGH-VELOCITY SOVEREIGN WELCOME. EAGLE IS ON THE NEST.")

# THE EAGLE NEST (ANIMATED VIDEO SECTION — 100% width, Navy shimmer background)
st.write("### 🦅 GEC SOVEREIGN OS: THE EAGLE NEST")
col_video, col_stats = st.columns([3, 1])

_eagle_video_path = _ASSETS / "eagle_anim.mp4"
with col_video:
    st.video(str(_eagle_video_path), autoplay=True, muted=True, loop=True, width="stretch")

with col_stats:
    st.write("### 💎 SFF ANALYTICS")
    st.metric("Monthly Revenue", "$50.1M", delta="Target")
    st.metric("Debt-Swap Coverage", "18.9x", delta="Sovereign Surplus")

# FOOTER: CAC, SIGNATURE, & COPYRIGHT
st.divider()
st.markdown("""
    <div style="text-align: center; color: #a3a3a3; font-size: 0.8rem;">
        <p><b>SIGNATURE SECURED:</b> Dr. Sa'ad Jaafaru, Chairman | <b>CAC:</b> 176917792057</p>
        <p>© 2026 GCSLC LTD/GTE. Proprietary 8R Stealth Paradigm Convergence. All Rights Reserved.</p>
    </div>
    """, unsafe_allow_html=True)
