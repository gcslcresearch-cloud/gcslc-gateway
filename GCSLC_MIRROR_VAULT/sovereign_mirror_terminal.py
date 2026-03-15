"""
Sovereign High-Velocity Nodal Mirror — System Directive: Start Fresh. Zero Omissions. Institutional Accuracy Only.
Galadiman Ruwa Center for Strategic Leadership and Communication (GCSLC) LTD/GTE.
© 2026 GCSLC. Chairman & Founder: Dr. Sa'ad Jaafaru.
Launch: streamlit run GCSLC_MIRROR_VAULT/sovereign_mirror_terminal.py --server.port 8056
Ido ba mudu bane amma yasan kima. Duniya a ido take.
"""

import base64
import os
import struct
import sys
import math

import streamlit as st

MIRROR_PORT = 8056
_VAULT = os.path.dirname(os.path.abspath(__file__))
_BASE = os.path.dirname(_VAULT)
if _BASE not in sys.path:
    sys.path.insert(0, _BASE)
ASSETS = os.path.join(_BASE, "assets")
EAGLE_AUDIO_PATH = os.path.join(ASSETS, "eagle_swat_fusion.mp3")
HUD_AUDIO_PATH = os.path.join(ASSETS, "hud_chirps.mp3")


def _minimal_chirp_wav_base64():
    """Generate a short SWAT-style digital chirp (two beeps) as WAV base64 for HUD loop."""
    rate = 8000
    duration = 0.5  # seconds
    n = int(rate * duration)
    freq = 880
    samples = []
    for i in range(n):
        t = i / rate
        # Two short beeps
        env = 1.0 if (0.05 < t % 0.2 < 0.12) or (0.15 < t % 0.2 < 0.22) else 0.0
        v = int(127 + 80 * env * math.sin(2 * math.pi * freq * t))
        samples.append(max(0, min(255, v)))
    data = bytes(samples)
    # WAV header: 44 bytes
    chunk = b"RIFF" + struct.pack("<I", 36 + len(data)) + b"WAVE"
    chunk += b"fmt " + struct.pack("<IHHIIHH", 16, 1, 1, rate, rate, 1, 8)
    chunk += b"data" + struct.pack("<I", len(data)) + data
    return base64.b64encode(chunk).decode("ascii")

st.set_page_config(
    page_title="Sovereign High-Velocity Nodal — GCSLC",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- Sovereign Login Gate: session state ----------
SOVEREIGN_KEY = "GCSLC2026"
if "sovereign_authenticated" not in st.session_state:
    st.session_state.sovereign_authenticated = False
if "play_eagle_on_login" not in st.session_state:
    st.session_state.play_eagle_on_login = False
if "security_overlay_visible" not in st.session_state:
    st.session_state.security_overlay_visible = False
if "initiate_triggered" not in st.session_state:
    st.session_state.initiate_triggered = False

# ---------- SOVEREIGN LOGIN GATE: show only when not authenticated ----------
if not st.session_state.sovereign_authenticated:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap');
        .login-gate { min-height: 100vh; background: #000033; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2rem; }
        .login-gate .vault-shield { margin-bottom: 1.5rem; }
        .login-gate .vault-title { font-family: 'Goldman', sans-serif; font-size: clamp(1rem, 2.5vw, 1.35rem); color: #D4AF37; letter-spacing: 0.15em; text-align: center; margin-bottom: 2rem; text-shadow: 0 0 20px rgba(212,175,55,0.5); }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="login-gate">'
        '<div class="vault-shield"><svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="#D4AF37" stroke-width="2"><path d="M12 2L4 5v6.09a7 7 0 0 0 5.5 6.81 7 7 0 0 0 5.5-6.81V5L12 2z"/></svg></div>'
        '<p class="vault-title">GCSLC STRATEGIC VAULT — SECURE ACCESS</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    key_input = st.text_input("Sovereign Key", type="password", key="sovereign_key_input", placeholder="Enter key")
    cent, col2, _ = st.columns([1, 1, 1])
    with col2:
        submitted = st.button("Enter", type="primary", use_container_width=True)
    if submitted:
        if (key_input or "").strip() == SOVEREIGN_KEY:
            st.session_state.sovereign_authenticated = True
            st.session_state.play_eagle_on_login = True
            st.rerun()
        else:
            st.error("Invalid Sovereign Key. Access denied.")
    st.markdown("---")
    st.caption("Galadiman Ruwa Center (GCSLC) LTD/GTE · Authorized personnel only.")
    st.stop()

# 36 states + Abuja (37 territories)
TERRITORIES = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno",
    "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "Gombe", "Imo",
    "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos",
    "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers",
    "Sokoto", "Taraba", "Yobe", "Zamfara", "Abuja",
]
STRATEGIC_13 = {"Enugu", "Kogi", "Gombe", "Benue", "Delta", "Nasarawa", "Anambra", "Plateau", "Adamawa", "Edo", "Bauchi", "Kwara", "Imo"}
# (x,y) for 37 territories in viewBox 0 0 400 520
TERRITORY_POS = [
    (120, 380), (280, 180), (200, 420), (160, 360), (260, 220), (180, 440), (220, 280), (320, 120),
    (240, 420), (140, 400), (200, 340), (120, 340), (80, 360), (200, 320), (300, 200), (160, 380),
    (280, 140), (240, 200), (260, 160), (260, 100), (180, 80), (220, 260), (200, 240), (60, 380),
    (240, 260), (220, 200), (100, 340), (100, 300), (80, 320), (120, 280), (260, 240), (180, 420),
    (180, 60), (300, 260), (320, 160), (240, 120), (220, 240),
]
D8 = ["D1: Refine", "D2: Reset", "D3: Research", "D4: Restructure", "D5: Resuscitate", "D6: Revitalize", "D7: Re-engineer", "D8: Retain"]

NAVY = "#000033"
GOLD = "#D4AF37"
WHITE = "#f8f8ff"
NIGERIA_PATH = "M 45 55 L 355 48 L 378 135 L 365 320 L 355 480 L 55 483 L 22 320 Z"
selected_territory = st.query_params.get("state")
if selected_territory and selected_territory not in TERRITORIES:
    selected_territory = None

# ---------- GLOBAL STYLES: Golden Navy Blue & White, Goldman, calligraphy, prism, security ----------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap');

:root { --navy: #000033; --gold: #D4AF37; --gold-subtle: rgba(212,175,55,0.75); --white: #f8f8ff; }
/* Golden Navy Blue & crisp White palette — institutional accuracy */

.stApp, [data-testid="stAppViewContainer"], .main .block-container { background: var(--navy) !important; }
.main .block-container { padding: 0.6rem 1rem 6rem; max-width: 100%; }

/* 1. Institutional Header — The Command: calligraphy + branding */
.cmd-heading {
    font-family: 'Goldman', serif;
    font-size: clamp(1.6rem, 4vw, 2.4rem);
    font-weight: 700;
    text-align: center;
    color: var(--gold);
    text-shadow: 0 0 24px rgba(212,175,55,0.5);
    letter-spacing: 0.06em;
    margin-bottom: 0.25rem;
    background: linear-gradient(135deg, #D4AF37 0%, #f8f8ff 50%, #D4AF37 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 4s ease-in-out infinite;
}
@keyframes shimmer { 0%,100% { background-position: 0% center; } 50% { background-position: 100% center; } }
.branding {
    font-family: 'Goldman', sans-serif;
    font-size: clamp(0.85rem, 1.8vw, 1.05rem);
    text-align: center;
    color: var(--gold-subtle);
    letter-spacing: 0.08em;
}

/* Global Pulse — live clocks bar */
.pulse-bar { display: flex; flex-wrap: wrap; justify-content: center; gap: 1.25rem; padding: 0.5rem 1rem; background: rgba(0,0,51,0.95); border-bottom: 2px solid var(--gold); }
.pulse-cell { font-family: 'Goldman', sans-serif; color: var(--gold); font-size: 0.85rem; text-align: center; }
.pulse-cell .tz { font-size: 0.7rem; opacity: 0.9; }
.pulse-cell .time { font-weight: 700; }

/* 2. Terrestrial Ground-Base — live-mode map: prism frame on every state territory, 13 strategic in golden */
.map-wrap { position: relative; width: 100%; margin: 1rem 0; }
#nigeria-svg { width: 100%; height: auto; max-height: 440px; }
.prism-frame { filter: drop-shadow(0 0 14px rgba(212,175,55,0.35)); }
.state-region { cursor: pointer; transition: all 0.2s; }
.state-region:hover { filter: brightness(1.15); }
.state-region .state-glow { filter: url(#prism-state); }
.state-region.strategic .state-glow { animation: golden-pulse 2s ease-in-out infinite; }
@keyframes golden-pulse { 0%,100% { filter: url(#prism-state) drop-shadow(0 0 8px rgba(212,175,55,0.6)); } 50% { filter: url(#prism-state) drop-shadow(0 0 20px rgba(212,175,55,0.95)); } }
/* GEC: Eagle moving inside map */
.eagle-moving { position: absolute; left: 50%; top: 45%; transform: translate(-50%,-50%); pointer-events: none; animation: eagle-float 8s ease-in-out infinite; }
@keyframes eagle-float { 0%,100% { transform: translate(-50%,-50%) translateX(0) translateY(0); } 25% { transform: translate(-50%,-50%) translateX(30px) translateY(-20px); } 50% { transform: translate(-50%,-50%) translateX(-20px) translateY(15px); } 75% { transform: translate(-50%,-50%) translateX(15px) translateY(10px); } }

/* 3. Speedometer: needle at $170.8B, numbers pop up/down */
.gauge-wrap { margin: 1rem auto; max-width: 460px; }
.gauge-label { font-family: 'Goldman', sans-serif; color: var(--gold); text-align: center; font-size: 0.95rem; margin-bottom: 0.25rem; }
.pop-up { animation: pop-up 1.8s ease-out forwards; color: #00ff88; }
.pop-down { animation: pop-down 1.8s ease-out forwards; color: #ff6b6b; }
@keyframes pop-up { 0% { opacity: 1; transform: translateY(0) scale(1); } 100% { opacity: 0; transform: translateY(-50px) scale(1.1); } }
@keyframes pop-down { 0% { opacity: 1; transform: translateY(0) scale(1); } 100% { opacity: 0; transform: translateY(30px) scale(1.05); } }

/* 4. Market & Paradigm: Coal/By-products squares, Yearly Cumulative, 8R */
.market-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0; max-width: 700px; margin-left: auto; margin-right: auto; }
.market-square {
    font-family: 'Goldman', sans-serif;
    border: 2px solid var(--gold);
    border-radius: 12px;
    padding: 1rem;
    background: rgba(0,0,51,0.85);
    color: var(--gold);
    text-align: center;
    box-shadow: 0 0 20px rgba(212,175,55,0.2);
}
.market-square h4 { margin: 0 0 0.5rem; font-size: 1rem; }
.market-square .price { font-size: 1.25rem; font-weight: 700; color: var(--white); }
.yearly-cumulative { font-family: 'Goldman', sans-serif; text-align: center; padding: 0.75rem; border: 2px solid var(--gold); border-radius: 10px; background: rgba(0,0,51,0.9); color: var(--gold); margin: 1rem auto; max-width: 500px; }
.d8-row { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; margin: 1rem 0; }
.d8-box { font-family: 'Goldman', sans-serif; font-size: 0.65rem; width: 72px; height: 72px; display: flex; align-items: center; justify-content: center; text-align: center; line-height: 1.2; border: 2px solid var(--gold); border-radius: 8px; background: rgba(0,0,51,0.85); color: var(--gold); animation: d8-breathe 2.6s ease-in-out infinite; }
.d8-box:nth-child(1){ animation-delay: 0s; }
.d8-box:nth-child(2){ animation-delay: 0.15s; }
.d8-box:nth-child(3){ animation-delay: 0.3s; }
.d8-box:nth-child(4){ animation-delay: 0.45s; }
.d8-box:nth-child(5){ animation-delay: 0.6s; }
.d8-box:nth-child(6){ animation-delay: 0.75s; }
.d8-box:nth-child(7){ animation-delay: 0.9s; }
.d8-box:nth-child(8){ animation-delay: 1.05s; }
@keyframes d8-breathe { 0%,100% { transform: scale(1); box-shadow: 0 0 12px rgba(212,175,55,0.3); } 50% { transform: scale(1.06); box-shadow: 0 0 22px rgba(212,175,55,0.5); } }

/* 5. Security: watermark, signature, copyright, shield, protection overlay */
.security-overlay {
    position: fixed; inset: 0; background: rgba(0,0,51,0.92);
    display: flex; align-items: center; justify-content: center;
    z-index: 9997; pointer-events: none;
}
.security-overlay .shield-text { font-family: 'Goldman', sans-serif; font-size: 1.5rem; color: var(--gold); letter-spacing: 0.2em; text-shadow: 0 0 20px rgba(212,175,55,0.6); }
.security-overlay .sub { font-size: 0.85rem; color: var(--gold-subtle); margin-top: 0.5rem; }
.security-overlay .shield-icon { margin-bottom: 0.5rem; }
.watermark-footer { position: fixed; bottom: 0; left: 0; right: 0; padding: 0.4rem 1rem; font-family: 'Goldman', sans-serif; font-size: 0.7rem; color: var(--gold-subtle); background: rgba(0,0,51,0.9); border-top: 1px solid rgba(212,175,55,0.4); z-index: 901; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; }
.sig-seal { border-left: 3px solid var(--gold); padding-left: 0.5rem; }
.stamp-copyright { letter-spacing: 0.05em; }
.credibility-shield { display: inline-flex; align-items: center; gap: 0.35rem; color: var(--gold-subtle); }
/* Chairman's Seal: bottom-right, gold seal border */
.chairman-seal {
    position: fixed; bottom: 0; right: 0; z-index: 902;
    font-family: 'Goldman', sans-serif; font-size: 0.75rem; color: var(--gold);
    padding: 0.5rem 1rem; margin: 0.4rem;
    border: 2px solid var(--gold); border-radius: 8px;
    background: rgba(0,0,51,0.92); box-shadow: 0 0 16px rgba(212,175,55,0.25);
    letter-spacing: 0.04em;
}

/* Hide audio for integrated experience */
audio, [data-testid="stAudio"], .element-container:has(audio) { display: none !important; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------- 1. THE INSTITUTIONAL HEADER (The Command) ----------
st.markdown('<p class="cmd-heading">Sovereign High-Velocity Nodal</p>', unsafe_allow_html=True)
st.markdown('<p class="branding">Galadiman Ruwa Center for Strategic Leadership and Communication (GCSLC) LTD/GTE</p>', unsafe_allow_html=True)
# Lock icon top-right: toggle Security Protection overlay (LinkedIn / screenshot mode)
lock_col1, lock_col2 = st.columns([5, 1])
with lock_col2:
    lock_label = "🔓 Hide overlay" if st.session_state.security_overlay_visible else "🔒 Security"
    if st.button(lock_label, key="security_overlay_toggle", help="Toggle Security Protection overlay for presentation"):
        st.session_state.security_overlay_visible = not st.session_state.security_overlay_visible
        st.rerun()
st.markdown("---")

# Eagle cry on successful login (Chairman's arrival)
if st.session_state.play_eagle_on_login:
    st.session_state.play_eagle_on_login = False
    if os.path.isfile(EAGLE_AUDIO_PATH):
        with open(EAGLE_AUDIO_PATH, "rb") as f:
            st.audio(f.read(), format="audio/mp3", autoplay=True, key="eagle_login")
    st.markdown('<style>audio, [data-testid="stAudio"], .element-container:has(audio){ display: none !important; }</style>', unsafe_allow_html=True)

# ---------- 6. GLOBAL PULSE — live clocks ----------
st.components.v1.html(
    """
    <div class="pulse-bar">
        <div class="pulse-cell"><div class="tz">Zaria (WAT)</div><div class="time" id="wat">--:--:--</div></div>
        <div class="pulse-cell"><div class="tz">London</div><div class="time" id="gmt">--:--:--</div></div>
        <div class="pulse-cell"><div class="tz">Dubai</div><div class="time" id="gst">--:--:--</div></div>
        <div class="pulse-cell"><div class="tz">Singapore</div><div class="time" id="sgt">--:--:--</div></div>
        <div class="pulse-cell"><div class="tz">Silicon Valley</div><div class="time" id="pdt">--:--:--</div></div>
        <div class="pulse-cell"><div class="tz">Wall Street</div><div class="time" id="edt">--:--:--</div></div>
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
    height=56,
)

# ---------- 2. THE TERRESTRIAL BASE — Live map: 36 States + Abuja, prism-frame, 13 strategic golden, GEC Eagle + music ----------
st.markdown("#### The Terrestrial Base — Live Map (36 States + Abuja)")
links = []
for i, name in enumerate(TERRITORIES):
    x, y = TERRITORY_POS[i]
    strat = " strategic" if name in STRATEGIC_13 else ""
    short = (name[:6] if name != "Abuja" else "Abuja")
    links.append(
        f'<a href="?state={name.replace(" ", "%20")}" target="_top" class="state-region{strat}">'
        f'<circle class="state-glow" cx="{x}" cy="{y}" r="13" fill="rgba(0,0,51,0.88)" stroke="#D4AF37" stroke-width="1.8" filter="url(#prism-state)"/>'
        f'<text x="{x}" y="{y+4}" text-anchor="middle" fill="#D4AF37" font-family="Goldman,sans-serif" font-size="6">{short}</text></a>'
    )
states_svg = "\n".join(links)
st.markdown(
    f'''
    <div class="map-wrap prism-frame">
        <svg id="nigeria-svg" viewBox="0 0 400 520" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <filter id="pf"><feGaussianBlur stdDeviation="1.5"/><feColorMatrix type="matrix" values="0 0 0 0 0.83 0 0 0 0 0.69 0 0 0 0 0.22 0 0 0 0.5 0"/></filter>
                <filter id="prism-state"><feGaussianBlur in="SourceGraphic" stdDeviation="2" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
            </defs>
            <path d="{NIGERIA_PATH}" fill="rgba(0,0,51,0.35)" stroke="#D4AF37" stroke-width="2" filter="url(#pf)"/>
            <g class="state-regions">{states_svg}</g>
        </svg>
        <div class="eagle-moving" aria-hidden="true">
            <svg width="48" height="34" viewBox="0 0 56 40"><ellipse cx="28" cy="20" rx="14" ry="10" fill="#D4AF37" stroke="#B8860B" stroke-width="1"/>
            <path d="M18 16 L28 12 L38 16" stroke="#B8860B" fill="none"/><circle cx="24" cy="18" r="2" fill="#1a1a1a"/><circle cx="32" cy="18" r="2" fill="#1a1a1a"/></svg>
        </div>
    </div>
    ''',
    unsafe_allow_html=True,
)
if selected_territory and selected_territory in STRATEGIC_13:
    st.success(f"**{selected_territory}** — 639.3M MT Reserves | 1.2GW Potential | $170.85B Valuation")
elif selected_territory:
    st.caption(f"**{selected_territory}** — Territorial node. Click a strategic node for reserves and valuation.")

# ---------- 3. LIVELY SPEEDOMETER — needle at $170.8B, numbers pop up/down ----------
needle_val = 170.8
needle_angle = math.radians(180 * 0.92)
nx = 100 + 70 * math.cos(needle_angle)
ny = 100 - 70 * math.sin(needle_angle)
st.components.v1.html(
    f"""
    <div class="gauge-wrap">
        <div class="gauge-label">AWC Valuation — $170.8B · Velocity ↑ Friction ↓</div>
        <svg viewBox="0 0 200 120" style="width:100%; height:150px;">
            <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="rgba(212,175,55,0.25)" stroke-width="12" stroke-linecap="round"/>
            <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="#D4AF37" stroke-width="10" stroke-linecap="round" stroke-dasharray="251" stroke-dashoffset="20"/>
            <line x1="100" y1="100" x2="{nx}" y2="{ny}" stroke="#D4AF37" stroke-width="3" stroke-linecap="round"/>
            <circle cx="100" cy="100" r="8" fill="#000033" stroke="#D4AF37"/>
            <text x="28" y="105" fill="#D4AF37" font-family="Goldman,sans-serif" font-size="8">$0</text>
            <text x="158" y="105" fill="#D4AF37" font-family="Goldman,sans-serif" font-size="8">$170.8B</text>
        </svg>
        <div id="pop-container" style="position:relative; height:40px; text-align:center;"></div>
        <div style="text-align:center; font-family: Goldman,sans-serif; color: #D4AF37; font-size: 1.1rem;">$170.8B</div>
        <div style="text-align:center; font-family: Goldman,sans-serif; font-size: 0.75rem; color: rgba(212,175,55,0.85); margin-top: 4px;">Pop-up: Velocity · Pop-down: Friction</div>
    </div>
    <script>
    (function(){{
        var c = document.getElementById('pop-container');
        if (!c) return;
        var ups = [2.1, 5.3, 1.8], downs = [0.5, 1.2];
        var idx = 0;
        function add(cls, val) {{
            var d = document.createElement('div');
            d.className = cls;
            d.style.cssText = 'position:absolute; left:50%; transform:translateX(-50%); font-family: Goldman,sans-serif; font-weight:700; font-size:0.9rem;';
            d.textContent = (cls === 'pop-up' ? '+' : '-') + val + 'B';
            c.appendChild(d);
            setTimeout(function() {{ d.remove(); }}, 1800);
        }}
        setInterval(function() {{
            if (idx % 2 === 0) add('pop-up', ups[Math.floor(idx/2) % 3]);
            else add('pop-down', downs[Math.floor((idx-1)/2) % 2]);
            idx++;
        }}, 2200);
    }})();
    </script>
    """,
    height=260,
)

# ---------- 4. MARKET & PARADIGM WIDGETS ----------
st.markdown("#### Coal & By-products — Current Market")
coal_price = 118
byproducts = "Germanium $2,152/kg · Ammonia $585/MT · Silicon feed $18.27/sq"
st.markdown(
    f"""
    <div class="market-row">
        <div class="market-square">
            <h4>Coal</h4>
            <p class="price">${coal_price}/MT</p>
            <p style="font-size:0.75rem; color: rgba(248,248,255,0.8);">Primary feedstock</p>
        </div>
        <div class="market-square">
            <h4>By-products</h4>
            <p class="price" style="font-size:0.9rem;">{byproducts}</p>
            <p style="font-size:0.75rem; color: rgba(248,248,255,0.8);">Derivative streams</p>
        </div>
    </div>
    <div class="yearly-cumulative">Yearly Cumulative Opportunity — $170.85B valuation anchor (8R Scientific Validation)</div>
    """,
    unsafe_allow_html=True,
)
st.markdown("#### 8R Stealth Paradigm Convergence")
st.caption("Each determinant drives market velocity. Eight determinants proving effect on valuation.")
d8_html = "".join(
    f'<div class="d8-box">{d.split(": ")[0]}<br/>{d.split(": ")[1] if ": " in d else ""}</div>' for d in D8
)
st.markdown(f'<div class="d8-row">{d8_html}</div>', unsafe_allow_html=True)

# ---------- 5. TACTICAL AUDIO-VISUAL SYNC: Eagle/Falcon handshake + HUD chirps (hidden), Security overlay ----------
st.markdown("#### Tactical Audio-Visual Sync")
st.markdown('<style>audio, [data-testid="stAudio"], .element-container:has(audio) { display: none !important; }</style>', unsafe_allow_html=True)
initiate = st.button("**INITIATE** — Cinematic Eagle / Falcon (Security Agency Effect)", type="primary")
if initiate:
    st.session_state.initiate_triggered = True
    st.rerun()

if st.session_state.initiate_triggered:
    if os.path.isfile(EAGLE_AUDIO_PATH):
        with open(EAGLE_AUDIO_PATH, "rb") as f:
            st.audio(f.read(), format="audio/mp3", autoplay=True, key="eagle")
    # HUD chirps: loop SWAT/Rookie-style digital chirps during scan phase (native OS feel, hidden)
    chirp_b64 = _minimal_chirp_wav_base64()
    st.components.v1.html(
        f"""
        <audio id="hud-chirps" loop autoplay style="display:none;">
            <source src="data:audio/wav;base64,{chirp_b64}" type="audio/wav"/>
        </audio>
        <script>
        (function(){{
            var a = document.getElementById('hud-chirps');
            if (a) {{ a.volume = 0.35; a.play().catch(function(){{}}); }}
        }})();
        </script>
        """,
    height=5,
)
    st.caption("Eagle handshake active. HUD chirps looping — scan phase. GEC music with map.")

# Security Protection overlay: toggled by Lock icon (LinkedIn / screenshot mode)
if st.session_state.security_overlay_visible:
    st.markdown(
        """
        <div class="security-overlay">
            <div style="text-align:center;">
                <div class="shield-icon"><svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#D4AF37" stroke-width="1.5"><path d="M12 2L4 5v6.09a7 7 0 0 0 5.5 6.81 7 7 0 0 0 5.5-6.81V5L12 2z"/></svg></div>
                <p class="shield-text">SECURITY PROTECTION</p>
                <p class="sub">Watermark · Signature · Copyright · Shield · Proprietary · Sovereign Data · GCSLC</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- 6. Footer: Copyright (left) + Chairman's Seal (bottom-right, gold border) ----------
st.markdown(
    '<div class="watermark-footer">'
    '<span class="stamp-copyright">© 2026 Galadiman Ruwa Center (GCSLC) LTD/GTE. All rights reserved.</span>'
    '<span class="credibility-shield">🛡 Shield</span>'
    '</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="chairman-seal" aria-label="Chairman signature">Dr. Jaafaru Sa\'ad — Chairman & Founder</div>',
    unsafe_allow_html=True,
)
