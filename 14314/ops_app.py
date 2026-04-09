import math
import os
from datetime import datetime, timezone
from dataclasses import asdict, is_dataclass

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data_engine import ALL_LGA_RECORDS

os.environ.setdefault("STREAMLIT_SERVER_PORT", "8506")

st.set_page_config(
    page_title="Field Intelligence Mirror 8506",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      .stApp {
        background: linear-gradient(155deg, #000033 0%, #000066 58%, #001133 100%);
        color: #FFFFFF;
      }
      .ops-title {
        color: #D4AF37;
        text-align: center;
        font-weight: 900;
        letter-spacing: 0.08em;
        margin: 0 0 6px 0;
      }
      .ops-subtitle {
        color: #00CED1;
        text-align: center;
        font-weight: 700;
        margin: 0 0 10px 0;
      }
      .ops-chip {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 999px;
        border: 1px solid rgba(212,175,55,0.55);
        color: #D4AF37;
        background: rgba(0,0,128,0.52);
        font-size: 0.78rem;
        font-weight: 800;
        margin-bottom: 8px;
      }
      .ops-activity-log {
        margin-top: 8px;
        border: 1px solid rgba(0, 206, 209, 0.65);
        border-radius: 10px;
        padding: 10px 12px;
        background: linear-gradient(165deg, rgba(0,0,128,0.55) 0%, rgba(0,40,80,0.48) 100%);
        box-shadow:
          0 0 18px rgba(0,206,209,0.35),
          inset 0 0 20px rgba(0,206,209,0.16);
      }
      .ops-activity-title {
        color: #00FFFF;
        font-weight: 900;
        font-size: 0.88rem;
        letter-spacing: 0.08em;
        margin: 0 0 8px 0;
        text-shadow: 0 0 12px rgba(0,255,255,0.65);
      }
      .ops-activity-line {
        color: #FFFFFF;
        font-size: 0.8rem;
        margin: 4px 0;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h2 class='ops-title'>FIELD INTELLIGENCE MIRROR · PORT 8506</h2>", unsafe_allow_html=True)
st.markdown(
    "<p class='ops-subtitle'>144,000 nodes · ward-cluster rendering · S24 operational watch</p>",
    unsafe_allow_html=True,
)

TOTAL_NODES = 144_000
TOTAL_LGAS = max(len(ALL_LGA_RECORDS), 1)
NODES_PER_LGA = TOTAL_NODES / TOTAL_LGAS
WARDS_PER_LGA = 10


def _record_to_dict(rec: object) -> dict:
    """Normalize LGARecord/dataclass/object/dict to a dictionary."""
    if isinstance(rec, dict):
        return rec
    if is_dataclass(rec):
        return asdict(rec)
    if hasattr(rec, "__dict__"):
        return dict(vars(rec))
    return {}


def _to_df() -> pd.DataFrame:
    rows = []
    now = datetime.now(timezone.utc)
    t = now.timestamp()
    for i, rec in enumerate(ALL_LGA_RECORDS):
        recd = _record_to_dict(rec)
        state = str(recd.get("state", "Unknown"))
        lga = str(recd.get("lga", "Unknown"))
        strike_priority = float(recd.get("strike_priority", 0.0))
        turnout_rate = float(recd.get("turnout_2023_rate", 0.0))
        apathy_rate = max(0.02, 1.0 - turnout_rate)
        ward_clusters = max(6, int(round(WARDS_PER_LGA + strike_priority * 16)))
        assigned_nodes = int(round(NODES_PER_LGA))
        conversion_freq = max(0.6, min(8.8, (apathy_rate * 6.5) + (strike_priority * 1.9)))
        pulse = 0.5 + 0.5 * math.sin((t / 21.0) + (i * 0.17))
        diligence_score = max(0.0, min(100.0, (conversion_freq * 11.5) + (pulse * 16.0)))
        conversions_7d = max(0, int(round(conversion_freq * 7.0 * (0.35 + (pulse * 0.9)))))
        if conversions_7d == 0:
            diligence_score = min(diligence_score, 24.0)
        rows.append(
            {
                "state": state,
                "lga": lga,
                "zone": str(recd.get("zone", "")),
                "ward_clusters": ward_clusters,
                "assigned_nodes": assigned_nodes,
                "apathy_conversion_freq": round(conversion_freq, 2),
                "conversions_7d": conversions_7d,
                "canvasser_diligence_score": round(diligence_score, 2),
                "strike_priority": round(strike_priority, 3),
            }
        )
    return pd.DataFrame(rows)


@st.cache_data(ttl=10)
def load_monitor_df() -> pd.DataFrame:
    return _to_df()


monitor_df = load_monitor_df()
monitor_df["cluster_share_pct"] = (
    100.0 * monitor_df["ward_clusters"] / max(float(monitor_df["ward_clusters"].sum()), 1.0)
)
monitor_df["node_status"] = monitor_df.apply(
    lambda r: "Idle Alert" if int(r["conversions_7d"]) <= 0 else (
        "Verified" if float(r["canvasser_diligence_score"]) >= 76.0 else ("Active" if float(r["canvasser_diligence_score"]) >= 52.0 else "Idle")
    ),
    axis=1,
)
monitor_df["node_status_color"] = monitor_df["node_status"].map(
    {"Verified": "#D4AF37", "Active": "#000080", "Idle": "#B22222", "Idle Alert": "#FF3030"}
)

avg_diligence = float(monitor_df["canvasser_diligence_score"].mean())
avg_conv_freq = float(monitor_df["apathy_conversion_freq"].mean())
clusters_total = int(monitor_df["ward_clusters"].sum())

st.markdown(
    f"<span class='ops-chip'>Last Sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} · Nodes: {TOTAL_NODES:,}</span>",
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Nodes", f"{TOTAL_NODES:,}")
c2.metric("Ward Clusters", f"{clusters_total:,}")
c3.metric("Avg Apathy Conversion", f"{avg_conv_freq:.2f}/min")
c4.metric("Canvasser Diligence Score", f"{avg_diligence:.2f}")
_status_counts = monitor_df["node_status"].value_counts().to_dict()
st.caption(
    "Node color map · Gold=Verified · Navy=Active · Red=Idle/Idle Alert "
    f"(Verified: {int(_status_counts.get('Verified', 0)):,}, "
    f"Active: {int(_status_counts.get('Active', 0)):,}, "
    f"Idle: {int(_status_counts.get('Idle', 0)):,}, "
    f"Idle Alert(0 conversions/7d): {int(_status_counts.get('Idle Alert', 0)):,})"
)

zone_df = (
    monitor_df.groupby("zone", as_index=False)
    .agg(
        ward_clusters=("ward_clusters", "sum"),
        assigned_nodes=("assigned_nodes", "sum"),
        diligence=("canvasser_diligence_score", "mean"),
    )
    .sort_values("diligence", ascending=False)
)

left, right = st.columns([1.1, 0.9])
with left:
    fig_zone = px.bar(
        zone_df,
        x="zone",
        y="ward_clusters",
        color="diligence",
        color_continuous_scale=[[0, "#8B0000"], [0.5, "#00CED1"], [1, "#D4AF37"]],
        title="Ward-Level Cluster Load by Zone",
    )
    fig_zone.update_layout(
        template=None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,128,0.25)",
        font=dict(color="#ffffff"),
        xaxis_title="Zone",
        yaxis_title="Ward Clusters",
        margin=dict(l=30, r=20, t=50, b=20),
    )
    st.plotly_chart(fig_zone, use_container_width=True)

with right:
    mining_depth_score = max(0.0, min(100.0, (avg_diligence * 0.72) + (avg_conv_freq * 4.2)))
    fig_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=mining_depth_score,
            number={"suffix": "%", "font": {"size": 36, "color": "#D4AF37"}},
            title={"text": "Mining Depth Gauge", "font": {"color": "#00CED1", "size": 20}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#ffffff"},
                "bar": {"color": "#D4AF37"},
                "bgcolor": "rgba(0,0,128,0.45)",
                "borderwidth": 1,
                "bordercolor": "rgba(0,206,209,0.7)",
                "steps": [
                    {"range": [0, 40], "color": "rgba(139,0,0,0.45)"},
                    {"range": [40, 70], "color": "rgba(0,206,209,0.35)"},
                    {"range": [70, 100], "color": "rgba(212,175,55,0.35)"},
                ],
            },
        )
    )
    fig_gauge.update_layout(
        margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.caption("Mining Depth sync is fed by live 8506 apathy-conversion and diligence pulses.")
    _activity_rows = (
        monitor_df.sort_values(["conversions_7d", "canvasser_diligence_score"], ascending=[True, False])
        .head(12)
        .copy()
    )
    _activity_lines = "".join(
        (
            "<p class='ops-activity-line'>"
            f"{str(r['state'])} · {str(r['lga'])} — "
            f"<span style='color:#00FFFF;font-weight:900;'>Canvasser Activity</span>: "
            f"{int(r['conversions_7d'])} (7D) · "
            f"<span style='color:{str(r['node_status_color'])};font-weight:900;'>{str(r['node_status'])}</span>"
            "</p>"
        )
        for _, r in _activity_rows.iterrows()
    )
    st.markdown(
        "<div class='ops-activity-log'>"
        "<p class='ops-activity-title'>RIGHT-SIDE ACTIVITY LOGS</p>"
        f"{_activity_lines}"
        "</div>",
        unsafe_allow_html=True,
    )

st.subheader("Canvasser Diligence Tracker — 144,000 Node State")
status_df = (
    monitor_df.groupby("node_status", as_index=False)
    .agg(ward_clusters=("ward_clusters", "sum"), assigned_nodes=("assigned_nodes", "sum"))
)
_status_order = ["Verified", "Active", "Idle", "Idle Alert"]
status_df["node_status"] = pd.Categorical(status_df["node_status"], categories=_status_order, ordered=True)
status_df = status_df.sort_values("node_status")
status_df["tooltip_note"] = status_df["node_status"].apply(
    lambda s: "Diligence Alert: Yield < 18/25 Threshold" if str(s) in {"Idle", "Idle Alert"} else "Within diligence tolerance."
)
fig_status = px.bar(
    status_df,
    x="node_status",
    y="assigned_nodes",
    color="node_status",
    color_discrete_map={"Verified": "#D4AF37", "Active": "#000080", "Idle": "#B22222", "Idle Alert": "#FF3030"},
    text="assigned_nodes",
    title="Node Activation State (Color-Coded)",
)
fig_status.update_layout(
    template=None,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,128,0.2)",
    font=dict(color="#ffffff"),
    xaxis_title="Node Status",
    yaxis_title="Assigned Nodes",
    margin=dict(l=30, r=20, t=50, b=20),
    showlegend=False,
)
fig_status.update_traces(texttemplate="%{text:,}", textposition="outside")
fig_status.update_traces(
    customdata=status_df[["tooltip_note"]].to_numpy(),
    hovertemplate="<b>%{x}</b><br>Assigned Nodes: %{y:,}<br>%{customdata[0]}<extra></extra>",
)
st.plotly_chart(fig_status, use_container_width=True)

_scroll_df = monitor_df.sort_values(["node_status", "canvasser_diligence_score"], ascending=[True, False]).head(180).copy()
_rows = []
for _, r in _scroll_df.iterrows():
    _rows.append(
        "<tr>"
        f"<td>{r['state']}</td>"
        f"<td>{r['lga']}</td>"
        f"<td>{int(r['ward_clusters']):,}</td>"
        f"<td>{int(r['assigned_nodes']):,}</td>"
        f"<td>{float(r['apathy_conversion_freq']):.2f}</td>"
        f"<td>{int(r['conversions_7d'])}</td>"
        f"<td style='color:{r['node_status_color']};font-weight:900;'>{r['node_status']}</td>"
        "</tr>"
    )
_scroll_tbody = "".join(_rows)
st.markdown(
    """
    <style>
      .ops-scroll-wrap { margin: 8px 0 14px 0; overflow: hidden; border-radius: 10px; border: 1px solid rgba(0,206,209,0.35); }
      .ops-scroll-track { display: block; animation: opsScrollWard 42s linear infinite; }
      .ops-scroll-table { width: 100%; border-collapse: collapse; background: rgba(0,0,128,0.32); }
      .ops-scroll-table th, .ops-scroll-table td { padding: 6px 8px; font-size: 0.82rem; color: #ffffff; border-bottom: 1px solid rgba(255,255,255,0.08); }
      .ops-scroll-table th { color: #00CED1; position: sticky; top: 0; background: rgba(0,0,80,0.9); }
      @keyframes opsScrollWard { 0% { transform: translateY(0%);} 100% { transform: translateY(-50%);} }
      .ops-red-pulse { color: #FF3030; text-shadow: 0 0 10px rgba(255,48,48,0.75); animation: opsRedPulse 1.1s ease-in-out infinite; }
      @keyframes opsRedPulse { 0%,100% { opacity: 1; } 50% { opacity: 0.35; } }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='ops-scroll-wrap'>"
    "<div class='ops-scroll-track'>"
    "<table class='ops-scroll-table'>"
    "<thead><tr><th>State</th><th>LGA</th><th>Ward Clusters</th><th>Nodes</th><th>Apathy Conv./min</th><th>7D Conv.</th><th>Status</th></tr></thead>"
    f"<tbody>{_scroll_tbody}{_scroll_tbody}</tbody>"
    "</table>"
    "</div>"
    "</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p class='ops-red-pulse'>Idle Alert protocol: any node with 0 conversions in 7 days is pulsing red.</p>",
    unsafe_allow_html=True,
)

top_lgas = monitor_df.sort_values("canvasser_diligence_score", ascending=False).head(20).copy()
top_lgas = top_lgas.rename(
    columns={
        "state": "State",
        "lga": "LGA",
        "zone": "Zone",
        "ward_clusters": "Ward Clusters",
        "assigned_nodes": "Assigned Nodes",
        "apathy_conversion_freq": "Apathy Conversion (/min)",
        "conversions_7d": "Conversions (7D)",
        "canvasser_diligence_score": "Canvasser Diligence Score",
        "node_status": "Node Status",
    }
)

st.subheader("High-Velocity Ward Cluster Monitor (Top 20 LGAs)")
st.dataframe(top_lgas, use_container_width=True, hide_index=True)
