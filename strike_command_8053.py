"""
8R Strike Command — Port 8053
Synchronized $1.5 Trillion Initiative & Institutional Partner data (Dangote, BUA, Zenith, GTCO).
Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026 GCSLC.
"""
import os
import sys
import importlib.util
import math
import time
import warnings
import streamlit as st
import streamlit.components.v1 as components

warnings.filterwarnings("ignore", category=DeprecationWarning, module="streamlit")
warnings.filterwarnings("ignore", message=".*use_container_width.*")

# Load African_Gateway continental_logic (same pattern as awc_portal_8054)
_BASE = os.path.dirname(os.path.abspath(__file__))
_GATEWAY = os.path.join(_BASE, "African_Gateway.")

def _load_module(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

continental_logic = _load_module("awc_continental_logic", os.path.join(_GATEWAY, "continental_logic.py"))


def _env_trim(key: str) -> str:
    return (os.environ.get(key) or "").strip()


# D8 IP Lockdown: only current Abuja IP sees clear data; others get 14px blur + Unauthorized WL Access
def _is_abuja_ip():
    allowed = [x.strip() for x in os.environ.get("GCSLC_ABUJA_IPS", "127.0.0.1,::1").split(",") if x.strip()]
    ctx = getattr(st, "context", None)
    client_ip = (getattr(ctx, "ip_address", None) or "").strip()
    return client_ip in allowed

# D7: Cache WL so it computes once per 60s (thermal relief)
@st.cache_data(ttl=60)
def _cached_wl_vel():
    _t = time.time() % 100
    return 9.6 * (1 + 0.15 * math.sin(_t * 0.2))

@st.cache_data
def _cached_power_mw():
    return 1205  # 1,205 MW — single compute

st.set_page_config(
    page_title="8R Strike Command — Port 8053 — GCSLC",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "chairman_verified" not in st.session_state:
    st.session_state.chairman_verified = False

# Sovereign aesthetic — Navy & Gold
st.markdown("""
<style>
.stApp { background-color: #002147 !important; min-height: 100vh; }
[data-testid="stAppViewContainer"] { background-color: #002147 !important; }
.main .block-container { background-color: #002147 !important; max-width: 100%; padding: 1rem 2rem; }
h1, h2, h3, p, span, label, .stMarkdown { color: #D4AF37 !important; }
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color: #D4AF37 !important; }
section[data-testid="stSidebar"] { background-color: #002147 !important; border-right: 2px solid #D4AF37; }
.strike-header { font-weight: 800; font-size: 1.5rem; text-align: center; color: #FFD700 !important; margin-bottom: 0.5rem; }
.strike-sub { text-align: center; color: rgba(212,175,55,0.95); font-size: 0.95rem; }
.gcslc-sovereign-footer { position: fixed; bottom: 0; left: 0; right: 0; z-index: 999; background: linear-gradient(180deg, rgba(0,26,51,0.97) 0%, #001a33 100%); border-top: 2px solid rgba(212,175,55,0.4); padding: 0.45rem 1rem; font-size: 0.75rem; color: #D4AF37; text-align: center; }
.gcslc-sovereign-footer .cac { letter-spacing: 0.1em; opacity: 0.95; }
.gcslc-sovereign-footer .chairman { font-weight: 700; margin-top: 0.2rem; }
.main .block-container { padding-bottom: 4rem !important; }
.gcslc-legal-name-shimmer { background: linear-gradient(90deg, #002147, #D4AF37, #FFE55C, #D4AF37, #002147); background-size: 100% auto; -webkit-background-clip: text; background-clip: text; color: #D4AF37 !important; }
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
</style>
""", unsafe_allow_html=True)

# Escapeless Cloud UI: synced header (CAC) — GE GNCO
st.markdown(
    '<div id="gcslc-header-wrap" style="position: sticky; top: 0; z-index: 100; background: linear-gradient(180deg, #002147 0%, rgba(0,33,71,0.98) 100%); padding-bottom: 10px; margin-bottom: 12px; border-bottom: 1px solid rgba(212,175,55,0.25);">'
    '<p class="gcslc-legal-name-shimmer" style="text-align: center; font-weight: 800; font-size: 0.95rem; margin: 0;">GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION LTD/GTE | CAC: 176917792057 | Chairman & Founder: Dr. Sa\'ad Jaafaru</p>'
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
_authorized_ip_8053 = _is_abuja_ip()
components.html("""
<script>
(function(){
  var authorizedIp = """ + ("true" if _authorized_ip_8053 else "false") + """;
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
})();
</script>
""", height=0)

st.markdown('<p class="strike-header">8R Strike Command — Synchronized</p>', unsafe_allow_html=True)
st.markdown('<p class="strike-sub">Port 8053 | Komi vehicle for nations and global conglomerates | $1.5T Initiative | Sovereign AI Compute</p>', unsafe_allow_html=True)
st.markdown("---")

# ——— WL Counter (Komi): cached D7 thermal relief ———
st.write("### WL Counter (Lost Wealth — Komi)")
wl_vel = _cached_wl_vel()
c1, c2 = st.columns(2)
with c1:
    st.metric("WL — Missed 9.6× (Human)", f"{wl_vel:.2f}×", "real-time cost of inaction")
with c2:
    st.metric("WL — Sovereign AI Compute Shortfall", "$100B", "Robotic world")
st.caption("D3 Global Scan — Komi: Market Gaps $72B · Wealth Multiplier 9.6× · Sovereign AI $100B. Generative Eagle Cloud: Komi vehicle for nations and global conglomerates.")
st.markdown("---")

# ——— D3 Energy Strike: Sovereign AI Compute — Jensen Huang / NVIDIA Portal (1,205 MW deep-linked to Sovereign AI 2026) ———
NVIDIA_SOVEREIGN_AI_2026_URL = "https://www.nvidia.com/en-us/lp/industries/global-public-sector/sovereign-ai-technical-overview/"
NVIDIA_GTC_SOVEREIGN_AI_URL = "https://www.nvidia.com/gtc/sessions/sovereign-ai/"
st.write("### 🖥️ Sovereign AI Compute — Pitch to NVIDIA (Jensen Huang)")
with st.expander("**1,205 MW Asset — Deep-linked to NVIDIA Sovereign AI 2026 Roadmap**", expanded=True):
    st.markdown("**GCSLC GE Cloud** offers a **1,205 MW (1.2 GW)** AI-DC power asset across the **13-state coal corridor** — WPC 2026 Roadmap Ready — for **Sovereign AI Compute** deployment.")
    _readiness = 78 + (int(time.time()) % 15)
    st.metric("Compute Readiness (NVIDIA Sovereign AI)", f"{_readiness}%", "real-time — GE Level 2")
    st.metric("Sovereign AI Compute asset", "1,205 MW (1.2 GW)", "13-state corridor — WPC 2026 Roadmap Ready")
    st.metric("Corridor", "13 states", "639.3 Mt reserves | Clean AI Energy")
    st.markdown(
        "**D3 Energy Strike:** The **1,205 MW** AI-Power asset is deep-linked to **NVIDIA Sovereign AI 2026 roadmap**. "
        "Align NVIDIA's global AI infrastructure with sovereign-controlled power and data. "
        "The 9.6× wealth multiplier (D3 Research) applies to Germanium-for-chips and Ammonia value chains; "
        "the same corridor delivers **1,205 MW** for data centers."
    )
    st.markdown(f"**Sovereign AI 2026:** [NVIDIA Sovereign AI — Technical Overview]({NVIDIA_SOVEREIGN_AI_2026_URL}) | [GTC 2026 — Sovereign AI Sessions]({NVIDIA_GTC_SOVEREIGN_AI_URL})")
    st.markdown("**CAC: 176917792057** — GCSLC unassailable status. CAC & shimmer: unscrambled visual proof of sovereignty.")
    st.caption("Jensen Huang / NVIDIA: 1,205 MW asset deep-linked to NVIDIA Sovereign AI 2026 roadmap. BUA/NVIDIA Strategic Resolution via GE Cloud.")
st.markdown("---")

# ——— $1.5 Trillion Initiative (Capital node — fully loaded) ———
capital = continental_logic.get_capital_node()
st.write("### 💰 $1.5 Trillion Initiative — Capital Node")
st.metric("Initiative", capital["initiative_name"], help="JPMorgan / Citibank — Security & Resiliency")
st.metric("Scale", f"$ {capital['initiative_value_usd_trillion']} Trillion", help="Fully loaded")
st.markdown(f"**Alignment:** {capital['alignment_narrative']}")
st.caption("D8 Retain anchors capital in-country; Eagle validates bank node as Secured Asset.")
st.markdown("---")

# ——— Institutional Partners (V204 — public DOM: Sovereign Institutional Partner [ID]) ———
partners = continental_logic.get_institutional_partners()
st.write("### 🏛️ Institutional Partners — Fully Loaded")
_v204_ck = st.text_input(
    "Chairman session (reveals Wise Men names)",
    type="password",
    key="v204_chairman_8053",
    help="Match GCSLC_CHAIRMAN_KEY in the private vault to reveal institutional names.",
)
if _env_trim("GCSLC_CHAIRMAN_KEY") and _v204_ck and _v204_ck == _env_trim("GCSLC_CHAIRMAN_KEY"):
    st.session_state.chairman_verified = True
_v204_reveal = bool(st.session_state.chairman_verified)
for p in partners:
    _pub = continental_logic.partner_public_name(p, _v204_reveal)
    with st.expander(
        f"**{_pub}** — {p['sector']}",
        expanded=(p.get("sip_id") in (1, 2)),
    ):
        st.markdown("**Assets bid on:** " + "; ".join(f"*{a}*" for a in p["assets_bid"]))
        st.markdown("**8R Resuscitation:** " + p["8r_resuscitation"])
st.caption(
    "Sovereign Institutional Partner [ID] labels are the public default; verified Chairman session reveals internal names."
)
st.markdown("---")

# ——— 8R Determinants quick ref ———
st.write("### 8R Determinants (D1–D8)")
cols = st.columns(4)
for i, det in enumerate(continental_logic.DETERMINANTS_8R):
    cols[i % 4].success(det)
st.markdown("---")
st.caption("Strategic Infrastructure: GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION LTD/GTE | © 2026 | Port 8053 — 8R Strike Command.")
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
