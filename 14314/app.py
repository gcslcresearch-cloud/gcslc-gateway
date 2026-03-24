import pandas as pd
import plotly.express as px
import pytz
import streamlit as st
from datetime import datetime

from data_engine import ALL_LGA_RECORDS, records_as_dicts

st.set_page_config(page_title="RHGI 774 Scientific Engine", layout="wide")

GOLD = "#FFD700"
NAVY = "#1A237E"


@st.cache_data(show_spinner=False)
def load_df() -> pd.DataFrame:
    df = pd.DataFrame(records_as_dicts(ALL_LGA_RECORDS))
    df["winner_2023"] = df[["apc_2023", "pdp_2023", "lp_2023", "adc_2023"]].max(axis=1)
    df["winner_2027"] = df[["apc_2027", "pdp_2027", "lp_2027", "adc_2027"]].max(axis=1)
    df["winning_margin"] = df["apc_2027"] - df[["pdp_2027", "lp_2027", "adc_2027"]].max(axis=1)
    df["projected_total"] = df[["apc_2027", "pdp_2027", "lp_2027", "adc_2027"]].sum(axis=1)
    df["apc_share_2027"] = (df["apc_2027"] / df["projected_total"]) * 100
    df["red_zone"] = df["canvasser_ratio"] < 16.0
    return df


df = load_df()

lagos_tz = pytz.timezone("Africa/Lagos")
abuja_now = datetime.now(lagos_tz)

state_projection = (
    df.groupby("state", as_index=False)[["apc_2027", "projected_total"]]
    .sum()
    .assign(apc_pct=lambda x: (x["apc_2027"] / x["projected_total"]) * 100)
)
states_25 = (state_projection["apc_pct"] >= 25).sum()
fct_validated = bool(
    state_projection.loc[state_projection["state"] == "FCT", "apc_pct"].ge(25).any()
)
constitutional_ok = states_25 >= 24 and fct_validated

st.markdown(
    """
    <style>
    .rhgi-kpi {padding: 10px 12px; border-radius: 10px; border:1px solid #334; background:#0b1024;}
    .rhgi-pulse-red { animation: pulseRed 1s ease-in-out infinite; }
    @keyframes pulseRed {
      0%,100% { box-shadow: 0 0 0 rgba(255,0,0,0); }
      50% { box-shadow: 0 0 20px rgba(255,0,0,0.8); }
    }
    .rhgi-glow { color:#FFD700; text-shadow: 0 0 10px rgba(255,215,0,0.6); }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("RHGI 774 Scientific Engine")
c1, c2, c3 = st.columns(3)
c1.markdown(
    f"<div class='rhgi-kpi'><b>Abuja Pulse (UTC+1)</b><br><span class='rhgi-glow'>{abuja_now.strftime('%I:%M:%S %p WAT')}</span></div>",
    unsafe_allow_html=True,
)
c2.markdown(
    f"<div class='rhgi-kpi'><b>Constitutional Sentinel</b><br>{states_25}/37 states at 25% APC threshold</div>",
    unsafe_allow_html=True,
)
c3.markdown(
    f"<div class='rhgi-kpi'><b>FCT (Abuja)</b><br>{'VALIDATED' if fct_validated else 'PENDING'} | {'PASS' if constitutional_ok else 'WATCH'}</div>",
    unsafe_allow_html=True,
)

st.subheader("Winning Margin by Geopolitical Zone")
zone_margin = (
    df.groupby("zone", as_index=False)["winning_margin"].sum().sort_values("winning_margin")
)
fig_zone = px.bar(
    zone_margin,
    x="zone",
    y="winning_margin",
    color_discrete_sequence=[GOLD],
    template="plotly_dark",
)
fig_zone.update_layout(
    paper_bgcolor="#0a0f22",
    plot_bgcolor="#0a0f22",
    font_color="#dbe2ff",
    xaxis_title="Zone",
    yaxis_title="Winning Margin (APC vs nearest rival)",
)
st.plotly_chart(fig_zone, use_container_width=True)

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
            df["apc_2027"].sum(),
            df["pdp_2027"].sum(),
            df["lp_2027"].sum(),
            df["adc_2027"].sum(),
        ],
    }
)
fig_party = px.bar(
    party_totals,
    x="Party",
    y="Votes",
    color="Year",
    barmode="group",
    color_discrete_map={"2023": "#1A237E", "2027": "#FFD700"},
    template="plotly_dark",
)
fig_party.update_layout(
    paper_bgcolor="#0a0f22",
    plot_bgcolor="#0a0f22",
    font_color="#dbe2ff",
)
st.plotly_chart(fig_party, use_container_width=True)

st.subheader("LGA Tactical Sheet (Logistics Alert)")
view = df[
    [
        "zone",
        "state",
        "lga",
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

rows = []
for _, r in view.iterrows():
    css = "rhgi-pulse-red" if r["red_zone"] else ""
    rows.append(
        f"<tr class='{css}'>"
        f"<td>{r['zone']}</td><td>{r['state']}</td><td>{r['lga']}</td>"
        f"<td>{r['apc_2023']}</td><td>{r['pdp_2023']}</td><td>{r['lp_2023']}</td><td>{r['adc_2023']}</td>"
        f"<td>{r['apc_2027']}</td><td>{r['pdp_2027']}</td><td>{r['lp_2027']}</td><td>{r['adc_2027']}</td>"
        f"<td class='rhgi-glow'>{r['winning_margin']}</td><td>{r['canvasser_ratio']}</td>"
        "</tr>"
    )

table_html = (
    "<table><thead><tr>"
    "<th>Zone</th><th>State</th><th>LGA</th>"
    "<th>APC23</th><th>PDP23</th><th>LP23</th><th>ADC23</th>"
    "<th>APC27</th><th>PDP27</th><th>LP27</th><th>ADC27</th>"
    "<th>Winning Margin</th><th>Canvasser Ratio</th>"
    "</tr></thead><tbody>"
    + "".join(rows[:200])  # keep page responsive
    + "</tbody></table>"
)
st.markdown(table_html, unsafe_allow_html=True)
st.caption("Showing first 200 LGAs for UI speed. Red pulsing rows indicate canvasser ratio below 1:16.")

