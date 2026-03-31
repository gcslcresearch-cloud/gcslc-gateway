import re
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="GCSLC Victory Donut 8507", layout="wide")

NAVY = "#000022"
GOLD = "#D4AF37"
CYAN = "#00FFFF"
TURQUOISE = "#40E0D0"

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Goldman', sans-serif;
    background-color: #000022;
    color: #D4AF37;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 1.4rem;
}

.prism-frame {
    border: 1px solid #D4AF37;
    outline: 1px solid #D4AF37;
    outline-offset: 5px;
    border-radius: 14px;
    padding: 0.9rem;
    margin: 0.3rem 0 1.1rem 0;
    background: #000022;
}

.title-card {
    border: 1px solid #D4AF37;
    border-radius: 14px;
    background: rgba(0, 0, 34, 0.96);
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
    border: 1px solid #D4AF37;
    border-radius: 12px;
    background: rgba(0, 0, 34, 0.92);
    padding: 0.7rem;
    min-height: 145px;
}

.swot-card h4 {
    color: #D4AF37;
    margin: 0 0 0.4rem 0;
    font-size: 1rem;
}

.swot-card p {
    color: #D4AF37;
    margin: 0.2rem 0;
    font-size: 0.85rem;
}

.small-note {
    color: #D4AF37;
    font-size: 0.82rem;
    margin-top: -0.2rem;
}

.gold-metric {
    border: 1px solid #D4AF37;
    border-radius: 12px;
    background: rgba(212, 175, 55, 0.08);
    padding: 0.6rem 0.75rem;
    margin-top: 0.5rem;
}

.gold-metric .label {
    color: #D4AF37;
    font-size: 0.78rem;
}

.gold-metric .value {
    color: #D4AF37;
    font-size: 1.35rem;
    font-weight: 700;
}

.gold-status {
    margin-top: 0.35rem;
    border-left: 2px solid #D4AF37;
    padding-left: 0.45rem;
    font-size: 0.72rem;
    color: #D4AF37;
    line-height: 1.35;
}

.understand-box button {
    border: 1px solid #D4AF37 !important;
    border-radius: 12px !important;
    background: rgba(0, 0, 34, 0.95) !important;
    color: #D4AF37 !important;
    font-weight: 700 !important;
}

.understand-box button:hover {
    border-color: #D4AF37 !important;
    color: #D4AF37 !important;
}

.gcslc-modal {
    border: 1px solid #D4AF37;
    border-radius: 14px;
    background: rgba(0, 0, 34, 0.98);
    padding: 0.9rem 1rem;
    margin: 0.7rem auto;
}

.gcslc-modal h4 {
    color: #D4AF37;
    margin: 0 0 0.35rem 0;
}

.gcslc-modal p {
    color: #D4AF37;
    margin: 0;
}
</style>
""",
    unsafe_allow_html=True,
)

def normalize_name(name: str) -> str:
    compact = re.sub(r"\s+", "", str(name).strip().lower())
    return re.sub(r"[^a-z0-9]", "", compact)


def build_lga_aliases() -> dict[str, str]:
    names = [
        "Birnin Gwari",
        "Chikun",
        "Giwa",
        "Igabi",
        "Ikara",
        "Jaba",
        "Jema'a",
        "Kachia",
        "Kaduna North",
        "Kaduna South",
        "Kagarko",
        "Kajuru",
        "Kaura",
        "Kauru",
        "Kubau",
        "Kudan",
        "Lere",
        "Makarfi",
        "Sabon Gari",
        "Sanga",
        "Soba",
        "Zangon Kataf",
        "Zaria",
    ]
    return {normalize_name(n): normalize_name(n) for n in names}


def extract_ballot_box_count(df: pd.DataFrame) -> int:
    preferred_cols = [
        "ballot box count",
        "ballot_boxes",
        "ballotboxcount",
        "polling unit count",
        "polling_unit_count",
        "pollingunits",
        "pu_count",
    ]
    normalized = {normalize_name(col): col for col in df.columns}
    for col_key in preferred_cols:
        hit = normalized.get(normalize_name(col_key))
        if hit is None:
            continue
        numeric_series = pd.to_numeric(df[hit], errors="coerce").dropna()
        if not numeric_series.empty:
            return int(numeric_series.sum())
    return int(len(df.index))


st.sidebar.markdown("## CIEN: Verified Votes")
uploaded_files = st.sidebar.file_uploader(
    "RHGI .xlsx Files (ZARIA, GIWA, SABON GARI, etc.)",
    type=["xlsx"],
    accept_multiple_files=True,
)

detected_files = []
if uploaded_files:
    detected_files.extend(uploaded_files)
else:
    detected_files.extend(sorted(Path(".").glob("*.xlsx")))

ingested_rows_total = 0
lga_ballot_lookup: dict[str, int] = {}
lga_aliases = build_lga_aliases()
for f in detected_files:
    file_name = f.name if hasattr(f, "name") else str(f)
    try:
        frame = pd.read_excel(f)
        rows = int(len(frame.index))
        ingested_rows_total += rows

        ballot_count = extract_ballot_box_count(frame)
        stem_key = normalize_name(Path(file_name).stem)
        matched_lga_key = stem_key
        for alias in lga_aliases:
            if alias in stem_key or stem_key in alias:
                matched_lga_key = alias
                break
        lga_ballot_lookup[matched_lga_key] = ballot_count
    except Exception:
        continue

st.sidebar.markdown(
    f"""
<div class="gold-metric">
  <div class="label">CIEN: Total Ingested Voters</div>
  <div class="value">{ingested_rows_total:,}</div>
</div>
""",
    unsafe_allow_html=True,
)
st.sidebar.caption(f"CIEN RHGI files detected: {len(detected_files)}")
if ingested_rows_total == 0:
    st.sidebar.error("No rows ingested from .xlsx files. Upload valid LGA Excel files (e.g., ZARIA.xlsx, GIWA.xlsx).")
    st.stop()

st.markdown(
    """
<div class="prism-frame">
<div class="title-card">
  <h1 style="color:#D4AF37; margin:0;">GCSLC Victory Donut - Kaduna 8507</h1>
  <p style="color:#D4AF37; margin:0.4rem 0 0 0;">Dr. Sa’ad Strategic Operations Board</p>
</div>
""",
    unsafe_allow_html=True,
)

# Victory donut (2023 vs 2027)
donut_fig = go.Figure(
    go.Pie(
        labels=["2023 Actuals", "2027 15/15 Projection"],
        values=[730002, 1800000],
        hole=0.62,
        pull=[0.0, 0.08],
        marker={"colors": [CYAN, GOLD]},
        text=[f"730,002", f"1,800,000"],
        textinfo="label+text",
        textfont={"color": GOLD, "size": 14},
        sort=False,
        direction="clockwise",
    )
)
donut_fig.update_layout(
    title="Victory Donut: 2023 Actuals vs 2027 Projection",
    plot_bgcolor=NAVY,
    paper_bgcolor=NAVY,
    font={"color": GOLD},
    showlegend=True,
    height=360,
)
st.plotly_chart(donut_fig, use_container_width=True)

# Historical turnout decay / apathy gap trend
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
    title="Historical Trend: Turnout Decay and Apathy Gap",
    plot_bgcolor=NAVY,
    paper_bgcolor=NAVY,
    font={"color": GOLD},
    xaxis={"dtick": 4, "gridcolor": GOLD},
    yaxis={"title": "Percent", "range": [30, 65], "gridcolor": GOLD},
    legend={"orientation": "h", "y": 1.08, "x": 0.04},
    height=340,
)
st.plotly_chart(trend_fig, use_container_width=True)

# 2027 SWOT analysis grid
st.markdown('<h3 class="section-head">2027 SWOT + Merger Opportunities</h3>', unsafe_allow_html=True)
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

st.markdown('<h3 class="section-head">2027 Projection Map - 23 LGAs</h3>', unsafe_allow_html=True)
st.markdown(
    '<p class="small-note">Gold markers are linked to LGA files; click to inspect target and ballot box counts.</p>',
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
map_df["Target"] = "15/15 Success"
map_df["file_key"] = map_df["LGA"].apply(normalize_name)
map_df["Ballot Boxes"] = map_df.apply(
    lambda r: lga_ballot_lookup.get(r["file_key"], r["Ballot Boxes"]), axis=1
)

missing_lga_sources = map_df.loc[
    ~map_df["file_key"].isin(set(lga_ballot_lookup.keys())), "LGA"
].tolist()
matched_lga_count = len(map_df) - len(missing_lga_sources)
if detected_files:
    st.sidebar.caption(f"LGA files matched: {matched_lga_count}/23")
if missing_lga_sources:
    names = "".join(f"<li>{name}</li>" for name in missing_lga_sources)
    st.sidebar.markdown(
        f"""
<div class="gold-status">
  <div><strong>Missing LGA Excel Match ({len(missing_lga_sources)}):</strong></div>
  <ul style="margin:0.15rem 0 0 0.8rem; padding:0;">
    {names}
  </ul>
</div>
""",
        unsafe_allow_html=True,
    )
else:
    st.sidebar.markdown(
        '<div class="gold-status"><strong>All 23 LGAs are data-verified from uploaded Excel files.</strong></div>',
        unsafe_allow_html=True,
    )

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
        marker={"size": [14 + (i % 3) for i in range(len(map_df))], "color": "gold"},
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
    st.markdown(
        f"""
<div class="gold-status">
  <strong>{row['LGA']}</strong> -> Target: 15/15 Success | Ballot Box Count: {row['Ballot Boxes']}
</div>
""",
        unsafe_allow_html=True,
    )
else:
    st.caption("Select a gold marker to reveal target and ballot box count.")

st.markdown('<h3 class="section-head">8R Strategic Understand Hub</h3>', unsafe_allow_html=True)
messages = {
    "Refine": "Refine trust signals through polling-unit proximity structures and evidence-led messaging.",
    "Reset": "Reset dormant support networks with household-level contact cycles.",
    "Research": "Research persuasion blocs where apathy is high but APC favorability can recover.",
    "Restructure": "Restructure ward-level mobilization for disciplined turnout execution.",
    "Resuscitate": "Resuscitate youth-facing narrative channels around dignity and delivery.",
    "Revitalize": "Revitalize coalition alignment under one turnout covenant per ward.",
    "Re-engineer": "Re-engineer election-day logistics with weekly field rehearsals.",
    "Retain": "Retain high-performing field cells with visibility, data access, and support.",
}

if "selected_r" not in st.session_state:
    st.session_state["selected_r"] = "Refine"
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
    if st.button("Close Strategic Message", key="close_modal"):
        st.session_state["show_modal"] = False
st.markdown("</div>", unsafe_allow_html=True)
