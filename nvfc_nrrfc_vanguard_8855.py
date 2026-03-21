#!/usr/bin/env python3
"""
NRRFC Vanguard — Node 8855 · Institutional Urgency Format
Particle/blueprint stream, vector prism, 12-cell grid, geology sidebar.
Launch: streamlit run nvfc_nrrfc_vanguard_8855.py --server.port 8855
"""
from __future__ import annotations

import time
import streamlit as st
from datetime import timedelta

BG_NAVY = "#001F3F"
GOLD = "#FFD700"
TEXT_SLATE = "#E0E0E0"

RESERVES_MT = 640.04
POWER_MW = 1199
LEAKAGE_ANCHOR_B = 1.812
LEAK_TICK_B = 0.01
LEAK_INTERVAL_SEC = 10

# Char-for-char identity
MASTER_BRAND = (
    "Galadiman Ruwa Center for Strategic Leadership and Communication (GCSLC) LTD/GTE"
)
ENTITY_LINE = (
    "Nigerian Green Energy and Chemicals Corporation (NGECC) — Special Strategic Mission Vehicle (SSMV)"
)

# 12 clickable nodes (video sync): Bauchi + Edo share one container
GRID_12_KEYS = (
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
    "Bauchi / Edo",
)

STATE_INTEL = {
    "Kogi": "<strong>Kogi Strike Zone</strong> — Corridor convergence; BUA-adjacent offtake; syngas & AI-DC alignment.",
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
    "Bauchi / Edo": "<strong>Bauchi / Edo Dual Node</strong> — NE cross-border research (Bauchi) + Benin corridor feedstock (Edo); unified NGECC lens.",
}

# Localized geological parameters (sidebar)
GEOLOGY = {
    "Kogi": "Basin: Nupe / Bida · Rank: sub-bituminous · Depth est.: 150–450 m · Sulfur: medium · Seismic: low",
    "Enugu": "Basin: Anambra · Rank: sub-bituminous · Depth est.: 80–350 m · Cleat: well-developed · Seismic: low",
    "Benue": "Basin: Benue Trough fringe · Rank: sub-bituminous · Depth est.: 200–500 m · Structure: folded · Seismic: low–moderate",
    "Nasarawa": "Basin: Middle Benue · Rank: sub-bituminous · Depth est.: 120–400 m · Proximity: Abuja DC arc · Seismic: low",
    "Adamawa": "Basin: Chad / Benue influence · Rank: lignite–sub-bituminous · Depth est.: 150–600 m · Seismic: low",
    "Anambra": "Basin: Anambra · Rank: sub-bituminous · Depth est.: 60–300 m · Permeability: moderate · Seismic: low",
    "Delta": "Basin: Niger Delta margin · Rank: sub-bituminous · Depth est.: 200–800 m · Overpressure risk: moderate",
    "Plateau": "Basin: Jos–Bauchi fringe · Rank: sub-bituminous · Depth est.: 100–400 m · Igneous intrusions: localized",
    "Gombe": "Basin: Benue Trough · Rank: sub-bituminous · Depth est.: 180–500 m · Seismic: low",
    "Ondo": "Basin: Dahomey / SW margin · Rank: sub-bituminous · Depth est.: 150–550 m · Coastal logistics: high",
    "Abia": "Basin: Imo / Anambra fringe · Rank: sub-bituminous · Depth est.: 80–280 m · Industrial density: high",
    "Bauchi / Edo": "Bauchi: Benue Trough NE — depth 200–550 m, rank sub-bituminous. Edo: Benin flank — depth 150–450 m, high-value feedstock signature. Joint: D3 cross-corridor.",
}

if "leak_t0" not in st.session_state:
    st.session_state.leak_t0 = time.time()
if "power_highlight" not in st.session_state:
    st.session_state.power_highlight = False
if "selected_state" not in st.session_state:
    st.session_state.selected_state = None


def _fragment_supported() -> bool:
    return hasattr(st, "fragment")


st.set_page_config(
    page_title="NRRFC Vanguard — Node 8855",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    f"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap" rel="stylesheet">
<style>
  @keyframes vg-blueprint-drift {{
    0% {{ transform: translate(0, 0); }}
    100% {{ transform: translate(-80px, 40px); }}
  }}
  @keyframes vg-particles {{
    0% {{ background-position: 0 0, 40px 60px; }}
    100% {{ background-position: 200px 100px, 240px 160px; }}
  }}
  @keyframes vg-shimmer {{
    0% {{ background-position: -150% 0; }}
    100% {{ background-position: 150% 0; }}
  }}
  @keyframes vg-prism-spin {{
    from {{ transform: translate(-50%, -50%) rotate(0deg); }}
    to {{ transform: translate(-50%, -50%) rotate(360deg); }}
  }}
  @keyframes vg-orbit {{
    from {{ transform: rotate(0deg); }}
    to {{ transform: rotate(360deg); }}
  }}
  /* Flowing particle / blueprint stream (no yellow — Radiant Gold #FFD700 only) */
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
    opacity: 0.35;
    background-image:
      repeating-linear-gradient(0deg, transparent, transparent 47px, rgba(255,215,0,0.06) 48px),
      repeating-linear-gradient(90deg, transparent, transparent 47px, rgba(255,215,0,0.05) 48px),
      radial-gradient(1px 1px at 20% 30%, rgba(255,215,0,0.25), transparent 1px),
      radial-gradient(1px 1px at 80% 70%, rgba(255,215,0,0.2), transparent 1px);
    background-size: 100% 100%, 100% 100%, 200px 200px, 180px 180px;
    animation: vg-particles 28s linear infinite, vg-blueprint-drift 45s linear infinite;
  }}
  /* Central vector prism (geometric overlay) */
  .vg-prism-vector {{
    position: fixed;
    left: 50%;
    top: 42%;
    width: min(72vw, 520px);
    height: min(72vw, 520px);
    z-index: 1;
    pointer-events: none;
    transform: translate(-50%, -50%);
    opacity: 0.14;
    background:
      conic-gradient(from 45deg at 50% 50%,
        rgba(255,215,0,0.22) 0deg,
        transparent 60deg,
        rgba(255,215,0,0.12) 120deg,
        transparent 180deg,
        rgba(255,215,0,0.18) 240deg,
        transparent 300deg,
        rgba(255,215,0,0.15) 360deg);
    clip-path: polygon(50% 0%, 100% 38%, 82% 100%, 18% 100%, 0% 38%);
    animation: vg-prism-spin 50s linear infinite;
    filter: drop-shadow(0 0 8px rgba(255,215,0,0.25));
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
    padding: 0.4rem 0.55rem !important;
    max-width: 100% !important;
    overflow: hidden !important;
    background: linear-gradient(
      to right,
      rgba(0, 31, 63, 0.94) 0%,
      rgba(0, 26, 51, 0.9) 5%,
      rgba(255, 215, 0, 0.1) 30%,
      rgba(224, 224, 224, 0.06) 42%,
      rgba(0, 26, 51, 0.9) 65%,
      rgba(0, 31, 63, 0.96) 100%
    ) !important;
    background-size: 1000px 100%;
    animation: vg-shimmer 18s linear infinite;
    border-radius: 10px;
    box-shadow: 0 0 14px rgba(255, 215, 0, 0.2), inset 0 0 18px rgba(255, 255, 255, 0.03);
  }}
  /* S24 Ultra landscape: zoom lock — fit console without scroll */
  @media (max-height: 520px) {{
    [data-testid="stMain"] .block-container {{
      zoom: 0.88;
    }}
  }}
  @media (max-height: 430px) {{
    [data-testid="stMain"] .block-container {{
      zoom: 0.78;
    }}
  }}
  .stApp, .stApp * {{
    font-family: 'Goldman', system-ui, sans-serif !important;
  }}
  .vg-header-primary {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-weight: 700;
    font-size: clamp(0.75rem, 2vw, 1.05rem);
    color: {GOLD};
    text-align: center;
    margin: 0 0 0.25rem 0;
    line-height: 1.2;
  }}
  .vg-header-secondary {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-weight: 400;
    font-size: clamp(0.65rem, 1.65vw, 0.88rem);
    color: {GOLD};
    text-align: center;
    margin: 0 0 0.2rem 0;
  }}
  .vg-gateway {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-weight: 700;
    font-size: clamp(0.64rem, 1.55vw, 0.82rem);
    color: {GOLD};
    text-align: center;
    margin: 0.15rem 0;
  }}
  .vg-command {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-size: clamp(0.6rem, 1.45vw, 0.76rem);
    color: {TEXT_SLATE};
    text-align: center;
    margin: 0.1rem 0 0.35rem 0;
  }}
  .vg-dash-title {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-weight: 700;
    font-size: clamp(0.68rem, 1.75vw, 0.9rem);
    color: {TEXT_SLATE};
    text-align: center;
    margin: 0.3rem 0 0.45rem 0;
    border-bottom: 1px solid rgba(255,215,0,0.28);
    padding-bottom: 0.35rem;
  }}
  [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    color: {GOLD} !important;
  }}
  .vg-section-label {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-weight: 700;
    color: {GOLD};
    font-size: clamp(0.65rem, 1.5vw, 0.8rem);
    margin: 0.35rem 0 0.25rem 0;
    letter-spacing: 0.06em;
  }}
  .vg-body {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    color: {TEXT_SLATE};
    font-size: clamp(0.58rem, 1.35vw, 0.72rem);
    line-height: 1.35;
  }}
  .vg-geo {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    color: {TEXT_SLATE};
    font-size: clamp(0.55rem, 1.25vw, 0.68rem);
    line-height: 1.4;
    border-left: 2px solid {GOLD};
    padding-left: 0.5rem;
    margin-top: 0.35rem;
  }}
  .vg-leak-wrap {{
    position: relative;
    min-height: 110px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0.2rem 0;
  }}
  .vg-falcon-orbit {{
    position: absolute;
    width: 100px;
    height: 100px;
    left: 50%;
    top: 50%;
    margin-left: -50px;
    margin-top: -50px;
    animation: vg-orbit 26s linear infinite;
    pointer-events: none;
  }}
  .vg-falcon-orbit svg {{
    position: absolute;
    left: 50%;
    top: 0;
    width: 26px;
    height: 20px;
    margin-left: -13px;
    filter: drop-shadow(0 0 5px rgba(255,215,0,0.75));
  }}
  .vg-leak-core {{
    position: relative;
    z-index: 2;
    text-align: center;
    padding: 0.35rem 0.45rem;
    background: rgba(0, 31, 63, 0.82);
    border-radius: 10px;
    border: 1px solid rgba(255,215,0,0.4);
  }}
  .vg-leak-label {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-size: clamp(0.58rem, 1.3vw, 0.7rem);
    color: {GOLD};
    font-weight: 700;
    margin-bottom: 0.15rem;
  }}
  .vg-leak-value {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-size: clamp(1.1rem, 3.2vw, 1.45rem);
    color: {GOLD};
    font-weight: 700;
  }}
  .vg-leak-ticker {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-size: clamp(0.5rem, 1.15vw, 0.62rem);
    color: {TEXT_SLATE};
    text-align: center;
    margin-top: 0.25rem;
  }}
  [data-testid="stMain"] .stButton > button {{
    font-family: 'Goldman', system-ui, sans-serif !important;
    background: rgba(0,40,80,0.9) !important;
    color: {TEXT_SLATE} !important;
    border: 1px solid rgba(255,215,0,0.45) !important;
    border-radius: 8px !important;
    min-height: 2rem;
  }}
  [data-testid="stMain"] .stButton > button:hover {{
    border-color: {GOLD} !important;
    color: {GOLD} !important;
  }}
  [data-testid="stSidebar"] {{
    background: rgba(0, 20, 45, 0.98) !important;
    border-right: 1px solid rgba(255,215,0,0.25) !important;
  }}
  [data-testid="stSidebar"] * {{
    font-family: 'Goldman', system-ui, sans-serif !important;
  }}
</style>
<div class="vg-prism-vector" aria-hidden="true"></div>
""",
    unsafe_allow_html=True,
)


def _current_leakage_b() -> float:
    elapsed = max(0.0, time.time() - float(st.session_state.leak_t0))
    steps = int(elapsed // LEAK_INTERVAL_SEC)
    return LEAKAGE_ANCHOR_B + steps * LEAK_TICK_B


def _falcon_svg() -> str:
    # Strict Radiant Gold #FFD700 — no legacy yellow hex
    return """<svg viewBox="0 0 32 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <path fill="#FFD700" stroke="#FFD700" stroke-width="0.45" opacity="0.85"
    d="M16 12 L8 14 L6 12 L8 10 L16 8 L24 10 L26 12 L24 14 Z"/>
  <path fill="#FFD700" opacity="0.95" d="M14 11 L4 8 L2 10 L6 12 Z"/>
  <path fill="#FFD700" opacity="0.95" d="M18 11 L28 8 L30 10 L26 12 Z"/>
  <path fill="#FFD700" opacity="0.75" d="M16 6 L18 4 L20 6 L18 8 Z"/>
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
<p class="vg-leak-ticker">INSTITUTIONAL URGENCY · 10s CADENCE · NODE 8855</p>
""",
        unsafe_allow_html=True,
    )


if _fragment_supported():

    @st.fragment(run_every=timedelta(seconds=LEAK_INTERVAL_SEC))
    def _leakage_fragment():
        _render_leakage_block()

else:

    def _leakage_fragment():
        _render_leakage_block()


# --- Sidebar: Strike Zone + geology (localized parameters) ---
with st.sidebar:
    st.markdown(f'<p class="vg-section-label">STRIKE ZONE PANEL</p>', unsafe_allow_html=True)
    if st.session_state.selected_state:
        sk = st.session_state.selected_state
        st.markdown(
            f'<div class="vg-body">{STATE_INTEL.get(sk, "")}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<p class="vg-section-label" style="margin-top:0.75rem;">GEOLOGICAL PARAMETERS</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<p class="vg-geo">{GEOLOGY.get(sk, "Parameters pending sovereign survey.")}</p>',
            unsafe_allow_html=True,
        )
        if st.button("Clear node selection", key="clear_sel"):
            st.session_state.selected_state = None
            st.rerun()
    else:
        st.markdown(
            '<p class="vg-body">Select a state node from the 12-cell grid to load localized geological parameters.</p>',
            unsafe_allow_html=True,
        )


# --- Main console ---
with st.container():
    # GCSLC Sovereign Header — forced visibility (Radiant Gold / Deepest Navy / Goldman non-serif)
    st.markdown(
        f"""
    <h1 style="
        text-align: center;
        color: #FFD700;
        font-family: 'Goldman', sans-serif;
        font-weight: 700;
        font-size: clamp(0.65rem, 1.85vw, 1rem);
        line-height: 1.35;
        letter-spacing: 0.02em;
        background-color: #001A33;
        padding: 10px 12px;
        margin: 0 0 0.5rem 0;
        border: 2px solid #FFD700;
        border-radius: 10px;
        position: relative;
        z-index: 9999;
    ">{MASTER_BRAND.upper()}</h1>
""",
        unsafe_allow_html=True,
    )
    st.markdown(f'<p class="vg-header-secondary">{ENTITY_LINE}</p>', unsafe_allow_html=True)
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
        st.markdown('<p class="vg-section-label">NRRFC ENGINE — 12 NODES</p>', unsafe_allow_html=True)
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
                f'<p class="vg-body" style="color:{GOLD};font-weight:700;border:2px solid {GOLD};border-radius:8px;padding:0.3rem;">ACTION ALERT: 1,199 MW Power potential for AI Data Centers</p>',
                unsafe_allow_html=True,
            )
        # 12 cells: 4 × 3 (stable widget keys — no slashes in key id)
        for r in range(3):
            row_keys = GRID_12_KEYS[r * 4 : (r + 1) * 4]
            cols = st.columns(4)
            for c in range(4):
                key = row_keys[c]
                with cols[c]:
                    if st.button(key, key=f"node_r{r}_c{c}", use_container_width=True):
                        st.session_state.selected_state = key

with st.container():
    st.markdown("---")
    st.caption("NRRFC Vanguard · Node 8855 · GCSLC LTD/GTE")
