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

# SOVEREIGN CONFIGURATION — S24 Ultra optimized, sidebar for Technical Glossary
st.set_page_config(page_title="GCSLC Sovereign Gateway", layout="wide", initial_sidebar_state="expanded")

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
    /* Sovereign Branding Standards - GCSLC */
    :root {
        --deep-navy: #000814;
        --gold-shimmer: #FFD700;
        --gold-grey: #b5a48b;
    }
    .sovereign-header {
        font-size: 1.1rem !important;
        letter-spacing: 0.1rem;
        text-transform: uppercase;
    }
    .glossary-sidebar {
        width: 220px;
        font-size: 0.75rem;
        color: var(--gold-grey);
        border-left: 1px solid rgba(255, 215, 0, 0.3);
        padding: 10px;
    }
    [data-testid="stSidebar"] {
        border-left: 1px solid rgba(255, 215, 0, 0.3);
        padding: 10px;
    }
    [data-testid="stSidebar"] .stMarkdown { font-size: 0.75rem; color: var(--gold-grey); }
    [data-testid="stSidebar"] .stMarkdown h3 { font-size: 0.9rem; color: var(--gold-shimmer); }
    .shimmer-text {
        background: linear-gradient(90deg, #FFD700, #FFF, #FFD700);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 3s linear infinite;
    }
    @keyframes shimmer {
        to { background-position: 200% center; }
    }
    /* NRRFC Sovereign Gateway — Deep Navy, Gold, sans-serif */
    .stApp, .main, [data-testid="stAppViewContainer"] {
        background-color: var(--deep-navy) !important;
        color: #FFFFFF;
        font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
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
    /* Meticulous table styling (Golden-Navy) — transparent bg, gold border */
    .stTable {
        background-color: transparent !important;
        border: 2px solid #FFD700 !important;
        border-radius: 15px;
    }
    .stTable th { color: #FFD700 !important; font-family: 'Inter', sans-serif; border-bottom: 2px solid #FFD700; }
    .stTable td { color: #ffffff !important; font-family: monospace; }
    /* Diamond shimmer — strike cycles for D3 nodal headline */
    @keyframes diamond-shimmer {
        0% { color: #FFD700; text-shadow: 0 0 5px #FFD700; }
        50% { color: #FFFFFF; text-shadow: 0 0 20px #FFFFFF; }
        100% { color: #FFD700; text-shadow: 0 0 5px #FFD700; }
    }
    .shimmer-node {
        animation: diamond-shimmer 2s infinite;
        font-weight: bold;
        text-align: center;
    }
    /* Gold & Navy lock — clinical table + gold-shimmer headline */
    @keyframes shimmer-opacity {
        0% { opacity: 0.7; } 50% { opacity: 1; } 100% { opacity: 0.7; }
    }
    .gold-shimmer {
        color: #FFD700 !important;
        font-weight: bold;
        text-shadow: 0 0 10px #FFD700;
        animation: shimmer-opacity 2s infinite;
    }
    table { background-color: #001F3F !important; border: 1px solid #FFD700 !important; width: 100%; color: white; }
    th { color: #FFD700 !important; text-align: left; border-bottom: 2px solid #FFD700; }
    td { border-bottom: 1px solid #334b63; padding: 8px; }
    /* GEC Sovereign Shimmer Engine (white & gold) */
    @keyframes gec-diamond-shimmer {
        0% { color: #FFD700; text-shadow: 0 0 10px #FFD700; }
        50% { color: #FFFFFF; text-shadow: 0 0 25px #FFFFFF; }
        100% { color: #FFD700; text-shadow: 0 0 10px #FFD700; }
    }
    .gec-shimmer {
        animation: gec-diamond-shimmer 2.5s infinite;
        font-weight: bold;
    }
    .brief-box {
        background-color: #001F3F;
        border: 2px solid #FFD700;
        border-radius: 10px;
        padding: 20px;
        margin-top: 25px;
    }
    /* Lean strategic styling (brainbox aesthetic) */
    h2, h3 {
        text-transform: none !important;
        font-size: 1.2rem !important;
        letter-spacing: 0.05rem;
    }
    .lean-brief {
        font-size: 0.95rem;
        line-height: 1.4;
        color: #e0e0e0;
    }
    .debt-card {
        background: rgba(0, 31, 63, 0.8);
        border: 1px solid #FFD700;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
    }
    /* Lean SFP Analytics */
    .sfp-header {
        color: #FFD700;
        font-size: 1.1rem !important;
        text-transform: none;
        margin-bottom: 5px;
    }
    .sfp-subtext {
        color: #e0e0e0;
        font-size: 0.85rem;
        margin-bottom: 20px;
    }
    .revenue-shimmer {
        color: #FFD700;
        font-weight: bold;
        animation: gec-diamond-shimmer 2s infinite;
    }
    /* Lean clinical styling (CC & Roadmap) */
    .cc-header {
        color: #FFD700;
        font-size: 1.05rem !important;
        text-transform: none;
        letter-spacing: 0.04rem;
        margin-top: 30px;
    }
    .road-step {
        border-left: 2px solid #FFD700;
        padding-left: 15px;
        margin-bottom: 15px;
    }
    .step-title {
        color: #FFD700;
        font-size: 0.9rem;
        font-weight: bold;
        text-transform: uppercase;
    }
    .step-detail {
        color: #e0e0e0;
        font-size: 0.8rem;
    }
    .sovereign-tax {
        background: rgba(255, 215, 0, 0.1);
        border: 1px dashed #FFD700;
        padding: 10px;
        text-align: center;
        border-radius: 5px;
    }
    /* S24 Ultra mobile engine (responsive strike) */
    @media (max-width: 480px) {
        .gec-card { padding: 10px; margin-bottom: 8px; border-radius: 6px; }
        .stMetric { font-size: 0.75rem !important; }
        .gec-shimmer { font-size: 0.85rem !important; }
        [data-testid="column"] { width: 100% !important; flex: 1 1 100% !important; }
    }
    .lean-header {
        color: #FFD700;
        font-size: 0.9rem;
        text-transform: none;
        letter-spacing: 0.03rem;
        margin-top: 25px;
    }
    .footer-sovereign {
        text-align: center;
        color: #a3a3a3;
        font-size: 0.85rem;
        padding: 20px 16px;
        border-top: 2px solid rgba(255, 215, 0, 0.4);
        background: rgba(0, 29, 61, 0.5);
    }
    .footer-sovereign strong { color: #FFD700; }
    /* Security & watermark — diagonal 12% opacity (KWAS-KWAS) */
    .watermark {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-25deg);
        font-size: clamp(3rem, 8vw, 5rem);
        color: rgba(212, 175, 55, 0.12);
        z-index: 9999;
        pointer-events: none;
        user-select: none;
        white-space: nowrap;
        font-weight: bold;
        font-family: 'Inter', sans-serif;
    }
    /* Welcome message — shimmering CSS text */
    @keyframes welcome-shimmer {
        0%, 100% { color: #FFF; text-shadow: 0 0 10px #FFF, 0 0 20px rgba(212, 175, 55, 0.4); }
        50% { color: #D4AF37; text-shadow: 0 0 16px #D4AF37, 0 0 32px rgba(212, 175, 55, 0.7); }
    }
    .welcome-shimmer {
        animation: welcome-shimmer 2.5s ease-in-out infinite;
        font-weight: 700;
        font-size: clamp(0.95rem, 2.2vw, 1.15rem);
        text-align: center;
        margin-bottom: 16px;
    }
    /* Sovereign Activation Alert — headline 25% smaller */
    .activation-alert {
        background: linear-gradient(145deg, #000050 0%, #000080 100%);
        border: 2px solid #D4AF37;
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        text-align: center;
    }
    .activation-alert .alert-heading {
        font-size: 0.75em; /* 25% reduction from 1em */
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #D4AF37;
        font-weight: 800;
        margin-bottom: 12px;
    }
    .activation-alert { font-size: 1.1rem; }
    /* All widget headings UPPERCASE */
    .widget-heading {
        text-transform: uppercase !important;
        letter-spacing: 0.04em;
        color: #D4AF37;
        font-weight: 700;
    }
    /* NGECC flow: Raw Coal = Blue Oval, Gasifier = Gold Box, Syngas = Pulsing Gold Box */
    .flow-raw-coal {
        background: linear-gradient(145deg, #1e3a5f 0%, #0d2137 100%);
        border: 2px solid #4a90d9;
        border-radius: 50%;
        padding: 16px 24px;
        text-align: center;
        color: #fff;
        min-width: 100px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }
    .flow-raw-coal .label { color: #a8d0ff; font-weight: bold; font-size: 0.85rem; }
    .flow-gasifier {
        background: rgba(0, 0, 80, 0.95);
        border: 2px solid #D4AF37;
        border-radius: 10px;
        padding: 16px 24px;
        text-align: center;
        color: #D4AF37;
        font-weight: bold;
        min-width: 100px;
    }
    .flow-syngas {
        background: rgba(0, 0, 80, 0.95);
        border: 2px solid #D4AF37;
        border-radius: 10px;
        padding: 16px 24px;
        text-align: center;
        color: #fff;
        min-width: 100px;
        animation: diamond-pulse 2s ease-in-out infinite;
    }
    .flow-syngas .label { color: #D4AF37; font-weight: bold; }
    /* Global Silicon Scarcity ticker (KWAS-KWAS D3 RESEARCH) */
    @keyframes ticker-pulse {
        0%, 100% { opacity: 0.85; border-color: rgba(212, 175, 55, 0.6); }
        50% { opacity: 1; border-color: #D4AF37; box-shadow: 0 0 20px rgba(212, 175, 55, 0.3); }
    }
    .silicon-ticker {
        background: linear-gradient(90deg, rgba(0,0,80,0.9) 0%, rgba(212,175,55,0.08) 50%, rgba(0,0,80,0.9) 100%);
        border: 1px solid #D4AF37;
        border-radius: 8px;
        padding: 10px 16px;
        text-align: center;
        color: #D4AF37;
        font-weight: 700;
        font-size: 0.9rem;
        animation: ticker-pulse 2s ease-in-out infinite;
    }
    .sovereign-signature {
        border-top: 1px solid #FFD700;
        margin-top: 50px;
        padding: 20px;
        text-align: center;
        background: linear-gradient(to right, transparent, rgba(255, 215, 0, 0.05), transparent);
    }
    /* NRRFC Value-Extraction Engine — Deep Navy #000080, Metallic Gold #D4AF37, S24-friendly */
    .nrrfc-module {
        background: linear-gradient(180deg, #000080 0%, #000050 100%);
        border: 2px solid #D4AF37;
        border-radius: 12px;
        padding: 24px;
        margin: 20px 0;
        max-width: 100%;
    }
    .nrrfc-title {
        color: #D4AF37;
        font-weight: 800;
        text-align: center;
        margin-bottom: 20px;
        font-size: clamp(1rem, 2.5vw, 1.4rem);
    }
    @keyframes diamond-pulse {
        0%, 100% { opacity: 0.9; transform: scale(1); box-shadow: 0 0 12px #D4AF37; }
        50% { opacity: 1; transform: scale(1.05); box-shadow: 0 0 24px #FFF, 0 0 36px rgba(212, 175, 55, 0.6); }
    }
    .diamond-bridge {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
        gap: 8px;
        margin: 12px 0;
    }
    .diamond-node {
        width: 14px;
        height: 14px;
        background: linear-gradient(135deg, #FFF 0%, #D4AF37 100%);
        transform: rotate(45deg);
        animation: diamond-pulse 2s ease-in-out infinite;
    }
    .diamond-node:nth-child(2) { animation-delay: 0.2s; }
    .diamond-node:nth-child(3) { animation-delay: 0.4s; }
    .diamond-node:nth-child(4) { animation-delay: 0.6s; }
    .flow-step {
        background: rgba(0, 0, 80, 0.9);
        border: 1px solid #D4AF37;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        color: #fff;
        min-width: 100px;
    }
    .flow-step .label { color: #D4AF37; font-weight: bold; font-size: 0.85rem; }
    .flow-arrow { color: #D4AF37; font-size: 1.5rem; margin: 0 4px; }
    .sovereign-feedstock { color: #D4AF37 !important; font-weight: bold; animation: diamond-pulse 2.5s infinite; }
    .nrrfc-footer {
        border-top: 1px solid #D4AF37;
        margin-top: 24px;
        padding-top: 16px;
        text-align: center;
        color: #e0e0e0;
        font-size: 0.95rem;
    }
    </style>
    """, unsafe_allow_html=True)
st.markdown("<div class='watermark'>GCSLC PROPRIETARY | SOVEREIGN</div>", unsafe_allow_html=True)

# HEADER: MEDALLION (embedded SVG) & SHIMMER TITLE
st.markdown(f"""
    <div class="medallion-header">
        <img src="{MEDALLION_DATA_URI}" width="150" height="150" style="border-radius:50%; border:3px solid #D4AF37; box-shadow: 0 0 24px rgba(212,175,55,0.5); display:block; margin:0 auto 16px;">
        <h1 class="shimmer-text sovereign-header">Galadiman Ruwa Center for Strategic Leadership and Communication</h1>
        <h2 style="color: #D4AF37; font-weight: 700;">GCSLC LTD/GTE</h2>
        <p style="font-style: italic; color: #c0c0c0;">Proponent of the 8R Stealth Paradigm Convergence and its Determinants</p>
    </div>
    """, unsafe_allow_html=True)

# WELCOME MESSAGE — shimmering CSS
st.markdown("""
    <p class="welcome-shimmer">Welcome, Chairman. The Eagle is Scanning. Nigeria's 638.3 MT Reserves are Live.</p>
""", unsafe_allow_html=True)

# KWAS-KWAS: Global Silicon Scarcity ticker (D3 RESEARCH)
st.markdown("""
    <div class="silicon-ticker">+12.2% Price Spike Detected. Revaluing Strategic Reserves...</div>
""", unsafe_allow_html=True)

# SOVEREIGN ACTIVATION ALERT — top-tier box, headline 25% reduced, INITIATE RESET gold button
st.markdown("""
    <div class="activation-alert">
        <div class="alert-heading">Sovereign Activation Alert</div>
    </div>
""", unsafe_allow_html=True)
if st.button("INITIATE RESET", type="primary", use_container_width=True):
    st.session_state.get("reset_clicked", True)
st.markdown("<br>", unsafe_allow_html=True)

# TECHNICAL GLOSSARY — Sidebar
with st.sidebar:
    st.markdown("### **TECHNICAL GLOSSARY**")
    st.markdown("---")
    st.markdown("**LLMs** — Large Language Models; AI systems used for sovereign data analysis and decision support.")
    st.markdown("**KPIs** — Key Performance Indicators. Primary revenue KPI: **$50.1M** monthly (SFP analytics).")
    st.markdown("**Python-to-Sovereign Feedstock** — End-to-end pipeline from Python/LLM stack to Syngas (Sovereign Feedstock) conversion and value extraction.")
    st.markdown("---")
    st.caption("2026 FX: ₦1,350 = $1")

# 1. SOVEREIGN TIMESTAMP (THE HEARTBEAT) — Format: YYYY-MM-DD HH:MM:SS UTC
current_time = time.strftime("%Y-%m-%d %H:%M:%S UTC")
st.markdown(f"""
    <div style="color: #FFD700; font-family: 'Inter', sans-serif; font-size: 1rem; margin-bottom: 20px;">
        ● Last updated: {current_time}
    </div>
""", unsafe_allow_html=True)

# RESOURCE DASHBOARD — 638.3 MT, 1,195 MW, 13 States (2026 FX: ₦1,350 = $1 for conversions)
st.markdown('<p class="widget-heading">RESOURCE DASHBOARD</p>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("RESERVES", "638.3", "MT")
with col2:
    st.metric("POWER POTENTIAL", "1,195", "MW")
with col3:
    st.metric("STATES", "13", "regions")

# 8R STEALTH PARADIGM
st.markdown('<p class="widget-heading">8R STEALTH PARADIGM NODAL</p>', unsafe_allow_html=True)
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

# 1. THE 13-STATE ASSET MAPPING (THE DIAMONDS — high-velocity pulse)
def get_shimmering_nodal_data():
    data = {
        "STATE": ["Enugu", "Kogi", "Nasarawa", "Benue", "Gombe", "Adamawa", "Bauchi", "Delta", "Edo", "Anambra", "Imo", "Abia", "Ondo"],
        "RESERVES (MT)": [168.3, 142.1, 47.7, 97.8, 62.5, 38.4, 12.5, 32.0, 18.0, 27.9, 32.1, 8.4, 4.6],
        "POWER (MW)": [402, 321, 85, 180, 110, 65, 22, 55, 30, 48, 55, 12, 10],
        "PRODUCTION": [0.01, 0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
        "STATUS": ["ACTIVE", "ACTIVE", "RESERVE", "RESERVE", "RESERVE", "RESERVE", "RESERVE", "RESERVE", "RESERVE", "RESERVE", "RESERVE", "RESERVE", "RESERVE"]
    }
    df = pd.DataFrame(data)
    df["RESERVES (MT)"] += [random.uniform(-0.15, 0.15) for _ in range(13)]
    return df

# D3: RESEARCH — 13-STATE ASSET MAPPING
st.divider()
st.markdown('<p class="widget-heading shimmer-node">D3: RESEARCH — 13-STATE ASSET MAPPING</p>', unsafe_allow_html=True)

registry_df = get_shimmering_nodal_data()
# IP masking: Nodal identifiers for public view (mask Power/Production)
registry_df["NODE_ID"] = [f"GEC-NODE-{i:03d}" for i in range(1, 14)]
display_df = registry_df[["STATE", "NODE_ID", "RESERVES (MT)", "STATUS"]]
st.table(display_df)

# 3. SIGNATURE ANCHOR
st.markdown("<div style='color: #FFD700; text-align: center; margin-top: 24px;'>SIGNATURE SECURED: Dr. Sa'ad Jaafaru | CAC: 176917792057</div>", unsafe_allow_html=True)

st.info("DATA INSIGHT: Enugu & Kogi ACTIVE (0.01). Nasarawa+ reserve. Aligns with $8,597/kg Germanium strike targets.")

# STRATEGIC BRIEF WIDGET
st.markdown("""
    <div class="brief-box">
        <h3 class="widget-heading" style="color: #D4AF37;">STRATEGIC BRIEF</h3>
        <p style="color: white; line-height: 1.6;">
            Nigeria's sub-bituminous coal is not a "dirty fuel"—it is a <span class="gec-shimmer">Sovereign Feedstock</span>.
            The NGECC, operating as an SSMV, utilizes the <span class="gec-shimmer">8R Stealth Paradigm</span>
            to extract Germanium ($8,597/kg) for AI chips and Ammonia ($430/MT) for fertilizers,
            delivering a <span class="gec-shimmer">9.6x wealth multiplier</span>.
            Funding at 51/49 from IFCs and Asian Banks de-risks the $15B Phase 1 CAPEX while preserving
            100% sovereign control over strategic data re-mapping.
        </p>
        <p style="color: #FFD700; font-weight: bold;">
            That sovereign asset clears the ₦50 Trillion national debt while powering the global AI revolution.
        </p>
    </div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# NRRFC VALUE-EXTRACTION ENGINE (PHASE 1) — Deep Navy #000080, Metallic Gold #D4AF37
# ═══════════════════════════════════════════════════════════════════════════════
st.divider()
st.markdown('<h2 class="nrrfc-title widget-heading">NRRFC VALUE-EXTRACTION ENGINE (PHASE 1)</h2>', unsafe_allow_html=True)

# 1. NGECC PROTOTYPE — Raw Coal (Blue Oval) → Gasifier (Gold Box) → Syngas (Pulsing Gold Box)
st.markdown("""
    <div class="nrrfc-module">
        <p class="widget-heading" style="margin-bottom: 12px;">NGECC MODULAR PLANT PROTOTYPE</p>
        <div style="display: flex; align-items: center; justify-content: center; flex-wrap: wrap; gap: 12px;">
            <div class="flow-raw-coal"><span class="label">Raw Coal</span></div>
            <span class="flow-arrow">→</span>
            <div class="diamond-bridge"><span class="diamond-node"></span><span class="diamond-node"></span><span class="diamond-node"></span></div>
            <div class="flow-gasifier"><span class="label">Gasifier</span></div>
            <span class="flow-arrow">→</span>
            <div class="diamond-bridge"><span class="diamond-node"></span><span class="diamond-node"></span><span class="diamond-node"></span></div>
            <div class="flow-syngas"><span class="label">Syngas</span><br><span class="sovereign-feedstock">Sovereign Feedstock</span></div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 2. ARBITRAGE WIDGET — Coal vs. Diesel (2026 FX: ₦1,350 = $1)
st.markdown('<p class="widget-heading">ARBITRAGE: COAL-TO-SYNGAS VS. DIESEL</p>', unsafe_allow_html=True)
st.caption("2026 FX: ₦1,350 = $1")
FX_RATE = 1350
DIESEL_USD_PER_L = 1.00
SYNGAS_USD_PER_L = 0.58
SAVINGS_PCT = round((1 - SYNGAS_USD_PER_L / DIESEL_USD_PER_L) * 100)
volume_liters = st.slider("Volume (Liters)", min_value=1000, max_value=500_000, value=10_000, step=1000, key="nrrfc_vol")
diesel_usd = volume_liters * DIESEL_USD_PER_L
syngas_usd = volume_liters * SYNGAS_USD_PER_L
savings_usd = diesel_usd - syngas_usd
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("Diesel cost", f"${diesel_usd:,.0f}", f"@ $1.00/L")
with col_b:
    st.metric("Coal-to-Syngas equivalent", f"${syngas_usd:,.0f}", f"@ $0.58/L")
with col_c:
    st.metric("Strike result", f"${savings_usd:,.0f} saved", f"{SAVINGS_PCT}% cost savings")
st.caption("Toggle volume to see USD savings at scale.")

# 3. DERIVATIVE STRIKE — Dynamic table: 9.6x multiplier (Germanium $6.9M, Ammonia $2.6M, Raw Coal $1.1M)
st.markdown('<p class="widget-heading">VALUE-ADDED DERIVATIVE STRIKE & MINERAL YIELD</p>', unsafe_allow_html=True)
st.caption("Base: 10,000 MT Coal")
BASE_MT = 10_000
value_df = pd.DataFrame({
    "Profit Center (SFP)": ["Germanium (Fly Ash)", "Ammonia", "Raw Coal"],
    "Output": ["800 KG", "6,000 MT", "10,000 MT"],
    "Price": ["$8,597/KG", "$430/MT", "$110/MT"],
    "Revenue (USD)": ["$6.9 M", "$2.6 M", "$1.1 M"],
})
st.dataframe(value_df, use_container_width=True, hide_index=True)
st.markdown("""
    <div class="nrrfc-module" style="margin-top: 12px;">
        <p style="color: #fff; margin: 0;"><strong>Bottom line:</strong> <span style="color: #D4AF37; font-weight: bold;">9.6× Value Multiplier</span> — from $1.1M raw to $10.6M processed.</p>
    </div>
""", unsafe_allow_html=True)

# 4. DEBT-SWAP FOOTER — 18.9x coverage of ₦50.0 T debt using 10% Big Tech CAPEX ($700B)
st.markdown("""
    <div class="nrrfc-footer">
        <p class="widget-heading">DEBT-SWAP FOOTER</p>
        <p>By capturing 10% of Global Big Tech CAPEX ($700B), we achieve <strong style="color:#D4AF37;">18.9×</strong> coverage of Nigeria's domestic debt (₦50.0 T).</p>
        <p style="font-size: 0.8rem; color: #a0a0a0;">GCSLC PROPRIETARY | SOVEREIGN — Watermark active.</p>
    </div>
""", unsafe_allow_html=True)

# NATIONAL DEBT-SWAP WIDGET
st.markdown("<p class='widget-heading gec-shimmer'>NATIONAL DEBT-SWAP: 10% BIG TECH CAPEX VS DOMESTIC DEBT</p>", unsafe_allow_html=True)
col_debt1, col_debt2, col_debt3 = st.columns(3)
with col_debt1:
    st.markdown("""<div class='debt-card'>
        <p style='color:#FFD700; font-size:0.8rem;'>10% BIG TECH CAPEX (A)</p>
        <h2 style='color:white;'>$700.00 B</h2>
        <p style='color:gray; font-size:0.7rem;'>₦945.0 T</p>
    </div>""", unsafe_allow_html=True)
with col_debt2:
    st.markdown("""<div class='debt-card'>
        <p style='color:#FFD700; font-size:0.8rem;'>NIGERIA DOMESTIC DEBT</p>
        <h2 style='color:white;'>₦50.0 T</h2>
        <p style='color:gray; font-size:0.7rem;'>$37.04 B</p>
    </div>""", unsafe_allow_html=True)
with col_debt3:
    st.markdown("""<div class='debt-card'>
        <p style='color:#FFD700; font-size:0.8rem;'>COVERAGE (10% CAPEX ÷ DEBT)</p>
        <h2 class='gec-shimmer'>18.9x</h2>
        <p style='color:gray; font-size:0.7rem;'>Sovereign Surplus</p>
    </div>""", unsafe_allow_html=True)

# SFP ANALYTICS WIDGET
st.markdown('<p class="widget-heading sfp-header gec-shimmer">SFP ANALYTICS — $50.1M MONTHLY REVENUE</p>', unsafe_allow_html=True)
st.markdown('<div class="sfp-subtext">50,000 MT coal input · 4 Profit Centers · Sovereign Feedstock</div>', unsafe_allow_html=True)
st.markdown("""
    <table style="width:100%; border-collapse: collapse; border: 1px solid #FFD700; background-color: #001F3F;">
        <tr style="background-color: #001d3d; color: #FFD700; font-size: 0.8rem;">
            <th style="padding: 8px; text-align: left;">PROFIT CENTER</th><th style="padding: 8px; text-align: left;">OUTPUT</th><th style="padding: 8px; text-align: left;">MONTHLY REVENUE (USD)</th>
        </tr>
        <tr style="color: #e0e0e0;"><td style="padding: 8px; border-bottom: 1px solid #334b63;">Syngas</td><td style="padding: 8px; border-bottom: 1px solid #334b63;">Sovereign Feedstock</td><td class="revenue-shimmer" style="padding: 8px; border-bottom: 1px solid #334b63;">$15.20 M</td></tr>
        <tr style="color: #e0e0e0;"><td style="padding: 8px; border-bottom: 1px solid #334b63;">Germanium</td><td style="padding: 8px; border-bottom: 1px solid #334b63;">Fly ash extraction</td><td class="revenue-shimmer" style="padding: 8px; border-bottom: 1px solid #334b63;">$18.50 M</td></tr>
        <tr style="color: #e0e0e0;"><td style="padding: 8px; border-bottom: 1px solid #334b63;">Ammonia</td><td style="padding: 8px; border-bottom: 1px solid #334b63;">Fertilizer grade</td><td class="revenue-shimmer" style="padding: 8px; border-bottom: 1px solid #334b63;">$9.81 M</td></tr>
        <tr style="color: #e0e0e0;"><td style="padding: 8px; border-bottom: 1px solid #334b63;">Silicon</td><td style="padding: 8px; border-bottom: 1px solid #334b63;">Semiconductor grade</td><td class="revenue-shimmer" style="padding: 8px; border-bottom: 1px solid #334b63;">$6.50 M</td></tr>
        <tr style="background-color: #001d3d; font-weight: bold;">
            <td colspan="2" style="color: #FFD700; padding: 8px;">Total Monthly Revenue</td>
            <td class="revenue-shimmer" style="font-size: 1.1rem; padding: 8px;">$50.1 M</td>
        </tr>
    </table>
""", unsafe_allow_html=True)

# COST CENTERS (CC)
st.markdown('<p class="widget-heading lean-header gec-shimmer">COST CENTERS (CC) — OPERATIONAL OUTLAYS</p>', unsafe_allow_html=True)
cc_cols = st.columns(3)
with cc_cols[0]:
    st.markdown("<div class='debt-card'><p style='color:#FFD700; font-size:0.7rem;'>LOGISTICS</p><p style='color:white; font-size:0.75rem;'>fleet, rail & port ops</p></div>", unsafe_allow_html=True)
with cc_cols[1]:
    st.markdown("<div class='debt-card'><p style='color:#FFD700; font-size:0.7rem;'>LEAN REMUNERATION</p><p style='color:white; font-size:0.75rem;'>minimal headcount</p></div>", unsafe_allow_html=True)
with cc_cols[2]:
    st.markdown("<div class='debt-card'><p style='color:#FFD700; font-size:0.7rem;'>AI TECHNOLOGY</p><p style='color:white; font-size:0.75rem;'>python / llm stack</p></div>", unsafe_allow_html=True)

# 100-DAY SSMV ROADMAP
st.markdown('<p class="widget-heading lean-header gec-shimmer">100-DAY SSMV ROADMAP</p>', unsafe_allow_html=True)
roadmap_logic = [
    ("reset", "sovereign data audit & baseline"),
    ("research", "ifc / asian bank term sheets (51/49)"),
    ("restructure", "ngecc plant commissioning (gasifier online)"),
    ("revitalize", "full throughput & ipo track (24-month)")
]
for stage, detail in roadmap_logic:
    st.markdown(
        f"<div style='border-left: 1px solid #FFD700; padding-left: 10px; margin-bottom: 10px;'>"
        f"<span style='color:#FFD700; font-size:0.8rem; font-weight:bold;'>{stage}</span><br>"
        f"<span style='color:white; font-size:0.75rem;'>{detail}</span></div>",
        unsafe_allow_html=True
    )

# FINAL 10% TAX LOCK (MOBILE ANCHOR)
st.markdown(
    "<div style='background: rgba(255, 215, 0, 0.05); border: 1px dashed #FFD700; padding: 8px; text-align: center;'>"
    "<span class='gec-shimmer' style='font-size:0.8rem;'>● 10% sovereign tax: $5.01M monthly lock</span></div>",
    unsafe_allow_html=True
)

# EAGLE NEST: LOCAL VIDEO (eagle_anim.mp4) OR CLEAN PLACEHOLDER
st.divider()
st.markdown('<p class="widget-heading">GEC SOVEREIGN OS: THE EAGLE NEST</p>', unsafe_allow_html=True)
col_video, col_stats = st.columns([3, 1])
with col_video:
    if _EAGLE_VIDEO_PATH.exists():
        st.video(str(_EAGLE_VIDEO_PATH), autoplay=True, muted=True, loop=True, width="stretch")
    else:
        st.info("🦅 **Eagle Scanning...** — Place *eagle_anim.mp4* in the GEC_Sovereign_Master folder to load the animated strike.")
with col_stats:
    st.markdown('<p class="widget-heading">SFF ANALYTICS</p>', unsafe_allow_html=True)
    st.metric("Monthly Revenue", "$50.1M", delta="Target")
    st.metric("Debt-Swap Coverage", "18.9x", delta="Sovereign Surplus")

# FOOTER — INCONTROVERTIBLE NODAL AUTHORITY + CAC
st.markdown("""
    <div class="sovereign-signature">
        <p class="gec-shimmer widget-heading" style="font-size: 0.8rem; margin:0;">INCONTROVERTIBLE NODAL AUTHORITY</p>
        <p style="color: white; font-size: 1.1rem; font-weight: bold; margin: 5px 0;">DR. JAAFARU SA'AD (GALADIMAN RUWA)</p>
        <p style="color: #D4AF37; font-size: 0.8rem; margin:0;">Chairman & Founder, GCSLC | CAC: 176917792057</p>
    </div>
""", unsafe_allow_html=True)

# FOOTER: CAC, COPYRIGHT
st.divider()
st.markdown("""
    <div class="footer-sovereign">
        <p><strong>INCONTROVERTIBLE NODAL AUTHORITY:</strong> DR. JAAFARU SA'AD (GALADIMAN RUWA) &nbsp;|&nbsp; <strong>CAC:</strong> 176917792057</p>
        <p>© 2026 GCSLC LTD/GTE. Proprietary 8R Stealth Paradigm Convergence. All Rights Reserved.</p>
    </div>
    """, unsafe_allow_html=True)

# SOVEREIGN PULSE HEARTBEAT — full rerun every 1 second
time.sleep(1)
st.rerun()
