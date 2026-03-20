"""
Sovereign Mirror — GCSLC Legal Vault Air-Lock (Streamlit)
Galadiman Ruwa Center for Strategic Leadership and Communication (GCSLC) LTD/GTE.

Backend preserved:
  - African_Gateway continental_logic → Universal Impact Radar (post-decode)
  - Session decode gate (8R-DECODE-2026)
  - Primary node targets: NRRFC 8090, NWC 8053, K-GEC 8054 (env-overridable URLs)

Frontend: Sovereign Vault aesthetic only (navy vault + metallic gold; prior UI removed).
"""

from __future__ import annotations

import importlib.util
import os
import sys

import streamlit as st

# --- African_Gateway load (Universal Impact Radar after decode) ---
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


# --- Primary nodes (backend targets; override for deployment) ---
NRRFC_URL = os.environ.get("GCSLC_NRRFC_URL", "http://127.0.0.1:8090")
NWC_URL = os.environ.get("GCSLC_NWC_URL", "http://127.0.0.1:8053")
KGEC_URL = os.environ.get("GCSLC_KGEC_URL", "http://127.0.0.1:8054")

st.set_page_config(
    page_title="Sovereign Mirror | GCSLC Vault",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "mirror_decoded" not in st.session_state:
    st.session_state.mirror_decoded = False

# --- Copy / data (backend-adjacent constants) ---
PASSWORD_UNLOCK = "8R-DECODE-2026"
FULL_NAME = "Galadiman Ruwa Center for Strategic Leadership and Communication (GCSLC) LTD/GTE"
SIGNATURE = "Dr. Jaafaru Sa'ad — Chairman & Founder"
TICKER_TEXT = (
    "COAL [NGECC]: $170.8B INDEX  |  SILICON FEEDSTOCK: 639.3M MT  |  "
    "GERMANIUM PULSE: ACTIVE  |  ABUJA-ZARIA-KANO CORRIDOR"
)
PULSE_LINE = "Germanium $8,597/kg  ·  Silicon $1.81/kg  ·  Ammonia $650/MT"

STATE_NODES = (
    "Enugu", "Kogi", "Gombe", "Benue", "Delta", "Nasarawa", "Anambra",
    "Plateau", "Adamawa", "Edo", "Bauchi", "Kwara", "Imo",
)

# --- Sovereign Vault: single CSS surface (replaces all prior mirror styling) ---
VAULT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap');

:root {
  --vault-navy: #000510;
  --vault-navy-mid: #0a1020;
  --vault-gold: #D4AF37;
  --vault-gold-dim: rgba(212, 175, 55, 0.45);
  --vault-ink: #c9c4b8;
}

html, body, .stApp, [data-testid="stAppViewContainer"] {
  background: var(--vault-navy) !important;
  color: var(--vault-ink) !important;
}

.main .block-container {
  padding: 1rem 1.25rem 5rem !important;
  max-width: 1200px !important;
  font-family: 'Goldman', system-ui, sans-serif !important;
}

h1, h2, h3, h4, p, span, label { font-family: 'Goldman', system-ui, sans-serif !important; }

/* Streamlit chrome */
header[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }

/* Vault title */
.vault-apex {
  text-align: center;
  padding: 0.75rem 0 1rem;
  border-bottom: 1px solid var(--vault-gold-dim);
  margin-bottom: 1rem;
}
.vault-apex h1 {
  margin: 0;
  font-size: clamp(1.05rem, 2.4vw, 1.45rem);
  font-weight: 700;
  letter-spacing: 0.06em;
  background: linear-gradient(110deg, #bf953f, #fcf6ba, #D4AF37, #aa771c);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: vault-shine 5s linear infinite;
}
@keyframes vault-shine { to { background-position: 200% center; } }
.vault-sub {
  margin: 0.5rem 0 0;
  font-size: 0.72rem;
  letter-spacing: 0.14em;
  color: var(--vault-gold);
  opacity: 0.9;
}

/* Pulse rail */
.vault-pulse {
  border: 1px solid var(--vault-gold-dim);
  background: rgba(0, 5, 16, 0.85);
  border-radius: 8px;
  padding: 0.5rem 0.85rem;
  margin-bottom: 1.25rem;
  font-size: 0.78rem;
  color: var(--vault-gold);
  letter-spacing: 0.04em;
}

/* Node portals */
.vault-nodes {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.85rem;
  margin-bottom: 1.25rem;
}
@media (max-width: 900px) { .vault-nodes { grid-template-columns: 1fr; } }

.vault-slab {
  border: 1px solid var(--vault-gold);
  border-radius: 10px;
  background: rgba(0, 5, 16, 0.72);
  padding: 1rem 0.9rem;
  box-shadow: inset 0 0 0 1px rgba(212, 175, 55, 0.08);
}
.vault-slab .port {
  display: inline-block;
  font-size: 0.65rem;
  font-weight: 700;
  letter-spacing: 0.18em;
  color: var(--vault-navy);
  background: var(--vault-gold);
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
}
.vault-slab h3 {
  margin: 0.5rem 0 0.35rem;
  font-size: 0.95rem;
  color: var(--vault-gold) !important;
}
.vault-slab p {
  margin: 0;
  font-size: 0.78rem;
  line-height: 1.45;
  color: var(--vault-ink) !important;
  opacity: 0.92;
}
.vault-slab a {
  display: inline-block;
  margin-top: 0.65rem;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--vault-gold) !important;
  text-decoration: none;
  border-bottom: 1px solid var(--vault-gold-dim);
}
.vault-slab a:hover { opacity: 0.85; }

/* 13-state strip */
.vault-registry {
  border-left: 3px solid var(--vault-gold);
  padding: 0.65rem 0.85rem;
  background: rgba(0, 5, 16, 0.5);
  margin: 1rem 0;
  font-size: 0.72rem;
  color: var(--vault-ink);
  line-height: 1.6;
}

/* Decode zone */
.vault-gate {
  border: 1px solid var(--vault-gold-dim);
  border-radius: 10px;
  padding: 1rem 1.1rem;
  background: rgba(0, 5, 16, 0.55);
  margin-top: 0.5rem;
}
.vault-gate h4 {
  margin: 0 0 0.5rem;
  color: var(--vault-gold) !important;
  font-size: 0.85rem;
  letter-spacing: 0.1em;
}

.stTextInput input {
  background: var(--vault-navy) !important;
  color: #fff !important;
  border: 1px solid var(--vault-gold) !important;
  border-radius: 8px !important;
  font-family: 'Goldman', sans-serif !important;
}
.stButton > button {
  font-family: 'Goldman', sans-serif !important;
  background: var(--vault-gold) !important;
  color: var(--vault-navy) !important;
  border: none !important;
  border-radius: 8px !important;
  font-weight: 700 !important;
}
.stButton > button:hover {
  filter: brightness(1.08);
}

/* Fixed ticker + seal */
.vault-ticker {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 900;
  background: rgba(0, 5, 16, 0.96);
  border-top: 1px solid var(--vault-gold-dim);
  padding: 0.4rem 0;
  overflow: hidden;
}
.vault-ticker-inner {
  display: inline-block;
  white-space: nowrap;
  animation: vault-scroll 40s linear infinite;
  padding-left: 100%;
  font-size: 0.72rem;
  letter-spacing: 0.1em;
  color: var(--vault-gold);
}
@keyframes vault-scroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-100%); }
}
.vault-seal {
  position: fixed;
  bottom: 2.35rem;
  left: 0.75rem;
  z-index: 901;
  font-size: 0.62rem;
  color: var(--vault-gold-dim);
  letter-spacing: 0.06em;
  max-width: 70vw;
}

/* Post-decode bridge (vault tone) */
.vault-bridge {
  text-align: center;
  padding: 2rem 1rem;
  border: 1px solid var(--vault-gold-dim);
  border-radius: 12px;
  background: rgba(0, 5, 16, 0.65);
  margin-bottom: 1rem;
}
.vault-bridge h2 {
  color: var(--vault-gold) !important;
  letter-spacing: 0.2em;
  font-size: 1.1rem;
}
</style>
"""

st.markdown(VAULT_CSS, unsafe_allow_html=True)


# --- Post-decode: same continental logic / radar (backend unchanged) ---
if st.session_state.mirror_decoded:
    st.markdown(
        """
        <div class="vault-bridge">
            <h2>VAULT UNSEALED</h2>
            <p style="color:rgba(201,196,184,0.9);font-size:0.85rem;margin:0;">
                Decode verified. Universal Impact Radar — live fusion.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### Universal Impact Radar")
    st.caption(
        "How the **$170.85B** anchor and **8R Strike on Atoms** (Energy/Minerals) drive Jobs, Security, and Health."
    )
    continental_logic = _get_continental_logic()
    radar_t1, radar_t2, radar_t3 = st.tabs(
        ["National Security Impact", "Social Well-being Index", "Sovereign Well-being Index"]
    )
    with radar_t1:
        st.write("**National Security Impact** — $170.85B anchor → regional stability")
        sec_heat = continental_logic.get_national_security_impact_heatmap()
        st.dataframe(
            [
                {
                    "Region": r["region"],
                    "Indicator": r["indicator"],
                    "Before anchor": r["before_anchor"],
                    "After anchor": r["after_anchor"],
                    "Δ Stability": r["stability_delta"],
                }
                for r in sec_heat
            ],
            use_container_width=True,
            hide_index=True,
        )
        st.caption(
            "Higher scores = more stability. The anchor increases sovereign retention and reduces resource conflict."
        )
    with radar_t2:
        st.write("**Social Well-being Index** — $170.85B anchor → poverty reduction")
        soc_heat = continental_logic.get_social_wellbeing_index_heatmap()
        st.dataframe(
            [
                {
                    "Dimension": d["dimension"],
                    "Baseline (%)": d["baseline_pct"],
                    "Post-anchor (%)": d["post_anchor_pct"],
                    "Change": d["reduction"],
                }
                for d in soc_heat
            ],
            use_container_width=True,
            hide_index=True,
        )
        st.caption(
            "Poverty headcount drops; employment and energy access rise under 8R sovereign corridors."
        )
    with radar_t3:
        st.write("**Sovereign Well-being Index** — 8R Strike on Atoms → Jobs, Security, Health")
        swi = continental_logic.get_sovereign_wellbeing_index()
        st.dataframe(
            [
                {
                    "Atoms domain": r["atoms_domain"],
                    "Well-being": r["wellbeing_dimension"],
                    "Metric": r["metric"],
                    "Before 8R": r["before_8r"],
                    "After 8R": r["after_8r"],
                    "Unit": r["unit"],
                }
                for r in swi
            ],
            use_container_width=True,
            hide_index=True,
        )
        st.caption(
            "The Eagle's strike on Energy and Minerals generates Jobs (FTE), Security (index), and Health (compliance / air quality)."
        )
    st.markdown(
        f'<div class="vault-ticker"><div class="vault-ticker-inner">{TICKER_TEXT} · {TICKER_TEXT}</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="vault-seal">{SIGNATURE}</div>', unsafe_allow_html=True)
    st.stop()


# --- Air-lock: Sovereign Vault face (no legacy layout) ---
st.markdown(
    f"""
    <div class="vault-apex">
        <h1>{FULL_NAME}</h1>
        <p class="vault-sub">SOVEREIGN MIRROR · LEGAL VAULT AIR-LOCK</p>
    </div>
    <div class="vault-pulse"><strong>PULSE</strong> — {PULSE_LINE}</div>
    <div class="vault-nodes">
        <div class="vault-slab">
            <span class="port">8090</span>
            <h3>NRRFC</h3>
            <p>National Resources Revitalization Fusion Center. Coal-to-chemicals &amp; 1.2 GW AI–DC engine.</p>
            <a href="{NRRFC_URL}" target="_blank" rel="noopener noreferrer">Open node →</a>
        </div>
        <div class="vault-slab">
            <span class="port">8053</span>
            <h3>NWC / C&amp;D</h3>
            <p>National Wealth Cloud. 37-node geopolitical grid &amp; sovereign materiality.</p>
            <a href="{NWC_URL}" target="_blank" rel="noopener noreferrer">Open node →</a>
        </div>
        <div class="vault-slab">
            <span class="port">8054</span>
            <h3>K-GEC</h3>
            <p>Komi Generative Eagle Cloud. Proprietary $170.85B global AI anchor.</p>
            <a href="{KGEC_URL}" target="_blank" rel="noopener noreferrer">Open node →</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f'<div class="vault-registry"><strong>13-State registry</strong> — {" · ".join(STATE_NODES)}</div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="vault-gate"><h4>ACCESS · UNIVERSAL IMPACT RADAR</h4></div>', unsafe_allow_html=True)
pwd = st.text_input(
    "Decode phrase",
    type="password",
    placeholder="Vault decode phrase",
    key="mirror_pwd",
    label_visibility="collapsed",
)
c1, c2, _ = st.columns([1, 1, 2])
with c1:
    submit = st.button("Decode", use_container_width=True)
if submit and pwd.strip() == PASSWORD_UNLOCK:
    st.session_state.mirror_decoded = True
    st.rerun()
elif submit and pwd:
    st.caption("Incorrect decode phrase.")

st.markdown(
    f'<div class="vault-ticker"><div class="vault-ticker-inner">{TICKER_TEXT} · {TICKER_TEXT}</div></div>',
    unsafe_allow_html=True,
)
st.markdown(f'<div class="vault-seal">{SIGNATURE}</div>', unsafe_allow_html=True)
