"""
National Wealth Cloud for Nigeria: Coal & Diamond (NWC/C&D)
Sovereign Gateway — 8R Stealth Paradigm | Galadiman Ruwa Center For Strategic Leadership and Communication LTD/GTE — GCSLC
Launch-ready: width="stretch" (2026 standard); no use_container_width.
PRESIDENTIAL_STRIKE_V1_RESTORE: Institutional Core, C&D Grid, 8R Engine, Tactical Audio-Visual Sync.
"""
import base64
import os
import warnings
from collections import defaultdict
import streamlit as st
import streamlit.components.v1 as components

warnings.filterwarnings("ignore", category=DeprecationWarning, module="streamlit")
warnings.filterwarnings("ignore", message=".*use_container_width.*")
import pydeck as pdk
import pandas as pd

from d8_logic import (
    WEALTH_RETENTION_LOCK,
    STRATEGIC_FOUNDATION,
    apply_talon_lock,
    apply_95_5_talon_lock,
    TALON_LOCK_NATIONAL_PCT,
    TALON_LOCK_GLOBAL_POOL_PCT,
    D3_WEALTH_MULTIPLIER,
    D3_GERMANIUM_USD_PER_KG,
    D3_AMMONIA_USD_PER_MT,
    D3_SILICON_MONTHLY_YIELD_M,
    D3_COAL_SYNGAS_MONTHLY_REVENUE_M,
)
from mineral_sovereignty import (
    get_nodes,
    retained_yield,
    global_market_impact_index,
    get_diamond_reserves,
)
from spc_generator import generate_spc_image
from handshake import run_diagnostic_pulse, play_talon_lock_confirmed, play_eagle_cry, get_swat_beep_path, STATES
from nwc_geopolitical import STATE_REGION, STATE_LGA_COUNT, get_lgas

FULL_NAME = "Galadiman Ruwa Center For Strategic Leadership and Communication LTD/GTE"
BRAND = "GCSLC"
SEAL_PATH = os.path.join(os.path.dirname(__file__), "assets", "gcslc_seal.png")
DETERMINANTS = ["Refine", "Reset", "Research", "Restructure", "Resuscitate", "Revitalize", "Re-engineer", "Retain"]
NWC_HEADER = "National Wealth Cloud for Nigeria: Coal & Diamond (NWC/C&D)"
NWC_SUBTITLE = "Cloud-Level Pragmatic Reality — Powered by GCSLC Sovereign Gateway"
VALUATION_ANCHOR_B = 170.85  # Central empirical metric — 95/5 Talon Lock flare

# Sovereign Retention Protocol (D8 Logic) — 95% National Equity (Talon Lock)
SOVEREIGN_RETENTION_PROTOCOL = f"""
**The Sovereign Retention Protocol (D8 Logic)**  
This partnership is governed by a **fixed {int(WEALTH_RETENTION_LOCK * 100)}% Value Anchor** (Talon Lock). By deploying the 8R Stealth Paradigm, GCSLC mandates that **{int(WEALTH_RETENTION_LOCK * 100)}% of all economic velocity and intellectual derivative value** remains proprietary to the Sovereign Node. This foundation is engineered at **1m × 1m Steel** structural depth, ensuring that global expansion (Alphabet/Apple) serves to **strengthen the national core** rather than deplete it.
"""

# D7: set_page_config must be the very first Streamlit command (no st.* before this)
st.set_page_config(
    page_title="NWC/C&D — GCSLC Sovereign Gateway",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Session state init (after set_page_config)
if "strike" not in st.session_state:
    st.session_state.strike = False
if "strike_manifested" not in st.session_state:
    st.session_state.strike_manifested = False
if "certificate_shown" not in st.session_state:
    st.session_state.certificate_shown = False
if "handshake_done" not in st.session_state:
    st.session_state.handshake_done = False
if "state_nodes" not in st.session_state:
    st.session_state.state_nodes = []
if "selected_state" not in st.session_state:
    st.session_state.selected_state = None
if "nwc_authenticated" not in st.session_state:
    st.session_state.nwc_authenticated = False

# NWC/C&D diagnostic pulse once at startup: initialize 37 nodes, then run pulse
if not st.session_state.handshake_done:
    st.session_state.state_nodes = list(STATES)
    run_diagnostic_pulse()
    st.session_state.handshake_done = True

# NWC/C&D Sovereign Aesthetic — Navy Blue (#002147) & Metallic Gold (#D4AF37) | GCSLC Sovereign Diagnostic
st.markdown("""
<style>
/* Viewport: GCSLC Sovereign Diagnostic | 8R Scientific Analysis */
.stApp { background-color: #002147 !important; min-height: 100vh; }
[data-testid="stAppViewContainer"] { background-color: #002147 !important; }
.main .block-container { background-color: #002147 !important; max-width: 100%; padding: 1rem 2rem; }
h1, h2, h3, p, span, label, .stMarkdown { color: #D4AF37 !important; }
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] { color: #D4AF37 !important; }
section[data-testid="stSidebar"] { background-color: #002147 !important; border-right: 2px solid #D4AF37; }
/* Clickable state node buttons + 774 LGA grid consistency */
.nwc-state-btn { background: linear-gradient(135deg, #002147, #003366); border: 1px solid #D4AF37; color: #D4AF37; border-radius: 6px; padding: 0.35rem 0.6rem; margin: 0.2rem; font-size: 0.85rem; }
.nwc-state-btn:hover { background: rgba(212,175,55,0.2); }
.glossary-term { font-weight: 700; color: #E8C547; }
.glossary-def { color: #D4AF37; font-size: 0.9rem; margin-bottom: 0.75rem; }
/* 774 LGA grid: Navy Blue & Metallic Gold theme */
.nwc-lga-grid, .nwc-lga-grid .stMarkdown, .nwc-lga-grid ul { background-color: #002147 !important; color: #D4AF37 !important; }
.nwc-lga-grid [data-testid="stExpander"] { background: rgba(0,33,71,0.98); border: 1px solid #D4AF37; border-radius: 6px; }
.nwc-lga-grid [data-testid="stExpander"] summary { color: #D4AF37 !important; }
.nwc-lga-grid [data-testid="stExpander"] li { color: #E8C547; }
/* 95/5 Talon Lock data flare on node click */
.talon-lock-flare {
    background: linear-gradient(135deg, rgba(212,175,55,0.25), rgba(0,33,71,0.9));
    border: 2px solid #D4AF37;
    border-radius: 8px;
    padding: 0.6rem 1rem;
    margin-bottom: 0.75rem;
    text-align: center;
    font-weight: 700;
}
.talon-lock-flare .flare-label { color: #E8C547; margin-right: 0.5rem; }
.talon-lock-flare .flare-value { color: #FFE55C; font-size: 1.1rem; }
/* 8R Stealth Engine — D1–D8 golden Breathing animation */
@keyframes d8-breathing {
    0%, 100% { box-shadow: 0 0 12px rgba(212,175,55,0.4); opacity: 0.9; transform: scale(1); }
    50% { box-shadow: 0 0 24px rgba(232,197,71,0.8); opacity: 1; transform: scale(1.02); }
}
.d8-widgets-grid { display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 0.75rem 0; }
.d8-widget-breathing {
    background: linear-gradient(135deg, rgba(0,33,71,0.95), rgba(0,51,102,0.9));
    border: 1px solid #D4AF37;
    border-radius: 8px;
    padding: 0.5rem 0.75rem;
    color: #D4AF37;
    font-weight: 700;
    font-size: 0.9rem;
    animation: d8-breathing 2.5s ease-in-out infinite;
}
.central-valuation { text-align: center; color: #E8C547 !important; margin-bottom: 0.5rem; }
</style>
""", unsafe_allow_html=True)
# Keyframes and .brand-8r kept in background (no leak)
st.markdown("""
<style>
/* Title shimmer: linear-gradient animation — 8R Center primary authority */
.brand-8r {
    font-weight: 800 !important;
    font-size: 1.8rem !important;
    text-align: center;
    background: linear-gradient(90deg, #D4AF37, #FFE55C, #D4AF37, #E8C547, #D4AF37);
    background-size: 300% 100%;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
    animation: title-shimmer 4s linear infinite;
}

@keyframes title-shimmer {
    0% { background-position: 0% 50%; }
    100% { background-position: 300% 50%; }
}

/* D1: REFINE - Sovereign branding animation */
@keyframes gold-shimmer {
    0% { background-position: -200% center; }
    100% { background-position: 200% center; }
}
.gcslc-header {
    font-family: 'Inter', sans-serif;
    font-weight: 800;
    font-size: 2.2rem;
    text-align: center;
    background: linear-gradient(90deg, #D4AF37, #FFFFFF, #D4AF37, #E8C547, #D4AF37);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gold-shimmer 5s linear infinite;
    margin-bottom: 0px;
}
.proprietor-tag {
    font-family: 'serif';
    font-style: italic;
    text-align: center;
    color: #D4AF37;
    font-size: 1.1rem;
    letter-spacing: 2px;
    margin-top: -10px;
}
/* Master Header (Metallic Gold) — PRESIDENTIAL_STRIKE_V1_RESTORE */
.nwc-master-header {
    font-family: 'Inter', sans-serif;
    font-weight: 800;
    font-size: 2rem;
    text-align: center;
    background: linear-gradient(90deg, #D4AF37, #FFE55C, #D4AF37, #E8C547, #D4AF37);
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
    animation: gold-shimmer 5s linear infinite;
    margin-bottom: 0.25rem;
}
.nwc-authority {
    text-align: center;
    color: #D4AF37;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 1px;
}
.nwc-subheader {
    font-family: 'serif';
    font-style: italic;
    text-align: center;
    color: #E8C547;
    font-size: 1.05rem;
    letter-spacing: 2px;
    margin-top: -4px;
    margin-bottom: 0.5rem;
}
/* Chairman signature — Bottom-right sticky bar with shimmer (Dr. Jaafaru Sa'ad) */
.chairman-signature-shimmer {
    background: linear-gradient(90deg, #D4AF37, #FFE55C, #E8C547, #D4AF37);
    background-size: 200% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent !important;
    animation: gold-shimmer 4s linear infinite;
}
.chairman-sticky-bar {
    position: fixed;
    bottom: 0;
    right: 0;
    z-index: 999;
    background: linear-gradient(90deg, rgba(0,33,71,0.97), rgba(0,33,71,0.98));
    border-top: 2px solid rgba(212,175,55,0.5);
    border-left: 2px solid rgba(212,175,55,0.5);
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
    font-weight: 700;
    border-radius: 8px 0 0 0;
    pointer-events: none;
}
.universal-message {
    background: rgba(212, 175, 55, 0.1);
    border-left: 5px solid #D4AF37;
    padding: 20px;
    border-radius: 10px;
    color: #E0E0E0;
    font-style: italic;
    text-align: center;
    margin: 20px 0;
}

/* GCSLC Gold Seal: linear-gradient shimmer (gradient ring + gold glow) */
[data-testid="stLogo"] {
    position: relative;
    border-radius: 50%;
    padding: 3px;
    background: linear-gradient(135deg, #D4AF37, #FFE55C, #E8C547, #D4AF37);
    background-size: 300% 300%;
    animation: seal-gradient-shimmer 3s linear infinite, seal-glow 2.5s ease-in-out infinite;
}
[data-testid="stLogo"] img {
    animation: seal-rotate 60s linear infinite, seal-pulse 2.5s ease-in-out infinite;
    transform-origin: center center;
    border-radius: 50%;
    display: block;
    background: #002147;
}

@keyframes seal-gradient-shimmer {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes seal-glow {
    0%, 100% { box-shadow: 0 0 12px rgba(212,175,55,0.5); }
    50% { box-shadow: 0 0 20px rgba(232,197,71,0.8); }
}

@keyframes seal-rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

@keyframes seal-pulse {
    0%, 100% { opacity: 0.85; }
    50% { opacity: 1; }
}

.spc-cert { border: 3px solid #D4AF37; border-radius: 12px; padding: 2rem; margin: 1.5rem 0; background: rgba(0,33,71,0.95); color: #D4AF37; position: relative; }
.spc-cert .seal-wrap { text-align: center; margin: 1rem 0; }
.spc-cert .cascade-map { margin: 1rem 0; line-height: 1.8; }
.spc-cert .talon-metric { font-size: 1.4rem; font-weight: 700; color: #E8C547; margin: 1rem 0; }
.spc-cert .footer-cert { margin-top: 1.5rem; font-size: 0.85rem; opacity: 0.95; }
.spc-watermark { position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%) rotate(-25deg); font-size: 0.9rem; opacity: 0.12; color: #D4AF37; white-space: nowrap; pointer-events: none; }
</style>
""", unsafe_allow_html=True)

# Global Branding: NWC/C&D header + seal
if os.path.isfile(SEAL_PATH):
    st.logo(SEAL_PATH)

# Top bar: Authority only (Chairman signature moved to bottom-right sticky bar)
st.markdown(
    '<div style="position: sticky; top: 0; z-index: 100; background: linear-gradient(180deg, #002147 0%, rgba(0,33,71,0.98) 100%); padding-bottom: 10px; margin-bottom: 8px; border-bottom: 1px solid rgba(212,175,55,0.25);">'
    '<p style="text-align: center; font-weight: 800; color: #D4AF37; font-size: 0.95rem; margin: 0;">Galadiman Ruwa Center (GCSLC) LTD/GTE</p>'
    '</div>',
    unsafe_allow_html=True,
)

# Master Header (Metallic Gold): National Wealth Cloud for Nigeria: Coal & Diamond (NWC/C&D)
st.markdown("""
<div class="nwc-master-header">
    National Wealth Cloud for Nigeria: Coal & Diamond (NWC/C&D)
</div>
<div class="nwc-authority">
    Authority: Galadiman Ruwa Center (GCSLC) LTD/GTE
</div>
<div class="nwc-subheader">
    Proprietors of 8R Stealth Paradigm Convergence
</div>

<div class="universal-message">
    "The 8R Determinants are universal. Whether applied to national assets or personal growth, 
    they provide the scientific blueprint to Refine, Reset, and Revitalize every facet of human endeavor. 
    Applying 8R to everything we do is the key to scientifically improving our lives."
</div>
""", unsafe_allow_html=True)

# ——— 37-Node Geopolitical Grid (36 States + FCT) ———
st.write("### 🗺️ Command & Control (C&D) Grid — 37-Node Geopolitical Grid")
st.caption("Click a state to trigger 95/5 Talon Lock data flare and drill down into Local Government Areas (774 LGA nodes).")

# Group states by region for display
region_to_states = defaultdict(list)
for state in STATES:
    region = STATE_REGION.get(state, "Other")
    region_to_states[region].append(state)

# Region order matching user spec
REGION_ORDER = [
    "North West", "North East", "North Central",
    "South South", "South East", "South West", "FCT",
]
for region in REGION_ORDER:
    states_in_region = region_to_states.get(region, [])
    if not states_in_region:
        continue
    with st.expander(f"**{region}** ({sum(STATE_LGA_COUNT.get(s, 0) for s in states_in_region)} LGAs)", expanded=(region == "North West")):
        cols = st.columns(min(len(states_in_region), 4))
        for idx, state in enumerate(states_in_region):
            col = cols[idx % len(cols)]
            with col:
                if st.button(f"📍 {state} ({STATE_LGA_COUNT.get(state, 0)} LGAs)", key=f"node_{state}"):
                    st.session_state.selected_state = state
                    st.rerun()

# Drill-down: selected state LGAs + 95/5 Talon Lock data flare (9.6x | $170.85B)
if st.session_state.selected_state:
    state = st.session_state.selected_state
    region = STATE_REGION.get(state, "")
    lgas = get_lgas(state)
    # 95/5 Talon Lock data flare on node click (per directive)
    st.markdown(
        f'<div class="talon-lock-flare">'
        f'<span class="flare-label">95/5 Talon Lock</span> '
        f'<span class="flare-value">9.6× Wealth Multiplier | ${VALUATION_ANCHOR_B:.2f}B Valuation Anchor.</span>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.write(f"#### 📌 {state} — {region}")
    st.caption(f"{len(lgas)} Local Government Areas (LGA Micro-Veracity active)")
    # 774 LGA grid: Navy Blue & Metallic Gold themed list (no overload)
    lga_items = "".join(f"<li>{lga}</li>" for lga in lgas)
    st.markdown(f'<div class="nwc-lga-grid"><ul style="color: #D4AF37; background: transparent;">{lga_items}</ul></div>', unsafe_allow_html=True)
    if st.button("Clear selection", key="clear_state"):
        st.session_state.selected_state = None
        st.rerun()

st.markdown("---")

# ——— D3 Scientific Profit Centers (9.6x wealth multiplier) ———
st.write("### ⚡ D3 Scientific Profit Centers")
st.caption("Per MT coal/diamond throughput: **9.6×** wealth multiplier. Unit-price derivatives below.")
d3_col1, d3_col2 = st.columns(2)
with d3_col1:
    st.metric("Wealth Multiplier (per MT throughput)", f"{D3_WEALTH_MULTIPLIER}×")
    st.metric("Germanium (AI Chip Grade)", f"${D3_GERMANIUM_USD_PER_KG:,.0f}/kg")
    st.metric("Ammonia (Fertilizer Grade)", f"${D3_AMMONIA_USD_PER_MT:,.0f}/MT")
with d3_col2:
    st.metric("Silicon (Semiconductor Grade) — Monthly Yield", f"${D3_SILICON_MONTHLY_YIELD_M}M")
    st.metric("Coal Syngas (Sovereign Feedstock) — Monthly Revenue", f"${D3_COAL_SYNGAS_MONTHLY_REVENUE_M}M")
st.caption("**Diamond (Industrial Tech Grade):** Heat Sinks & Precision Abrasives — sovereign value chain.")

st.markdown("---")

# ——— 95/5 Talon Lock Algorithm ———
st.write("### 🔒 Sovereign Retention — 95/5 Talon Lock")
national_pct = int(TALON_LOCK_NATIONAL_PCT * 100)
global_pct = int(TALON_LOCK_GLOBAL_POOL_PCT * 100)
st.markdown(f"**{national_pct}% National Equity** (locked) | **{global_pct}% Global Adoption Pool** (Wall Street / Silicon Valley partners)")
example_rev = 100.0  # $100M derivative revenue example
nat, gl = apply_95_5_talon_lock(example_rev)
st.metric("Example: $100M derivative revenue", f"National: **${nat:.0f}M** · Global Pool: **${gl:.0f}M**")

st.markdown("---")

# 8R Stealth Engine — D1–D8 Determinant Widgets (golden Breathing animation)
st.write("### 8R Stealth Engine — Determinant Widgets (D1–D8)")
# Central valuation linked to apply_95_5_talon_lock from d8_logic
_central_rev = VALUATION_ANCHOR_B * 1e9 / 1e6  # $170.85B as equivalent revenue scale for split
_nat_anchor, _gl_pool = apply_95_5_talon_lock(_central_rev)
st.markdown(
    f'<p class="central-valuation">Central Valuation (D8 Talon Lock): <strong>${VALUATION_ANCHOR_B:.2f}B</strong> '
    f'→ National: <strong>${_nat_anchor:,.0f}M</strong> · Global Pool: <strong>${_gl_pool:,.0f}M</strong></p>',
    unsafe_allow_html=True,
)
st.caption("apply_95_5_talon_lock from d8_logic.py linked to central valuation.")
# D1–D8 with golden Breathing animation (CSS class .d8-widget-breathing)
d8_html = "".join(
    f'<div class="d8-widget-breathing">D{i}: {det}</div>' for i, det in enumerate(DETERMINANTS, 1)
)
st.markdown(f'<div class="d8-widgets-grid">{d8_html}</div>', unsafe_allow_html=True)

# Sovereign Retention Protocol (D8 Logic) — 95% National Equity (Talon Lock)
with st.expander("🔒 Sovereign Retention Protocol (D8 Logic)", expanded=True):
    st.markdown(SOVEREIGN_RETENTION_PROTOCOL)
    st.metric(label="Value Anchor (D8 Talon Lock)", value=f"{int(WEALTH_RETENTION_LOCK * 100)}%")
    st.caption(f"Structural foundation: {STRATEGIC_FOUNDATION} — national core preserved under global expansion.")
    # Example: apply_talon_lock
    example_value = 4.2  # e.g. $4.2B
    retained = apply_talon_lock(example_value)
    st.caption(f"*Example:* `apply_talon_lock({example_value})` → **{retained:.2f}** retained by Sovereign Node.")

# Interactive NRRFC Dashboard – Mineral Density & Defense Toggle
st.write("### 🛡️ NRRFC – Mineral Density & Defense Dashboard")
toggle_minerals = st.checkbox("Activate Mineral Density & Defense Toggle", value=False)
if toggle_minerals:
    st.caption("NGECC – Sovereign Minerals: Coal (Energy), Diamonds (Value), Uranium (Strategic Depth) under 95% Talon Lock.")

    # Unified Carbon Gateway — Diamond-Coal Bridge (anchor: Line 117)
    st.write("#### NRRFC Fusion Strike: Unified Carbon Gateway")
    st.caption("Diamond-Coal Bridge: NW/NE Diamond Nodes integrated with Coal (Energy) under D3 Research.")

    # New layer: NW/NE Diamond Nodes (Diamond-Coal Bridge)
    st.write("**Diamond-Coal Bridge — NW/NE Diamond Nodes Layer**")
    diamond_reserves = get_diamond_reserves()
    nw_ne_nodes = [n for n in diamond_reserves if n.get("region") in ("North East", "North West")]
    if nw_ne_nodes:
        bridge_df = pd.DataFrame(nw_ne_nodes)[["state", "region", "proven_reserve_probability", "retained_value_usd"]].copy()
        bridge_df = bridge_df.rename(columns={"state": "State", "region": "Region", "proven_reserve_probability": "Proven Reserve Probability"})
        bridge_df["95% Retained Sovereign Value"] = bridge_df["retained_value_usd"].apply(lambda v: f"${v:,.0f}")
        st.dataframe(bridge_df[["State", "Region", "Proven Reserve Probability", "95% Retained Sovereign Value"]], width="stretch")
    else:
        st.caption("No NW/NE diamond nodes in current dataset.")

    # 95% Metric: monthly revenue (verified North West Hydrothermal Discovery default)
    GROSS_MONTHLY_REVENUE_M = 415  # $415M default — verified North West Hydrothermal Discovery
    monthly_gross_usd = GROSS_MONTHLY_REVENUE_M * 1_000_000
    monthly_retained = apply_talon_lock(monthly_gross_usd)  # 95% Talon Lock
    retained_display_m = int(monthly_retained / 100_000) / 10
    c1, c2 = st.columns(2)
    with c1:
        st.metric(label="Monthly Revenue (Gross)", value=f"${GROSS_MONTHLY_REVENUE_M}M")
    with c2:
        st.metric(label="Monthly Revenue (95% Retained — Talon Lock)", value=f"${retained_display_m:.1f}M")

    nodes = get_nodes() or []  # D7: ensure list, never None
    rows = []
    for node in nodes:
        r = retained_yield(node)
        idx = global_market_impact_index(node)
        rows.append(
            {
                "Node": node.name,
                "Region": node.region,
                "Type": node.mineral_type,
                "D-Index": node.d_index,
                "Base Yield": node.base_yield,
                "Retained Yield (95%)": round(r, 2),
                "Global Impact Index": round(idx, 2),
            }
        )
    st.dataframe(rows, width="stretch")

    # D3: Mineral Research Node – State-by-state table (Proven Reserve Probability | 95% Retained Sovereign Value)
    st.write("#### D3: Mineral Research Node — Sovereign Mineral Fortress")
    st.caption("Nigeria is not just an oil nation: kimberlite pipe signatures (NE) and structural hydrothermal trends (NW) under 8R D3 Research.")
    diamond_data = get_diamond_reserves()
    if diamond_data:
        df = pd.DataFrame(diamond_data)
        table_df = df[["state", "proven_reserve_probability", "retained_value_usd"]].copy()
        table_df.rename(
            columns={
                "state": "State",
                "proven_reserve_probability": "Proven Reserve Probability",
                "retained_value_usd": "95% Retained Sovereign Value",
            },
            inplace=True,
        )
        table_df["95% Retained Sovereign Value"] = table_df["95% Retained Sovereign Value"].map(lambda v: f"${v:,.0f}")
        st.dataframe(table_df, width="stretch")

        # 3D NRRFC Heatmap — Sovereign Mineral Fortress (finalized pydeck at ~Line 158)
        st.write("#### 3D NRRFC Heatmap — Sovereign Mineral Fortress")
        st.caption("Proving Nigeria as a Sovereign Mineral Fortress: D3 Research nodes across North East (kimberlite) and North West (hydrothermal).")
        heat_df = df.copy()
        heat_df["elevation"] = (heat_df["retained_value_usd"] / 1_000_000_000).clip(lower=0.5)  # billions, min height for visibility
        heat_df["retained_display"] = heat_df["retained_value_usd"].apply(lambda x: f"${x:,.0f}")

        nrrfc_layer = pdk.Layer(
            "ColumnLayer",
            data=heat_df,
            get_position="[lon, lat]",
            get_elevation="elevation",
            elevation_scale=8,
            radius=45000,
            get_fill_color="[212, 175, 55, 180]",
            pickable=True,
            auto_highlight=True,
        )
        nrrfc_view = pdk.ViewState(
            longitude=8.5,
            latitude=9.5,
            zoom=5,
            pitch=50,
            bearing=0,
        )
        sovereign_fortress_deck = pdk.Deck(
            layers=[nrrfc_layer],
            initial_view_state=nrrfc_view,
            map_style="mapbox://styles/mapbox/dark-v10",
            tooltip={"text": "State: {state}\nProven Reserve Probability: {proven_reserve_probability}\n95% Retained Sovereign Value: {retained_display}"},
        )
        st.pydeck_chart(sovereign_fortress_deck)

# Tactical Experience: Login (Password GCSLC2026) → Eagle cry; SWAT soundscape
with st.sidebar:
    st.header("🔐 NWC/C&D Access")
    if not st.session_state.nwc_authenticated:
        _pw = st.text_input("Password", type="password", key="nwc_pw", placeholder="Enter directive password")
        if st.button("Login", key="nwc_login") and _pw == "GCSLC2026":
            st.session_state.nwc_authenticated = True
            play_eagle_cry()  # Majestic Eagle/Falcon cry on login
            st.rerun()
        st.caption("Password: GCSLC2026 — Triggers Majestic Eagle/Falcon cry on success.")
    else:
        st.success("Authenticated — Eagle cry triggered.")
        swat_path = get_swat_beep_path()
        if swat_path:
            try:
                with open(swat_path, "rb") as f:
                    wav_b64 = base64.b64encode(f.read()).decode("utf-8")
                # Loop SWAT-style HUD two-beep WAV (injected HTML5 audio)
                components.html(
                    f'<audio id="swat-hud-loop" loop autoplay><source src="data:audio/wav;base64,{wav_b64}" type="audio/wav"></audio>',
                    height=0,
                )
            except Exception:
                try:
                    with open(swat_path, "rb") as _f:
                        st.audio(_f.read(), format="audio/wav")
                except Exception:
                    pass
        st.caption("Soundscape: SWAT-style HUD two-beep (swat_hud_beep.wav) looping when asset present.")
    st.markdown("---")
    st.header("📖 Sovereign Tactical Glossary")
    with st.expander("NWC/C&D", expanded=True):
        st.markdown(
            "**National Wealth Cloud for Nigeria: Coal & Diamond** — "
            "The unassailable master framework for sovereign mineral and energy value chains; "
            "37-Node Geopolitical Grid (36 States + FCT) with LGA-level drill-down."
        )
    with st.expander("SSMV"):
        st.markdown(
            "**Sovereign Strategic Mineral Value** — "
            "The proprietary valuation of coal, diamond, and derivative streams (Germanium, Ammonia, Silicon, Syngas) "
            "under the 9.6× D3 multiplier and Talon Lock."
        )
    with st.expander("95/5 Talon Lock"):
        st.markdown(
            "**Sovereign Retention Algorithm** — "
            "95% of all derivative revenue locked as **National Equity**; "
            "5% **Global Adoption Pool** for Wall Street / Silicon Valley partners."
        )
    with st.expander("8R Stealth Paradigm (D1–D8)"):
        for i, det in enumerate(DETERMINANTS, 1):
            st.caption(f"**D{i}:** {det}")
    st.markdown("---")
    st.header("Strategic Strike Input")
    friction_target = st.text_input("Enter Friction Target:", "National Asset", key="gcslc_friction_key")
    if st.button("EXECUTE 8R STRIKE", key="gcslc_strike_button"):
        st.session_state.strike = True
        st.session_state.strike_manifested = False
        st.session_state.certificate_shown = False
        st.rerun()

# After strike: show 100% manifested state, then certificate button
if st.session_state.strike:
    # Simulate 100% manifestation (immediate in this build; could add 0.4s cascade here)
    st.session_state.strike_manifested = True
    st.success(f"**8R Strike 100% manifested** — Friction Target: **{friction_target}**")
    st.metric(label="Strike Status", value="MANIFESTED")

    # Certificate Trigger: button only after strike 100% manifested
    if st.session_state.strike_manifested and not st.session_state.certificate_shown:
        if st.button("GENERATE SOVEREIGN PROOF CERTIFICATE", type="primary", key="spc_gen_btn"):
            st.session_state.certificate_shown = True
            play_talon_lock_confirmed()  # Submarine chime when 95% Talon Lock confirmed
            st.rerun()

    # Visual Proof: Sovereign Proof Certificate
    if st.session_state.certificate_shown:
        st.write("---")
        st.write("### 📜 Sovereign Proof Certificate (SPC)")

        # GCSLC Gold Seal — visual proof at top of certificate
        if os.path.isfile(SEAL_PATH):
            st.image(SEAL_PATH, caption="GCSLC Gold Seal", width=120)
        else:
            st.markdown(
                '<div style="width: 120px; height: 120px; margin: 0 auto 1rem; border: 3px solid #D4AF37; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; color: #D4AF37;">GCSLC<br/>SEAL</div>',
                unsafe_allow_html=True,
            )

        cert_html = """
        <div class="spc-cert">
        <div class="spc-watermark">Proprietary Nodal Logic — Galadiman Ruwa Center — Protected Asset</div>
        <p style="text-align: center; font-weight: 700; font-size: 1.2rem;">SOVEREIGN PROOF CERTIFICATE</p>
        <p style="text-align: center;">Galadiman Ruwa Center For Strategic Leadership and Communication LTD/GTE — GCSLC</p>
        <p class="cascade-map"><strong>D1–D8 Cascade (Hierarchical Map):</strong><br/>
        D1 Refine → D2 Reset → D3 Research → D4 Restructure → D5 Resuscitate → D6 Revitalize → D7 Re-engineer → D8 Retain
        </p>
        <p class="talon-metric">🔒 95% Legacy Retention / Talon Lock — Primary Security Metric for this Strike</p>
        <p class="footer-cert" style="font-size: 0.8rem; margin-top: 0.75rem;">Governed by the <strong>Sovereign Retention Protocol (D8 Logic)</strong>: 95% Value Anchor (Talon Lock); 1m × 1m structural depth; economic velocity and intellectual derivative value retained by the Sovereign Node.</p>
        <p class="footer-cert">This Certificate validates the Scientific Universality of the 8R Stealth Paradigm across Human, Economic, and AI Systems.</p>
        <p class="footer-cert" style="margin-top: 0.5rem; font-size: 0.75rem; opacity: 0.85;">Strategic DNA v4.0 - Proprietary Nodal Logic of GCSLC. Unauthorized Replication Subject to Sovereign Re-engineering.</p>
        </div>
        """
        st.markdown(cert_html, unsafe_allow_html=True)

# Footer (always)
st.markdown("---")
st.caption(f"Strategic Infrastructure Manifested by: {FULL_NAME} - {BRAND}  |  © 2026  |  Proprietary Nodal Logic — Protected Asset")

# Chairman Signature: Bottom-right sticky bar with shimmer (Dr. Jaafaru Sa'ad — Chairman & Founder)
st.markdown(
    '<div class="chairman-sticky-bar chairman-signature-shimmer">Dr. Jaafaru Sa\'ad — Chairman & Founder</div>',
    unsafe_allow_html=True,
)
