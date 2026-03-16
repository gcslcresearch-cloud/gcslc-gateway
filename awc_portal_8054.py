"""
African Wealth Cloud (AWC) Portal — Port 8054 (standalone entity)
The Eagle flies here. Sovereign Cloud interface: Deep Navy, Gold Shimmer, 8R Convergence, Nigeria Sovereign Pulse.
Sovereign Glass continental view + AI-Compute metrics (RealTimeEngine: $50.1M, 1,203 MW, 9.6×).

User Profile: Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau)
Entity: Galadiman Ruwa Center (GCSLC) LTD/GTE.
© 2026 Galadiman Ruwa Center (GCSLC) LTD/GTE.
Sannu a hankali.
"""

import os
import sys
import urllib.parse
import importlib.util
import math
import time
from datetime import datetime

import streamlit as st
import warnings

try:
    from d8_logic import get_d3_liquid_wl_west_africa, get_d3_cassava_2026_nigerian_infra
except ImportError:
    get_d3_liquid_wl_west_africa = None
    get_d3_cassava_2026_nigerian_infra = None

# 2026 engine standard: full-width elements use width="stretch" (replaces deprecated use_container_width=True)
WIDTH_2026 = "stretch"

# Suppress deprecation warnings from dependencies to avoid "Temporary Error" / warning tab in browser
warnings.filterwarnings("ignore", category=DeprecationWarning, module="streamlit")
warnings.filterwarnings("ignore", message=".*use_container_width.*")

# Load African_Gateway modules (folder name has a dot; use file path)
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

# D8 IP Lockdown: only current Abuja IP sees clear data; others get 14px blur + Unauthorized WL Access
def _is_abuja_ip():
    allowed = [x.strip() for x in os.environ.get("GCSLC_ABUJA_IPS", "127.0.0.1,::1").split(",") if x.strip()]
    ctx = getattr(st, "context", None)
    client_ip = (getattr(ctx, "ip_address", None) or "").strip()
    return client_ip in allowed

# D7: Cache WL and friction so they compute once per 60s (thermal relief)
@st.cache_data(ttl=60)
def _cached_wl_velocity():
    _t = time.time() % 100
    return 9.6 * (1 + 0.15 * math.sin(_t * 0.2))

@st.cache_data(ttl=60)
def _cached_friction():
    _mineral_delay = max(1, int(time.time() / 30) % 18 + 1)
    friction_mult = 9.6 * (1 + 0.08 * (_mineral_delay ** 0.7))
    return friction_mult, _mineral_delay

# AWC Nodal: 1,203 MW (13-state) + 9.6× wealth multiplier + $50.1M monthly revenue (GEC-COAL-BASE-13 aligned)
MONTHLY_REVENUE_M = 50.1
WEALTH_MULTIPLIER_9_6 = 9.6
TOTAL_POWER_MW_S24 = 1203
REALTIME_ENGINE_INTERVAL_SEC = int(os.environ.get("GCSLC_AWC_REALTIME_INTERVAL_SEC", "60"))
CAC_AV_CODE = "176917792057"
CHAIRMAN_LOCK = "Dr. Sa'ad Jaafaru"

# Talon Lock: Apex Eagle asset path — African_Gateway/assets/ (fallback to inline SVG if missing)
EAGLE_ASSET_PATH = os.path.join(_GATEWAY, "assets", "apex_eagle.svg")
APEX_EAGLE_INLINE_SVG = '''<svg class="awc-apex-eagle-header" width="48" height="34" viewBox="0 0 56 40" fill="none" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="28" cy="20" rx="14" ry="10" fill="#FFD700" stroke="#B8860B" stroke-width="1"/>
  <path d="M18 16 L28 12 L38 16" stroke="#B8860B" stroke-width="1" fill="none"/>
  <path d="M20 22 Q28 18 36 22" stroke="#C9A227" stroke-width="0.7" fill="none" opacity="0.9"/>
  <circle cx="24" cy="18" r="2" fill="#1a1a1a"/><circle cx="32" cy="18" r="2" fill="#1a1a1a"/>
  <path d="M26 24 L28 30 L30 24" stroke="#B8860B" stroke-width="0.5" fill="none"/>
</svg>'''
def _render_apex_eagle(use_asset_path=True):
    """Render Apex Predator Eagle: from assets/ if present, else inline SVG. Explicit call for Talon Lock."""
    if use_asset_path and os.path.isfile(EAGLE_ASSET_PATH):
        try:
            st.image(EAGLE_ASSET_PATH, width=48)
            return
        except Exception:
            pass
    st.markdown(APEX_EAGLE_INLINE_SVG, unsafe_allow_html=True)


# Inline fallback when pydeck/GPU unavailable or map data missing — force manifest Sovereign Glass map
SOVEREIGN_GLASS_MAP_FALLBACK_HTML = """
<div class="awc-map-glass" style="padding: 16px; min-height: 280px; border-radius: 16px;">
  <span class="gcslc-proprietary-watermark" aria-hidden="true">Proprietary Methodology</span>
  <p style="color: #FFD700; font-weight: 700; margin-bottom: 12px;">Sovereign Glass — Continental View (inline fallback)</p>
  <p style="color: rgba(212,175,55,0.9); font-size: 0.9rem;">Nigeria · Ghana · South Africa · Egypt · Dubai (UAE)</p>
  <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px;">
    <span style="background: rgba(255,215,0,0.2); border: 1px solid #FFD700; padding: 6px 12px; border-radius: 8px; color: #FFD700;">Nigeria</span>
    <span style="background: rgba(255,215,0,0.2); border: 1px solid #FFD700; padding: 6px 12px; border-radius: 8px; color: #FFD700;">Ghana</span>
    <span style="background: rgba(255,215,0,0.2); border: 1px solid #FFD700; padding: 6px 12px; border-radius: 8px; color: #FFD700;">South Africa</span>
    <span style="background: rgba(255,215,0,0.2); border: 1px solid #FFD700; padding: 6px 12px; border-radius: 8px; color: #FFD700;">Egypt</span>
    <span style="background: rgba(255,215,0,0.2); border: 1px solid #FFD700; padding: 6px 12px; border-radius: 8px; color: #FFD700;">Dubai (UAE)</span>
  </div>
  <p style="color: rgba(212,175,55,0.7); font-size: 0.8rem; margin-top: 16px;">Select a node in the sidebar to center. PyDeck/WebGL unavailable — using inline fallback.</p>
</div>
"""

# --- Page config (must be first Streamlit call) ---
st.set_page_config(
    page_title="K-GEC Sovereign Gateway",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Hardware & Defense: @st.cache_resource so Mac remains thermally stable during 24/7/365 (single load per session)
@st.cache_resource
def _cached_awc_gateway():
    """Load African_Gateway modules once per session — thermal relief for 24/7/365 motion."""
    return (
        _load_module("awc_africa_map", os.path.join(_GATEWAY, "africa_map.py")),
        _load_module("awc_continental_logic", os.path.join(_GATEWAY, "continental_logic.py")),
    )

africa_map, continental_logic = _cached_awc_gateway()

# --- Phase 4 Fused Nodal: single source of truth for continental node + pulse ---
CONTINENTAL_NODE_IDS = ("nigeria", "ghana", "south_africa", "egypt", "dubai")
# Node → pulse CSS class (fused map; default sovereign-pulse-active for nigeria/egypt/other)
NODE_PULSE_CLASS = {
    "nigeria": "sovereign-pulse-active",
    "ghana": "pulse-ghana",
    "dubai": "pulse-dubai",
    "south_africa": "pulse-south_africa",
    "egypt": "sovereign-pulse-active",
}


def _fused_select_node(node_id: str | None):
    """Phase 4: single gate for node selection; sets all nodal state and reruns."""
    st.session_state.selected_node = node_id
    st.session_state.nigeria_selected = node_id == "nigeria"
    st.session_state.pulse_triggered = node_id is not None
    st.session_state.play_swat = node_id is not None
    st.rerun()


def _get_map_container_class(selected_node, pulse_triggered, is_10b_plus_fn):
    """Fused logic: base glass + optional pulse class + optional radar sweep."""
    out = "awc-map-glass"
    if pulse_triggered and selected_node:
        out += " " + NODE_PULSE_CLASS.get(selected_node, "sovereign-pulse-active")
    if selected_node and is_10b_plus_fn(selected_node):
        out += " awc-radar-sweep"
    return out


# Session state: Phase 4 Fused Nodal (single init block)
_defaults = {
    "selected_node": None,
    "pulse_triggered": False,
    "play_swat": False,
    "nigeria_selected": False,
    "autonomous_sniff_enabled": True,
    "autonomous_sniff_index": 0,
}
for key, val in _defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Autonomous Sniff: ?autonomous=1 → Eagle strikes next $10B+ node (Phase 4 fused state)
try:
    qp = st.query_params
    if qp.get("autonomous") == "1":
        nodes_10b = continental_logic.get_autonomous_sniff_nodes()
        if nodes_10b:
            idx = st.session_state.autonomous_sniff_index % len(nodes_10b)
            st.session_state.selected_node = nodes_10b[idx]
            st.session_state.nigeria_selected = nodes_10b[idx] == "nigeria"
            st.session_state.pulse_triggered = True
            st.session_state.play_swat = True
            st.session_state.autonomous_sniff_index = idx + 1
        try:
            del qp["autonomous"]
        except Exception:
            qp["autonomous"] = ""
        st.rerun()
except Exception:
    pass


class RealTimeEngine:
    """60s rerun loop so mobile (e.g. Wayan's S24 Ultra) gets live $50.1M / 1,203 MW / 9.6× instead of stale snapshot."""

    @staticmethod
    @st.fragment(run_every=REALTIME_ENGINE_INTERVAL_SEC)
    def run():
        ph = st.empty()
        with ph.container():
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Monthly revenue (AWC nodal)", f"${MONTHLY_REVENUE_M}M", help="D3 validated from 13 states")
            with c2:
                st.metric("Power potential", f"{TOTAL_POWER_MW_S24:,} MW", help="AI DC ready")
            with c3:
                st.metric("Wealth multiplier", f"{WEALTH_MULTIPLIER_9_6}×", help="Sovereign anchor")
            st.caption(f"Last refresh: {datetime.now().strftime('%H:%M:%S')} — RealTimeEngine 60s")


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
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Playfair+Display:wght@700&display=swap');

/* Sidebar Headings: 2pt Increase + Shimmer */
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
    font-family: 'Great Vibes', cursive !important;
    font-size: 26px !important;
    background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 3s infinite linear;
    background-size: 200% auto;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

/* MAIN HEADING: Apex Predator Eagle */
.shimmer-gold {
    font-family: 'Playfair Display', serif !important;
    font-size: 46px !important;
    text-align: center;
    background: linear-gradient(to right, #BF953F, #FBF5B7, #AA771C);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 5s infinite linear;
    background-size: 200% auto;
    font-weight: bold;
}

@keyframes shimmer {
    to { background-position: 200% center; }
}

/* TOP BANNER: K-GEC Vehicle - Higher Opacity & Shimmer */
.top-banner {
    font-family: 'Playfair Display', serif;
    font-size: 24px !important;
    color: rgba(252, 246, 186, 0.95);
    text-align: center;
    letter-spacing: 2px;
    background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 4s infinite linear;
    margin-bottom: 0px;
}

/* CHAIRMAN LOCK: The Full Title */
.chairman-lock {
    font-family: 'Great Vibes', cursive;
    font-size: 22px !important;
    text-align: center;
    color: #FCF6BA;
    margin-top: -10px;
}

/* Deep Navy background; content above particles */
.stApp, [data-testid="stAppViewContainer"] { background-color: #001a33 !important; min-height: 100vh; }
.main .block-container { background-color: transparent !important; position: relative; z-index: 1; }

/* Phase 4: Glassmorphism design tokens (4K-friendly) */
.stApp {
    --awc-glass-blur: 12px;
    --awc-glass-radius: 16px;
    --awc-glass-border: 1px solid rgba(255, 215, 0, 0.25);
    --awc-glass-bg: rgba(0, 26, 51, 0.15);
    --awc-glass-shadow: inset 0 1px 0 rgba(255,255,255,0.08);
}
/* Gold Shimmer keyframes */
@keyframes awc-float {
    0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.7; }
    25% { transform: translate(10px, -15px) scale(1.2); opacity: 1; }
    50% { transform: translate(-5px, -25px) scale(0.9); opacity: 0.9; }
    75% { transform: translate(-15px, -10px) scale(1.1); opacity: 0.85; }
}
/* Glassmorphism: Phase 4 fused — design tokens for 4K polish */
.awc-map-glass {
    background: var(--awc-glass-bg, rgba(0, 26, 51, 0.15));
    backdrop-filter: blur(var(--awc-glass-blur, 12px));
    -webkit-backdrop-filter: blur(var(--awc-glass-blur, 12px));
    border-radius: var(--awc-glass-radius, 16px);
    border: var(--awc-glass-border, 1px solid rgba(255, 215, 0, 0.25));
    box-shadow: var(--awc-glass-shadow, inset 0 1px 0 rgba(255,255,255,0.08));
    position: relative;
}
/* IP Shield: Proprietary Methodology watermark (8R Stealth Paradigm — screen-grab protection) */
.gcslc-proprietary-watermark { position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%) rotate(-22deg); font-size: 1.4rem; font-weight: 700; color: rgba(212,175,55,0.18); pointer-events: none; white-space: nowrap; letter-spacing: 0.2em; text-transform: uppercase; z-index: 2; }
/* Sovereign Stamp: persistent non-scrollable footer (CAC + Chairman Lock) */
.gcslc-sovereign-footer { position: fixed; bottom: 0; left: 0; right: 0; z-index: 999; background: linear-gradient(180deg, rgba(0,26,51,0.97) 0%, #001a33 100%); border-top: 2px solid rgba(212,175,55,0.4); padding: 0.45rem 1rem; font-size: 0.75rem; color: #D4AF37; text-align: center; }
.gcslc-sovereign-footer .cac { letter-spacing: 0.1em; opacity: 0.95; }
.gcslc-sovereign-footer .chairman { font-weight: 700; margin-top: 0.2rem; }
.main .block-container { padding-bottom: 4rem !important; }
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
.awc-vortex-dot { position: absolute; width: 4px; height: 4px; background: #FFD700; border-radius: 50%; animation: vortex-pull 8s ease-in infinite, awc-float 6s ease-in-out infinite; }
/* Velocity header shimmer (legacy) */
/* D8 Mac: static title — no shimmer animation to reduce GPU/thermal load */
.awc-title { font-weight: 800; font-size: 1.9rem; text-align: center; color: #D4AF37 !important; }
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
/* Talon Lock: Chairman & Founder credentials locked at top across all views */
.awc-header-lock { position: sticky; top: 0; z-index: 100; background: linear-gradient(180deg, #001a33 0%, rgba(0,26,51,0.98) 100%); padding-bottom: 12px; margin-bottom: 0; border-bottom: 1px solid rgba(255,215,0,0.2); }
.awc-apex-eagle-header { display: inline-block; vertical-align: middle; margin: 8px 12px 0 0; filter: drop-shadow(0 0 10px rgba(255,215,0,0.5)); animation: eagle-header-float 3s ease-in-out infinite; }
@keyframes eagle-header-float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-3px); } }
.gcslc-legal-name-shimmer { background: linear-gradient(90deg, #001a33, #D4AF37, #FFE55C, #D4AF37, #001a33); background-size: 100% auto; -webkit-background-clip: text; background-clip: text; color: #D4AF37 !important; }
#gcslc-bubble-wrap { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 998; overflow: hidden; }
/* D8 Mac: static bubble — no animation to reduce GPU load / thermal blanking */
.gcslc-bubble { position: absolute; font-size: 0.85rem; font-weight: 700; color: rgba(212,175,55,0.5); letter-spacing: 0.15em; white-space: nowrap; opacity: 0.07; }
body.gcslc-blur-defend [data-testid="stAppViewContainer"] { filter: blur(14px); transition: filter 0.25s ease; }
.gcslc-sovereign-strip-top, .gcslc-sovereign-strip-bottom { display: none; position: fixed; left: 0; right: 0; z-index: 1002; background: rgba(0,33,71,0.98); color: #D4AF37; text-align: center; padding: 0.5rem 1rem; font-size: 0.85rem; }
.gcslc-sovereign-strip-top { top: 0; border-bottom: 2px solid rgba(212,175,55,0.5); }
.gcslc-sovereign-strip-bottom { bottom: 0; border-top: 2px solid rgba(212,175,55,0.5); }
body.gcslc-blur-defend .gcslc-sovereign-strip-top, body.gcslc-blur-defend .gcslc-sovereign-strip-bottom { display: block !important; }
.gcslc-header-opportunity-pulse { animation: gcslc-gold-pulse 0.6s ease-in-out 4; }
@keyframes gcslc-gold-pulse { 0%, 100% { filter: brightness(1); box-shadow: 0 0 0 rgba(255,215,0,0); } 50% { filter: brightness(1.4); box-shadow: 0 0 24px rgba(255,215,0,0.8); } }

/* 4K display: Phase 4 Glassmorphism polish — stronger blur, larger radius, scaled typography */
@media (min-width: 2560px) {
    .stApp {
        --awc-glass-blur: 24px;
        --awc-glass-radius: 24px;
        --awc-glass-border: 2px solid rgba(255, 215, 0, 0.28);
        --awc-glass-bg: rgba(0, 26, 51, 0.12);
        --awc-glass-shadow: inset 0 2px 0 rgba(255,255,255,0.1), 0 8px 32px rgba(0,0,0,0.2);
    }
    .awc-map-glass { min-height: 360px; padding: 1.25rem; }
    .awc-determinant-popup {
        border-radius: 20px;
        backdrop-filter: blur(var(--awc-glass-blur));
        -webkit-backdrop-filter: blur(var(--awc-glass-blur));
        padding: 1.25rem 1.5rem;
    }
    [data-testid="stExpander"] {
        border-radius: 16px !important;
        border-width: 2px !important;
    }
    .shimmer-gold { font-size: clamp(42px, 2.8vw, 52px) !important; }
    .top-banner { font-size: clamp(22px, 1.4vw, 28px) !important; }
    .chairman-lock { font-size: clamp(20px, 1.3vw, 26px) !important; }
    .awc-prism-card, .awc-lab-panel { border-radius: 14px; }
}
</style>
<div id="awc-shimmer-wrap">""" + particles_html + """</div>
""", unsafe_allow_html=True)

# Bubbling GCSLC Watermark Overlay
st.markdown("""
<style>
/* Bubbling GCSLC Watermark Overlay */
.watermark {
    position: fixed;
    bottom: 10px;
    right: 10px;
    opacity: 0.15;
    z-index: 9999;
    pointer-events: none;
    font-family: serif;
    font-size: 12px;
    color: #FCF6BA;
}
@keyframes bubble {
    0% { transform: translateY(0) scale(1); opacity: 0.1; }
    50% { transform: translateY(-20px) scale(1.1); opacity: 0.3; }
    100% { transform: translateY(0) scale(1); opacity: 0.1; }
}
.bubble-unit {
    display: inline-block;
    animation: bubble 4s infinite ease-in-out;
}
</style>
<div class="watermark">
    <span class="bubble-unit">© GCSLC SOVEREIGN ASSET - DR. JAAFÀRU SA'AD</span>
</div>
""", unsafe_allow_html=True)

# --- Escapeless Cloud UI: synced header (CAC) — GE GNCO ---
st.markdown(
    '<div class="awc-header-lock" id="gcslc-header-wrap">'
    '<p class="awc-impact-header">KOMI — GENERATIVE EAGLE CLOUD: VEHICLE FOR NATIONS AND GLOBAL CONGLOMERATES</p>'
    '<p class="awc-sub-header gcslc-legal-name-shimmer">GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION LTD/GTE | CAC: 176917792057 | Chairman Lock: Dr. Sa\'ad Jaafaru</p>'
    '</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div id="gcslc-bubble-wrap" aria-hidden="true">'
    '<span class="gcslc-bubble" style="left:5%;top:15%;animation-delay:0s">PROPRIETARY 8R METHODOLOGY</span>'
    '<span class="gcslc-bubble" style="left:60%;top:25%;animation-delay:3s">CAC: 176917792057</span>'
    '<span class="gcslc-bubble" style="left:25%;top:70%;animation-delay:6s">PROPRIETARY 8R METHODOLOGY</span>'
    '<span class="gcslc-bubble" style="left:75%;top:55%;animation-delay:9s">CAC: 176917792057</span>'
    '<span class="gcslc-bubble" style="left:40%;top:40%;animation-delay:12s">PROPRIETARY 8R METHODOLOGY</span>'
    '<span class="gcslc-bubble" style="left:85%;top:80%;animation-delay:2s">CAC: 176917792057</span>'
    '</div>',
    unsafe_allow_html=True,
)
_authorized_ip_8054 = _is_abuja_ip()
st.components.v1.html("""
<script>
(function(){
  var authorizedIp = """ + ("true" if _authorized_ip_8054 else "false") + """;
  var CAC = '176917792057';
  var stripTop = document.createElement('div');
  stripTop.className = 'gcslc-sovereign-strip-top';
  stripTop.innerHTML = 'CAC Reservation: ' + CAC + ' | GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION LTD/GTE | Chairman & Founder: Dr. Sa\\'ad Jaafaru';
  document.body.appendChild(stripTop);
  var stripBottom = document.createElement('div');
  stripBottom.className = 'gcslc-sovereign-strip-bottom';
  stripBottom.innerHTML = 'CAC Reservation: ' + CAC + ' — Unscrambled visual proof of sovereignty.';
  document.body.appendChild(stripBottom);
  var overlay = document.createElement('div');
  overlay.id = 'gcslc-wl-penalty-overlay';
  overlay.style.cssText = 'display:none;position:fixed;inset:0;z-index:1001;background:rgba(0,33,71,0.92);align-items:center;justify-content:center;flex-direction:column;pointer-events:auto;';
  overlay.innerHTML = '<p style="font-size:1.5rem;font-weight:800;color:#FFD700;">Unauthorized WL Access</p><p style="color:#D4AF37;text-align:center;margin:1rem 0;">Access restricted to authorized Abuja IP. Sovereign data protected.</p><a href="/chairman-executive-brief" target="_blank" rel="noopener" style="color:#D4AF37;text-decoration:underline;font-weight:700;">Chairman\'s Executive Brief</a>';
  document.body.appendChild(overlay);
  function setDefend(on) {
    document.body.classList.toggle('gcslc-blur-defend', on);
    overlay.style.display = on ? 'flex' : 'none';
    stripTop.style.display = on ? 'block' : 'none';
    stripBottom.style.display = on ? 'block' : 'none';
  }
  if (!authorizedIp) { setDefend(true); overlay.style.display = 'flex'; }
  document.addEventListener('visibilitychange', function(){ setDefend(document.hidden); });
  document.addEventListener('contextmenu', function(e){ e.preventDefault(); });
  var h = document.getElementById('gcslc-header-wrap');
  if (h) { h.classList.add('gcslc-header-opportunity-pulse'); setTimeout(function(){ h.classList.remove('gcslc-header-opportunity-pulse'); }, 2500); }
})();
</script>
""", height=0)
# --- SOVEREIGN UI MANIFEST - K-GEC / GCSLC ---
st.markdown(
    '<p class="top-banner">KOMI — GENERATIVE EAGLE CLOUD (K-GEC): VEHICLE FOR NATIONS AND CONGLOMERATES</p>',
    unsafe_allow_html=True,
)
ch_name = "Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau)"
st.markdown(
    f'<p class="chairman-lock">Chairman Lock: {ch_name}</p>',
    unsafe_allow_html=True,
)
st.write("---")
st.markdown(
    '<p class="shimmer-gold">Apex Predator Eagle — 8R Interface</p>',
    unsafe_allow_html=True,
)
# Apex Predator Eagle: Talon Lock visual beside caption when Agentic Eagle is active
agentic_eagle = st.session_state.get("autonomous_sniff_enabled", True)
if agentic_eagle:
    col_cap, col_eagle = st.columns([4, 1])
    with col_cap:
        st.caption("Agentic Eagle active. Sovereign OS interface locked.")
    with col_eagle:
        _render_apex_eagle(use_asset_path=True)
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
st.write("### Sovereign Cloud — AI-Compute metrics")
RealTimeEngine.run()
st.markdown("---")

# --- WL Counter (D2 Reset): cached D7 thermal relief ---
wl_velocity = _cached_wl_velocity()
friction_mult, _mineral_delay = _cached_friction()
wl_c1, wl_c2, wl_c3 = st.columns(3)
with wl_c1:
    st.metric("WL — Missed 9.6× (Human Assets)", f"{wl_velocity:.2f}×", "non-linear velocity")
with wl_c2:
    st.metric("WL — Sovereign AI Compute Shortfall", "$100B", "Robotic world gap")
with wl_c3:
    st.metric("WL Friction Costs (mineral delays)", f"{friction_mult:.2f}×", f"{_mineral_delay} mo market delay")
st.caption("D3 Global Scan — Komi: Market Gaps $72B · 9.6× Wealth Multiplier · Sovereign AI $100B. Generative Eagle Cloud: Komi vehicle for nations and global conglomerates.")
st.markdown("---")

# --- Sidebar: Continental Nodes + Eagle's Talon (play_swat on every strike) ---
with st.sidebar:
    st.markdown("**CAC:** " + CAC_AV_CODE)
    st.markdown("**Chairman Lock:** " + CHAIRMAN_LOCK)
    st.markdown("---")
    # Sovereign Frequency — Eagle + SWAT fusion audio (assets/eagle_swat_fusion.mp3)
    _audio_path = os.path.join(_BASE, "assets", "eagle_swat_fusion.mp3")
    if os.path.isfile(_audio_path):
        st.markdown("### 🦅 Sovereign Frequency")
        with open(_audio_path, "rb") as _f:
            st.audio(_f.read(), format="audio/mp3", autoplay=True, loop=True)
    st.markdown("---")
    st.write("### Sovereign OS — 8R Stealth Paradigm")
    st.caption("Agentic, Generative. Interface: Apex Predator Eagle. Goal: Asset Resuscitation.")
    # Force manifest Apex Eagle in sidebar — asset at African_Gateway/assets/apex_eagle.svg
    _render_apex_eagle(use_asset_path=True)
    with st.expander("**Sovereign OS Pillars**", expanded=False):
        for p in continental_logic.get_sovereign_os_pillars():
            st.markdown(f"**{p['title']}**  \n{p['body']}")
        st.markdown(f'<p style="font-weight: 800; color: #FFD700; margin-top: 8px;">{continental_logic.SOVEREIGN_OS_SIGN_OFF}</p>', unsafe_allow_html=True)
    # Recursive 8R within 8R: D3 within D3 strike — Liquid Intelligent Technologies WL (West African grid-interaction)
    if get_d3_liquid_wl_west_africa is not None:
        with st.expander("**D3 within D3 — Liquid WL (West Africa)**", expanded=False):
            liquid = get_d3_liquid_wl_west_africa(has_liquid_grid_data=False)
            st.metric("WL (Wealth Lost) — grid-interaction", f"${liquid.get('wl_usd_m', 0):.0f}M", "D3 modelled")
            st.metric("Power shortfall vs. 1,205 MW anchor", f"{liquid.get('wl_power_shortfall_mw', 0):.0f} MW", "West African grid")
            _msg = liquid.get("message", "")
            st.caption((_msg[:280] + "…") if len(_msg) > 280 else _msg)
    # D3 within D3 — Cassava 2026 Nigerian infrastructure (1.2 GW anchor); 639.3 M MT → Abuja-Zaria-Kano
    if get_d3_cassava_2026_nigerian_infra is not None:
        with st.expander("**D3 within D3 — Cassava 2026 (1.2 GW anchor)**", expanded=False):
            cassava = get_d3_cassava_2026_nigerian_infra(has_cassava_feed=False)
            st.metric("Power potential (2026 anchor)", f"{cassava.get('power_gw', 1.2)} GW", "Cassava Nigerian AI Factory")
            st.metric("Coal reserves (primary feedstock)", f"{cassava.get('coal_reserves_m_mt', 639.3)} M MT", "600M MT Coal-to-Compute Strike")
            st.caption(f"Primary corridor: **{cassava.get('corridor', 'Abuja-Zaria-Kano')}** — Sovereign AI Factories.")
    st.markdown("---")
    st.write("### Continental Nodes")
    # Phase 4 Fused Nodal: single gate per node
    _node_labels = (
        ("nigeria", "🇳🇬 Nigeria"),
        ("ghana", "🇬🇭 Ghana"),
        ("south_africa", "🇿🇦 South Africa"),
        ("egypt", "🇪🇬 Egypt"),
        ("dubai", "🇦🇪 Dubai (UAE)"),
    )
    for nid, label in _node_labels:
        if st.button(label, key=f"btn_{nid}"):
            _fused_select_node(nid)
    if st.button("Clear selection", key="btn_clear"):
        _fused_select_node(None)
    st.caption("Eagle's Talon: any node → map centers on country + play_swat (180 Hz → 40 Hz) on strike.")
    st.session_state.autonomous_sniff_enabled = st.checkbox(
        "**Agentic Eagle** (Autonomous Sniffer)", value=st.session_state.autonomous_sniff_enabled, key="agentic_eagle"
    )
    if st.session_state.autonomous_sniff_enabled:
        st.caption("Every 60s the Eagle auto-highlights a $10B+ opportunity.")
    st.markdown("---")
    # Foundational Intelligence Layer: Investor Manifesto + Doctor vs. Pharmacist (hardcoded)
    st.write("### Foundational Intelligence")
    with st.expander("**Investor Manifesto**", expanded=False):
        st.markdown(continental_logic.INVESTOR_MANIFESTO)
    with st.expander("**Doctor vs. Pharmacist**", expanded=False):
        st.markdown(continental_logic.DOCTOR_VS_PHARMACIST)
    # Phase 4: single gate for $10B+ strike (CEO + Silicon expanders)
    _is_10b_strike = bool(
        st.session_state.selected_node
        and continental_logic.is_10b_plus_opportunity(st.session_state.selected_node)
    )
    with st.expander("**Strategic Doctrine (CEO Brief)**", expanded=_is_10b_strike):
        st.markdown(continental_logic.STRATEGIC_DOCTRINE_CEO)
        if _is_10b_strike:
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
    with st.expander("**Silicon Valley Strategic Intent**", expanded=_is_10b_strike):
        st.markdown(continental_logic.ENERGY_MINERAL_SHIELD)
        st.markdown("---")
        st.markdown(continental_logic.SANTIAGO_COMPLIANCE)
    st.markdown("---")

# --- Sovereign Rationale: Big Tech Handshake Manifesto (linked to Natural Gas, Gold, Rare Earth) ---
with st.expander("**Sovereign Rationale — Big Tech Handshake Manifesto**", expanded=False):
    st.markdown(continental_logic.BIG_TECH_HANDSHAKE_MANIFESTO)
    st.caption("Linked SSMV corridors: **" + "**, **".join(continental_logic.SSMV_CORRIDORS_MANIFESTO) + "**")

# --- Map container: Sovereign Cloud / Sovereign Glass — Continental View + Eagle's Talon ---
st.write("### Sovereign Cloud — The Sovereign Glass (Continental View)")
st.caption("**GCSLC Sovereign Diagnostic** | **Live Eagle Engine:** Sniffer hovers over map → on node click, high-velocity **Talon Strike** with **play_swat** 180 Hz audio sync. ($10B+ nodes: golden radar sweep.)")
# Talon Lock 100%: Force Sovereign Glass fallback so nodes always appear (GPU/WebGL disabled or not)
st.markdown(SOVEREIGN_GLASS_MAP_FALLBACK_HTML, unsafe_allow_html=True)
map_container_class = _get_map_container_class(
    st.session_state.selected_node,
    st.session_state.pulse_triggered,
    continental_logic.is_10b_plus_opportunity,
)
# Build deck; if .json/data or import missing, deck is None — use inline fallback
try:
    deck = africa_map.build_africa_deck(selected_node=st.session_state.selected_node, opacity=0.85)
except Exception:
    deck = None
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
        f'<div class="{map_container_class}" style="padding: 8px; position: relative;">'
        f'<span class="gcslc-proprietary-watermark" aria-hidden="true">Proprietary Methodology</span>{eagle_html}',
        unsafe_allow_html=True,
    )
    try:
        st.pydeck_chart(deck, use_container_width=True)  # 2026 equivalent stretch; may fail if GPU/WebGL disabled
    except Exception:
        pass  # Fallback already shown above — nodes always visible
    st.markdown("</div>", unsafe_allow_html=True)
if st.session_state.pulse_triggered and st.session_state.selected_node:
    st.session_state.pulse_triggered = False

# --- Generative SSMV: Dynamic Brief on node strike ---
if st.session_state.selected_node:
    reveal_text = continental_logic.get_determinant_reveal(st.session_state.selected_node)
    node_name = africa_map.CONTINENTAL_NODES.get(st.session_state.selected_node, {}).get("name", st.session_state.selected_node)
    gap = continental_logic.get_market_gap_for_node(st.session_state.selected_node)
    gap_b = gap["gap_b_usd"]
    # Generated value for Dynamic Brief (node-dependent)
    generated_value_b = round(gap_b * 0.45 + 14.2, 1)
    st.markdown(
        f'<div class="awc-determinant-popup awc-sovereign-glass-window" style="margin-bottom: 8px;">'
        f'<p style="font-weight: 800; color: #FFD700; margin-bottom: 6px;">GCSLC ANALYSIS: Asset Resuscitation detected.</p>'
        f'<p style="font-size: 0.95rem;">Applying D4 (Restructure) + D6 (Revitalize).</p>'
        f'<p class="awc-opportunity-badge">Potential Wealth Retention: <span class="awc-digital-counter">{generated_value_b}</span>B USD.</p>'
        f'</div>',
        unsafe_allow_html=True,
    )
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
      // Generative audio: sync with eye-contact — "Get to work" directive (once after head-turn)
      setTimeout(function() {
        try {
          var u = new SpeechSynthesisUtterance('I have identified the gap. The anchor is secured. Get to work.');
          u.rate = 0.9;
          u.pitch = 1;
          u.volume = 1;
          if (window.speechSynthesis) window.speechSynthesis.speak(u);
        } catch (e) {}
      }, 2600);
    })();
    </script>
    """, height=240)

st.caption("Continental nodes: Nigeria, Ghana, South Africa, Egypt. Strategic Partner: Dubai (UAE). Select a node to center map and trigger Eagle's Talon + play_swat.")

# --- Agentic Eagle: 60s autonomous sniff (redirect to ?autonomous=1 to highlight $10B+ node) ---
if st.session_state.get("autonomous_sniff_enabled", True):
    st.components.v1.html(
        """
        <div id="awc-autonomous-timer" style="font-size: 0.85rem; color: #D4AF37; margin-top: 4px;">
          <span id="awc-timer-text">Agentic Eagle: next autonomous sniff in <span id="awc-countdown">60</span>s</span>
        </div>
        <script>
        (function() {
          var start = Date.now();
          var el = document.getElementById('awc-countdown');
          var interval = setInterval(function() {
            var left = 60 - Math.floor((Date.now() - start) / 1000);
            if (left <= 0) {
              clearInterval(interval);
              window.location = window.location.pathname + '?autonomous=1';
              return;
            }
            if (el) el.textContent = left;
          }, 1000);
        })();
        </script>
        """,
        height=32,
    )

# --- Universal Impact Radar: tabs (Security | Social Well-being | Sovereign Well-being Index) ---
st.markdown("---")
st.write("### Universal Impact Radar")
st.caption("How the **$170.85B** anchor and **8R Strike on Atoms** (Energy/Minerals) drive Jobs, Security, and Health.")
radar_t1, radar_t2, radar_t3 = st.tabs(["National Security Impact", "Social Well-being Index", "Sovereign Well-being Index"])
with radar_t1:
    st.write("**National Security Impact** — $170.85B anchor → regional stability")
    sec_heat = continental_logic.get_national_security_impact_heatmap()
    st.dataframe(
        [{"Region": r["region"], "Indicator": r["indicator"], "Before anchor": r["before_anchor"], "After anchor": r["after_anchor"], "Δ Stability": r["stability_delta"]} for r in sec_heat],
        width=WIDTH_2026,
        hide_index=True,
    )
    st.caption("Higher scores = more stability. The anchor increases sovereign retention and reduces resource conflict.")
with radar_t2:
    st.write("**Social Well-being Index** — $170.85B anchor → poverty reduction")
    soc_heat = continental_logic.get_social_wellbeing_index_heatmap()
    st.dataframe(
        [{"Dimension": d["dimension"], "Baseline (%)": d["baseline_pct"], "Post-anchor (%)": d["post_anchor_pct"], "Change": d["reduction"]} for d in soc_heat],
        width=WIDTH_2026,
        hide_index=True,
    )
    st.caption("Poverty headcount drops; employment and energy access rise under 8R sovereign corridors.")
with radar_t3:
    st.write("**Sovereign Well-being Index** — 8R Strike on Atoms (Energy/Minerals) → Jobs, Security, Health")
    swi = continental_logic.get_sovereign_wellbeing_index()
    st.dataframe(
        [{"Atoms domain": r["atoms_domain"], "Well-being": r["wellbeing_dimension"], "Metric": r["metric"], "Before 8R": r["before_8r"], "After 8R": r["after_8r"], "Unit": r["unit"]} for r in swi],
        width=WIDTH_2026,
        hide_index=True,
    )
    st.caption("The Eagle's strike on Energy and Minerals generates Jobs (FTE), Security (index), and Health (compliance / air quality).")

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

# --- Idea Engine: Share to X / LinkedIn — Talon Lock report broadcast ---
st.markdown("---")
st.write("### Idea Engine — Social Connectivity")
st.caption("Broadcast the Eagle's strike as a **GCSLC Sovereign Diagnostic** to the global elite.")
# Build Talon Lock report text from current selection (or default)
_node = st.session_state.selected_node
_report_node = africa_map.CONTINENTAL_NODES.get(_node or "", {}).get("name", "Continental") if _node else "Continental"
_reveal = continental_logic.get_determinant_reveal(_node) if _node else "8R Paradigm Applied"
_talon_report = f"GCSLC Sovereign Diagnostic — {_report_node}. {_reveal} $170.85B Talon Lock. Galadiman Ruwa Center (GCSLC) — 8R Stealth Paradigm."
_tweet_text = urllib.parse.quote(_talon_report)
_linkedin_summary = urllib.parse.quote(_talon_report[:200] + ("…" if len(_talon_report) > 200 else ""))
_share_url = "https://www.gcslc.org"  # placeholder; replace with actual portal URL if desired
_twitter_url = f"https://twitter.com/intent/tweet?text={_tweet_text}"
_linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url={urllib.parse.quote(_share_url)}&summary={_linkedin_summary}"
st.markdown(
    f'<p style="margin-bottom: 8px;">'
    f'<a href="{_twitter_url}" target="_blank" rel="noopener noreferrer" style="display: inline-block; margin-right: 12px; padding: 8px 16px; background: #000; color: #fff; border-radius: 8px; text-decoration: none; font-weight: 700;">Share to X</a> '
    f'<a href="{_linkedin_url}" target="_blank" rel="noopener noreferrer" style="display: inline-block; padding: 8px 16px; background: #0A66C2; color: #fff; border-radius: 8px; text-decoration: none; font-weight: 700;">Share to LinkedIn</a>'
    f'</p>',
    unsafe_allow_html=True,
)
st.caption("Every Eagle strike attaches the Talon Lock report to your share.")

# --- Gulf Anchor: Petro-to-Data (Saudi/UAE/Qatar) ---
st.markdown("---")
st.write("### Gulf Anchor — Petro-to-Data")
st.caption("**Saudi / UAE / Qatar** — $30B AI Investment Gap · NGECC Green Energy → 1GW AI Data Center ambitions.")
petro = continental_logic.get_petro_to_data_node()
with st.expander("**Petro-to-Data** — Saudi / UAE / Qatar", expanded=True):
    st.metric("AI Investment Gap", f"$ {petro['ai_investment_gap_b_usd']:.0f}B", help="Gulf AI infrastructure gap")
    st.metric("AI Data Center ambition", f"{petro['ai_data_center_ambition_gw']} GW", help="1GW AI Data Center plans")
    st.markdown("**NGECC Green Energy link:** " + petro["narrative"])

# --- Aviation Hub Sync: Dubai ↔ Emirates/Etihad, 2026 F1 ---
st.markdown("---")
st.write("### Aviation Hub Sync")
st.caption("Dubai Hub ↔ **Emirates / Etihad** flight corridors · Eagle sniffs paths → energy security for **2026 Formula 1** travel surge.")
av = continental_logic.get_aviation_hub_sync()
with st.expander("**Dubai Hub** — Emirates / Etihad", expanded=True):
    st.write("**Flight corridors:** " + ", ".join(av["flight_corridors"]))
    st.markdown(f"**{av['f1_surge_year']} Formula 1 travel surge:** " + av["narrative"])
    st.markdown(
        '''
        <div class="awc-lab-panel" style="margin-top: 12px; text-align: center; padding: 12px;">
          <style>
            .awc-eagle-flight { display: inline-block; animation: sniff-float 2s ease-in-out infinite; filter: drop-shadow(0 0 8px rgba(255,215,0,0.6)); }
            @keyframes sniff-float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-4px); } }
            .awc-flight-badge { display: inline-block; margin-top: 8px; padding: 6px 14px; border: 2px solid #FFD700; border-radius: 8px; font-weight: 800; color: #FFD700; font-size: 0.85rem; letter-spacing: 1px; }
          </style>
          <p style="color: #D4AF37; font-size: 0.85rem; margin-bottom: 6px;">Eagle sniffs flight paths</p>
          <div class="awc-eagle-flight">
            <svg width="40" height="28" viewBox="0 0 56 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <ellipse cx="28" cy="20" rx="12" ry="8" fill="#FFD700" stroke="#B8860B" stroke-width="0.8"/>
              <path d="M18 16 L28 12 L38 16" stroke="#B8860B" stroke-width="0.8" fill="none"/>
              <circle cx="24" cy="18" r="1.5" fill="#1a1a1a"/><circle cx="32" cy="18" r="1.5" fill="#1a1a1a"/>
            </svg>
          </div>
          <p style="margin-top: 4px; font-size: 0.8rem; color: rgba(212,175,55,0.9);">↓</p>
          <span class="awc-flight-badge">ENERGY-SECURED · 2026 F1</span>
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
        width=WIDTH_2026,
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
        width=WIDTH_2026,
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
# Sovereign Stamp: CAC + Chairman Lock — persistent non-scrollable footer (D8 Retain)
st.markdown(
    '<div class="gcslc-sovereign-footer">'
    '<span class="cac">CAC Name Availability Code: 176917792057</span>'
    '<p class="chairman">GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION LTD/GTE | Chairman & Founder: Dr. Sa\'ad Jaafaru</p>'
    '<p class="gcslc-signature-lock" style="font-size:0.7rem;opacity:0.9;margin-top:0.2rem;">CAC & Chairman Lock: local, non-transferable signature — Dr. Sa\'ad Jaafaru. D8 Retain.</p>'
    '<p style="font-size:0.7rem;opacity:0.9;margin-top:0.2rem;">CAC Code & shimmering branding — unscrambled visual proof of sovereignty.</p>'
    '</div>',
    unsafe_allow_html=True,
)
