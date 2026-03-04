import streamlit as st

# SOVEREIGN CONFIGURATION (Optimized for S24 Ultra & Desktop)
st.set_page_config(page_title="GCSLC Sovereign Gateway", layout="wide")

# METALLIC GOLD & NAVY BLUE PALETTE WITH UNIVERSAL SHIMMER
st.markdown("""
    <style>
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    .main {
        background: linear-gradient(90deg, #001f3f 25%, #002d5b 50%, #001f3f 75%);
        background-size: 1000px 100%;
        animation: shimmer 10s infinite linear;
        color: #FFD700;
        font-family: 'Inter', sans-serif;
    }
    .sovereign-card {
        background: rgba(0, 31, 63, 0.85);
        border: 2px solid #FFD700;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(255, 215, 0, 0.15);
        transition: transform 0.3s ease;
    }
    .sovereign-card:hover {
        transform: scale(1.02);
        border-color: #FFFFFF;
    }
    .metallic-title {
        color: #FFD700;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .data-text {
        color: #FFFFFF;
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# PERSISTENT ANCHOR HEADER
st.markdown('<h1 class="metallic-title">🔱 GCSLC SOVEREIGN GATEWAY</h1>', unsafe_allow_html=True)
st.markdown("### National Resources Revitalization Fusion Center (NRRFC)")
st.info(f"🛡️ **SIGNATURE SECURED:** Chairman Dr. Sa'ad Jaafaru | **CAC:** 176917792057")

st.divider()

# THE 8-CARD NRRFC REGISTRY (The 8R Stealth Paradigm)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""<div class="sovereign-card"><h4 class="metallic-title">D1: REFINE</h4>
    <p class="data-text">Status: <b>ACTIVE</b><br>Asset: Subsoil Density Logic</p></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="sovereign-card"><h4 class="metallic-title">D5: RESUSCITATE</h4>
    <p class="data-text">Status: <b>PENDING</b><br>Target: 1,200 MW Power Strike</p></div>""", unsafe_allow_html=True)

with col2:
    st.markdown("""<div class="sovereign-card"><h4 class="metallic-title">D2: RESET</h4>
    <p class="data-text">Status: <b>LOADED</b><br>Reserve: 639.3M MT Coal</p></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="sovereign-card"><h4 class="metallic-title">D6: REVITALIZE</h4>
    <p class="data-text">Status: <b>RECOVERING</b><br>Strike: 12% WL Cassava</p></div>""", unsafe_allow_html=True)

with col3:
    st.markdown("""<div class="sovereign-card"><h4 class="metallic-title">D3: RESEARCH</h4>
    <p class="data-text">Status: <b>MAPPING</b><br>Scope: 13 Coal-Potential States</p></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="sovereign-card"><h4 class="metallic-title">D7: RE-ENGINEER</h4>
    <p class="data-text">Status: <b>MODELING</b><br>Goal: $100B AI Compute Gap</p></div>""", unsafe_allow_html=True)

with col4:
    st.markdown("""<div class="sovereign-card"><h4 class="metallic-title">D4: RESTRUCTURE</h4>
    <p class="data-text">Status: <b>LEGAL LOCK</b><br>Entity: NGECC-SSMV</p></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="sovereign-card"><h4 class="metallic-title">D8: RETAIN</h4>
    <p class="data-text">Status: <b>TALON LOCK</b><br>Retention: 85% Registry</p></div>""", unsafe_allow_html=True)

st.divider()
st.success("By the Minute Diagnostic: Identifying the Global $700B Capex Opportunity...")
