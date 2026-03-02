"""
8R Strike Command — Port 8053
Synchronized $1.5 Trillion Initiative & Institutional Partner data (Dangote, BUA, Zenith, GTCO).
Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026 GCSLC.
"""
import os
import sys
import importlib.util
import warnings
import streamlit as st

warnings.filterwarnings("ignore", category=DeprecationWarning, module="streamlit")
warnings.filterwarnings("ignore", message=".*use_container_width.*")

# Load African_Gateway continental_logic (same pattern as awc_portal_8054)
_BASE = os.path.dirname(os.path.abspath(__file__))
_GATEWAY = os.path.join(_BASE, "African_Gateway.")

def _load_module(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

continental_logic = _load_module("awc_continental_logic", os.path.join(_GATEWAY, "continental_logic.py"))

st.set_page_config(
    page_title="8R Strike Command — Port 8053 — GCSLC",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sovereign aesthetic — Navy & Gold
st.markdown("""
<style>
.stApp { background-color: #002147 !important; min-height: 100vh; }
[data-testid="stAppViewContainer"] { background-color: #002147 !important; }
.main .block-container { background-color: #002147 !important; max-width: 100%; padding: 1rem 2rem; }
h1, h2, h3, p, span, label, .stMarkdown { color: #D4AF37 !important; }
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color: #D4AF37 !important; }
section[data-testid="stSidebar"] { background-color: #002147 !important; border-right: 2px solid #D4AF37; }
.strike-header { font-weight: 800; font-size: 1.5rem; text-align: center; color: #FFD700 !important; margin-bottom: 0.5rem; }
.strike-sub { text-align: center; color: rgba(212,175,55,0.95); font-size: 0.95rem; }
</style>
""", unsafe_allow_html=True)

# ——— Chairman Lock (Port 8053) ———
st.markdown(
    '<div style="position: sticky; top: 0; z-index: 100; background: linear-gradient(180deg, #002147 0%, rgba(0,33,71,0.98) 100%); padding-bottom: 10px; margin-bottom: 12px; border-bottom: 1px solid rgba(212,175,55,0.25);">'
    '<p style="text-align: center; font-weight: 800; color: #D4AF37; font-size: 0.95rem; margin: 0;">Galadiman Ruwa Center (GCSLC) LTD/GTE | Chairman & Founder: Dr. Sa\'ad Jaafaru</p>'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown('<p class="strike-header">8R Strike Command — Synchronized</p>', unsafe_allow_html=True)
st.markdown('<p class="strike-sub">Port 8053 | $1.5 Trillion Initiative & Institutional Partners</p>', unsafe_allow_html=True)
st.markdown("---")

# ——— $1.5 Trillion Initiative (Capital node — fully loaded) ———
capital = continental_logic.get_capital_node()
st.write("### 💰 $1.5 Trillion Initiative — Capital Node")
st.metric("Initiative", capital["initiative_name"], help="JPMorgan / Citibank — Security & Resiliency")
st.metric("Scale", f"$ {capital['initiative_value_usd_trillion']} Trillion", help="Fully loaded")
st.markdown(f"**Alignment:** {capital['alignment_narrative']}")
st.caption("D8 Retain anchors capital in-country; Eagle validates bank node as Secured Asset.")
st.markdown("---")

# ——— Institutional Partners (Dangote, BUA, Zenith, GTCO) ———
partners = continental_logic.get_institutional_partners()
st.write("### 🏛️ Institutional Partners — Fully Loaded")
for p in partners:
    with st.expander(f"**{p['name']}** — {p['sector']}", expanded=(p['name'] in ("Dangote", "BUA"))):
        st.markdown("**Assets bid on:** " + "; ".join(f"*{a}*" for a in p["assets_bid"]))
        st.markdown("**8R Resuscitation:** " + p["8r_resuscitation"])
st.caption("Dangote, BUA, Zenith Bank, GTCO — sovereign value chains under 8R Strike Command.")
st.markdown("---")

# ——— 8R Determinants quick ref ———
st.write("### 8R Determinants (D1–D8)")
cols = st.columns(4)
for i, det in enumerate(continental_logic.DETERMINANTS_8R):
    cols[i % 4].success(det)
st.markdown("---")
st.caption("Strategic Infrastructure: Galadiman Ruwa Center (GCSLC) LTD/GTE | © 2026 | Port 8053 — 8R Strike Command.")
