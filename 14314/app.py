import pandas as pd
import plotly.express as px
import pytz
import streamlit as st
from datetime import datetime

from data_engine import ALL_LGA_RECORDS, STATE_COORDS, records_as_dicts

st.set_page_config(page_title="RHGI 774 Scientific Engine", layout="wide")

GOLD = "#FFD700"
NAVY = "#1A237E"
# Prism-Frame Navy (dashboard canvas + plot wells).
PRISM_NAVY = "#0b1024"
PRISM_NAVY_PLOT = "#0e1733"
# 20.7M national vote mandate anchor (fixed reference).
NATIONAL_VOTE_TARGET = 20_709_668


@st.cache_data(show_spinner=False)
def load_df() -> pd.DataFrame:
    df = pd.DataFrame(records_as_dicts(ALL_LGA_RECORDS))
    df["actual_2023"] = (
        df["apc_2023"] + df["pdp_2023"] + df["lp_2023"] + df["adc_2023"]
    )
    df["registered_voters"] = (
        df["actual_2023"] / df["turnout_2023_rate"].replace(0, 1e-9)
    ).round().astype(int)
    # Sovereign yield gap per LGA: (Registered × PVC rate) − 2023 actual votes.
    df["sovereign_yield_gap"] = (
        df["registered_voters"] * df["pvc_collection_rate"] - df["actual_2023"]
    )
    df["winner_2023"] = df[["apc_2023", "pdp_2023", "lp_2023", "adc_2023"]].max(axis=1)
    df["winner_2027"] = df[["apc_2027", "pdp_2027", "lp_2027", "adc_2027"]].max(axis=1)
    df["projected_total"] = df[["apc_2027", "pdp_2027", "lp_2027", "adc_2027"]].sum(axis=1)
    df["winning_margin"] = df["apc_2027"] - df[["pdp_2027", "lp_2027", "adc_2027"]].max(
        axis=1
    )
    df["apc_share_2027"] = (df["apc_2027"] / df["projected_total"].replace(0, 1)) * 100
    df["red_zone"] = df["canvasser_ratio"] < 16.0
    # Strike priority: high PVC + low 2023 turnout → high-priority strike zones.
    df["strike_priority"] = df["pvc_collection_rate"] * (1.0 - df["turnout_2023_rate"])
    return df


def apply_turnout_lift(df: pd.DataFrame, lift_pct: int) -> pd.DataFrame:
    """Scale 2027 vote totals by scientific turnout lift (1%–15%)."""
    m = 1.0 + float(lift_pct) / 100.0
    out = df.copy()
    for c in ["apc_2027", "pdp_2027", "lp_2027", "adc_2027"]:
        out[c] = (out[c] * m).round().astype(int)
    out["projected_total"] = out[["apc_2027", "pdp_2027", "lp_2027", "adc_2027"]].sum(
        axis=1
    )
    out["winning_margin"] = out["apc_2027"] - out[["pdp_2027", "lp_2027", "adc_2027"]].max(
        axis=1
    )
    out["apc_share_2027"] = (out["apc_2027"] / out["projected_total"].replace(0, 1)) * 100
    return out


def fct_apc_percent(dff: pd.DataFrame) -> float:
    m = dff["state"] == "FCT"
    if not m.any():
        return 0.0
    tot = dff.loc[m, "projected_total"].sum()
    if tot <= 0:
        return 0.0
    return 100.0 * dff.loc[m, "apc_2027"].sum() / tot


def constitutional_sentinel(dff: pd.DataFrame) -> tuple[int, bool, bool]:
    state_projection = (
        dff.groupby("state", as_index=False)[["apc_2027", "projected_total"]]
        .sum()
        .assign(
            apc_pct=lambda x: (x["apc_2027"] / x["projected_total"].replace(0, 1)) * 100
        )
    )
    states_25 = int((state_projection["apc_pct"] >= 25).sum())
    fct = state_projection.loc[state_projection["state"] == "FCT", "apc_pct"]
    fct_validated = bool(fct.ge(25).any()) if len(fct) else False
    constitutional_ok = states_25 >= 24 and fct_validated
    return states_25, fct_validated, constitutional_ok


def build_state_heatmap_df(dff: pd.DataFrame) -> pd.DataFrame:
    g = dff.groupby("state", as_index=False).agg(
        strike_priority=("strike_priority", "mean"),
        pvc_collection_rate=("pvc_collection_rate", "mean"),
        turnout_2023_rate=("turnout_2023_rate", "mean"),
    )
    g["lat"] = g["state"].map(lambda s: STATE_COORDS.get(s, (9.0, 8.0))[0])
    g["lon"] = g["state"].map(lambda s: STATE_COORDS.get(s, (9.0, 8.0))[1])
    return g


df = load_df()
sovereign_total = float(df["sovereign_yield_gap"].sum())

lagos_tz = pytz.timezone("Africa/Lagos")

st.markdown(
    """
    <style>
    .rhgi-kpi {padding: 10px 12px; border-radius: 10px; border:1px solid rgba(26,35,126,0.55); background:#0b1024;}
    .rhgi-pulse-red { animation: pulseRed 1s ease-in-out infinite; }
    @keyframes pulseRed {
      0%,100% { box-shadow: 0 0 0 rgba(255,0,0,0); }
      50% { box-shadow: 0 0 20px rgba(255,0,0,0.8); }
    }
    .rhgi-glow { color:#FFD700; text-shadow: 0 0 10px rgba(255,215,0,0.6); }
    .rhgi-gauge { font-size: 1.1rem; letter-spacing: 0.03em; }
    .rhgi-abuja-strobe {
      border: 2px solid rgba(220, 40, 40, 0.95) !important;
      animation: diamondStrobe 0.85s ease-in-out infinite;
    }
    @keyframes diamondStrobe {
      0%, 100% { box-shadow: 0 0 4px rgba(255, 0, 0, 0.35); }
      50% { box-shadow: 0 0 22px rgba(255, 0, 0, 0.95); }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Scientific controls")
    turnout_lift = st.slider(
        "Scientific turnout lift (%)",
        min_value=1,
        max_value=15,
        value=5,
        help="Increases projected 2027 vote totals across all parties proportionally.",
    )
    st.metric(
        "Sovereign Voter Yield",
        f"{sovereign_total:,.0f}",
        help="Σ over LGAs: (Registered Voters × PVC Collection Rate) − 2023 Actual Votes.",
    )
    st.caption("PVC & turnout rates are forensic anchors per LGA in data_engine.")
    projected_national = int(df[["apc_2027", "pdp_2027", "lp_2027", "adc_2027"]].sum().sum())
    st.metric(
        "National anchor (2027 base)",
        f"{NATIONAL_VOTE_TARGET:,}",
        delta=f"Base projection {projected_national:,}",
        help="Mandate reference total; live yield updates with turnout lift.",
    )

dff = apply_turnout_lift(df, turnout_lift)
states_25, fct_validated, constitutional_ok = constitutional_sentinel(dff)
fct_pct = fct_apc_percent(dff)
projected_yield = int(dff["projected_total"].sum())
remittance_gap = NATIONAL_VOTE_TARGET - projected_yield
abuja_strobe = fct_pct < 25.0
total_winning_margin = float(dff["winning_margin"].sum())

abuja_now = datetime.now(lagos_tz)

st.title("RHGI 774 Scientific Engine")
c1, c2, c3 = st.columns(3)
# Abuja Pulse lead (UTC+1); Diamond Strobe when FCT projected APC < 25%.
_pulse_cls = "rhgi-kpi rhgi-abuja-strobe" if abuja_strobe else "rhgi-kpi"
c1.markdown(
    f"<div class='{_pulse_cls}'><b>Abuja Pulse (UTC+1)</b><br><span class='rhgi-glow'>{abuja_now.strftime('%I:%M:%S %p WAT')}</span>"
    f"<br><small style='color:#aab8e0'>FCT APC (proj): {fct_pct:.2f}%</small></div>",
    unsafe_allow_html=True,
)
c2.markdown(
    f"<div class='rhgi-kpi'><b>24/37 Constitutional Gauge</b><br><span class='rhgi-gauge'>{states_25} / 37 states at ≥25% APC</span><br>"
    f"FCT: {'VALIDATED' if fct_validated else 'PENDING'} | {'PASS' if constitutional_ok else 'WATCH'}</div>",
    unsafe_allow_html=True,
)
c3.markdown(
    f"<div class='rhgi-kpi'><b>Winning Margin (live)</b><br><span class='rhgi-glow'>{total_winning_margin:,.0f}</span><br>"
    f"Turnout lift +{turnout_lift}%</div>",
    unsafe_allow_html=True,
)

st.markdown(
    f"<div class='rhgi-kpi' style='margin-bottom:12px;'><b>20.7M mandate anchor</b> — Target: <span class='rhgi-glow'>{NATIONAL_VOTE_TARGET:,}</span> · "
    f"Projected yield: <span class='rhgi-glow'>{projected_yield:,}</span> · "
    f"<b>Remittance gap:</b> <span class='rhgi-glow'>{remittance_gap:,}</span></div>",
    unsafe_allow_html=True,
)

st.subheader("Winning Margin by Geopolitical Zone (turnout-adjusted)")
zone_margin = (
    dff.groupby("zone", as_index=False)["winning_margin"].sum().sort_values("winning_margin")
)
fig_zone = px.bar(
    zone_margin,
    x="zone",
    y="winning_margin",
    color_discrete_sequence=[GOLD],
    template="plotly_dark",
)
fig_zone.update_layout(
    paper_bgcolor=PRISM_NAVY,
    plot_bgcolor=PRISM_NAVY_PLOT,
    font_color="#dbe2ff",
    xaxis_title="Zone",
    yaxis_title="Winning Margin (APC vs nearest rival)",
)
fig_zone.update_traces(marker=dict(color=GOLD, line=dict(color=GOLD, width=0)))
st.plotly_chart(fig_zone, use_container_width=True)

st.subheader("Turnout heatmap — Nigeria (strike priority)")
state_hm = build_state_heatmap_df(dff)
fig_scatter = px.scatter_mapbox(
    state_hm,
    lat="lat",
    lon="lon",
    color="strike_priority",
    size="strike_priority",
    hover_name="state",
    hover_data=["pvc_collection_rate", "turnout_2023_rate"],
    color_continuous_scale=[NAVY, "#2a4d8c", GOLD],
    mapbox_style="open-street-map",
    zoom=4.85,
    center={"lat": 9.082, "lon": 8.6753},
    template="plotly_dark",
    title="High PVC + low 2023 turnout → metallic gold (high-priority strike zones)",
)
fig_scatter.update_layout(
    paper_bgcolor=PRISM_NAVY,
    plot_bgcolor=PRISM_NAVY,
    font_color="#dbe2ff",
    margin=dict(l=0, r=0, t=40, b=0),
)
# Strike priority encoded as navy → metallic gold on Prism-Frame canvas.
fig_scatter.update_traces(marker=dict(line=dict(width=0.4, color="rgba(255,215,0,0.35)")))
st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader("2023 vs 2027 Party Totals")
party_totals = pd.DataFrame(
    {
        "Party": ["APC", "PDP", "LP", "ADC"] * 2,
        "Year": ["2023"] * 4 + ["2027"] * 4,
        "Votes": [
            df["apc_2023"].sum(),
            df["pdp_2023"].sum(),
            df["lp_2023"].sum(),
            df["adc_2023"].sum(),
            dff["apc_2027"].sum(),
            dff["pdp_2027"].sum(),
            dff["lp_2027"].sum(),
            dff["adc_2027"].sum(),
        ],
    }
)
fig_party = px.bar(
    party_totals,
    x="Party",
    y="Votes",
    color="Year",
    barmode="group",
    color_discrete_map={"2023": NAVY, "2027": GOLD},
    template="plotly_dark",
)
fig_party.update_layout(
    paper_bgcolor=PRISM_NAVY,
    plot_bgcolor=PRISM_NAVY_PLOT,
    font_color="#dbe2ff",
)
st.plotly_chart(fig_party, use_container_width=True)

st.subheader("LGA Tactical Sheet (Logistics Alert)")
view = dff[
    [
        "zone",
        "state",
        "lga",
        "pvc_collection_rate",
        "turnout_2023_rate",
        "apc_2023",
        "pdp_2023",
        "lp_2023",
        "adc_2023",
        "apc_2027",
        "pdp_2027",
        "lp_2027",
        "adc_2027",
        "winning_margin",
        "canvasser_ratio",
        "red_zone",
    ]
].copy()

view["winning_margin"] = view["winning_margin"].map(lambda x: f"{x:,.0f}")
view["canvasser_ratio"] = view["canvasser_ratio"].map(lambda x: f"{x:.2f}")
view["pvc_collection_rate"] = view["pvc_collection_rate"].map(lambda x: f"{x:.2%}")
view["turnout_2023_rate"] = view["turnout_2023_rate"].map(lambda x: f"{x:.2%}")

rows = []
for _, r in view.iterrows():
    css = "rhgi-pulse-red" if r["red_zone"] else ""
    rows.append(
        f"<tr class='{css}'>"
        f"<td>{r['zone']}</td><td>{r['state']}</td><td>{r['lga']}</td>"
        f"<td>{r['pvc_collection_rate']}</td><td>{r['turnout_2023_rate']}</td>"
        f"<td>{r['apc_2023']}</td><td>{r['pdp_2023']}</td><td>{r['lp_2023']}</td><td>{r['adc_2023']}</td>"
        f"<td>{r['apc_2027']}</td><td>{r['pdp_2027']}</td><td>{r['lp_2027']}</td><td>{r['adc_2027']}</td>"
        f"<td class='rhgi-glow'>{r['winning_margin']}</td><td>{r['canvasser_ratio']}</td>"
        "</tr>"
    )

table_html = (
    "<table><thead><tr>"
    "<th>Zone</th><th>State</th><th>LGA</th>"
    "<th>PVC %</th><th>Turnout '23</th>"
    "<th>APC23</th><th>PDP23</th><th>LP23</th><th>ADC23</th>"
    "<th>APC27</th><th>PDP27</th><th>LP27</th><th>ADC27</th>"
    "<th>Winning Margin</th><th>Canvasser Ratio</th>"
    "</tr></thead><tbody>"
    + "".join(rows[:200])
    + "</tbody></table>"
)
st.markdown(table_html, unsafe_allow_html=True)
st.caption(
    "Showing first 200 LGAs. Red pulsing rows: canvasser ratio below 1:16. "
    "Move the sidebar slider to watch winning margin and constitutional gauge update."
)
