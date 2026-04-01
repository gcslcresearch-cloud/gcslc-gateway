# CIEN Kaduna 2027 — Galadiman Ruwa Center (GCSLC LTD/GTE)
# Run: python3 -m streamlit run cien_kaduna_2027.py --server.port 9099

from __future__ import annotations

import html
import os
import random
import time
import urllib.parse
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

os.environ.setdefault("STREAMLIT_SERVER_PORT", "9099")
os.environ.setdefault("STREAMLIT_SERVER_FILE_WATCHER_TYPE", "none")

BASE_DIR = Path(__file__).resolve().parent
VOTER_DB_CSV = Path(os.environ.get("GCSLC_VOTER_DB", str(BASE_DIR / "voter_db.csv")))

# Executive Test Module — Node 0 (Chairman) / Node 1 (His Excellency); override via env or UI
DEFAULT_EXEC_NODE0 = float(os.environ.get("GCSLC_EXEC_NODE0", "14314"))
DEFAULT_EXEC_NODE1 = float(os.environ.get("GCSLC_EXEC_NODE1", "8507"))

EXECUTIVE_BRIEFING_WHATSAPP = (
    "The CIEN Kaduna 2027 Command Center is active. This digital fortress is built to ensure our 15/15 victory "
    "through precision and detail. Standing by for your sovereign signal. "
    "— Dr. Jaafaru Sa'ad (Galadiman Ruwa)"
)
# Single URL-encode of the briefing for ?text= (phone paths below are fixed literals; no digit math).
_EXEC_BRIEFING_TEXT_ENCODED = urllib.parse.quote(EXECUTIVE_BRIEFING_WHATSAPP, safe="")
# Full hrefs: https://wa.me/[DIGITS]?text=… — digits contiguous, no + or spaces in the number segment.
WA_ME_HREF_NODE0_CHAIRMAN = "https://wa.me/2348099111515?text=" + _EXEC_BRIEFING_TEXT_ENCODED
WA_ME_HREF_NODE1_EXECUTIVE = "https://wa.me/2348099111119?text=" + _EXEC_BRIEFING_TEXT_ENCODED
WA_ME_HREF_NODE2_VALIDATOR = "https://wa.me/2348037649077?text=" + _EXEC_BRIEFING_TEXT_ENCODED
WA_ME_HREF_NODE3_CONTROL = "https://wa.me/2348079000900?text=" + _EXEC_BRIEFING_TEXT_ENCODED


def _executive_wa_gateway_sidebar_html() -> str:
    """Galadima Center: four stacked wa.me links; hrefs are module-level literals + encoded briefing only."""
    u0 = html.escape(WA_ME_HREF_NODE0_CHAIRMAN, quote=True)
    u1 = html.escape(WA_ME_HREF_NODE1_EXECUTIVE, quote=True)
    u2 = html.escape(WA_ME_HREF_NODE2_VALIDATOR, quote=True)
    u3 = html.escape(WA_ME_HREF_NODE3_CONTROL, quote=True)
    return f"""
<div class="wa-gateway-wrap"><div class="wa-gateway-inner">
  <p class="wa-galadima-header">Galadima Center</p>
  <p class="wa-gateway-sub">Executive WhatsApp Gateway</p>
  <div class="wa-gateway-btn-stack">
    <a class="wa-sidebar-wa-link" href="{u0}" target="_blank" rel="noopener noreferrer">SEND BRIEFING · NODE 0 (Chairman)</a>
    <a class="wa-sidebar-wa-link" href="{u1}" target="_blank" rel="noopener noreferrer">SEND BRIEFING · NODE 1 (Executive)</a>
    <a class="wa-sidebar-wa-link" href="{u2}" target="_blank" rel="noopener noreferrer">SEND BRIEFING · NODE 2 (Validator)</a>
    <a class="wa-sidebar-wa-link" href="{u3}" target="_blank" rel="noopener noreferrer">SEND BRIEFING · NODE 3 (Control)</a>
  </div>
  <p class="wa-safety-protocol">Safety: these four nodes are the only active outbound briefing targets until you manually authorize &quot;PUSH TO 1.5M NODES&quot;.</p>
  <p class="wa-env-hint">WhatsApp targets are fixed in source (no env override).</p>
</div></div>
"""

NAVY_DEEP = "#000033"
GOLD = "#D4AF37"
CYAN = "#00E5FF"
TURQ = "#2DD4BF"


def _tactical_bolt_svg_data_url() -> str:
    """High-visibility Material-style bolt for collapsed sidebar (S24 / devices without emoji fonts)."""
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" role="img" aria-label="Tactical alert">'
        '<path fill="#FFD700" d="M11 21h-1l1-7H7.5c-.58 0-.57-.32-.38-.66l.08-.14C8.48 10.94 '
        "10.42 7.54 13 3h1l-1 7h3.5c.49 0 .56.33.47.51l-.07.15C12.96 17.55 11 21 11 21z"
        '"/></svg>'
    )
    return "data:image/svg+xml," + urllib.parse.quote(svg)

ORG_NAME = "Galadiman Ruwa Center for Strategic Leadership and Communication LTD/GTE"
CHAIRMAN_LINE = "Chairman: Galadimanruwa"
COMMANDER_LINE = "Commander: Galadiman Ruwa"
MOTTO = (
    "We decode the Kaduna 2027 election based on our superior 15/15 scientific model."
)

# Timing hub — sovereign strike dates
GUBER_PRIMARIES_DATE = date(2026, 4, 23)
GENERAL_ELECTION_2027_DATE = date(2027, 2, 6)

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


# 8R Stealth Paradigm — full paradigm copy + clinical-audit proprietary determinant (on demand)
PARADIGMS_8R: list[dict[str, str]] = [
    {
        "id": "R1",
        "title": "Reach Density",
        "paradigm": (
            "Polling-unit proximity grids weighted by the 1.5M verified voter pool — contact depth "
            "mapped to turnout elasticity, ward heat, and nodal strength so outreach lands where "
            "ballot leverage is highest."
        ),
        "proprietary": (
            "Clinical audit · Proprietary Determinant — REFINE: Recalibrate reach matrices against "
            "live PU density; drop cold corridors; elevate 15/15 validation lanes only."
        ),
    },
    {
        "id": "R2",
        "title": "Resource Alignment",
        "paradigm": (
            "Executive-Load-142 cadence synchronized to nodal strength so spend, transport, and "
            "comms follow ballot-box leverage rather than vanity geographies."
        ),
        "proprietary": (
            "Clinical audit · Proprietary Determinant — RESET: Zero-base the field budget to PU ROI; "
            "re-issue strike packs per LGA command grid."
        ),
    },
    {
        "id": "R3",
        "title": "Reputation Capital",
        "paradigm": (
            "Incumbency delivery narratives reinforced by third-party validators in high-trust "
            "community nodes — evidence-led messaging that survives rival counter-spin."
        ),
        "proprietary": (
            "Clinical audit · Proprietary Determinant — RE-ANCHOR: Re-bind narrative to audited "
            "outcomes; purge stale talking points from the clinical comms runbook."
        ),
    },
    {
        "id": "R4",
        "title": "Rival Neutralization",
        "paradigm": (
            "Counter-messaging lanes that collapse opposition fragmentation without amplifying "
            "their frames — disciplined escalation and observer-ready documentation."
        ),
        "proprietary": (
            "Clinical audit · Proprietary Determinant — RECONCILE: Map rival narratives to "
            "fact-check packets; hold formation until nodal command authorizes release."
        ),
    },
    {
        "id": "R5",
        "title": "Rally Cadence",
        "paradigm": (
            "Rhythmic mobilization from weekly pulses through election hour — logistics rehearsal, "
            "observer coverage, and turnout covenant discipline in every ward cell."
        ),
        "proprietary": (
            "Clinical audit · Proprietary Determinant — REINFORCE: Compress cadence to daily "
            "readiness inside T-14; rehearse PU arrival and 15/15 validation drill."
        ),
    },
    {
        "id": "R6",
        "title": "Resilience & Compliance",
        "paradigm": (
            "Incident escalation, data hygiene, and audit-ready reporting for field integrity — "
            "D6 compliance lane aligned to sovereign gateway and mobile stream security."
        ),
        "proprietary": (
            "Clinical audit · Proprietary Determinant — REGISTER: Log every incident with time-stamp "
            "and PU reference; seal chain-of-custody before DG/RHGI review."
        ),
    },
    {
        "id": "R7",
        "title": "Recognition Systems",
        "paradigm": (
            "High-performing cells receive visibility, data access, and repeatable playbooks — "
            "reward loops that scale winning behaviors across the 23 LGAs."
        ),
        "proprietary": (
            "Clinical audit · Proprietary Determinant — REPLICATE: Clone top-quartile ward SOPs "
            "into adjacent nodes with Executive-Load-142 handshake verification."
        ),
    },
    {
        "id": "R8",
        "title": "Replication Runbooks",
        "paradigm": (
            "Standard operating packages per LGA so 18/25 nodal targets scale without drift — "
            "one sovereign doctrine, many localized execution threads."
        ),
        "proprietary": (
            "Clinical audit · Proprietary Determinant — RE-CERTIFY: Re-run clinical audit on each "
            "runbook version; no field deployment without RHGI sign-off."
        ),
    },
]

def _normalize_voter_df(raw: pd.DataFrame) -> pd.DataFrame:
    if raw.empty:
        return pd.DataFrame(columns=["first_name", "last_name", "lga", "number"])
    norm = {str(c).strip().lower().replace(" ", "_"): c for c in raw.columns}

    def col(*candidates: str) -> str | None:
        for k in candidates:
            if k in norm:
                return norm[k]
        return None

    c_fn = col("first_name", "firstname", "fname")
    c_ln = col("last_name", "lastname", "surname", "lname")
    c_lga = col("lga", "lga_name", "ward_lga")
    c_num = col("number", "phone", "msisdn", "phone_number")
    if not (c_fn and c_ln and c_lga):
        return pd.DataFrame(columns=["first_name", "last_name", "lga", "number"])
    out = pd.DataFrame(
        {
            "first_name": raw[c_fn].astype(str).fillna(""),
            "last_name": raw[c_ln].astype(str).fillna(""),
            "lga": raw[c_lga].astype(str).fillna(""),
            "number": raw[c_num].astype(str).fillna("") if c_num else "",
        }
    )
    return out[out["first_name"].str.len() > 0]


@st.cache_data(show_spinner="Ingesting voter_db.csv…")
def _load_voter_db(csv_path: str) -> pd.DataFrame:
    p = Path(csv_path)
    if not p.is_file():
        return pd.DataFrame(columns=["first_name", "last_name", "lga", "number"])
    try:
        raw = pd.read_csv(p)
    except Exception:
        return pd.DataFrame(columns=["first_name", "last_name", "lga", "number"])
    return _normalize_voter_df(raw)

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
@keyframes gold-title-shimmer {
  0% { background-position: 0% center; }
  100% { background-position: 200% center; }
}
@keyframes cyan-slow-pulse {
  0%, 100% {
    opacity: 1;
    color: #00E5FF !important;
    text-shadow: 0 0 6px rgba(0, 229, 255, 0.35), 0 0 14px rgba(0, 229, 255, 0.2);
  }
  50% {
    opacity: 0.78;
    color: #7df9ff !important;
    text-shadow: 0 0 12px rgba(0, 229, 255, 0.65), 0 0 22px rgba(0, 229, 255, 0.35);
  }
}
@keyframes sovereign-breathe {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(0.8); }
}
@keyframes clock-line-pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.82; }
}
@keyframes sim-scroll {
  0% { transform: translateY(0); }
  100% { transform: translateY(-50%); }
}
@keyframes logistics-feed-scroll {
  0% { transform: translateY(0); }
  100% { transform: translateY(-50%); }
}
@keyframes sentiment-bar-pulse {
  0%, 100% { filter: brightness(1) drop-shadow(0 0 6px rgba(45, 212, 191, 0.35)); }
  50% { filter: brightness(1.12) drop-shadow(0 0 14px rgba(45, 212, 191, 0.65)); }
}

/* Sidebar — Matte Charcoal + high-contrast gold / bright cyan (S24 / no ghosting) */
[data-testid="stSidebar"] {
  background-color: #121212 !important;
  background-image: none !important;
  border-right: 1px solid rgba(255, 215, 0, 0.22) !important;
}
[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
  background-color: #121212 !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] h5,
[data-testid="stSidebar"] h6 {
  color: #FFD700 !important;
  font-weight: 700 !important;
  text-shadow: none !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] label,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] span,
[data-testid="stSidebar"] [data-testid="stMetricLabel"] *,
[data-testid="stSidebar"] [data-testid="stMetricValue"] * {
  color: #FFD700 !important;
  font-weight: 700 !important;
  -webkit-font-smoothing: antialiased !important;
  -moz-osx-font-smoothing: grayscale !important;
  text-rendering: geometricPrecision !important;
  text-shadow: none !important;
  opacity: 1 !important;
}
[data-testid="stSidebar"] a,
[data-testid="stSidebar"] a:visited {
  color: #00F5FF !important;
  font-weight: 700 !important;
  text-shadow: none !important;
}
[data-testid="stSidebar"] .status-live,
[data-testid="stSidebar"] .status-synced {
  color: #00F5FF !important;
  text-shadow: none !important;
}
[data-testid="stSidebar"] textarea,
[data-testid="stSidebar"] input {
  color: #FFD700 !important;
  font-weight: 600 !important;
  background-color: #1a1a1a !important;
  border-color: rgba(255, 215, 0, 0.35) !important;
  -webkit-text-fill-color: #FFD700 !important;
}
[data-testid="stSidebar"] .stButton button {
  font-weight: 700 !important;
}
[data-testid="stSidebar"] [data-testid="stLinkButton"] a {
  color: #00F5FF !important;
  font-weight: 700 !important;
  text-decoration: none !important;
  border: 1px solid rgba(0, 245, 255, 0.45) !important;
  border-radius: 8px !important;
  padding: 0.35rem 0.5rem !important;
  display: block !important;
  text-align: center !important;
  background: rgba(26, 26, 26, 0.95) !important;
}
[data-testid="stSidebar"] [data-testid="stLinkButton"] {
  margin-bottom: 0.35rem !important;
}

html, body, [data-testid="stAppViewContainer"] {
  font-family: 'Goldman', sans-serif !important;
  background-color: #000033 !important;
  color: #D4AF37 !important;
}
.stApp, [data-testid="stAppViewContainer"] {
  background: linear-gradient(180deg, #000022 0%, #000033 55%, #000044 100%) !important;
}
/* Commander-level: clear Streamlit chrome overlap on title stack */
header[data-testid="stHeader"] {
  background: linear-gradient(180deg, rgba(0,0,34,0.97) 0%, rgba(0,0,51,0.88) 100%) !important;
  border-bottom: 1px solid rgba(212, 175, 55, 0.25) !important;
}
[data-testid="stDecoration"] { display: none !important; }
.block-container {
  padding-top: 3.25rem !important;
  padding-bottom: 1.4rem !important;
}
@media (max-width: 768px) {
  .block-container {
    padding-top: 3.5rem !important;
    padding-left: 0.65rem !important;
    padding-right: 0.65rem !important;
  }
  /* S24 / iPhone: stack all Streamlit horizontal bands (Senatorial, 8R rows, Timing Strike, etc.) */
  [data-testid="stHorizontalBlock"] {
    flex-direction: column !important;
    flex-wrap: nowrap !important;
    gap: 0.45rem !important;
    align-items: stretch !important;
    width: 100% !important;
  }
  [data-testid="stHorizontalBlock"] > [data-testid="column"] {
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
    flex: 0 0 auto !important;
  }
  /* Winner/Loser donut: centered, ~90% viewport width; map chart resets below */
  [data-testid="stPlotlyChart"] {
    width: 90vw !important;
    max-width: 90vw !important;
    margin-left: auto !important;
    margin-right: auto !important;
    display: block !important;
  }
  [data-testid="stPlotlyChart"] ~ [data-testid="stPlotlyChart"] {
    width: 100% !important;
    max-width: 100% !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
  }
  .cien-title {
    font-size: clamp(0.74rem, 3.6vw, 1.08rem) !important;
    letter-spacing: 0.02em !important;
    line-height: 1.28 !important;
  }
  .cien-motto { font-size: 0.64rem !important; line-height: 1.42 !important; }
  .cien-foundation { font-size: 0.58rem !important; letter-spacing: 0.05em !important; }
  .cien-chairman, .cien-commander { font-size: 0.68rem !important; }
  .section-prism h3 { font-size: 0.92rem !important; }
  .r8-shimmer-inner { min-height: 0 !important; }
  .r8-body { font-size: 0.62rem !important; }
  .r8-name { font-size: 0.76rem !important; }
  .timing-count { font-size: 0.82rem !important; }
  .outreach-command-inner h3 { font-size: 0.88rem !important; }
  .sim-feed-outer { height: 140px !important; }
  .sim-feed-line { font-size: 0.62rem !important; padding: 0.32rem 0.5rem !important; }
  .logistics-feed-outer { height: 160px !important; }
  .logistics-line { font-size: 0.6rem !important; padding: 0.3rem 0.45rem !important; }
  /* Global clocks: 2×2 grid to save vertical space */
  .clock-grid {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 0.25rem 0.35rem !important;
  }
  .clock-line {
    flex-direction: column !important;
    align-items: flex-start !important;
    gap: 0.06rem !important;
    font-size: 0.56rem !important;
    border: 1px solid rgba(212, 175, 55, 0.12) !important;
    border-bottom: 3px solid #FFD700 !important;
    border-radius: 6px !important;
    padding: 0.2rem 0.28rem !important;
    margin: 0 !important;
    box-sizing: border-box !important;
  }
  .clock-line span:last-child {
    font-size: 0.52rem !important;
    word-break: break-word;
  }
  .sovereign-clock-inner { min-height: 0 !important; padding: 0.45rem 0.5rem !important; }
  /* Main canvas: crisp type on OLED (no ghosted halos on body copy) */
  .main [data-testid="stMarkdownContainer"] p,
  .main [data-testid="stMarkdownContainer"] h1,
  .main [data-testid="stMarkdownContainer"] h2,
  .main [data-testid="stMarkdownContainer"] h3,
  .main [data-testid="stMarkdownContainer"] h4,
  .main [data-testid="stMarkdownContainer"] li,
  .main [data-testid="stMarkdownContainer"] span,
  .main [data-testid="stCaption"],
  .main [data-testid="stMetricLabel"] *,
  .main [data-testid="stMetricValue"] * {
    text-shadow: none !important;
  }
}

/* Collapsed sidebar: SVG bolt (S24 / emoji-safe) */
@keyframes tactical-bolt-pulse {
  0%, 100% { opacity: 1; transform: scale(1); filter: drop-shadow(0 0 4px rgba(255, 215, 0, 0.9)); }
  50% { opacity: 0.72; transform: scale(1.14); filter: drop-shadow(0 0 10px rgba(0, 229, 255, 0.55)); }
}
[data-testid="collapsedControl"] {
  position: relative !important;
}
[data-testid="collapsedControl"]::after {
  content: "" !important;
  position: absolute;
  top: -4px;
  right: -4px;
  width: 17px;
  height: 17px;
  background: url("__TACTICAL_BOLT_SVG__") center / contain no-repeat;
  animation: tactical-bolt-pulse 1.65s ease-in-out infinite;
  pointer-events: none;
}
@media (min-width: 769px) {
  [data-testid="collapsedControl"]::after {
    width: 19px;
    height: 19px;
    top: -5px;
    right: -5px;
  }
}

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
  font-size: clamp(1.05rem, 2.9vw, 1.5rem);
  letter-spacing: 0.04em;
  margin: 0 0 0.45rem 0;
  text-align: center;
  line-height: 1.35;
  background: linear-gradient(
    90deg,
    #8a6a00 0%,
    #FFD700 22%,
    #fff8dc 42%,
    #FFD700 58%,
    #b8860b 78%,
    #FFD700 100%
  );
  background-size: 220% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gold-title-shimmer 5s linear infinite;
  filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.35));
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
.cien-chairman {
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.78rem;
  font-weight: 700;
  text-align: center;
  margin: 0 0 0.25rem 0;
  letter-spacing: 0.06em;
  animation: cyan-slow-pulse 5.5s ease-in-out infinite;
}
.cien-commander {
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.74rem;
  text-align: center;
  margin: 0 0 0.55rem 0;
  letter-spacing: 0.05em;
  animation: cyan-slow-pulse 5.5s ease-in-out infinite;
  animation-delay: 0.75s;
}

.timing-prism {
  border-radius: 14px;
  padding: 3px;
  background: linear-gradient(120deg, #000033, #D4AF37, #00e5ff, #000033);
  background-size: 280% 100%;
  animation: prism-shimmer 14s linear infinite;
  margin-bottom: 0.65rem;
  height: 100%;
}
.timing-prism-inner {
  background: linear-gradient(180deg, #000011 0%, #000044 100%);
  border-radius: 11px;
  padding: 0.75rem 0.85rem;
  border: 1px solid rgba(212, 175, 55, 0.4);
  min-height: 118px;
}
.timing-prism-inner h4 {
  font-family: 'Goldman', sans-serif !important;
  color: #FFD700 !important;
  margin: 0 0 0.45rem 0;
  font-size: 0.82rem;
  letter-spacing: 0.06em;
  text-align: center;
}
.timing-count {
  font-family: 'Goldman', sans-serif !important;
  color: #00E5FF !important;
  font-size: 0.95rem;
  font-weight: 700;
  text-align: center;
  line-height: 1.35;
  font-variant-numeric: tabular-nums;
}
.timing-sub {
  font-family: 'Goldman', sans-serif !important;
  color: rgba(212, 175, 55, 0.85) !important;
  font-size: 0.68rem;
  text-align: center;
  margin-top: 0.35rem;
  letter-spacing: 0.04em;
}

.timing-shimmer {
  border-radius: 14px;
  padding: 3px;
  background: linear-gradient(120deg, #2a2a3a, #FFD700, #D4AF37, #00e5ff, #2a2a3a);
  background-size: 320% 100%;
  animation: prism-shimmer 5s linear infinite;
  margin-bottom: 0.65rem;
  height: 100%;
}
.timing-shimmer-inner {
  background: linear-gradient(180deg, #0a0a18 0%, #12122a 100%);
  border-radius: 11px;
  padding: 0.75rem 0.85rem;
  border: 1px solid rgba(255, 215, 0, 0.45);
  min-height: 118px;
}
.timing-shimmer-inner h4 {
  font-family: 'Goldman', sans-serif !important;
  color: #D4AF37 !important;
  margin: 0 0 0.45rem 0;
  font-size: 0.82rem;
  letter-spacing: 0.05em;
  text-align: center;
}

.sovereign-clock-box {
  border-radius: 14px;
  padding: 3px;
  background: linear-gradient(120deg, #000033, #00e5ff, #D4AF37, #000033);
  background-size: 260% 100%;
  animation: prism-shimmer 9s linear infinite;
  margin-bottom: 0.65rem;
  height: 100%;
}
.sovereign-clock-inner {
  background: linear-gradient(180deg, #000011 0%, #000044 100%);
  border-radius: 11px;
  padding: 0.55rem 0.65rem;
  border: 1px solid rgba(0, 229, 255, 0.35);
  min-height: 152px;
}
.sovereign-clock-inner h4 {
  font-family: 'Goldman', sans-serif !important;
  color: #FFD700 !important;
  margin: 0 0 0.4rem 0;
  font-size: 0.78rem;
  letter-spacing: 0.08em;
  text-align: center;
  animation: clock-line-pulse 3s ease-in-out infinite;
}
.clock-grid {
  display: block;
}
.clock-line {
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.68rem;
  color: #00E5FF !important;
  display: flex;
  justify-content: space-between;
  gap: 0.35rem;
  padding: 0.1rem 0;
  border-bottom: 1px solid rgba(212, 175, 55, 0.12);
  animation: clock-line-pulse 2.8s ease-in-out infinite;
}
.clock-line:nth-child(2) { animation-delay: 0.2s; }
.clock-line:nth-child(3) { animation-delay: 0.4s; }
.clock-line:nth-child(4) { animation-delay: 0.6s; }
.clock-line:nth-child(5) { animation-delay: 0.8s; }
.clock-line span:last-child {
  font-variant-numeric: tabular-nums;
  color: #D4AF37 !important;
}

/* Winner/Loser donut — breathe first Plotly only (map chart follows later) */
div[data-testid="stPlotlyChart"] {
  transform-origin: center center;
  animation: sovereign-breathe 5.5s ease-in-out infinite;
}
div[data-testid="stPlotlyChart"] ~ div[data-testid="stPlotlyChart"] {
  animation: none !important;
  transform: none !important;
}

.direct-tactical-wrap {
  border-radius: 12px;
  padding: 3px;
  background: linear-gradient(120deg, #000033, #D4AF37, #000033);
  background-size: 240% 100%;
  animation: prism-shimmer 11s linear infinite;
  margin-bottom: 0.85rem;
}
.direct-tactical-inner {
  background: linear-gradient(180deg, #000011 0%, #000033 100%);
  border-radius: 9px;
  padding: 0.75rem 0.65rem;
  border: 1px solid rgba(212, 175, 55, 0.38);
}
.direct-tactical-inner h4 {
  font-family: 'Goldman', sans-serif !important;
  color: #FFD700 !important;
  margin: 0 0 0.5rem 0;
  font-size: 0.85rem;
  text-align: center;
  letter-spacing: 0.06em;
}
.dt-verified {
  font-family: 'Goldman', sans-serif !important;
  color: #D4AF37 !important;
  font-size: 0.72rem;
  text-align: center;
  margin: 0 0 0.35rem 0;
}
.dt-verified strong { color: #FFD700 !important; font-size: 1.05em; }
.dt-ticker {
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.68rem;
  color: #2DD4BF !important;
  text-align: center;
  letter-spacing: 0.06em;
  margin: 0 0 0.45rem 0;
  text-shadow: 0 0 10px rgba(45, 212, 191, 0.55);
  animation: cien-pulse-gold 2.5s ease-in-out infinite;
}
.dt-handshake {
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.66rem;
  color: #00E5FF !important;
  line-height: 1.45;
  border-top: 1px solid rgba(0, 229, 255, 0.2);
  padding-top: 0.45rem;
  margin: 0;
  text-align: center;
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
  transform-origin: center center;
  animation: sovereign-breathe 5.5s ease-in-out 0.45s infinite;
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
  width: var(--cien-twothirds-pct, 69.57%);
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

.r8-shimmer-grid {
  border-radius: 14px;
  padding: 3px;
  background: linear-gradient(120deg, #001a33, #1e5a8c, #00e5ff, #1e5a8c, #001a33);
  background-size: 280% 100%;
  animation: prism-shimmer 8s linear infinite;
  margin-bottom: 0.55rem;
  box-shadow:
    0 0 18px rgba(30, 100, 200, 0.45),
    0 0 32px rgba(0, 229, 255, 0.12);
}
.r8-shimmer-inner {
  background: linear-gradient(180deg, #050518 0%, #0a1530 100%);
  border-radius: 11px;
  padding: 0.65rem 0.7rem;
  border: 1px solid rgba(80, 160, 255, 0.55);
  box-shadow:
    inset 0 0 14px rgba(0, 120, 255, 0.12),
    0 0 12px rgba(0, 80, 200, 0.25);
  min-height: 11.5rem;
}
.r8-id {
  font-family: 'Goldman', sans-serif !important;
  color: #5eb3ff !important;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  margin: 0 0 0.2rem 0;
}
.r8-name {
  font-family: 'Goldman', sans-serif !important;
  color: #FFD700 !important;
  font-size: 0.82rem;
  font-weight: 700;
  margin: 0 0 0.35rem 0;
  letter-spacing: 0.04em;
}
.r8-body {
  font-family: 'Goldman', sans-serif !important;
  color: rgba(0, 229, 255, 0.88) !important;
  font-size: 0.68rem;
  line-height: 1.45;
  margin: 0 0 0.45rem 0;
}
.r8-shimmer-inner button {
  font-family: 'Goldman', sans-serif !important;
  width: 100%;
  border-radius: 8px !important;
  border: 1px solid rgba(80, 160, 255, 0.65) !important;
  background: rgba(0, 40, 80, 0.55) !important;
  color: #7df9ff !important;
  font-weight: 700 !important;
  font-size: 0.68rem !important;
  letter-spacing: 0.05em !important;
}
.r8-shimmer-inner button:hover {
  border-color: #FFD700 !important;
  color: #FFD700 !important;
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
.det-modal h4 { color: #5eb3ff !important; margin: 0 0 0.4rem 0; font-family: 'Goldman', sans-serif !important; }
.det-modal .det-prop { color: #FFD700 !important; font-size: 0.78rem; font-weight: 700; margin-bottom: 0.35rem; }
.det-modal p { color: #00E5FF !important; margin: 0; font-size: 0.82rem; line-height: 1.5; }

.outreach-command-wrap {
  border-radius: 14px;
  padding: 3px;
  background: linear-gradient(120deg, #000033, #D4AF37, #000033);
  background-size: 240% 100%;
  animation: prism-shimmer 14s linear infinite;
  margin: 1rem 0 0.85rem 0;
}
.outreach-command-inner {
  background: linear-gradient(180deg, #000011 0%, #000044 100%);
  border-radius: 11px;
  padding: 0.85rem 1rem;
  border: 1px solid rgba(212, 175, 55, 0.4);
}
.outreach-command-inner h3 {
  font-family: 'Goldman', sans-serif !important;
  color: #FFD700 !important;
  margin: 0 0 0.35rem 0;
  font-size: 1rem;
  letter-spacing: 0.06em;
}
.outreach-csv-note {
  font-family: 'Goldman', sans-serif !important;
  color: rgba(0, 229, 255, 0.85) !important;
  font-size: 0.72rem;
  margin: 0 0 0.65rem 0;
  line-height: 1.45;
}
.sim-feed-outer {
  height: 168px;
  overflow: hidden;
  border: 1px solid rgba(0, 229, 255, 0.25);
  border-radius: 10px;
  background: rgba(0, 0, 34, 0.75);
  position: relative;
}
.sim-feed-track {
  animation: sim-scroll 18s linear infinite;
}
.sim-feed-line {
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.7rem;
  color: #00E5FF !important;
  padding: 0.4rem 0.65rem;
  border-bottom: 1px solid rgba(212, 175, 55, 0.1);
  line-height: 1.4;
}
.sim-feed-line strong { color: #FFD700 !important; }
.sim-feed-line .sim-auth { color: #7df9ff !important; font-size: 0.66rem; letter-spacing: 0.04em; }

.status-live, .status-synced {
  color: #2DD4BF !important;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-shadow:
    0 0 6px rgba(45, 212, 191, 0.55),
    0 0 14px rgba(32, 178, 170, 0.45);
}
.live-audit-tag {
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.74rem;
  color: rgba(0, 229, 255, 0.9) !important;
  margin: 0 0 0.55rem 0;
  line-height: 1.45;
}
.logistics-feed-outer {
  height: 200px;
  overflow: hidden;
  border: 1px solid rgba(45, 212, 191, 0.35);
  border-radius: 10px;
  background: rgba(0, 0, 34, 0.82);
  box-shadow: inset 0 0 16px rgba(45, 212, 191, 0.08);
}
.logistics-feed-track {
  animation: logistics-feed-scroll 22s linear infinite;
}
.logistics-line {
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.68rem;
  color: #00E5FF !important;
  padding: 0.38rem 0.6rem;
  border-bottom: 1px solid rgba(255, 215, 0, 0.22);
  line-height: 1.45;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.logistics-line-empty { color: #D4AF37 !important; white-space: normal; }
.lt-time { color: #D4AF37 !important; font-variant-numeric: tabular-nums; }
.lt-name { color: #fff8dc !important; }
.lt-lga { color: #7df9ff !important; }
.lt-sep { color: rgba(212, 175, 55, 0.45) !important; padding: 0 0.15rem; }

.polling-prism-wrap {
  border-radius: 14px;
  padding: 3px;
  background: linear-gradient(120deg, #000033, #D4AF37, #2DD4BF, #000033);
  background-size: 280% 100%;
  animation: prism-shimmer 12s linear infinite;
  margin: 0.75rem 0 0.5rem 0;
}
.polling-prism-inner {
  background: linear-gradient(180deg, #000011 0%, #000044 100%);
  border-radius: 11px;
  padding: 0.65rem 0.6rem;
  border: 1px solid rgba(45, 212, 191, 0.35);
}
.polling-prism-inner label, .polling-prism-inner .stTextArea label {
  font-family: 'Goldman', sans-serif !important;
  color: #FFD700 !important;
  font-size: 0.72rem !important;
}
.sentiment-shell {
  margin-top: 0.45rem;
  padding: 0.35rem 0.15rem 0.15rem 0.15rem;
  border-radius: 10px;
  border: 1px solid rgba(45, 212, 191, 0.3);
  animation: sentiment-bar-pulse 2.4s ease-in-out infinite;
}

.exec-test-prism-wrap {
  border-radius: 14px;
  padding: 3px;
  background: linear-gradient(120deg, #000033, #FFD700, #D4AF37, #00e5ff, #000033);
  background-size: 300% 100%;
  animation: prism-shimmer 11s linear infinite;
  margin-bottom: 0.9rem;
}
.exec-test-prism-inner {
  background: linear-gradient(180deg, #000011 0%, #000044 100%);
  border-radius: 11px;
  padding: 0.85rem 1rem 1rem 1rem;
  border: 1px solid rgba(255, 215, 0, 0.42);
}
.exec-test-prism-inner h3 {
  font-family: 'Goldman', sans-serif !important;
  color: #FFD700 !important;
  margin: 0 0 0.2rem 0;
  font-size: 1.02rem;
  letter-spacing: 0.06em;
}
.exec-node-banner {
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.72rem;
  color: #00E5FF !important;
  margin: 0 0 0.45rem 0;
  line-height: 1.45;
}

.wa-gateway-wrap {
  border-radius: 12px;
  padding: 3px;
  background: linear-gradient(120deg, #121212, #FFD700, #00F5FF, #121212);
  background-size: 280% 100%;
  animation: prism-shimmer 14s linear infinite;
  margin: 0.75rem 0 0.55rem 0;
}
.wa-gateway-inner {
  background: #121212;
  border-radius: 9px;
  padding: 0.65rem 0.55rem 0.75rem 0.55rem;
  border: 1px solid rgba(255, 215, 0, 0.4);
}
.wa-gateway-inner h4 {
  font-family: 'Goldman', sans-serif !important;
  color: #FFD700 !important;
  text-align: center;
  font-size: 0.76rem;
  letter-spacing: 0.1em;
  margin: 0 0 0.5rem 0;
}
.wa-galadima-header {
  font-family: 'Goldman', sans-serif !important;
  color: #FFD700 !important;
  text-align: center;
  font-size: 0.84rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin: 0 0 0.2rem 0;
  font-weight: 700 !important;
  text-shadow: none !important;
}
.wa-gateway-sub {
  font-family: 'Goldman', sans-serif !important;
  color: #00F5FF !important;
  text-align: center;
  font-size: 0.68rem;
  margin: 0 0 0.55rem 0;
  letter-spacing: 0.07em;
  font-weight: 700 !important;
  text-shadow: none !important;
}
.wa-gateway-btn-stack {
  display: flex;
  flex-direction: column;
  gap: 0.42rem;
  align-items: stretch;
  width: 100%;
}
[data-testid="stSidebar"] .wa-sidebar-wa-link {
  display: block !important;
  color: #00F5FF !important;
  font-weight: 700 !important;
  text-decoration: none !important;
  border: 1px solid rgba(0, 245, 255, 0.45) !important;
  border-radius: 8px !important;
  padding: 0.42rem 0.55rem !important;
  text-align: center !important;
  background: rgba(26, 26, 26, 0.95) !important;
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.72rem !important;
  text-shadow: none !important;
  box-sizing: border-box !important;
  width: 100% !important;
  line-height: 1.3 !important;
}
[data-testid="stSidebar"] .wa-sidebar-wa-link:hover {
  border-color: rgba(255, 215, 0, 0.5) !important;
  color: #FFD700 !important;
}
.wa-env-hint {
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.58rem !important;
  color: rgba(255, 215, 0, 0.78) !important;
  margin: 0.4rem 0 0 0 !important;
  text-align: center !important;
  text-shadow: none !important;
  line-height: 1.38 !important;
}
.wa-safety-protocol {
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.62rem !important;
  color: rgba(0, 245, 255, 0.92) !important;
  line-height: 1.45 !important;
  margin: 0.55rem 0 0 0 !important;
  text-align: center !important;
  text-shadow: none !important;
  border-top: 1px solid rgba(255, 215, 0, 0.2);
  padding-top: 0.45rem !important;
}

.exec-forensic-muted {
  margin-top: 0.5rem;
  padding-top: 0.35rem;
  border-top: 1px solid rgba(212, 175, 55, 0.22);
}
.exec-forensic-muted .forensic-hint {
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.65rem !important;
  color: rgba(212, 175, 55, 0.75) !important;
  margin: 0 0 0.4rem 0 !important;
}
.exec-forensic-muted [data-testid="stExpander"] {
  border: 1px solid rgba(212, 175, 55, 0.25) !important;
  border-radius: 10px !important;
  background: rgba(0, 0, 34, 0.35) !important;
}
.exec-forensic-muted [data-testid="stMetricValue"],
.exec-forensic-muted [data-testid="stMetricLabel"] {
  font-size: 0.78rem !important;
}
"""

_CSS = _CSS.replace("__TACTICAL_BOLT_SVG__", _tactical_bolt_svg_data_url())


def _format_countdown(target: date, tz_key: str) -> tuple[str, str]:
    tz = ZoneInfo(tz_key)
    end = datetime.combine(target, datetime.min.time(), tzinfo=tz)
    now = datetime.now(tz)
    if now >= end:
        return "STRIKE WINDOW ACTIVE", target.strftime("%d %b %Y")
    total_sec = max(0, int((end - now).total_seconds()))
    days, rem = divmod(total_sec, 86400)
    h, rem2 = divmod(rem, 3600)
    m, s = divmod(rem2, 60)
    main = f"{days}d {h:02d}h {m:02d}m {s:02d}s"
    return main, target.strftime("%d %b %Y")


@st.fragment(run_every=timedelta(seconds=1))
def _render_timing_hub() -> None:
    st.markdown(
        '<div class="section-prism"><h3>THE TIMING STRIKE</h3></div>',
        unsafe_allow_html=True,
    )
    pc, mc, cc = st.columns(3)
    prim_main, prim_sub = _format_countdown(GUBER_PRIMARIES_DATE, "Africa/Lagos")
    gen_main, gen_sub = _format_countdown(GENERAL_ELECTION_2027_DATE, "Africa/Lagos")
    with pc:
        st.markdown(
            '<div class="timing-prism"><div class="timing-prism-inner">'
            "<h4>Governorship Primary Countdown</h4>"
            f'<div class="timing-count">{html.escape(prim_main)}</div>'
            f'<div class="timing-sub">Governorship primary · {html.escape(prim_sub)}</div>'
            "</div></div>",
            unsafe_allow_html=True,
        )
    with mc:
        st.markdown(
            '<div class="timing-shimmer"><div class="timing-shimmer-inner">'
            "<h4>General Election 2027</h4>"
            f'<div class="timing-count" style="color:#D4AF37">{html.escape(gen_main)}</div>'
            f'<div class="timing-sub">General election day · {html.escape(gen_sub)}</div>'
            "</div></div>",
            unsafe_allow_html=True,
        )
    with cc:
        kad = datetime.now(ZoneInfo("Africa/Lagos"))
        lon = datetime.now(ZoneInfo("Europe/London"))
        ny = datetime.now(ZoneInfo("America/New_York"))
        dubai = datetime.now(ZoneInfo("Asia/Dubai"))
        rows = "".join(
            '<div class="clock-line"><span>'
            f"{html.escape(label)}</span><span>"
            f"{html.escape(dt.strftime('%a %d %b %Y · %H:%M:%S'))}</span></div>"
            for label, dt in (
                ("Kaduna (WAT)", kad),
                ("London (GMT)", lon),
                ("New York (EST)", ny),
                ("Dubai (GST)", dubai),
            )
        )
        st.markdown(
            '<div class="sovereign-clock-box"><div class="sovereign-clock-inner">'
            "<h4>The Pulse · Global Sovereign Clock</h4>"
            f'<div class="clock-grid">{rows}</div>'
            "</div></div>",
            unsafe_allow_html=True,
        )


def _build_logistics_feed_html(df: pd.DataFrame, n_lines: int = 42) -> str:
    lines: list[str] = []
    if df.empty:
        lines.append(
            '<div class="logistics-line logistics-line-empty">'
            f"Ingest path: <code>{html.escape(str(VOTER_DB_CSV))}</code> — "
            "<span class=\"status-live\">OFFLINE</span> · add rows to activate stream.</div>"
        )
    else:
        for _ in range(n_lines):
            r = df.sample(n=1).iloc[0]
            ts = (datetime.now() - timedelta(seconds=random.randint(0, 7200))).strftime("%H:%M:%S")
            fn = str(r["first_name"]).strip()
            ln = str(r["last_name"]).strip()
            lga = str(r["lga"]).strip()
            lines.append(
                '<div class="logistics-line">'
                f'<span class="lt-time">[{html.escape(ts)}]</span>'
                '<span class="lt-sep">|</span>'
                f'<span class="lt-name">{html.escape(fn)} {html.escape(ln)}</span>'
                '<span class="lt-sep">|</span>'
                f'<span class="lt-lga">{html.escape(lga)}</span>'
                '<span class="lt-sep">|</span>'
                '<span class="status-synced">Status: SYNCED</span>'
                "</div>"
            )
    body = "".join(lines)
    dup = body + body
    return f'<div class="logistics-feed-outer"><div class="logistics-feed-track">{dup}</div></div>'


@st.fragment(run_every=timedelta(seconds=2))
def _render_live_outreach_panel() -> None:
    vdf = _load_voter_db(str(VOTER_DB_CSV))
    n = len(vdf)
    src = html.escape(VOTER_DB_CSV.name)
    live_row = (
        f'<span class="status-live">LIVE INGESTION</span> · {n:,} rows · <span class="status-synced">SYNCED</span>'
        if n
        else '<span class="status-live">STANDBY</span> — awaiting voter_db.csv'
    )
    st.markdown(
        '<div class="outreach-command-wrap"><div class="outreach-command-inner">'
        "<h3>1.5M Voter Tactical Outreach · Logistics Command</h3>"
        '<p class="live-audit-tag"><span class="status-live">LIVE</span> Nodal Audit · voter registry stream</p>'
        f'<p class="outreach-csv-note">Source: <strong>{src}</strong> · {live_row}</p>'
        '<p class="outreach-csv-note" style="margin-bottom:0.5rem;">'
        "Logistics feed: <strong>[Time]</strong> | <strong>First Last</strong> | <strong>LGA</strong> | "
        '<span class="status-synced">Status: SYNCED</span></p>'
        f"{_build_logistics_feed_html(vdf)}"
        "</div></div>",
        unsafe_allow_html=True,
    )


@st.fragment(run_every=timedelta(seconds=3))
def _render_live_nodal_sidebar_line() -> None:
    vdf = _load_voter_db(str(VOTER_DB_CSV))
    if vdf.empty:
        st.markdown(
            '<p class="dt-handshake">Live Nodal Audit: <span class="status-live">STANDBY</span> — '
            f"point <code>{html.escape(VOTER_DB_CSV.name)}</code> alongside the app.</p>",
            unsafe_allow_html=True,
        )
        return
    r = vdf.sample(n=1).iloc[0]
    st.markdown(
        '<p class="dt-handshake">Live Nodal Audit · <span class="status-synced">SYNCED</span> · '
        f"{html.escape(str(r['first_name']))} {html.escape(str(r['last_name']))} · "
        f"{html.escape(str(r['lga']))}</p>",
        unsafe_allow_html=True,
    )


@st.fragment(run_every=timedelta(milliseconds=400))
def _render_sentiment_sidebar() -> None:
    t0 = st.session_state.get("cien_poll_mono_t0")
    targets = st.session_state.get("cien_poll_targets")
    if t0 is None or targets is None:
        y, n_, u = 34.0, 33.0, 33.0
        subtitle = "Awaiting PUSH to 1.5M nodes"
    else:
        elapsed = time.monotonic() - float(t0)
        ty = float(targets["Yes"])
        tn = float(targets["No"])
        tu = float(targets["Undecided"])
        if elapsed < 10.0:
            y = max(8.0, min(92.0, ty + random.uniform(-16, 16)))
            n_ = max(8.0, min(92.0, tn + random.uniform(-16, 16)))
            u = max(5.0, min(45.0, tu + random.uniform(-12, 12)))
            s = y + n_ + u
            y, n_, u = 100.0 * y / s, 100.0 * n_ / s, 100.0 * u / s
            subtitle = f"Field pulse · {max(0.0, 10.0 - elapsed):.1f}s to scientific lock"
        else:
            y, n_, u = ty, tn, tu
            subtitle = "Scientific projection · stabilized"
    fig = go.Figure(
        data=[
            go.Bar(
                x=["Yes", "No", "Undecided"],
                y=[y, n_, u],
                marker=dict(
                    color=[TURQ, "#D4AF37", "#8899aa"],
                    line=dict(color="#000033", width=1),
                ),
            )
        ]
    )
    fig.update_layout(
        title=dict(text="Live Sentiment Analysis", font=dict(family="Goldman", size=12, color=GOLD)),
        paper_bgcolor=NAVY_DEEP,
        plot_bgcolor=NAVY_DEEP,
        font=dict(family="Goldman", color=GOLD),
        height=210,
        margin=dict(t=32, b=28, l=36, r=12),
        yaxis=dict(range=[0, 100], title="%", gridcolor="#003350"),
        xaxis=dict(title=""),
        showlegend=False,
    )
    st.markdown('<div class="sentiment-shell">', unsafe_allow_html=True)
    st.plotly_chart(
        fig,
        use_container_width=True,
        key="cien_sentiment_sidebar",
        config={"displayModeBar": False, "responsive": True},
    )
    st.caption(subtitle)
    st.markdown("</div>", unsafe_allow_html=True)


def _donut_purity(apc_v: int, pdp_v: int, lp_v: int, lift_pct: int, margin: int) -> go.Figure:
    fig = go.Figure(
        data=[
            go.Pie(
                labels=["APC", "PDP", "LP"],
                values=[apc_v, pdp_v, lp_v],
                hole=0.52,
                marker=dict(colors=["#D4AF37", "#00E5FF", "#8899aa"], line=dict(color="#000033", width=2)),
                textinfo="label+value",
                texttemplate="%{label}<br>%{value:,}",
                hovertemplate="<b>%{label}</b><br>%{value:,} votes<extra></extra>",
            )
        ]
    )
    sub = f"Turnout lift sim {lift_pct}% · APC−PDP margin {margin:,}"
    fig.update_layout(
        title=dict(
            text=f"The Winner/Loser Cycle — dynamic · {sub}",
            font=dict(family="Goldman", size=14, color=GOLD),
        ),
        paper_bgcolor=NAVY_DEEP,
        plot_bgcolor=NAVY_DEEP,
        font=dict(family="Goldman", color=GOLD),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.12, x=0.5, xanchor="center"),
        height=400,
        margin=dict(t=52, b=48, l=24, r=24),
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


def _render_executive_variance_forensic() -> None:
    """Forensic variance lock at bottom of main — low visual weight; expander default collapsed."""
    st.session_state.setdefault("cien_exec_n0", DEFAULT_EXEC_NODE0)
    st.session_state.setdefault("cien_exec_n1", DEFAULT_EXEC_NODE1)
    st.session_state.setdefault("cien_exec_tol", 0.0)

    st.markdown('<div class="exec-forensic-muted">', unsafe_allow_html=True)
    st.markdown(
        '<p class="forensic-hint">Variance lock · Node registers (GCSLC_EXEC_NODE0 / GCSLC_EXEC_NODE1)</p>',
        unsafe_allow_html=True,
    )
    with st.expander("Forensic alignment · Executive variance (Node 0 / Node 1)", expanded=False):
        st.caption("Same mathematics as prior executive test — kept below Purity / 2/3rds command focus.")
        e0, e1, et = st.columns(3)
        with e0:
            n0 = st.number_input(
                "Node 0 (Chairman)",
                min_value=0.0,
                max_value=1e15,
                step=1.0,
                format="%.0f",
                key="cien_exec_n0",
            )
        with e1:
            n1 = st.number_input(
                "Node 1 (His Excellency)",
                min_value=0.0,
                max_value=1e15,
                step=1.0,
                format="%.0f",
                key="cien_exec_n1",
            )
        with et:
            tol = st.number_input(
                "Parity tolerance (±)",
                min_value=0.0,
                max_value=1e15,
                step=1.0,
                format="%.0f",
                key="cien_exec_tol",
            )

        f0, f1 = float(n0), float(n1)
        delta = f1 - f0
        blended = (f0 + f1) / 2.0
        synced = abs(delta) <= float(tol)
        em1, em2, em3 = st.columns(3)
        with em1:
            st.metric("Node delta (1 − 0)", f"{delta:+,.0f}")
        with em2:
            st.metric("Blended executive register", f"{blended:,.2f}")
        with em3:
            ratio = (f1 / f0) if f0 else float("nan")
            st.metric("Node 1 ÷ Node 0", f"{ratio:.6f}" if f0 else "—")

        if synced:
            st.markdown(
                '<p class="live-audit-tag" style="margin:0.35rem 0 0 0;">'
                '<span class="status-synced">EXEC_NODES_SYNCED</span> · within tolerance</p>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<p class="live-audit-tag" style="margin:0.35rem 0 0 0;">'
                '<span class="status-live">VARIANCE_LOCK</span> · |Δ| exceeds tolerance corridor</p>',
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)


def main() -> None:
    st.set_page_config(
        page_title="CIEN Kaduna 2027 · GCSLC",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(f"<style>{_CSS}</style>", unsafe_allow_html=True)

    with st.sidebar:
        st.caption(
            "Sidebar is collapsible. When closed, the header shows a gold bolt (SVG) tactical alert — "
            "the 1.5M outreach simulation keeps running."
        )
        st.markdown(
            '<div class="direct-tactical-wrap"><div class="direct-tactical-inner">',
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h4>Direct Tactical Pulse</h4>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="dt-verified">Verified Kaduna Database: <strong>1,500,000</strong> · '
            '<span class="status-live">LIVE</span> stream</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="dt-ticker"><span class="status-synced">SMS/WhatsApp Precision Strike: ACTIVE</span></p>',
            unsafe_allow_html=True,
        )
        _render_live_nodal_sidebar_line()
        st.markdown("</div></div>", unsafe_allow_html=True)
        st.markdown(
            '<div class="polling-prism-wrap"><div class="polling-prism-inner">',
            unsafe_allow_html=True,
        )
        st.text_area(
            "Broadcast Strategic Question",
            key="cien_bcast_q",
            height=90,
            placeholder="Sovereign poll text for 1.5M nodes…",
        )
        if st.button("PUSH TO 1.5M NODES", key="cien_push_nodes", use_container_width=True):
            st.session_state["cien_poll_question"] = (st.session_state.get("cien_bcast_q") or "").strip()
            y = random.randint(46, 60)
            n = random.randint(18, min(40, 100 - y - 6))
            u = float(100 - y - n)
            st.session_state["cien_poll_mono_t0"] = time.monotonic()
            st.session_state["cien_poll_targets"] = {
                "Yes": float(y),
                "No": float(n),
                "Undecided": u,
            }
        _render_sentiment_sidebar()
        st.markdown("</div></div>", unsafe_allow_html=True)
        st.markdown(_executive_wa_gateway_sidebar_html(), unsafe_allow_html=True)
        st.markdown(
            '<div class="sidebar-handshake" style="margin-top:0.5rem">'
            "<b>Executive-Load-142</b><br>"
            "Leadership handshake: ward captains, uplink, and ballot-box packs synchronized "
            "before each mobilization wave."
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="prism-widget"><div class="prism-widget-inner">'
        '<div class="cien-identity-stack">'
        f'<p class="cien-title">{html.escape(ORG_NAME)}</p>'
        f'<p class="cien-chairman">{html.escape(CHAIRMAN_LINE)}</p>'
        f'<p class="cien-commander">{html.escape(COMMANDER_LINE)}</p>'
        f'<p class="cien-motto">{html.escape(MOTTO)}</p>'
        '<p class="cien-foundation">Foundational logic · '
        '<span class="cien-8r">8R Stealth Paradigm</span></p>'
        "</div></div></div>",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="prism-widget"><div class="prism-widget-inner">', unsafe_allow_html=True)
    st.markdown("#### Chairman · Turnout lift simulation", unsafe_allow_html=True)
    lift_pct = st.radio(
        "Simulate APC-weighted turnout lift on 2023 baseline",
        options=[0, 5, 10, 15],
        format_func=lambda x: f"{x}% lift",
        horizontal=True,
        key="cien_turnout_lift",
    )
    lift_f = lift_pct / 100.0
    v_apc = int(round(V_2023_APC * (1 + lift_f)))
    margin = v_apc - V_2023_PDP
    tm1, tm2 = st.columns(2)
    with tm1:
        st.metric("Winning margin (APC − PDP)", f"{margin:,}")
    with tm2:
        st.metric("Adjusted APC votes (sim)", f"{v_apc:,}", delta=f"+{lift_pct}% lift")
    st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="section-prism"><h3>WINNER / LOSER CYCLE</h3></div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(
        _donut_purity(v_apc, V_2023_PDP, V_2023_LP, lift_pct, margin),
        use_container_width=True,
        key="cien_wl_cycle",
        config={"responsive": True, "displayModeBar": False},
    )

    _render_timing_hub()

    base_pct = 100.0 * LGA_MAJORITY_NEED / LGA_TARGET
    fill_pct = min(100.0, base_pct * (1 + lift_f * 0.55))
    st.markdown('<div class="section-prism"><h3>THE 2/3RDS TRACKER</h3></div>', unsafe_allow_html=True)
    st.markdown(
        f"""
<div class="twothirds-wrap" style="--cien-twothirds-pct: {fill_pct:.2f}%;">
  <div class="twothirds-label">
    <span>LGA majority path <span class="status-live">(dynamic)</span></span>
    <span>{LGA_MAJORITY_NEED} / {LGA_TARGET} LGAs</span>
  </div>
  <div class="twothirds-track"><div class="twothirds-fill"></div></div>
  <p style="color:#00E5FF;font-size:0.78rem;margin:0.45rem 0 0 0;font-family:Goldman,sans-serif;">
    Progress toward securing {LGA_MAJORITY_NEED} of {LGA_TARGET} LGAs · turnout lift {lift_pct}% synthetic nodal pressure
    (<span class="status-synced">bar width live</span>).
  </p>
</div>
""",
        unsafe_allow_html=True,
    )

    _render_live_outreach_panel()

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
        '<div class="section-prism"><h3>THE 8R SHIMMER-GRID</h3></div>',
        unsafe_allow_html=True,
    )
    if "cien_r8" not in st.session_state:
        st.session_state["cien_r8"] = None

    for row_start in (0, 4):
        rcols = st.columns(4)
        for j in range(4):
            idx = row_start + j
            if idx >= len(PARADIGMS_8R):
                break
            p = PARADIGMS_8R[idx]
            with rcols[j]:
                st.markdown(
                    '<div class="r8-shimmer-grid"><div class="r8-shimmer-inner">',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<p class="r8-id">{html.escape(p["id"])}</p>'
                    f'<p class="r8-name">{html.escape(p["title"])}</p>'
                    f'<p class="r8-body">{html.escape(p["paradigm"])}</p>',
                    unsafe_allow_html=True,
                )
                if st.button(
                    "Proprietary determinant",
                    key=f"r8_btn_{p['id']}",
                    use_container_width=True,
                ):
                    st.session_state["cien_r8"] = p["id"]
                st.markdown("</div></div>", unsafe_allow_html=True)

    sel_r8 = st.session_state["cien_r8"]
    if sel_r8:
        item = next(x for x in PARADIGMS_8R if x["id"] == sel_r8)
        st.markdown(
            f'<div class="det-modal"><h4>{html.escape(item["id"])} · {html.escape(item["title"])}</h4>'
            f'<p class="det-prop">{html.escape(item["proprietary"])}</p>'
            "<p>Paradigm (clinical reference): "
            f"{html.escape(item['paradigm'])}</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Dismiss proprietary determinant", key="dismiss_r8"):
            st.session_state["cien_r8"] = None
            st.rerun()

    _render_executive_variance_forensic()

    st.caption(
        f"CIEN Kaduna 2027 · live ingest {VOTER_DB_CSV.name} (override with GCSLC_VOTER_DB) · "
        f"port {os.environ.get('STREAMLIT_SERVER_PORT', '9099')} · "
        "Scientific model narrative for strategic planning only."
    )


if __name__ == "__main__":
    main()
