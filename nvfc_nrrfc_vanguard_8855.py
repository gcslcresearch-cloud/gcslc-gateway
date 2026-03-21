#!/usr/bin/env python3
"""
NRRFC Sovereign Vanguard — Node 8855
Pure Streamlit. Goldman typography. Blu-Ray shimmer. Falcon orbit on leakage ticker.
Launch: streamlit run nvfc_nrrfc_vanguard_8855.py --server.port 8855
"""
from __future__ import annotations

import time
import streamlit as st
from datetime import timedelta

# -----------------------------------------------------------------------------
# Design tokens — Pure GCSLC Navy, Radiant Gold (#FFD700), no watermarks
# -----------------------------------------------------------------------------
BG_NAVY = "#001F3F"  # Pure GCSLC Navy Blue
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

# Per-state info panels (HTML <strong> for strike zone titles)
STATE_INTEL = {
    "Kogi": "<strong>Kogi Strike Zone</strong> — Corridor convergence node; BUA-adjacent offtake; coal-to-syngas & AI-DC power alignment.",
    "Enugu": "<strong>Enugu Strike Zone</strong> — Anambra Basin anchor; proven reserves; D1 Refine / D3 Research priority.",
    "Benue": "<strong>Benue Strike Zone</strong> — Central belt reserves; SSMV integration for agro-industrial synergy.",
    "Nasarawa": "<strong>Nasarawa Strike Zone</strong> — Data-center corridor proximity; Abuja–Zaria–Kano strategic flank.",
    "Adamawa": "<strong>Adamawa Strike Zone</strong> — North-East proven coal; reserve activation under 8R determinants.",
    "Anambra": "<strong>Anambra Strike Zone</strong> — Active production profile; NGECC SSMV feedstock linkage.",
    "Delta": "<strong>Delta Strike Zone</strong> — Niger Delta energy corridor; coal + gas hybrid sovereignty narrative.",
    "Plateau": "<strong>Plateau Strike Zone</strong> — Central highland reserves; cold-chain & mineral co-location.",
    "Gombe": "<strong>Gombe Strike Zone</strong> — North-East reserve tier; D2 Reset for moribund sector capture.",
    "Ondo": "<strong>Ondo Strike Zone</strong> — Southwest coastal flank; logistics to export & AI hubs.",
    "Abia": "<strong>Abia Strike Zone</strong> — Aba industrial corridor; SME coal-to-value chain.",
    "Bauchi": "<strong>Bauchi Strike Zone</strong> — North-East reserve tier; D2/D3 cross-border research.",
    "Edo": "<strong>Edo Strike Zone</strong> — Benin industrial corridor; high-value feedstock detection (NRRFC lens).",
}

# Zero-mistake master brand (exact string)
MASTER_BRAND = (
    "Galadiman Ruwa Center for Strategic Leadership and Communication (GCSLC) LTD/GTE"
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
    page_title="NRRFC Sovereign Vanguard — Node 8855",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap" rel="stylesheet">
<style>
  /* Blu-Ray Shimmer — subtle refracting prism (reduced opacity) */
  @keyframes shimmer {{
    0% {{ background-position: -150% 0; }}
    100% {{ background-position: 150% 0; }}
  }}
  html, body, [data-testid="stAppViewContainer"], .stApp {{
    background-color: {BG_NAVY} !important;
    font-family: 'Goldman', system-ui, sans-serif !important;
  }}
  [data-testid="stMain"] .block-container,
  section.main .block-container {{
    padding: 0.45rem 0.65rem !important;
    max-width: 100% !important;
    overflow-x: hidden !important;
    background: linear-gradient(
      to right,
      rgba(0, 26, 51, 0.92) 0%,
      rgba(0, 26, 51, 0.88) 4%,
      rgba(255, 215, 0, 0.14) 28%,
      rgba(192, 192, 192, 0.08) 40%,
      rgba(0, 26, 51, 0.88) 62%,
      rgba(0, 26, 51, 0.95) 100%
    ) !important;
    background-size: 1000px 100%;
    animation: shimmer 18s linear infinite;
    border-radius: 10px;
    box-shadow: 0 0 12px rgba(255, 215, 0, 0.22), inset 0 0 20px rgba(255, 255, 255, 0.03);
  }}
  @media (max-height: 500px) {{
    [data-testid="stMain"] .block-container,
    section.main .block-container {{ padding: 0.25rem 0.4rem !important; }}
    .vg-header-primary {{ font-size: 0.68rem !important; margin: 0 0 0.15rem 0; }}
    .vg-header-secondary {{ font-size: 0.6rem !important; }}
    .vg-gateway {{ font-size: 0.58rem !important; }}
    .vg-command {{ font-size: 0.58rem !important; margin: 0.08rem 0 0.25rem 0; }}
    .vg-dash-title {{ font-size: 0.62rem !important; margin: 0.25rem 0 0.4rem 0; padding-bottom: 0.3rem; }}
  }}
  .stApp, .stApp * {{
    font-family: 'Goldman', system-ui, sans-serif !important;
  }}
  .vg-header-primary {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-weight: 700;
    font-size: clamp(0.8rem, 2.1vw, 1.1rem);
    color: {GOLD};
    text-align: center;
    margin: 0 0 0.3rem 0;
    line-height: 1.22;
    letter-spacing: 0.02em;
  }}
  .vg-header-secondary {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-weight: 400;
    font-size: clamp(0.7rem, 1.75vw, 0.92rem);
    color: {GOLD};
    text-align: center;
    margin: 0 0 0.25rem 0;
    line-height: 1.28;
  }}
  .vg-gateway {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-weight: 700;
    font-size: clamp(0.68rem, 1.65vw, 0.86rem);
    color: {GOLD};
    text-align: center;
    margin: 0.2rem 0;
  }}
  .vg-command {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-weight: 400;
    font-size: clamp(0.65rem, 1.55vw, 0.8rem);
    color: {TEXT_SLATE};
    text-align: center;
    margin: 0.15rem 0 0.45rem 0;
    line-height: 1.32;
  }}
  .vg-dash-title {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-weight: 700;
    font-size: clamp(0.72rem, 1.9vw, 0.95rem);
    color: {TEXT_SLATE};
    text-align: center;
    margin: 0.4rem 0 0.55rem 0;
    border-bottom: 1px solid rgba(255,215,0,0.3);
    padding-bottom: 0.45rem;
  }}
  /* Radiant Gold for primary metric labels + values */
  [data-testid="stMetricLabel"] {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    color: {GOLD} !important;
  }}
  [data-testid="stMetricValue"] {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    color: {GOLD} !important;
  }}
  .vg-section-label {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-weight: 700;
    color: {GOLD};
    font-size: clamp(0.7rem, 1.65vw, 0.85rem);
    margin: 0.45rem 0 0.35rem 0;
    letter-spacing: 0.07em;
  }}
  .vg-body {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    color: {TEXT_SLATE};
    font-size: clamp(0.62rem, 1.45vw, 0.76rem);
    line-height: 1.4;
  }}
  /* Falcon orbit around leakage ticker */
  .vg-leak-wrap {{
    position: relative;
    min-height: 118px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0.25rem 0;
  }}
  .vg-falcon-orbit {{
    position: absolute;
    width: 108px;
    height: 108px;
    left: 50%;
    top: 50%;
    margin-left: -54px;
    margin-top: -54px;
    animation: vg-orbit 22s linear infinite;
    pointer-events: none;
  }}
  @keyframes vg-orbit {{
    from {{ transform: rotate(0deg); }}
    to {{ transform: rotate(360deg); }}
  }}
  .vg-falcon-orbit svg {{
    position: absolute;
    left: 50%;
    top: 0;
    width: 28px;
    height: 21px;
    margin-left: -14px;
    filter: drop-shadow(0 0 4px rgba(255,215,0,0.6));
  }}
  .vg-leak-core {{
    position: relative;
    z-index: 2;
    text-align: center;
    padding: 0.4rem 0.5rem;
    background: rgba(0, 31, 63, 0.75);
    border-radius: 10px;
    border: 1px solid rgba(255,215,0,0.35);
    box-shadow: 0 0 12px rgba(0,0,0,0.25);
  }}
  .vg-leak-label {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-size: clamp(0.62rem, 1.4vw, 0.74rem);
    color: {GOLD};
    font-weight: 700;
    margin-bottom: 0.2rem;
  }}
  .vg-leak-value {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-size: clamp(1.25rem, 3.5vw, 1.55rem);
    color: {GOLD};
    font-weight: 700;
    letter-spacing: 0.04em;
  }}
  .vg-leak-ticker {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-size: clamp(0.55rem, 1.25vw, 0.68rem);
    color: {TEXT_SLATE};
    text-align: center;
    margin-top: 0.35rem;
    opacity: 0.9;
    letter-spacing: 0.05em;
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
  .vg-info-panel {{
    border: 1px solid rgba(255,215,0,0.35);
    border-radius: 10px;
    padding: 0.5rem 0.65rem;
    margin-top: 0.35rem;
    background: rgba(0, 26, 51, 0.55);
    box-shadow: 0 0 10px rgba(255,215,0,0.08);
  }}
  /* Crystal-edge glow on horizontal state-button rows (Streamlit blocks) */
  [data-testid="stMain"] div[data-testid="stHorizontalBlock"] {{
    border-radius: 10px;
    padding: 0.15rem 0 !important;
    margin: 0.12rem 0 !important;
    box-shadow: 0 0 14px rgba(255, 215, 0, 0.1), inset 0 0 12px rgba(255, 255, 255, 0.03);
  }}
</style>
""",
    unsafe_allow_html=True,
)


def _current_leakage_b() -> float:
    elapsed = max(0.0, time.time() - float(st.session_state.leak_t0))
    steps = int(elapsed // LEAK_INTERVAL_SEC)
    return LEAKAGE_ANCHOR_B + steps * LEAK_TICK_B


def _falcon_svg() -> str:
    return """<svg viewBox="0 0 32 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <path fill="#b8962e" stroke="#FFD700" stroke-width="0.5" d="M16 12 L8 14 L6 12 L8 10 L16 8 L24 10 L26 12 L24 14 Z"/>
  <path fill="#FFD700" d="M14 11 L4 8 L2 10 L6 12 Z"/>
  <path fill="#FFD700" d="M18 11 L28 8 L30 10 L26 12 Z"/>
  <path fill="#f0c14b" d="M16 6 L18 4 L20 6 L18 8 Z"/>
</svg>"""


def _render_leakage_block():
    v = _current_leakage_b()
    st.markdown(
        f"""
<div class="vg-leak-wrap">
  <div class="vg-falcon-orbit" aria-hidden="true">{_falcon_svg()}</div>
  <div class="vg-leak-core">
    <div class="vg-leak-label">Sovereign Wealth Leakage</div>
    <div class="vg-leak-value">${v:.3f} B</div>
  </div>
</div>
<p class="vg-leak-ticker">LIVE TICKER · NODE 8855 · 10s CADENCE · STAGNATION COST</p>
""",
        unsafe_allow_html=True,
    )


if _fragment_supported():

    @st.fragment(run_every=timedelta(seconds=LEAK_INTERVAL_SEC))
    def _leakage_fragment():
        _render_leakage_block()

else:

    def _leakage_fragment():
        st.caption("Streamlit ≥1.33 recommended for 10s refresh.")
        _render_leakage_block()


# -----------------------------------------------------------------------------
# Identity & authority — exact copy (9.6x per directive; contextual sub-header)
# -----------------------------------------------------------------------------
with st.container():
    st.markdown(
        f'<p class="vg-header-primary">{MASTER_BRAND}</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="vg-header-secondary">Nigerian Green Energy and Chemicals Corporation (NGECC) — Special Strategic Mission Vehicle (SSMV)</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="vg-gateway">Falcon-Class Sovereign Gateway: Seizing the 9.6x Wealth Multiplier</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="vg-command">National Resources Revitalization Fusion Center (NRRFC) — Powered by the 8R Stealth Paradigm Convergence and its Determinants</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="vg-dash-title">Nigeria Coal Reserves — Real-Time Dashboard | Energy solution for global AI data centers</p>',
        unsafe_allow_html=True,
    )

mirror_col, engine_col = st.columns([1, 3])
with mirror_col:
    with st.container():
        st.markdown('<p class="vg-section-label">NVFC MIRROR</p>', unsafe_allow_html=True)
        _leakage_fragment()

with engine_col:
    with st.container():
        st.markdown('<p class="vg-section-label">NRRFC ENGINE — 13 STATES</p>', unsafe_allow_html=True)
        m1, m2 = st.columns(2)
        with m1:
            st.metric("Proven Reserves (13-State)", f"{RESERVES_MT} Mt")
        with m2:
            st.metric("Power Potential (AI DC ready)", f"{POWER_MW:,} MW")
        if st.button("1,199 MW Power potential for AI Data Centers", use_container_width=True, key="power_alert"):
            st.session_state.power_highlight = True
            st.rerun()
        if st.session_state.power_highlight:
            st.markdown(
                f'<p class="vg-body" style="color:{GOLD};font-weight:700;border:2px solid {GOLD};border-radius:8px;padding:0.35rem;margin:0.25rem 0;">ACTION ALERT: 1,199 MW Power potential for AI Data Centers</p>',
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
    st_ = st.session_state.selected_state
    with st.container():
        st.markdown(
            f'<div class="vg-info-panel"><p class="vg-body">{STATE_INTEL.get(st_, st_)}</p></div>',
            unsafe_allow_html=True,
        )
        if st.button("Clear selection", key="clear_sel"):
            st.session_state.selected_state = None
            st.rerun()

with st.container():
    st.markdown("---")
    st.caption("NRRFC Sovereign Vanguard · Node 8855 · GCSLC LTD/GTE · Streamlit")
