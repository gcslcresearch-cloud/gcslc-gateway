from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

from Part_01_Telecom.shard_index import KadunaContactShardIndex
from Part_02_Finance.sovereign_yield import debt_erasure_projection, sovereign_yield_for_state
from Part_03_Security.build_quad_pillar_reality import ZARIA_ANCHOR, buildQuadPillarReality
from Part_03_Security.risk_engine import correlate_blackout_vandalism_risk
from Part_04_Social.distance_to_service import nearest_service

NAVY_DEEP = "#000B2D"
NAVY = "#001F3F"
EGGSHELL = "#F8F6EC"
GOLD = "#D4AF37"
CYAN = "#00FFFF"

BASE_DIR = Path(__file__).resolve().parent
P1_DATA = BASE_DIR / "Part_01_Telecom" / "data"
P2_DATA = BASE_DIR / "Part_02_Finance" / "data"
P3_DATA = BASE_DIR / "Part_03_Security" / "data"
P4_DATA = BASE_DIR / "Part_04_Social" / "data"

st.set_page_config(page_title="Sovereign Eagle Mirror 2026", layout="wide")

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap');
html, body, .stApp {{
  background: #001f3f !important;
  color: {EGGSHELL} !important;
  font-family: 'Goldman', sans-serif !important;
}}
[data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stMain"] {{
  background: #001f3f !important;
  font-family: 'Goldman', sans-serif !important;
}}
* {{
  font-family: 'Goldman', sans-serif !important;
}}
h1, h2, h3, h4, h5, p, span, label, div {{
  color: {CYAN} !important;
}}
.sovereign-subline {{
  color: unset !important;
}}
.quad-row {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-top: 4px;
  margin-bottom: 12px;
}}
.quad-chip {{
  border: 1px solid rgba(212, 175, 55, 0.9);
  border-radius: 10px;
  text-align: center;
  padding: 0.45rem;
  color: {GOLD};
  font-weight: 700;
  letter-spacing: 0.08em;
  animation: pulse 1.8s infinite ease-in-out;
}}
@keyframes pulse {{
  0% {{ box-shadow: 0 0 4px rgba(212, 175, 55, 0.2); }}
  50% {{ box-shadow: 0 0 16px rgba(212, 175, 55, 0.7); }}
  100% {{ box-shadow: 0 0 4px rgba(212, 175, 55, 0.2); }}
}}
.sovereign-head-wrap {{
  margin: 0.3rem 0 0.65rem;
  border-bottom: 1px solid rgba(212, 175, 55, 0.45);
  padding-bottom: 0.5rem;
}}
.sovereign-typewriter {{
  display: inline-block;
  font-family: 'Goldman', sans-serif;
  font-size: clamp(0.9rem, 1.9vw, 1.3rem);
  letter-spacing: 0.05em;
  font-weight: 700;
  background: linear-gradient(90deg, #ffffff 0%, {GOLD} 35%, #fff8d6 50%, {GOLD} 65%, #ffffff 100%);
  background-size: 250% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shimmer 8s linear infinite;
}}
.gcslc-legal-name-shimmer {{
  background: linear-gradient(90deg, #001f3f, {GOLD}, #fff8d6, {GOLD}, #001f3f);
  background-size: 220% auto;
  -webkit-background-clip: text;
  background-clip: text;
  color: {GOLD} !important;
  animation: shimmer 7s linear infinite;
}}
.sovereign-subline {{
  margin-top: 0.35rem;
  font-family: 'Goldman', sans-serif;
  font-size: clamp(0.68rem, 1.2vw, 0.9rem);
  letter-spacing: 0.08em;
  background: linear-gradient(90deg, #ffffff, {GOLD}, #ffffff);
  background-size: 220% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shimmer 6s linear infinite;
}}
@keyframes shimmer {{
  0% {{ background-position: 0% center; }}
  100% {{ background-position: 200% center; }}
}}
.status-ticker {{
  overflow: hidden;
  border-top: 1px solid rgba(212,175,55,.4);
  border-bottom: 1px solid rgba(212,175,55,.4);
  margin: 0.4rem 0 0.7rem;
  background: rgba(0,0,0,.15);
  white-space: nowrap;
}}
.status-track {{
  display: inline-block;
  padding: 0.35rem 0;
  color: {GOLD};
  letter-spacing: .08em;
  animation: status-scroll 28s linear infinite;
}}
@keyframes status-scroll {{
  from {{ transform: translateX(100%); }}
  to {{ transform: translateX(-100%); }}
}}
[data-testid="stDataFrame"] {{
  background: rgba(0, 0, 128, 0.85) !important;
  border: 1px solid {GOLD} !important;
  border-radius: 10px !important;
  padding: 0.35rem !important;
}}
[data-testid="stDataFrame"] * {{
  color: {EGGSHELL} !important;
  font-family: 'Goldman', sans-serif !important;
}}
[data-testid="stMetric"] {{
  border: 1px solid rgba(212, 175, 55, 0.65);
  border-radius: 8px;
  padding: 0.25rem 0.5rem;
  background: rgba(0, 0, 90, 0.65);
}}
[data-testid="stMetric"] label, [data-testid="stMetric"] div {{
  color: {GOLD} !important;
}}
[data-testid="stButton"] button {{
  background: rgba(0, 0, 90, 0.95) !important;
  color: {GOLD} !important;
  border: 1px solid {GOLD} !important;
}}
.glass-map-frame {{
  border: 1px solid {GOLD};
  border-radius: 14px;
  background: rgba(0, 26, 51, 0.15);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.08), 0 18px 40px rgba(0, 0, 0, 0.35), inset 0 0 0 1px rgba(212, 175, 55, 0.25);
  padding: 0.45rem;
  margin-top: 0.4rem;
}}
[data-testid="stPlotlyChart"] {{
  border-radius: 12px;
  overflow: hidden;
}}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="sovereign-head-wrap">
      <div class="sovereign-typewriter gcslc-legal-name-shimmer">
        Galadiman Ruwa Center for Strategic Leadership and Communication GCSLC LTD/GTE
      </div>
      <div class="sovereign-subline">Galadiman Ruwa Nigeria Ltd RC 1871418</div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption("Phase-1 Strike: Real-World Ingestion handshake across COMM, FIN, SEC, SOC.")
st.markdown(
    """
    <div class="status-ticker">
      <div class="status-track">
      [AUDITING 13-STATE ENERGY NODES] ... [CALCULATING COAL-TO-SILICON CONVERSION] ... [SOVEREIGN WEALTH POTENTIAL ACTIVE] ...
      [AUDITING 13-STATE ENERGY NODES] ... [CALCULATING COAL-TO-SILICON CONVERSION] ... [SOVEREIGN WEALTH POTENTIAL ACTIVE] ...
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

components.html(
    f"""
    <style>
      .clock-grid {{
        background:#001f3f;
        display:grid;
        grid-template-columns:repeat(6,minmax(110px,1fr));
        gap:8px;
        padding:4px 2px 10px;
      }}
      .clock-card {{
        border:1px solid rgba(212,175,55,.45);
        border-radius:8px;
        background:rgba(248,246,236,.1);
        text-align:center;
        padding:6px 4px;
        color:{EGGSHELL};
        font-family:'Goldman',sans-serif;
      }}
      .clock-label {{
        font-size:11px;
        letter-spacing:.08em;
        color:{GOLD};
        margin-bottom:3px;
      }}
      .dial {{
        width:74px;height:74px;margin:0 auto;position:relative;
        border-radius:50%;
        background:{EGGSHELL};
        border:2px solid {GOLD};
        box-shadow: inset 0 0 0 1px rgba(0,0,0,.1);
      }}
      .hand {{ position:absolute; left:50%; bottom:50%; transform-origin:bottom center; border-radius:3px; }}
      .h {{ width:3px;height:18px;background:#262626; }}
      .m {{ width:2px;height:26px;background:#3e3e3e; }}
      .s {{ width:1.5px;height:30px;background:#B22222; }}
      .pin {{ position:absolute;left:50%;top:50%; width:6px;height:6px; transform:translate(-50%,-50%); border-radius:50%; background:{GOLD}; }}
    </style>
    <div class="clock-grid" id="clock-grid"></div>
    <script>
      const zones = [
        ["Abuja", "Africa/Lagos"],
        ["London", "Europe/London"],
        ["Dubai", "Asia/Dubai"],
        ["New York", "America/New_York"],
        ["Beijing", "Asia/Shanghai"],
        ["Geneva", "Europe/Zurich"],
      ];
      const grid = document.getElementById("clock-grid");
      zones.forEach((z, i) => {{
        const card = document.createElement("div");
        card.className = "clock-card";
        card.innerHTML = `<div class="clock-label">${{z[0]}}</div>
          <div class="dial">
            <div class="hand h" id="h-${{i}}"></div>
            <div class="hand m" id="m-${{i}}"></div>
            <div class="hand s" id="s-${{i}}"></div>
            <div class="pin"></div>
          </div>`;
        grid.appendChild(card);
      }});
      function tick() {{
        zones.forEach((z, i) => {{
          const now = new Date(new Date().toLocaleString("en-US", {{ timeZone: z[1] }}));
          const sec = now.getSeconds();
          const min = now.getMinutes();
          const hour = now.getHours() % 12;
          const sDeg = sec * 6;
          const mDeg = min * 6 + sec * 0.1;
          const hDeg = hour * 30 + min * 0.5;
          document.getElementById(`s-${{i}}`).style.transform = `translateX(-50%) rotate(${{sDeg}}deg)`;
          document.getElementById(`m-${{i}}`).style.transform = `translateX(-50%) rotate(${{mDeg}}deg)`;
          document.getElementById(`h-${{i}}`).style.transform = `translateX(-50%) rotate(${{hDeg}}deg)`;
        }});
      }}
      tick();
      setInterval(tick, 1000);
    </script>
    """,
    height=130,
)

with (P1_DATA / "signal_blackouts.json").open("r", encoding="utf-8") as f:
    blackout_events = json.load(f)["events"]
with (P2_DATA / "binji_jega_pos_registry.json").open("r", encoding="utf-8") as f:
    pos_registry = json.load(f)["registry"]
with (P2_DATA / "coal_reserve_nodes.json").open("r", encoding="utf-8") as f:
    coal_nodes = json.load(f)["nodes"]
with (P3_DATA / "northern_pulse_markets.json").open("r", encoding="utf-8") as f:
    northern_pulse = json.load(f)["markets"]
with (P3_DATA / "vandalism_incidents.json").open("r", encoding="utf-8") as f:
    vandalism_incidents = json.load(f)["incidents"]
with (P4_DATA / "service_infrastructure.json").open("r", encoding="utf-8") as f:
    facilities = json.load(f)["facilities"]
with (P4_DATA / "human_residence_nodes.json").open("r", encoding="utf-8") as f:
    villages = json.load(f)["villages"]


if "active_sync" not in st.session_state:
    st.session_state.active_sync = "COMM"

q1, q2, q3, q4 = st.columns(4)
with q1:
    if st.button("COMM-SYNC", use_container_width=True):
        st.session_state.active_sync = "COMM"
with q2:
    if st.button("FIN-SYNC", use_container_width=True):
        st.session_state.active_sync = "FIN"
with q3:
    if st.button("SEC-SYNC", use_container_width=True):
        st.session_state.active_sync = "SEC"
with q4:
    if st.button("SOC-SYNC", use_container_width=True):
        st.session_state.active_sync = "SOC"

st.markdown(
    '<div class="quad-row"><div class="quad-chip">COMM</div><div class="quad-chip">FIN</div>'
    '<div class="quad-chip">SEC</div><div class="quad-chip">SOC</div></div>',
    unsafe_allow_html=True,
)
st.info(f"Data Handshake Active: `{st.session_state.active_sync}`")
global_demand = st.toggle("Global Demand Bridge", value=False)


@st.cache_resource
def build_contact_index_preview() -> dict:
    index = KadunaContactShardIndex()
    sample_rows = []
    lgas = ["Zaria", "Sabon Gari", "Igabi", "Kudan", "Soba", "Chikun"]
    for i in range(7000):
        sample_rows.append(
            {
                "contact_id": f"KD-{i:07d}",
                "phone_e164": f"+234810{i:07d}"[-14:],
                "ward_code": f"WD-{i % 412:03d}",
                "lga_code": lgas[i % len(lgas)],
            }
        )
    index.ingest_batch(sample_rows)
    return {"summary": index.summary(), "top_wards": index.top_wards(limit=8)}


index_preview = build_contact_index_preview()
quad = buildQuadPillarReality(
    ZARIA_ANCHOR["lat"],
    ZARIA_ANCHOR["lon"],
    blackout_events=blackout_events,
    vandalism_incidents=vandalism_incidents,
)
c1, c2 = st.columns(2)
with c1:
    st.subheader("Part_03_Security - Real Risk Quad")
    st.json(
        {
            "commHealth": quad["commHealth"],
            "financialDepth": quad["financialDepth"],
            "securityPresence": quad["securityPresence"],
            "socialResonance": quad["socialResonance"],
            "riskRaw": quad["raw"]["risk"],
        }
    )
with c2:
    st.subheader("Part_01_Telecom - Shard+Index Skeleton")
    st.json(index_preview["summary"])
    st.caption("Index preview is bounded to avoid browser lock; target capacity remains 2.0M.")

st.subheader("Part_04_Social - Northern Pulse Coordinates")
st.metric("Market Nodes Ingested", len(northern_pulse))
st.metric("Primary Anchor", f'{ZARIA_ANCHOR["lat"]}, {ZARIA_ANCHOR["lon"]}')

records = [nearest_service(v, facilities) for v in villages]
risk_rows = []
for village in villages:
    risk_rows.append(
        {
            "village": village["name"],
            **correlate_blackout_vandalism_risk(
                lat=village["lat"],
                lon=village["lon"],
                blackout_events=blackout_events,
                vandalism_incidents=vandalism_incidents,
            ),
        }
    )

distance_df = pd.DataFrame(records).sort_values("distance_km")
risk_df = pd.DataFrame(risk_rows).sort_values("risk_score", ascending=False)

yield_rows = [sovereign_yield_for_state(node["state"], node["reserves_mt"]) for node in coal_nodes]
debt_projection = debt_erasure_projection(yield_rows)

s1, s2 = st.columns(2)
with s1:
    st.subheader("Human Residence - Distance-to-Service")
    st.dataframe(distance_df, use_container_width=True, hide_index=True)
with s2:
    st.subheader("Lalata Correlation Risk Table")
    st.dataframe(risk_df, use_container_width=True, hide_index=True)
st.subheader("Part_02_Finance - Sovereign Debt Coupling")
fc1, fc2, fc3 = st.columns(3)
with fc1:
    st.metric("Debt Target", "N55T")
with fc2:
    st.metric("Projected Annual Yield", f"N{debt_projection['total_annual_value_naira']/1e12:.2f}T")
with fc3:
    st.metric("Debt Coverage", f"{debt_projection['debt_coverage_pct']}%")

map_fig = go.Figure()
map_fig.add_trace(
    go.Scattermap(
        lat=[ZARIA_ANCHOR["lat"]],
        lon=[ZARIA_ANCHOR["lon"]],
        mode="markers+text",
        text=["Zaria Anchor"],
        textposition="top center",
        marker=dict(size=24, color="rgba(212,175,55,0.24)"),
        name="Zaria Glow",
        hoverinfo="skip",
        showlegend=False,
    )
)
map_fig.add_trace(
    go.Scattermap(
        lat=[ZARIA_ANCHOR["lat"]],
        lon=[ZARIA_ANCHOR["lon"]],
        mode="markers+text",
        text=["Zaria Anchor"],
        textposition="top center",
        marker=dict(size=14, color=GOLD),
        name="Zaria Anchor",
    )
)
map_fig.add_trace(
    go.Scattermap(
        lat=[v["lat"] for v in villages],
        lon=[v["lon"] for v in villages],
        mode="markers+text",
        text=[v["name"] for v in villages],
        textposition="bottom center",
        marker=dict(size=20, color="rgba(0,255,255,0.18)"),
        name="Residence Glow",
        hoverinfo="skip",
        showlegend=False,
    )
)
map_fig.add_trace(
    go.Scattermap(
        lat=[v["lat"] for v in villages],
        lon=[v["lon"] for v in villages],
        mode="markers+text",
        text=[v["name"] for v in villages],
        textposition="bottom center",
        marker=dict(size=11, color="#00FFFF"),
        name="Human Residence Nodes",
    )
)
map_fig.add_trace(
    go.Scattermap(
        lat=[n["lat"] for n in coal_nodes],
        lon=[n["lon"] for n in coal_nodes],
        mode="markers+text",
        text=[f'⬢ {n["state"]}' for n in coal_nodes],
        textposition="top center",
        marker=dict(size=18, color=GOLD, symbol="hexagon"),
        name="13-State Coal Reserves",
        customdata=[[n["state"], n["reserves_mt"], "coal"] for n in coal_nodes],
        hovertemplate=(
            "<b>%{customdata[0]} Coal Node</b><br>"
            "Proven Reserve: %{customdata[1]} MT<br>"
            "Potential: 500MW Energy + Silicon Feedstock<br>"
            "Status: Moribund / Awaiting Resuscitation<extra></extra>"
        ),
    )
)
map_fig.add_trace(
    go.Scattermap(
        lat=[n["lat"] for n in coal_nodes],
        lon=[n["lon"] for n in coal_nodes],
        mode="markers",
        marker=dict(size=34, color="rgba(212,175,55,0.28)", symbol="hexagon"),
        name="Energy Pulse",
        hoverinfo="skip",
        showlegend=False,
    )
)
if global_demand:
    tech_hubs = [
        {"name": "Silicon Valley", "lat": 37.3875, "lon": -122.0575},
        {"name": "London", "lat": 51.5074, "lon": -0.1278},
        {"name": "Beijing", "lat": 39.9042, "lon": 116.4074},
    ]
    map_fig.add_trace(
        go.Scattermap(
            lat=[h["lat"] for h in tech_hubs],
            lon=[h["lon"] for h in tech_hubs],
            mode="markers+text",
            text=[h["name"] for h in tech_hubs],
            textposition="top center",
            marker=dict(size=12, color="#8D99AE"),
            name="Global Tech Hubs",
        )
    )
    for node in coal_nodes:
        for hub in tech_hubs:
            map_fig.add_trace(
                go.Scattermap(
                    lat=[node["lat"], hub["lat"]],
                    lon=[node["lon"], hub["lon"]],
                    mode="lines",
                    line=dict(width=1.2, color="rgba(212,175,55,0.8)"),
                    hoverinfo="skip",
                    showlegend=False,
                )
            )

active = st.session_state.active_sync
if active == "COMM":
    map_fig.add_trace(
        go.Scattermap(
            lat=[e["lat"] for e in blackout_events],
            lon=[e["lon"] for e in blackout_events],
            mode="markers+text",
            text=[e["site"] for e in blackout_events],
            textposition="top right",
            marker=dict(size=12, color="#A31621"),
            name="Signal Blackouts",
        )
    )
elif active == "FIN":
    # Required handshake: FIN-SYNC -> Binji/Jega POS Registry logic
    map_fig.add_trace(
        go.Scattermap(
            lat=[p["lat"] for p in pos_registry],
            lon=[p["lon"] for p in pos_registry],
            mode="markers+text",
            text=[f'{p["zone"]}: {p["agents"]} agents' for p in pos_registry],
            textposition="top right",
            marker=dict(size=13, color=GOLD),
            name="Binji/Jega POS Registry",
        )
    )
elif active == "SEC":
    map_fig.add_trace(
        go.Scattermap(
            lat=[i["lat"] for i in vandalism_incidents],
            lon=[i["lon"] for i in vandalism_incidents],
            mode="markers+text",
            text=[i["asset"] for i in vandalism_incidents],
            textposition="top right",
            marker=dict(size=13, color="#6A040F"),
            name="Vandalism Incidents",
        )
    )
    map_fig.add_trace(
        go.Scattermap(
            lat=[v["lat"] for v in villages],
            lon=[v["lon"] for v in villages],
            mode="markers",
            marker=dict(size=15, color="#9D0208"),
            name="Risk Probe Nodes",
            hovertext=[f'{r["village"]}: {r["risk_score"]} ({r["risk_tier"]})' for r in risk_rows],
            hoverinfo="text",
        )
    )
elif active == "SOC":
    map_fig.add_trace(
        go.Scattermap(
            lat=[v["lat"] for v in villages],
            lon=[v["lon"] for v in villages],
            mode="markers+text",
            text=[v["name"] for v in villages],
            textposition="bottom center",
            marker=dict(size=13, color=GOLD),
            name="Human Residence Nodes",
        )
    )
    for row in records:
        service = next(f for f in facilities if f["name"] == row["nearest_service"])
        map_fig.add_trace(
            go.Scattermap(
                lat=[row["lat"], service["lat"]],
                lon=[row["lon"], service["lon"]],
                mode="lines",
                line=dict(width=2.2, color="rgba(212, 175, 55, 0.9)"),
                hoverinfo="text",
                text=f'{row["village"]} -> {row["nearest_service"]} ({row["distance_km"]} km)',
                showlegend=False,
            )
        )

map_fig.update_layout(
    map=dict(
        style="carto-positron",
        center=dict(lat=ZARIA_ANCHOR["lat"], lon=ZARIA_ANCHOR["lon"]),
        zoom=3.1 if global_demand else 5.3,
        pitch=14,
        bearing=0,
    ),
    paper_bgcolor=EGGSHELL,
    plot_bgcolor=EGGSHELL,
    font=dict(color="#1D3557", family="Goldman, sans-serif"),
    margin=dict(l=0, r=0, t=0, b=0),
    height=560,
    uirevision="glass-core",
    legend=dict(
        bgcolor="rgba(255,255,255,0.65)",
        bordercolor=GOLD,
        borderwidth=1,
        font=dict(family="Goldman, sans-serif", color="#1D3557", size=11),
    ),
)
map_fig.update_traces(textfont=dict(family="Goldman, sans-serif", color="#1D3557", size=11))
st.subheader("Sovereign Map - White & Gold Skin")
components.html(
    f"""
    <style>
      .clock-inline{{display:grid;grid-template-columns:repeat(6,1fr);gap:6px;background:#001f3f;padding:2px 0 8px}}
      .clock-inline .u{{border:1px solid rgba(212,175,55,.45);border-radius:8px;background:rgba(248,246,236,.1);padding:4px;text-align:center;font-family:'Goldman',sans-serif;color:{EGGSHELL};font-size:11px}}
      .clock-inline .d{{width:58px;height:58px;margin:3px auto;position:relative;border-radius:50%;background:{EGGSHELL};border:2px solid {GOLD}}}
      .clock-inline .h,.clock-inline .m,.clock-inline .s{{position:absolute;left:50%;bottom:50%;transform-origin:bottom center}}
      .clock-inline .h{{height:14px;width:3px;background:#333}} .clock-inline .m{{height:20px;width:2px;background:#555}} .clock-inline .s{{height:24px;width:1px;background:#B22222}}
    </style>
    <div class="clock-inline" id="clock-inline"></div>
    <script>
      const z=[["Abuja","Africa/Lagos"],["London","Europe/London"],["Dubai","Asia/Dubai"],["New York","America/New_York"],["Beijing","Asia/Shanghai"],["Geneva","Europe/Zurich"]];
      const c=document.getElementById("clock-inline");
      z.forEach((x,i)=>{{const d=document.createElement("div");d.className="u";d.innerHTML=`${{x[0]}}<div class="d"><div class="h" id="ih-${{i}}"></div><div class="m" id="im-${{i}}"></div><div class="s" id="is-${{i}}"></div></div>`;c.appendChild(d);}});
      function t(){{z.forEach((x,i)=>{{const n=new Date(new Date().toLocaleString("en-US",{{timeZone:x[1]}}));const s=n.getSeconds(),m=n.getMinutes(),h=n.getHours()%12;document.getElementById(`is-${{i}}`).style.transform=`translateX(-50%) rotate(${{s*6}}deg)`;document.getElementById(`im-${{i}}`).style.transform=`translateX(-50%) rotate(${{m*6+s*0.1}}deg)`;document.getElementById(`ih-${{i}}`).style.transform=`translateX(-50%) rotate(${{h*30+m*0.5}}deg)`;}});}}
      t(); setInterval(t,1000);
    </script>
    """,
    height=105,
)
st.markdown('<div class="glass-map-frame">', unsafe_allow_html=True)
map_event = st.plotly_chart(
    map_fig,
    use_container_width=True,
    on_select="rerun",
    selection_mode="points",
    config={"scrollZoom": True, "displayModeBar": False},
)
st.markdown('</div>', unsafe_allow_html=True)
selected_points = map_event.get("selection", {}).get("points", []) if map_event else []
if selected_points:
    point = selected_points[0]
    cdata = point.get("customdata")
    if cdata and len(cdata) >= 3 and cdata[2] == "coal":
        state = cdata[0]
        reserve = cdata[1]
        st.success(
            f"{state} Sovereign Yield -> Potential: 500MW Energy + Silicon Feedstock. "
            f"Status: Moribund / Awaiting Resuscitation. Reserve: {reserve} MT."
        )
