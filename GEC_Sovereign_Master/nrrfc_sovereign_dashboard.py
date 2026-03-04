import streamlit as st
import pandas as pd

# SOVEREIGN CONFIGURATION
st.set_page_config(page_title="GCSLC Sovereign Gateway", layout="wide")

# NAVY BLUE BASE / WHITE SHIMMER / GOLD ACCENTS
st.markdown("""
    <style>
    @keyframes shimmer-white {
        0% { color: #FFFFFF; text-shadow: 0 0 5px #FFFFFF; }
        50% { color: #FFD700; text-shadow: 0 0 20px #FFD700; }
        100% { color: #FFFFFF; text-shadow: 0 0 5px #FFFFFF; }
    }
    .main {
        background-color: #000814; /* Ultra Deep Navy */
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
    }
    .header-container {
        text-align: center;
        padding: 40px;
        border-bottom: 2px solid #FFD700;
        background: radial-gradient(circle, #001d3d 0%, #000814 100%);
    }
    .medallion {
        width: 150px;
        border-radius: 50%;
        border: 4px solid #FFD700;
        box-shadow: 0 0 30px #FFD700;
        margin-bottom: 20px;
    }
    .shimmer-text {
        animation: shimmer-white 3s infinite;
        font-weight: 800;
        text-transform: uppercase;
    }
    .eightr-card {
        background: rgba(0, 29, 61, 0.7);
        border-left: 5px solid #FFD700;
        padding: 20px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .eightr-visible {
        color: #FFD700;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# HEADER SECTION: MEDALLION & TITLE
st.markdown("""
    <div class="header-container">
        <h1 class="shimmer-text">Galadiman Ruwa Center for Strategic Leadership and Communication</h1>
        <h2 style="color: #FFD700;">GCSLC LTD/GTE</h2>
        <p style="font-style: italic; color: #a3a3a3;">Proponent of the 8R Stealth Paradigm Convergence and its Determinants</p>
    </div>
    """, unsafe_allow_html=True)

st.success("⚡ HIGH-VELOCITY SOVEREIGN WELCOME INITIALIZED. EAGLE IS ON THE NEST.")

# THE 8R STEALTH MATRIX (HIGH VISIBILITY)
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
            <div class="eightr-card">
                <div class="eightr-visible">{d_code}: {d_name}</div>
                <p style="color: white;">{d_desc}</p>
            </div>
            """, unsafe_allow_html=True)

# THE NIGERIAN MAP FEEDSTOCK HUB
st.divider()
st.write("### 🦅 GEC NESTING: COAL-TO-COMPUTE FEEDSTOCK MAP")
st.info("The Eagle is hovering over 13 key nests. Identifying high-yield opportunities in Germanium, Ammonia, and Silicon.")

# PROPRIETARY MARKET DATA
data = {
    "Derivative": ["Germanium (Fly Ash)", "Ammonia", "Silicon", "Syngas"],
    "Market Price": ["$8,597 / kg", "$430 / MT", "$6.50 / M", "$15.20 / M"],
    "Sovereign Yield": ["9.6x", "High", "Strategic", "Sovereign Feedstock"]
}
st.table(pd.DataFrame(data))
