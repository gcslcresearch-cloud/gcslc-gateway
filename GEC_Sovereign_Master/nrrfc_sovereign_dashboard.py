"""
GCSLC Sovereign Gateway — NRRFC Dashboard (Port 8051).
Zero local file dependencies: web-hosted placeholders for medallion and video.
Deep Navy background, Gold/White shimmer, 8R Determinant cards. CAC & Chairman Lock.
© 2026 GCSLC LTD/GTE.
"""
import streamlit as st
import base64
import pandas as pd
import random
import time
from pathlib import Path

# SOVEREIGN CONFIGURATION
st.set_page_config(page_title="GCSLC Sovereign Gateway", layout="wide", initial_sidebar_state="collapsed")

# WEB-HOSTED / EMBEDDED ASSETS (no local files)
# Medallion: inline SVG (gold circle, GCSLC) — zero file dependency
MEDALLION_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 150 150">
  <defs><linearGradient id="gold" x1="0%%" y1="0%%" x2="100%%" y2="100%%"><stop offset="0%%" style="stop-color:#FFD700"/><stop offset="100%%" style="stop-color:#B8860B"/></linearGradient></defs>
  <circle cx="75" cy="75" r="72" fill="none" stroke="url(#gold)" stroke-width="4"/>
  <circle cx="75" cy="75" r="58" fill="#001d3d"/>
  <text x="75" y="78" text-anchor="middle" fill="#FFD700" font-size="20" font-weight="bold" font-family="system-ui,sans-serif">GCSLC</text>
</svg>"""
MEDALLION_DATA_URI = "data:image/svg+xml;base64," + base64.b64encode(MEDALLION_SVG.encode()).decode()

# Eagle video: local file (same folder as this script); Path.exists() avoids FileNotFoundError
_EAGLE_VIDEO_PATH = Path(__file__).resolve().parent / "eagle_anim.mp4"

# CUSTOM CSS: DEEP NAVY BASE, GOLD/WHITE SHIMMER, HIGHLY VISIBLE 8R CARDS
st.markdown("""
    <style>
    /* Strict Deep Navy background */
    .stApp, .main, [data-testid="stAppViewContainer"] {
        background-color: #000814 !important;
        color: #FFFFFF;
    }
    @keyframes shimmer-gold-white {
        0% { color: #FFFFFF; text-shadow: 0 0 8px #FFFFFF, 0 0 12px rgba(255,215,0,0.3); }
        50% { color: #FFD700; text-shadow: 0 0 12px #FFD700, 0 0 24px rgba(255,215,0,0.6); }
        100% { color: #FFFFFF; text-shadow: 0 0 8px #FFFFFF, 0 0 12px rgba(255,215,0,0.3); }
    }
    .shimmer-text {
        animation: shimmer-gold-white 2.5s ease-in-out infinite;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .medallion-header {
        text-align: center;
        padding: 36px 24px;
        border-bottom: 3px solid #FFD700;
        background: linear-gradient(180deg, #001d3d 0%, #000814 100%);
    }
    /* 8R Determinant cards — high visibility */
    .determinant-card {
        background: linear-gradient(145deg, rgba(0, 45, 90, 0.95) 0%, rgba(0, 29, 61, 0.98) 100%);
        border: 2px solid #FFD700;
        padding: 20px 16px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(255, 215, 0, 0.2), inset 0 1px 0 rgba(255,255,255,0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .determinant-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 28px rgba(255, 215, 0, 0.35);
    }
    .determinant-title {
        color: #FFD700;
        font-size: 1.15rem;
        font-weight: 800;
        margin-bottom: 8px;
        letter-spacing: 1px;
    }
    .determinant-desc {
        color: #e0e0e0;
        font-size: 0.95rem;
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
        border: 1px solid rgba(255, 215, 0, 0.35);
    }
    div[data-testid="stVideo"] video { width: 100% !important; }
    /* Gold shimmer gradient on text (D3 headline) */
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    .shimmer-headline {
        font-family: 'Inter', sans-serif;
        font-weight: bold;
        color: #FFD700;
        background: linear-gradient(90deg, #FFD700 25%, #FFFACD 50%, #FFD700 75%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 3s linear infinite;
    }
    /* Tables: navy background, gold border (no white) */
    .stDataFrame, div[data-testid="stDataFrame"], div[data-testid="stTable"] {
        background-color: #001F3F !important;
        border: 1px solid #FFD700;
    }
    /* Shimmer strike cycles — gold-pulse for D3 nodal headline */
    @keyframes gold-pulse {
        0% { text-shadow: 0 0 5px #FFD700; opacity: 0.8; }
        50% { text-shadow: 0 0 20px #FFFACD; opacity: 1; }
        100% { text-shadow: 0 0 5px #FFD700; opacity: 0.8; }
    }
    .shimmer-nodal {
        color: #FFD700 !important;
        font-weight: bold;
        animation: gold-pulse 2s infinite;
        text-align: center;
    }
    /* Force navy table visibility (13-state strike) */
    .stTable {
        background-color: #001F3F !important;
        border: 2px solid #FFD700 !important;
        border-radius: 10px;
    }
    .stTable th { color: #FFD700 !important; background-color: #001d3d !important; }
    .stTable td { color: #ffffff !important; }
    .footer-sovereign {
        text-align: center;
        color: #a3a3a3;
        font-size: 0.85rem;
        padding: 20px 16px;
        border-top: 2px solid rgba(255, 215, 0, 0.4);
        background: rgba(0, 29, 61, 0.5);
    }
    .footer-sovereign strong { color: #FFD700; }
    </style>
    """, unsafe_allow_html=True)

# HEADER: MEDALLION (embedded SVG) & SHIMMER TITLE
st.markdown(f"""
    <div class="medallion-header">
        <img src="{MEDALLION_DATA_URI}" width="150" height="150" style="border-radius:50%; border:3px solid #FFD700; box-shadow: 0 0 24px rgba(255,215,0,0.5); display:block; margin:0 auto 16px;">
        <h1 class="shimmer-text">Galadiman Ruwa Center for Strategic Leadership and Communication</h1>
        <h2 style="color: #FFD700; font-weight: 700;">GCSLC LTD/GTE</h2>
        <p style="font-style: italic; color: #c0c0c0;">Proponent of the 8R Stealth Paradigm Convergence and its Determinants</p>
    </div>
    """, unsafe_allow_html=True)

st.success("⚡ HIGH-VELOCITY SOVEREIGN WELCOME. EAGLE IS ON THE NEST.")

# 1. SOVEREIGN TIMESTAMP (THE HEARTBEAT) — Format: YYYY-MM-DD HH:MM:SS UTC
current_time = time.strftime("%Y-%m-%d %H:%M:%S UTC")
st.markdown(f"""
    <div style="color: #FFD700; font-family: 'Inter', sans-serif; font-size: 1rem; margin-bottom: 20px;">
        ● Last updated: {current_time}
    </div>
""", unsafe_allow_html=True)

# 2. DYNAMIC NODAL PULSE — metrics fluctuate slightly to simulate real-time monitoring of proven reserves
col1, col2, col3 = st.columns(3)
with col1:
    reserves = 640.2 + random.uniform(-1.8, 1.8)
    st.metric("TOTAL PROVEN RESERVES", f"{reserves:.1f}", "million tonnes")
with col2:
    power = 1200 + random.randint(-5, 5)
    st.metric("POWER POTENTIAL", f"{power}", "MW (AI DC ready)")
with col3:
    st.metric("STATES WITH RESERVES", "13", "regions")

# 8R STEALTH PARADIGM — HIGHLY VISIBLE DETERMINANT CARDS
st.write("### 🛡️ 8R STEALTH PARADIGM NODAL")
cols = st.columns(4)
determinants = [
    ("D1", "REFINE", "Subsoil Density Logic"),
    ("D2", "RESET", "639.3M MT Coal Reserve"),
    ("D3", "RESEARCH", "13-State Mapping"),
    ("D4", "RESTRUCTURE", "NGECC-SSMV Legal Lock"),
    ("D5", "RESUSCITATE", "1,200 MW Power Strike"),
    ("D6", "REVITALIZE", "12% WL Cassava Recovery"),
    ("D7", "RE-ENGINEER", "$100B AI Compute Gap"),
    ("D8", "RETAIN", "85% Talon Lock Registry"),
]
for i, (code, name, desc) in enumerate(determinants):
    with cols[i % 4]:
        st.markdown(f"""
            <div class="determinant-card">
                <div class="determinant-title">{code}: {name}</div>
                <p class="determinant-desc">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

# 1. THE 13-STATE SOVEREIGN REGISTRY (high-velocity pulse on reserves)
def get_13_state_nodal():
    data = {
        "STATE": ["Enugu", "Kogi", "Nasarawa", "Benue", "Gombe", "Adamawa", "Bauchi", "Delta", "Edo", "Anambra", "Imo", "Abia", "Ondo"],
        "RESERVES (MT)": [168.2, 142.1, 47.9, 98.2, 62.1, 38.5, 12.1, 32.1, 18.0, 27.9, 32.1, 8.4, 4.2],
        "POWER (MW)": [401, 319, 85, 180, 110, 65, 22, 55, 30, 48, 55, 12, 10],
        "PRODUCTION": ["0.01", "0.01", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
        "STATUS": ["ACTIVE", "ACTIVE", "RESERVE", "RESERVE", "RESERVE", "RESERVE", "RESERVE", "RESERVE", "RESERVE", "RESERVE", "RESERVE", "RESERVE", "RESERVE"]
    }
    df = pd.DataFrame(data)
    df["RESERVES (MT)"] = df["RESERVES (MT)"].apply(lambda x: x + random.uniform(-0.5, 0.5))
    return df

# 2. THE SHIMMERING NODAL HEADLINE
st.divider()
st.markdown('<h2 class="shimmer-nodal">D3: RESEARCH - 13-STATE ASSET MAPPING</h2>', unsafe_allow_html=True)

# 3. THE 13-STATE TABLE STRIKE
st.table(get_13_state_nodal())

st.info("DATA INSIGHT: Enugu & Kogi ACTIVE (0.01 production). Nasarawa+ reserve. Aligns with $8,597/kg Germanium strike targets.")

# EAGLE NEST: LOCAL VIDEO (eagle_anim.mp4) OR CLEAN PLACEHOLDER
st.divider()
st.write("### 🦅 GEC SOVEREIGN OS: THE EAGLE NEST")
col_video, col_stats = st.columns([3, 1])
with col_video:
    if _EAGLE_VIDEO_PATH.exists():
        st.video(str(_EAGLE_VIDEO_PATH), autoplay=True, muted=True, loop=True, width="stretch")
    else:
        st.info("🦅 **Eagle Scanning...** — Place *eagle_anim.mp4* in the GEC_Sovereign_Master folder to load the animated strike.")
with col_stats:
    st.write("### 💎 SFF ANALYTICS")
    st.metric("Monthly Revenue", "$50.1M", delta="Target")
    st.metric("Debt-Swap Coverage", "18.9x", delta="Sovereign Surplus")

# FOOTER: CAC, SIGNATURE, COPYRIGHT
st.divider()
st.markdown("""
    <div class="footer-sovereign">
        <p><strong>SIGNATURE SECURED:</strong> Dr. Sa'ad Jaafaru, Chairman & Founder &nbsp;|&nbsp; <strong>CAC:</strong> 176917792057</p>
        <p>© 2026 GCSLC LTD/GTE. Proprietary 8R Stealth Paradigm Convergence. All Rights Reserved.</p>
    </div>
    """, unsafe_allow_html=True)

# 3. GLOBAL HEARTBEAT — refreshes the entire dashboard every 2 seconds
time.sleep(2)
st.rerun()
