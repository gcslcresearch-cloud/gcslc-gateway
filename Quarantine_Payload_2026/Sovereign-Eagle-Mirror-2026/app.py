"""
Sovereign Eagle Mirror 2026 — Initialization (clean slate).
Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026
"""

from __future__ import annotations

from datetime import datetime

import streamlit as st

SHELL = "#000080"
GLASS = "rgba(255, 255, 255, 0.08)"
GOLD = "#D4AF37"
CYAN = "#00E5FF"

st.set_page_config(
    page_title="Sovereign Eagle Mirror 2026",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Viewport: 1:1 scaling for mobile (injected into parent document) ---
st.components.v1.html(
    """
<script>
(function(){
  try {
    var p = window.parent.document;
    if (!p.getElementById('mirror-viewport-meta')) {
      var m = p.createElement('meta');
      m.id = 'mirror-viewport-meta';
      m.name = 'viewport';
      m.content = 'width=device-width, initial-scale=1.0, maximum-scale=5.0, viewport-fit=cover';
      p.head.appendChild(m);
    }
  } catch (e) {}
})();
</script>
""",
    height=0,
    width=0,
)

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap');
/* Kill default Streamlit lavender / theme tint — anchor Eagle Cloud navy everywhere */
html, body {{
  background-color: {SHELL} !important;
  background-image: none !important;
  min-height: 100vh;
}}
.stApp {{
  background-color: {SHELL} !important;
  background-image: none !important;
  color: #f0f4ff !important;
  --background-color: {SHELL} !important;
  --secondary-background-color: {SHELL} !important;
  font-family: 'Goldman', sans-serif !important;
}}
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > section,
[data-testid="stAppViewContainer"] section.main,
section.main,
div.main {{
  background-color: {SHELL} !important;
  background-image: none !important;
}}
[data-testid="block-container"],
[data-testid="stVerticalBlockBorderWrapper"],
.stMainBlockContainer,
[data-testid="stMain"] {{
  background-color: {SHELL} !important;
  background-image: none !important;
}}
[data-testid="stBottomBlockContainer"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] {{
  background-color: {SHELL} !important;
  background: {SHELL} !important;
}}
[data-testid="stHeader"] {{
  background-color: {SHELL} !important;
  background: {SHELL} !important;
}}
[data-testid="stSidebar"] {{
  background-color: {SHELL} !important;
}}
.handshake-wrap {{
  font-family: 'Goldman', sans-serif !important;
  text-align: center;
  padding: 1.25rem 0.75rem 1.5rem;
  touch-action: manipulation;
}}
.layer-typewriter {{
  font-weight: 700;
  font-size: clamp(0.85rem, 2.8vw, 1.15rem);
  color: {CYAN} !important;
  letter-spacing: 0.04em;
  line-height: 1.45;
  min-height: 3.2em;
  text-shadow:
    0 0 1px rgba(0, 0, 0, 0.95),
    0 2px 6px rgba(0, 0, 0, 0.9),
    0 0 18px rgba(0, 0, 0, 0.55),
    0 0 2px rgba(0, 0, 128, 0.9) !important;
}}
.layer-rc {{
  font-weight: 700;
  font-size: clamp(1rem, 3.2vw, 1.35rem);
  color: {GOLD} !important;
  margin-top: 1rem;
  animation: mirror-pulse-zoom 2.4s ease-in-out infinite;
  text-shadow:
    0 0 1px rgba(0, 0, 0, 0.95),
    0 2px 8px rgba(0, 0, 0, 0.88),
    0 0 14px rgba(0, 0, 0, 0.5) !important;
}}
.layer-manifesto {{
  margin-top: 1.25rem;
  font-size: clamp(0.8rem, 2.4vw, 1rem);
  line-height: 1.5;
  font-weight: 700;
  background: linear-gradient(90deg, #001a4d 0%, {GOLD} 35%, #FFE566 50%, {GOLD} 65%, #001a4d 100%);
  background-size: 220% auto;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent !important;
  animation: mirror-manifesto-shimmer 5s linear infinite;
}}
@keyframes mirror-pulse-zoom {{
  0%, 100% {{ transform: scale(1); filter: brightness(1); }}
  50% {{ transform: scale(1.06); filter: brightness(1.25); }}
}}
@keyframes mirror-manifesto-shimmer {{
  0% {{ background-position: 0% 50%; }}
  100% {{ background-position: 200% 50%; }}
}}
/* March 7 white eggshell glass — must read crisp on #000080 (no lavender bleed) */
.mirror-map-glass {{
  position: relative !important;
  background-color: rgba(255, 255, 255, 0.08) !important;
  background-image: linear-gradient(
    165deg,
    rgba(255, 255, 255, 0.14) 0%,
    rgba(255, 255, 255, 0.06) 42%,
    rgba(255, 255, 255, 0.09) 100%
  ) !important;
  backdrop-filter: blur(14px) saturate(1.05) !important;
  -webkit-backdrop-filter: blur(14px) saturate(1.05) !important;
  border-radius: 16px !important;
  border: 1px solid rgba(212, 175, 55, 0.92) !important;
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.42),
    inset 0 -1px 0 rgba(0, 0, 0, 0.12),
    0 4px 24px rgba(0, 0, 0, 0.35),
    0 0 0 1px rgba(255, 255, 255, 0.06) !important;
  touch-action: manipulation !important;
  -webkit-touch-callout: none;
  overflow: hidden;
}}
.mirror-phase-panel {{
  border: 1px solid rgba(212, 175, 55, 0.45);
  border-radius: 12px;
  padding: 12px 14px;
  background: rgba(255, 255, 255, 0.04);
  margin-bottom: 10px;
  touch-action: manipulation !important;
}}
/* Tam-Tam / Dam-Dam anti-screenshot drift bubbles */
.tam-layer {{
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 4;
  overflow: hidden;
}}
.tam-bubble {{
  position: absolute;
  font-family: 'Goldman', sans-serif;
  font-weight: 700;
  font-size: clamp(0.65rem, 1.8vw, 0.85rem);
  letter-spacing: 0.12em;
  color: rgba(212, 175, 55, 0.22);
  white-space: nowrap;
  text-transform: uppercase;
  animation: tam-drift 22s ease-in-out infinite;
}}
.tam-bubble.b2 {{ animation-duration: 28s; animation-delay: -4s; }}
.tam-bubble.b3 {{ animation-duration: 18s; animation-delay: -9s; }}
.tam-bubble.b4 {{ animation-duration: 26s; animation-delay: -2s; }}
@keyframes tam-drift {{
  0%, 100% {{ transform: translate(0,0) rotate(-6deg); opacity: 0.18; }}
  33% {{ transform: translate(8px,-6px) rotate(4deg); opacity: 0.28; }}
  66% {{ transform: translate(-6px,8px) rotate(-3deg); opacity: 0.22; }}
}}
h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown,
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
  font-family: 'Goldman', sans-serif !important;
}}
h1, h2, h3, h4, h5, h6 {{
  color: {GOLD} !important;
  text-shadow:
    0 0 1px rgba(0, 0, 0, 0.9),
    0 2px 6px rgba(0, 0, 0, 0.85) !important;
}}
[data-testid="stMetricValue"] {{
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.75) !important;
}}
[data-testid="stTabs"] {{
  background-color: {SHELL} !important;
}}
[data-testid="stTabs"] [data-baseweb="tab-list"] {{
  background-color: rgba(0, 0, 128, 0.35) !important;
}}
[data-baseweb="tab-panel"] {{
  background-color: {SHELL} !important;
}}
.footer-sovereign {{
  text-align: center;
  padding: 1rem 0.5rem 2rem;
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.72rem;
  letter-spacing: 0.06em;
  color: rgba(212, 175, 55, 0.55) !important;
}}
</style>
""",
    unsafe_allow_html=True,
)

# --- Layer 1–3: Handshake (typewriter + pulse + manifesto via single animated HTML host) ---
_HANDSHAKE_HTML = """
<link href="https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap" rel="stylesheet">
<style>
.hroot { font-family: 'Goldman', sans-serif; text-align: center; padding: 8px 6px 16px; color: #D4AF37;
  background: #000080; }
.tw-line { color: #00E5FF !important; font-weight: 700; font-size: clamp(11px, 2.8vw, 15px); letter-spacing: 0.03em; min-height: 4.5em; line-height: 1.45;
  text-shadow: 0 0 1px rgba(0,0,0,0.95), 0 2px 6px rgba(0,0,0,0.9), 0 0 16px rgba(0,0,0,0.45); }
.rc-line { margin-top: 14px; font-weight: 700; font-size: clamp(13px, 3.2vw, 17px); color: #D4AF37 !important;
  animation: pz 2.4s ease-in-out infinite;
  text-shadow: 0 0 1px rgba(0,0,0,0.95), 0 2px 8px rgba(0,0,0,0.88); }
@keyframes pz { 0%,100%{ transform: scale(1); } 50%{ transform: scale(1.07); } }
.man-line { margin-top: 16px; font-weight: 700; font-size: clamp(10px, 2.4vw, 13px); line-height: 1.55;
  background: linear-gradient(90deg,#001a4d,#D4AF37,#FFE566,#D4AF37,#001a4d); background-size: 220% auto;
  -webkit-background-clip: text; background-clip: text; color: transparent;
  animation: sh 5s linear infinite; }
@keyframes sh { 0%{background-position:0% 50%} 100%{background-position:200% 50%} }
</style>
<div class="hroot">
  <div class="tw-line" id="tw-out"></div>
  <div class="rc-line" id="rc-out" style="opacity:0;">Galadiman Ruwa Nigeria Ltd RC 1871418</div>
  <div class="man-line" id="man-out" style="opacity:0;">Proponent of 8R Paradigm Convergence and its Determinants—come in for you to decode and understand.</div>
</div>
<script>
(function(){
  var full = "Goldman Ruwa Center for Strategic Leadership and Communication GCSLC LTD/GTE";
  var el = document.getElementById("tw-out");
  var rc = document.getElementById("rc-out");
  var mn = document.getElementById("man-out");
  var i = 0;
  var slow = 95;
  function tick(){
    if (i <= full.length) {
      el.textContent = full.slice(0, i);
      i++;
      setTimeout(tick, slow);
    } else {
      setTimeout(function(){ rc.style.opacity = "1"; rc.style.transition = "opacity 1.2s ease"; }, 400);
      setTimeout(function(){ mn.style.opacity = "1"; mn.style.transition = "opacity 1.4s ease"; }, 2200);
    }
  }
  tick();
})();
</script>
"""

st.components.v1.html(_HANDSHAKE_HTML, height=220)

st.markdown("---")

tab_tel, tab_fin, tab_sec, tab_soc = st.tabs(
    ["① Telecom (NCC)", "② Finance (CBN / Banks)", "③ Security (ONSA)", "④ Social & Logistics"]
)

with tab_tel:
    st.markdown(
        '<div class="mirror-phase-panel"><strong>Telecom</strong> — NCC overlays · AZK corridor · signal / fiber bind.</div>',
        unsafe_allow_html=True,
    )
with tab_fin:
    st.markdown(
        '<div class="mirror-phase-panel"><strong>Finance</strong> — CBN / inclusion · ward-gated aggregates.</div>',
        unsafe_allow_html=True,
    )
with tab_sec:
    st.markdown(
        '<div class="mirror-phase-panel"><strong>Security</strong> — ONSA correlation windows · policy automation.</div>',
        unsafe_allow_html=True,
    )
with tab_soc:
    st.markdown(
        '<div class="mirror-phase-panel"><strong>Social & logistics</strong> — Trade pulse · services · fleet contracts.</div>',
        unsafe_allow_html=True,
    )

st.markdown("### National map host — Federation glass")
st.markdown(
    f'''
<div class="mirror-map-glass" style="min-height: 400px; padding: 14px;">
  <div class="tam-layer" aria-hidden="true">
    <span class="tam-bubble" style="top:10%;left:6%;">Tam-Tam · Sovereign</span>
    <span class="tam-bubble b2" style="top:62%;right:8%;">Dam-Dam · GCSLC</span>
    <span class="tam-bubble b3" style="bottom:14%;left:18%;">Proprietary Methodology</span>
    <span class="tam-bubble b4" style="top:38%;right:22%;">176,846 Units · Vigil</span>
  </div>
  <p style="position:relative;z-index:2;text-align:center;color:{GOLD};font-weight:700;margin:0 0 8px 0;font-family:'Goldman',sans-serif;">
    GOOGLE OF NIGERIA — LIVE SOCKET</p>
  <p style="position:relative;z-index:2;text-align:center;font-size:0.88rem;opacity:0.92;margin:0;color:{GOLD};font-family:'Goldman',sans-serif;">
    Vector tiles · PostGIS spine · polling-unit drill-down (Phase bind)</p>
</div>
''',
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("States", "36")
c2.metric("LGAs", "774")
c3.metric("Wards", "8,806")
c4.metric("Polling units", "176,846")


@st.fragment(run_every=60)
def _eagle_vigil_fragment():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    st.caption(f"Eagle vigil · 60s autonomous scan · last tick {ts}")


if hasattr(st, "fragment"):
    _eagle_vigil_fragment()
else:
    st.caption("Eagle vigil · enable Streamlit ≥1.33 for 60s autonomous scans.")

st.markdown(
    """
<div class="footer-sovereign">
  SCUML Certificate · SC 151653884 · Copyright Registration LW15954<br/>
  © 2026 Galadiman Ruwa Center (GCSLC) LTD/GTE · Sovereign-by-Design
</div>
""",
    unsafe_allow_html=True,
)
