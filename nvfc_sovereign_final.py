"""
NVFC Sovereign Final — Pure Streamlit engine (D7).
High-fidelity Nigeria map aligned with Node 8090 (app.html falcon convergence).
Run: streamlit run nvfc_sovereign_final.py --server.port 8090
"""
import streamlit as st

# Hard-coded signature (zero-error guard)
SIGNATURE_NAME = "Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau)"
SIGNATURE_TITLE = "Chairman, GCSLC Strategic Command"

# Primary widget: Global Strategic Context (UAE vs. Nigeria)
GLOBAL_STRATEGIC_CONTEXT = """
### GLOBAL STRATEGIC CONTEXT

| | |
|---|---|
| **UAE (G42/Microsoft)** | **$15.2B Investment** in AI Cloud |
| **NIGERIA (NGECC)** | **2 Billion MT** Coal Ground-Base |

*Strategic Insight:* The NVFC provides the energy feedstock (D1–D8) that global AI clouds need to thrive.
"""

# 8R Stealth Paradigm Convergence — engine of the NGECC mission (D1–D8)
D1, D2, D3, D4, D5, D6, D7, D8 = (
    "Refinement", "Reset", "Research", "Restructure",
    "Resuscitate", "Revitalize", "Re-engineer", "Retain",
)

# KPIs aligned with Node 8090 / app.html baseline
BASELINE_RESERVES_MT = 640.04
BASELINE_POWER_MW = 1199
BASELINE_STATES = 13
UAE_AI_INVESTMENT_B = 15.2
NIGERIA_COAL_GROUND_MT_B = 2.0  # 2 Billion MT narrative anchor

st.set_page_config(
    page_title="NVFC Sovereign Gateway — Streamlit",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sovereign shell + diagonal ghost watermark (30% opacity) — security overlay
st.markdown(
    """
<style>
  .stApp { background: linear-gradient(180deg, #0a0a1a 0%, #000033 50%, #0a0a1a 100%) !important; }
  [data-testid="stHeader"] { background: rgba(0,0,51,0.85) !important; }
  #nvfc-ghost-watermark {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 1000000;
    overflow: hidden;
  }
  #nvfc-ghost-watermark .ghost-diagonal {
    position: absolute;
    top: 38%;
    left: -30%;
    width: 200%;
    font-family: system-ui, -apple-system, sans-serif;
    font-size: clamp(1.25rem, 3.5vw, 2.25rem);
    font-weight: 800;
    letter-spacing: 0.18em;
    color: rgba(212, 175, 55, 0.3);
    white-space: nowrap;
    transform: rotate(-24deg);
    transform-origin: center center;
    user-select: none;
  }
  .nvfc-map-host {
    --navy-bg: #050a15;
    --navy-surface: #0a1225;
    --navy-border: #1e3a5f;
    --gold: #D4AF37;
    --gold-dim: #b8962e;
    --gold-bright: #f0c14b;
    --muted: #8fa3bf;
    font-family: 'Segoe UI', system-ui, sans-serif;
    color: #e8eef4;
    border-radius: 12px;
    overflow: hidden;
  }
  .nvfc-map-host .glassmorphism {
    background: var(--navy-surface);
    border: 1px solid var(--navy-border);
  }
  .nvfc-map-host .falcon-map-wrap {
    position: relative;
    min-height: 220px;
    margin-bottom: 0;
    border-radius: 12px;
    overflow: hidden;
  }
  .nvfc-map-host .nigeria-map-svg {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0.45;
  }
  .nvfc-map-host .nigeria-outline { width: 160px; height: auto; }
  .nvfc-map-host .falcon-sprite {
    position: absolute;
    width: 36px;
    height: 27px;
    z-index: 3;
    left: 42%;
    top: 62%;
    transform: translate(-50%, -50%);
  }
  .nvfc-map-host .falcon-svg { width: 100%; height: 100%; }
  .nvfc-map-host .falcon-wing.left {
    animation: nvfc-wing-l 0.45s ease-in-out infinite;
    transform-origin: right center;
  }
  .nvfc-map-host .falcon-wing.right {
    animation: nvfc-wing-r 0.45s ease-in-out infinite;
    transform-origin: left center;
  }
  @keyframes nvfc-wing-l {
    0%, 100% { transform: rotate(-5deg); }
    50% { transform: rotate(12deg); }
  }
  @keyframes nvfc-wing-r {
    0%, 100% { transform: rotate(5deg); }
    50% { transform: rotate(-12deg); }
  }
  .nvfc-map-host .falcon-data-bubble {
    position: absolute;
    z-index: 2;
    left: 48%;
    top: 52%;
    transform: translate(0, -100%);
    padding: 0.4rem 0.65rem;
    background: rgba(19, 39, 79, 0.92);
    border: 1px solid var(--gold);
    border-radius: 8px;
    font-size: 0.78rem;
    white-space: nowrap;
    box-shadow: 0 0 12px rgba(212, 175, 55, 0.25);
    pointer-events: none;
  }
  .nvfc-map-host .bubble-label { display: block; color: var(--muted); font-size: 0.65rem; text-transform: uppercase; }
  .nvfc-map-host .bubble-value { color: var(--gold-bright); font-weight: 700; }
  .nvfc-map-host .market-strike-data {
    position: absolute;
    bottom: 0.5rem;
    left: 0.5rem;
    z-index: 2;
    padding: 0.45rem 0.65rem;
    background: rgba(19, 39, 79, 0.94);
    border: 1px solid var(--gold);
    border-radius: 8px;
    font-size: 0.72rem;
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
  }
  .nvfc-map-host .strike-label { color: var(--muted); text-transform: uppercase; font-size: 0.6rem; }
  .nvfc-map-host .strike-ge { color: var(--gold-bright); font-weight: 700; }
  .nvfc-map-host .strike-nh3 { color: var(--gold); font-weight: 600; }
  .nvfc-map-host .falcon-convergence {
    display: grid;
    grid-template-columns: 1fr 168px;
    gap: 1rem;
    align-items: start;
  }
  @media (max-width: 700px) {
    .nvfc-map-host .falcon-convergence { grid-template-columns: 1fr; }
  }
  .nvfc-map-host .determinants-sidebar {
    padding: 0.75rem;
    border-radius: 12px;
    border: 1px solid var(--navy-border);
    background: rgba(0,0,0,0.25);
  }
  .nvfc-map-host .determinants-title {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.65rem;
    color: var(--gold);
  }
  .nvfc-map-host .determinant {
    padding: 0.35rem 0.45rem;
    margin-bottom: 0.3rem;
    border-radius: 6px;
    border: 1px solid var(--navy-border);
    font-size: 0.72rem;
    display: flex;
    align-items: center;
    gap: 0.45rem;
  }
  .nvfc-map-host .determinant.d1-on {
    border-color: var(--gold);
    background: rgba(212, 175, 55, 0.12);
    box-shadow: 0 0 10px rgba(212, 175, 55, 0.25);
  }
  .nvfc-map-host .det-badge { font-weight: 800; color: var(--gold); min-width: 1.8em; }
  .nvfc-map-host .det-label { color: var(--muted); font-size: 0.65rem; }
</style>
<div id="nvfc-ghost-watermark" aria-hidden="true">
  <div class="ghost-diagonal">GCSLC PROPRIETARY — LW15954 — NON-TRANSFERABLE — SOVEREIGN NODE</div>
</div>
""",
    unsafe_allow_html=True,
)

st.title("National Velocity Falcon Cloud (NVFC)")
st.caption("Streamlit engine · aligned with Node 8090 sovereign map · GCSLC LTD/GTE")

# Institutional metrics (Streamlit-native)
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("UAE AI cloud investment (G42 / Microsoft)", f"${UAE_AI_INVESTMENT_B}B")
with m2:
    st.metric("Nigeria coal ground-base (NGECC)", f"{NIGERIA_COAL_GROUND_MT_B}B MT")
with m3:
    st.metric("Power potential (AI DC ready)", f"{BASELINE_POWER_MW:,} MW")
with m4:
    st.metric("Proven reserves (13-state)", f"{BASELINE_RESERVES_MT} Mt")

st.markdown("---")

left, right = st.columns([1, 1.35])
with left:
    st.markdown(GLOBAL_STRATEGIC_CONTEXT)
    st.markdown("---")
    st.subheader("8R Stealth Paradigm Convergence")
    st.caption("Engine of the NGECC mission")
    for i, d in enumerate(
        (D1, D2, D3, D4, D5, D6, D7, D8), start=1
    ):
        st.markdown(f"**D{i}** {d}")

with right:
    st.subheader("High-fidelity Nigeria map — Falcon convergence (Node 8090 parity)")
    # Embedded markup mirrors app.html falcon-map-wrap + determinants strip
    st.markdown(
        """
<div class="nvfc-map-host">
  <div class="falcon-convergence">
    <div class="falcon-map-wrap glassmorphism">
      <div class="nigeria-map-svg" aria-hidden="true">
        <svg viewBox="0 0 200 240" class="nigeria-outline" xmlns="http://www.w3.org/2000/svg">
          <path fill="none" stroke="#1e3a5f" stroke-width="1.5"
            d="M100 20 L160 50 L180 100 L165 160 L120 220 L80 200 L40 150 L35 90 L60 40 Z" />
        </svg>
      </div>
      <div class="falcon-data-bubble">
        <span class="bubble-label">NGECC SSMV Strike</span>
        <span class="bubble-value">High-Value Feedstock Detected — Edo</span>
      </div>
      <div class="market-strike-data">
        <span class="strike-label">Global demand at this state</span>
        <span class="strike-ge">Germanium: $8,597/kg</span>
        <span class="strike-nh3">Ammonia: $430/MT</span>
      </div>
      <div class="falcon-sprite" aria-hidden="true">
        <svg viewBox="0 0 32 24" class="falcon-svg" xmlns="http://www.w3.org/2000/svg">
          <path class="falcon-body" fill="#b8962e" stroke="#D4AF37" stroke-width="0.5"
            d="M16 12 L8 14 L6 12 L8 10 L16 8 L24 10 L26 12 L24 14 Z" />
          <path class="falcon-wing left" fill="#D4AF37" d="M14 11 L4 8 L2 10 L6 12 Z" />
          <path class="falcon-wing right" fill="#D4AF37" d="M18 11 L28 8 L30 10 L26 12 Z" />
          <path class="falcon-head" fill="#f0c14b" d="M16 6 L18 4 L20 6 L18 8 Z" />
        </svg>
      </div>
    </div>
    <aside class="determinants-sidebar glassmorphism" aria-label="8R Determinants">
      <div class="determinants-title">Determinants (8R)</div>
      <div class="determinant d1-on"><span class="det-badge">D1</span><span class="det-label">Trigger</span></div>
      <div class="determinant"><span class="det-badge">D2</span><span class="det-label">Trigger</span></div>
      <div class="determinant"><span class="det-badge">D3</span><span class="det-label">Trigger</span></div>
      <div class="determinant"><span class="det-badge">D4</span><span class="det-label">Trigger</span></div>
      <div class="determinant"><span class="det-badge">D5</span><span class="det-label">Trigger</span></div>
      <div class="determinant"><span class="det-badge">D6</span><span class="det-label">Trigger</span></div>
      <div class="determinant"><span class="det-badge">D7</span><span class="det-label">Trigger</span></div>
      <div class="determinant"><span class="det-badge">D8</span><span class="det-label">Trigger</span></div>
    </aside>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown("### NVFC Strategic Command")
st.markdown(
    "*National Velocity Falcon Cloud* — sovereign energy feedstock for global AI infrastructure."
)
st.markdown(f"### {SIGNATURE_NAME}")
st.caption(SIGNATURE_TITLE)
