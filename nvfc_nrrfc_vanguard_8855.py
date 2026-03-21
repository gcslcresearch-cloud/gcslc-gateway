#!/usr/bin/env python3
"""
Vanguard National Resources Revitalization Fusion Center (NRRFC) — Node 8855
Pure Streamlit (no Gradio). Goldman typography. NVFC Mirror (left) + NRRFC Engine (main).
Launch: streamlit run nvfc_nrrfc_vanguard_8855.py --server.port 8855
"""
from __future__ import annotations

import time
import streamlit as st
from datetime import timedelta

# -----------------------------------------------------------------------------
# Design tokens (Logo sync — no serif)
# -----------------------------------------------------------------------------
BG_NAVY = "#001F3F"
GOLD = "#FFD700"
TEXT_SLATE = "#E0E0E0"

RESERVES_MT = 640.04
POWER_MW = 1199
LEAKAGE_ANCHOR_B = 1.812
LEAK_TICK_B = 0.01
LEAK_INTERVAL_SEC = 10

STATES_13 = (
    "Kogi",
    "Enugu",
    "Benue",
    "Nasarawa",
    "Adamawa",
    "Anambra",
    "Delta",
    "Plateau",
    "Gombe",
    "Ondo",
    "Abia",
    "Bauchi",
    "Edo",
)

# -----------------------------------------------------------------------------
# Session state
# -----------------------------------------------------------------------------
if "leak_t0" not in st.session_state:
    st.session_state.leak_t0 = time.time()
if "power_highlight" not in st.session_state:
    st.session_state.power_highlight = False
if "selected_state" not in st.session_state:
    st.session_state.selected_state = None


def _fragment_supported() -> bool:
    return hasattr(st, "fragment")


st.set_page_config(
    page_title="GCSLC Vanguard — Node 8855",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Goldman only for headers & metrics; deepest navy background; no watermarks
st.markdown(
    f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap" rel="stylesheet">
<style>
  html, body, [data-testid="stAppViewContainer"], .stApp {{
    background-color: {BG_NAVY} !important;
    font-family: 'Goldman', system-ui, sans-serif !important;
  }}
  .block-container {{
    padding-top: 0.5rem !important;
    padding-bottom: 0.5rem !important;
    max-width: 100% !important;
    overflow-x: hidden !important;
  }}
  /* S24 Ultra / iPhone landscape: flexbox single-screen, no scroll */
  .vg-flex-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    align-items: flex-start;
    min-height: 0;
  }}
  @media (max-height: 500px) {{
    .block-container {{ padding-top: 0.25rem !important; padding-bottom: 0.25rem !important; }}
    .vg-header-primary {{ font-size: 0.72rem !important; margin: 0 0 0.2rem 0; }}
    .vg-header-secondary {{ font-size: 0.6rem !important; margin: 0 0 0.15rem 0; }}
    .vg-gateway {{ font-size: 0.6rem !important; margin: 0.15rem 0; }}
    .vg-command {{ font-size: 0.58rem !important; margin: 0.1rem 0 0.3rem 0; }}
    .vg-dash-title {{ font-size: 0.65rem !important; margin: 0.3rem 0 0.5rem 0; padding-bottom: 0.35rem; }}
  }}
  /* No serif anywhere in app chrome */
  .stApp, .stApp * {{
    font-family: 'Goldman', system-ui, sans-serif !important;
  }}
  .vg-header-primary {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-weight: 700;
    font-size: clamp(0.85rem, 2.2vw, 1.15rem);
    color: {GOLD};
    text-align: center;
    margin: 0 0 0.35rem 0;
    line-height: 1.25;
    letter-spacing: 0.02em;
  }}
  .vg-header-secondary {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-weight: 400;
    font-size: clamp(0.72rem, 1.8vw, 0.95rem);
    color: {GOLD};
    text-align: center;
    margin: 0 0 0.3rem 0;
    opacity: 0.95;
    line-height: 1.3;
  }}
  .vg-gateway {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-weight: 700;
    font-size: clamp(0.7rem, 1.7vw, 0.88rem);
    color: {GOLD};
    text-align: center;
    margin: 0.25rem 0;
  }}
  .vg-command {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-weight: 400;
    font-size: clamp(0.68rem, 1.6vw, 0.82rem);
    color: {TEXT_SLATE};
    text-align: center;
    margin: 0.2rem 0 0.5rem 0;
    line-height: 1.35;
  }}
  .vg-dash-title {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-weight: 700;
    font-size: clamp(0.78rem, 2vw, 1rem);
    color: {TEXT_SLATE};
    text-align: center;
    margin: 0.5rem 0 0.75rem 0;
    border-bottom: 1px solid rgba(255,215,0,0.35);
    padding-bottom: 0.5rem;
  }}
  [data-testid="stMetricLabel"] {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    color: {TEXT_SLATE} !important;
  }}
  [data-testid="stMetricValue"] {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    color: {GOLD} !important;
  }}
  [data-testid="stMetricDelta"] {{
    font-family: 'Goldman', system-ui, sans-serif !important;
  }}
  .vg-metric-power-highlight {{
    border: 2px solid {GOLD};
    border-radius: 12px;
    padding: 0.5rem 0.35rem 0.65rem 0.35rem;
    background: linear-gradient(180deg, rgba(255,215,0,0.12) 0%, rgba(0,31,63,0.4) 100%);
    box-shadow: 0 0 24px rgba(255,215,0,0.45), inset 0 0 20px rgba(255,215,0,0.08);
  }}
  .vg-leak-ticker {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-size: clamp(0.65rem, 1.5vw, 0.8rem);
    color: {TEXT_SLATE};
    text-align: center;
    margin-top: 0.25rem;
    opacity: 0.9;
    letter-spacing: 0.06em;
  }}
  .stButton > button {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    background: rgba(0,40,80,0.92) !important;
    color: {TEXT_SLATE} !important;
    border: 1px solid rgba(255,215,0,0.4) !important;
    border-radius: 8px !important;
  }}
  .stButton > button:hover {{
    border-color: {GOLD} !important;
    color: {GOLD} !important;
    box-shadow: 0 0 12px rgba(255,215,0,0.25);
  }}
  .vg-section-label {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-weight: 700;
    color: {GOLD};
    font-size: clamp(0.75rem, 1.8vw, 0.9rem);
    margin: 0.75rem 0 0.5rem 0;
    letter-spacing: 0.08em;
  }}
  .vg-body {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    color: {TEXT_SLATE};
    font-size: clamp(0.65rem, 1.5vw, 0.78rem);
  }}
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Leakage rhythm: anchor $1.812B, +$0.01B every 10s (time-based, no first-tick jump)
# -----------------------------------------------------------------------------
def _current_leakage_b() -> float:
    elapsed = max(0.0, time.time() - float(st.session_state.leak_t0))
    steps = int(elapsed // LEAK_INTERVAL_SEC)
    return LEAKAGE_ANCHOR_B + steps * LEAK_TICK_B


def _render_leakage_block():
    st.metric(
        "Sovereign Wealth Leakage",
        f"${_current_leakage_b():.3f} B",
        help="Cumulative sector moribund cost — +$0.01 B each 10s cadence",
    )
    st.markdown(
        '<p class="vg-leak-ticker">LIVE TICKER · NODE 8855 · 10s CADENCE</p>',
        unsafe_allow_html=True,
    )


if _fragment_supported():

    @st.fragment(run_every=timedelta(seconds=LEAK_INTERVAL_SEC))
    def _leakage_fragment():
        _render_leakage_block()

else:

    def _leakage_fragment():
        st.caption(
            "Streamlit ≥1.33 recommended for 10s auto-refresh; value still correct on manual rerun."
        )
        _render_leakage_block()


# -----------------------------------------------------------------------------
# Main layout — containers for mobile landscape (S24 Ultra / iPhone)
# -----------------------------------------------------------------------------
with st.container():
    st.markdown(
        '<p class="vg-header-primary">Galadiman Ruwa Center for Strategic Leadership and Communication (GCSLC) LTD/GTE</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="vg-header-secondary">Nigerian Green Energy and Chemicals Corporation (NGECC) — Special Strategic Mission Vehicle (SSMV)</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="vg-gateway">Falcon-Class Sovereign Gateway: Seizing the 9.6× Wealth Multiplier</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="vg-command">National Resources Revitalization Fusion Center (NRRFC) — Powered by the 8R Stealth Paradigm Convergence and its Determinants</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="vg-dash-title">Nigeria Coal Reserves — Real-Time Dashboard | Galadiman Ruwa- GCSLC Sovereign Energy solution for global AI data centers</p>',
        unsafe_allow_html=True,
    )

# NVFC Mirror (Left) | NRRFC Engine (Main) — flexbox-style single-screen layout
mirror_col, engine_col = st.columns([1, 3])
with mirror_col:
    with st.container():
        st.markdown('<p class="vg-section-label">NVFC MIRROR</p>', unsafe_allow_html=True)
        _leakage_fragment()

with engine_col:
    with st.container():
        st.markdown('<p class="vg-section-label">NRRFC ENGINE — 13 STATES</p>', unsafe_allow_html=True)
        st.metric("Proven Reserves (13-State)", f"{RESERVES_MT} Mt", help="Primary metric")
        if st.button("1,199 MW Power potential for AI Data Centers", use_container_width=True, key="power_alert"):
            st.session_state.power_highlight = True
            st.rerun()
        if st.session_state.power_highlight:
            st.markdown(
                f'<p class="vg-body" style="color:{GOLD};font-weight:700;border:2px solid {GOLD};border-radius:8px;padding:0.4rem;margin-top:0.3rem;">ACTION ALERT: 1,199 MW Power potential for AI Data Centers</p>',
                unsafe_allow_html=True,
            )
        n_cols = 4
        rows = [STATES_13[i : i + n_cols] for i in range(0, len(STATES_13), n_cols)]
        for row_states in rows:
            cols = st.columns(len(row_states))
            for col, state in zip(cols, row_states):
                with col:
                    if st.button(state, key=f"st_{state}", use_container_width=True):
                        st.session_state.selected_state = state

if st.session_state.selected_state:
    with st.container():
        st.markdown(
            f'<p class="vg-body"><strong style="color:{GOLD}">Selected:</strong> {st.session_state.selected_state}</p>',
            unsafe_allow_html=True,
        )
        if st.button("Clear selection", key="clear_sel"):
            st.session_state.selected_state = None
            st.rerun()

with st.container():
    st.markdown("---")
    st.caption("Vanguard NRRFC · Node 8855 · GCSLC LTD/GTE · Streamlit")
