"""
Sovereign Mirror — Digital Doorstep for GCSLC (Sovereign Command Aesthetic)
Galadiman Ruwa Center for Strategic Leadership and Communication (GCSLC) LTD/GTE.
Port 8055. Key 8R-DECODE-2026 fuses into full Universal Impact Radar.
© 2026 GCSLC. Chairman & Founder: Dr. Sa'ad Jaafaru.
"""

import os
import sys
import importlib.util
import streamlit as st

# --- African_Gateway load (for Universal Impact Radar after decode) ---
_BASE = os.path.dirname(os.path.abspath(__file__))
_GATEWAY = os.path.join(_BASE, "African_Gateway.")
if _BASE not in sys.path:
    sys.path.insert(0, _BASE)


def _load_module(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@st.cache_resource
def _get_continental_logic():
    return _load_module("awc_continental_logic", os.path.join(_GATEWAY, "continental_logic.py"))


# --- Page config (must be first Streamlit call) ---
st.set_page_config(
    page_title="Sovereign Mirror — GCSLC",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Session state ---
if "mirror_decoded" not in st.session_state:
    st.session_state.mirror_decoded = False

# --- Design tokens ---
NAVY = "#000033"
GOLD = "#D4AF37"
PASSWORD_UNLOCK = "8R-DECODE-2026"
FULL_NAME = "Galadiman Ruwa Center for Strategic Leadership and Communication (GCSLC) LTD/GTE"
SIGNATURE = "Dr. Jaafaru Sa'ad — Chairman & Founder"
TICKER_TEXT = "COAL [NGECC]: $170.8B INDEX  |  SILICON FEEDSTOCK: 639.3M MT  |  GERMANIUM PULSE: ACTIVE  |  ABUJA-ZARIA-KANO CORRIDOR"

# 13 State Nodes (Map of Authority): Enugu to Imo corridor
STATE_NODES = (
    "Enugu", "Kogi", "Gombe", "Benue", "Delta", "Nasarawa", "Anambra",
    "Plateau", "Adamawa", "Edo", "Bauchi", "Kwara", "Imo",
)

# Apex Predator Eagle emblem (inline SVG, top center)
APEX_EAGLE_SVG = '''<svg width="64" height="46" viewBox="0 0 56 40" fill="none" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto;filter:drop-shadow(0 0 12px rgba(212,175,55,0.6));">
  <ellipse cx="28" cy="20" rx="14" ry="10" fill="#D4AF37" stroke="#B8860B" stroke-width="1"/>
  <path d="M18 16 L28 12 L38 16" stroke="#B8860B" stroke-width="1" fill="none"/>
  <path d="M20 22 Q28 18 36 22" stroke="#C9A227" stroke-width="0.7" fill="none" opacity="0.9"/>
  <circle cx="24" cy="18" r="2" fill="#1a1a1a"/><circle cx="32" cy="18" r="2" fill="#1a1a1a"/>
  <path d="M26 24 L28 30 L30 24" stroke="#B8860B" stroke-width="0.5" fill="none"/>
</svg>'''

# --- Global CSS: Sovereign Command aesthetic ---
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap');

:root {
    --institutional-navy: #000033;
    --sovereign-gold: #D4AF37;
    --gold-light: rgba(212, 175, 55, 0.95);
    --gold-subtle: rgba(212, 175, 55, 0.6);
}

.stApp, [data-testid="stAppViewContainer"], .main .block-container {
    background: var(--institutional-navy) !important;
    color: var(--sovereign-gold) !important;
}
.main .block-container { padding: 1rem 2rem 6rem; max-width: 100%; }

h1, h2, h3, .gcslc-header, .ticker-text, .market-card h3, .map-node {
    font-family: 'Goldman', sans-serif !important;
    color: var(--sovereign-gold) !important;
}

/* Header: Goldman + Shimmering Prism (liquid gold) */
.prism-name {
    font-family: 'Goldman', sans-serif !important;
    font-size: clamp(1.25rem, 3vw, 2rem) !important;
    font-weight: 700;
    text-align: center;
    letter-spacing: 0.02em;
    line-height: 1.4;
    background: linear-gradient(110deg, #D4AF37 0%, #F9F295 15%, #FFFFFF 35%, #F9F295 55%, #D4AF37 75%, #B8960C 100%);
    background-size: 300% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: prism-shimmer 4s ease-in-out infinite;
}
@keyframes prism-shimmer {
    0%, 100% { background-position: 0% center; }
    50% { background-position: 100% center; }
}

/* Real-Time Market Values: 4 high-fidelity glowing cards */
.market-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 1.5rem 0;
    max-width: 1100px;
    margin-left: auto;
    margin-right: auto;
}
.market-card {
    background: rgba(0, 0, 51, 0.7);
    border: 2px solid var(--sovereign-gold);
    border-radius: 12px;
    padding: 1.25rem;
    text-align: center;
    box-shadow: 0 0 24px rgba(212, 175, 55, 0.2), inset 0 1px 0 rgba(255,255,255,0.06);
    transition: box-shadow 0.3s ease, transform 0.2s ease;
}
.market-card:hover {
    box-shadow: 0 0 32px rgba(212, 175, 55, 0.4), inset 0 1px 0 rgba(255,255,255,0.08);
    transform: translateY(-2px);
}
.market-card h3 { font-size: clamp(0.8rem, 1.2vw, 1rem); margin: 0 0 0.4rem; text-transform: uppercase; letter-spacing: 0.08em; }
.market-card .price { font-family: 'Goldman', sans-serif; font-size: clamp(1rem, 1.8vw, 1.3rem); font-weight: 700; color: var(--sovereign-gold); }
.market-card .sub { font-size: 0.7rem; color: var(--gold-subtle); margin-top: 0.35rem; line-height: 1.3; }

/* Map of Authority: 13 State Nodes */
.map-of-authority {
    margin: 2rem 0;
    padding: 1.25rem;
    border: 2px solid rgba(212, 175, 55, 0.4);
    border-radius: 12px;
    background: rgba(0, 0, 51, 0.5);
}
.map-of-authority h3 {
    font-family: 'Goldman', sans-serif !important;
    color: var(--sovereign-gold) !important;
    text-align: center;
    margin-bottom: 1rem;
    letter-spacing: 0.15em;
}
.map-nodes {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.5rem;
}
.map-node {
    padding: 0.4rem 0.75rem;
    border: 1px solid var(--sovereign-gold);
    border-radius: 8px;
    font-size: 0.85rem;
    background: rgba(212, 175, 55, 0.08);
    color: var(--sovereign-gold);
}

/* Live Ticker */
.ticker-wrap {
    position: fixed;
    bottom: 3rem;
    left: 0;
    right: 0;
    height: 2.5rem;
    background: rgba(0, 0, 51, 0.95);
    border-top: 2px solid var(--sovereign-gold);
    overflow: hidden;
    z-index: 900;
    display: flex;
    align-items: center;
}
.ticker-inner { display: flex; animation: ticker-scroll 35s linear infinite; white-space: nowrap; }
.ticker-text { font-family: 'Goldman', sans-serif; font-size: 0.9rem; color: var(--sovereign-gold); letter-spacing: 0.15em; padding: 0 3rem; }
@keyframes ticker-scroll { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

/* Signature: bottom-left, sovereign seal */
.signature-watermark {
    position: fixed;
    bottom: 0.5rem;
    left: 1rem;
    font-family: 'Goldman', sans-serif;
    font-size: 0.7rem;
    color: var(--gold-subtle);
    letter-spacing: 0.08em;
    z-index: 901;
    opacity: 0.9;
    padding: 0.25rem 0.5rem;
    border-left: 3px solid var(--sovereign-gold);
    background: rgba(0, 0, 51, 0.6);
}
.signature-watermark { border-radius: 0 4px 4px 0; }

/* Sovereign Bridge (after decode) */
.bridge-overlay {
    position: fixed;
    inset: 0;
    background: var(--institutional-navy);
    z-index: 9999;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    animation: bridge-fade-in 0.5s ease-out;
}
.bridge-scan {
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, transparent, var(--sovereign-gold), transparent);
    animation: bridge-scan 2s ease-in-out 1;
    box-shadow: 0 0 20px var(--sovereign-gold);
}
.bridge-title {
    font-family: 'Goldman', sans-serif;
    font-size: clamp(1.5rem, 4vw, 2.5rem);
    color: var(--sovereign-gold);
    margin: 2rem 0;
    letter-spacing: 0.2em;
    animation: bridge-glow 1.5s ease-in-out 2;
}
@keyframes bridge-fade-in { from { opacity: 0; } to { opacity: 1; } }
@keyframes bridge-scan { 0% { transform: translateY(-100vh); } 100% { transform: translateY(100vh); } }
@keyframes bridge-glow {
    0%, 100% { opacity: 1; text-shadow: 0 0 20px var(--gold-subtle); }
    50% { opacity: 0.9; text-shadow: 0 0 40px var(--sovereign-gold); }
}

/* Password / Decode */
.stTextInput input { border: 2px solid var(--sovereign-gold) !important; border-radius: 8px !important; }
.stButton > button {
    font-family: 'Goldman', sans-serif !important;
    background: transparent !important;
    color: var(--sovereign-gold) !important;
    border: 2px solid var(--sovereign-gold) !important;
    border-radius: 8px !important;
}
.stButton > button:hover {
    background: rgba(212, 175, 55, 0.15) !important;
    border-color: var(--sovereign-gold) !important;
    color: var(--sovereign-gold) !important;
}

/* Universal Impact Radar (fused view) */
.radar-header { font-family: 'Goldman', sans-serif !important; color: var(--sovereign-gold) !important; }

@media (max-width: 768px) {
    .market-row { grid-template-columns: 1fr 1fr; }
    .main .block-container { padding: 0.75rem 1rem 5rem; }
    .ticker-wrap { bottom: 2.5rem; height: 2rem; }
    .ticker-text { font-size: 0.75rem; }
    .signature-watermark { font-size: 0.6rem; left: 0.5rem; }
}
</style>
""",
    unsafe_allow_html=True,
)

# --- Post-decode: Sovereign Bridge then fuse into Universal Impact Radar ---
if st.session_state.mirror_decoded:
    st.markdown(
        """
        <div class="bridge-overlay" id="gcslc-bridge">
            <div class="bridge-scan"></div>
            <p class="bridge-title">SOVEREIGN BRIDGE</p>
            <p style="font-family: Goldman, sans-serif; color: rgba(212,175,55,0.8); font-size: 0.95rem;">Decode verified. Fusing into Universal Impact Radar.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown("### Universal Impact Radar")
    st.caption("How the **$170.85B** anchor and **8R Strike on Atoms** (Energy/Minerals) drive Jobs, Security, and Health.")
    continental_logic = _get_continental_logic()
    radar_t1, radar_t2, radar_t3 = st.tabs(["National Security Impact", "Social Well-being Index", "Sovereign Well-being Index"])
    with radar_t1:
        st.write("**National Security Impact** — $170.85B anchor → regional stability")
        sec_heat = continental_logic.get_national_security_impact_heatmap()
        st.dataframe(
            [{"Region": r["region"], "Indicator": r["indicator"], "Before anchor": r["before_anchor"], "After anchor": r["after_anchor"], "Δ Stability": r["stability_delta"]} for r in sec_heat],
            use_container_width=True,
            hide_index=True,
        )
        st.caption("Higher scores = more stability. The anchor increases sovereign retention and reduces resource conflict.")
    with radar_t2:
        st.write("**Social Well-being Index** — $170.85B anchor → poverty reduction")
        soc_heat = continental_logic.get_social_wellbeing_index_heatmap()
        st.dataframe(
            [{"Dimension": d["dimension"], "Baseline (%)": d["baseline_pct"], "Post-anchor (%)": d["post_anchor_pct"], "Change": d["reduction"]} for d in soc_heat],
            use_container_width=True,
            hide_index=True,
        )
        st.caption("Poverty headcount drops; employment and energy access rise under 8R sovereign corridors.")
    with radar_t3:
        st.write("**Sovereign Well-being Index** — 8R Strike on Atoms → Jobs, Security, Health")
        swi = continental_logic.get_sovereign_wellbeing_index()
        st.dataframe(
            [{"Atoms domain": r["atoms_domain"], "Well-being": r["wellbeing_dimension"], "Metric": r["metric"], "Before 8R": r["before_8r"], "After 8R": r["after_8r"], "Unit": r["unit"]} for r in swi],
            use_container_width=True,
            hide_index=True,
        )
        st.caption("The Eagle's strike on Energy and Minerals generates Jobs (FTE), Security (index), and Health (compliance / air quality).")
    st.markdown(
        f'<div class="ticker-wrap"><div class="ticker-inner"><span class="ticker-text">{TICKER_TEXT}</span><span class="ticker-text">{TICKER_TEXT}</span></div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="signature-watermark">{SIGNATURE}</div>', unsafe_allow_html=True)
    st.stop()

# --- Main Mirror: Sovereign Command face ---
# Eagle at top center
st.markdown(f'<div style="text-align:center; margin-bottom:0.5rem;">{APEX_EAGLE_SVG}</div>', unsafe_allow_html=True)
st.markdown(f'<p class="prism-name">{FULL_NAME}</p>', unsafe_allow_html=True)
st.markdown("---")

# Real-Time Market Values: 4 glowing cards
st.markdown(
    """
    <div class="market-row">
        <div class="market-card">
            <h3>Germanium</h3>
            <p class="price">$2,152/kg</p>
            <p class="sub">Optics, chips, sensors.</p>
        </div>
        <div class="market-card">
            <h3>Silicon</h3>
            <p class="price">$18.27/sq</p>
            <p class="sub">Solar, wafers, compute.</p>
        </div>
        <div class="market-card">
            <h3>Benzene</h3>
            <p class="price">$858/MT</p>
            <p class="sub">Petrochem feedstock.</p>
        </div>
        <div class="market-card">
            <h3>Rare Earths</h3>
            <p class="price">$132,853/kg</p>
            <p class="sub">Magnets, EV, Defense.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("---")

# Map of Authority: 13 State Nodes (Enugu to Imo)
nodes_html = "".join(f'<span class="map-node">{s}</span>' for s in STATE_NODES)
st.markdown(
    f"""
    <div class="map-of-authority">
        <h3>Map of Authority — 13 State Nodes</h3>
        <div class="map-nodes">{nodes_html}</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("---")

# Decode: key 8R-DECODE-2026 fuses into Universal Impact Radar
st.markdown("#### Access Universal Impact Radar")
pwd = st.text_input("Decode phrase", type="password", placeholder="Enter decode phrase", key="mirror_pwd", label_visibility="collapsed")
col1, col2, _ = st.columns([1, 1, 2])
with col1:
    submit = st.button("Decode")
if submit and pwd.strip() == PASSWORD_UNLOCK:
    st.session_state.mirror_decoded = True
    st.rerun()
elif submit and pwd:
    st.caption("Incorrect decode phrase.")

# Live Ticker + Signature (bottom-left seal)
st.markdown(
    f'<div class="ticker-wrap"><div class="ticker-inner"><span class="ticker-text">{TICKER_TEXT}</span><span class="ticker-text">{TICKER_TEXT}</span></div></div>',
    unsafe_allow_html=True,
)
st.markdown(f'<div class="signature-watermark">{SIGNATURE}</div>', unsafe_allow_html=True)
