#!/usr/bin/env python3
"""
NRRFC Sovereign Vanguard — Node 8855 (rebuild)
Institutional Urgency Format · Pure Streamlit · Port 8855
Launch: streamlit run nvfc_nrrfc_vanguard_8855.py --server.port 8855
"""
from __future__ import annotations

import time
from datetime import timedelta

import streamlit as st

# -----------------------------------------------------------------------------
# Constants (no Streamlit session access before set_page_config + state init)
# -----------------------------------------------------------------------------
BG_NAVY = "#001F3F"
NAVY_DEEP = "#001A33"
SLATE_SILVER = "#C8D0D8"
GOLD = "#FFD700"
TEXT_SLATE = "#E0E0E0"

RESERVES_MT = 640.04
POWER_MW = 1199
LEAKAGE_ANCHOR_B = 1.812
LEAK_TICK_B = 0.01
LEAK_INTERVAL_SEC = 10
WEALTH_MULTIPLIER_9_6 = 9.6

ENTITY_LINE = (
    "Nigerian Green Energy and Chemicals Corporation (NGECC) — Special Strategic Mission Vehicle (SSMV)"
)
GATEWAY_LINE = "Falcon-Class Sovereign Gateway: Seizing the 9.6x Wealth Multiplier"
PARADIGM_LINE = (
    "National Resources Revitalization Fusion Center (NRRFC) — Powered by the 8R Stealth Paradigm Convergence and its Determinants"
)

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

# Per-state reserve share (Mt) for VADS / equity lens — sums ~ portfolio
STATE_RESERVE_MT: dict[str, float] = {
    "Kogi": 142.0,
    "Enugu": 168.0,
    "Benue": 85.0,
    "Nasarawa": 22.0,
    "Adamawa": 48.0,
    "Anambra": 55.0,
    "Delta": 38.0,
    "Plateau": 28.0,
    "Gombe": 32.0,
    "Ondo": 24.0,
    "Abia": 18.0,
    "Bauchi": 44.0,
    "Edo": 36.0,
}

STATE_INTEL = {
    "Kogi": "<strong>Kogi Strike Zone</strong> — Okaba / Ogboyoga strike zones; BUA corridor; syngas & AI-DC alignment.",
    "Enugu": "<strong>Enugu Strike Zone</strong> — Anambra Basin anchor; D1/D3 priority.",
    "Benue": "<strong>Benue Strike Zone</strong> — Central belt reserves; SSMV agro-industrial synergy.",
    "Nasarawa": "<strong>Nasarawa Strike Zone</strong> — Data-center corridor; AZK strategic flank.",
    "Adamawa": "<strong>Adamawa Strike Zone</strong> — NE proven coal; 8R reserve activation.",
    "Anambra": "<strong>Anambra Strike Zone</strong> — Active production; NGECC feedstock linkage.",
    "Delta": "<strong>Delta Strike Zone</strong> — Niger Delta energy corridor; hybrid sovereignty.",
    "Plateau": "<strong>Plateau Strike Zone</strong> — Central highland reserves; mineral co-location.",
    "Gombe": "<strong>Gombe Strike Zone</strong> — NE tier; D2 moribund capture.",
    "Ondo": "<strong>Ondo Strike Zone</strong> — SW coastal flank; export logistics.",
    "Abia": "<strong>Abia Strike Zone</strong> — Aba industrial corridor; SME value chain.",
    "Bauchi": "<strong>Bauchi Strike Zone</strong> — NE tier; Benue Trough NE signature.",
    "Edo": "<strong>Edo Strike Zone</strong> — Benin corridor; high-value feedstock (NRRFC lens).",
}

GEOLOGY = {
    "Kogi": "Okaba / Ogboyoga strike zones · Nupe/Bida basin · Sub-bituminous · Depth 150–450 m · Localized AI power potential: 1,199 MW (13-state portfolio)",
    "Enugu": "Anambra basin · Sub-bituminous · Depth 80–350 m · Cleat well-developed",
    "Benue": "Benue Trough fringe · Folded structure · Depth 200–500 m",
    "Nasarawa": "Middle Benue · Abuja DC arc proximity · Depth 120–400 m",
    "Adamawa": "Chad/Benue influence · Lignite–sub-bituminous · Depth 150–600 m",
    "Anambra": "Anambra basin · Depth 60–300 m · Active production corridor",
    "Delta": "Niger Delta margin · Depth 200–800 m · Overpressure risk moderate",
    "Plateau": "Jos–Bauchi fringe · Depth 100–400 m · Localized intrusions",
    "Gombe": "Benue Trough · Depth 180–500 m",
    "Ondo": "Dahomey/SW margin · Coastal logistics · Depth 150–550 m",
    "Abia": "Imo/Anambra fringe · Industrial density high · Depth 80–280 m",
    "Bauchi": "Benue Trough NE · Depth 200–550 m",
    "Edo": "Benin flank / Dahomey margin · Feedstock signature high-value · Depth 150–450 m",
}


def calculate_gcslc_equity(state: str) -> dict[str, float | str]:
    """
    Value-Added Derivative Strike (VADS) — GCSLC equity lens with 9.6× multiplier.
    Visualizes sovereign uplift index for the selected strike zone.
    """
    mt = STATE_RESERVE_MT.get(state, RESERVES_MT / 13)
    share = mt / max(RESERVES_MT, 1e-6)
    # Uplift index: multiplier × reserve share (normalized institutional signal)
    uplift = WEALTH_MULTIPLIER_9_6 * (0.85 + 0.3 * share)
    strike_code = f"VADS-GCSLC-{state[:3].upper()}-9.6X"
    return {
        "strike_code": strike_code,
        "multiplier": WEALTH_MULTIPLIER_9_6,
        "state_mt": round(mt, 2),
        "reserve_share_pct": round(100.0 * share, 2),
        "equity_uplift_index": round(uplift, 3),
        "implied_cycle_signal_b": round(LEAKAGE_ANCHOR_B * share * WEALTH_MULTIPLIER_9_6 / 9.6, 3),
    }


def _fragment_supported() -> bool:
    return hasattr(st, "fragment")


# =============================================================================
# Streamlit bootstrap — session state MUST initialize before any @st.fragment
# =============================================================================
st.set_page_config(
    page_title="NRRFC Sovereign Vanguard — Node 8855",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "leak_t0" not in st.session_state:
    st.session_state.leak_t0 = time.time()
if "selected_state" not in st.session_state:
    st.session_state.selected_state = None
if "power_highlight" not in st.session_state:
    st.session_state.power_highlight = False

# Goldman font
st.markdown(
    """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap" rel="stylesheet">""",
    unsafe_allow_html=True,
)

# Exact sovereign header (character-for-character per directive)
st.markdown(
    "<h1 style='text-align: center; color: #FFD700; font-family: Goldman, sans-serif;'>GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION (GCSLC) LTD/GTE</h1>",
    unsafe_allow_html=True,
)

# Full institutional CSS: blueprint stream, prism slate→navy, shimmer, S24 zoom ~0.7, header on top
st.markdown(
    f"""
<style>
  @keyframes vg-particles {{
    0% {{ background-position: 0 0, 40px 60px; }}
    100% {{ background-position: 200px 100px, 240px 160px; }}
  }}
  @keyframes vg-blueprint-drift {{
    0% {{ transform: translate(0, 0); }}
    100% {{ transform: translate(-72px, 36px); }}
  }}
  @keyframes vg-shimmer {{
    0% {{ background-position: -150% 0; }}
    100% {{ background-position: 150% 0; }}
  }}
  @keyframes vg-prism-spin {{
    from {{ transform: translate(-50%, -50%) rotate(0deg); }}
    to {{ transform: translate(-50%, -50%) rotate(360deg); }}
  }}
  @keyframes vg-orbit-slow {{
    from {{ transform: rotate(0deg); }}
    to {{ transform: rotate(360deg); }}
  }}
  @keyframes vg-sovereign-ignite {{
    0%, 100% {{ opacity: 0.7; }}
    50% {{ opacity: 0.95; }}
  }}
  .stApp {{
    background-color: {BG_NAVY} !important;
    font-family: 'Goldman', system-ui, sans-serif !important;
    position: relative;
  }}
  .stApp::before {{
    content: '';
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    opacity: 0.38;
    background-image:
      repeating-linear-gradient(0deg, transparent, transparent 46px, rgba(255,215,0,0.055) 47px),
      repeating-linear-gradient(90deg, transparent, transparent 46px, rgba(255,215,0,0.045) 47px),
      radial-gradient(1px 1px at 25% 35%, rgba(255,215,0,0.22), transparent 1px),
      radial-gradient(1px 1px at 75% 65%, rgba(200,208,216,0.18), transparent 1px);
    background-size: 100% 100%, 100% 100%, 200px 200px, 220px 220px;
    animation: vg-particles 26s linear infinite, vg-blueprint-drift 42s linear infinite;
  }}
  /* Central prism: refracting slate silver → navy (no legacy yellow) */
  .vg-prism-vector {{
    position: fixed;
    left: 50%;
    top: 42%;
    width: min(70vw, 500px);
    height: min(70vw, 500px);
    z-index: 1;
    pointer-events: none;
    transform: translate(-50%, -50%);
    opacity: 0.16;
    background:
      conic-gradient(from 30deg at 50% 50%,
        rgba(200,208,216,0.35) 0deg,
        rgba(0,26,51,0.5) 70deg,
        rgba(255,215,0,0.12) 140deg,
        rgba(0,31,63,0.45) 210deg,
        rgba(200,208,216,0.25) 280deg,
        rgba(0,26,51,0.4) 360deg);
    clip-path: polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%);
    animation: vg-prism-spin 55s linear infinite;
    filter: drop-shadow(0 0 10px rgba(255,215,0,0.2));
  }}
  [data-testid="stAppViewContainer"] {{
    position: relative;
    z-index: 2;
    background: transparent !important;
  }}
  [data-testid="stMain"] .block-container,
  section.main .block-container {{
    position: relative;
    z-index: 3;
    padding: 0.35rem 0.5rem !important;
    max-width: 100% !important;
    overflow: hidden !important;
    background: linear-gradient(
      to right,
      rgba(0, 31, 63, 0.94) 0%,
      rgba(0, 26, 51, 0.88) 8%,
      rgba(255, 215, 0, 0.09) 35%,
      rgba(200, 208, 216, 0.06) 48%,
      rgba(0, 26, 51, 0.88) 72%,
      rgba(0, 31, 63, 0.96) 100%
    ) !important;
    background-size: 900px 100%;
    animation: vg-shimmer 17s linear infinite, vg-sovereign-ignite 20s ease-in-out infinite;
    border-radius: 10px;
    box-shadow: 0 0 12px rgba(255, 215, 0, 0.18);
  }}
  /* Samsung S24 Ultra landscape — scale full stack (header + NGECC + 13 grid) */
  @media (max-height: 900px) and (orientation: landscape) {{
    [data-testid="stMain"] .block-container {{ zoom: 0.82; }}
  }}
  @media (max-height: 720px) and (orientation: landscape) {{
    [data-testid="stMain"] .block-container {{ zoom: 0.75; }}
  }}
  @media (max-height: 600px) and (orientation: landscape) {{
    [data-testid="stMain"] .block-container {{ zoom: 0.7; }}
  }}
  @media (max-height: 480px) {{
    [data-testid="stMain"] .block-container {{ zoom: 0.65; }}
  }}
  h1 {{
    position: relative !important;
    z-index: 10050 !important;
    margin: 0.2rem 0 0.35rem 0 !important;
    text-shadow: 0 0 12px rgba(255,215,0,0.25);
  }}
  .vg-auth-stack p {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    color: {GOLD} !important;
    text-align: center;
    margin: 0.12rem 0;
    line-height: 1.3;
    position: relative;
    z-index: 10040;
  }}
  .vg-auth-ngecc {{ font-size: clamp(0.55rem, 1.4vw, 0.82rem); font-weight: 400; }}
  .vg-auth-gateway {{ font-size: clamp(0.54rem, 1.35vw, 0.78rem); font-weight: 700; }}
  .vg-auth-paradigm {{ font-size: clamp(0.52rem, 1.28vw, 0.74rem); font-weight: 400; }}
  .stApp, .stApp * {{
    font-family: 'Goldman', system-ui, sans-serif !important;
  }}
  .vg-section-label {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-weight: 700;
    color: {GOLD};
    font-size: clamp(0.58rem, 1.35vw, 0.76rem);
    margin: 0.25rem 0 0.15rem 0;
  }}
  .vg-body {{
    color: {TEXT_SLATE};
    font-size: clamp(0.52rem, 1.2vw, 0.68rem);
    line-height: 1.35;
  }}
  .vg-geo {{
    color: {TEXT_SLATE};
    font-size: clamp(0.5rem, 1.12vw, 0.64rem);
    line-height: 1.4;
    border-left: 2px solid {GOLD};
    padding-left: 0.45rem;
  }}
  .vg-vads {{
    color: {GOLD};
    font-size: clamp(0.5rem, 1.1vw, 0.65rem);
    font-weight: 700;
    margin-top: 0.35rem;
    padding: 0.35rem;
    border: 1px solid rgba(255,215,0,0.45);
    border-radius: 8px;
    background: rgba(0,26,51,0.65);
  }}
  .vg-leak-wrap {{
    position: relative;
    min-height: 108px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0.15rem 0;
  }}
  .vg-falcon-orbit {{
    position: absolute;
    width: 120px;
    height: 120px;
    left: 50%;
    top: 50%;
    margin-left: -60px;
    margin-top: -60px;
    animation: vg-orbit-slow 52s linear infinite;
    pointer-events: none;
  }}
  .vg-falcon-orbit svg {{
    position: absolute;
    left: 50%;
    top: 0;
    width: 28px;
    height: 22px;
    margin-left: -14px;
    filter: drop-shadow(0 0 6px rgba(255,215,0,0.85));
  }}
  .vg-leak-core {{
    position: relative;
    z-index: 2;
    text-align: center;
    padding: 0.32rem 0.42rem;
    background: rgba(0, 31, 63, 0.88);
    border-radius: 10px;
    border: 1px solid rgba(255,215,0,0.42);
  }}
  .vg-leak-label {{
    font-size: clamp(0.52rem, 1.15vw, 0.66rem);
    color: {GOLD};
    font-weight: 700;
    margin-bottom: 0.1rem;
  }}
  .vg-leak-value {{
    font-size: clamp(1.05rem, 2.9vw, 1.35rem);
    color: {GOLD};
    font-weight: 700;
  }}
  .vg-leak-ticker {{
    font-size: clamp(0.46rem, 1.05vw, 0.58rem);
    color: {TEXT_SLATE};
    text-align: center;
    margin-top: 0.18rem;
  }}
  [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {{
    color: {GOLD} !important;
  }}
  [data-testid="stMain"] .stButton > button {{
    background: rgba(0,40,80,0.92) !important;
    color: {TEXT_SLATE} !important;
    border: 1px solid rgba(255,215,0,0.42) !important;
    border-radius: 8px !important;
    min-height: 1.75rem;
    font-size: clamp(0.55rem, 1.2vw, 0.72rem) !important;
  }}
  [data-testid="stMain"] .stButton > button:hover {{
    border-color: {GOLD} !important;
    color: {GOLD} !important;
  }}
  [data-testid="stSidebar"] {{
    background: rgba(0, 18, 40, 0.99) !important;
    border-right: 1px solid rgba(255,215,0,0.22) !important;
  }}
  header[data-testid="stHeader"] {{
    background: rgba(0, 26, 51, 0.98) !important;
    border-bottom: 1px solid rgba(255, 215, 0, 0.22) !important;
  }}
  [data-testid="stDecoration"] {{ display: none !important; }}
  [data-testid="stToolbar"] {{ background: transparent !important; }}
</style>
<div class="vg-prism-vector" aria-hidden="true"></div>
""",
    unsafe_allow_html=True,
)

# Authority stack — GCSLC identity above is fully visible; NGECC → Falcon → NRRFC
st.markdown(
    f"""
<div class="vg-auth-stack">
  <p class="vg-auth-ngecc">{ENTITY_LINE}</p>
  <p class="vg-auth-gateway">{GATEWAY_LINE}</p>
  <p class="vg-auth-paradigm">{PARADIGM_LINE}</p>
</div>
""",
    unsafe_allow_html=True,
)


def _current_leakage_b() -> float:
    elapsed = max(0.0, time.time() - float(st.session_state["leak_t0"]))
    steps = int(elapsed // LEAK_INTERVAL_SEC)
    return LEAKAGE_ANCHOR_B + steps * LEAK_TICK_B


def _falcon_svg() -> str:
    return """<svg viewBox="0 0 32 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <path fill="#FFD700" stroke="#FFD700" stroke-width="0.45" opacity="0.9"
    d="M16 12 L8 14 L6 12 L8 10 L16 8 L24 10 L26 12 L24 14 Z"/>
  <path fill="#FFD700" opacity="0.95" d="M14 11 L4 8 L2 10 L6 12 Z"/>
  <path fill="#FFD700" opacity="0.95" d="M18 11 L28 8 L30 10 L26 12 Z"/>
  <path fill="#FFD700" opacity="0.8" d="M16 6 L18 4 L20 6 L18 8 Z"/>
</svg>"""


def _render_leakage_block() -> None:
    v = _current_leakage_b()
    st.markdown(
        f"""
<div class="vg-leak-wrap">
  <div class="vg-falcon-orbit" aria-hidden="true">{_falcon_svg()}</div>
  <div class="vg-leak-core">
    <div class="vg-leak-label">Wealth Leakage (anchor ${LEAKAGE_ANCHOR_B:.3f} B · live stream)</div>
    <div class="vg-leak-value">${v:.3f} B</div>
  </div>
</div>
<p class="vg-leak-ticker">NODE 8855 · FALCON ORBIT · 10s CADENCE</p>
""",
        unsafe_allow_html=True,
    )


if _fragment_supported():

    @st.fragment(run_every=timedelta(seconds=LEAK_INTERVAL_SEC))
    def _leakage_fragment() -> None:
        _render_leakage_block()

else:

    def _leakage_fragment() -> None:
        _render_leakage_block()


# --- Sidebar: localized geology + VADS equity ---
with st.sidebar:
    st.markdown('<p class="vg-section-label">STRIKE ZONE PANEL</p>', unsafe_allow_html=True)
    if st.session_state.selected_state:
        sk = st.session_state.selected_state
        st.markdown(f'<div class="vg-body">{STATE_INTEL.get(sk, "")}</div>', unsafe_allow_html=True)
        st.markdown('<p class="vg-section-label" style="margin-top:0.6rem;">LOCALIZED GEOLOGICAL PARAMETERS</p>', unsafe_allow_html=True)
        st.markdown(
            f'<p class="vg-geo">{GEOLOGY.get(sk, "Parameters pending sovereign survey.")}</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<p class="vg-section-label" style="margin-top:0.5rem;">AI POWER (PORTFOLIO)</p>'
            f'<p class="vg-body" style="color:{GOLD};font-weight:700;">1,199 MW AI Power Potential (13-state portfolio)</p>',
            unsafe_allow_html=True,
        )
        vads = calculate_gcslc_equity(sk)
        st.markdown(
            f"""<div class="vg-vads">
<strong>Value-Added Derivative Strike (VADS)</strong><br/>
Code: {vads["strike_code"]}<br/>
9.6× multiplier · Reserve share {vads["reserve_share_pct"]}% ({vads["state_mt"]} Mt)<br/>
Equity uplift index: {vads["equity_uplift_index"]} · Cycle signal: ${vads["implied_cycle_signal_b"]} B
</div>""",
            unsafe_allow_html=True,
        )
        if st.button("Clear selection", key="clear_sel"):
            st.session_state.selected_state = None
            st.rerun()
    else:
        st.markdown(
            '<p class="vg-body">Select a state on the 13-node grid for localized parameters and VADS equity.</p>',
            unsafe_allow_html=True,
        )


# --- Main: mirror + engine + 13-state grid ---
with st.container():
    mirror_col, engine_col = st.columns([1.1, 2.9])
    with mirror_col:
        st.markdown('<p class="vg-section-label">NVFC MIRROR</p>', unsafe_allow_html=True)
        _leakage_fragment()
    with engine_col:
        st.markdown('<p class="vg-section-label">NRRFC ENGINE</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Proven Reserves (13-State)", f"{RESERVES_MT} Mt")
        with c2:
            st.metric("Wealth Leakage (anchor)", f"${LEAKAGE_ANCHOR_B:.3f} B")
        with c3:
            st.metric("AI Power Potential", f"{POWER_MW:,} MW")
        if st.button("1,199 MW — AI Data Center Power Potential", use_container_width=True, key="pwr_alert"):
            st.session_state.power_highlight = True
            st.rerun()
        if st.session_state.power_highlight:
            st.markdown(
                f'<p class="vg-body" style="color:{GOLD};font-weight:700;">ACTION ALERT: 1,199 MW sovereign AI DC potential</p>',
                unsafe_allow_html=True,
            )
        st.markdown('<p class="vg-section-label">13-STATE GEOPOLITICAL GRID</p>', unsafe_allow_html=True)
        for r in range(4):
            ncols = 4 if r < 3 else 1
            chunk = STATES_13[r * 4 : r * 4 + ncols]
            cols = st.columns(ncols)
            for i, st_name in enumerate(chunk):
                with cols[i]:
                    if st.button(st_name, key=f"s13_r{r}_c{i}", use_container_width=True):
                        st.session_state.selected_state = st_name

st.caption("NRRFC Sovereign Vanguard · Node 8855 · GCSLC LTD/GTE")
