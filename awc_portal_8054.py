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

# Session state: continental node selection (Eagle's Global Strike)
if "selected_node" not in st.session_state:
    st.session_state.selected_node = None  # nigeria | ghana | south_africa | egypt | dubai
if "pulse_triggered" not in st.session_state:
    st.session_state.pulse_triggered = False
if "play_swat" not in st.session_state:
    st.session_state.play_swat = False
# Backwards compat
if "nigeria_selected" not in st.session_state:
    st.session_state.nigeria_selected = False

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
/* Regional pulses */
@keyframes pulse-ghana { 0% { box-shadow: 0 0 24px #C8102E; border-color: #C8102E; } 25% { box-shadow: 0 0 28px #FFD700; border-color: #FFD700; } 50% { box-shadow: 0 0 24px #008751; border-color: #008751; } 100% { box-shadow: 0 0 32px #FFD700; border-color: #FFD700; } }
@keyframes pulse-dubai { 0% { box-shadow: 0 0 24px #C8102E; border-color: #C8102E; } 33% { box-shadow: 0 0 28px #008751; border-color: #008751; } 66% { box-shadow: 0 0 28px #fff; border-color: #fff; } 100% { box-shadow: 0 0 32px #FFD700; border-color: #FFD700; } }
@keyframes pulse-south_africa { 0% { box-shadow: 0 0 20px #008751; border-color: #008751; } 20% { box-shadow: 0 0 20px #FFD700; border-color: #FFD700; } 40% { box-shadow: 0 0 20px #000; border-color: #333; } 60% { box-shadow: 0 0 20px #007749; border-color: #007749; } 80% { box-shadow: 0 0 20px #DE3831; border-color: #DE3831; } 100% { box-shadow: 0 0 32px #FFD700; border-color: #FFD700; } }
.pulse-ghana { animation: pulse-ghana 3s ease-in-out 1 forwards; border: 2px solid #FFD700; border-radius: 16px; position: relative; }
.pulse-dubai { animation: pulse-dubai 3s ease-in-out 1 forwards; border: 2px solid #FFD700; border-radius: 16px; position: relative; }
.pulse-south_africa { animation: pulse-south_africa 3s ease-in-out 1 forwards; border: 2px solid #FFD700; border-radius: 16px; position: relative; }
/* Live Eagle Engine: Sniffer hover + Talon Strike */
@keyframes eagle-hover-float { 0%, 100% { transform: translate(-50%, -80%) scale(1) rotate(-2deg); opacity: 0.95; } 50% { transform: translate(-50%, -95%) scale(1.05) rotate(2deg); opacity: 1; } }
@keyframes eagle-dive { 0% { transform: translate(-50%,-120%) scale(1.5); opacity: 0.9; } 100% { transform: translate(-50%,-50%) scale(0.7); opacity: 0.4; } }
.awc-eagle-sniffer { position: absolute; left: 50%; top: 50%; transform: translate(-50%,-80%); pointer-events: none; z-index: 10; animation: eagle-hover-float 2.2s ease-in-out infinite; filter: drop-shadow(0 0 12px rgba(255,215,0,0.6)); }
.awc-eagle-talon { position: absolute; left: 50%; top: 50%; transform: translate(-50%,-50%); pointer-events: none; z-index: 10; animation: eagle-dive 0.7s ease-out 1 forwards; filter: drop-shadow(0 0 16px rgba(255,215,0,0.8)); }
/* High-velocity typography */
h1, h2, h3, p, span, label, .stMarkdown { color: #D4AF37 !important; }
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color: #E8C547 !important; }
section[data-testid="stSidebar"] { background: linear-gradient(180deg, #001a33 0%, #002244 100%) !important; border-right: 2px solid #D4AF37; }
/* Mission Handshake: Impact Header & Sub-header */
.awc-impact-header { font-weight: 800; font-size: 1.35rem; text-align: center; line-height: 1.35; letter-spacing: 0.5px; color: #FFD700 !important; text-transform: uppercase; margin-bottom: 4px; }
.awc-sub-header { text-align: center; color: rgba(212,175,55,0.95); font-size: 0.95rem; letter-spacing: 2px; margin-top: 2px; }
/* 3D "8" zoom on entry */
@keyframes eight-zoom { 0% { transform: scale(0.3) translateZ(-80px); opacity: 0; } 60% { transform: scale(1.15) translateZ(0); opacity: 1; } 100% { transform: scale(1) translateZ(0); opacity: 1; } }
.awc-eight { font-size: 4rem; font-weight: 900; color: #FFD700; animation: eight-zoom 1.2s ease-out 1; display: inline-block; text-shadow: 0 0 30px rgba(255,215,0,0.6); }
/* Radar Blink (0.8s) on Stealth Paradigm */
@keyframes radar-blink { 0%, 100% { opacity: 1; text-shadow: 0 0 12px #FFD700; } 50% { opacity: 0.75; text-shadow: 0 0 24px #FFD700, 0 0 36px rgba(255,215,0,0.5); } }
.awc-stealth-text { animation: radar-blink 0.8s ease-in-out infinite; }
/* Prism Lens (iridescent, non-glass) for asset cards */
.awc-prism-card { background: linear-gradient(135deg, rgba(255,215,0,0.08) 0%, rgba(180,130,70,0.06) 25%, rgba(255,230,150,0.1) 50%, rgba(212,175,55,0.07) 75%, rgba(255,215,0,0.09) 100%); border: 1px solid rgba(255,215,0,0.35); border-radius: 12px; padding: 1rem; margin: 0.5rem 0; box-shadow: 0 4px 20px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.08); }
/* Vortex particle container (swirling golden vortex) */
@keyframes vortex-spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes vortex-pull { 0% { transform: scale(1) translate(0,0); opacity: 0.9; } 100% { transform: scale(0.3) translate(0,0); opacity: 0.4; } }
#awc-vortex-wrap { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; overflow: hidden; }
.awc-vortex-dot { position: absolute; width: 4px; height: 4px; background: #FFD700; border-radius: 50%; animation: vortex-pull 4s ease-in infinite, awc-float 3s ease-in-out infinite; }
/* Velocity header shimmer (legacy) */
.awc-title { font-weight: 800; font-size: 1.9rem; text-align: center; background: linear-gradient(90deg, #D4AF37, #FFE55C, #D4AF37); background-size: 200% auto; -webkit-background-clip: text; background-clip: text; color: transparent !important; animation: title-shimmer 3s linear infinite; }
@keyframes title-shimmer { 0% { background-position: 0% 50%; } 100% { background-position: 200% 50%; } }
.awc-sub { text-align: center; color: rgba(212,175,55,0.9); font-size: 0.95rem; letter-spacing: 2px; margin-top: -8px; }
/* Mind-hooking metrics */
.awc-metric-box { background: rgba(0,33,71,0.7); border: 1px solid #D4AF37; border-radius: 8px; padding: 1rem; margin: 0.5rem 0; }
.footer-awc { text-align: center; font-size: 0.8rem; color: rgba(212,175,55,0.85); margin-top: 2rem; padding: 1rem; border-top: 1px solid rgba(212,175,55,0.3); }
/* Gold Shimmer particles */
#awc-shimmer-wrap { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0; overflow: hidden; }
.awc-particle { position: absolute; width: 6px; height: 6px; background: radial-gradient(circle, #FFD700 0%, #D4AF37 60%, transparent 100%); border-radius: 50%; opacity: 0.9; animation: awc-float 5s ease-in-out infinite; }
/* Convergence: vortex dots */
.awc-vortex-dot { position: absolute; width: 4px; height: 4px; background: #FFD700; border-radius: 50%; box-shadow: 0 0 8px rgba(255,215,0,0.8); }
/* Prism Lens: iridescent asset cards (expanders) */
[data-testid="stExpander"] { border: 1px solid rgba(255,215,0,0.35) !important; border-radius: 12px !important; background: linear-gradient(135deg, rgba(255,215,0,0.08) 0%, rgba(180,130,70,0.06) 50%, rgba(255,230,150,0.1) 100%) !important; box-shadow: 0 4px 20px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.06) !important; }
/* Determinant pop-up: Sovereign Glass + instrumentation flash */
.awc-determinant-popup { position: relative; background: linear-gradient(135deg, rgba(0,26,51,0.95) 0%, rgba(0,33,71,0.98) 100%); border: 2px solid #FFD700; border-radius: 12px; padding: 1rem 1.25rem; margin: 0.75rem 0; font-weight: 700; color: #FFD700; text-align: center; animation: popup-reveal 0.5s ease-out, instrument-flash 2s ease-in-out 2; backdrop-filter: blur(8px); box-shadow: inset 0 0 40px rgba(255,215,0,0.08), 0 0 32px rgba(255,215,0,0.2); }
@keyframes popup-reveal { 0% { transform: scale(0.9); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
@keyframes instrument-flash { 0%, 100% { box-shadow: 0 0 24px rgba(255,215,0,0.3); } 50% { box-shadow: 0 0 48px rgba(255,215,0,0.8), 0 0 72px rgba(0,255,136,0.4); } }
@keyframes sovereign-glass-shimmer { 0%, 100% { border-color: #FFD700; box-shadow: inset 0 0 40px rgba(255,215,0,0.08), 0 0 24px rgba(255,215,0,0.25); } 50% { border-color: #E8C547; box-shadow: inset 0 0 50px rgba(255,215,0,0.12), 0 0 40px rgba(255,215,0,0.4); } }
.awc-sovereign-glass-window { animation: sovereign-glass-shimmer 2.5s ease-in-out infinite; }
.awc-determinant-wordpop { font-size: 1rem; letter-spacing: 2px; color: #00ff88; margin: 0.5rem 0; text-shadow: 0 0 12px rgba(0,255,136,0.7); }
.awc-opportunity-badge { font-size: 1.1rem; font-weight: 800; color: #FFD700; margin-bottom: 4px; }
/* Lab panel + digital counter instrumentation flash */
.awc-lab-panel { background: rgba(0,26,51,0.9); border: 1px solid rgba(255,215,0,0.4); border-radius: 8px; padding: 1rem; font-family: monospace; animation: panel-flash 3s ease-in-out 1; }
@keyframes panel-flash { 0% { box-shadow: 0 0 12px rgba(255,215,0,0.2); } 30% { box-shadow: 0 0 32px rgba(255,215,0,0.5), inset 0 0 20px rgba(0,255,136,0.1); } 100% { box-shadow: 0 0 16px rgba(255,215,0,0.3); } }
@keyframes counter-flash { 0%, 100% { text-shadow: 0 0 8px rgba(0,255,136,0.6); opacity: 1; } 50% { text-shadow: 0 0 20px #00ff88, 0 0 30px rgba(255,215,0,0.8); opacity: 1; } }
/* 5km: Golden radar sweep when $10B+ opportunity (before strike) */
@keyframes radar-sweep { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.awc-radar-sweep::before { content: ''; position: absolute; inset: 0; border-radius: inherit; pointer-events: none; z-index: 5; background: conic-gradient(from 0deg, transparent 0deg 30deg, rgba(255,215,0,0.35) 35deg, transparent 60deg); animation: radar-sweep 1.5s linear 1; }
/* Final handshake: Eagle in Gap box — flap, head turn, eye contact + CTA */
@keyframes eagle-flap { 0%, 100% { transform: scaleY(1) rotate(-2deg); } 50% { transform: scaleY(1.08) rotate(2deg); } }
@keyframes eagle-head-turn { 0%, 80% { transform: rotate(0deg); } 85% { transform: rotate(-8deg); } 90% { transform: rotate(5deg); } 95%, 100% { transform: rotate(0deg); } }
.awc-final-eagle { display: inline-block; animation: eagle-flap 0.6s ease-in-out infinite; }
.awc-final-eagle .eagle-head { transform-origin: 50% 30%; animation: eagle-head-turn 3s ease-in-out 1; }
.awc-cta-secured { font-weight: 900; font-size: 1.1rem; color: #FFD700; text-align: center; margin-top: 8px; letter-spacing: 1px; text-shadow: 0 0 16px rgba(255,215,0,0.8); animation: instrument-flash 2.5s ease-in-out 2; }
/* Sovereign Glass lab: oscilloscope + digital counters */
.awc-lab-panel-inner { background: rgba(0,26,51,0.9); border: 1px solid rgba(255,215,0,0.4); border-radius: 8px; padding: 1rem; font-family: monospace; }
.awc-oscilloscope { height: 48px; background: linear-gradient(180deg, transparent 45%, rgba(255,215,0,0.15) 50%, transparent 55%); border-radius: 4px; position: relative; overflow: hidden; }
.awc-oscilloscope::before { content: ''; position: absolute; left: 0; top: 50%; width: 200%; height: 2px; background: repeating-linear-gradient(90deg, transparent, transparent 8px, rgba(255,215,0,0.6) 8px, rgba(255,215,0,0.6) 10px); animation: scope-wave 2s linear infinite; }
@keyframes scope-wave { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
.awc-digital-counter { font-size: 1.25rem; font-weight: 700; color: #00ff88; text-shadow: 0 0 8px rgba(0,255,136,0.6); letter-spacing: 2px; animation: counter-flash 2s ease-in-out 2; }
</style>
<div id="awc-shimmer-wrap">""" + particles_html + """</div>
""", unsafe_allow_html=True)

# --- Mission Handshake: Impact Header & Sub-header ---
st.markdown(
    '<p class="awc-impact-header">ARCHITECTING NATIONAL ASSET REVITALIZATION: FROM NIGERIA & AFRICA TO THE GLOBAL SOUTH</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="awc-sub-header">Galadiman Ruwa Center (GCSLC) LTD/GTE | Chairman & Founder: Dr. Sa\'ad Jaafaru</p>',
    unsafe_allow_html=True,
)
# --- Advanced Animation: "8" zoom + Radar Blink "Stealth Paradigm" + Convergence ---
st.markdown(
    '<div style="text-align: center; margin: 1rem 0;">'
    '<span class="awc-eight">8</span> '
    '<span class="awc-stealth-text" style="font-size: 1.25rem; font-weight: 700; color: #FFD700;">R Stealth Paradigm</span> '
    '<span style="color: rgba(212,175,55,0.9); font-size: 1rem;">Convergence</span>'
    '</div>',
    unsafe_allow_html=True,
)
st.markdown("---")

# --- Sidebar: Continental Nodes + Eagle's Talon (play_swat on every strike) ---
with st.sidebar:
    st.write("### Continental Nodes")
    if st.button("🇳🇬 Nigeria", key="btn_nigeria"):
        st.session_state.selected_node = "nigeria"
        st.session_state.nigeria_selected = True
        st.session_state.pulse_triggered = True
        st.session_state.play_swat = True
        st.rerun()
    if st.button("🇬🇭 Ghana", key="btn_ghana"):
        st.session_state.selected_node = "ghana"
        st.session_state.pulse_triggered = True
        st.session_state.play_swat = True
        st.rerun()
    if st.button("🇿🇦 South Africa", key="btn_south_africa"):
        st.session_state.selected_node = "south_africa"
        st.session_state.pulse_triggered = True
        st.session_state.play_swat = True
        st.rerun()
    if st.button("🇪🇬 Egypt", key="btn_egypt"):
        st.session_state.selected_node = "egypt"
        st.session_state.pulse_triggered = True
        st.session_state.play_swat = True
        st.rerun()
    if st.button("🇦🇪 Dubai (UAE)", key="btn_dubai"):
        st.session_state.selected_node = "dubai"
        st.session_state.pulse_triggered = True
        st.session_state.play_swat = True
        st.rerun()
    if st.button("Clear selection", key="btn_clear"):
        st.session_state.selected_node = None
        st.session_state.nigeria_selected = False
        st.session_state.pulse_triggered = False
        st.rerun()
    st.caption("Eagle's Talon: any node → map centers on country + play_swat (180 Hz → 40 Hz) on strike.")
    st.markdown("---")
    # Foundational Intelligence Layer: Investor Manifesto + Doctor vs. Pharmacist (hardcoded)
    st.write("### Foundational Intelligence")
    with st.expander("**Investor Manifesto**", expanded=False):
        st.markdown(continental_logic.INVESTOR_MANIFESTO)
    with st.expander("**Doctor vs. Pharmacist**", expanded=False):
        st.markdown(continental_logic.DOCTOR_VS_PHARMACIST)
    # Strategic Doctrine: show when CEO interacts (i.e. when $10B+ node selected — eagle has struck)
    _ceo_interaction = bool(st.session_state.selected_node and continental_logic.is_10b_plus_opportunity(st.session_state.selected_node))
    with st.expander("**Strategic Doctrine (CEO Brief)**", expanded=_ceo_interaction):
        st.markdown(continental_logic.STRATEGIC_DOCTRINE_CEO)
        if _ceo_interaction:
            st.caption("AI models are moribund without physical asset grounding. This node secures the anchor.")
    st.markdown("---")
    st.write("### D3-Alpha Cross-Border (8R Paradigm)")
    st.markdown(
        "**Nigeria SSMVs ↔ Ghana Gold**  \n"
        "Refine (D1): High-purity gold corridors in Ghana feed Nigeria SSMV mineral chains.  \n"
        "Reset (D2): Shared SPV→SSMV structures across West African nodes."
    )
    st.markdown(
        "**Nigeria SSMVs ↔ Dubai logistical hubs**  \n"
        "Research (D3): Dubai hubs align with Nigeria Rare Earth supply chains.  \n"
        "Retain (D8): Sovereign retention flows through UAE strategic partner nodes."
    )
    st.markdown("---")
    # Silicon Valley Strategic Intent — auto-open when $10B+ gap revealed
    _expanded_silicon = bool(st.session_state.selected_node and continental_logic.is_10b_plus_opportunity(st.session_state.selected_node))
    with st.expander("**Silicon Valley Strategic Intent**", expanded=_expanded_silicon):
        st.markdown(continental_logic.ENERGY_MINERAL_SHIELD)
        st.markdown("---")
        st.markdown(continental_logic.SANTIAGO_COMPLIANCE)
    st.markdown("---")

# --- Sovereign Rationale: Big Tech Handshake Manifesto (linked to Natural Gas, Gold, Rare Earth) ---
with st.expander("**Sovereign Rationale — Big Tech Handshake Manifesto**", expanded=False):
    st.markdown(continental_logic.BIG_TECH_HANDSHAKE_MANIFESTO)
    st.caption("Linked SSMV corridors: **" + "**, **".join(continental_logic.SSMV_CORRIDORS_MANIFESTO) + "**")

# --- Map container: Glassmorphism + Regional Pulse + Eagle's Talon dive ---
st.write("### The Sovereign Glass — Continental View")
st.caption("**GCSLC Sovereign Diagnostic** | **Live Eagle Engine:** Sniffer hovers over map → on node click, high-velocity **Talon Strike** with **play_swat** 180 Hz audio sync. ($10B+ nodes: golden radar sweep.)")
map_container_class = "awc-map-glass"
if st.session_state.pulse_triggered and st.session_state.selected_node:
    if st.session_state.selected_node == "nigeria":
        map_container_class += " sovereign-pulse-active"
    elif st.session_state.selected_node == "ghana":
        map_container_class += " pulse-ghana"
    elif st.session_state.selected_node == "dubai":
        map_container_class += " pulse-dubai"
    elif st.session_state.selected_node == "south_africa":
        map_container_class += " pulse-south_africa"
    else:
        map_container_class += " sovereign-pulse-active"  # Egypt / fallback
# 5km: Golden radar sweep when $10B+ opportunity (before strike)
if st.session_state.selected_node and continental_logic.is_10b_plus_opportunity(st.session_state.selected_node):
    map_container_class += " awc-radar-sweep"
deck = africa_map.build_africa_deck(selected_node=st.session_state.selected_node, opacity=0.85)
# Live Eagle Engine: high-fidelity Sniffer (hover) → Talon Strike (on node click, 180 Hz play_swat)
EAGLE_SNIFFER_SVG = '''<svg class="awc-eagle-sniffer" width="72" height="52" viewBox="0 0 72 52" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M36 4 L40 14 L36 12 L32 14 Z" fill="#FFD700" stroke="#B8860B" stroke-width="0.8"/>
  <path d="M36 48 L32 36 L36 38 L40 36 Z" fill="#FFD700" stroke="#B8860B" stroke-width="0.8"/>
  <path d="M12 26 L26 20 L22 26 L26 32 Z" fill="#FFD700" stroke="#B8860B" stroke-width="0.8"/>
  <path d="M60 26 L46 32 L50 26 L46 20 Z" fill="#FFD700" stroke="#B8860B" stroke-width="0.8"/>
  <ellipse cx="36" cy="26" rx="14" ry="10" fill="#FFD700" stroke="#B8860B" stroke-width="1"/>
  <path d="M28 18 Q36 12 44 18" stroke="#B8860B" stroke-width="1" fill="none" stroke-linecap="round"/>
  <path d="M30 22 Q36 17 42 22" stroke="#C9A227" stroke-width="0.7" fill="none" opacity="0.9"/>
  <circle cx="32" cy="22" r="2.5" fill="#1a1a1a"/><circle cx="40" cy="22" r="2.5" fill="#1a1a1a"/>
  <path d="M34 28 L36 36 L38 28" stroke="#B8860B" stroke-width="0.6" fill="none"/>
</svg>'''
EAGLE_TALON_SVG = '''<svg class="awc-eagle-talon" width="72" height="52" viewBox="0 0 72 52" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M36 4 L40 14 L36 12 L32 14 Z" fill="#FFD700" stroke="#B8860B" stroke-width="0.8"/>
  <path d="M36 48 L32 36 L36 38 L40 36 Z" fill="#FFD700" stroke="#B8860B" stroke-width="0.8"/>
  <path d="M12 26 L26 20 L22 26 L26 32 Z" fill="#FFD700" stroke="#B8860B" stroke-width="0.8"/>
  <path d="M60 26 L46 32 L50 26 L46 20 Z" fill="#FFD700" stroke="#B8860B" stroke-width="0.8"/>
  <ellipse cx="36" cy="26" rx="14" ry="10" fill="#FFD700" stroke="#B8860B" stroke-width="1"/>
  <path d="M28 18 Q36 12 44 18" stroke="#B8860B" stroke-width="1" fill="none" stroke-linecap="round"/>
  <circle cx="32" cy="22" r="2.5" fill="#1a1a1a"/><circle cx="40" cy="22" r="2.5" fill="#1a1a1a"/>
  <path d="M34 28 L36 36 L38 28" stroke="#B8860B" stroke-width="0.6" fill="none"/>
</svg>'''
show_talon_strike = st.session_state.pulse_triggered and st.session_state.selected_node
show_sniffer_hover = deck and not show_talon_strike
eagle_html = EAGLE_TALON_SVG if show_talon_strike else (EAGLE_SNIFFER_SVG if show_sniffer_hover else "")
if deck:
    st.markdown(
        f'<div class="{map_container_class}" style="padding: 8px; position: relative;">{eagle_html}',
        unsafe_allow_html=True,
    )
    st.pydeck_chart(deck, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Map engine unavailable. Install pydeck and pandas.")
if st.session_state.pulse_triggered and st.session_state.selected_node:
    st.session_state.pulse_triggered = False

# --- Scintillating Data Reveal: Sovereign Glass window + 8R Determinant Word-Pop ---
if st.session_state.selected_node:
    reveal_text = continental_logic.get_determinant_reveal(st.session_state.selected_node)
    node_name = africa_map.CONTINENTAL_NODES.get(st.session_state.selected_node, {}).get("name", st.session_state.selected_node)
    gap = continental_logic.get_market_gap_for_node(st.session_state.selected_node)
    gap_b = gap["gap_b_usd"]
    st.markdown(
        f'<div class="awc-determinant-popup awc-sovereign-glass-window">'
        f'<p class="awc-opportunity-badge">Real-time market gaps: <span class="awc-digital-counter">${gap_b:.0f}B</span> Opportunity identified</p>'
        f'<p class="awc-determinant-wordpop">D1: Refine | D2: Reset | D3: Research</p>'
        f'<span style="font-size: 0.85rem; opacity: 0.9;">{node_name} — 8R Scientific Validation (Sovereign)</span><br/>'
        f'{reveal_text}'
        f'</div>',
        unsafe_allow_html=True,
    )
    # --- Market Gap Analysis (Sovereign Glass) + Scientific Reveal + Final Handshake (gap already from reveal) ---
    gap = continental_logic.get_market_gap_for_node(st.session_state.selected_node)  # reuse for lab panels
    st.write("**Market Gap Analysis** — Global Opportunity (Demand vs Supply)")
    st.markdown(
        f'<p style="color: rgba(212,175,55,0.95); font-size: 0.95rem; margin-bottom: 8px;">'
        f'<strong>Scientific Reveal:</strong> Demand: <span class="awc-digital-counter">{gap["demand_pct"]}%</span> vs Supply: <span class="awc-digital-counter">{gap["supply_pct"]}%</span> '
        f'— <strong>{gap["asset"]}</strong>. Anchored Valuation: <strong>$170.85B</strong> Central Empirical Metric.</p>',
        unsafe_allow_html=True,
    )
    lab1, lab2 = st.columns(2)
    with lab1:
        st.markdown(
            f'<div class="awc-lab-panel">'
            f'<div class="awc-oscilloscope"></div>'
            f'<p style="color: #D4AF37; margin-top: 8px;">Demand: <span class="awc-digital-counter">{gap["demand_pct"]}%</span></p>'
            f'<p style="color: #D4AF37;">Supply: <span class="awc-digital-counter">{gap["supply_pct"]}%</span></p>'
            f'<p style="color: #FFD700;">Asset: {gap["asset"]}</p>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with lab2:
        st.markdown(
            f'<div class="awc-lab-panel">'
            f'<div class="awc-oscilloscope"></div>'
            f'<p style="color: #D4AF37; margin-top: 8px;">Gap: <span class="awc-digital-counter">${gap["gap_b_usd"]:.1f}B</span></p>'
            f'<p style="color: #00ff88;">Valuation anchor: <span class="awc-digital-counter">$170.85B</span></p>'
            f'<p style="color: rgba(212,175,55,0.9); font-size: 0.85rem;">Central empirical metric — 8R Sovereign</p>'
            f'</div>',
            unsafe_allow_html=True,
        )
    # Eagle's Final Handshake: after Talon Strike — eagle locks gaze (direct eye-contact), CTA
    st.components.v1.html("""
    <div id="awc-eagle-gap-box" class="awc-lab-panel" style="margin-top: 12px; text-align: center; padding: 16px;">
      <style>
        @keyframes feather-flap { 0%, 100% { transform: scaleY(1) rotate(-3deg); } 50% { transform: scaleY(1.12) rotate(3deg); } }
        @keyframes head-turn { 0%, 70% { transform: rotate(0deg); } 78% { transform: rotate(-10deg); } 85% { transform: rotate(8deg); } 92%, 100% { transform: rotate(0deg); } }
        .awc-eagle-wrap { display: inline-block; animation: feather-flap 0.55s ease-in-out infinite; }
        .awc-eagle-wrap svg { display: block; }
        .awc-eagle-wrap .eagle-head { transform-origin: 50% 35%; animation: head-turn 2.5s ease-in-out 1; }
        .awc-eagle-pupil { transition: transform 0.15s ease-out; }
        .awc-directive-label { font-size: 0.75rem; color: rgba(212,175,55,0.9); letter-spacing: 1.5px; margin-top: 8px; text-transform: uppercase; }
        .awc-cta-line { font-weight: 900; font-size: 1.25rem; color: #FFD700; margin-top: 10px; letter-spacing: 2px; text-shadow: 0 0 24px rgba(255,215,0,0.9); animation: cta-pulse 2s ease-in-out infinite; }
        @keyframes cta-pulse { 0%, 100% { opacity: 1; text-shadow: 0 0 24px rgba(255,215,0,0.9); } 50% { opacity: 0.95; text-shadow: 0 0 32px rgba(255,215,0,1); } }
      </style>
      <div class="awc-eagle-wrap">
        <svg class="eagle-head" id="awc-eagle-svg" width="80" height="56" viewBox="0 0 80 56" fill="none" xmlns="http://www.w3.org/2000/svg">
          <ellipse cx="40" cy="34" rx="24" ry="16" fill="#FFD700" stroke="#B8860B" stroke-width="1.2"/>
          <path class="feather" d="M18 24 Q40 14 62 24" stroke="#B8860B" stroke-width="2" fill="none" stroke-linecap="round"/>
          <path class="feather" d="M22 28 Q40 20 58 28" stroke="#C9A227" stroke-width="1.2" fill="none" opacity="0.9"/>
          <g id="awc-eagle-eyes">
            <circle cx="34" cy="28" r="4" fill="#1a1a1a"/><circle cx="46" cy="28" r="4" fill="#1a1a1a"/>
            <circle class="awc-eagle-pupil" id="pupil-l" cx="34" cy="28" r="1.2" fill="#fff"/><circle class="awc-eagle-pupil" id="pupil-r" cx="46" cy="28" r="1.2" fill="#fff"/>
          </g>
          <path d="M40 40 L37 50 L40 47 L43 50 Z" fill="#FFD700" stroke="#B8860B" stroke-width="0.8"/>
        </svg>
      </div>
      <p class="awc-directive-label">Direct eye-contact directive — eagle locked on you</p>
      <p class="awc-cta-line" id="awc-eagle-message">GCSLC SECURED THE ANCHOR. GET TO WORK.</p>
    </div>
    <script>
    (function() {
      var box = document.getElementById('awc-eagle-gap-box');
      if (!box) return;
      var svg = document.getElementById('awc-eagle-svg');
      var pl = document.getElementById('pupil-l');
      var pr = document.getElementById('pupil-r');
      var msgEl = document.getElementById('awc-eagle-message');
      var messages = [
        'GCSLC SECURED THE ANCHOR. GET TO WORK.',
        'RETAINING WEALTH. PROTECTING SOVEREIGNTY.',
        '8R: THE DOCTOR\'S DIAGNOSTIC FOR A NEW AFRICA.'
      ];
      var idx = 0;
      if (msgEl) {
        setInterval(function() {
          idx = (idx + 1) % messages.length;
          msgEl.textContent = messages[idx];
        }, 4500);
      }
      function setGaze(x, y) {
        if (!svg) return;
        var r = svg.getBoundingClientRect();
        var cx = r.left + r.width / 2, cy = r.top + r.height * 0.5;
        var dx = (x - cx) / r.width * 3, dy = (y - cy) / r.height * 3;
        dx = Math.max(-2, Math.min(2, dx)); dy = Math.max(-2, Math.min(2, dy));
        if (pl) pl.setAttribute('transform', 'translate(' + dx + ',' + dy + ')');
        if (pr) pr.setAttribute('transform', 'translate(' + dx + ',' + dy + ')');
      }
      setTimeout(function() {
        document.addEventListener('mousemove', function(e) { setGaze(e.clientX, e.clientY); });
        setGaze(window.innerWidth / 2, window.innerHeight / 2);
      }, 800);
    })();
    </script>
    """, height=240)

st.caption("Continental nodes: Nigeria, Ghana, South Africa, Egypt. Strategic Partner: Dubai (UAE). Select a node to center map and trigger Eagle's Talon + play_swat.")

# --- Universal Sovereign Impact Radar: Security & Social Well-being toggles ---
st.markdown("---")
st.write("### Universal Sovereign Impact Radar")
st.caption("How the **$170.85B** valuation anchor reduces poverty and increases regional stability.")
col_sec, col_soc = st.columns(2)
with col_sec:
    show_security_impact = st.checkbox("National Security Impact", value=False, key="radar_security")
with col_soc:
    show_social_wellbeing = st.checkbox("Social Well-being Index", value=False, key="radar_social")
if show_security_impact:
    st.write("**National Security Impact** — $170.85B anchor → regional stability")
    sec_heat = continental_logic.get_national_security_impact_heatmap()
    st.dataframe(
        [{"Region": r["region"], "Indicator": r["indicator"], "Before anchor": r["before_anchor"], "After anchor": r["after_anchor"], "Δ Stability": r["stability_delta"]} for r in sec_heat],
        use_container_width=True,
        hide_index=True,
    )
    st.caption("Higher scores = more stability. The anchor increases sovereign retention and reduces resource conflict.")
if show_social_wellbeing:
    st.write("**Social Well-being Index** — $170.85B anchor → poverty reduction")
    soc_heat = continental_logic.get_social_wellbeing_index_heatmap()
    st.dataframe(
        [{"Dimension": d["dimension"], "Baseline (%)": d["baseline_pct"], "Post-anchor (%)": d["post_anchor_pct"], "Change": d["reduction"]} for d in soc_heat],
        use_container_width=True,
        hide_index=True,
    )
    st.caption("Poverty headcount drops; employment and energy access rise under 8R sovereign corridors.")

# --- The Wise Men: Institutional Partner nodes (Dangote / BUA / Zenith / GTCO) ---
st.markdown("---")
st.write("### The Wise Men — Institutional Partners")
st.caption("Nigeria's industrial and financial giants: how the **8R Strike** resuscitates the assets they bid on.")
for partner in continental_logic.get_institutional_partners():
    with st.expander(f"**{partner['name']}** — {partner['sector']}"):
        st.markdown("**Assets bid on:** " + "; ".join(f"*{a}*" for a in partner["assets_bid"]))
        st.markdown("**8R Resuscitation:** " + partner["8r_resuscitation"])

# --- Global Sector Intelligence: Atoms / Bits / Capital ---
st.markdown("---")
st.write("### Global Sector Intelligence")
st.caption("**Atoms** (Exxon/Total/Maersk) · **Bits** (Samsung/MTN/Airtel) · **Capital** (JPMorgan/Citibank)")
atoms = continental_logic.get_atoms_node()
bits = continental_logic.get_bits_node()
capital = continental_logic.get_capital_node()

with st.expander("**Atoms** — Exxon / Total / Maersk", expanded=True):
    st.write("**Supply chain gap: LNG & Rare Earths**")
    for g in atoms["supply_chain_gaps"]:
        st.markdown(
            f"- **{g['commodity']}**: Demand {g['demand_pct']}% vs Supply {g['supply_pct']}% · Gap ${g['gap_b_usd']:.0f}B — *{g['corridor']}*"
        )
    st.markdown(
        f'<p style="color: #00ff88; font-weight: 700; margin-top: 8px;">'
        f'<span class="awc-digital-counter">D1: Refine & D7: Re-engineer applied to Exxon 2030 Plan.</span></p>',
        unsafe_allow_html=True,
    )

with st.expander("**Bits** — Samsung / MTN / Airtel"):
    st.write("**2% global data center capacity gap in Africa**")
    st.metric("Africa share of global data center capacity", f"{bits['data_center_capacity_gap_pct']}%", help="Gap vs global share")
    st.markdown("**NGECC ↔ MTN AI-RAN:** " + bits["narrative"])

with st.expander("**Capital** — JPMorgan / Citibank"):
    st.write(f"**{capital['initiative_name']}** — alignment with sovereign corridors")
    st.metric("Initiative scale", f"$ {capital['initiative_value_usd_trillion']} Trillion", help="Security & Resiliency Initiative")
    st.markdown(capital["alignment_narrative"])
    # Visual: Eagle sniffs the bank node → Secured Asset
    st.markdown(
        '''
        <div class="awc-lab-panel" style="margin-top: 12px; text-align: center; padding: 12px;">
          <style>
            .awc-eagle-sniff-icon { display: inline-block; animation: sniff-float 2s ease-in-out infinite; filter: drop-shadow(0 0 8px rgba(255,215,0,0.6)); }
            @keyframes sniff-float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-4px); } }
            .awc-secured-badge { display: inline-block; margin-top: 8px; padding: 6px 14px; border: 2px solid #00ff88; border-radius: 8px; font-weight: 800; color: #00ff88; font-size: 0.9rem; letter-spacing: 1px; text-shadow: 0 0 12px rgba(0,255,136,0.6); animation: badge-glow 2s ease-in-out infinite; }
            @keyframes badge-glow { 0%, 100% { box-shadow: 0 0 12px rgba(0,255,136,0.3); } 50% { box-shadow: 0 0 24px rgba(0,255,136,0.6); } }
          </style>
          <p style="color: #D4AF37; font-size: 0.85rem; margin-bottom: 6px;">Eagle sniffs the bank node</p>
          <div class="awc-eagle-sniff-icon">
            <svg width="40" height="28" viewBox="0 0 56 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <ellipse cx="28" cy="20" rx="12" ry="8" fill="#FFD700" stroke="#B8860B" stroke-width="0.8"/>
              <path d="M18 16 L28 12 L38 16" stroke="#B8860B" stroke-width="0.8" fill="none"/>
              <circle cx="24" cy="18" r="1.5" fill="#1a1a1a"/><circle cx="32" cy="18" r="1.5" fill="#1a1a1a"/>
            </svg>
          </div>
          <p style="margin-top: 4px; font-size: 0.8rem; color: rgba(212,175,55,0.9);">↓</p>
          <span class="awc-secured-badge">SECURED ASSET</span>
        </div>
        ''',
        unsafe_allow_html=True,
    )

# --- Triple-D3: GCSLC Sovereign Diagnostic | 8R Scientific Analysis ---
st.markdown("---")
st.write("### GCSLC Sovereign Diagnostic — Triple-D3 Research (8R Scientific Analysis)")
d3a, d3b, d3c = st.tabs(["D3-Alpha (Geopolitical)", "D3-Beta (Temporal)", "D3-Gamma (Security)"])
with d3a:
    st.write("**Global Tech Alignment** — Nigeria Rare Earths → Big Tech supply chains")
    tech_align = continental_logic.get_global_tech_alignment()
    st.dataframe(
        [{"Nigeria Asset": t["nigeria_asset"], "Elements": t["elements"], "Big Tech": t["big_tech"], "Use Case": t["use_case"]} for t in tech_align],
        use_container_width=True,
        hide_index=True,
    )
with d3b:
    st.write("**Wealth Retention Timeline** — $170.85B unlock cycle (2026–2050)")
    year_beta = st.slider("Year", 2026, 2050, 2035, key="timeline_year")
    yearly_b = continental_logic.get_wealth_retention_timeline(year_beta)
    cumulative_b = continental_logic.get_timeline_cumulative(year_beta)
    st.metric("Unlock in selected year ($B)", f"${yearly_b:.2f}B")
    st.metric("Cumulative unlock by end of year ($B)", f"${cumulative_b:.2f}B")
    st.caption(f"Total cycle: ${continental_logic.WEALTH_UNLOCK_TOTAL_B}B over 2026–2050.")
with d3c:
    st.write("**Risk Defense Heatmap** — 8R Paradigm protection vs market volatility")
    heatmap = continental_logic.get_risk_defense_heatmap()
    st.dataframe(
        [{"Determinant": r["determinant"], "Volatility Risk": r["volatility_risk"], "Defense Score": r["defense_score"]} for r in heatmap],
        use_container_width=True,
        hide_index=True,
    )
    st.caption("Defense Score: 0–100. Higher = stronger 8R protection against this risk.")

# --- Build success: Eagle's Talon audio (play_swat 180 Hz → 40 Hz) ---
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

# --- 8R Logical Engine: Continental logic output (purely sovereign; no corporate/SEC branding) ---
st.markdown("---")
st.write("### 8R Determinants — Nigeria Assets → Digital SSMVs")
st.markdown("**Central empirical metric:** **$170.85B** valuation anchor (8R Scientific Validation).")
summary = continental_logic.get_convergence_summary()
st.caption(f"AWC Nigeria: Minerals (Gold, Bauxite, Iron Ore, Lead-Zinc), Gems (Sapphire, Tourmaline, Aquamarine, Emerald), Energy (Oil, Natural Gas, NGECC). D1: Refine (high-purity corridors), D2: Reset (SPV→SSMV), D3: Research (rare earth coords). Wealth Retention: {summary['wealth_retention_lock_pct']}%.")

cols = st.columns(4)
for i, d in enumerate(continental_logic.DETERMINANTS_8R[:4]):
    cols[i % 4].metric(d.split(": ")[0], d.split(": ")[1] if ": " in d else d)

st.write("#### Digital SSMVs (Special Strategic Mission Vehicles) — *Prism Lens asset cards; mineral/gem data converges into unified SSMV nodes*")
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
st.markdown('<p class="footer-awc">© 2026 GCSLC. All Rights Reserved.</p>', unsafe_allow_html=True)
