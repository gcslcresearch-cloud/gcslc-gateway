"""
African Wealth Cloud (AWC) Portal — Port 8054
The Sovereign Glass: Deep Navy, Gold Shimmer, 8R Convergence, Nigeria Sovereign Pulse.

User Profile: Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau)
Entity: Galadiman Ruwa Center (GCSLC) LTD/GTE.
© 2026 Galadiman Ruwa Center (GCSLC) LTD/GTE.
"""

import os
import sys
import importlib.util

import streamlit as st

# Load African_Gateway modules (folder name has a dot; use file path)
_BASE = os.path.dirname(os.path.abspath(__file__))
_GATEWAY = os.path.join(_BASE, "African_Gateway.")

def _load_module(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

africa_map = _load_module("awc_africa_map", os.path.join(_GATEWAY, "africa_map.py"))
continental_logic = _load_module("awc_continental_logic", os.path.join(_GATEWAY, "continental_logic.py"))

# --- Page config (must be first Streamlit call) ---
st.set_page_config(
    page_title="Galadiman Ruwa Center (GCSLC) — AWC Portal",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Session state
if "nigeria_selected" not in st.session_state:
    st.session_state.nigeria_selected = False
if "pulse_triggered" not in st.session_state:
    st.session_state.pulse_triggered = False
if "play_swat" not in st.session_state:
    st.session_state.play_swat = False

# --- The Sovereign Glass: Deep Navy + Gold Shimmer particles + styles ---
# Build 50 particle divs with varied positions (CSS-only, no script)
PARTICLE_POSITIONS = [(7, 12), (22, 8), (88, 15), (45, 25), (3, 40), (67, 35), (15, 55), (92, 60), (30, 72), (78, 18),
                      (5, 85), (50, 5), (95, 45), (12, 28), (70, 78), (25, 92), (60, 12), (38, 48), (82, 88), (18, 65),
                      (55, 38), (9, 52), (72, 22), (42, 95), (28, 10), (85, 58), (11, 75), (63, 42), (33, 18), (76, 68),
                      (48, 82), (19, 33), (91, 7), (57, 55), (8, 90), (69, 30), (26, 48), (81, 72), (14, 62), (52, 25)]
particles_html = "".join(
    f'<span class="awc-particle" style="left:{x}%; top:{y}%; animation-delay: {i * 0.08}s;"></span>'
    for i, (x, y) in enumerate(PARTICLE_POSITIONS)
)

st.markdown("""
<style>
/* Deep Navy background; content above particles */
.stApp, [data-testid="stAppViewContainer"] { background-color: #001a33 !important; min-height: 100vh; }
.main .block-container { background-color: transparent !important; position: relative; z-index: 1; }
/* Gold Shimmer keyframes */
@keyframes awc-float {
    0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.7; }
    25% { transform: translate(10px, -15px) scale(1.2); opacity: 1; }
    50% { transform: translate(-5px, -25px) scale(0.9); opacity: 0.9; }
    75% { transform: translate(-15px, -10px) scale(1.1); opacity: 0.85; }
}
/* Glassmorphism: 85% transparent map container */
.awc-map-glass { background: rgba(0, 26, 51, 0.15); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-radius: 16px; border: 1px solid rgba(255, 215, 0, 0.25); box-shadow: inset 0 1px 0 rgba(255,255,255,0.08); }
/* Sovereign Pulse: 3s Green -> White -> Green -> GCSLC Gold Shimmer #FFD700 + glitter overlay */
@keyframes sovereign-pulse {
    0%   { box-shadow: 0 0 24px #008751, 0 0 48px rgba(0,135,81,0.7); border-color: #008751; }
    33%  { box-shadow: 0 0 28px #ffffff, 0 0 56px rgba(255,255,255,0.6); border-color: #ffffff; }
    66%  { box-shadow: 0 0 24px #008751, 0 0 48px rgba(0,135,81,0.7); border-color: #008751; }
    100% { box-shadow: 0 0 32px #FFD700, 0 0 64px rgba(255,215,0,0.6); border-color: #FFD700; }
}
.sovereign-pulse-active { animation: sovereign-pulse 3s ease-in-out 1 forwards; border: 2px solid #FFD700; border-radius: 16px; position: relative; }
.sovereign-pulse-active::after { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; pointer-events: none; border-radius: inherit; background: radial-gradient(circle at 30% 30%, rgba(255,215,0,0.12) 0%, transparent 50%), radial-gradient(circle at 70% 70%, rgba(255,215,0,0.08) 0%, transparent 45%); }
/* High-velocity typography */
h1, h2, h3, p, span, label, .stMarkdown { color: #D4AF37 !important; }
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color: #E8C547 !important; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg, #001a33 0%, #002244 100%) !important; border-right: 2px solid #D4AF37; }
/* Velocity header shimmer */
.awc-title { font-weight: 800; font-size: 1.9rem; text-align: center; background: linear-gradient(90deg, #D4AF37, #FFE55C, #D4AF37); background-size: 200% auto; -webkit-background-clip: text; background-clip: text; color: transparent !important; animation: title-shimmer 3s linear infinite; }
@keyframes title-shimmer { 0% { background-position: 0% 50%; } 100% { background-position: 200% 50%; } }
.awc-sub { text-align: center; color: rgba(212,175,55,0.9); font-size: 0.95rem; letter-spacing: 2px; margin-top: -8px; }
/* Mind-hooking metrics */
.awc-metric-box { background: rgba(0,33,71,0.7); border: 1px solid #D4AF37; border-radius: 8px; padding: 1rem; margin: 0.5rem 0; }
.footer-awc { text-align: center; font-size: 0.8rem; color: rgba(212,175,55,0.85); margin-top: 2rem; padding: 1rem; border-top: 1px solid rgba(212,175,55,0.3); }
/* Gold Shimmer particles */
#awc-shimmer-wrap { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; overflow: hidden; }
.awc-particle { position: absolute; width: 6px; height: 6px; background: radial-gradient(circle, #FFD700 0%, #D4AF37 60%, transparent 100%); border-radius: 50%; opacity: 0.9; animation: awc-float 5s ease-in-out infinite; }
</style>
<div id="awc-shimmer-wrap">""" + particles_html + """</div>
""", unsafe_allow_html=True)

# --- Header: Global Title & Branding ---
st.markdown('<p class="awc-title">Galadiman Ruwa Center (GCSLC)</p>', unsafe_allow_html=True)
st.markdown('<p class="awc-sub">LTD/GTE</p>', unsafe_allow_html=True)
st.markdown('<p class="awc-sub" style="margin-top: 4px;">The Sovereign Glass — 8R Stealth Paradigm | Dr. Sa\'ad Jaafaru (Galadiman Ruwan Zazzau)</p>', unsafe_allow_html=True)
st.markdown("---")

# --- Sidebar: Nigeria selection triggers Sovereign Pulse ---
with st.sidebar:
    st.write("### Sovereign Nodes")
    if st.button("🇳🇬 Select Nigeria", key="btn_nigeria", type="primary"):
        st.session_state.nigeria_selected = True
        st.session_state.pulse_triggered = True
        st.session_state.play_swat = True  # Build success → audio trigger
        st.rerun()
    if st.button("Clear selection", key="btn_clear"):
        st.session_state.nigeria_selected = False
        st.session_state.pulse_triggered = False
        st.rerun()
    st.caption("Select Nigeria to trigger Sovereign Pulse (Green-White-Green → GCSLC Gold).")

# --- Map container: Glassmorphism + Sovereign Pulse when Nigeria selected ---
st.write("### The Sovereign Glass — Continental View")
map_container_class = "awc-map-glass"
if st.session_state.nigeria_selected and st.session_state.pulse_triggered:
    map_container_class += " sovereign-pulse-active"
deck = africa_map.build_africa_deck(nigeria_selected=st.session_state.nigeria_selected, opacity=0.85)
if deck:
    st.markdown(f'<div class="{map_container_class}" style="padding: 8px;">', unsafe_allow_html=True)
    st.pydeck_chart(deck, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Map engine unavailable. Install pydeck and pandas.")
# After first pulse, keep Nigeria highlighted but stop animating
if st.session_state.pulse_triggered and st.session_state.nigeria_selected:
    st.session_state.pulse_triggered = False

st.caption("Africa map at 85% transparency with glitter layer. Nigeria highlighted under 8R Sovereign Pulse.")

# --- Build success: system-level audio trigger (simulated swat sound) ---
if st.session_state.get("play_swat"):
    st.session_state.play_swat = False
    st.components.v1.html("""
    <script>
    (function() {
        try {
            var C = new (window.AudioContext || window.webkitAudioContext)();
            var g = C.createGain();
            g.gain.setValueAtTime(0.35, C.currentTime);
            g.gain.exponentialRampToValueAtTime(0.01, C.currentTime + 0.08);
            g.connect(C.destination);
            var o = C.createOscillator();
            o.frequency.setValueAtTime(180, C.currentTime);
            o.frequency.exponentialRampToValueAtTime(40, C.currentTime + 0.06);
            o.connect(g);
            o.start(C.currentTime);
            o.stop(C.currentTime + 0.08);
        } catch (e) {}
    })();
    </script>
    """, height=0)

# --- 8R Logical Engine: Continental logic output ---
st.markdown("---")
st.write("### 8R Determinants — Nigeria Assets → Digital SSMVs")

summary = continental_logic.get_convergence_summary()
st.caption(f"AWC Nigeria: Minerals (Gold, Bauxite, Iron Ore, Lead-Zinc), Gems (Sapphire, Tourmaline, Aquamarine, Emerald), Energy (Oil, Natural Gas, NGECC). D1: Refine (high-purity corridors), D2: Reset (SPV→SSMV), D3: Research (rare earth coords). Wealth Retention: {summary['wealth_retention_lock_pct']}%.")

cols = st.columns(4)
for i, d in enumerate(continental_logic.DETERMINANTS_8R[:4]):
    cols[i % 4].metric(d.split(": ")[0], d.split(": ")[1] if ": " in d else d)

st.write("#### Digital SSMVs (Special Strategic Mission Vehicles)")
for s in continental_logic.get_nigeria_ssmvs():
    with st.expander(f"**{s.code}** — {s.asset_source} ({s.asset_category})"):
        c1, c2, c3 = st.columns(3)
        c1.metric("D1: Refine yield", f"${s.d1_refine_yield/1e9:.2f}B")
        c2.metric("D2: Reset yield", f"${s.d2_reset_yield/1e9:.2f}B")
        c3.metric("D3: Research yield", f"${s.d3_research_yield/1e9:.2f}B")
        if s.high_purity_corridors:
            st.caption(f"D1 corridors: {', '.join(s.high_purity_corridors[:3])}{'…' if len(s.high_purity_corridors) > 3 else ''}")
        st.caption(f"Retained value: ${s.retained_value_usd/1e9:.2f}B USD (Talon Lock) | {s.mandate}")

total = summary["total_retained_value_usd"]
st.metric("Total retained value (all Nigeria SSMVs)", f"${total/1e9:.2f}B USD")

# --- Footer: Copyright ---
st.markdown('<p class="footer-awc">© 2026 Galadiman Ruwa Center (GCSLC) LTD/GTE.</p>', unsafe_allow_html=True)
