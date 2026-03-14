"""
FINAL Sovereign Nodal Mirror — High-Velocity Specifications
Galadiman Ruwa Center for Strategic Leadership and Communication (GCSLC) LTD/GTE.
Temporal Awareness · Terrestrial Ground-Base (SVG Map) · AWC Valuation Speedometer ·
8R Determinants · Audio-Visual Handshake · Signature & Credibility.
© 2026 GCSLC. Chairman & Founder: Dr. Sa'ad Jaafaru.
"""

import os
import sys
import math
import time

import streamlit as st

# --- Paths ---
_VAULT = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_VAULT)
if _BASE not in sys.path:
    sys.path.insert(0, _BASE)
ASSETS = os.path.join(_BASE, "assets")
EAGLE_CRY_PATH = os.path.join(ASSETS, "eagle_swat_fusion.mp3")
HUD_CHIRP_PATH = os.path.join(ASSETS, "eagle_swat_fusion.mp3")

st.set_page_config(page_title="Sovereign Nodal Mirror — GCSLC", layout="wide", initial_sidebar_state="collapsed")

# --- Session state ---
if "initiate_triggered" not in st.session_state:
    st.session_state.initiate_triggered = False

# --- Query param for map click (Terrestrial Ground-Base) ---
selected_state = st.query_params.get("state")
if selected_state and selected_state not in [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno",
    "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "Gombe", "Imo",
    "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos",
    "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers",
    "Sokoto", "Taraba", "Yobe", "Zamfara",
]:
    selected_state = None

NAVY = "#000033"
GOLD = "#D4AF37"
STRATEGIC_13 = {"Enugu", "Kogi", "Gombe", "Benue", "Delta", "Nasarawa", "Anambra", "Plateau", "Adamawa", "Edo", "Bauchi", "Kwara", "Imo"}
STATES_36 = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno",
    "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "Gombe", "Imo",
    "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos",
    "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers",
    "Sokoto", "Taraba", "Yobe", "Zamfara",
]
DETERMINANTS_8R = [
    "D1: Refine", "D2: Reset", "D3: Research", "D4: Restructure",
    "D5: Resuscitate", "D6: Revitalize", "D7: Re-engineer", "D8: Retain",
]
# Approximate (x,y) positions for 36 states in SVG viewBox 0 0 400 500 (Nigeria outline)
STATE_POS = [
    (120, 380), (280, 180), (200, 420), (160, 360), (260, 220), (180, 440), (220, 280), (320, 120),
    (240, 420), (140, 400), (200, 340), (120, 340), (80, 360), (200, 320), (300, 200), (160, 380),
    (280, 140), (240, 200), (260, 160), (260, 100), (180, 80), (220, 260), (200, 240), (60, 380),
    (240, 260), (220, 200), (100, 340), (100, 300), (80, 320), (120, 280), (260, 240), (180, 420),
    (180, 60), (300, 260), (320, 160), (240, 120),
]
VALUATION_MAX = 170.8

# --- Global CSS ---
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap');
:root { --navy: #000033; --gold: #D4AF37; --gold-subtle: rgba(212,175,55,0.7); }
.stApp, [data-testid="stAppViewContainer"], .main .block-container { background: var(--navy) !important; }
.main .block-container { padding: 0.6rem 1rem 5rem; max-width: 100%; }

/* Global Header: Temporal Awareness — 6 clocks */
.clocks-bar {
    display: flex; flex-wrap: wrap; justify-content: center; gap: 1.25rem;
    padding: 0.6rem 1rem; background: var(--navy);
    border-bottom: 2px solid var(--gold);
    margin-bottom: 0.75rem;
}
.clock-cell { font-family: 'Goldman', sans-serif; color: var(--gold); font-size: 0.85rem; text-align: center; }
.clock-cell .tz { opacity: 0.85; font-size: 0.7rem; }
.clock-cell .time { font-weight: 700; letter-spacing: 0.05em; }

/* Terrestrial Ground-Base: SVG map prism-frame + golden pulse */
#nigeria-svg { width: 100%; height: auto; max-height: 420px; }
.prism-frame { filter: drop-shadow(0 0 12px rgba(212,175,55,0.4)); }
.state-region { cursor: pointer; transition: all 0.2s; }
.state-region:hover { filter: brightness(1.2); }
.state-region.strategic { animation: golden-pulse 1.8s ease-in-out infinite; }
@keyframes golden-pulse { 0%,100% { filter: drop-shadow(0 0 6px rgba(212,175,55,0.6)); } 50% { filter: drop-shadow(0 0 18px rgba(212,175,55,0.9)); } }
/* Data Flare (floating popup on strategic state click) */
.data-flare {
    position: fixed; top: 50%; left: 50%; transform: translate(-50%,-50%);
    font-family: 'Goldman', sans-serif; font-size: 1.1rem; color: var(--gold);
    background: rgba(0,0,51,0.95); border: 2px solid var(--gold);
    padding: 1rem 1.5rem; border-radius: 12px;
    box-shadow: 0 0 32px rgba(212,175,55,0.5);
    z-index: 9998; animation: flare-in 0.3s ease-out;
}
@keyframes flare-in { from { opacity: 0; transform: translate(-50%,-50%) scale(0.9); } to { opacity: 1; transform: translate(-50%,-50%) scale(1); } }

/* AWC Valuation Speedometer */
.gauge-wrap { margin: 1rem auto; max-width: 480px; }
.gauge-title { font-family: 'Goldman', sans-serif; color: var(--gold); text-align: center; font-size: 0.95rem; margin-bottom: 0.25rem; }
.floating-num { position: absolute; font-family: 'Goldman', sans-serif; color: #00ff88; font-size: 0.85rem; font-weight: 700; pointer-events: none; animation: float-up 2s ease-out forwards; }
@keyframes float-up { 0% { opacity: 1; transform: translateY(0); } 100% { opacity: 0; transform: translateY(-60px); } }

/* 8R Determinants: breathe (zoom in/out) + golden glow */
.d8-row { display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; margin: 1rem 0; padding: 0.75rem; }
.d8-box {
    font-family: 'Goldman', sans-serif; font-size: 0.65rem;
    width: 74px; height: 74px;
    display: flex; align-items: center; justify-content: center; text-align: center; line-height: 1.2;
    border: 2px solid var(--gold); border-radius: 8px;
    background: rgba(0,0,51,0.85); color: var(--gold);
    animation: d8-breathe 2.8s ease-in-out infinite;
}
.d8-box:nth-child(1) { animation-delay: 0s; }
.d8-box:nth-child(2) { animation-delay: 0.2s; }
.d8-box:nth-child(3) { animation-delay: 0.4s; }
.d8-box:nth-child(4) { animation-delay: 0.6s; }
.d8-box:nth-child(5) { animation-delay: 0.8s; }
.d8-box:nth-child(6) { animation-delay: 1s; }
.d8-box:nth-child(7) { animation-delay: 1.2s; }
.d8-box:nth-child(8) { animation-delay: 1.4s; }
@keyframes d8-breathe {
    0%,100% { transform: scale(1); box-shadow: 0 0 14px rgba(212,175,55,0.3); }
    50% { transform: scale(1.08); box-shadow: 0 0 24px rgba(212,175,55,0.6); }
}

/* Signature & Credibility */
.footer-left {
    position: fixed; bottom: 0.5rem; left: 1rem; z-index: 901;
    font-family: 'Goldman', sans-serif; font-size: 0.8rem; color: var(--gold-subtle);
    letter-spacing: 0.12em;
    background: linear-gradient(110deg, #D4AF37, #F9F295, #D4AF37); background-size: 200% auto;
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: shimmer 3s ease-in-out infinite;
}
@keyframes shimmer { 0%,100% { background-position: 0% center; } 50% { background-position: 100% center; } }
.footer-right {
    position: fixed; bottom: 0.5rem; right: 1rem; z-index: 901;
    font-family: 'Goldman', sans-serif; font-size: 0.7rem; color: var(--gold-subtle);
    letter-spacing: 0.06em; border-left: 3px solid var(--gold); padding-left: 0.5rem;
    background: rgba(0,0,51,0.9);
}

/* Captain: hide audio component entirely so sound feels like integrated system response, not a website playing a media file */
[data-testid="stAudio"], .stAudio, .element-container:has(audio) { display: none !important; }
audio { display: none !important; }
</style>
""",
    unsafe_allow_html=True,
)

# --- 1. Global Header: 6 live clocks (Temporal Awareness) ---
st.components.v1.html(
    """
    <div class="clocks-bar">
        <div class="clock-cell"><div class="tz">Zaria/Abuja (WAT)</div><div class="time" id="wat">--:--:--</div></div>
        <div class="clock-cell"><div class="tz">London (GMT)</div><div class="time" id="gmt">--:--:--</div></div>
        <div class="clock-cell"><div class="tz">Dubai (GST)</div><div class="time" id="gst">--:--:--</div></div>
        <div class="clock-cell"><div class="tz">Singapore (SGT)</div><div class="time" id="sgt">--:--:--</div></div>
        <div class="clock-cell"><div class="tz">Silicon Valley (PDT)</div><div class="time" id="pdt">--:--:--</div></div>
        <div class="clock-cell"><div class="tz">Wall Street (EDT)</div><div class="time" id="edt">--:--:--</div></div>
    </div>
    <script>
    (function(){
        var z=[{id:'wat',o:1},{id:'gmt',o:0},{id:'gst',o:4},{id:'sgt',o:8},{id:'pdt',o:-7},{id:'edt',o:-4}];
        function p(n){ return (n<10?'0':'')+n; }
        function run(){ var d=new Date(); var u=d.getTime()+d.getTimezoneOffset()*60000;
            z.forEach(function(x){ var l=new Date(u+x.o*3600000); var e=document.getElementById(x.id); if(e) e.textContent=p(l.getHours())+':'+p(l.getMinutes())+':'+p(l.getSeconds()); });
        }
        run(); setInterval(run,1000);
    })();
    </script>
    """,
    height=58,
)

# --- 2. Terrestrial Ground-Base: Full-width SVG map of Nigeria, 36 states Prism-Frame, 13 Golden Pulse ---
# Simplified Nigeria outline (polygon) + 36 state circles; click → ?state=X → Data Flare for strategic
NIGERIA_PATH = "M 45 55 L 355 48 L 378 135 L 365 320 L 355 465 L 55 468 L 22 320 Z"
state_links = []
for i, state in enumerate(STATES_36):
    x, y = STATE_POS[i]
    strat = " strategic" if state in STRATEGIC_13 else ""
    # Use Streamlit-friendly navigation: link to same app with query param
    state_links.append(
        f'<a href="?state={state.replace(" ", "%20")}" target="_top" class="state-region{strat}" data-state="{state}">'
        f'<circle cx="{x}" cy="{y}" r="14" fill="rgba(0,0,51,0.9)" stroke="#D4AF37" stroke-width="1.5"/>'
        f'<text x="{x}" y="{y+4}" text-anchor="middle" fill="#D4AF37" font-family="Goldman,sans-serif" font-size="6">{state[:8]}</text>'
        f"</a>"
    )
states_svg = "\n".join(state_links)
st.markdown(
    f"""
    <div class="prism-frame" style="width:100%; overflow:hidden;">
        <svg id="nigeria-svg" viewBox="0 0 400 500" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <filter id="prism-glow"><feGaussianBlur stdDeviation="2"/><feColorMatrix type="matrix" values="0 0 0 0 0.83 0 0 0 0 0.69 0 0 0 0 0.22 0 0 0 0.6 0"/></filter>
            </defs>
            <path d="{NIGERIA_PATH}" fill="rgba(0,0,51,0.4)" stroke="#D4AF37" stroke-width="2" filter="url(#prism-glow)"/>
            <g class="state-regions">{states_svg}</g>
        </svg>
    </div>
    """,
    unsafe_allow_html=True,
)

# Data Flare: floating popup when a strategic state is clicked
if selected_state and selected_state in STRATEGIC_13:
    st.markdown(
        f'''
        <div class="data-flare">
            <strong>Data Flare — {selected_state}</strong><br/>
            Reserves: 639.3M MT | Potential: 1.2GW
        </div>
        ''',
        unsafe_allow_html=True,
    )
    st.caption(f"Strategic node **{selected_state}** selected. Close by navigating away or refreshing.")

# --- 3. High-Velocity Gauge: AWC VALUATION VELOCITY $0–$170.8B, needle + floating pop-up numbers ---
t = time.time()
gauge_value = max(0, min(1, 0.5 + 0.35 * math.sin(t * 0.25)))  # 0..1
valuation_b = gauge_value * VALUATION_MAX
needle_angle_rad = math.radians(180 * (1 - gauge_value))
needle_x = 100 + 72 * math.cos(needle_angle_rad)
needle_y = 100 - 72 * math.sin(needle_angle_rad)
arc_len = 251
arc_offset = arc_len * (1 - gauge_value)
# Floating numbers: show a few "opportunity gains" that animate upward (HTML/JS)
st.components.v1.html(
    f"""
    <div class="gauge-wrap">
        <div class="gauge-title">AWC VALUATION VELOCITY</div>
        <div style="position:relative;">
            <svg viewBox="0 0 200 120" style="width:100%; height:150px;">
                <defs>
                    <linearGradient id="vg" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#333"/>
                        <stop offset="100%" stop-color="#D4AF37"/>
                    </linearGradient>
                </defs>
                <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="rgba(212,175,55,0.25)" stroke-width="14" stroke-linecap="round"/>
                <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="url(#vg)" stroke-width="10" stroke-linecap="round" stroke-dasharray="{arc_len}" stroke-dashoffset="{arc_offset}"/>
                <line x1="100" y1="100" x2="{needle_x}" y2="{needle_y}" stroke="#D4AF37" stroke-width="3" stroke-linecap="round"/>
                <circle cx="100" cy="100" r="10" fill="#000033" stroke="#D4AF37" stroke-width="2"/>
                <text x="100" y="92" text-anchor="middle" fill="#D4AF37" font-family="Goldman,sans-serif" font-size="10">$0</text>
                <text x="28" y="105" fill="#D4AF37" font-family="Goldman,sans-serif" font-size="8">$0</text>
                <text x="168" y="105" fill="#D4AF37" font-family="Goldman,sans-serif" font-size="8">$170.8B</text>
            </svg>
            <div id="gauge-float-container" style="position:absolute; top:0; left:0; right:0; bottom:0; pointer-events:none;"></div>
            <div style="text-align:center; font-family: Goldman, sans-serif; color: #D4AF37; font-size: 1rem; margin-top: 4px;">${valuation_b:.1f}B</div>
        </div>
    </div>
    <script>
    (function() {{
        var container = document.getElementById('gauge-float-container');
        if (!container) return;
        var values = [2.1, 5.3, 1.8, 4.2, 3.0];
        var idx = 0;
        function spawn() {{
            var n = document.createElement('div');
            n.className = 'floating-num';
            n.textContent = '+' + values[idx % 5] + 'B';
            n.style.left = (50 + (Math.random() * 20 - 10)) + '%';
            n.style.top = '55%';
            container.appendChild(n);
            idx++;
            setTimeout(function() {{ n.remove(); }}, 2100);
        }}
        setInterval(spawn, 1200);
        setTimeout(spawn, 400);
    }})();
    </script>
    """,
    height=220,
)

# --- 4. 8R Determinant Widgets: 8 squares that breathe (zoom in/out) with golden glow ---
st.markdown("#### 8R Determinants")
d8_html = "".join(
    f'<div class="d8-box">{d.split(": ")[0]}<br/>{d.split(": ")[1] if ": " in d else ""}</div>' for d in DETERMINANTS_8R
)
st.markdown(f'<div class="d8-row">{d8_html}</div>', unsafe_allow_html=True)

# --- 5. Cinematic Soundscape (Professional Integration) ---
# Captain: Streamlit renders a visible player by default. Hide the component entirely using CSS
# so the sound feels like an integrated system response, not a website playing a media file.
st.markdown('<style>audio { display: none; }</style>', unsafe_allow_html=True)

st.markdown("#### Sovereign Scan")
# The Handshake (Eagle): autoplay=True triggered by button to satisfy browser security (user gesture required)
initiate = st.button("**INITIATE SOVEREIGN SCAN**", type="primary")
if initiate:
    st.session_state.initiate_triggered = True
    st.rerun()

if st.session_state.initiate_triggered:
    # The Handshake (Eagle): Cinematic Eagle Cry — autoplay once
    if os.path.isfile(EAGLE_CRY_PATH):
        with open(EAGLE_CRY_PATH, "rb") as f:
            st.audio(f.read(), format="audio/mp3", autoplay=True, key="eagle_handshake")
    # The Scan (HUD Chirps): Futuristic HUD Sound Design — loop during data-processing phase
    if os.path.isfile(HUD_CHIRP_PATH):
        with open(HUD_CHIRP_PATH, "rb") as f:
            st.audio(f.read(), format="audio/mp3", autoplay=True, loop=True, key="hud_scan")
    st.caption("Eagle handshake + HUD scan active. Audio components hidden for integrated experience.")
else:
    st.caption("Click **INITIATE SOVEREIGN SCAN** to play the Eagle Cry and Futuristic HUD Sound.")

# --- 6. Signature & Credibility ---
st.markdown('<div class="footer-left">GCSLC / LTD / GTE</div>', unsafe_allow_html=True)
st.markdown('<div class="footer-right">Dr. Jaafaru Sa\'ad — Chairman & Founder</div>', unsafe_allow_html=True)
