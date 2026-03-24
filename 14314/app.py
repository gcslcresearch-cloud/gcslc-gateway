import hashlib
import html
import pandas as pd
import plotly.express as px
import pytz
import streamlit as st
from datetime import datetime, time

from data_engine import ALL_LGA_RECORDS, STATE_COORDS, records_as_dicts

st.set_page_config(
    page_title="Renewed Hope Grassroots Initiatives — RHGI 774",
    layout="wide",
    initial_sidebar_state="expanded",
)
if "corridor_zone" not in st.session_state:
    st.session_state.corridor_zone = None
if "r8_note" not in st.session_state:
    st.session_state.r8_note = ""

# RHGI-GOLDMAN palette (mirrors :root CSS variables).
METALLIC_GOLD = "#D4AF37"
ROSE_GOLD = "#B76E79"
NAVY_CSS = "#000080"
GOLD = METALLIC_GOLD
NAVY = NAVY_CSS
# Prism Navy canvas + plot wells (Goldman corridor-27).
PRISM_NAVY = "#000080"
PRISM_NAVY_PLOT = "#0a0a5c"
CANVASSER_BUDGET_ANCHOR_NGN = 30_000
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


def _format_election_countdown(now: datetime) -> str:
    """Months : Days : Hours : Minutes : Seconds (30-day month units) until election anchor WAT."""
    now = now.astimezone(_LAGOS_TZ)
    tgt = ELECTION_DATETIME_WAT
    if now >= tgt:
        return "0 : 0 : 00 : 00 : 00 — verify certified INEC 2027 calendar."
    delta = tgt - now
    total_sec = int(delta.total_seconds())
    sec_per_month = 30 * 24 * 3600
    months = total_sec // sec_per_month
    rem = total_sec % sec_per_month
    days = rem // (24 * 3600)
    rem %= 24 * 3600
    h = rem // 3600
    rem %= 3600
    m = rem // 60
    s = rem % 60
    return f"{months} : {days} : {h:02d} : {m:02d} : {s:02d}"


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
      --rose-gold: #B76E79;
      --navy: #000080;
      --stark-white: #ffffff;
    }
    .stApp {
      background-color: var(--navy) !important;
      background-image: radial-gradient(ellipse at 20% 0%, rgba(212,175,55,0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 100%, rgba(183,110,121,0.06) 0%, transparent 45%) !important;
      color: var(--stark-white) !important;
      font-family: 'Goldman', sans-serif !important;
      user-select: none;
      -webkit-user-select: none;
    }
    [data-testid="stSidebar"] {
      background: linear-gradient(180deg, #000080 0%, #05054a 100%) !important;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] label { color: var(--stark-white) !important; }
    .block-container {
      font-size: 1.1rem;
      position: relative;
      z-index: 2 !important;
      font-family: 'Goldman', sans-serif !important;
      color: var(--stark-white) !important;
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
      text-shadow: 0 0 18px rgba(212, 175, 55, 0.95), 0 0 36px rgba(183, 110, 121, 0.45);
      box-shadow:
        0 0 36px rgba(212, 175, 55, 0.45),
        inset 0 0 28px rgba(212, 175, 55, 0.18);
      animation: emblemGoldPulse 2.8s ease-in-out infinite;
    }
    @keyframes emblemGoldPulse {
      0%, 100% { filter: brightness(1); box-shadow: 0 0 28px rgba(212,175,55,0.4); }
      50% { filter: brightness(1.15); box-shadow: 0 0 52px rgba(212,175,55,0.7); }
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
      color: var(--rose-gold) !important;
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
        repeating-linear-gradient(90deg, rgba(0,0,128,0.06) 0px, transparent 1px, transparent 14px),
        radial-gradient(ellipse at 30% 20%, rgba(212,175,55,0.04) 0%, transparent 55%);
      mix-blend-mode: soft-light;
      opacity: 0.92;
    }
    button, input, textarea, [data-testid="stMarkdownContainer"], .stMarkdown { user-select: text !important; -webkit-user-select: text !important; }
    div[data-testid="column"] button[kind="secondary"],
    div[data-testid="column"] button[kind="primary"] {
      position: relative !important;
      overflow: hidden !important;
      font-size: 1.06rem !important;
      font-weight: 700 !important;
      padding-top: 0.68rem !important;
      padding-bottom: 0.68rem !important;
      color: var(--metallic-gold) !important;
      border: 1px solid rgba(212, 175, 55, 0.55) !important;
      background: linear-gradient(155deg, rgba(0,0,128,0.45) 0%, #0b1024 55%, rgba(183,110,121,0.12) 100%) !important;
      background-size: 220% 100% !important;
      animation: r8MetalPulse 2.6s ease-in-out infinite, r8ShimmerSweep 2.8s linear infinite;
    }
    @keyframes r8MetalPulse {
      0%, 100% { box-shadow: 0 0 10px rgba(183,110,121,0.35); }
      50% { box-shadow: 0 0 26px rgba(212,175,55,0.45); }
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
      background: rgba(0, 0, 128, 0.22);
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
      background: rgba(0, 0, 128, 0.35);
    }
    .rhgi-kpi {
      padding: 12px 14px;
      border-radius: 10px;
      border: 1px solid rgba(183, 110, 121, 0.35);
      background: rgba(255, 255, 255, 0.06);
      font-family: 'Goldman', sans-serif !important;
    }
    .rhgi-pulse-red { animation: pulseRed 1s ease-in-out infinite; }
    @keyframes pulseRed {
      0%,100% { box-shadow: 0 0 0 rgba(255,0,0,0); }
      50% { box-shadow: 0 0 20px rgba(255,0,0,0.8); }
    }
    .rhgi-glow { color: var(--metallic-gold); text-shadow: 0 0 12px rgba(212,175,55,0.65); }
    .rhgi-gauge { font-size: 1.1rem; letter-spacing: 0.03em; }
    .rhgi-abuja-strobe {
      border: 2px solid rgba(220, 40, 40, 0.95) !important;
      animation: diamondStrobe 0.85s ease-in-out infinite;
    }
    @keyframes diamondStrobe {
      0%, 100% { box-shadow: 0 0 4px rgba(255, 0, 0, 0.35); }
      50% { box-shadow: 0 0 22px rgba(255, 0, 0, 0.95); }
    }
    .rhgi-8r-stealth {
      font-size: 1.05rem;
      font-weight: 800;
      letter-spacing: 0.28em;
      text-transform: uppercase;
      color: #e8ecff;
      text-shadow: 0 0 14px rgba(212,175,55,0.55), 0 0 28px rgba(0,0,128,0.55);
      margin: 8px 0 6px 0;
    }
    .rhgi-mandate-secured {
      text-align: center;
      padding: 14px 18px;
      margin: 12px 0 16px 0;
      border-radius: 12px;
      border: 3px solid var(--metallic-gold);
      background: linear-gradient(180deg, rgba(11,16,36,0.95), rgba(26,35,126,0.35));
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
      background: #000080;
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
      margin: 0.5rem 0 0.35rem 0; text-shadow: 0 0 12px rgba(212,175,55,0.45); letter-spacing: 0.02em; }
    .stApp h1 { color: var(--metallic-gold) !important; font-weight: 800 !important; text-shadow: 0 0 14px rgba(212,175,55,0.4); }
    .rhgi-corridor-table { width: 100%; border-collapse: collapse; font-size: 1.14rem; line-height: 1.55; }
    .rhgi-corridor-table th {
      color: var(--metallic-gold) !important; font-weight: 800 !important;
      text-align: left; padding: 14px 16px;
      background: rgba(0, 0, 128, 0.45);
      border-bottom: 2px solid rgba(212, 175, 55, 0.5);
      text-shadow: 0 0 8px rgba(212, 175, 55, 0.4);
      font-size: 1.12rem !important;
    }
    .rhgi-corridor-table td {
      color: #ffffff !important; padding: 12px 16px;
      border-bottom: 1px solid rgba(212, 175, 55, 0.15);
      font-size: 1.1rem !important;
      font-weight: 500;
    }
    .rhgi-corridor-table tr:nth-child(even) td { background: rgba(14, 23, 51, 0.45); }
    [data-testid="stCaption"] { color: var(--rose-gold) !important; font-family: 'Goldman', sans-serif !important; }
    [data-testid="stSelectbox"] label { color: var(--rose-gold) !important; font-family: 'Goldman', sans-serif !important; }
    [data-baseweb="select"] { font-family: 'Goldman', sans-serif !important; }
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
      <h1 class="rhgi-brand-title">Renewed Hope Grassroots Initiatives</h1>
      <div class="rhgi-emblem-wrap"><div class="rhgi-emblem">RHGI</div></div>
      <p class="rhgi-countdown-keys">Months : Days : Hours : Minutes : Seconds (WAT) → Feb 2027</p>
      <div class="rhgi-countdown-meter">{_countdown_line}</div>
      <p class="rhgi-creed">This sovereign dashboard decodes the 2027 elections with scientific, uncorruptible precision. Powered by the 8R Stealth Paradigm Convergence and its Determinants.</p>
      <p class="rhgi-signature">Prepared by Galadiman Ruwa Center for Strategic Leadership and Communication GCSLC LTD/GTE.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
_r8_cols = st.columns(8)
for _ri, (_r8_label, _r8_det) in enumerate(EIGHT_R_DETERMINANTS):
    with _r8_cols[_ri]:
        if st.button(_r8_label, key=f"r8_btn_{_ri}", use_container_width=True):
            st.session_state.r8_note = _r8_det
if st.session_state.r8_note:
    st.info(st.session_state.r8_note)

c1, c2, c3 = st.columns(3)
# Abuja Pulse lead (UTC+1); Diamond Strobe when FCT projected APC < 25%.
_pulse_cls = "rhgi-kpi rhgi-abuja-strobe" if abuja_strobe else "rhgi-kpi"
c1.markdown(
    f"<div class='{_pulse_cls}'><b>Abuja Pulse (UTC+1)</b><br><span class='rhgi-glow'>{abuja_now.strftime('%I:%M:%S %p WAT')}</span>"
    f"<br><small style='color:#aab8e0'>FCT APC (proj): {fct_pct:.2f}%</small></div>",
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
        "<small style='color:#c8d4f8;'>Legal Gatekeeper — ≥24 of 36 states at ≥25% APC and FCT ≥25%</small></div>",
        unsafe_allow_html=True,
    )

_gold_heading("Winning Margin by Geopolitical Zone (turnout-adjusted)")
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
fig_zone.update_traces(marker=dict(color=GOLD))
st.plotly_chart(fig_zone, use_container_width=True)

_gold_heading("Corridor nodes — drill-down (774 LGAs)")
st.caption(
    "Choose a corridor, then a state. Canvasser budget = ₦30,000 × canvasser headcount per LGA. "
    "Velocity % = (2027 APC − 2023 APC) ÷ 2023 APC × 100. Large LGA roll-ups scroll slowly; hover to pause."
)
_cor_cols = st.columns(6)
for _ci, (_abbr, _zname) in enumerate(CORRIDOR_NODES):
    with _cor_cols[_ci]:
        _nlg = int((dff["zone"] == _zname).sum())
        if st.button(f"{_abbr} · {_nlg}", key=f"cor_btn_{_abbr}", use_container_width=True):
            st.session_state.corridor_zone = _zname
if st.session_state.corridor_zone is None:
    st.markdown(
        '<p class="rhgi-creed" style="margin-top:8px;">Select a corridor widget (NW · NE · NC · SW · SS · SE) to begin.</p>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        f'<p class="rhgi-gold-heading" style="font-size:1.1rem;">Active corridor: '
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
    if _nrows <= 4:
        _tbl = (
            '<div class="rhgi-lga-scroll"><table class="rhgi-corridor-table">'
            f"{_thead_html}<tbody>{_tbody}</tbody></table></div>"
        )
    else:
        _roll_sec = max(90.0, min(520.0, _nrows * 2.75))
        _tbl = (
            f'<div class="rhgi-lga-scroll-outer"><div class="rhgi-lga-marquee" '
            f'style="animation-duration:{_roll_sec:.0f}s;">'
            f'<table class="rhgi-corridor-table">{_thead_html}<tbody>{_tbody}</tbody></table>'
            f'<table class="rhgi-corridor-table">{_thead_html}<tbody>{_tbody}</tbody></table>'
            f"</div></div>"
        )
    st.markdown(_tbl, unsafe_allow_html=True)

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
    template="plotly_dark",
    title="774 LGAs — winning margin (deep navy → metallic gold)",
)
fig_lga.update_traces(marker=dict(size=8, opacity=0.8))
fig_lga.update_layout(
    paper_bgcolor=PRISM_NAVY,
    plot_bgcolor=PRISM_NAVY,
    font_color="#dbe2ff",
    margin=dict(l=0, r=0, t=48, b=0),
    coloraxis_colorbar=dict(title="Winning margin"),
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
    template="plotly_dark",
    title="High PVC + low 2023 turnout → metallic gold (high-priority strike zones)",
)
fig_scatter.update_layout(
    paper_bgcolor=PRISM_NAVY,
    plot_bgcolor=PRISM_NAVY,
    font_color="#dbe2ff",
    margin=dict(l=0, r=0, t=40, b=0),
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
    color_discrete_map={"2023": NAVY, "2027": GOLD},
    template="plotly_dark",
)
fig_party.update_layout(
    paper_bgcolor=PRISM_NAVY,
    plot_bgcolor=PRISM_NAVY_PLOT,
    font_color="#dbe2ff",
)
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
