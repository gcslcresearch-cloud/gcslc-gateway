import streamlit as st
import pandas as pd

# 1. SOVEREIGN CONFIGURATION & LAYOUT
st.set_page_config(page_title="GCSLC Sovereign Gateway", layout="wide", initial_sidebar_state="collapsed")

# 2. THE NAVY-GOLD-SHIMMER ARCHITECTURE (CSS INJECTION)
st.markdown("""
    <style>
    @keyframes shimmer-gold {
        0% { border-color: #FFD700; box-shadow: 0 0 5px #FFD700; }
        50% { border-color: #FFFFFF; box-shadow: 0 0 20px #FFFFFF; }
        100% { border-color: #FFD700; box-shadow: 0 0 5px #FFD700; }
    }
    .stApp {
        background-color: #000814; /* Deep Navy Void */
        color: #FFFFFF;
    }
    .header-box {
        background: linear-gradient(180deg, #001d3d 0%, #000814 100%);
        padding: 30px;
        border-bottom: 2px solid #FFD700;
        text-align: center;
    }
    .medallion {
        border: 3px solid #FFD700;
        border-radius: 50%;
        width: 120px;
        height: 120px;
        margin: 0 auto 15px;
        animation: shimmer-gold 4s infinite;
    }
    .determinant-card {
        background: rgba(0, 29, 61, 0.8);
        border: 1px solid #FFD700;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        transition: 0.3s;
    }
    .determinant-card:hover {
        background: rgba(0, 53, 102, 1);
        transform: translateY(-5px);
    }
    .eagle-box {
        background: linear-gradient(135deg, #001d3d 0%, #000814 50%, rgba(255, 215, 0, 0.08) 100%);
        border: 2px solid #FFD700;
        border-radius: 12px;
        padding: 24px;
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.15);
    }
    </style>
    """, unsafe_allow_html=True)

# HEADER
st.markdown("""
    <div class="header-box">
        <div class="medallion"></div>
        <h1 style="color: #FFD700; font-weight: 800; text-transform: uppercase;">Galadiman Ruwa Center for Strategic Leadership and Communication</h1>
        <h2 style="color: #FFFFFF;">GCSLC LTD/GTE</h2>
        <p style="font-style: italic; color: #a3a3a3;">Proponent of the 8R Stealth Paradigm Convergence and its Determinants</p>
    </div>
    """, unsafe_allow_html=True)

st.success("⚡ HIGH-VELOCITY SOVEREIGN WELCOME INITIALIZED. EAGLE IS ON THE NEST.")

# 8R STEALTH MATRIX (determinant cards)
st.write("### 🛡️ 8R STEALTH PARADIGM NODAL")
cols = st.columns(4)
determinants = [
    ("D1", "REFINE", "Subsoil Density"), ("D2", "RESET", "639.3M MT Coal"),
    ("D3", "RESEARCH", "13-State Mapping"), ("D4", "RESTRUCTURE", "NGECC-SSMV"),
    ("D5", "RESUSCITATE", "1,200 MW Power"), ("D6", "REVITALIZE", "12% WL Cassava"),
    ("D7", "RE-ENGINEER", "$100B AI Gap"), ("D8", "RETAIN", "85% Talon Lock")
]

for i, (d_code, d_name, d_desc) in enumerate(determinants):
    with cols[i % 4]:
        st.markdown(f"""
            <div class="determinant-card">
                <div style="color: #FFD700; font-size: 1.25rem; font-weight: bold;">{d_code}: {d_name}</div>
                <p style="color: #FFFFFF; margin: 8px 0 0 0;">{d_desc}</p>
            </div>
            """, unsafe_allow_html=True)

# EAGLE BOX (GEC Nesting)
st.divider()
st.markdown('<div class="eagle-box"><h3 style="color: #FFD700;">🦅 GEC NESTING: COAL-TO-COMPUTE FEEDSTOCK MAP</h3><p style="color: #e0e0e0;">The Eagle is hovering over 13 key nests. Identifying high-yield opportunities in Germanium, Ammonia, and Silicon.</p></div>', unsafe_allow_html=True)

# PROPRIETARY MARKET DATA
data = {
    "Derivative": ["Germanium (Fly Ash)", "Ammonia", "Silicon", "Syngas"],
    "Market Price": ["$8,597 / kg", "$430 / MT", "$6.50 / M", "$15.20 / M"],
    "Sovereign Yield": ["9.6x", "High", "Strategic", "Sovereign Feedstock"]
}
st.table(pd.DataFrame(data))
