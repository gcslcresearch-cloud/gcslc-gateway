import streamlit as st
import pandas as pd

# 1. SOVEREIGN UI CONFIG — PURGING ALL ERRORS & WHITE BOXES
st.set_page_config(layout="wide", page_title="GCSLC Sovereign Gateway")

st.markdown("""
<style>
    .stApp { background-color: #00040a !important; color: #D4AF37 !important; }
    [data-testid="stSidebar"] { background-color: #000814 !important; border-left: 1px solid #D4AF37; }
    .metric-box { border: 1px solid #D4AF37; padding: 20px; background: rgba(0, 8, 20, 0.8); text-align: center; border-radius: 5px; }
    h1, h2 { color: #D4AF37 !important; text-transform: uppercase; text-align: center; }
</style>
""", unsafe_allow_html=True)

# 2. PRIMARY BRANDING — GALADIMAN RUWA CENTER AS MAIN HEADER
st.markdown("# GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION")
st.markdown("### NRRFC VALUE-ADDED DERIVATIVE STRIKE")

# 3. THE 9.6x MULTIPLIER (Replica of Image 2)
c1, c2, c3, c4 = st.columns([1, 1, 1, 0.5])
with c1:
    st.markdown("<div class='metric-box'>RAW COAL VALUE<br><b>$1.1 M</b><br>₦1.49 B</div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='metric-box'>DERIVATIVE UPSIDE<br><b>$9.5 M</b><br>₦12.77 B</div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='metric-box'>TOTAL EQUITY<br><b>$10.6 M</b><br>₦14.25 B</div>", unsafe_allow_html=True)
with c4:
    st.markdown("<div class='metric-box' style='border: 2px solid #FFD700;'>MULTIPLIER<br><b style='font-size:24px;'>9.6x</b></div>", unsafe_allow_html=True)

# 4. MOBILE GAUGES — CORRECT SPELLING (Sovereign, Government, Produced)
st.markdown("---")
g1, g2, g3 = st.columns(3)
with g1:
    st.markdown("<div class='metric-box'><span style='color:#D4AF37;'>Sovereign</span><br><small>Feedstock lock</small></div>", unsafe_allow_html=True)
with g2:
    st.markdown("<div class='metric-box'><span style='color:#D4AF37;'>Government</span><br><small>Debt-swap anchor</small></div>", unsafe_allow_html=True)
with g3:
    st.markdown("<div class='metric-box'><span style='color:#D4AF37;'>Produced</span><br><small>Revenue yield</small></div>", unsafe_allow_html=True)


def show_subsoil_map():
    """Render 13-state subsoil nodal mapping table. Defined before any call to avoid NameError."""
    data = {
        "State": ["Enugu", "Kogi", "Gombe", "Benue", "Delta", "Nasarawa", "Anambra", "Plateau", "Adamawa", "Edo"],
        "Reserves (MT)": [150.0, 120.0, 80.0, 70.0, 55.0, 45.0, 35.0, 25.0, 20.0, 15.0],
    }
    st.table(pd.DataFrame(data))


# 5. SUBSOIL NODAL MAPPING (calls defined function)
st.markdown("---")
show_subsoil_map()

# 6. RIGHT SIDEBAR GLOSSARY
with st.sidebar:
    st.markdown("### TECHNICAL GLOSSARY")
    st.markdown("<p style='color:#b5a48b;'>LLMS: AI for yield prediction.</p>", unsafe_allow_html=True)
    st.markdown("<p style='color:#b5a48b;'>KPIs: Revenue ($50.1M strike).</p>", unsafe_allow_html=True)

# 7. SOVEREIGN ACTIVATION — AT BOTTOM (Initiate Reset bar moved from top)
st.markdown("---")
if st.button("INITIATE RESET — SOVEREIGN ACTIVATION"):
    st.success("D1: RESET PHASE ACTIVE. SYSTEM ONLINE.")
