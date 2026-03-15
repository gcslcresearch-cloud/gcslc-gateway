"""
National Wealth Cloud for Nigeria: Coal & Diamond (NWC/C&D)
Sovereign Gateway — 8R Stealth Paradigm | Galadiman Ruwa Center For Strategic Leadership and Communication LTD/GTE — GCSLC
Senior Sovereign Architect: Command Deck deployment.
- Core: ZoneInfo fallback (Python < 3.9); Screenshot-Shield for Sovereign Valuation.
- Mirror: Deep Navy (#000080) + Metallic Gold (#D4AF37); corporate Energy & Chemicals facade; Glass-Shatter on GCSLC handshake.
- 8R Stealth: Plotly dashboard (95/5 Talon Lock, 9.6× multiplier, Abuja-Zaria-Kano Corridor). On error, core logic gates prioritized.
- Performance: S24 Ultra responsive; viewport-fit. Duniya a ido take.
"""
import base64
import os
import warnings
from collections import defaultdict
import streamlit as st
import streamlit.components.v1 as components

warnings.filterwarnings("ignore", category=DeprecationWarning, module="streamlit")
warnings.filterwarnings("ignore", message=".*use_container_width.*")
import pandas as pd

from datetime import datetime, timezone, timedelta
# ZoneInfo fallback: ensuring compatibility for Python < 3.9 (Sovereign Architect mandate)
try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None  # Python < 3.9 — use UTC-offset fallback in _now_tz()

from d8_logic import (
    WEALTH_RETENTION_LOCK,
    STRATEGIC_FOUNDATION,
    apply_talon_lock,
    apply_95_5_talon_lock,
    TALON_LOCK_NATIONAL_PCT,
    TALON_LOCK_GLOBAL_POOL_PCT,
    D3_WEALTH_MULTIPLIER,
    D3_GERMANIUM_USD_PER_KG,
    D3_AMMONIA_USD_PER_MT,
    D3_SILICON_MONTHLY_YIELD_M,
    D3_COAL_SYNGAS_MONTHLY_REVENUE_M,
    GEC_COAL_RESERVES_M_MT,
    POWER_POTENTIAL_GW,
    ABUJA_ZARIA_KANO_CORRIDOR,
)
from mineral_sovereignty import (
    get_nodes,
    retained_yield,
    global_market_impact_index,
    get_diamond_reserves,
)
from spc_generator import generate_spc_image
from handshake import run_diagnostic_pulse, play_talon_lock_confirmed, play_eagle_cry, get_swat_beep_path, STATES
from nwc_geopolitical import STATE_REGION, STATE_LGA_COUNT, get_lgas

FULL_NAME = "Galadiman Ruwa Center For Strategic Leadership and Communication LTD/GTE"
BRAND = "GCSLC"
SEAL_PATH = os.path.join(os.path.dirname(__file__), "assets", "gcslc_seal.png")
DETERMINANTS = ["Refine", "Reset", "Research", "Restructure", "Resuscitate", "Revitalize", "Re-engineer", "Retain"]
NWC_HEADER = "National Wealth Cloud for Nigeria: Coal & Diamond (NWC/C&D)"
NWC_SUBTITLE = "Cloud-Level Pragmatic Reality — Powered by GCSLC Sovereign Gateway"
VALUATION_ANCHOR_B = 170.85  # Central empirical metric — 95/5 Talon Lock flare

# Sovereign Retention Protocol (D8 Logic) — 95% National Equity (Talon Lock)
SOVEREIGN_RETENTION_PROTOCOL = f"""
**The Sovereign Retention Protocol (D8 Logic)**  
This partnership is governed by a **fixed {int(WEALTH_RETENTION_LOCK * 100)}% Value Anchor** (Talon Lock). By deploying the 8R Stealth Paradigm, GCSLC mandates that **{int(WEALTH_RETENTION_LOCK * 100)}% of all economic velocity and intellectual derivative value** remains proprietary to the Sovereign Node. This foundation is engineered at **1m × 1m Steel** structural depth, ensuring that global expansion (Alphabet/Apple) serves to **strengthen the national core** rather than deplete it.
"""

# D7: set_page_config must be the very first Streamlit command (no st.* before this)
st.set_page_config(
    page_title="NWC/C&D — GCSLC Sovereign Gateway",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Session state init (after set_page_config)
if "strike" not in st.session_state:
    st.session_state.strike = False
if "strike_manifested" not in st.session_state:
    st.session_state.strike_manifested = False
if "certificate_shown" not in st.session_state:
    st.session_state.certificate_shown = False
if "handshake_done" not in st.session_state:
    st.session_state.handshake_done = False
if "state_nodes" not in st.session_state:
    st.session_state.state_nodes = []
if "selected_state" not in st.session_state:
    st.session_state.selected_state = None
if "nwc_authenticated" not in st.session_state:
    st.session_state.nwc_authenticated = False
# Mirror Interface: corporate facade until GCSLC logo handshake
if "handshake_unlocked" not in st.session_state:
    st.session_state.handshake_unlocked = False
if "handshake_shatter_pending" not in st.session_state:
    st.session_state.handshake_shatter_pending = False

# NWC/C&D diagnostic pulse once at startup: initialize 37 nodes, then run pulse
if not st.session_state.handshake_done:
    st.session_state.state_nodes = list(STATES)
    run_diagnostic_pulse()
    st.session_state.handshake_done = True

# NWC/C&D Sovereign Aesthetic — Goldman font, Prism-Text, diagonal watermark | GCSLC Institutional Finalization
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap" rel="stylesheet">
<style>
/* Viewport: GCSLC Sovereign Diagnostic | Persistent 15% opacity shimmering watermark (Security Layer) */
.stApp { background-color: #000080 !important; min-height: 100vh; position: relative; }
.stApp::before {
    content: "GCSLC PROPRIETARY";
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(-35deg);
    font-family: 'Goldman', sans-serif;
    font-size: clamp(3rem, 8vw, 6rem);
    font-weight: 700;
    color: rgba(212, 175, 55, 0.15);
    white-space: nowrap;
    letter-spacing: 0.2em;
    pointer-events: none;
    z-index: 0;
    animation: watermark-pulse 3s ease-in-out infinite;
}
@keyframes watermark-pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}
/* Screenshot Shield: Flash overlay — PROPRIETARY stamp on print / copy attempt */
@media print {
    body * { visibility: hidden !important; }
    body::after {
        content: "PROPRIETARY — GCSLC"; visibility: visible !important; position: fixed; top: 50%; left: 50%; transform: translate(-50%,-50%); font-size: 3rem; color: #D4AF37;
    }
}
/* Prism Ticker frame */
.prism-ticker-wrap {
    border: 2px solid rgba(212,175,55,0.6);
    border-radius: 8px;
    padding: 0.5rem 0.75rem;
    margin: 0.75rem 0;
    background: linear-gradient(135deg, rgba(0,0,128,0.95), rgba(0,0,160,0.9));
    overflow: hidden;
    animation: prism-border 2s linear infinite;
}
@keyframes prism-border {
    0%, 100% { box-shadow: 0 0 12px rgba(212,175,55,0.4); }
    50% { box-shadow: 0 0 24px rgba(255,229,92,0.6); }
}
.prism-ticker {
    display: flex;
    flex-wrap: nowrap;
    gap: 1.5rem;
    font-family: 'Goldman', sans-serif;
    font-size: 0.9rem;
    color: #D4AF37;
    animation: ticker-scroll 30s linear infinite;
}
.prism-ticker span { white-space: nowrap; }
@keyframes ticker-scroll {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
/* Abuja-Zaria-Kano Corridor — Energy-Industrial Spine */
.azk-corridor {
    background: linear-gradient(135deg, rgba(212,175,55,0.15), rgba(0,0,128,0.95));
    border: 2px solid #D4AF37;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin: 0.75rem 0;
    text-align: center;
    font-family: 'Goldman', sans-serif;
}
.azk-corridor .azk-title { font-size: 1.1rem; font-weight: 700; color: #FFE55C; margin-bottom: 0.25rem; }
.azk-corridor .azk-desc { color: #E8C547; font-size: 0.95rem; }
/* Global Clocks — 4 shimmering nodes */
.global-clocks {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    justify-content: center;
    margin: 0.75rem 0;
}
.clock-node {
    background: linear-gradient(135deg, rgba(0,0,128,0.98), rgba(0,0,160,0.95));
    border: 1px solid #D4AF37;
    border-radius: 8px;
    padding: 0.5rem 0.75rem;
    min-width: 120px;
    text-align: center;
    animation: d8-breathing 2.5s ease-in-out infinite;
}
.clock-node .clock-label { font-size: 0.75rem; color: #E8C547; text-transform: uppercase; letter-spacing: 0.1em; }
.clock-node .clock-time { font-family: 'Goldman', sans-serif; font-weight: 700; color: #FFE55C; font-size: 1rem; }
[data-testid="stAppViewContainer"] { background-color: #000080 !important; position: relative; z-index: 1; }
.main .block-container { background-color: #000080 !important; max-width: 100%; padding: 1rem 2rem; position: relative; z-index: 1; }
/* Primary headings: Goldman font + Shimmering Prism-Text (gold-to-white high-velocity gradient) */
h1, h2, h3 { font-family: 'Goldman', sans-serif !important; }
.main h3 {
    background: linear-gradient(90deg, #D4AF37, #FFFFFF, #FFE55C, #FFFFFF, #D4AF37);
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
    animation: prism-shimmer 2.5s linear infinite;
}
.prism-text {
    font-family: 'Goldman', sans-serif !important;
    background: linear-gradient(90deg, #D4AF37, #FFFFFF, #FFE55C, #FFFFFF, #D4AF37);
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
    animation: prism-shimmer 2s linear infinite;
}
@keyframes prism-shimmer {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}
h1, h2, h3, p, span, label, .stMarkdown { color: #D4AF37 !important; }
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color: #D4AF37 !important; }
section[data-testid="stSidebar"] { background-color: #000080 !important; border-right: 2px solid #D4AF37; }
/* Clickable state node buttons + 774 LGA grid consistency */
.nwc-state-btn { background: linear-gradient(135deg, #000080, #0000a0); border: 1px solid #D4AF37; color: #D4AF37; border-radius: 6px; padding: 0.35rem 0.6rem; margin: 0.2rem; font-size: 0.85rem; }
.nwc-state-btn:hover { background: rgba(212,175,55,0.2); }
.glossary-term { font-weight: 700; color: #E8C547; }
.glossary-def { color: #D4AF37; font-size: 0.9rem; margin-bottom: 0.75rem; }
/* 774 LGA grid: Navy Blue & Metallic Gold theme */
.nwc-lga-grid, .nwc-lga-grid .stMarkdown, .nwc-lga-grid ul { background-color: #000080 !important; color: #D4AF37 !important; }
.nwc-lga-grid [data-testid="stExpander"] { background: rgba(0,0,128,0.98); border: 1px solid #D4AF37; border-radius: 6px; }
.nwc-lga-grid [data-testid="stExpander"] summary { color: #D4AF37 !important; }
.nwc-lga-grid [data-testid="stExpander"] li { color: #E8C547; }
/* 95/5 Talon Lock data flare on node click */
.talon-lock-flare {
    background: linear-gradient(135deg, rgba(212,175,55,0.25), rgba(0,0,128,0.9));
    border: 2px solid #D4AF37;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    margin-bottom: 0.75rem;
    text-align: center;
    font-weight: 700;
}
.talon-lock-flare .flare-label { color: #E8C547; margin-right: 0.5rem; }
.talon-lock-flare .flare-value { color: #FFE55C; font-size: 1.1rem; }
/* 8R Stealth Engine — D1–D8 golden Breathing animation */
@keyframes d8-breathing {
    0%, 100% { box-shadow: 0 0 12px rgba(212,175,55,0.4); opacity: 0.9; transform: scale(1); }
    50% { box-shadow: 0 0 24px rgba(232,197,71,0.8); opacity: 1; transform: scale(1.02); }
}
.d8-widgets-grid { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.75rem 0; }
.d8-widget-breathing {
    background: linear-gradient(135deg, rgba(0,0,128,0.95), rgba(0,0,160,0.9));
    border: 1px solid #D4AF37;
    border-radius: 8px;
    padding: 0.5rem 0.75rem;
    color: #D4AF37;
    font-weight: 700;
    font-size: 0.9rem;
    animation: d8-breathing 2.5s ease-in-out infinite;
}
.central-valuation { text-align: center; color: #E8C547 !important; margin-bottom: 0.5rem; }
</style>
""", unsafe_allow_html=True)
# Keyframes and .brand-8r kept in background (no leak)
st.markdown("""
<style>
/* Title shimmer: linear-gradient animation — 8R Center primary authority */
.brand-8r {
    font-weight: 800 !important;
    font-size: 1.8rem !important;
    text-align: center;
    background: linear-gradient(90deg, #D4AF37, #FFE55C, #D4AF37, #E8C547, #D4AF37);
    background-size: 300% 100%;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
    animation: title-shimmer 4s linear infinite;
}

@keyframes title-shimmer {
    0% { background-position: 0% 50%; }
    100% { background-position: 300% 50%; }
}

/* D1: REFINE - Sovereign branding animation */
@keyframes gold-shimmer {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
}
.gcslc-header {
    font-family: 'Inter', sans-serif;
    font-weight: 800;
    font-size: 2.2rem;
    text-align: center;
    background: linear-gradient(90deg, #D4AF37, #FFFFFF, #D4AF37, #E8C547, #D4AF37);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gold-shimmer 5s linear infinite;
    margin-bottom: 0px;
}
.proprietor-tag {
    font-family: 'serif';
    font-style: italic;
    text-align: center;
    color: #D4AF37;
    font-size: 1.1rem;
    letter-spacing: 2px;
    margin-top: -10px;
}
/* Master Header — Goldman + Shimmering Prism-Text (gold-to-white high-velocity) */
.nwc-master-header {
    font-family: 'Goldman', sans-serif !important;
    font-weight: 700;
    font-size: 2rem;
    text-align: center;
    background: linear-gradient(90deg, #D4AF37, #FFFFFF, #FFE55C, #FFFFFF, #D4AF37);
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
    animation: prism-shimmer 2s linear infinite;
    margin-bottom: 0.25rem;
}
/* Identity Anchor — dominant top bar: GCSLC name with uniform Goldman Prism-Text shimmer */
.identity-anchor-dominant {
    font-family: 'Goldman', sans-serif !important;
    font-weight: 700;
    font-size: clamp(1.5rem, 4vw, 2.25rem);
    text-align: center;
    margin: 0;
    background: linear-gradient(90deg, #D4AF37, #FFFFFF, #FFE55C, #FFFFFF, #D4AF37);
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
    animation: prism-shimmer 2s linear infinite;
    letter-spacing: 0.02em;
}
.nwc-subtitle-balanced {
    font-family: 'Goldman', sans-serif !important;
    font-weight: 700;
    font-size: clamp(1.1rem, 2.5vw, 1.5rem);
    text-align: center;
    margin: 0.4rem 0 0.2rem 0;
    background: linear-gradient(90deg, #D4AF37, #FFFFFF, #FFE55C, #FFFFFF, #D4AF37);
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
    animation: prism-shimmer 2.5s linear infinite;
    letter-spacing: 0.03em;
    line-height: 1.3;
}
.nwc-authority {
    font-family: 'Goldman', sans-serif !important;
    text-align: center;
    color: #D4AF37;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 1px;
}
.nwc-subheader {
    font-family: 'Goldman', sans-serif !important;
    font-style: italic;
    text-align: center;
    color: #E8C547;
    font-size: 1.05rem;
    letter-spacing: 2px;
    margin-top: -4px;
    margin-bottom: 0.5rem;
}
/* Chairman's Seal — Bottom-right fixed sticky bar, shimmering gold signature */
.chairman-signature-shimmer {
    font-family: 'Goldman', sans-serif !important;
    background: linear-gradient(90deg, #D4AF37, #FFE55C, #FFFFFF, #E8C547, #D4AF37);
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
    animation: prism-shimmer 2.5s linear infinite;
}
.chairman-sticky-bar {
    position: fixed;
    bottom: 0;
    right: 0;
    z-index: 999;
    background: linear-gradient(90deg, rgba(0,0,128,0.97), rgba(0,0,128,0.98));
    border-top: 2px solid rgba(212,175,55,0.5);
    border-left: 2px solid rgba(212,175,55,0.5);
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
    font-weight: 700;
    border-radius: 8px 0 0 0;
    pointer-events: none;
}
.universal-message {
    background: rgba(212, 175, 55, 0.1);
    border-left: 5px solid #D4AF37;
    padding: 20px;
    border-radius: 10px;
    color: #E0E0E0;
    font-style: italic;
    text-align: center;
    margin: 20px 0;
}

/* GCSLC Gold Seal: linear-gradient shimmer (gradient ring + gold glow) */
[data-testid="stLogo"] {
    position: relative;
    border-radius: 50%;
    padding: 3px;
    background: linear-gradient(135deg, #D4AF37, #FFE55C, #E8C547, #D4AF37);
    background-size: 300% 300%;
    animation: seal-gradient-shimmer 3s linear infinite, seal-glow 2.5s ease-in-out infinite;
}
[data-testid="stLogo"] img {
    animation: seal-rotate 60s linear infinite, seal-pulse 2.5s ease-in-out infinite;
    transform-origin: center center;
    border-radius: 50%;
    display: block;
    background: #000080;
}

@keyframes seal-gradient-shimmer {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes seal-glow {
    0%, 100% { box-shadow: 0 0 12px rgba(212,175,55,0.5); }
    50% { box-shadow: 0 0 20px rgba(232,197,71,0.8); }
}

@keyframes seal-rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

@keyframes seal-pulse {
    0%, 100% { opacity: 0.85; }
    50% { opacity: 1; }
}

.spc-cert { border: 3px solid #D4AF37; border-radius: 12px; padding: 2rem; margin: 1.5rem 0; background: rgba(0,0,128,0.95); color: #D4AF37; position: relative; }
.spc-cert .seal-wrap { text-align: center; margin: 1rem 0; }
.spc-cert .cascade-map { margin: 1rem 0; line-height: 1.8; }
.spc-cert .talon-metric { font-size: 1.4rem; font-weight: 700; color: #E8C547; margin: 1rem 0; }
.spc-cert .footer-cert { margin-top: 1.5rem; font-size: 0.85rem; opacity: 0.95; }
.spc-watermark { position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%) rotate(-25deg); font-size: 0.9rem; opacity: 0.12; color: #D4AF37; white-space: nowrap; pointer-events: none; }
</style>
""", unsafe_allow_html=True)

# Screenshot-Shield: Protect sensitive Sovereign Valuation data from unauthorized capture (Senior Sovereign Architect)
components.html("""
<script>
(function(){
  document.addEventListener('copy', function(e) {
    e.clipboardData.setData('text/plain', 'PROPRIETARY — GCSLC Sovereign Gateway. Unauthorized distribution prohibited.');
    e.preventDefault();
  });
  document.addEventListener('cut', function(e) { e.preventDefault(); });
  var flash = document.createElement('div');
  flash.id = 'gcslc-shield-flash';
  flash.style.cssText = 'position:fixed;inset:0;z-index:9999;background:rgba(0,0,128,0.85);display:none;align-items:center;justify-content:center;pointer-events:none;font-family:sans-serif;font-size:2rem;font-weight:800;color:#D4AF37;';
  flash.textContent = 'PROPRIETARY';
  document.body.appendChild(flash);
  document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && (e.key === 'c' || e.key === 'C') || e.metaKey && (e.key === 'c' || e.key === 'C')) {
      flash.style.display = 'flex';
      setTimeout(function(){ flash.style.display = 'none'; }, 400);
    }
  });
  var m = document.createElement('meta');
  m.name = 'viewport';
  m.content = 'width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover';
  if (document.head) document.head.appendChild(m);
})();
</script>
""", height=0)

# ——— Mirror Interface: Corporate facade (Energy & Chemicals) until GCSLC logo handshake ———
if not st.session_state.handshake_unlocked:
    # Landing: standard corporate "Energy & Chemicals" facade
    st.markdown(
        '<div style="text-align:center; padding: 3rem 1rem; color: #D4AF37; font-family: sans-serif;">'
        '<h1 style="color: #D4AF37; margin-bottom: 1rem;">Energy & Chemicals</h1>'
        '<p style="font-size: 1.1rem; opacity: 0.95;">Strategic resources and industrial solutions.</p>'
        '<p style="margin-top: 2rem; font-size: 0.9rem;">Click the GCSLC logo below to enter the Sovereign Gateway.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔷 GCSLC", type="primary", key="gcslc_handshake", use_container_width=True):
            st.session_state.handshake_unlocked = True
            st.session_state.handshake_shatter_pending = True
            st.rerun()
    st.stop()

# Glass-Shatter transition (once) when entering from facade
if st.session_state.handshake_shatter_pending:
    components.html("""
    <div id="gcslc-shatter" style="position:fixed;inset:0;z-index:10000;pointer-events:none;">
      <div style="position:absolute;inset:0;background:linear-gradient(135deg,rgba(0,0,128,0.97),rgba(0,0,128,0.9));animation:gcslc-fade 1.5s ease-out forwards;"></div>
      <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-family:sans-serif;font-size:1.5rem;font-weight:800;color:#D4AF37;opacity:0;animation:gcslc-pop 0.8s 0.3s ease-out forwards;">Sovereign Gateway — 8R Stealth</div>
    </div>
    <style>
    @keyframes gcslc-fade { 0% { opacity: 1; } 70% { opacity: 1; } 100% { opacity: 0; } }
    @keyframes gcslc-pop { 0% { opacity: 0; transform: translate(-50%,-50%) scale(0.8); } 100% { opacity: 1; transform: translate(-50%,-50%) scale(1); } }
    </style>
    """, height=0)
    st.session_state.handshake_shatter_pending = False

# Global Branding: NWC/C&D header + seal
if os.path.isfile(SEAL_PATH):
    st.logo(SEAL_PATH)

# Identity Anchor (Top Bar): Galadiman Ruwa Center (GCSLC) LTD/GTE — dominant heading with uniform Goldman Prism-Text shimmer
st.markdown(
    '<div style="position: sticky; top: 0; z-index: 100; background: linear-gradient(180deg, #000080 0%, rgba(0,0,128,0.98) 100%); padding: 0.75rem 1rem 1rem; margin-bottom: 8px; border-bottom: 1px solid rgba(212,175,55,0.25);">'
    '<p class="identity-anchor-dominant">Galadiman Ruwa Center (GCSLC) LTD/GTE</p>'
    '</div>',
    unsafe_allow_html=True,
)

# Balanced sub-title and sub-header (symmetrical, authoritative)
st.markdown("""
<div class="nwc-subtitle-balanced">
    National Wealth Cloud for Nigeria: Coal & Diamond (NWC/C&D)
</div>
<div class="nwc-subheader">
    Proprietors of 8R Stealth Paradigm Convergence
</div>

<div class="universal-message">
    "The 8R Determinants are universal. Whether applied to national assets or personal growth, 
    they provide the scientific blueprint to Refine, Reset, and Revitalize every facet of human endeavor. 
    Applying 8R to everything we do is the key to scientifically improving our lives."
</div>
""", unsafe_allow_html=True)

# ——— Live Market Pulse: Prism Ticker (Germanium, Silicon, Benzene, Ammonia, Coal, Diamond) ———
# Placeholder live indices (D3 anchors + market-style; cycle via CSS scroll)
_BENZENE_USD_PER_MT = 720.0  # placeholder
_COAL_INDEX = 142.0  # placeholder index
_DIAMOND_INDEX = 98.5  # placeholder index
_ticker_items = (
    f"Germanium ${D3_GERMANIUM_USD_PER_KG:,.0f}/kg",
    f"Silicon ${D3_SILICON_MONTHLY_YIELD_M}M/mo",
    f"Benzene ${_BENZENE_USD_PER_MT:,.0f}/MT",
    f"Ammonia ${D3_AMMONIA_USD_PER_MT:,.0f}/MT",
    f"Coal Index {_COAL_INDEX:.1f}",
    f"Diamond Index {_DIAMOND_INDEX:.1f}",
)
_ticker_html = "".join(f'<span>{t}</span>' for t in _ticker_items)
st.markdown(
    f'<div class="prism-ticker-wrap">'
    f'<div class="prism-ticker">{_ticker_html}{_ticker_html}</div>'
    f'</div>',
    unsafe_allow_html=True,
)

# ——— Abuja-Zaria-Kano Corridor: Energy-Industrial Spine (Silk Road of NWC/C&D) ———
st.markdown(
    f'<div class="azk-corridor">'
    f'<div class="azk-title">🛤️ {ABUJA_ZARIA_KANO_CORRIDOR} Corridor</div>'
    f'<div class="azk-desc">Energy-Industrial Spine of NWC/C&D — The Silk Road linking sovereign coal-to-compute and 1.2 GW power potential.</div>'
    f'</div>',
    unsafe_allow_html=True,
)

# ——— Global Clocks: Wall Street (NY), Silicon Valley (CA), Dubai (UAE), Main Street (Abuja) ———
def _now_tz(tz_name):
    if ZoneInfo is None:
        # Fallback for Python < 3.9: use UTC offset hints
        offsets = {"America/New_York": -5, "America/Los_Angeles": -8, "Asia/Dubai": 4, "Africa/Lagos": 1}
        off = offsets.get(tz_name, 0)
        return (datetime.utcnow() + timedelta(hours=off)).strftime("%H:%M")
    try:
        return datetime.now(ZoneInfo(tz_name)).strftime("%H:%M")
    except Exception:
        return "—"
_ny = _now_tz("America/New_York")
_ca = _now_tz("America/Los_Angeles")
_dubai = _now_tz("Asia/Dubai")
_abuja = _now_tz("Africa/Lagos")
st.markdown(
    '<div class="global-clocks">'
    f'<div class="clock-node"><div class="clock-label">Wall Street (NY)</div><div class="clock-time">{_ny}</div></div>'
    f'<div class="clock-node"><div class="clock-label">Silicon Valley (CA)</div><div class="clock-time">{_ca}</div></div>'
    f'<div class="clock-node"><div class="clock-label">Dubai (UAE)</div><div class="clock-time">{_dubai}</div></div>'
    f'<div class="clock-node"><div class="clock-label">Main Street (Abuja)</div><div class="clock-time">{_abuja}</div></div>'
    '</div>',
    unsafe_allow_html=True,
)
st.caption("Global operational readiness — live time nodes.")

# ——— 37-Node Geopolitical Grid (36 States + FCT) ———
st.write("### 🗺️ Command & Control (C&D) Grid — 37-Node Geopolitical Grid")
st.caption("Click a state to trigger 95/5 Talon Lock data flare and drill down into Local Government Areas (774 LGA nodes).")

# Group states by region for display
region_to_states = defaultdict(list)
for state in STATES:
    region = STATE_REGION.get(state, "Other")
    region_to_states[region].append(state)

# Region order matching user spec
REGION_ORDER = [
    "North West", "North East", "North Central",
    "South South", "South East", "South West", "FCT",
]
for region in REGION_ORDER:
    states_in_region = region_to_states.get(region, [])
    if not states_in_region:
        continue
    with st.expander(f"**{region}** ({sum(STATE_LGA_COUNT.get(s, 0) for s in states_in_region)} LGAs)", expanded=(region == "North West")):
        cols = st.columns(min(len(states_in_region), 4))
        for idx, state in enumerate(states_in_region):
            col = cols[idx % len(cols)]
            with col:
                if st.button(f"📍 {state} ({STATE_LGA_COUNT.get(state, 0)} LGAs)", key=f"node_{state}"):
                    st.session_state.selected_state = state
                    st.rerun()

# Drill-down: selected state LGAs + 95/5 Talon Lock data flare (9.6x | $170.85B)
if st.session_state.selected_state:
    state = st.session_state.selected_state
    region = STATE_REGION.get(state, "")
    lgas = get_lgas(state)
    # 95/5 Talon Lock data flare on node click (per directive)
    st.markdown(
        f'<div class="talon-lock-flare">'
        f'<span class="flare-label">95/5 Talon Lock</span> '
        f'<span class="flare-value">9.6× Wealth Multiplier | ${VALUATION_ANCHOR_B:.2f}B Valuation Anchor.</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.write(f"#### 📌 {state} — {region}")
    st.caption(f"{len(lgas)} Local Government Areas (LGA Micro-Veracity active)")
    # 774 LGA grid: Navy Blue & Metallic Gold themed list (no overload)
    lga_items = "".join(f"<li>{lga}</li>" for lga in lgas)
    st.markdown(f'<div class="nwc-lga-grid"><ul style="color: #D4AF37; background: transparent;">{lga_items}</ul></div>', unsafe_allow_html=True)
    if st.button("Clear selection", key="clear_state"):
        st.session_state.selected_state = None
        st.rerun()

st.markdown("---")

# ——— D3 Scientific Profit Centers (9.6x wealth multiplier) ———
st.write("### ⚡ D3 Scientific Profit Centers")
st.caption("Per MT coal/diamond throughput: **9.6×** wealth multiplier. Unit-price derivatives below.")
d3_col1, d3_col2 = st.columns(2)
with d3_col1:
    st.metric("Wealth Multiplier (per MT throughput)", f"{D3_WEALTH_MULTIPLIER}×")
    st.metric("Germanium (AI Chip Grade)", f"${D3_GERMANIUM_USD_PER_KG:,.0f}/kg")
    st.metric("Ammonia (Fertilizer Grade)", f"${D3_AMMONIA_USD_PER_MT:,.0f}/MT")
with d3_col2:
    st.metric("Silicon (Semiconductor Grade) — Monthly Yield", f"${D3_SILICON_MONTHLY_YIELD_M}M")
    st.metric("Coal Syngas (Sovereign Feedstock) — Monthly Revenue", f"${D3_COAL_SYNGAS_MONTHLY_REVENUE_M}M")
st.caption("**Diamond (Industrial Tech Grade):** Heat Sinks & Precision Abrasives — sovereign value chain.")

st.markdown("---")

# ——— 95/5 Talon Lock Algorithm ———
st.write("### 🔒 Sovereign Retention — 95/5 Talon Lock")
national_pct = int(TALON_LOCK_NATIONAL_PCT * 100)
global_pct = int(TALON_LOCK_GLOBAL_POOL_PCT * 100)
st.markdown(f"**{national_pct}% National Equity** (locked) | **{global_pct}% Global Adoption Pool** (Wall Street / Silicon Valley partners)")
example_rev = 100.0  # $100M derivative revenue example
nat, gl = apply_95_5_talon_lock(example_rev)
st.metric("Example: $100M derivative revenue", f"National: **${nat:.0f}M** · Global Pool: **${gl:.0f}M**")

st.markdown("---")

# ——— 8R Stealth Multiplier: Dynamic dashboard (Recharts-style via Plotly) ———
# Performance mandate: on connection/chart error, prioritize core 8R logic gates; charts are optional.
try:
    import plotly.graph_objects as go

    st.write("### 📊 8R Stealth Multiplier — Dynamic Dashboard")
    # 1) 95/5 Talon Lock: Raw carbon assets → $170.85B Sovereign Valuation
    fig_talon = go.Figure(data=[
        go.Bar(name="National (95%)", x=["Raw carbon assets", "Sovereign Valuation"], y=[100, VALUATION_ANCHOR_B * 0.95], marker_color="#D4AF37"),
        go.Bar(name="Global Pool (5%)", x=["Raw carbon assets", "Sovereign Valuation"], y=[0, VALUATION_ANCHOR_B * 0.05], marker_color="#E8C547"),
    ])
    fig_talon.update_layout(barmode="stack", title="95/5 Talon Lock → $170.85B Sovereign Valuation", template="plotly_dark", paper_bgcolor="rgba(0,0,128,0.9)", plot_bgcolor="rgba(0,0,128,0.8)", font=dict(color="#D4AF37"), height=280, margin=dict(t=40,b=30,l=40,r=30))
    st.plotly_chart(fig_talon, use_container_width=True)

    # 2) 9.6× Wealth Multiplier: Raw commodities → AI-ready Germanium/Silicon
    raw_val = 1.0
    derived_val = D3_WEALTH_MULTIPLIER * raw_val
    fig_mult = go.Figure(data=[
        go.Bar(x=["Raw commodities", "AI-ready (9.6×)"], y=[raw_val, derived_val], marker_color=["#5a6c7d", "#D4AF37"], text=[f"{raw_val}×", f"{derived_val}×"], textposition="outside"),
    ])
    fig_mult.update_layout(title="9.6× Wealth Multiplier: Raw → Germanium/Silicon precursors", template="plotly_dark", paper_bgcolor="rgba(0,0,128,0.9)", plot_bgcolor="rgba(0,0,128,0.8)", font=dict(color="#D4AF37"), height=280, margin=dict(t=40,b=30,l=40,r=30))
    st.plotly_chart(fig_mult, use_container_width=True)

    # 3) Industrial Spine: Abuja-Zaria-Kano Corridor (interactive)
    corridor_nodes = ["Abuja", "Zaria", "Kano"]
    corridor_vals = [1.2, 0.9, 1.0]  # relative power/activity
    fig_corridor = go.Figure(data=[go.Scatter(x=corridor_nodes, y=corridor_vals, mode="lines+markers", line=dict(color="#D4AF37", width=3), marker=dict(size=14))])
    fig_corridor.update_layout(title=f"Industrial Spine: {ABUJA_ZARIA_KANO_CORRIDOR} Corridor", template="plotly_dark", paper_bgcolor="rgba(0,0,128,0.9)", plot_bgcolor="rgba(0,0,128,0.8)", font=dict(color="#D4AF37"), height=260, margin=dict(t=40,b=30,l=40,r=30))
    st.plotly_chart(fig_corridor, use_container_width=True)
except Exception as e:
    # Prioritize core 8R logic; charts optional (high-velocity deployment, connection-error resilience)
    st.caption("8R Stealth charts load on demand. Core logic gates active.")

st.markdown("---")

# 8R Stealth Engine — D1–D8 Determinant Widgets (golden Breathing animation)
st.write("### 8R Stealth Engine — Determinant Widgets (D1–D8)")
# Central valuation + Compute Potential (Inference-Ready) gauge — Diamond Standard for Silicon Valley / Jensen Huang
_central_rev = VALUATION_ANCHOR_B * 1e9 / 1e6  # $170.85B as equivalent revenue scale for split
_nat_anchor, _gl_pool = apply_95_5_talon_lock(_central_rev)
# Coal reserves → power (1.2 GW) → H100/H200 GPU-Hours: 1.2e6 kW / ~0.7 kW per H100 ≈ 1.71e6 GPUs × 8760 hrs/yr
_H100_KW = 0.7
_H200_KW = 1.4
_gpu_h100_hrs_yr = (POWER_POTENTIAL_GW * 1e6 / _H100_KW) * 8760
_gpu_h200_hrs_yr = (POWER_POTENTIAL_GW * 1e6 / _H200_KW) * 8760
_val_col, _compute_col = st.columns(2)
with _val_col:
    st.markdown(
        f'<p class="central-valuation">Central Valuation (D8 Talon Lock): <strong>${VALUATION_ANCHOR_B:.2f}B</strong> '
        f'→ National: <strong>${_nat_anchor:,.0f}M</strong> · Global Pool: <strong>${_gl_pool:,.0f}M</strong></p>',
        unsafe_allow_html=True,
    )
with _compute_col:
    st.metric("Compute Potential (Inference-Ready)", f"~{_gpu_h100_hrs_yr/1e9:.1f}B H100 GPU-Hrs/yr", "Diamond Standard for Silicon Valley")
    st.caption(f"~{_gpu_h200_hrs_yr/1e9:.1f}B H200 GPU-Hrs/yr from {POWER_POTENTIAL_GW} GW corridor — coal reserves to GPU-hours.")
st.caption("apply_95_5_talon_lock from d8_logic.py linked to central valuation. Inference-Ready metric: coal reserves → GPU-hours.")
# D1–D8 with golden Breathing animation (CSS class .d8-widget-breathing)
d8_html = "".join(
    f'<div class="d8-widget-breathing">D{i}: {det}</div>' for i, det in enumerate(DETERMINANTS, 1)
)
st.markdown(f'<div class="d8-widgets-grid">{d8_html}</div>', unsafe_allow_html=True)

# Sovereign Retention Protocol (D8 Logic) — 95% National Equity (Talon Lock)
with st.expander("🔒 Sovereign Retention Protocol (D8 Logic)", expanded=True):
    st.markdown(SOVEREIGN_RETENTION_PROTOCOL)
    st.metric(label="Value Anchor (D8 Talon Lock)", value=f"{int(WEALTH_RETENTION_LOCK * 100)}%")
    st.caption(f"Structural foundation: {STRATEGIC_FOUNDATION} — national core preserved under global expansion.")
    # Example: apply_talon_lock
    example_value = 4.2  # e.g. $4.2B
    retained = apply_talon_lock(example_value)
    st.caption(f"*Example:* `apply_talon_lock({example_value})` → **{retained:.2f}** retained by Sovereign Node.")

# Interactive NRRFC Dashboard – Mineral Density & Defense Toggle
st.write("### 🛡️ NRRFC – Mineral Density & Defense Dashboard")
toggle_minerals = st.checkbox("Activate Mineral Density & Defense Toggle", value=False)
if toggle_minerals:
    st.caption("NGECC – Sovereign Minerals: Coal (Energy), Diamonds (Value), Uranium (Strategic Depth) under 95% Talon Lock.")

    # Unified Carbon Gateway — Diamond-Coal Bridge (anchor: Line 117)
    st.write("#### NRRFC Fusion Strike: Unified Carbon Gateway")
    st.caption("Diamond-Coal Bridge: NW/NE Diamond Nodes integrated with Coal (Energy) under D3 Research.")

    # New layer: NW/NE Diamond Nodes (Diamond-Coal Bridge)
    st.write("**Diamond-Coal Bridge — NW/NE Diamond Nodes Layer**")
    diamond_reserves = get_diamond_reserves()
    nw_ne_nodes = [n for n in diamond_reserves if n.get("region") in ("North East", "North West")]
    if nw_ne_nodes:
        bridge_df = pd.DataFrame(nw_ne_nodes)[["state", "region", "proven_reserve_probability", "retained_value_usd"]].copy()
        bridge_df = bridge_df.rename(columns={"state": "State", "region": "Region", "proven_reserve_probability": "Proven Reserve Probability"})
        bridge_df["95% Retained Sovereign Value"] = bridge_df["retained_value_usd"].apply(lambda v: f"${v:,.0f}")
        st.dataframe(bridge_df[["State", "Region", "Proven Reserve Probability", "95% Retained Sovereign Value"]], width="stretch")
    else:
        st.caption("No NW/NE diamond nodes in current dataset.")

    # 95% Metric: monthly revenue (verified North West Hydrothermal Discovery default)
    GROSS_MONTHLY_REVENUE_M = 415  # $415M default — verified North West Hydrothermal Discovery
    monthly_gross_usd = GROSS_MONTHLY_REVENUE_M * 1_000_000
    monthly_retained = apply_talon_lock(monthly_gross_usd)  # 95% Talon Lock
    retained_display_m = int(monthly_retained / 100_000) / 10
    c1, c2 = st.columns(2)
    with c1:
        st.metric(label="Monthly Revenue (Gross)", value=f"${GROSS_MONTHLY_REVENUE_M}M")
    with c2:
        st.metric(label="Monthly Revenue (95% Retained — Talon Lock)", value=f"${retained_display_m:.1f}M")

    nodes = get_nodes() or []  # D7: ensure list, never None
    rows = []
    for node in nodes:
        r = retained_yield(node)
        idx = global_market_impact_index(node)
        rows.append(
            {
                "Node": node.name,
                "Region": node.region,
                "Type": node.mineral_type,
                "D-Index": node.d_index,
                "Base Yield": node.base_yield,
                "Retained Yield (95%)": round(r, 2),
                "Global Impact Index": round(idx, 2),
            }
        )
    st.dataframe(rows, width="stretch")

    # D3: Mineral Research Node – State-by-state table (Proven Reserve Probability | 95% Retained Sovereign Value)
    st.write("#### D3: Mineral Research Node — Sovereign Mineral Fortress")
    st.caption("Nigeria is not just an oil nation: kimberlite pipe signatures (NE) and structural hydrothermal trends (NW) under 8R D3 Research.")
    diamond_data = get_diamond_reserves()
    if diamond_data:
        df = pd.DataFrame(diamond_data)
        table_df = df[["state", "proven_reserve_probability", "retained_value_usd"]].copy()
        table_df.rename(
            columns={
                "state": "State",
                "proven_reserve_probability": "Proven Reserve Probability",
                "retained_value_usd": "95% Retained Sovereign Value",
            },
            inplace=True,
        )
        table_df["95% Retained Sovereign Value"] = table_df["95% Retained Sovereign Value"].map(lambda v: f"${v:,.0f}")
        st.dataframe(table_df, width="stretch")

# Tactical Experience: Login (Password GCSLC2026) → Eagle cry; SWAT soundscape
with st.sidebar:
    st.header("🔐 NWC/C&D Access")
    if not st.session_state.nwc_authenticated:
        _pw = st.text_input("Password", type="password", key="nwc_pw", placeholder="Enter directive password")
        if st.button("Login", key="nwc_login") and _pw == "GCSLC2026":
            st.session_state.nwc_authenticated = True
            play_eagle_cry()  # Majestic Eagle/Falcon cry on login
            st.rerun()
        st.caption("Password: GCSLC2026 — Triggers Majestic Eagle/Falcon cry on success.")
    else:
        st.success("Authenticated — Eagle cry triggered.")
        swat_path = get_swat_beep_path()
        if swat_path:
            try:
                with open(swat_path, "rb") as f:
                    wav_b64 = base64.b64encode(f.read()).decode("utf-8")
                # Loop SWAT-style HUD two-beep WAV (injected HTML5 audio)
                components.html(
                    f'<audio id="swat-hud-loop" loop autoplay><source src="data:audio/wav;base64,{wav_b64}" type="audio/wav"></audio>',
                    height=0,
                )
            except Exception:
                try:
                    with open(swat_path, "rb") as _f:
                        st.audio(_f.read(), format="audio/wav")
                except Exception:
                    pass
        st.caption("Soundscape: SWAT-style HUD two-beep (swat_hud_beep.wav) looping when asset present.")
    st.markdown("---")
    st.header("📖 Sovereign Tactical Glossary")
    with st.expander("NWC/C&D", expanded=True):
        st.markdown(
            "**National Wealth Cloud for Nigeria: Coal & Diamond** — "
            "The unassailable master framework for sovereign mineral and energy value chains; "
            "37-Node Geopolitical Grid (36 States + FCT) with LGA-level drill-down."
        )
    with st.expander("SSMV"):
        st.markdown(
            "**Special Strategic Mission Vehicle** — "
            "The institutional framework designed to execute the 8R Stealth Paradigm and manifest the 9.6× wealth multiplier."
        )
    with st.expander("95/5 Talon Lock"):
        st.markdown(
            "**Sovereign Retention Algorithm** — "
            "95% of all derivative revenue locked as **National Equity**; "
            "5% **Global Adoption Pool** for Wall Street / Silicon Valley partners."
        )
    with st.expander("8R Stealth Paradigm (D1–D8)"):
        for i, det in enumerate(DETERMINANTS, 1):
            st.caption(f"**D{i}:** {det}")
    st.markdown("---")
    # WhatsApp Gateway — Contact for Sovereign Access (deep-data clearance)
    st.header("📱 Sovereign Access")
    whatsapp_contact = "https://wa.me/2340000000000"  # Replace with official GCSLC number for deep-data clearance
    st.link_button("Contact WhatsApp for Sovereign Access", whatsapp_contact, type="secondary", help="Deep-data clearance and sovereign gateway access.")
    st.caption("Security Layer: Use for verified sovereign access.")
    st.markdown("---")
    st.header("Strategic Strike Input")
    friction_target = st.text_input("Enter Friction Target:", "National Asset", key="gcslc_friction_key")
    if st.button("EXECUTE 8R STRIKE", key="gcslc_strike_button"):
        st.session_state.strike = True
        st.session_state.strike_manifested = False
        st.session_state.certificate_shown = False
        st.rerun()

# After strike: show 100% manifested state, then certificate button
if st.session_state.strike:
    # Simulate 100% manifestation (immediate in this build; could add 0.4s cascade here)
    st.session_state.strike_manifested = True
    st.success(f"**8R Strike 100% manifested** — Friction Target: **{friction_target}**")
    st.metric(label="Strike Status", value="MANIFESTED")

    # Certificate Trigger: button only after strike 100% manifested
    if st.session_state.strike_manifested and not st.session_state.certificate_shown:
        if st.button("GENERATE SOVEREIGN PROOF CERTIFICATE", type="primary", key="spc_gen_btn"):
            st.session_state.certificate_shown = True
            play_talon_lock_confirmed()  # Submarine chime when 95% Talon Lock confirmed
            st.rerun()

    # Visual Proof: Sovereign Proof Certificate
    if st.session_state.certificate_shown:
        st.write("---")
        st.write("### 📜 Sovereign Proof Certificate (SPC)")

        # GCSLC Gold Seal — visual proof at top of certificate
        if os.path.isfile(SEAL_PATH):
            st.image(SEAL_PATH, caption="GCSLC Gold Seal", width=120)
        else:
            st.markdown(
                '<div style="width: 120px; height: 120px; margin: 0 auto 1rem; border: 3px solid #D4AF37; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; color: #D4AF37;">GCSLC<br/>SEAL</div>',
                unsafe_allow_html=True,
            )

        cert_html = """
        <div class="spc-cert">
        <div class="spc-watermark">Proprietary Nodal Logic — Galadiman Ruwa Center — Protected Asset</div>
        <p style="text-align: center; font-weight: 700; font-size: 1.2rem;">SOVEREIGN PROOF CERTIFICATE</p>
        <p style="text-align: center;">Galadiman Ruwa Center For Strategic Leadership and Communication LTD/GTE — GCSLC</p>
        <p class="cascade-map"><strong>D1–D8 Cascade (Hierarchical Map):</strong><br/>
        D1 Refine → D2 Reset → D3 Research → D4 Restructure → D5 Resuscitate → D6 Revitalize → D7 Re-engineer → D8 Retain
        </p>
        <p class="talon-metric">🔒 95% Legacy Retention / Talon Lock — Primary Security Metric for this Strike</p>
        <p class="footer-cert" style="font-size: 0.8rem; margin-top: 0.75rem;">Governed by the <strong>Sovereign Retention Protocol (D8 Logic)</strong>: 95% Value Anchor (Talon Lock); 1m × 1m structural depth; economic velocity and intellectual derivative value retained by the Sovereign Node.</p>
        <p class="footer-cert">This Certificate validates the Scientific Universality of the 8R Stealth Paradigm across Human, Economic, and AI Systems.</p>
        <p class="footer-cert" style="margin-top: 0.5rem; font-size: 0.75rem; opacity: 0.85;">Strategic DNA v4.0 - Proprietary Nodal Logic of GCSLC. Unauthorized Replication Subject to Sovereign Re-engineering.</p>
        </div>
        """
        st.markdown(cert_html, unsafe_allow_html=True)

# Footer — Contact & Credibility (official contact; password gate GCSLC2026 maintained)
st.markdown("---")
st.caption(
    f"Strategic Infrastructure Manifested by: {FULL_NAME} — {BRAND}  |  © 2026  |  Proprietary Nodal Logic — Protected Asset  |  "
    "**Contact:** [info@galadimanruwacenter.org](mailto:info@galadimanruwacenter.org)"
)

# Chairman's Seal: Bottom-right fixed sticky bar — Dr. Sa'ad Jaafaru with shimmering gold signature
st.markdown(
    '<div class="chairman-sticky-bar chairman-signature-shimmer">Dr. Sa\'ad Jaafaru — Chairman & Founder</div>',
    unsafe_allow_html=True,
)
