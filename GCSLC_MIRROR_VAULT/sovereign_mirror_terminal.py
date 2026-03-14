"""
FINAL Sovereign Nodal Mirror — GCSLC Mirror Vault
Galadiman Ruwa Center for Strategic Leadership and Communication (GCSLC) LTD/GTE.
Global Hub Clocks · Command Map (36 States, 13 Strategic) · Velocity Speedometer ·
Eagle Scan + HUD Soundscape · 8R Determinant Widgets · Sovereign Signature.
© 2026 GCSLC. Chairman & Founder: Dr. Sa'ad Jaafaru.
"""

import os
import sys
import math
import time
from datetime import datetime

import streamlit as st

# --- Paths ---
_VAULT = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_VAULT)
if _BASE not in sys.path:
    sys.path.insert(0, _BASE)
ASSETS = os.path.join(_BASE, "assets")
EAGLE_CRY_PATH = os.path.join(ASSETS, "eagle_swat_fusion.mp3")
HUD_CHIRP_PATH = os.path.join(ASSETS, "eagle_swat_fusion.mp3")  # same or separate file

# --- Page config ---
st.set_page_config(
    page_title="Sovereign Nodal Mirror — GCSLC",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Session state ---
if "selected_state" not in st.session_state:
    st.session_state.selected_state = None
if "scan_played" not in st.session_state:
    st.session_state.scan_played = False

# --- Constants ---
NAVY = "#000033"
GOLD = "#D4AF37"
FULL_HEADER = "Galadiman Ruwa Center for Strategic Leadership and Communication (GCSLC) LTD/GTE"
SIGNATURE = "Dr. Jaafaru Sa'ad — Chairman & Founder"
VALUATION_ANCHOR_B = 170.85

# 36 states (Nigeria)
STATES_36 = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno",
    "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "Gombe", "Imo",
    "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos",
    "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers",
    "Sokoto", "Taraba", "Yobe", "Zamfara",
]

# 13 Strategic States (Golden Pulse) — coal/mineral corridor
STRATEGIC_13 = {
    "Enugu", "Kogi", "Gombe", "Benue", "Delta", "Nasarawa", "Anambra",
    "Plateau", "Adamawa", "Edo", "Bauchi", "Kwara", "Imo",
}

# 8R Determinants
DETERMINANTS_8R = [
    "D1: Refine", "D2: Reset", "D3: Research", "D4: Restructure",
    "D5: Resuscitate", "D6: Revitalize", "D7: Re-engineer", "D8: Retain",
]

# --- Global CSS ---
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap');

:root { --navy: #000033; --gold: #D4AF37; --gold-subtle: rgba(212,175,55,0.7); }

.stApp, [data-testid="stAppViewContainer"], .main .block-container { background: var(--navy) !important; }
.main .block-container { padding: 0.75rem 1.5rem 4rem; max-width: 100%; }

/* Shimmering GCSLC header */
.gcslc-shimmer-header {
    font-family: 'Goldman', sans-serif !important;
    font-size: clamp(1rem, 2.2vw, 1.4rem) !important;
    font-weight: 700;
    text-align: center;
    letter-spacing: 0.08em;
    background: linear-gradient(110deg, #D4AF37 0%, #F9F295 20%, #fff 50%, #F9F295 80%, #D4AF37 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: header-shimmer 3s ease-in-out infinite;
    margin-bottom: 0.5rem;
}
@keyframes header-shimmer { 0%,100% { background-position: 0% center; } 50% { background-position: 100% center; } }

/* Hub clocks bar */
.clocks-bar { display: flex; flex-wrap: wrap; justify-content: center; gap: 1rem; padding: 0.5rem; background: rgba(0,0,51,0.9); border-bottom: 2px solid var(--gold); margin-bottom: 1rem; }
.clock-cell { font-family: 'Goldman', sans-serif; color: var(--gold); font-size: 0.85rem; text-align: center; }
.clock-cell .tz { opacity: 0.8; font-size: 0.7rem; }
.clock-cell .time { font-weight: 700; letter-spacing: 0.05em; }

/* Command Map: state grid with prism-glow */
.map-wrap { width: 100%; padding: 1rem 0; }
.map-title {
    font-family: 'Goldman', sans-serif; color: var(--gold); text-align: center; margin-bottom: 0.75rem;
    letter-spacing: 0.15em; font-size: 1rem;
    border: 1px solid rgba(212,175,55,0.4); border-radius: 8px; padding: 0.5rem;
    box-shadow: 0 0 20px rgba(212,175,55,0.25);
}
.state-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(90px, 1fr)); gap: 6px; }
.state-node {
    font-family: 'Goldman', sans-serif;
    font-size: 0.7rem;
    padding: 0.4rem 0.3rem;
    text-align: center;
    border: 1px solid rgba(212,175,55,0.5);
    border-radius: 6px;
    background: rgba(0,0,51,0.8);
    color: var(--gold-subtle);
    cursor: pointer;
    transition: all 0.25s ease;
    box-shadow: 0 0 12px rgba(212,175,55,0.15);
}
.state-node:hover { border-color: var(--gold); color: var(--gold); box-shadow: 0 0 20px rgba(212,175,55,0.35); }
.state-node.strategic { border-color: var(--gold); color: var(--gold); animation: prism-pulse 2s ease-in-out infinite; }
@keyframes prism-pulse { 0%,100% { box-shadow: 0 0 12px rgba(212,175,55,0.3); } 50% { box-shadow: 0 0 24px rgba(212,175,55,0.6); } }

/* Velocity Speedometer container */
.speed-wrap { margin: 1rem 0; }

/* 8R Determinant widgets */
.d8-row { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; margin: 1rem 0; padding: 0.75rem; }
.d8-box {
    font-family: 'Goldman', sans-serif;
    font-size: 0.65rem;
    width: 72px; height: 72px;
    display: flex; align-items: center; justify-content: center;
    text-align: center; line-height: 1.2;
    border: 2px solid var(--gold);
    border-radius: 8px;
    background: rgba(0,0,51,0.8);
    color: var(--gold);
    animation: d8-pulse 2.5s ease-in-out infinite;
}
.d8-box:nth-child(1) { animation-delay: 0s; }
.d8-box:nth-child(2) { animation-delay: 0.15s; }
.d8-box:nth-child(3) { animation-delay: 0.3s; }
.d8-box:nth-child(4) { animation-delay: 0.45s; }
.d8-box:nth-child(5) { animation-delay: 0.6s; }
.d8-box:nth-child(6) { animation-delay: 0.75s; }
.d8-box:nth-child(7) { animation-delay: 0.9s; }
.d8-box:nth-child(8) { animation-delay: 1.05s; }
@keyframes d8-pulse { 0%,100% { opacity: 1; box-shadow: 0 0 12px rgba(212,175,55,0.25); } 50% { opacity: 0.9; box-shadow: 0 0 20px rgba(212,175,55,0.5); } }

/* Signature watermark */
.sig-watermark {
    position: fixed;
    bottom: 0.5rem;
    right: 1rem;
    font-family: 'Goldman', sans-serif;
    font-size: 0.7rem;
    color: var(--gold-subtle);
    letter-spacing: 0.06em;
    z-index: 901;
    border-left: 3px solid var(--gold);
    padding-left: 0.5rem;
    background: rgba(0,0,51,0.85);
}
</style>
""",
    unsafe_allow_html=True,
)

# --- 1. Shimmering GCSLC header ---
st.markdown(f'<p class="gcslc-shimmer-header">{FULL_HEADER}</p>', unsafe_allow_html=True)

# --- 2. Global Hub Clocks (live via HTML/JS) ---
st.components.v1.html(
    """
    <div class="clocks-bar" id="hub-clocks" style="font-family: 'Goldman', sans-serif;">
        <div class="clock-cell"><div class="tz">Zaria/Abuja (WAT)</div><div class="time" id="wat">--:--:--</div></div>
        <div class="clock-cell"><div class="tz">London (GMT)</div><div class="time" id="gmt">--:--:--</div></div>
        <div class="clock-cell"><div class="tz">Dubai (GST)</div><div class="time" id="gst">--:--:--</div></div>
        <div class="clock-cell"><div class="tz">Singapore (SGT)</div><div class="time" id="sgt">--:--:--</div></div>
        <div class="clock-cell"><div class="tz">Silicon Valley (PDT)</div><div class="time" id="pdt">--:--:--</div></div>
        <div class="clock-cell"><div class="tz">Wall Street (EDT)</div><div class="time" id="edt">--:--:--</div></div>
    </div>
    <script>
    (function(){
        var zones = [
            { id: 'wat', off: 1 },
            { id: 'gmt', off: 0 },
            { id: 'gst', off: 4 },
            { id: 'sgt', off: 8 },
            { id: 'pdt', off: -7 },
            { id: 'edt', off: -4 }
        ];
        function pad(n){ return (n<10?'0':'')+n; }
        function run(){
            var d = new Date();
            zones.forEach(function(z){
                var utc = d.getTime() + d.getTimezoneOffset()*60000;
                var local = new Date(utc + z.off*3600000);
                var el = document.getElementById(z.id);
                if(el) el.textContent = pad(local.getHours())+':'+pad(local.getMinutes())+':'+pad(local.getSeconds());
            });
        }
        run(); setInterval(run, 1000);
    })();
    </script>
    """,
    height=70,
)

# --- 3. Command Map: 36 states, 13 strategic with Golden Pulse; click → $170.8B logic ---
st.markdown('<p class="map-title">THE COMMAND MAP — Terrestrial Ground-Base (36 States)</p>', unsafe_allow_html=True)

# Build state grid HTML: each state is a link/button that triggers Streamlit rerun with query param or we use st.button per state (many). Use a single selectbox or radio for "selected state" and render the grid as HTML with data-state attributes; we can't get click from HTML to Streamlit easily. So: use Streamlit buttons in columns. 36 buttons in a grid (6x6 or 4x9). Each button sets session_state.selected_state and reruns. Then below we show valuation logic if selected_state is in STRATEGIC_13.
cols_per_row = 9
for i in range(0, len(STATES_36), cols_per_row):
    row = STATES_36[i : i + cols_per_row]
    cols = st.columns(len(row))
    for j, state in enumerate(row):
        with cols[j]:
            is_strategic = state in STRATEGIC_13
            label = f"🟡 {state}" if is_strategic else state
            if st.button(label, key=f"state_{state}", use_container_width=True):
                st.session_state.selected_state = state
                st.rerun()

# Popup: $170.8B valuation logic when a strategic state is selected
if st.session_state.selected_state:
    s = st.session_state.selected_state
    if s in STRATEGIC_13:
        with st.expander(f"**$170.85B Valuation Logic — {s}** (Strategic Node)", expanded=True):
            st.markdown(
                f"""
                **Central Empirical Metric:** **$170.85B** valuation anchor (8R Scientific Validation).  
                **{s}** is one of the **13 Strategic States** in the coal/mineral corridor.  
                - **Wealth retention:** 95% sovereign value retained in-country.  
                - **Power potential:** 1,203 MW (13-state nodal).  
                - **Coal feedstock:** 639.3M MT aligned to Abuja–Zaria–Kano corridor.  
                - **Determinants:** D1 Refine (high-purity corridors), D2 Reset (SPV→SSMV), D3 Research (rare earth coordinates).
                """
            )
    else:
        with st.expander(f"**State node: {s}**", expanded=False):
            st.caption(f"{s} — 36-state territorial coverage. Strategic nodes (13) carry the $170.85B valuation anchor.")

# --- 4. Velocity Speedometer: semi-circle gauge, National Opportunity vs Global Friction ---
t = time.time()
gauge_value = max(0.1, min(0.9, 0.5 + 0.2 * math.sin(t * 0.3)))
needle_angle_rad = math.radians(180 * (1 - gauge_value))  # 0 at left, 180 at right
needle_x = 100 + 70 * math.cos(needle_angle_rad)
needle_y = 100 - 70 * math.sin(needle_angle_rad)
arc_offset = 251 * (1 - gauge_value)
st.components.v1.html(
    f"""
    <div class="speed-wrap" style="max-width:420px; margin:1rem auto;">
        <div style="text-align:center; font-family: Goldman, sans-serif; color: #D4AF37; font-size: 0.9rem; margin-bottom: 0.25rem;">Velocity — Real-Time Valuation</div>
        <svg viewBox="0 0 200 120" style="width:100%; height:140px;">
            <defs>
                <linearGradient id="goldGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" style="stop-color:#333"/>
                    <stop offset="100%" style="stop-color:#D4AF37"/>
                </linearGradient>
            </defs>
            <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="rgba(212,175,55,0.3)" stroke-width="12" stroke-linecap="round"/>
            <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="url(#goldGrad)" stroke-width="10" stroke-linecap="round" stroke-dasharray="251" stroke-dashoffset="{arc_offset}"/>
            <line x1="100" y1="100" x2="{needle_x}" y2="{needle_y}" stroke="#D4AF37" stroke-width="3" stroke-linecap="round"/>
            <circle cx="100" cy="100" r="8" fill="#000033" stroke="#D4AF37" stroke-width="2"/>
        </svg>
        <div style="display:flex; justify-content:space-between; font-family: Goldman, sans-serif; font-size: 0.7rem; color: rgba(212,175,55,0.9); padding: 0 10px;">
            <span>Global Friction</span>
            <span>National Opportunity</span>
        </div>
    </div>
    """,
    height=200,
)

# --- 5. Cinematic Soundscape: Eagle Cry (Sovereign Scan) + HUD chirps ---
st.markdown("#### Sovereign Scan & HUD")
col_audio1, col_audio2 = st.columns(2)
with col_audio1:
    if os.path.isfile(EAGLE_CRY_PATH):
        with open(EAGLE_CRY_PATH, "rb") as f:
            st.audio(f.read(), format="audio/mp3", key="eagle_cry")
        st.caption("Eagle Cry — Sovereign Scan")
    else:
        st.caption("Eagle Cry (asset optional): eagle_swat_fusion.mp3")
with col_audio2:
    if os.path.isfile(HUD_CHIRP_PATH):
        with open(HUD_CHIRP_PATH, "rb") as f:
            st.audio(f.read(), format="audio/mp3", key="hud_chirp")
        st.caption("HUD Sound Link — data-processing phase")
    else:
        st.caption("HUD chirps (asset optional)")

# --- 6. 8R Determinant Widgets: 8 pulsing squares ---
st.markdown("#### 8R Determinants")
d8_html = "".join(
    f'<div class="d8-box">{d.split(": ")[0]}<br/>{d.split(": ")[1] if ": " in d else ""}</div>' for d in DETERMINANTS_8R
)
st.markdown(f'<div class="d8-row">{d8_html}</div>', unsafe_allow_html=True)

# --- 7. Signature watermark ---
st.markdown(f'<div class="sig-watermark">{SIGNATURE}</div>', unsafe_allow_html=True)
