import hashlib
import html
import pandas as pd
import plotly.express as px
import pytz
import streamlit as st
from datetime import datetime, time

from data_engine import ALL_LGA_RECORDS, STATE_COORDS, records_as_dicts

st.set_page_config(
    page_title="Renewed Hope Grassroots Initiatives (RHGI) - 15/15 Sovereign Mirror",
    layout="wide",
    initial_sidebar_state="expanded",
)
if "corridor_zone" not in st.session_state:
    st.session_state.corridor_zone = None
if "_prev_corridor_state_key" not in st.session_state:
    st.session_state._prev_corridor_state_key = None

# RHGI-GOLDMAN palette (mirrors :root CSS variables).
METALLIC_GOLD = "#D4AF37"
NAVY_CSS = "#000033"
GOLD = METALLIC_GOLD
NAVY = NAVY_CSS
# Deep Prism Navy (video match — RHGI ABSOLUTE RESTORE-39).
PRISM_NAVY = "#000033"
CANVASSER_BUDGET_ANCHOR_NGN = 30_000
# RHGI TOTAL RESTORE-30 — Sovereign Budget Engine (personnel lines per mandate brief).
SOVEREIGN_CANVASSERS_LINE = 144_000
SOVEREIGN_EDAY_STAFF_LINE = 144_000
SOVEREIGN_UNIT_NGN = 30_000
SOVEREIGN_MISC_PCT = 0.15
SOVEREIGN_CONTINGENCY_PCT = 0.10
# RHGI video brief — sovereign headline (₦108.96B); line-model arithmetic shown in UI.
SOVEREIGN_BUDGET_MANDATE_NGN = 108_960_000_000
# Deep Navy → metallic gold — 774 LGA winning-margin map.
DEEP_NAVY_SAFE = "#152a45"
METALLIC_GOLD_TARGET = METALLIC_GOLD
# 20.7M national vote mandate anchor (fixed reference).
NATIONAL_VOTE_TARGET = 20_709_668
# Drill-down order: abbrev → full zone name (matches dff["zone"]).
CORRIDOR_NODES = (
    ("NW", "North West"),
    ("NE", "North East"),
    ("NC", "North Central"),
    ("SW", "South West"),
    ("SS", "South South"),
    ("SE", "South East"),
)
# 2027 general election countdown anchor (WAT); adjust if INEC publishes a firm date.
_LAGOS_TZ = pytz.timezone("Africa/Lagos")
ELECTION_DATETIME_WAT = _LAGOS_TZ.localize(datetime(2027, 2, 25, 8, 0, 0))
EIGHT_R_DETERMINANTS = [
    ("Refine", "Proprietary Determinant — Refine: Sharpening ward-level turnout models and PVC reconciliation."),
    ("Reset", "Proprietary Determinant — Reset: Re-anchoring baselines to 2023 forensic vote totals."),
    ("Research", "Proprietary Determinant — Research: Fusing polling streams with sovereign yield signals."),
    ("Restructure", "Proprietary Determinant — Restructure: Re-drawing corridor logistics and canvasser geometry."),
    ("Resuscitate", "Proprietary Determinant — Resuscitate: Activating dormant voter banks in low-turnout cells."),
    ("Revitalize", "Proprietary Determinant — Revitalize: Calibrating coalition messaging to zone determinants."),
    ("Re-engineer", "Proprietary Determinant — Re-engineer: Re-scaling scenario lifts to scientific turnout bands."),
    ("Retain", "Proprietary Determinant — Retain: Locking mandate gains through post-election stewardship."),
]


def _gold_heading(text: str) -> None:
    st.markdown(f'<p class="rhgi-gold-heading">{text}</p>', unsafe_allow_html=True)


def _rose_heading(text: str) -> None:
    """Corridor section titles — Yellow Gold (strict video / COMPLIANCE-45)."""
    st.markdown(f'<p class="rhgi-corridor-gold-heading">{html.escape(text)}</p>', unsafe_allow_html=True)


def sovereign_budget_engine_breakdown() -> tuple[int, int, int]:
    """(144k + 144k) × ₦30k + 15% misc + 10% contingency → returns (base, after_misc, total) in ₦."""
    base = (SOVEREIGN_CANVASSERS_LINE + SOVEREIGN_EDAY_STAFF_LINE) * SOVEREIGN_UNIT_NGN
    after_misc = round(base * (1.0 + SOVEREIGN_MISC_PCT))
    total = round(after_misc * (1.0 + SOVEREIGN_CONTINGENCY_PCT))
    return base, after_misc, total


def _format_election_countdown(now: datetime) -> str:
    """Election Countdown: Days : Hours : Minutes : Seconds until election anchor WAT."""
    now = now.astimezone(_LAGOS_TZ)
    tgt = ELECTION_DATETIME_WAT
    if now >= tgt:
        return "Election Countdown: 0 : 00 : 00 : 00 — verify certified INEC 2027 calendar."
    delta = tgt - now
    total_sec = int(delta.total_seconds())
    days = total_sec // (24 * 3600)
    rem = total_sec % (24 * 3600)
    h = rem // 3600
    rem %= 3600
    m = rem // 60
    s = rem % 60
    return f"Election Countdown: {days} : {h:02d} : {m:02d} : {s:02d}"


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
    df["logistics_alert"] = df["canvasser_ratio"] < 16.0
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


def legal_gatekeeper(dff: pd.DataFrame) -> tuple[int, bool, bool]:
    """Count the 36 states (excl. FCT) where APC projected share ≥ 25%.
    Constitutional mandate: count ≥ 24 of those states AND FCT ≥ 25%."""
    state_projection = (
        dff.groupby("state", as_index=False)[["apc_2027", "projected_total"]]
        .sum()
        .assign(
            apc_pct=lambda x: (x["apc_2027"] / x["projected_total"].replace(0, 1)) * 100
        )
    )
    sp36 = state_projection[state_projection["state"] != "FCT"]
    states_ge_25 = int((sp36["apc_pct"] >= 25).sum())
    fct = state_projection.loc[state_projection["state"] == "FCT", "apc_pct"]
    fct_ge_25 = bool(fct.ge(25).any()) if len(fct) else False
    mandate_secured = states_ge_25 >= 24 and fct_ge_25
    return states_ge_25, fct_ge_25, mandate_secured


def constitutional_sentinel(dff: pd.DataFrame) -> tuple[int, bool, bool]:
    """Backward-compatible alias for legal_gatekeeper."""
    return legal_gatekeeper(dff)


def _lga_lat_lon(state: str, lga: str) -> tuple[float, float]:
    """Deterministic jitter around state centroid so 774 LGAs map as distinct points."""
    base_lat, base_lon = STATE_COORDS.get(state, (9.0, 8.0))
    digest = hashlib.sha256(f"{state}:{lga}".encode("utf-8")).hexdigest()
    jlat = (int(digest[:4], 16) / 0xFFFF - 0.5) * 0.42
    jlon = (int(digest[4:8], 16) / 0xFFFF - 0.5) * 0.42
    return base_lat + jlat, base_lon + jlon


def margin_zone(row: pd.Series) -> str:
    """Classify LGA by winning margin (share of projected total)."""
    m = float(row["winning_margin"])
    pt = max(float(row["projected_total"]), 1.0)
    m_pct = 100.0 * m / pt
    if m < 0:
        return "Opposition Stronghold"
    if m_pct < 4.0:
        return "Target"
    return "Safe APC"


def build_lga_heatmap_df(dff: pd.DataFrame) -> pd.DataFrame:
    out = dff.copy()
    lats, lons = [], []
    for _, r in out.iterrows():
        la, lo = _lga_lat_lon(str(r["state"]), str(r["lga"]))
        lats.append(la)
        lons.append(lo)
    out["lat"] = lats
    out["lon"] = lons
    out["margin_zone"] = out.apply(margin_zone, axis=1)
    return out


def acceptance_velocity_pct(apc_2023: int, apc_2027: int) -> float:
    """YoY-style growth in APC votes: (2027 − 2023) / 2023 × 100."""
    a3 = max(int(apc_2023), 0)
    a7 = int(apc_2027)
    if a3 <= 0:
        return 0.0 if a7 <= 0 else 100.0
    return round(100.0 * (a7 - a3) / a3, 2)


def build_state_lga_matrix_df(dff: pd.DataFrame, state: str) -> pd.DataFrame:
    """Per-state LGA matrix for corridor drill-down."""
    sub = dff.loc[dff["state"] == state, ["lga", "apc_2023", "apc_2027", "canvassers"]].copy()
    sub["_lk"] = sub["lga"].str.lower()
    sub = sub.sort_values("_lk").drop(columns="_lk")
    sub["Acceptance Velocity (%)"] = sub.apply(
        lambda r: acceptance_velocity_pct(r["apc_2023"], r["apc_2027"]),
        axis=1,
    )
    sub["Canvasser Budget (₦30k anchor)"] = (
        sub["canvassers"].astype(int) * CANVASSER_BUDGET_ANCHOR_NGN
    )
    sub = sub.rename(
        columns={
            "lga": "LGA Name",
            "apc_2023": "2023 Actual APC",
            "apc_2027": "2027 Sovereign Projection",
        }
    )
    return sub[
        [
            "LGA Name",
            "2023 Actual APC",
            "2027 Sovereign Projection",
            "Acceptance Velocity (%)",
            "Canvasser Budget (₦30k anchor)",
        ]
    ]


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

lagos_tz = _LAGOS_TZ

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap');
    :root {
      --metallic-gold: #D4AF37;
      --rose-gold: #D4AF37;
      --navy: #000033;
      --stark-white: #ffffff;
    }
    /* Anti-Blue Strike — strip default Streamlit / BaseWeb blues */
    html, body { background: #000033 !important; }
    [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] > .main {
      background: #000033 !important;
    }
    [data-testid="stHeader"], header[data-testid="stHeader"] {
      background: rgba(0, 0, 51, 0.97) !important;
      border-bottom: 1px solid rgba(212, 175, 55, 0.25) !important;
    }
    [data-testid="stDecoration"] { background: #000033 !important; }
    [data-testid="stToolbar"] { background: transparent !important; }
    [data-testid="stSidebarNav"] { background: transparent !important; }
    div[data-testid="stVerticalBlockBorderWrapper"] { border-color: rgba(212,175,55,0.2) !important; }
    [data-baseweb="slider"] [role="slider"] { background: var(--metallic-gold) !important; }
    [data-baseweb="slider"] [data-testid="stThumbValue"] { color: var(--metallic-gold) !important; }
    [data-baseweb="slider"] [style*="background"] { background: rgba(0,0,51,0.6) !important; }
    [data-testid="stSlider"], [data-testid="stSlider"] > label,
    [data-testid="stSlider"] + div { background: transparent !important; }
    .stMetric, [data-testid="stMetricContainer"], [data-testid="stMetricContainer"] > div {
      background: rgba(0,0,51,0.55) !important;
      background-image: none !important;
      border: 1px solid rgba(212,175,55,0.3) !important;
      border-radius: 10px !important;
      box-shadow: none !important;
    }
    .stMetric [data-testid="stMetricValue"] { color: var(--stark-white) !important; }
    .stMetric [data-testid="stMetricLabel"] { color: var(--metallic-gold) !important; }
    [data-testid="stMetricDelta"] { color: var(--metallic-gold) !important; }
    .stAlert, [data-testid="stNotification"], [data-testid="stAlert"] {
      background: rgba(0,0,51,0.65) !important;
      background-image: none !important;
      border: 1px solid rgba(212,175,55,0.35) !important;
      box-shadow: none !important;
    }
    .stInfo { color: var(--stark-white) !important; }
    [data-testid="stAlert"] { color: var(--stark-white) !important; font-family: 'Goldman', sans-serif !important; }
    a, a:visited { color: var(--metallic-gold) !important; }
    a:hover { color: var(--metallic-gold) !important; }
    iframe { background: #000033 !important; }
    /* Kill residual Streamlit / BaseWeb light surfaces */
    [data-testid="stVerticalBlock"] > div,
    [data-testid="stVerticalBlockBorderWrapper"] > div { background-color: transparent !important; }
    div[data-baseweb="select"] > div,
    [data-baseweb="popover"],
    ul[data-testid="stSelectboxVirtualDropdown"],
    [data-baseweb="menu"] { background-color: #000033 !important; color: var(--stark-white) !important; }
    [data-baseweb="menu"] li { font-family: 'Goldman', sans-serif !important; color: var(--stark-white) !important; }
    .stCodeBlock, [data-testid="stCode"] { background: rgba(0,0,51,0.5) !important; }
    /* No white cards: selectbox, popover, expanders, columns */
    [data-testid="stSelectbox"] > div,
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
      background-color: #000033 !important;
      color: var(--stark-white) !important;
      border-color: rgba(212,175,55,0.35) !important;
    }
    [data-testid="stExpander"] details { background: #000033 !important; border: 1px solid rgba(212,175,55,0.25) !important; }
    [data-testid="stExpander"] summary { background: rgba(0,0,51,0.5) !important; color: var(--stark-white) !important; }
    [data-testid="stVerticalBlock"] > div { background-color: transparent !important; }
    div[data-testid="column"] > div { background-color: transparent !important; }
    .stApp {
      background-color: #000033 !important;
      background-image: none !important;
      color: var(--stark-white) !important;
      font-family: 'Goldman', sans-serif !important;
      user-select: none;
      -webkit-user-select: none;
    }
    .stApp h1, .stApp h2, .stApp h3, .stApp h4,
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
    [data-testid="stHeader"] { font-family: 'Goldman', sans-serif !important; }
    .stApp, .stApp label, .stApp p, .stApp span, .stApp div, .stApp li,
    .stApp input, .stApp textarea, .stApp button, .stApp select,
    [data-testid="stSidebar"], [data-testid="stSidebar"] * {
      font-family: 'Goldman', sans-serif !important;
    }
    .stApp *:not(svg):not(path):not(circle):not(rect):not(line):not(polyline):not(polygon) {
      font-family: 'Goldman', sans-serif !important;
    }
    svg text { font-family: 'Goldman', sans-serif !important; }
    [data-testid="stSidebar"] {
      background: #000033 !important;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] label { color: var(--stark-white) !important; }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
      color: var(--metallic-gold) !important;
    }
    .block-container {
      font-size: 1.1rem;
      position: relative;
      z-index: 2 !important;
      font-family: 'Goldman', sans-serif !important;
      color: var(--stark-white) !important;
      background: #000033 !important;
    }
    section.main [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
      background-color: #000033 !important;
      border-radius: 10px;
      border: none !important;
      box-shadow: none !important;
    }
    div[data-testid="stAppViewContainer"] > section.main { position: relative; z-index: 1; }
    .rhgi-brand-title {
      font-family: 'Goldman', system-ui, sans-serif !important;
      font-size: clamp(1.85rem, 4.2vw, 2.65rem);
      font-weight: 700;
      letter-spacing: 0.06em;
      color: var(--metallic-gold) !important;
      -webkit-text-fill-color: var(--metallic-gold);
      text-shadow:
        0 0 20px rgba(212, 175, 55, 0.55),
        0 0 40px rgba(183, 110, 121, 0.35);
      text-align: center;
      margin: 0.35rem 0 0.65rem 0;
      line-height: 1.2;
      animation: rhgiGoldmanShimmer 3.5s ease-in-out infinite;
    }
    @keyframes rhgiGoldmanShimmer {
      0%, 100% { filter: brightness(1) drop-shadow(0 0 8px rgba(212,175,55,0.4)); }
      50% { filter: brightness(1.12) drop-shadow(0 0 22px rgba(212,175,55,0.75)); }
    }
    .rhgi-emblem-wrap { text-align: center; margin: 8px 0 12px 0; transform: scale(1.05); }
    .rhgi-emblem {
      width: 128px; height: 128px; margin: 0 auto;
      border-radius: 50%;
      border: 4px solid var(--metallic-gold);
      display: flex; align-items: center; justify-content: center;
      font-family: 'Goldman', sans-serif;
      font-weight: 700;
      font-size: 2rem;
      letter-spacing: 0.08em;
      color: var(--metallic-gold);
      text-shadow: 0 0 18px rgba(212, 175, 55, 0.95), 0 0 36px rgba(212, 175, 55, 0.35);
      box-shadow:
        0 0 36px rgba(212, 175, 55, 0.45),
        inset 0 0 28px rgba(212, 175, 55, 0.12);
      animation: emblemGoldPulse 2.8s ease-in-out infinite;
    }
    @keyframes emblemGoldPulse {
      0%, 100% { filter: brightness(1); box-shadow: 0 0 28px rgba(212,175,55,0.45); }
      50% { filter: brightness(1.12); box-shadow: 0 0 52px rgba(212,175,55,0.75); }
    }
    .rhgi-countdown-meter {
      text-align: center;
      font-size: clamp(1.25rem, 3.5vw, 1.55rem);
      font-weight: 800;
      font-family: 'Goldman', sans-serif !important;
      color: var(--stark-white) !important;
      margin: 4px 0 6px 0;
      letter-spacing: 0.12em;
      text-shadow: 0 0 18px rgba(212, 175, 55, 0.55);
    }
    .rhgi-countdown-keys {
      text-align: center;
      font-size: clamp(0.82rem, 2.2vw, 0.92rem);
      font-weight: 600;
      color: var(--metallic-gold) !important;
      margin: 0 0 12px 0;
      letter-spacing: 0.06em;
    }
    .rhgi-creed {
      font-size: clamp(1.08rem, 2.9vw, 1.22rem);
      line-height: 1.65;
      color: var(--stark-white) !important;
      font-family: 'Goldman', sans-serif !important;
      max-width: 1000px;
      margin: 0 auto 16px auto;
      text-align: center;
      font-weight: 500;
    }
    .rhgi-signature {
      font-size: clamp(0.98rem, 2.6vw, 1.08rem);
      color: var(--metallic-gold) !important;
      font-weight: 700;
      text-align: center;
      margin-bottom: 22px;
      letter-spacing: 0.03em;
    }
    .rhgi-wm-root { position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden; opacity: 0.45; }
    .rhgi-wm-inner {
      position: absolute; width: 260%; height: 260%; left: -80%; top: -80%;
      display: flex; flex-wrap: wrap; align-content: flex-start; gap: 2.2rem 3.2rem;
      transform: rotate(-14deg);
      animation: wmBubbleDrift 110s ease-in-out infinite;
    }
    .rhgi-wm-cell {
      font-size: clamp(2rem, 6.5vw, 3.4rem);
      font-weight: 900;
      color: rgba(212, 175, 55, 0.5);
      user-select: none;
      animation: wmCellBubble 8s ease-in-out infinite;
    }
    .rhgi-wm-cell:nth-child(3n) { animation-delay: 0s; }
    .rhgi-wm-cell:nth-child(3n+1) { animation-delay: 2s; }
    .rhgi-wm-cell:nth-child(3n+2) { animation-delay: 4s; }
    @keyframes wmCellBubble {
      0%, 100% { transform: translateY(0) scale(1); opacity: 0.85; }
      50% { transform: translateY(-12px) scale(1.04); opacity: 1; }
    }
    @keyframes wmBubbleDrift {
      0% { transform: rotate(-14deg) translate(0, 0); }
      33% { transform: rotate(-14deg) translate(-36px, -48px); }
      66% { transform: rotate(-14deg) translate(24px, -80px); }
      100% { transform: rotate(-14deg) translate(0, 0); }
    }
    .rhgi-capture-shield {
      position: fixed; inset: 0; pointer-events: none; z-index: 9999;
      background:
        repeating-linear-gradient(0deg, rgba(255,255,255,0.04) 0px, transparent 1px, transparent 12px),
        repeating-linear-gradient(90deg, rgba(0,0,51,0.06) 0px, transparent 1px, transparent 14px),
        radial-gradient(ellipse at 30% 20%, rgba(212,175,55,0.04) 0%, transparent 55%);
      mix-blend-mode: soft-light;
      opacity: 0.92;
    }
    button, input, textarea, [data-testid="stMarkdownContainer"], .stMarkdown { user-select: text !important; -webkit-user-select: text !important; }
    /* 8R row: no white card behind buttons */
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)) [data-testid="element-container"],
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)) [data-testid="column"] {
      background: transparent !important;
      border: none !important;
      box-shadow: none !important;
    }
    /* Column buttons default: metallic gold */
    div[data-testid="column"] button[kind="secondary"],
    div[data-testid="column"] button[kind="primary"] {
      position: relative !important;
      overflow: hidden !important;
      font-size: 1.06rem !important;
      font-weight: 700 !important;
      font-family: 'Goldman', sans-serif !important;
      padding-top: 0.68rem !important;
      padding-bottom: 0.68rem !important;
      color: var(--metallic-gold) !important;
      border: 1px solid rgba(212, 175, 55, 0.55) !important;
      background: linear-gradient(155deg, #00000e 0%, #00001a 55%, #000033 100%) !important;
      background-size: 220% 100% !important;
      animation: r8MetalPulse 2.6s ease-in-out infinite;
    }
    /* 8R belt: Yellow Gold text + navy field + shimmer (no white, no neon) */
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)) button[kind="secondary"],
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)) button[kind="primary"] {
      color: var(--metallic-gold) !important;
      border: 1px solid rgba(212, 175, 55, 0.55) !important;
      background: linear-gradient(155deg, #000005 0%, #00000f 50%, #00001c 100%) !important;
      background-size: 220% 100% !important;
      animation: r8WidgetPulse 2s ease-in-out infinite, r8ShimmerSweep 3s linear infinite !important;
    }
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)) button p,
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)) button span {
      color: #D4AF37 !important;
      animation: r8GoldTextShimmer 2.4s ease-in-out infinite !important;
    }
    @keyframes r8GoldTextShimmer {
      0%, 100% {
        color: #D4AF37 !important;
        text-shadow: 0 0 8px rgba(212,175,55,0.45), 0 0 14px rgba(0,0,51,0.6);
      }
      50% {
        color: #f0e68c !important;
        text-shadow:
          0 0 22px rgba(212, 175, 55, 0.75),
          0 0 36px rgba(212, 175, 55, 0.35),
          0 0 4px rgba(255, 255, 255, 0.25);
      }
    }
    /* 6-column corridor belt: Yellow Gold + navy + shimmer */
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)):not(:has(> div:nth-child(7))) button[kind="secondary"],
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)):not(:has(> div:nth-child(7))) button[kind="primary"] {
      color: var(--metallic-gold) !important;
      border: 1px solid rgba(212, 175, 55, 0.55) !important;
      background: linear-gradient(155deg, #000005 0%, #00000f 50%, #00001c 100%) !important;
      background-size: 220% 100% !important;
      animation: r8WidgetPulse 2s ease-in-out infinite, r8ShimmerSweep 3s linear infinite !important;
    }
    @keyframes r8WidgetPulse {
      0%, 100% { box-shadow: 0 0 8px rgba(212,175,55,0.25); transform: scale(1); }
      50% { box-shadow: 0 0 22px rgba(212,175,55,0.45); transform: scale(1.02); }
    }
    @keyframes r8MetalPulse {
      0%, 100% { box-shadow: 0 0 10px rgba(212,175,55,0.2); }
      50% { box-shadow: 0 0 26px rgba(212,175,55,0.4); }
    }
    @keyframes r8ShimmerSweep {
      0% { background-position: 200% center; }
      100% { background-position: -200% center; }
    }
    .rhgi-lga-scroll-outer {
      overflow: hidden;
      max-height: 58vh;
      border: 1px solid rgba(212, 175, 55, 0.4);
      border-radius: 14px;
      background: rgba(0, 0, 51, 0.22);
    }
    .rhgi-lga-marquee {
      display: flex;
      flex-direction: column;
      animation: rhgiSlowRoll 140s linear infinite;
    }
    .rhgi-lga-marquee:hover { animation-play-state: paused; }
    @keyframes rhgiSlowRoll {
      0% { transform: translateY(0); }
      100% { transform: translateY(-50%); }
    }
    .rhgi-lga-scroll {
      max-height: 58vh;
      overflow-y: auto;
      scroll-behavior: smooth;
      border: 1px solid rgba(212, 175, 55, 0.35);
      border-radius: 12px;
      background: rgba(0, 0, 51, 0.35);
    }
    .rhgi-kpi {
      padding: 12px 14px;
      border-radius: 10px;
      border: 1px solid rgba(212, 175, 55, 0.35);
      background: rgba(0, 0, 51, 0.45);
      font-family: 'Goldman', sans-serif !important;
      color: var(--stark-white) !important;
    }
    .rhgi-pulse-logistics { animation: pulseLogisticsGold 1.1s ease-in-out infinite; }
    @keyframes pulseLogisticsGold {
      0%,100% { box-shadow: 0 0 0 rgba(212,175,55,0); }
      50% { box-shadow: 0 0 18px rgba(212,175,55,0.65); }
    }
    .rhgi-glow { color: var(--metallic-gold); text-shadow: 0 0 12px rgba(212,175,55,0.65); }
    .rhgi-gauge { font-size: 1.1rem; letter-spacing: 0.03em; }
    .rhgi-abuja-strobe {
      border: 2px solid rgba(212, 175, 55, 0.85) !important;
      animation: abujaGoldStrobe 0.9s ease-in-out infinite;
    }
    @keyframes abujaGoldStrobe {
      0%, 100% { box-shadow: 0 0 4px rgba(212, 175, 55, 0.35); }
      50% { box-shadow: 0 0 22px rgba(212, 175, 55, 0.75); }
    }
    .rhgi-8r-stealth {
      font-size: 1.05rem;
      font-weight: 800;
      letter-spacing: 0.28em;
      text-transform: uppercase;
      color: var(--metallic-gold) !important;
      text-shadow: 0 0 14px rgba(212,175,55,0.5), 0 0 28px rgba(0,0,51,0.55);
      margin: 8px 0 6px 0;
    }
    .rhgi-mandate-secured {
      text-align: center;
      padding: 14px 18px;
      margin: 12px 0 16px 0;
      border-radius: 12px;
      border: 3px solid var(--metallic-gold);
      background: #000033 !important;
      animation: mandateGoldPulse 1.4s ease-in-out infinite;
    }
    @keyframes mandateGoldPulse {
      0%, 100% { box-shadow: 0 0 6px rgba(212, 175, 55, 0.45), inset 0 0 20px rgba(212,175,55,0.08); }
      50% { box-shadow: 0 0 26px rgba(212, 175, 55, 0.95), inset 0 0 28px rgba(212,175,55,0.15); }
    }
    .rhgi-ticker-wrap {
      position: relative;
      overflow: hidden;
      width: 100%;
      background: #000033;
      border-top: 1px solid rgba(212,175,55,0.4);
      border-bottom: 1px solid rgba(212,175,55,0.4);
      margin-top: 18px;
    }
    .rhgi-ticker {
      display: inline-block;
      white-space: nowrap;
      padding: 10px 0;
      animation: tickerScroll 42s linear infinite;
      color: var(--metallic-gold);
      font-weight: 600;
      letter-spacing: 0.04em;
      text-shadow: 0 0 8px rgba(212,175,55,0.5);
    }
    .rhgi-ticker span { padding-right: 4rem; }
    @keyframes tickerScroll {
      0% { transform: translateX(0); }
      100% { transform: translateX(-50%); }
    }
    .rhgi-gold-heading { color: var(--metallic-gold) !important; font-weight: 800 !important; font-size: 1.38rem !important;
      margin: 0.5rem 0 0.35rem 0; text-shadow: 0 0 12px rgba(212,175,55,0.45); letter-spacing: 0.02em; font-family: 'Goldman', sans-serif !important; }
    .rhgi-corridor-gold-heading {
      color: var(--metallic-gold) !important;
      font-weight: 800 !important;
      font-size: 1.38rem !important;
      margin: 0.5rem 0 0.35rem 0;
      line-height: 1.35;
      letter-spacing: 0.08em;
      text-shadow: 0 0 14px rgba(212, 175, 55, 0.45);
      font-family: 'Goldman', sans-serif !important;
    }
    .stApp h1 { color: var(--metallic-gold) !important; font-weight: 800 !important; text-shadow: 0 0 14px rgba(212,175,55,0.4); }
    .rhgi-corridor-table { width: 100%; border-collapse: collapse; font-size: 1.14rem; line-height: 1.55; }
    .rhgi-corridor-table th {
      font-family: 'Goldman', sans-serif !important;
      color: var(--metallic-gold) !important; font-weight: 800 !important;
      text-align: left; padding: 14px 16px;
      background: rgba(0, 0, 51, 0.55);
      border-bottom: 2px solid rgba(212, 175, 55, 0.5);
      text-shadow: 0 0 10px rgba(212, 175, 55, 0.5), 0 0 20px rgba(212, 175, 55, 0.2);
      font-size: 1.12rem !important;
    }
    .rhgi-corridor-table td {
      font-family: 'Goldman', sans-serif !important;
      color: #ffffff !important; padding: 12px 16px;
      border-bottom: 1px solid rgba(212, 175, 55, 0.15);
      font-size: 1.1rem !important;
      font-weight: 600;
    }
    .rhgi-corridor-table tr:nth-child(even) td { background: rgba(0, 0, 51, 0.35); }
    [data-testid="stCaption"] { color: var(--metallic-gold) !important; font-family: 'Goldman', sans-serif !important; }
    [data-testid="stSelectbox"] label { color: var(--metallic-gold) !important; font-family: 'Goldman', sans-serif !important; }
    [data-baseweb="select"] { font-family: 'Goldman', sans-serif !important; }
    .rhgi-sovereign-budget {
      margin: 22px 0 8px 0;
      padding: 4px;
      border-radius: 16px;
      background: linear-gradient(120deg,
        rgba(212,175,55,0.95) 0%, rgba(255,248,220,0.5) 22%, rgba(212,175,55,0.9) 48%,
        rgba(255,236,160,0.45) 72%, rgba(212,175,55,0.95) 100%);
      background-size: 280% 100%;
      animation: sovereignFrameShimmer 4s ease-in-out infinite;
      box-shadow: 0 0 28px rgba(212, 175, 55, 0.35);
    }
    @keyframes sovereignFrameShimmer {
      0%, 100% { background-position: 0% center; filter: brightness(1); }
      50% { background-position: 100% center; filter: brightness(1.08); }
    }
    .rhgi-sovereign-budget-inner {
      background: #000033;
      border-radius: 13px;
      padding: 18px 22px;
      text-align: center;
    }
    .rhgi-sovereign-budget-inner h3 {
      font-family: 'Goldman', sans-serif !important;
      color: var(--metallic-gold) !important;
      margin: 0 0 10px 0;
      font-size: 1.25rem;
      letter-spacing: 0.06em;
      text-shadow: 0 0 14px rgba(212,175,55,0.5);
    }
    .rhgi-sovereign-mandate {
      font-family: 'Goldman', sans-serif !important;
      font-size: clamp(1.5rem, 4vw, 2.1rem);
      font-weight: 800;
      color: var(--metallic-gold) !important;
      margin: 0 0 8px 0;
      text-shadow: 0 0 20px rgba(212,175,55,0.65);
      animation: rhgiGoldmanShimmer 3.5s ease-in-out infinite;
    }
    .rhgi-sovereign-detail {
      font-family: 'Goldman', sans-serif !important;
      color: var(--stark-white) !important;
      font-size: 0.95rem;
      margin: 4px 0;
      line-height: 1.45;
    }
    /* RHGI-SOVEREIGN-ALIGNMENT-50 — allow per-figure Plotly backgrounds */
    [data-testid="stPlotlyChart"],
    [data-testid="stPlotlyChart"] .js-plotly-plot,
    [data-testid="stPlotlyChart"] .plotly-graph-div { background: transparent !important; }
    .js-plotly-plot .plotly .bg,
    .js-plotly-plot .plotly .bglayer rect { fill: transparent !important; }
    </style>
    """,
    unsafe_allow_html=True,
)
_wm_cells = "".join('<span class="rhgi-wm-cell">GCSLC</span>' for _ in range(48))
st.markdown(
    f'<div class="rhgi-wm-root" aria-hidden="true"><div class="rhgi-wm-inner">{_wm_cells}</div></div>'
    '<div class="rhgi-capture-shield" aria-hidden="true"></div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Scientific controls")
    st.subheader("Sovereign Budget Engine (Tranche 1)")
    st.metric("Global Sovereign Logistics Fuel:", "₦108,961,000,000")
    st.markdown(
        "₦8.64B (Canvassers) + ₦86.32B (Logistics) + ₦14B (Contingency)"
    )
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
PROJECTED_TOTAL = projected_yield
apc_national = int(dff["apc_2027"].sum())
national_apc_share = 100.0 * apc_national / max(projected_yield, 1)
remittance_gap = NATIONAL_VOTE_TARGET - PROJECTED_TOTAL
abuja_strobe = fct_pct < 25.0
total_winning_margin = float(dff["winning_margin"].sum())

abuja_now = datetime.now(lagos_tz)
_countdown_line = _format_election_countdown(abuja_now)
st.markdown(
    f"""
    <div class="rhgi-brand-block">
      <h1 class="rhgi-brand-title">Renewed Hope Grassroots Initiatives (RHGI) - 15/15 Sovereign Mirror</h1>
      <div class="rhgi-emblem-wrap"><div class="rhgi-emblem">RHGI</div></div>
      <p class="rhgi-countdown-keys">Election Countdown: Days : Hours : Minutes : Seconds → Feb 2027</p>
      <div class="rhgi-countdown-meter">{_countdown_line}</div>
      <p class="rhgi-creed">Decoding the 20.7M mandate anchor with scientific, uncorruptible precision. Powered by the 8R Stealth Paradigm.</p>
      <p class="rhgi-signature">Prepared by Galadiman Ruwa Center for Strategic Leadership and Communication GCSLC LTD/GTE.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
_r8_cols = st.columns(8)
for _ri, (_r8_label, _r8_det) in enumerate(EIGHT_R_DETERMINANTS):
    with _r8_cols[_ri]:
        st.button(
            _r8_label,
            key=f"r8_btn_{_ri}",
            help=_r8_det,
            use_container_width=True,
        )

c1, c2, c3 = st.columns(3)
# Abuja Pulse lead (UTC+1); Diamond Strobe when FCT projected APC < 25%.
_pulse_cls = "rhgi-kpi rhgi-abuja-strobe" if abuja_strobe else "rhgi-kpi"
c1.markdown(
    f"<div class='{_pulse_cls}'><b>Abuja Pulse (UTC+1)</b><br><span class='rhgi-glow'>{abuja_now.strftime('%I:%M:%S %p WAT')}</span>"
    f"<br><small style='color:#ffffff;font-weight:600;'>FCT APC (proj): {fct_pct:.2f}%</small></div>",
    unsafe_allow_html=True,
)
c2.markdown(
    f"<div class='rhgi-kpi'><b>24/36 + FCT Constitutional Gauge</b><br><span class='rhgi-gauge'>{states_25} / 36 states at ≥25% APC</span><br>"
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

if constitutional_ok:
    st.markdown(
        "<div class='rhgi-mandate-secured'><span class='rhgi-glow' style='font-size:1.35rem;font-weight:800;'>"
        "CONSTITUTIONAL MANDATE: SECURED</span><br>"
        "<small style='color:#ffffff;'>Legal Gatekeeper — ≥24 of 36 states at ≥25% APC and FCT ≥25%</small></div>",
        unsafe_allow_html=True,
    )

_gold_heading("Winning Margin by Geopolitical Zone (turnout-adjusted)")
zone_margin = (
    dff.groupby("zone", as_index=False)["winning_margin"].sum().sort_values("winning_margin")
)
# template=None only — no plotly_dark. Canvas controlled explicitly.
fig_zone = px.bar(
    zone_margin,
    x="zone",
    y="winning_margin",
    color_discrete_sequence=[GOLD],
)
_axis_title_font = dict(family="Goldman, sans-serif", size=14, color=GOLD)
_tick_font = dict(family="Goldman, sans-serif", size=12, color="#ffffff")
fig_zone.update_layout(
    template=None,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Goldman, sans-serif", color="#ffffff", size=13),
    font_color="#ffffff",
    showlegend=False,
    margin=dict(t=28, b=52, l=72, r=28),
    xaxis=dict(
        title=dict(text="Zone", font=_axis_title_font),
        tickfont=_tick_font,
        showgrid=False,
        linecolor="rgba(255,255,255,0.4)",
        zeroline=False,
    ),
    yaxis=dict(
        title=dict(
            text="Winning Margin (APC vs nearest rival)",
            font=dict(family="Goldman, sans-serif", size=13, color=GOLD),
        ),
        tickfont=_tick_font,
        showgrid=True,
        gridcolor="rgba(255,255,255,0.12)",
        gridwidth=1,
        zeroline=True,
        zerolinecolor="rgba(255,255,255,0.22)",
        zerolinewidth=1,
        linecolor="rgba(255,255,255,0.4)",
    ),
)
fig_zone.update_traces(marker=dict(color="#D4AF37", line=dict(width=0)))
st.plotly_chart(fig_zone, use_container_width=True)

_rose_heading("Corridor nodes — drill-down (774 LGAs)")
st.caption(
    "Choose a corridor, then a state. LGA roll-up ≈ one row every 0.5s (slow-mo); hover the marquee to pause. "
    "Canvasser budget = ₦30,000 × canvasser headcount per LGA."
)
_cor_cols = st.columns(6)
for _ci, (_abbr, _zname) in enumerate(CORRIDOR_NODES):
    with _cor_cols[_ci]:
        _nlg = int((dff["zone"] == _zname).sum())
        if st.button(
            f"{_abbr} · {_nlg}",
            key=f"cor_btn_{_abbr}",
            help=f"Geopolitical corridor — {_zname}. Click to drill down to states and LGAs.",
            use_container_width=True,
        ):
            st.session_state.corridor_zone = _zname
if st.session_state.corridor_zone is None:
    st.session_state._prev_corridor_state_key = None
    st.markdown(
        '<p class="rhgi-creed" style="margin-top:8px;">Select a corridor widget (NW · NE · NC · SW · SS · SE) to begin.</p>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        f'<p class="rhgi-corridor-gold-heading" style="font-size:1.12rem;margin-top:6px;">Active corridor · '
        f'<span style="color:#ffffff;">{html.escape(st.session_state.corridor_zone)}</span></p>',
        unsafe_allow_html=True,
    )
    _states_in_zone = sorted(dff[dff["zone"] == st.session_state.corridor_zone]["state"].unique())
    _sel_state = st.selectbox(
        "State (drill-down)",
        options=_states_in_zone,
        index=0,
        key=f"state_drill_{st.session_state.corridor_zone}",
    )
    _corridor_state_key = f"{st.session_state.corridor_zone}|{_sel_state}"
    _state_just_changed = st.session_state._prev_corridor_state_key != _corridor_state_key
    st.session_state._prev_corridor_state_key = _corridor_state_key
    _mat = build_state_lga_matrix_df(dff, _sel_state)
    _rows_html = []
    for _, _r in _mat.iterrows():
        _nm = html.escape(str(_r["LGA Name"]))
        _bud = int(_r["Canvasser Budget (₦30k anchor)"])
        _rows_html.append(
            "<tr>"
            f"<td>{_nm}</td>"
            f"<td>{int(_r['2023 Actual APC']):,}</td>"
            f"<td>{int(_r['2027 Sovereign Projection']):,}</td>"
            f"<td>{_r['Acceptance Velocity (%)']:.2f}</td>"
            f"<td>₦{_bud:,}</td>"
            "</tr>"
        )
    _tbody = "".join(_rows_html)
    _thead_html = (
        "<thead><tr>"
        "<th>LGA Name</th><th>2023 Actual APC</th><th>2027 Sovereign Projection</th>"
        "<th>Velocity %</th><th>Canvasser Budget (₦30k anchor)</th>"
        "</tr></thead>"
    )
    _nrows = len(_mat)
    if _nrows < 2:
        _tbl = (
            '<div class="rhgi-lga-scroll"><table class="rhgi-corridor-table">'
            f"{_thead_html}<tbody>{_tbody}</tbody></table></div>"
        )
    else:
        # ~1 row per 0.5s across one full LGA table scroll (marquee translates one table height)
        _roll_sec = max(3.0, min(480.0, _nrows * 0.5))
        if _state_just_changed:
            _roll_sec = max(_roll_sec, _nrows * 0.5 + 0.5)
        _roll_nonce = abs(hash(_corridor_state_key)) % 1_000_000
        _tbl = (
            f'<div class="rhgi-lga-scroll-outer" data-roll-key="{_roll_nonce}">'
            f'<div class="rhgi-lga-marquee" style="animation-duration:{_roll_sec:.0f}s;animation-name:rhgiSlowRoll;">'
            f'<table class="rhgi-corridor-table">{_thead_html}<tbody>{_tbody}</tbody></table>'
            f'<table class="rhgi-corridor-table">{_thead_html}<tbody>{_tbody}</tbody></table>'
            f"</div></div>"
        )
    st.markdown(_tbl, unsafe_allow_html=True)

_sb_base, _sb_after_misc, _sb_line_total = sovereign_budget_engine_breakdown()
_sb_line_bn = _sb_line_total / 1e9
_sb_mandate = SOVEREIGN_BUDGET_MANDATE_NGN
_sb_mandate_bn = _sb_mandate / 1e9
st.markdown(
    f"""
    <div class="rhgi-sovereign-budget">
      <div class="rhgi-sovereign-budget-inner">
        <h3>Sovereign Budget Engine — ₦{_sb_mandate_bn:,.2f}B</h3>
        <p class="rhgi-sovereign-mandate">₦{_sb_mandate:,}</p>
        <p class="rhgi-sovereign-detail">
          (144,000 canvassers + 144,000 E-day staff) × ₦30,000 → ₦{_sb_base/1e9:.2f}B;
          +15% misc → ₦{_sb_after_misc/1e9:.2f}B; +10% contingency → line-model subtotal <b>₦{_sb_line_total:,}</b> (₦{_sb_line_bn:.2f}B).
          RHGI sovereign headline total: <b>₦{_sb_mandate_bn:,.2f} billion</b>.
        </p>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

_gold_heading("774 LGA heatmap — winning margin (rugged)")
lga_map_df = build_lga_heatmap_df(dff)
lga_map_df["winning_margin"] = pd.to_numeric(lga_map_df["winning_margin"], errors="coerce")
lga_map_df = lga_map_df.dropna(subset=["lat", "lon", "winning_margin"])
wm = lga_map_df["winning_margin"].astype(float)
wm_min = float(wm.min()) if len(wm) else 0.0
wm_max = float(wm.max()) if len(wm) else 1.0
if wm_min == wm_max:
    wm_max = wm_min + 1.0
fig_lga = px.scatter_mapbox(
    lga_map_df,
    lat="lat",
    lon="lon",
    color="winning_margin",
    color_continuous_scale=[DEEP_NAVY_SAFE, "#2a4d7a", "#6b8fc9", METALLIC_GOLD_TARGET],
    range_color=(wm_min, wm_max),
    hover_name="lga",
    hover_data=["state", "zone", "margin_zone", "projected_total"],
    mapbox_style="carto-darkmatter",
    zoom=4.9,
    center={"lat": 9.082, "lon": 8.6753},
)
fig_lga.update_traces(marker=dict(size=8, opacity=0.8))
fig_lga.update_layout(
    template=None,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Goldman, sans-serif", color="#ffffff", size=13),
    font_color="#ffffff",
    margin=dict(l=0, r=0, t=12, b=0),
    coloraxis_colorbar=dict(
        title=dict(text="Winning margin", font=dict(family="Goldman, sans-serif", color=GOLD, size=12)),
        tickfont=dict(family="Goldman, sans-serif", color="#ffffff", size=11),
        bgcolor="rgba(0,0,51,0.55)",
        bordercolor="rgba(212,175,55,0.35)",
        len=0.72,
    ),
)
st.plotly_chart(fig_lga, use_container_width=True)

_gold_heading("Turnout heatmap — Nigeria (strike priority)")
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
)
fig_scatter.update_layout(
    template=None,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Goldman, sans-serif", color="#ffffff", size=13),
    font_color="#ffffff",
    margin=dict(l=0, r=0, t=12, b=0),
    coloraxis_colorbar=dict(
        title=dict(text="Strike priority", font=dict(family="Goldman, sans-serif", color=GOLD, size=12)),
        tickfont=dict(family="Goldman, sans-serif", color="#ffffff", size=11),
        bgcolor="rgba(0,0,51,0.55)",
        bordercolor="rgba(212,175,55,0.35)",
        len=0.72,
    ),
)
st.plotly_chart(fig_scatter, use_container_width=True)

_gold_heading("2023 vs 2027 Party Totals")
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
    color_discrete_map={"2023": "#b8962e", "2027": "#D4AF37"},
)
fig_party.update_layout(
    template=None,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Goldman, sans-serif", color="#ffffff", size=13),
    font_color="#ffffff",
    bargap=0.22,
    bargroupgap=0.08,
    legend=dict(
        title=dict(text="Year", font=dict(family="Goldman, sans-serif", color=GOLD, size=13)),
        font=dict(family="Goldman, sans-serif", color="#ffffff", size=12),
        bgcolor="rgba(0,0,51,0.5)",
        bordercolor="rgba(212,175,55,0.35)",
        borderwidth=1,
    ),
    xaxis=dict(
        title=dict(text="Party", font=_axis_title_font),
        tickfont=_tick_font,
        showgrid=False,
        linecolor="rgba(255,255,255,0.4)",
        zeroline=False,
    ),
    yaxis=dict(
        title=dict(text="Votes", font=dict(family="Goldman, sans-serif", size=14, color=GOLD)),
        tickfont=_tick_font,
        showgrid=True,
        gridcolor="rgba(255,255,255,0.12)",
        zerolinecolor="rgba(255,255,255,0.22)",
        linecolor="rgba(255,255,255,0.4)",
    ),
    margin=dict(t=36, b=48, l=72, r=36),
)
fig_party.update_traces(marker_line_width=0)
st.plotly_chart(fig_party, use_container_width=True)

_gold_heading("LGA Tactical Sheet (Logistics Alert)")
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
        "logistics_alert",
    ]
].copy()

view["winning_margin"] = view["winning_margin"].map(lambda x: f"{x:,.0f}")
view["canvasser_ratio"] = view["canvasser_ratio"].map(lambda x: f"{x:.2f}")
view["pvc_collection_rate"] = view["pvc_collection_rate"].map(lambda x: f"{x:.2%}")
view["turnout_2023_rate"] = view["turnout_2023_rate"].map(lambda x: f"{x:.2%}")

rows = []
for _, r in view.iterrows():
    css = "rhgi-pulse-logistics" if r["logistics_alert"] else ""
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
    "Showing first 200 LGAs. Gold-pulse rows: canvasser ratio below 1:16. "
    "Move the sidebar slider to watch winning margin and constitutional gauge update."
)

_ticker = (
    f"NATIONAL PROJECTION — APC votes {apc_national:,} · Total projected {projected_yield:,} · "
    f"APC share {national_apc_share:.2f}% · Legal Gatekeeper {states_25}/36 states ≥25% APC · "
    f"FCT APC {fct_pct:.2f}% · Remittance gap {remittance_gap:,} vs 20.7M anchor · "
    f"Turnout lift +{turnout_lift}% (live) · "
)
st.markdown(
    f"<div class='rhgi-ticker-wrap'><div class='rhgi-ticker'><span>{_ticker}</span><span>{_ticker}</span></div></div>",
    unsafe_allow_html=True,
)
