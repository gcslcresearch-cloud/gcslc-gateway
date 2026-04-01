# CIEN Kaduna 2027 — Galadiman Ruwa Center (GCSLC LTD/GTE)
# Run: python3 -m streamlit run cien_kaduna_2027.py --server.port 9099

from __future__ import annotations

import html
import os

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

os.environ.setdefault("STREAMLIT_SERVER_PORT", "9099")
os.environ.setdefault("STREAMLIT_SERVER_FILE_WATCHER_TYPE", "none")

NAVY_DEEP = "#000033"
GOLD = "#D4AF37"
CYAN = "#00E5FF"

ORG_NAME = "Galadiman Ruwa Center for Strategic Leadership and Communication LTD/GTE"
MOTTO = (
    "We decode the Kaduna 2027 election based on our superior 15/15 scientific model."
)

# 2023 governorship tight margin (statewide)
V_2023_APC = 730_002
V_2023_PDP = 719_196
V_2023_LP = 58_285
V_2023_TOTAL = V_2023_APC + V_2023_PDP + V_2023_LP

LGA_TARGET = 23
LGA_MAJORITY_NEED = 16
DENSITY_DB = 1_500_000
DENSITY_FACTOR = DENSITY_DB / V_2023_TOTAL

# Zone baselines (sum to statewide 2023)
ZONES: dict[str, dict[str, int]] = {
    "Zone 1: Central": {"APC": 268_000, "PDP": 251_000, "LP": 28_000},
    "Zone 2: North": {"APC": 298_000, "PDP": 262_000, "LP": 14_000},
    "Zone 3: South": {"APC": 164_002, "PDP": 206_196, "LP": 16_285},
}


def _zone_2027_projection(row: dict[str, int]) -> dict[str, int]:
    """Scale by 1.5M database density + 15/15 model uplift (illustrative)."""
    out: dict[str, int] = {}
    for k, v in row.items():
        uplift = 1.042 if k == "APC" else (0.988 if k == "PDP" else 1.015)
        out[k] = int(round(v * DENSITY_FACTOR * uplift))
    return out


DETERMINANTS: dict[str, str] = {
    "D1": (
        "Reach Density: Polling-unit proximity grids weighted by the 1.5M voter pool — "
        "where contact depth meets turnout elasticity."
    ),
    "D2": (
        "Resource Alignment: Executive-Load-142 cadence matched to ward-level nodal strength "
        "so spend follows ballot-box leverage."
    ),
    "D3": (
        "Reputation Capital: Incumbency delivery narratives reinforced by third-party validators "
        "in high-trust community nodes."
    ),
    "D4": (
        "Rival Neutralization: Counter-messaging lanes that collapse opposition fragmentation "
        "without amplifying their frames."
    ),
    "D5": (
        "Rally Cadence: Rhythmic mobilization (weekly → daily → election hour) synced to "
        "logistics rehearsal and observer coverage."
    ),
    "D6": (
        "Resilience & Compliance: Incident escalation, data hygiene, and audit-ready reporting "
        "for field integrity."
    ),
    "D7": (
        "Recognition Systems: High-performing cells receive visibility, data access, and "
        "repeatable playbooks."
    ),
    "D8": (
        "Replication Runbooks: Standard operating packages per LGA so 18/25 nodal targets "
        "scale without drift."
    ),
}

# LGA name, lat, lon, ballot boxes (targets), nodal_strength / 25
LGA_ROWS: list[tuple[str, float, float, int, int]] = [
    ("Birnin Gwari", 10.6456, 6.5403, 312, 17),
    ("Chikun", 10.5236, 7.4383, 428, 19),
    ("Giwa", 11.3153, 7.4497, 295, 18),
    ("Igabi", 10.7963, 7.6005, 387, 20),
    ("Ikara", 11.1822, 8.2240, 271, 17),
    ("Jaba", 9.3210, 8.2842, 163, 16),
    ("Jema'a", 9.2137, 8.3722, 202, 18),
    ("Kachia", 9.8764, 7.9541, 246, 18),
    ("Kaduna North", 10.5410, 7.4380, 341, 21),
    ("Kaduna South", 10.4811, 7.4402, 336, 20),
    ("Kagarko", 9.4665, 7.6822, 188, 17),
    ("Kajuru", 10.3221, 7.6484, 177, 17),
    ("Kaura", 9.5865, 8.4622, 169, 16),
    ("Kauru", 10.6564, 8.1396, 214, 18),
    ("Kubau", 10.9122, 8.4111, 237, 18),
    ("Kudan", 11.0527, 7.8312, 206, 17),
    ("Lere", 10.3884, 8.3851, 223, 18),
    ("Makarfi", 11.3772, 7.8743, 191, 17),
    ("Sabon Gari", 11.1125, 7.7222, 258, 19),
    ("Sanga", 9.5712, 8.3779, 171, 17),
    ("Soba", 10.9812, 8.0615, 236, 18),
    ("Zangon Kataf", 9.7037, 8.2899, 209, 18),
    ("Zaria", 11.0671, 7.7197, 365, 22),
]

MASTER_2027 = _zone_2027_projection(
    {"APC": V_2023_APC, "PDP": V_2023_PDP, "LP": V_2023_LP}
)

_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap');

@keyframes cien-pulse-gold {
  0%, 100% { transform: scale(1); opacity: 1; filter: brightness(1); }
  50% { transform: scale(1.02); opacity: 0.92; filter: brightness(1.12); }
}
@keyframes prism-shimmer {
  0% { background-position: 0% 50%; }
  100% { background-position: 200% 50%; }
}

html, body, [data-testid="stAppViewContainer"] {
  font-family: 'Goldman', sans-serif !important;
  background-color: #000033 !important;
  color: #D4AF37 !important;
}
.stApp, [data-testid="stAppViewContainer"] {
  background: linear-gradient(180deg, #000022 0%, #000033 55%, #000044 100%) !important;
}
.block-container { padding-top: 0.75rem !important; padding-bottom: 1.2rem !important; }

.prism-widget {
  border-radius: 14px;
  padding: 3px;
  background: linear-gradient(120deg, #000033, #D4AF37, #00e5ff, #000033);
  background-size: 280% 100%;
  animation: prism-shimmer 12s linear infinite;
  margin-bottom: 0.85rem;
}
.prism-widget-inner {
  background: linear-gradient(180deg, #000011 0%, #000044 100%);
  border-radius: 11px;
  padding: 0.9rem 1rem;
  border: 1px solid rgba(212, 175, 55, 0.35);
}
.cien-identity-stack {
  max-width: 56rem;
  margin: 0 auto;
  text-align: center;
}
.cien-title {
  font-family: 'Goldman', sans-serif !important;
  font-weight: 700 !important;
  color: #FFD700 !important;
  font-size: clamp(1.05rem, 2.9vw, 1.5rem);
  letter-spacing: 0.04em;
  margin: 0 0 0.45rem 0;
  text-align: center;
  line-height: 1.35;
  text-shadow:
    0 0 1px rgba(255, 215, 0, 0.95),
    0 1px 0 rgba(139, 105, 20, 0.45),
    0 -1px 0 rgba(255, 248, 200, 0.35),
    0 0 12px rgba(255, 215, 0, 0.25);
}
.cien-motto {
  font-family: 'Goldman', sans-serif !important;
  color: #00E5FF !important;
  font-size: 0.72rem;
  text-align: center;
  margin: 0 0 0.5rem 0;
  line-height: 1.5;
  letter-spacing: 0.02em;
}
.cien-foundation {
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.65rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(0, 229, 255, 0.72) !important;
  text-align: center;
  margin: 0;
  line-height: 1.4;
  border-top: 1px solid rgba(0, 229, 255, 0.2);
  padding-top: 0.5rem;
}
.cien-foundation .cien-8r {
  color: #FFD700 !important;
  font-weight: 700;
  letter-spacing: 0.1em;
}
.section-prism {
  margin-top: 1rem;
  margin-bottom: 0.5rem;
  padding: 0.5rem 0.65rem;
  border: 2px solid #D4AF37;
  outline: 1px solid #00E5FF;
  outline-offset: 3px;
  border-radius: 12px;
  background: rgba(0,0,34,0.92);
}
.section-prism h3 {
  font-family: 'Goldman', sans-serif !important;
  color: #D4AF37 !important;
  margin: 0;
  font-size: 1.05rem;
  letter-spacing: 0.06em;
}

.twothirds-wrap {
  margin-top: 0.5rem;
}
.twothirds-label {
  display: flex;
  justify-content: space-between;
  font-family: 'Goldman', sans-serif !important;
  color: #D4AF37 !important;
  font-size: 0.78rem;
  margin-bottom: 0.25rem;
}
.twothirds-track {
  height: 22px;
  border-radius: 10px;
  border: 1px solid #D4AF37;
  background: #000022;
  overflow: hidden;
}
.twothirds-fill {
  height: 100%;
  width: """ + str(round(100 * LGA_MAJORITY_NEED / LGA_TARGET, 2)) + """%;
  background: linear-gradient(90deg, #b8860b, #D4AF37, #00e5ff);
  box-shadow: 0 0 14px rgba(212,175,55,0.45);
}

.zone-prism-btn button {
  font-family: 'Goldman', sans-serif !important;
  border-radius: 12px !important;
  border: 2px solid #D4AF37 !important;
  background: linear-gradient(180deg, #1a1a2e 0%, #0f0f22 100%) !important;
  color: #D4AF37 !important;
  font-weight: 700 !important;
  min-height: 3.2rem !important;
  box-shadow: inset 0 0 12px rgba(0,229,255,0.12), 0 2px 8px rgba(0,0,0,0.35) !important;
}
.zone-prism-btn button:hover {
  border-color: #00E5FF !important;
  color: #00E5FF !important;
}

.d8-box {
  border-radius: 12px;
  padding: 3px;
  background: linear-gradient(120deg, #2a2a3a, #D4AF37, #8899aa, #D4AF37, #2a2a3a);
  background-size: 300% 100%;
  animation: prism-shimmer 6s linear infinite;
  margin-bottom: 0.45rem;
}
.d8-inner {
  background: linear-gradient(180deg, #0a0a18 0%, #12122a 100%);
  border-radius: 9px;
  padding: 0.55rem;
  border: 1px solid rgba(212,175,55,0.4);
}
.d8-inner button {
  font-family: 'Goldman', sans-serif !important;
  width: 100%;
  background: transparent !important;
  border: none !important;
  color: #D4AF37 !important;
  font-weight: 700 !important;
  font-size: 0.95rem !important;
}

.sidebar-pool {
  font-family: 'Goldman', sans-serif !important;
  font-size: clamp(1.4rem, 4vw, 2rem);
  font-weight: 700;
  color: #D4AF37 !important;
  text-align: center;
  animation: cien-pulse-gold 2.2s ease-in-out infinite;
  text-shadow: 0 0 18px rgba(212,175,55,0.55);
}
.sidebar-handshake {
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.78rem;
  color: #00E5FF !important;
  line-height: 1.55;
  border: 1px solid rgba(212,175,55,0.35);
  border-radius: 10px;
  padding: 0.65rem;
  background: rgba(0,0,34,0.85);
  margin-top: 0.75rem;
}

.det-modal {
  border: 2px solid #D4AF37;
  outline: 1px solid #00E5FF;
  outline-offset: 2px;
  border-radius: 12px;
  padding: 0.85rem 1rem;
  background: #000022;
  margin-top: 0.5rem;
}
.det-modal h4 { color: #D4AF37 !important; margin: 0 0 0.4rem 0; font-family: 'Goldman', sans-serif !important; }
.det-modal p { color: #00E5FF !important; margin: 0; font-size: 0.88rem; line-height: 1.5; }
"""


def _donut_purity() -> go.Figure:
    fig = go.Figure(
        data=[
            go.Pie(
                labels=["APC", "PDP", "LP"],
                values=[V_2023_APC, V_2023_PDP, V_2023_LP],
                hole=0.52,
                marker=dict(colors=["#D4AF37", "#00E5FF", "#8899aa"], line=dict(color="#000033", width=2)),
                textinfo="label+value",
                texttemplate="%{label}<br>%{value:,}",
                hovertemplate="<b>%{label}</b><br>%{value:,} votes<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        title=dict(
            text="The Purity Cycle — 2023 tight margin (statewide)",
            font=dict(family="Goldman", size=16, color=GOLD),
        ),
        paper_bgcolor=NAVY_DEEP,
        plot_bgcolor=NAVY_DEEP,
        font=dict(family="Goldman", color=GOLD),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.12, x=0.5, xanchor="center"),
        height=400,
        margin=dict(t=48, b=48, l=24, r=24),
    )
    return fig


def _micro_strike_map() -> go.Figure:
    df = pd.DataFrame(
        LGA_ROWS,
        columns=["LGA", "lat", "lon", "ballot_boxes", "nodal"],
    )
    texts = [
        (
            f"<b>{row.LGA}</b><br>Golden Coordinates: {row.lat:.4f}°N, {row.lon:.4f}°E<br>"
            f"Nodal Strength: {row.nodal}/25 Ballot Box targets<br>"
            f"Ballot boxes (ward density): {row.ballot_boxes}"
        )
        for _, row in df.iterrows()
    ]
    fig = go.Figure(
        go.Scattergeo(
            lat=df["lat"],
            lon=df["lon"],
            mode="markers",
            text=texts,
            hoverinfo="text",
            marker=dict(
                size=11,
                color=GOLD,
                line=dict(width=1, color=CYAN),
            ),
            name="Kaduna LGAs",
        )
    )
    fig.update_geos(
        scope="africa",
        projection_type="natural earth",
        showcountries=True,
        countrycolor=GOLD,
        bgcolor=NAVY_DEEP,
        landcolor="#0a0a22",
        coastlinecolor=CYAN,
        showocean=True,
        oceancolor="#000022",
        lataxis_range=[8.5, 13.2],
        lonaxis_range=[2.8, 14.2],
        resolution=50,
    )
    fig.update_layout(
        title=dict(
            text="Micro-Strike Map — Nigeria viewport · Golden Coordinates · Kaduna 23 LGAs",
            font=dict(family="Goldman", size=15, color=GOLD),
        ),
        paper_bgcolor=NAVY_DEEP,
        font=dict(family="Goldman", color=GOLD),
        height=520,
        margin=dict(l=0, r=0, t=48, b=0),
    )
    return fig


def _render_zone_detail(zone_key: str) -> None:
    st.markdown('<div class="prism-widget"><div class="prism-widget-inner">', unsafe_allow_html=True)
    if zone_key == "Master Aggregate":
        b2023 = {"APC": V_2023_APC, "PDP": V_2023_PDP, "LP": V_2023_LP}
        b27 = MASTER_2027
        st.subheader("Master Aggregate — statewide")
    else:
        b2023 = ZONES[zone_key]
        b27 = _zone_2027_projection(b2023)
        st.subheader(html.escape(zone_key))
    st.caption(
        f"2027 projections use 1.5M voter-database density factor ({DENSITY_FACTOR:.4f}×) "
        "plus party-specific 15/15 model adjustment."
    )
    c1, c2, c3 = st.columns(3)
    parties = ["APC", "PDP", "LP"]
    colors = [GOLD, CYAN, "#aab"]
    for col, party, colr in zip((c1, c2, c3), parties, colors):
        with col:
            st.metric(
                label=f"2023 {party}",
                value=f"{b2023[party]:,}",
                delta=f"2027 proj: {b27[party]:,}",
                delta_color="normal",
            )
            st.markdown(f"<div style='color:{colr};font-size:0.75rem'>Baseline vs projection</div>", unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)


def main() -> None:
    st.set_page_config(
        page_title="CIEN Kaduna 2027 · GCSLC",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)

    # Sidebar strike
    with st.sidebar:
        st.markdown("### Sidebar Strike")
        st.markdown(
            f'<div class="sidebar-pool">{DENSITY_DB:,}</div>',
            unsafe_allow_html=True,
        )
        st.caption("Voter Pool (pulsing)")
        st.markdown(
            '<div class="sidebar-handshake">'
            "<b>Outreach Pulse</b><br>"
            "Executive-Load-142 handshake (field video): synchronized leadership load-in at "
            "nodal hubs — confirms ward captains, data uplink, and ballot-box target packs before "
            "each mobilization wave."
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="prism-widget"><div class="prism-widget-inner">'
        '<div class="cien-identity-stack">'
        f'<p class="cien-title">{html.escape(ORG_NAME)}</p>'
        f'<p class="cien-motto">{html.escape(MOTTO)}</p>'
        '<p class="cien-foundation">Foundational logic · '
        '<span class="cien-8r">8R Stealth Paradigm</span></p>'
        "</div></div></div>",
        unsafe_allow_html=True,
    )

    row1_c1, row1_c2 = st.columns([1.15, 1.0])
    with row1_c1:
        st.markdown('<div class="section-prism"><h3>TOP-LEVEL SOVEREIGNTY</h3></div>', unsafe_allow_html=True)
        st.plotly_chart(_donut_purity(), use_container_width=True)
    with row1_c2:
        st.markdown('<div class="section-prism"><h3>THE 2/3RDS TRACKER</h3></div>', unsafe_allow_html=True)
        st.markdown(
            f"""
<div class="twothirds-wrap">
  <div class="twothirds-label">
    <span>LGA majority path</span>
    <span>{LGA_MAJORITY_NEED} / {LGA_TARGET} LGAs</span>
  </div>
  <div class="twothirds-track"><div class="twothirds-fill"></div></div>
  <p style="color:#00E5FF;font-size:0.78rem;margin:0.45rem 0 0 0;font-family:Goldman,sans-serif;">
    Progress toward securing {LGA_MAJORITY_NEED} of {LGA_TARGET} LGAs (two-thirds constitutional rhythm).
  </p>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-prism"><h3>SENATORIAL COMMAND GRID</h3></div>',
        unsafe_allow_html=True,
    )
    gz1, gz2, gz3, gz4 = st.columns(4)
    zones_order = [
        "Zone 1: Central",
        "Zone 2: North",
        "Zone 3: South",
        "Master Aggregate",
    ]
    zone_cols = (gz1, gz2, gz3, gz4)
    for i, zk in enumerate(zones_order):
        with zone_cols[i]:
            st.markdown('<div class="zone-prism-btn">', unsafe_allow_html=True)
            label = zk if zk == "Master Aggregate" else zk.replace(": ", ":\n")
            if st.button(label, key=f"zone_btn_{i}", use_container_width=True):
                st.session_state["cien_zone"] = zk
            st.markdown("</div>", unsafe_allow_html=True)

    if "cien_zone" not in st.session_state:
        st.session_state["cien_zone"] = "Master Aggregate"
    _render_zone_detail(st.session_state["cien_zone"])

    st.markdown(
        '<div class="section-prism"><h3>MICRO-STRIKE MAP</h3></div>',
        unsafe_allow_html=True,
    )
    map_df = pd.DataFrame(
        LGA_ROWS,
        columns=["LGA", "lat", "lon", "ballot_boxes", "nodal"],
    )
    map_fig = _micro_strike_map()
    map_event = st.plotly_chart(
        map_fig,
        use_container_width=True,
        on_select="rerun",
        selection_mode="points",
    )
    if map_event and map_event.get("selection", {}).get("points"):
        pidx = map_event["selection"]["points"][0]["point_index"]
        r = map_df.iloc[pidx]
        st.success(
            f"{r['LGA']} — Nodal Strength: {int(r['nodal'])}/25 Ballot Box targets · "
            f"Coordinates {r['lat']:.4f}°N, {r['lon']:.4f}°E · Ballot boxes: {int(r['ballot_boxes'])}"
        )
    else:
        st.caption("Click an LGA marker for nodal strength and golden coordinates.")

    st.markdown(
        '<div class="section-prism"><h3>THE 8R PARADIGM PANEL</h3></div>',
        unsafe_allow_html=True,
    )
    if "cien_d" not in st.session_state:
        st.session_state["cien_d"] = None

    dcols = st.columns(4)
    for i, (code, body) in enumerate(DETERMINANTS.items()):
        with dcols[i % 4]:
            st.markdown('<div class="d8-box"><div class="d8-inner">', unsafe_allow_html=True)
            if st.button(code, key=f"det_{code}", use_container_width=True):
                st.session_state["cien_d"] = code
            st.markdown("</div></div>", unsafe_allow_html=True)

    sel = st.session_state["cien_d"]
    if sel:
        st.markdown(
            f'<div class="det-modal"><h4>{html.escape(sel)} — Determinant</h4>'
            f"<p>{html.escape(DETERMINANTS[sel])}</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Dismiss determinant", key="dismiss_det"):
            st.session_state["cien_d"] = None
            st.rerun()

    st.caption(
        f"CIEN Kaduna 2027 · 8R Stealth Paradigm (foundational logic) · "
        f"port {os.environ.get('STREAMLIT_SERVER_PORT', '9099')} · "
        "Scientific model narrative for strategic planning only."
    )


if __name__ == "__main__":
    main()
