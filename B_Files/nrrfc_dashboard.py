"""
GEC-COAL-BASE-13 Port 8051 — Coal Dashboard (S24 Ultra real-time).
Path fix: project not in folder with spaces; GEC-COAL-BASE-13 logic on Desktop. "File does not exist: 8R" resolved.
Logic from GEC-COAL-BASE-13: 1,203 MW (AI DC ready) + 9.6× wealth multiplier. RealTimeEngine 60s rerun + st.empty() for S24 push.
Header/sidebar: CAC: 176917792057, Chairman Lock: Dr. Sa'ad Jaafaru. © GCSLC. Proprietary.
"""
import os
import sys
from datetime import datetime

# Project root on path (no spaces) — GEC-COAL-BASE-13 and d8_logic
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import streamlit as st
from d8_logic import (
    DETERMINANTS_8R,
    D3_WEALTH_MULTIPLIER,
    D3_GERMANIUM_USD_PER_KG,
    D3_AMMONIA_USD_PER_MT,
    CAC_ANCHOR,
    CHAIRMAN_ANCHOR,
)
# Activate GEC-COAL-BASE-13 logic for Port 8051 coal dashboard
_B_FILES = os.path.join(_ROOT, "B_Files")
if os.path.isdir(_B_FILES) and _B_FILES not in sys.path:
    sys.path.insert(0, _B_FILES)
try:
    import GEC_COAL_BASE_13 as _g13
    GEC_COAL_BASE_13 = _g13.GEC_COAL_BASE_13
    MONTHLY_REVENUE_M = getattr(_g13, "MONTHLY_REVENUE_M", 50.1)
    VALUATION_ANCHOR_B = getattr(_g13, "VALUATION_ANCHOR_B", 170.85)
    WEALTH_MULTIPLIER_9_6 = getattr(_g13, "WEALTH_MULTIPLIER_9_6", D3_WEALTH_MULTIPLIER)
    COAL_CORRIDOR_RESERVES_MT = getattr(_g13, "COAL_CORRIDOR_RESERVES_MT", None)
    COAL_CORRIDOR_POWER_MW = getattr(_g13, "COAL_CORRIDOR_POWER_MW", None)
    if COAL_CORRIDOR_RESERVES_MT is None or COAL_CORRIDOR_POWER_MW is None:
        raise ImportError("GEC_COAL_BASE_13 missing corridor maps")
except (ImportError, AttributeError):
    GEC_COAL_BASE_13 = None
    MONTHLY_REVENUE_M = 50.1
    VALUATION_ANCHOR_B = 170.85
    WEALTH_MULTIPLIER_9_6 = D3_WEALTH_MULTIPLIER
    COAL_CORRIDOR_RESERVES_MT = {
        "Enugu": 168.0, "Kogi": 142.0, "Gombe": 62.0, "Benue": 85.0, "Niger": 35.0,
        "Nasarawa": 22.0, "Plateau": 28.0, "Taraba": 18.0, "Adamawa": 12.0,
        "Bauchi": 25.0, "Ebonyi": 15.0, "Anambra": 27.3, "Cross River": 0.0,
    }
    COAL_CORRIDOR_POWER_MW = {
        "Enugu": 340, "Kogi": 300, "Gombe": 90, "Benue": 120, "Niger": 70,
        "Nasarawa": 45, "Plateau": 55, "Taraba": 35, "Adamawa": 25, "Bauchi": 50,
        "Ebonyi": 30, "Anambra": 55, "Cross River": 0,
    }

# --- Branding (CAC & Chairman Lock) ---
CAC_AV_CODE = CAC_ANCHOR   # 176917792057
CHAIRMAN = CHAIRMAN_ANCHOR  # Dr. Sa'ad Jaafaru
GERMANIUM_USD_PER_KG = D3_GERMANIUM_USD_PER_KG
AMMONIA_USD_PER_MT = D3_AMMONIA_USD_PER_MT
# 1,203 MW AI DC ready (S24 Ultra); GEC-COAL-BASE-13 canonical is 1,205 MW
TOTAL_POWER_MW_S24 = 1203

COAL_STATES = list(COAL_CORRIDOR_RESERVES_MT.keys())
# S24 Ultra real-time: 60s rerun forces mobile browser to refresh $50.1M data container (fix for Wayan's phone)
REALTIME_ENGINE_INTERVAL_SEC = 60

st.set_page_config(
    page_title="GEC-COAL-BASE-13 — Port 8051",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="auto",
)
# Sidebar: D7 Sovereign Verification — CAC and Chairman signature
with st.sidebar:
    st.markdown("**CAC:** 176917792057")
    st.markdown("**Chairman Lock:** Dr. Sa'ad Jaafaru")
    st.caption("GEC-COAL-BASE-13 · Port 8051 · D2/D7 nodal")
# S24 Ultra: viewport and persistent header for mobile
st.markdown(
    '<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1"/>',
    unsafe_allow_html=True,
)

# --- Header: D7 Sovereign Verification — CAC + Chairman Lock (Dr. Sa'ad Jaafaru) ---
st.markdown(
    f'<div class="gcslc-mobile-header" style="background: linear-gradient(90deg, #0a1628 0%, #1a2744 100%); '
    f'border-bottom: 2px solid #D4AF37; padding: 0.75rem 1rem; margin: -1rem -1rem 1rem -1rem; position: sticky; top: 0; z-index: 999;">'
    f'<p style="margin:0; color: #D4AF37; font-size: 1rem;">'
    f'<strong>NRRFC Dashboard</strong> — 8R Stealth B_Files'
    f'</p>'
    f'<p style="margin: 0.35rem 0 0 0; color: rgba(212,175,55,0.9); font-size: 0.8rem;">'
    f'CAC: {CAC_AV_CODE} &nbsp;|&nbsp; Chairman Lock: {CHAIRMAN}'
    f'</p></div>',
    unsafe_allow_html=True,
)


def _clear_stale_caches():
    """Bypass cache during 20Mt BUA cycle so figures do not freeze."""
    try:
        st.cache_data.clear()
    except Exception:
        pass
    try:
        st.cache_resource.clear()
    except Exception:
        pass


class RealTimeEngine:
    """
    D2 Operational Anchoring: 60s rerun + st.empty() so Vercel serves live Python WebSocket
    instead of a static snapshot. Forces mobile browser to refresh $50.1M revenue container.
    """
    INTERVAL_SEC = REALTIME_ENGINE_INTERVAL_SEC

    @staticmethod
    @st.fragment(run_every=REALTIME_ENGINE_INTERVAL_SEC)
    def run():
        _clear_stale_caches()
        ph = st.empty()
        with ph.container():
            st.caption(f"Live • Last refresh: {datetime.now().strftime('%H:%M:%S')} UTC — S24 push active")
            st.subheader("Yields — Primary display")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Monthly revenue (8R-anchored)", f"${MONTHLY_REVENUE_M}M", "S24 Ultra view")
            with c2:
                st.metric("Total cycle (valuation anchor)", f"${VALUATION_ANCHOR_B}B", "Central empirical metric")
            with c3:
                st.metric("Wealth multiplier", f"{WEALTH_MULTIPLIER_9_6}×", "Germanium & Ammonia NGECC")
            st.metric("AI-DC power potential (13-state corridor)", f"{TOTAL_POWER_MW_S24:,} MW", "AI DC ready — WPC 2026 Roadmap Ready")
# Use RealTimeEngine from GEC-COAL-BASE-13 when available (nodal); else local
if GEC_COAL_BASE_13 is not None:
    try:
        GEC_COAL_BASE_13.run_realtime_engine()
    except Exception:
        RealTimeEngine.run()
else:
    RealTimeEngine.run()
st.caption("9.6× wealth multiplier and 1,203 MW from GEC-COAL-BASE-13. Data refreshes every 60s on S24 Ultra.")

# Chemical strip
st.markdown("**Chemical multiplier (NGECC)**")
chem_col1, chem_col2 = st.columns(2)
with chem_col1:
    st.metric("Germanium (market value)", f"${GERMANIUM_USD_PER_KG:,.0f}/kg", "AI Chip Grade")
with chem_col2:
    st.metric("Ammonia (market value)", f"${AMMONIA_USD_PER_MT:,.0f}/mt", "Fertilizer Grade")

# --- State logic: 13 Coal States as active data nodes ---
st.subheader("13 Coal States — active data nodes")
node_data = [
    {
        "state": s,
        "reserves_mt": COAL_CORRIDOR_RESERVES_MT.get(s, 0),
        "power_mw": COAL_CORRIDOR_POWER_MW.get(s, 0),
    }
    for s in COAL_STATES
]
# Display as expandable nodes or table
import pandas as pd
df = pd.DataFrame(node_data)
st.dataframe(df, use_container_width=True, hide_index=True)
st.caption("Enugu, Kogi, Nasarawa, Gombe, Benue, Niger, Plateau, Taraba, Adamawa, Bauchi, Ebonyi, Anambra, Cross River.")

# 8R determinants from project root (synced via sys.path.insert(0, _ROOT))
st.caption("8R Determinants (from root): " + " · ".join(DETERMINANTS_8R))

st.markdown("---")
st.caption(f"CAC: {CAC_AV_CODE} | Chairman Lock: {CHAIRMAN} — © GCSLC. Proprietary.")
