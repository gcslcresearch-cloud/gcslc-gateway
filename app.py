import math
import time

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="GCSLC Victory Donut 8507", layout="wide")

NAVY = "#001F3F"
GOLD = "#D4AF37"
CYAN = "#00E5FF"

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Goldman', sans-serif;
    background-color: #001F3F;
    color: #D4AF37;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 1.4rem;
}

.prism-frame {
    border: 1px solid #00E5FF;
    outline: 1px solid #D4AF37;
    outline-offset: 4px;
    border-radius: 14px;
    padding: 0.9rem;
    margin: 0.3rem 0 1.1rem 0;
    background: #001F3F;
}

.title-card {
    border: 1px solid #00E5FF;
    border-radius: 14px;
    background: rgba(0, 31, 63, 0.96);
    padding: 1rem 1.2rem;
    margin-bottom: 0.9rem;
}

.section-head {
    color: #D4AF37;
    margin-top: 0.3rem;
    margin-bottom: 0.4rem;
}

.swot-grid {
    display: grid;
    grid-template-columns: repeat(5, minmax(170px, 1fr));
    gap: 10px;
    margin-top: 0.4rem;
    margin-bottom: 1rem;
}

.swot-card {
    border: 1px solid #00E5FF;
    border-radius: 12px;
    background: rgba(0, 31, 63, 0.92);
    padding: 0.7rem;
    min-height: 145px;
}

.swot-card h4 {
    color: #D4AF37;
    margin: 0 0 0.4rem 0;
    font-size: 1rem;
}

.swot-card p {
    color: #00E5FF;
    margin: 0.2rem 0;
    font-size: 0.85rem;
}

.small-note {
    color: #00E5FF;
    font-size: 0.82rem;
    margin-top: -0.2rem;
}

.understand-box button {
    border: 1px solid #00E5FF !important;
    border-radius: 12px !important;
    background: rgba(0, 31, 63, 0.95) !important;
    color: #D4AF37 !important;
    font-weight: 700 !important;
}

.understand-box button:hover {
    border-color: #D4AF37 !important;
    color: #00E5FF !important;
}

.gcslc-modal {
    border: 1px solid #00E5FF;
    border-radius: 14px;
    background: rgba(0, 31, 63, 0.98);
    padding: 0.9rem 1rem;
    margin: 0.7rem auto;
}

.gcslc-modal h4 {
    color: #D4AF37;
    margin: 0 0 0.35rem 0;
}

.gcslc-modal p {
    color: #00E5FF;
    margin: 0;
}
</style>
""",
    unsafe_allow_html=True,
)

st.sidebar.markdown("## CIEN: Verified Votes")
st.sidebar.metric("Verified Votes Stream", "730,002", "+18,700")

st.markdown(
    """
<div class="prism-frame">
<div class="title-card">
  <h1 style="color:#D4AF37; margin:0;">GCSLC Victory Donut — Kaduna 8507</h1>
  <p style="color:#00E5FF; margin:0.4rem 0 0 0;">Dr. Sa’ad Strategic Operations Board</p>
</div>
""",
    unsafe_allow_html=True,
)

# 1) Victory Pulse — single pulsing graph (2023 APC vs 2027 projection)
pulse_factor = 18 + int((math.sin(time.time() * 2) + 1) * 8)
pulse_df = pd.DataFrame(
    {
        "Milestone": ["2023 Actuals (APC)", "2027 15/15 Projection"],
        "Votes": [730_002, 1_800_000],
    }
)
pulse_fig = go.Figure()
pulse_fig.add_trace(
    go.Scatter(
        x=pulse_df["Milestone"],
        y=pulse_df["Votes"],
        mode="lines+markers+text",
        text=[f"{v:,}" for v in pulse_df["Votes"]],
        textposition="top center",
        marker={"size": [14, pulse_factor], "color": GOLD},
        line={"color": CYAN, "width": 4},
        name="Victory Pulse",
    )
)
pulse_fig.update_layout(
    title="Victory Pulse: 2023 Actuals (APC) vs 2027 15/15 Projection",
    plot_bgcolor=NAVY,
    paper_bgcolor=NAVY,
    font={"color": GOLD},
    xaxis={"title": "", "gridcolor": "#003D66"},
    yaxis={"title": "Votes", "gridcolor": "#003D66"},
    height=360,
)
st.plotly_chart(pulse_fig, use_container_width=True)

# 2) Historical trend — Apathy Gap / turnout decay
apathy_df = pd.DataFrame(
    {
        "Year": [2015, 2019, 2023],
        "Turnout %": [58, 49, 41],
        "Apathy Gap %": [42, 51, 59],
    }
)
trend_fig = go.Figure()
trend_fig.add_trace(
    go.Scatter(
        x=apathy_df["Year"],
        y=apathy_df["Turnout %"],
        mode="lines+markers+text",
        text=[f"{v}%" for v in apathy_df["Turnout %"]],
        textposition="top center",
        marker={"size": 13, "color": CYAN},
        line={"color": CYAN, "width": 3},
        name="Turnout",
    )
)
trend_fig.add_trace(
    go.Scatter(
        x=apathy_df["Year"],
        y=apathy_df["Apathy Gap %"],
        mode="lines+markers+text",
        text=[f"{v}%" for v in apathy_df["Apathy Gap %"]],
        textposition="bottom center",
        marker={"size": 13, "color": GOLD},
        line={"color": GOLD, "width": 3},
        name="Apathy Gap",
    )
)
trend_fig.update_layout(
    title="Historical Trend: Turnout Decay and Apathy Gap (2015–2023)",
    plot_bgcolor=NAVY,
    paper_bgcolor=NAVY,
    font={"color": GOLD},
    xaxis={"dtick": 4, "gridcolor": "#003D66"},
    yaxis={"title": "Percent", "range": [30, 65], "gridcolor": "#003D66"},
    legend={"orientation": "h", "y": 1.08, "x": 0.04},
    height=340,
)
st.plotly_chart(trend_fig, use_container_width=True)

# 3) 2027 SWOT — Goldman via global font; merger lines for opposition
st.markdown('<h3 class="section-head">2027 SWOT Analysis</h3>', unsafe_allow_html=True)
swot = {
    "APC": "Strength: incumbency infrastructure\nOpportunity: consolidate turnout engines.",
    "ADC": "Merger Opportunity: absorb ward-level reform clusters and local canvass teams.",
    "PDP": "Merger Opportunity: align disaffected legacy blocs into issue-based coalition units.",
    "LP": "Merger Opportunity: convert youth digital cells into coordinated GOTV partners.",
    "SDP": "Merger Opportunity: integrate micro-structures in competitive LGAs for ballot security.",
}
cards = []
for party, note in swot.items():
    lines = "".join(f"<p>{ln}</p>" for ln in note.split("\n"))
    cards.append(f'<div class="swot-card"><h4>{party}</h4>{lines}</div>')
st.markdown(f'<div class="swot-grid">{"".join(cards)}</div>', unsafe_allow_html=True)

# 4) Kaduna 23 LGAs — gold markers (shimmer via size cycle is optional; spec requires size 15)
st.markdown('<h3 class="section-head">2027 Projection Map — 23 LGAs</h3>', unsafe_allow_html=True)
st.markdown(
    '<p class="small-note">Shimmering gold markers — select a point for Target and Ballot Box Count.</p>',
    unsafe_allow_html=True,
)

lga_data = [
    ("Birnin Gwari", 10.6456, 6.5403, 312),
    ("Chikun", 10.5236, 7.4383, 428),
    ("Giwa", 11.3153, 7.4497, 295),
    ("Igabi", 10.7963, 7.6005, 387),
    ("Ikara", 11.1822, 8.2240, 271),
    ("Jaba", 9.3210, 8.2842, 163),
    ("Jema'a", 9.2137, 8.3722, 202),
    ("Kachia", 9.8764, 7.9541, 246),
    ("Kaduna North", 10.5410, 7.4380, 341),
    ("Kaduna South", 10.4811, 7.4402, 336),
    ("Kagarko", 9.4665, 7.6822, 188),
    ("Kajuru", 10.3221, 7.6484, 177),
    ("Kaura", 9.5865, 8.4622, 169),
    ("Kauru", 10.6564, 8.1396, 214),
    ("Kubau", 10.9122, 8.4111, 237),
    ("Kudan", 11.0527, 7.8312, 206),
    ("Lere", 10.3884, 8.3851, 223),
    ("Makarfi", 11.3772, 7.8743, 191),
    ("Sabon Gari", 11.1125, 7.7222, 258),
    ("Sanga", 9.5712, 8.3779, 171),
    ("Soba", 10.9812, 8.0615, 236),
    ("Zangon Kataf", 9.7037, 8.2899, 209),
    ("Zaria", 11.0671, 7.7197, 365),
]
map_df = pd.DataFrame(lga_data, columns=["LGA", "lat", "lon", "Ballot Boxes"])

map_fig = go.Figure(
    go.Scattermapbox(
        lat=map_df["lat"],
        lon=map_df["lon"],
        mode="markers",
        text=[
            f"{row.LGA}<br>Target: 15/15 Success<br>Ballot Box Count: {row['Ballot Boxes']}"
            for _, row in map_df.iterrows()
        ],
        hoverinfo="text",
        marker={"size": 15, "color": "gold"},
        name="Kaduna LGAs",
    )
)
map_fig.update_layout(
    mapbox={"style": "carto-darkmatter", "zoom": 6.8, "center": {"lat": 10.5, "lon": 7.8}},
    plot_bgcolor=NAVY,
    paper_bgcolor=NAVY,
    font={"color": GOLD},
    margin={"l": 0, "r": 0, "t": 0, "b": 0},
    height=520,
)
map_event = st.plotly_chart(
    map_fig,
    use_container_width=True,
    on_select="rerun",
    selection_mode="points",
)

if map_event and map_event.get("selection", {}).get("points"):
    idx = map_event["selection"]["points"][0]["point_index"]
    row = map_df.iloc[idx]
    st.success(
        f"{row['LGA']} — Target: 15/15 Success | Ballot Box Count: {row['Ballot Boxes']}"
    )
else:
    st.caption("Click a gold marker: Target 15/15 Success and Ballot Box Count.")

# 5) 8R Hub — Understand Boxes
st.markdown('<h3 class="section-head">8R Strategic Hub</h3>', unsafe_allow_html=True)
messages = {
    "R1 Understand Box": "Rebuild trust via polling-unit proximity structures and evidence-led messaging.",
    "R2 Understand Box": "Re-activate dormant supporters with household-level contact cycles.",
    "R3 Understand Box": "Re-target persuasion blocs where apathy is high but APC favorability is recoverable.",
    "R4 Understand Box": "Reinforce ballot security through observer discipline and incident escalation lanes.",
    "R5 Understand Box": "Re-message youth channels using jobs, dignity, and delivery-focused narratives.",
    "R6 Understand Box": "Reconcile factional interests under one turnout covenant per ward.",
    "R7 Understand Box": "Rehearse election-day logistics weekly to remove uncertainty from mobilization.",
    "R8 Understand Box": "Reward high-performing field cells with visibility, data access, and operational support.",
}

if "selected_r" not in st.session_state:
    st.session_state["selected_r"] = "R1 Understand Box"
if "show_modal" not in st.session_state:
    st.session_state["show_modal"] = False

cols = st.columns(4)
for i, key in enumerate(messages):
    with cols[i % 4]:
        st.markdown('<div class="understand-box">', unsafe_allow_html=True)
        if st.button(key, key=f"box_{i}", use_container_width=True):
            st.session_state["selected_r"] = key
            st.session_state["show_modal"] = True
        st.markdown("</div>", unsafe_allow_html=True)

selected = st.session_state["selected_r"]
if st.session_state["show_modal"]:
    st.markdown(
        f"""
<div class="gcslc-modal">
  <h4>{selected}</h4>
  <p>{messages[selected]}</p>
</div>
""",
        unsafe_allow_html=True,
    )
    if st.button("Close", key="close_modal"):
        st.session_state["show_modal"] = False

st.markdown("</div>", unsafe_allow_html=True)
