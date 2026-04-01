# CIEN Kaduna 2027 — Galadiman Ruwa Center (GCSLC LTD/GTE)
# Run: python3 -m streamlit run cien_kaduna_2027.py --server.port 9099

from __future__ import annotations

import base64
import html
import math
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
VERIFY_IMG_NAMES = ("image_0.png", "image_1.png")


def _resolve_verification_png(filename: str) -> Path | None:
    """Sidebar verification thumbnails: repo assets/, repo root, optional GCSLC_VERIFY_IMG_DIR."""
    override = os.environ.get(f"GCSLC_VERIFY_{filename.replace('.', '_').upper()}")
    if override:
        p = Path(override).expanduser().resolve()
        if p.is_file():
            return p
    extra = os.environ.get("GCSLC_VERIFY_IMG_DIR")
    roots = [BASE_DIR / "assets", BASE_DIR]
    if extra:
        roots.insert(0, Path(extra).expanduser().resolve())
    for root in roots:
        cand = root / filename
        if cand.is_file():
            return cand
    return None


def _png_data_uri(path: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii")


# Single-source lock: Desktop KADUNA_Data_2027 (override only via GCSLC_KADUNA_DATA_2027).
_DESKTOP_KADUNA_2027 = Path.home() / "Desktop" / "KADUNA_Data_2027"
KADUNA_DATA_2027_DIR = Path(os.environ.get("GCSLC_KADUNA_DATA_2027", str(_DESKTOP_KADUNA_2027))).resolve()
# Never auto-mount repo voter_db.csv — saves RAM; set GCSLC_VOTER_DB to bind a file explicitly.
_REPO_VOTER_DB_CSV = (BASE_DIR / "voter_db.csv").resolve()

# Bounded lake walk — never enumerate millions of dentries into session / UI state.
KADUNA_LAKE_SCAN_CAP = 2000
KADUNA_LAKE_SKIP_FILES = frozenset(
    name.lower()
    for name in (
        "voter_db.csv",
        ".ds_store",
        "thumbs.db",
        "desktop.ini",
    )
)


@st.cache_data(ttl=120, show_spinner=False)
def _kaduna_lake_preview_pool() -> list[str]:
    """Collect at most KADUNA_LAKE_SCAN_CAP filenames (unordered scan → sorted) — virtualized roller source."""
    d = KADUNA_DATA_2027_DIR
    if not d.is_dir():
        return []
    names: list[str] = []
    try:
        with os.scandir(d) as it:
            for ent in it:
                if len(names) >= KADUNA_LAKE_SCAN_CAP:
                    break
                try:
                    if not ent.is_file(follow_symlinks=False):
                        continue
                except OSError:
                    continue
                n = ent.name
                if n.startswith(".") or n.lower() in KADUNA_LAKE_SKIP_FILES:
                    continue
                names.append(n)
    except OSError:
        return []
    names.sort()
    return names


def _lake_display_slice(pool: list[str], window: int, use_tail: bool) -> list[str]:
    """Head-only or head+tail window; never materializes beyond len(pool)."""
    if not pool:
        return []
    w = max(1, min(int(window), len(pool)))
    if not use_tail or len(pool) <= w:
        return pool[:w]
    head_n = max(1, w // 2)
    tail_n = w - head_n
    return pool[:head_n] + pool[-tail_n:]


# Kaduna anchor (not national PU total)
PU_COUNT_KADUNA = 8_012
KADUNA_VOTER_TARGET = 1_500_000
NATIONAL_MANDATE_TOTAL = 20_700_000
KADUNA_NATIONAL_CONTRIBUTION_PCT = 7.25
KADUNA_EMERALD = "#046A38"
_VOTERS_PER_PU_KADUNA = KADUNA_VOTER_TARGET / float(PU_COUNT_KADUNA)
# 2027 sovereign consolidation (D3): 1.5M goal ÷ 8,012 PUs → 187 voters/node requirement
VOTERS_PER_PU_D3_REQUIREMENT = 187
CONSOLIDATION_GOAL_2027 = KADUNA_VOTER_TARGET
CONSOLIDATION_CONSTANT = KADUNA_VOTER_TARGET  # 1.5M consolidation constant (command target)
BUFFER_20_7M_LABEL = "20.7M"

CHANNEL_OPTION_PRIVATE = "📱 SMS/WA (The Private Strike)"
CHANNEL_OPTION_GRASSROOTS = "🎥 Grassroots (TikTok/FB/IG)"
CHANNEL_OPTION_SOVEREIGN = "🏛️ Sovereign (X/LinkedIn)"
CHANNEL_OPTIONS: list[str] = [
    CHANNEL_OPTION_PRIVATE,
    CHANNEL_OPTION_GRASSROOTS,
    CHANNEL_OPTION_SOVEREIGN,
]
# Legacy multiselect values → re-mapped lanes (session migration)
LEGACY_CHANNEL_MAP: dict[str, str] = {
    "WhatsApp/SMS (Primary)": CHANNEL_OPTION_PRIVATE,
    "TikTok (Mass Mobilization)": CHANNEL_OPTION_GRASSROOTS,
    "X / FB / IG (Public Pulse)": CHANNEL_OPTION_SOVEREIGN,
}


def _migrate_mc_channels_session() -> None:
    raw = st.session_state.get("cien_mc_channels")
    if not isinstance(raw, list):
        st.session_state["cien_mc_channels"] = list(CHANNEL_OPTIONS)
        return
    seen: set[str] = set()
    out: list[str] = []
    for x in raw:
        if not isinstance(x, str):
            continue
        m = LEGACY_CHANNEL_MAP.get(x, x)
        if m in CHANNEL_OPTIONS and m not in seen:
            seen.add(m)
            out.append(m)
    st.session_state["cien_mc_channels"] = out or list(CHANNEL_OPTIONS)


def _channel_lane_tiles_html(selected: list[str] | None) -> str:
    """Broadcast Switchboard lane cards — cyan border/glow when lane is selected (multiselect)."""
    if not isinstance(selected, list):
        selected = list(CHANNEL_OPTIONS)
    sel = set(selected)

    def one(option: str, emoji: str, title: str, sub: str) -> str:
        active = " channel-lane-tile-active" if option in sel else ""
        return (
            f'<div class="channel-lane-tile{active}">'
            f'<span class="channel-lane-emoji" aria-hidden="true">{emoji}</span>'
            f'<span class="channel-lane-title">{html.escape(title)}</span>'
            f'<span class="channel-lane-sub">{html.escape(sub)}</span></div>'
        )

    inner = (
        one(CHANNEL_OPTION_PRIVATE, "📱", "SMS / WA", "The Private Strike")
        + one(CHANNEL_OPTION_GRASSROOTS, "🎥", "Grassroots", "TikTok · FB · IG")
        + one(CHANNEL_OPTION_SOVEREIGN, "🏛️", "Sovereign", "X · LinkedIn")
    )
    return f'<div class="channel-lane-icons-row">{inner}</div>'


def _format_reminder_for_lane(channel: str, raw: str) -> str:
    """Single-lane formatted payload (Chairman reminder)."""
    brand = "CIEN Kaduna 2027"
    if channel == CHANNEL_OPTION_PRIVATE:
        return f"【{brand}】{raw}\n— Reply CONFIRM · Polling Unit ready."
    if channel == CHANNEL_OPTION_GRASSROOTS:
        return f"{raw} · {brand} #Kaduna2027 #Galadima #VoteSmart #Grassroots #15of15"
    if channel == CHANNEL_OPTION_SOVEREIGN:
        return f"[Sovereign] {raw} · {brand} #Kaduna2027 #CIEN #LinkedIn #X"
    if channel == "WhatsApp/SMS (Primary)":
        return _format_reminder_for_lane(CHANNEL_OPTION_PRIVATE, raw)
    if channel == "TikTok (Mass Mobilization)":
        return _format_reminder_for_lane(CHANNEL_OPTION_GRASSROOTS, raw)
    if channel == "X / FB / IG (Public Pulse)":
        return _format_reminder_for_lane(CHANNEL_OPTION_SOVEREIGN, raw)
    return f"{brand}: {raw}"


def _format_master_reminder_for_channels(raw: str, channels: list[str]) -> dict[str, str]:
    """Chairman reminder → channel-specific copy (same core message, channel-native formatting)."""
    raw = (raw or "").strip()
    if not raw:
        return {c: "" for c in channels}
    return {c: _format_reminder_for_lane(c, raw) for c in channels}


def _format_master_reminder_all_lanes(raw: str) -> dict[str, str]:
    """Always produce all three strike-lane payloads (preview / parity)."""
    raw = (raw or "").strip()
    if not raw:
        return {c: "" for c in CHANNEL_OPTIONS}
    return {c: _format_reminder_for_lane(c, raw) for c in CHANNEL_OPTIONS}


# Executive Test Module — Node 0 (Chairman) / Node 1 (His Excellency); override via env or UI
DEFAULT_EXEC_NODE0 = float(os.environ.get("GCSLC_EXEC_NODE0", "14314"))
DEFAULT_EXEC_NODE1 = float(os.environ.get("GCSLC_EXEC_NODE1", "8507"))

# Executive Gateway — verified handshake nodes (final override). wa.me digits only, no + or spaces.
EXECUTIVE_HANDSHAKE_MAP: tuple[dict[str, str], ...] = (
    {
        "node_id": "0",
        "pillar": "Strategy",
        "name": "Dr. Fabian Okoye",
        "wa_me_id": "2348037861894",
        "label": "SA Research & Strategy",
    },
    {
        "node_id": "1",
        "pillar": "Execution",
        "name": "Chief of Staff",
        "wa_me_id": "2348033701212",
        "label": "Command Hub",
    },
    {
        "node_id": "2",
        "pillar": "Outreach",
        "name": "Dr. Abdul Ishaq",
        "wa_me_id": "2348037004981",
        "label": "SA Stakeholders",
    },
)

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

# D3 — Official historical audit (locked administrative figures: lead / total votes)
HIST_D3_2015 = {"year": 2015, "lead": 1_120_000, "total": 1_610_000}
HIST_D3_2019 = {"year": 2019, "lead": 993_000, "total": 1_660_000}
HIST_D3_2023 = {"year": 2023, "lead": 554_000, "total": 1_360_000}
HIST_D3_AUDIT_ROWS: list[dict[str, int]] = [HIST_D3_2015, HIST_D3_2019, HIST_D3_2023]
D3_FRAGMENTATION_LEAKAGE_2019_2023 = HIST_D3_2019["total"] - HIST_D3_2023["total"]  # 300,000

# Dual-track trend — Governorship = D3 lock; Presidential total = Gov + gap (2023 gap locked)
DUAL_TRACK_PRES_GOV_GAP: dict[int, int] = {2015: 180_000, 2019: 175_000, 2023: 182_134}
DUAL_TRACK_2023_PRES_GOV_TURNOUT_GAP = DUAL_TRACK_PRES_GOV_GAP[2023]  # 182,134 · OPPORTUNITY FOR CONSOLIDATION
GOV_TREND_AUDIT: dict[int, dict[str, int]] = {
    2015: {"total": HIST_D3_2015["total"], "lead": HIST_D3_2015["lead"]},
    2019: {"total": HIST_D3_2019["total"], "lead": HIST_D3_2019["lead"]},
    2023: {"total": HIST_D3_2023["total"], "lead": HIST_D3_2023["lead"]},
}
PRES_TREND_AUDIT: dict[int, dict[str, int]] = {
    y: {
        "total": GOV_TREND_AUDIT[y]["total"] + DUAL_TRACK_PRES_GOV_GAP[y],
        "lead": max(
            0,
            int(round(GOV_TREND_AUDIT[y]["lead"] * (GOV_TREND_AUDIT[y]["total"] + DUAL_TRACK_PRES_GOV_GAP[y]) / GOV_TREND_AUDIT[y]["total"])),
        ),
    }
    for y in (2015, 2019, 2023)
}
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
        return pd.DataFrame(columns=["first_name", "last_name", "lga", "ward", "pu_id", "number"])
    norm = {str(c).strip().lower().replace(" ", "_"): c for c in raw.columns}

    def col(*candidates: str) -> str | None:
        for k in candidates:
            if k in norm:
                return norm[k]
        return None

    c_fn = col("first_name", "firstname", "fname")
    c_ln = col("last_name", "lastname", "surname", "lname")
    c_lga = col("lga", "lga_name", "ward_lga")
    c_ward = col("ward", "ward_name", "wardname", "ward_code", "polling_ward")
    c_pu = col("pu_id", "polling_unit", "polling_unit_id", "polling_unit_code", "pu", "unit_id", "unit")
    c_num = col("number", "phone", "msisdn", "phone_number")
    if not (c_fn and c_ln and c_lga):
        return pd.DataFrame(columns=["first_name", "last_name", "lga", "ward", "pu_id", "number"])
    ward_series = raw[c_ward].astype(str).fillna("") if c_ward else pd.Series([""] * len(raw), index=raw.index)
    pu_series = raw[c_pu].astype(str).fillna("") if c_pu else pd.Series([""] * len(raw), index=raw.index)
    out = pd.DataFrame(
        {
            "first_name": raw[c_fn].astype(str).fillna(""),
            "last_name": raw[c_ln].astype(str).fillna(""),
            "lga": raw[c_lga].astype(str).fillna(""),
            "ward": ward_series,
            "pu_id": pu_series,
            "number": raw[c_num].astype(str).fillna("") if c_num else "",
        }
    )
    return out[out["first_name"].str.len() > 0]


@st.cache_data(ttl=90, show_spinner=False)
def _discover_first_valid_csv_in_lake_dir() -> str | None:
    """First lexicographic .csv under the lake that yields at least one normalized voter row."""
    d = KADUNA_DATA_2027_DIR
    if not d.is_dir():
        return None
    candidates = sorted(p for p in d.iterdir() if p.is_file() and p.suffix.lower() == ".csv")
    for p in candidates:
        if p.resolve() == _REPO_VOTER_DB_CSV and not os.environ.get("GCSLC_VOTER_DB"):
            continue
        try:
            sniff = pd.read_csv(p, nrows=96)
            if sniff.empty or len(sniff.columns) == 0:
                continue
            norm = _normalize_voter_df(sniff)
            if not norm.empty:
                return str(p.resolve())
        except Exception:
            continue
    return None


def _resolve_voter_db_csv() -> Path:
    env = os.environ.get("GCSLC_VOTER_DB")
    if env:
        return Path(env).expanduser().resolve()
    discovered = _discover_first_valid_csv_in_lake_dir()
    if discovered:
        return Path(discovered)
    return (KADUNA_DATA_2027_DIR / "voter_db.csv").resolve()


VOTER_DB_CSV = _resolve_voter_db_csv()


# UI / sidebar: keep only a small head in RAM (1.5M-safe virtualized ingest).
_VOTER_DB_HEAD_DEFAULT = 256
_SWOT_CSV_MAX_ROWS = 200_000


_EMPTY_VOTER_COLS = ["first_name", "last_name", "lga", "ward", "pu_id", "number"]


@st.cache_data(show_spinner=False)
def _load_voter_db(csv_path: str, nrows: int = _VOTER_DB_HEAD_DEFAULT) -> pd.DataFrame:
    p = Path(csv_path)
    if not p.is_file():
        return pd.DataFrame(columns=_EMPTY_VOTER_COLS)
    if p.resolve() == _REPO_VOTER_DB_CSV and not os.environ.get("GCSLC_VOTER_DB"):
        return pd.DataFrame(columns=_EMPTY_VOTER_COLS)
    try:
        cap = max(8, min(int(nrows), 50_000))
        raw = pd.read_csv(p, nrows=cap)
    except Exception:
        return pd.DataFrame(columns=_EMPTY_VOTER_COLS)
    return _normalize_voter_df(raw)


@st.cache_data(show_spinner=False)
def _load_voter_raw_for_swot(csv_path: str) -> pd.DataFrame:
    """Capped CSV read for optional party/trend columns (memory-safe vs full 1.5M)."""
    p = Path(csv_path)
    if not p.is_file():
        return pd.DataFrame()
    if p.resolve() == _REPO_VOTER_DB_CSV and not os.environ.get("GCSLC_VOTER_DB"):
        return pd.DataFrame()
    try:
        return pd.read_csv(p, nrows=_SWOT_CSV_MAX_ROWS)
    except Exception:
        return pd.DataFrame()


# 2023 governorship razor-thin benchmark (APC − PDP), per tactical directive
MARGIN_2023_APC_PDP = V_2023_APC - V_2023_PDP  # 10,806
NEON_WARNING_ORANGE = "#FF6B35"
OPPOSITION_PULSE_PARTIES: tuple[str, ...] = ("PDP", "LP", "ADC", "SDP")


def _df_norm_col_map(raw: pd.DataFrame) -> dict[str, str]:
    return {str(c).strip().lower().replace(" ", "_"): c for c in raw.columns}


def _opposition_growth_pulse_flags(raw: pd.DataFrame) -> dict[str, bool]:
    """
    Red pulse when the 1.5M voter CSV shows Growth for an opposition node.
    Uses optional columns: node_trend / trend / signal / growth / status + party / affiliation.
    If a trend column has 'growth' but no party column, all four opposition lights go red.
    """
    out = {p: False for p in OPPOSITION_PULSE_PARTIES}
    if raw.empty or len(raw.columns) == 0:
        return out
    norm = _df_norm_col_map(raw)
    trend_keys = (
        "node_trend",
        "trend",
        "signal",
        "swot_signal",
        "opposition_signal",
        "growth",
        "status",
        "pulse",
    )
    party_keys = (
        "party",
        "party_affiliation",
        "opposition_node",
        "node_party",
        "affiliation",
        "swot_party",
        "opposition",
    )
    trend_col = next((norm[k] for k in trend_keys if k in norm), None)
    party_col = next((norm[k] for k in party_keys if k in norm), None)
    if not trend_col:
        return out
    mask = raw[trend_col].astype(str).str.lower().str.contains("growth", na=False)
    sub = raw.loc[mask]
    if sub.empty:
        return out
    if party_col:
        for _, row in sub.iterrows():
            pv = str(row[party_col]).strip().upper().replace(" ", "")
            for p in OPPOSITION_PULSE_PARTIES:
                if p in pv or pv == p:
                    out[p] = True
    else:
        for p in OPPOSITION_PULSE_PARTIES:
            out[p] = True
    return out


def _allocate_kaduna_pu_counts() -> list[int]:
    """Split PU_COUNT_KADUNA across LGAs by ballot_boxes weight."""
    weights = [int(r[3]) for r in LGA_ROWS]
    s = float(sum(weights))
    n = PU_COUNT_KADUNA
    fracs = [w / s * n for w in weights]
    counts = [int(x) for x in fracs]
    rem = n - sum(counts)
    order = sorted(range(len(weights)), key=lambda i: fracs[i] - counts[i], reverse=True)
    for k in range(rem):
        counts[order[k % len(order)]] += 1
    return counts


def _build_pu_swot_registry() -> pd.DataFrame:
    """Synthetic 8,012 PU nodes: deterministic margin; battleground if margin < 50."""
    counts = _allocate_kaduna_pu_counts()
    rows: list[dict[str, object]] = []
    pu_seq = 0
    for idx, count in enumerate(counts):
        lga, base_lat, base_lon, _, _ = LGA_ROWS[idx]
        for j in range(count):
            pu_seq += 1
            seed = (0xC1E7_2027 << 16) ^ (idx * 7919) ^ (j * 104729)
            rng = random.Random(seed)
            dlat = rng.uniform(-0.09, 0.09)
            dlon = rng.uniform(-0.09, 0.09)
            margin_votes = int(rng.randint(0, 180))
            rows.append(
                {
                    "pu_id": pu_seq,
                    "LGA": lga,
                    "lat": base_lat + dlat,
                    "lon": base_lon + dlon,
                    "margin_votes": margin_votes,
                    "battleground": margin_votes < 50,
                }
            )
    return pd.DataFrame(rows)


@st.cache_data(show_spinner=False)
def _pu_swot_registry_cached() -> pd.DataFrame:
    return _build_pu_swot_registry()


def _sovereign_shift_velocity_parts() -> tuple[float, float, float, str]:
    """PDP peel, LP peel, APC capture (votes) from 2023 → 1.5M-density 2027 projection."""
    pdp_loss = max(0.0, float(V_2023_PDP - MASTER_2027["PDP"]))
    lp_loss = max(0.0, float(V_2023_LP - MASTER_2027["LP"]))
    apc_gain = max(0.0, float(MASTER_2027["APC"] - V_2023_APC))
    tot = pdp_loss + lp_loss + apc_gain
    if tot <= 0:
        return 0.0, 0.0, 0.0, "Projection parity — no modeled peel (check baselines)."
    return pdp_loss, lp_loss, apc_gain, ""


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


def _executive_dashboard_summary_plain() -> str:
    """Pre-formatted WhatsApp body: 1.5M dashboard + Victory Donut projection figures."""
    m = MASTER_2027
    return (
        "CIEN KADUNA 2027 · 1.5M DASHBOARD SUMMARY\n"
        "Galadiman Ruwa Center (GCSLC) — Executive Gateway\n\n"
        f"• Command target / DB lock: {KADUNA_VOTER_TARGET:,} verified records\n"
        f"• PU lattice: {PU_COUNT_KADUNA:,} nodes · D3 lock: {VOTERS_PER_PU_D3_REQUIREMENT} voters/PU\n"
        f"• Consolidation constant: {CONSOLIDATION_CONSTANT:,}\n"
        "• Victory Donut (2027 projection): APC 1.5M anchor vs opposition nodes\n"
        f"  – PDP (projected): {m['PDP']:,}\n"
        f"  – LP (projected): {m['LP']:,}\n"
        f"  – APC (projected baseline): {m['APC']:,}\n"
        f"• 1.5M density factor: ×{DENSITY_FACTOR:.4f}\n"
        f"• LGA command grid: {LGA_TARGET} LGAs · majority path {LGA_MAJORITY_NEED}/{LGA_TARGET}\n"
        "• OLED command UI: #121212 matte · monospace gold + cyan pulse\n\n"
        "Acknowledge when read — operational cadence only."
    )


def _executive_handshake_gateway_sidebar_html() -> str:
    """Three cyan-pulsing wa.me links — same 1.5M dashboard text; node-specific destination."""
    enc = urllib.parse.quote(_executive_dashboard_summary_plain(), safe="")
    parts: list[str] = []
    for i, e in enumerate(EXECUTIVE_HANDSHAKE_MAP):
        url = f"https://wa.me/{e['wa_me_id']}?text={enc}"
        delay = f"{i * 0.22}s"
        crest = html.escape(f"NODE {e['node_id']} · {e['pillar'].upper()}")
        nm = html.escape(e["name"])
        lab = html.escape(e["label"])
        parts.append(
            f'<a class="exec-wa-pulse-btn" style="animation-delay:{delay}" '
            f'href="{html.escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">'
            f'<span class="exec-wa-line exec-wa-crest">{crest}</span>'
            f'<span class="exec-wa-line exec-wa-name">{nm}</span>'
            f'<span class="exec-wa-line exec-wa-role">{lab}</span>'
            '<span class="exec-wa-line exec-wa-cta">WHATSAPP · 1.5M DASHBOARD SUMMARY</span>'
            "</a>"
        )
    stack = "".join(parts)
    return (
        '<div class="exec-handshake-wrap"><div class="exec-handshake-inner">'
        '<p class="exec-handshake-title">EXECUTIVE GATEWAY · VICTORY DONUT</p>'
        '<p class="exec-handshake-sub">Hard-wired handshake map · tap any node to open WhatsApp with the full '
        "1.5M dashboard summary (paired with the main Victory Donut command target).</p>"
        f'<div class="exec-wa-btn-stack">{stack}</div>'
        '<p class="exec-handshake-foot">Sovereign lane · matte #121212 · monospace gold</p>'
        "</div></div>"
    )


def _html_sovereign_roller_ticker(rolled: int) -> str:
    """High-velocity scrolling lines: Ward/LGA rollups + KADUNA_Data_2027 lake path."""
    vdf = _load_voter_db(str(VOTER_DB_CSV))
    files = _kaduna_data_2027_inventory()
    lake = html.escape(KADUNA_DATA_2027_DIR.name)
    path_ok = KADUNA_DATA_2027_DIR.is_dir()
    n_lines = 42
    tick = int(time.monotonic() * 4) & 0xFFFF
    lines: list[str] = []
    denom = max(12, n_lines)
    base = rolled // denom if rolled else 0
    for i in range(n_lines):
        if not vdf.empty:
            ri = (i + tick) % len(vdf)
            lga = str(vdf.iloc[ri]["lga"]).strip() or "KADUNA"
        else:
            lga = LGA_ROWS[(i + tick) % len(LGA_ROWS)][0]
        wn = 1 + (i * 13 + tick) % 19
        chunk = base + (i % 11) * max(0, rolled // 12000) + (i % 5) * 3
        if rolled <= 0:
            chunk = 0
        else:
            chunk = max(1, min(chunk, rolled))
        fn = files[(i + tick) % len(files)] if files else "—"
        tag = "INGEST_LIVE" if path_ok else "LAKE_PENDING"
        ts = (datetime.now() - timedelta(seconds=min(7200, i * 2))).strftime("%H:%M:%S")
        lines.append(
            '<div class="sovereign-roller-line">'
            f'<span class="sr-ts">[{html.escape(ts)}]</span> '
            f"<strong>{html.escape(lga)}</strong> · Ward {wn} · "
            f'<span class="sr-roll">+{chunk:,}</span> rollup · '
            f"<code>{lake}/{html.escape(fn)}</code> · "
            f'<span class="sr-tag">{html.escape(tag)}</span></div>'
        )
    body = "".join(lines)
    dup = body + body
    return (
        '<div class="sovereign-roller-feed-outer">'
        f'<div class="sovereign-roller-feed-track">{dup}</div></div>'
    )


def _render_sovereign_ingestion_monitor_sidebar() -> None:
    """Slider-driven 1.5M rollup + sovereign roller ticker (sidebar)."""
    st.markdown('<div class="sovereign-ingest-wrap">', unsafe_allow_html=True)
    st.markdown(
        '<p class="sovereign-ingest-title">SOVEREIGN INGESTION MONITOR</p>'
        "<p class=\"sovereign-ingest-sub\">1.5M command pool · Ward/LGA roll-up · "
        f"<code>{html.escape(KADUNA_DATA_2027_DIR.name)}</code> data lake</p>",
        unsafe_allow_html=True,
    )
    st.slider(
        "Chairman rollup sweep (% of 1.5M target)",
        min_value=0,
        max_value=100,
        value=72,
        key="cien_sovereign_roller_pct",
        help="Simulated sovereign ingestion sweep toward the 1,500,000 voter anchor.",
    )
    pct = int(st.session_state.get("cien_sovereign_roller_pct", 0))
    rolled = int(round(KADUNA_VOTER_TARGET * (pct / 100.0)))
    st.markdown(
        '<div class="sovereign-roll-total">'
        '<span class="srt-label">ROLLED INGEST (SIM)</span>'
        f'<span class="srt-val">{rolled:,}</span>'
        f'<span class="srt-of"> / {KADUNA_VOTER_TARGET:,}</span>'
        "</div>",
        unsafe_allow_html=True,
    )
    _render_sovereign_roller_ticker_fragment()
    st.markdown("</div>", unsafe_allow_html=True)


@st.fragment(run_every=timedelta(milliseconds=480))
def _render_sovereign_roller_ticker_fragment() -> None:
    pct = int(st.session_state.get("cien_sovereign_roller_pct", 0))
    rolled = int(round(KADUNA_VOTER_TARGET * (pct / 100.0)))
    st.markdown(_html_sovereign_roller_ticker(rolled), unsafe_allow_html=True)


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
@keyframes sov-trend-2027-velocity-pulse {
  0%, 100% {
    color: #4ADE80 !important;
    text-shadow: 0 0 10px rgba(74, 222, 128, 0.75);
  }
  50% {
    color: #22C55E !important;
    text-shadow: 0 0 22px rgba(34, 197, 94, 0.95), 0 0 36px rgba(22, 163, 74, 0.45);
  }
}
@keyframes clinical-2027-green-shimmer {
  0% { background-position: 0% 50%; box-shadow: 0 0 12px rgba(74, 222, 128, 0.35); }
  50% { background-position: 100% 50%; box-shadow: 0 0 24px rgba(34, 197, 94, 0.65); }
  100% { background-position: 200% 50%; box-shadow: 0 0 14px rgba(74, 222, 128, 0.45); }
}
@keyframes verify-node-pulse {
  0%, 100% { transform: scale(1); box-shadow: 0 0 8px rgba(255, 215, 0, 0.45), 0 0 2px rgba(0, 229, 255, 0.55); filter: brightness(1); }
  50% { transform: scale(1.06); box-shadow: 0 0 18px rgba(0, 229, 255, 0.65), 0 0 6px rgba(255, 215, 0, 0.55); filter: brightness(1.12); }
}
@keyframes exec-wa-cyan-pulse {
  0%, 100% {
    border-color: rgba(0, 229, 255, 0.45) !important;
    box-shadow: 0 0 8px rgba(0, 229, 255, 0.35), inset 0 0 0 1px rgba(255, 215, 0, 0.12);
    color: #00E5FF !important;
  }
  50% {
    border-color: rgba(255, 215, 0, 0.55) !important;
    box-shadow: 0 0 18px rgba(0, 229, 255, 0.55), 0 0 8px rgba(255, 215, 0, 0.25);
    color: #7df9ff !important;
  }
}
@keyframes victory-donut-ring-shimmer {
  0% { background-position: 0% 50%; box-shadow: 0 0 14px rgba(255, 215, 0, 0.35), 0 0 8px rgba(0, 229, 255, 0.25); }
  50% { background-position: 100% 50%; box-shadow: 0 0 28px rgba(0, 229, 255, 0.55), 0 0 18px rgba(255, 215, 0, 0.45); }
  100% { background-position: 200% 50%; box-shadow: 0 0 16px rgba(255, 215, 0, 0.4), 0 0 10px rgba(0, 229, 255, 0.35); }
}
@keyframes victory-donut-gold-breathe {
  0%, 100% { filter: drop-shadow(0 0 6px rgba(255, 215, 0, 0.45)); }
  50% { filter: drop-shadow(0 0 16px rgba(255, 215, 0, 0.85)) drop-shadow(0 0 8px rgba(0, 229, 255, 0.45)); }
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

@keyframes nodal-bar-pulse {
  0%, 100% {
    opacity: 1;
    transform: scaleY(1);
    box-shadow: 0 0 6px rgba(34, 211, 238, 0.45);
  }
  50% {
    opacity: 0.72;
    transform: scaleY(1.28);
    box-shadow: 0 0 14px rgba(6, 182, 212, 0.85);
  }
}
.nodal-stream-rail {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.45rem;
  margin: 0 0 0.45rem 0;
  padding: 0.38rem 0.55rem;
  border-radius: 8px;
  border: 1px solid rgba(34, 211, 238, 0.42);
  background: #121212 !important;
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, 0.35);
}
.nodal-stream-label {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  font-size: 0.58rem !important;
  font-weight: 800 !important;
  letter-spacing: 0.12em !important;
  color: #22D3EE !important;
  text-shadow: 0 0 10px rgba(34, 211, 238, 0.35);
  flex: 1;
  text-align: left;
}
.nodal-stream-bars {
  display: flex;
  gap: 5px;
  align-items: flex-end;
  height: 16px;
}
.nodal-stream-bar {
  width: 5px;
  height: 100%;
  border-radius: 2px;
  background: linear-gradient(180deg, #22D3EE, #06B6D4);
  animation: nodal-bar-pulse 1.05s ease-in-out infinite;
}
.nodal-stream-bar:nth-child(1) { animation-delay: 0s; }
.nodal-stream-bar:nth-child(2) { animation-delay: 0.12s; }
.nodal-stream-bar:nth-child(3) { animation-delay: 0.24s; }
.nodal-stream-bar:nth-child(4) { animation-delay: 0.36s; }
.nodal-stream-bar:nth-child(5) { animation-delay: 0.48s; }

.outreach-command-wrap {
  border-radius: 14px;
  padding: 2px;
  background: #121212 !important;
  border: 1px solid rgba(255, 215, 0, 0.28);
  margin: 1rem 0 0.85rem 0;
}
.outreach-command-inner {
  background: #121212 !important;
  border-radius: 11px;
  padding: 0.85rem 1rem;
  border: 1px solid rgba(255, 215, 0, 0.22);
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
  border: 1px solid rgba(255, 215, 0, 0.28);
  border-radius: 10px;
  background: #121212 !important;
  box-shadow: inset 0 0 12px rgba(255, 215, 0, 0.06);
}
.logistics-feed-track {
  animation: logistics-feed-scroll 12s linear infinite;
}
.logistics-line {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace !important;
  font-size: 0.62rem !important;
  font-weight: 700 !important;
  color: #FFD700 !important;
  padding: 0.38rem 0.6rem;
  border-bottom: 1px solid rgba(255, 215, 0, 0.22);
  line-height: 1.45;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.logistics-line-empty { color: #FFD700 !important; white-space: normal; }
.lt-time { color: rgba(255, 215, 0, 0.62) !important; font-variant-numeric: tabular-nums; }
.lt-name { color: #FFD700 !important; }
.lt-lga { color: rgba(255, 215, 0, 0.85) !important; }
.lt-ward { color: rgba(255, 215, 0, 0.78) !important; font-weight: 700 !important; }
.lt-phone {
  color: #FFD700 !important;
  font-weight: 800 !important;
  font-variant-numeric: tabular-nums;
  letter-spacing: 0.04em;
}
.lt-pu {
  color: rgba(255, 215, 0, 0.92) !important;
  font-weight: 800 !important;
}
.lt-verified {
  color: #22D3EE !important;
  font-weight: 800 !important;
  letter-spacing: 0.05em;
}
.lt-weak {
  color: #67E8F9 !important;
  font-weight: 800 !important;
  letter-spacing: 0.05em;
}
.lt-unverified {
  color: rgba(255, 215, 0, 0.6) !important;
  font-weight: 700 !important;
}
.lt-sep { color: rgba(255, 215, 0, 0.38) !important; padding: 0 0.15rem; }

.live-achievement-wrap {
  background: #121212 !important;
  border: 1px solid rgba(255, 215, 0, 0.28);
  border-radius: 10px;
  padding: 0.48rem 0.5rem 0.55rem 0.5rem;
  margin: 0.55rem 0 0.4rem 0;
}
.live-achievement-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.35rem;
  margin-bottom: 0.35rem;
}
.live-achievement-title {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  color: #FFD700 !important;
  font-size: 0.58rem !important;
  font-weight: 800 !important;
  letter-spacing: 0.1em !important;
  margin: 0 !important;
  flex: 1 1 auto;
  line-height: 1.35 !important;
}
.live-achievement-verify {
  display: flex;
  flex-direction: column;
  gap: 0.28rem;
  flex-shrink: 0;
}
.live-verify-img {
  width: 38px;
  height: 38px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid rgba(0, 229, 255, 0.45);
  background: #0a0a0a;
  animation: verify-node-pulse 2.4s ease-in-out infinite;
}
.live-verify-img:nth-child(2) {
  animation-delay: 0.45s;
}
.live-verify-fallback {
  display: inline-flex;
  width: 38px;
  height: 38px;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  border: 1px dashed rgba(255, 215, 0, 0.35);
  color: #00E5FF !important;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  font-size: 0.55rem !important;
  font-weight: 800 !important;
  background: #0a0a0a;
  animation: verify-node-pulse 2.4s ease-in-out infinite;
}
.live-achievement-line {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  color: #FFD700 !important;
  font-size: 0.56rem !important;
  font-weight: 700 !important;
  line-height: 1.45 !important;
  margin: 0.2rem 0 !important;
  padding-left: 0.1rem;
  border-left: 2px solid rgba(0, 229, 255, 0.35);
}
.live-achievement-sub {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  color: #00E5FF !important;
  font-size: 0.5rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.08em !important;
  margin: 0.35rem 0 0 0 !important;
  opacity: 0.92 !important;
}

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
  border: 1px solid rgba(34, 211, 238, 0.28);
  background: #121212 !important;
  animation: none;
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

/* Executive handshake — three cyan-pulsing WhatsApp gateways (sidebar, #121212) */
.exec-handshake-wrap {
  border-radius: 12px;
  padding: 2px;
  background: linear-gradient(120deg, #121212, #00E5FF, #FFD700, #121212);
  background-size: 260% 100%;
  animation: victory-donut-ring-shimmer 4.5s ease-in-out infinite;
  margin: 0.55rem 0 0.45rem 0;
}
.exec-handshake-inner {
  background: #121212 !important;
  border-radius: 10px;
  padding: 0.52rem 0.5rem 0.58rem 0.5rem;
  border: 1px solid rgba(0, 229, 255, 0.28);
}
.exec-handshake-title {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  color: #FFD700 !important;
  font-size: 0.58rem !important;
  font-weight: 800 !important;
  letter-spacing: 0.1em !important;
  text-align: center !important;
  margin: 0 0 0.32rem 0 !important;
  line-height: 1.35 !important;
}
.exec-handshake-sub {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  color: rgba(255, 215, 0, 0.88) !important;
  font-size: 0.52rem !important;
  font-weight: 700 !important;
  line-height: 1.42 !important;
  margin: 0 0 0.42rem 0 !important;
  text-align: center !important;
}
.exec-handshake-foot {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  color: rgba(0, 229, 255, 0.75) !important;
  font-size: 0.48rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.08em !important;
  text-align: center !important;
  margin: 0.38rem 0 0 0 !important;
}
.exec-wa-btn-stack {
  display: flex;
  flex-direction: column;
  gap: 0.38rem;
  align-items: stretch;
  width: 100%;
}
[data-testid="stSidebar"] .exec-wa-pulse-btn {
  display: block !important;
  text-decoration: none !important;
  border-radius: 9px !important;
  padding: 0.4rem 0.48rem !important;
  text-align: center !important;
  background: rgba(10, 10, 10, 0.98) !important;
  border: 1px solid rgba(0, 229, 255, 0.45) !important;
  box-sizing: border-box !important;
  width: 100% !important;
  animation: exec-wa-cyan-pulse 2.35s ease-in-out infinite !important;
}
[data-testid="stSidebar"] .exec-wa-pulse-btn:hover {
  border-color: rgba(255, 215, 0, 0.55) !important;
  color: #FFD700 !important;
}
.exec-wa-line {
  display: block !important;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  line-height: 1.32 !important;
}
.exec-wa-crest {
  color: #FFD700 !important;
  font-size: 0.54rem !important;
  font-weight: 800 !important;
  letter-spacing: 0.08em !important;
}
.exec-wa-name {
  color: #FFD700 !important;
  font-size: 0.62rem !important;
  font-weight: 800 !important;
  margin-top: 0.12rem !important;
}
.exec-wa-role {
  color: rgba(0, 229, 255, 0.92) !important;
  font-size: 0.56rem !important;
  font-weight: 700 !important;
  margin-top: 0.08rem !important;
}
.exec-wa-cta {
  color: #00E5FF !important;
  font-size: 0.5rem !important;
  font-weight: 800 !important;
  letter-spacing: 0.1em !important;
  margin-top: 0.18rem !important;
}

/* 20.7M buffer — gold on matte black (OLED) */
.buffer-20m-matte {
  background: #121212 !important;
  border: 1px solid rgba(255, 215, 0, 0.38);
  border-radius: 10px;
  padding: 0.42rem 0.55rem;
  margin: 0.35rem 0 0.55rem 0;
  text-align: center;
}
.buffer-20m-gold {
  font-family: 'Goldman', sans-serif !important;
  color: #FFD700 !important;
  font-weight: 700 !important;
  font-size: 0.78rem !important;
  letter-spacing: 0.1em !important;
  margin: 0 !important;
  text-shadow: none !important;
}
.buffer-20m-live {
  color: #00F5FF !important;
  font-weight: 700 !important;
}
.broadcast-switchboard-inner h4 {
  font-family: 'Goldman', sans-serif !important;
  color: #FFD700 !important;
  font-size: 0.82rem !important;
  margin: 0 0 0.45rem 0 !important;
  text-align: center;
  letter-spacing: 0.08em;
}

/* Channel selector — matte #121212, bold gold labels (S24 / OLED) */
.channel-strike-board {
  background: #121212 !important;
  border-radius: 10px;
  border: 1px solid rgba(255, 215, 0, 0.28);
  padding: 0.45rem 0.5rem 0.55rem 0.5rem;
  margin: 0.35rem 0 0.45rem 0;
}
.channel-lane-icons-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 0.35rem;
  margin: 0 0 0.45rem 0;
}
.channel-lane-tile {
  background: #121212 !important;
  border: 1px solid rgba(212, 175, 55, 0.42);
  border-radius: 8px;
  padding: 0.38rem 0.32rem;
  text-align: center;
  font-family: 'Goldman', sans-serif !important;
}
.channel-lane-emoji {
  font-size: 1.15rem;
  line-height: 1.2;
  display: block;
  margin-bottom: 0.12rem;
}
.channel-lane-title {
  color: #FFD700 !important;
  font-weight: 800 !important;
  font-size: 0.62rem !important;
  letter-spacing: 0.04em;
  line-height: 1.25;
  display: block;
}
.channel-lane-sub {
  color: rgba(255, 215, 0, 0.78) !important;
  font-weight: 700 !important;
  font-size: 0.56rem !important;
  margin-top: 0.08rem;
  line-height: 1.2;
  display: block;
}
.channel-lane-tile-active {
  border: 2px solid #00E5FF !important;
  box-shadow:
    0 0 14px rgba(0, 229, 255, 0.48),
    0 0 6px rgba(0, 229, 255, 0.22),
    inset 0 0 0 1px rgba(255, 215, 0, 0.14) !important;
}
[data-testid="stSidebar"] .channel-lane-tile-active .channel-lane-title {
  color: #FFD700 !important;
  text-shadow: 0 0 10px rgba(0, 229, 255, 0.42);
}
[data-testid="stSidebar"] .execute-master-strike-wrap {
  margin-top: 0.45rem;
  margin-bottom: 0.15rem;
}
[data-testid="stSidebar"] .execute-master-strike-wrap button {
  background: #121212 !important;
  color: #FFD700 !important;
  font-weight: 800 !important;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  letter-spacing: 0.06em !important;
  border: 2px solid #FFD700 !important;
  border-radius: 10px !important;
  box-shadow: 0 0 12px rgba(255, 215, 0, 0.22) !important;
}
[data-testid="stSidebar"] .execute-master-strike-wrap button:hover:not(:disabled) {
  border-color: #00E5FF !important;
  box-shadow: 0 0 16px rgba(0, 229, 255, 0.35) !important;
  color: #00E5FF !important;
}
[data-testid="stSidebar"] .execute-master-strike-wrap button:disabled {
  border-color: rgba(255, 215, 0, 0.32) !important;
  color: rgba(255, 215, 0, 0.42) !important;
  box-shadow: none !important;
  opacity: 0.72 !important;
}
.channel-selector-gold-label label,
.channel-selector-gold-label span {
  color: #FFD700 !important;
  font-weight: 800 !important;
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.72rem !important;
  letter-spacing: 0.05em !important;
}
[data-testid="stSidebar"] div[data-baseweb="tag"] {
  background: #1a1a1a !important;
  color: #FFD700 !important;
  border: 1px solid rgba(255, 215, 0, 0.82) !important;
  font-family: 'Goldman', sans-serif !important;
  font-weight: 700 !important;
}
[data-testid="stSidebar"] div[data-baseweb="tag"] span,
[data-testid="stSidebar"] div[data-baseweb="tag"] svg {
  color: #FFD700 !important;
  fill: #FFD700 !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div {
  background-color: #121212 !important;
  border-color: rgba(255, 215, 0, 0.45) !important;
}
[data-testid="stSidebar"] .channel-strike-board [data-testid="stMarkdownContainer"] p {
  color: #FFD700 !important;
  font-weight: 700 !important;
}

/* Sovereign sidebar stack — OLED matte #121212 · bold gold · zero halos */
.sovereign-sidebar-oled-stack {
  background: #121212 !important;
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 10px;
  padding: 0.42rem 0.45rem 0.5rem 0.45rem;
  margin: 0.5rem 0 0.35rem 0;
}
.sovereign-ingest-wrap {
  background: #121212 !important;
  border-bottom: 1px solid rgba(255, 215, 0, 0.18);
  padding: 0 0 0.45rem 0;
  margin: 0 0 0.4rem 0;
}
.sovereign-ingest-title {
  font-family: 'Goldman', sans-serif !important;
  color: #FFD700 !important;
  font-weight: 800 !important;
  font-size: 0.74rem !important;
  letter-spacing: 0.12em !important;
  text-align: center !important;
  margin: 0 0 0.25rem 0 !important;
  text-shadow: none !important;
}
.sovereign-ingest-sub {
  font-family: 'Goldman', sans-serif !important;
  color: rgba(0, 229, 255, 0.88) !important;
  font-size: 0.58rem !important;
  text-align: center !important;
  margin: 0 0 0.4rem 0 !important;
  line-height: 1.35 !important;
}
.sovereign-ingest-sub code {
  color: #FFD700 !important;
  font-weight: 700 !important;
  word-break: break-all;
}
.sovereign-roll-total {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: center;
  gap: 0.25rem 0.45rem;
  font-family: 'Goldman', sans-serif !important;
  margin: 0.35rem 0 0.4rem 0 !important;
}
.sovereign-roll-total .srt-label {
  color: #FFD700 !important;
  font-weight: 800 !important;
  font-size: 0.58rem !important;
  letter-spacing: 0.1em !important;
}
.sovereign-roll-total .srt-val {
  color: #00E5FF !important;
  font-weight: 800 !important;
  font-size: 1.05rem !important;
  font-variant-numeric: tabular-nums;
}
.sovereign-roll-total .srt-of {
  color: rgba(255, 215, 0, 0.82) !important;
  font-weight: 700 !important;
  font-size: 0.62rem !important;
}
@keyframes sovereign-roller-scroll {
  0% { transform: translateY(0); }
  100% { transform: translateY(-50%); }
}
@keyframes cc-shimmer-sweep {
  0% { background-position: 0% 50%; }
  100% { background-position: 200% 50%; }
}
.cc-load-shimmer {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace !important;
  font-size: 0.62rem !important;
  font-weight: 800 !important;
  letter-spacing: 0.18em !important;
  color: #FFD700 !important;
  text-align: center !important;
  padding: 0.45rem 0.5rem !important;
  margin: 0 0 0.45rem 0 !important;
  border-radius: 8px !important;
  border: 1px solid rgba(255, 215, 0, 0.35) !important;
  background: linear-gradient(90deg, #121212 0%, #2a2410 35%, #FFD700 50%, #2a2410 65%, #121212 100%) !important;
  background-size: 220% 100% !important;
  animation: cc-shimmer-sweep 1.1s linear infinite !important;
}
.cc-load-shimmer-inline {
  margin: 0.35rem 0 !important;
  padding: 0.32rem 0.4rem !important;
  font-size: 0.56rem !important;
}
.lake-roller-meta {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace !important;
  font-size: 0.56rem !important;
  font-weight: 700 !important;
  color: #FFD700 !important;
  text-align: center !important;
  margin: 0 0 0.35rem 0 !important;
  line-height: 1.35 !important;
}
.sovereign-roller-feed-outer {
  height: 148px;
  overflow: hidden;
  border: 1px solid rgba(255, 215, 0, 0.28);
  border-radius: 8px;
  background: #121212 !important;
}
.sovereign-roller-feed-track {
  animation: sovereign-roller-scroll 7.5s linear infinite;
}
.sovereign-roller-line {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace !important;
  font-size: 0.6rem !important;
  font-weight: 700 !important;
  color: #FFD700 !important;
  padding: 0.32rem 0.5rem;
  border-bottom: 1px solid rgba(255, 215, 0, 0.12);
  line-height: 1.38 !important;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.sovereign-roller-line strong {
  color: #FFD700 !important;
  font-weight: 800 !important;
}
.sovereign-roller-line code {
  color: #FFD700 !important;
  font-size: 0.58rem !important;
  font-weight: 700 !important;
  word-break: break-all;
}
.sovereign-roller-line .lr-idx {
  color: rgba(255, 215, 0, 0.55) !important;
  font-weight: 800 !important;
  margin-right: 0.35rem;
}
.sovereign-roller-line .sr-ts { color: rgba(255, 215, 0, 0.55) !important; font-weight: 700 !important; }
.sovereign-roller-line .sr-roll { color: #FFD700 !important; font-weight: 800 !important; }
.sovereign-roller-line .sr-tag {
  color: #FFD700 !important;
  font-weight: 800 !important;
  letter-spacing: 0.05em;
}

/* Opposition Threat Radar — kinetic / vibrational / static (no halos) */
.threat-radar-wrap {
  background: #121212 !important;
  border: none !important;
  border-radius: 0;
  padding: 0.35rem 0.15rem 0.45rem 0.15rem;
  margin: 0 !important;
}
.threat-radar-oled .threat-radar-title {
  font-family: 'Goldman', sans-serif !important;
  color: #FFD700 !important;
  font-weight: 800 !important;
  font-size: 0.72rem !important;
  letter-spacing: 0.12em !important;
  text-align: center !important;
  margin: 0 0 0.35rem 0 !important;
  text-shadow: none !important;
}
.sovereign-margin-shield {
  border: 1px solid rgba(239, 68, 68, 0.55);
  border-radius: 8px;
  background: #0a0a0a !important;
  padding: 0.38rem 0.45rem 0.42rem 0.45rem;
  margin: 0 0 0.45rem 0 !important;
  text-align: center !important;
}
.sovereign-margin-shield .sms-label {
  display: block;
  font-family: 'Goldman', sans-serif !important;
  color: #FFD700 !important;
  font-weight: 800 !important;
  font-size: 0.58rem !important;
  letter-spacing: 0.14em !important;
  margin-bottom: 0.12rem !important;
  text-shadow: none !important;
}
.sovereign-margin-shield .sms-val {
  display: block;
  font-family: 'Goldman', sans-serif !important;
  color: #EF4444 !important;
  font-weight: 800 !important;
  font-size: 1.25rem !important;
  font-variant-numeric: tabular-nums;
  line-height: 1.15;
  text-shadow: none !important;
}
.sovereign-margin-shield .sms-sub {
  display: block;
  font-family: 'Goldman', sans-serif !important;
  color: rgba(255, 215, 0, 0.75) !important;
  font-size: 0.54rem !important;
  font-weight: 700 !important;
  margin-top: 0.15rem !important;
}
.threat-radar-row {
  display: flex;
  align-items: flex-start;
  gap: 0.45rem;
  margin: 0.26rem 0;
  font-family: 'Goldman', sans-serif !important;
}
.radar-led {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 0.2rem;
  box-shadow: none !important;
}
.radar-led-pdp-kinetic {
  background: #7F1D1D;
  border: 1px solid #DC2626;
  animation: radar-pdp-kinetic 0.85s ease-in-out infinite;
}
.radar-led-lp-vibe {
  background: #083344;
  border: 1px solid #00E5FF;
  animation: radar-lp-vibrational 0.95s ease-in-out infinite;
}
.radar-led-spoiler-static {
  background: #B45309;
  border: 1px solid #F59E0B;
  animation: none !important;
}
@keyframes radar-pdp-kinetic {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.22); opacity: 0.82; }
}
@keyframes radar-lp-vibrational {
  0%, 100% { transform: scale(1) translateX(0); opacity: 1; }
  25% { transform: scale(1.06) translateX(0.5px); opacity: 0.9; }
  50% { transform: scale(0.94) translateX(-0.5px); opacity: 1; }
  75% { transform: scale(1.04) translateX(0.5px); opacity: 0.92; }
}
.radar-row-text {
  color: #FFD700 !important;
  font-weight: 800 !important;
  font-size: 0.66rem !important;
  line-height: 1.35 !important;
  text-shadow: none !important;
}
.radar-row-text .radar-emoji-hint {
  font-weight: 800 !important;
}
.radar-row-sub {
  display: block;
  color: rgba(255, 215, 0, 0.78) !important;
  font-weight: 700 !important;
  font-size: 0.56rem !important;
  margin-top: 0.06rem;
  text-shadow: none !important;
}

.sovereign-2027-anchor {
  border-top: 1px solid rgba(255, 215, 0, 0.2);
  margin-top: 0.4rem !important;
  padding: 0.4rem 0.35rem 0.1rem 0.35rem !important;
  text-align: center !important;
  font-family: 'Goldman', sans-serif !important;
}
.sovereign-2027-anchor .s27-head {
  display: block;
  color: #FFD700 !important;
  font-weight: 800 !important;
  font-size: 0.62rem !important;
  letter-spacing: 0.12em !important;
  margin-bottom: 0.2rem !important;
  text-shadow: none !important;
}
.sovereign-2027-anchor .s27-line {
  display: block;
  color: rgba(0, 229, 255, 0.9) !important;
  font-weight: 700 !important;
  font-size: 0.58rem !important;
  line-height: 1.4 !important;
}

.payload-preview-head {
  font-family: 'Goldman', sans-serif !important;
  color: #FFD700 !important;
  font-weight: 800 !important;
  font-size: 0.72rem !important;
  margin: 0.35rem 0 0.15rem 0 !important;
}

.csv-payload-compact {
  margin: 0 !important;
  font-size: 0.7rem !important;
}
.csv-payload-compact code {
  color: #00E5FF !important;
  font-weight: 600 !important;
  word-break: break-all;
}
.pu-tactical-line {
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.74rem !important;
  color: rgba(0, 229, 255, 0.92) !important;
  margin: 0 0 0.55rem 0 !important;
  line-height: 1.45 !important;
}
.pu-tactical-line code {
  color: #D4AF37 !important;
  font-size: 0.68rem !important;
}
.kaduna-anchor-emerald {
  color: #046A38 !important;
  font-weight: 800 !important;
  text-shadow: none !important;
}
.pu-box-pack-line {
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.64rem !important;
  margin: 0.4rem 0 0.25rem 0 !important;
  line-height: 1.4 !important;
  border-top: 1px solid rgba(4, 106, 56, 0.35);
  padding-top: 0.4rem !important;
}
.kaduna-emerald-label {
  color: #FFD700 !important;
}
.pu-box-sealed {
  color: #046A38 !important;
  font-weight: 800 !important;
  letter-spacing: 0.06em;
}
.pu-box-await {
  color: #00F5FF !important;
  font-weight: 700 !important;
}
.kaduna-pu-node {
  color: #046A38 !important;
  font-weight: 800 !important;
  letter-spacing: 0.04em;
}
[data-testid="stSidebar"] .kaduna-pu-node {
  color: #046A38 !important;
}
.outreach-velocity-wrap {
  border-radius: 12px;
  border: 1px solid rgba(255, 215, 0, 0.28);
  background: rgba(0, 0, 34, 0.55);
  padding: 0.55rem 0.65rem;
  margin-top: 0.55rem;
}
.d3-audit-wrap {
  border-radius: 14px;
  padding: 3px;
  background: linear-gradient(120deg, #121212, #D4AF37, #00E5FF, #121212);
  background-size: 260% 100%;
  animation: prism-shimmer 16s linear infinite;
  margin: 0.85rem 0 1rem 0;
}
.d3-audit-inner {
  background: linear-gradient(180deg, #0a0a12 0%, #000028 100%);
  border-radius: 11px;
  padding: 0.75rem 0.9rem 0.9rem 0.9rem;
  border: 1px solid rgba(212, 175, 55, 0.35);
}
.d3-audit-inner h3 {
  font-family: 'Goldman', sans-serif !important;
  color: #FFD700 !important;
  margin: 0 0 0.45rem 0;
  font-size: 1rem;
  letter-spacing: 0.06em;
}
.d3-audit-table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.78rem;
  color: #00E5FF !important;
  margin: 0 0 0.55rem 0;
}
.d3-audit-table th {
  color: #FFD700 !important;
  text-align: left;
  padding: 0.35rem 0.45rem;
  border-bottom: 1px solid rgba(212, 175, 55, 0.35);
}
.d3-audit-table td {
  padding: 0.32rem 0.45rem;
  border-bottom: 1px solid rgba(0, 229, 255, 0.12);
}
.d3-red-variance {
  color: #EF4444 !important;
  font-weight: 800 !important;
  letter-spacing: 0.04em;
}
.d3-consolidation-callout {
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.74rem !important;
  color: rgba(0, 229, 255, 0.92) !important;
  margin: 0.35rem 0 0 0 !important;
  line-height: 1.45 !important;
}
.d3-consolidation-callout strong {
  color: #FFD700 !important;
}
.sov-trend-wrap {
  border-radius: 14px;
  padding: 3px;
  background: #121212 !important;
  border: 1px solid rgba(255, 215, 0, 0.3);
  margin: 0.85rem 0 1rem 0;
}
.sov-trend-inner {
  background: #121212 !important;
  border-radius: 11px;
  padding: 0.75rem 0.9rem 0.95rem 0.9rem;
  border: 1px solid rgba(0, 229, 255, 0.2);
}
.sov-trend-gap-row td {
  background: rgba(239, 68, 68, 0.12) !important;
  border-top: 1px solid rgba(239, 68, 68, 0.45) !important;
  border-bottom: 1px solid rgba(255, 215, 0, 0.35) !important;
  font-weight: 700 !important;
}
.sov-trend-gap-number {
  color: #F87171 !important;
  font-variant-numeric: tabular-nums;
}
.sov-trend-gap-opp {
  color: #FFD700 !important;
  letter-spacing: 0.04em;
}
.clinical-2027-gauge-wrap {
  border-radius: 14px;
  padding: 3px;
  background: linear-gradient(120deg, #121212, #FFD700, #00E5FF, #121212);
  background-size: 240% 100%;
  animation: victory-donut-ring-shimmer 2.8s ease-in-out infinite;
  margin-top: 0.55rem;
}
.clinical-2027-gauge-inner {
  background: #121212 !important;
  border-radius: 11px;
  padding: 0.45rem 0.5rem 0.55rem 0.5rem;
  border: 1px solid rgba(0, 229, 255, 0.35);
}
.clinical-2027-gauge-inner .stPlotlyChart {
  margin-bottom: 0 !important;
  animation: victory-donut-gold-breathe 2.6s ease-in-out infinite;
}
.sov-trend-inner h3 {
  font-family: 'Goldman', sans-serif !important;
  color: #FFD700 !important;
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
  letter-spacing: 0.06em;
}
.sov-trend-table {
  width: 100%;
  border-collapse: collapse;
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.74rem;
  margin: 0 0 0.55rem 0;
}
.sov-trend-table th {
  color: #FFD700 !important;
  text-align: left;
  padding: 0.32rem 0.4rem;
  border-bottom: 1px solid rgba(212, 175, 55, 0.35);
}
.sov-trend-table td {
  padding: 0.28rem 0.4rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}
.sov-trend-pres-cell {
  color: #FFD700 !important;
  font-weight: 700 !important;
}
.sov-trend-gov-cell {
  color: #00E5FF !important;
  font-weight: 700 !important;
}
.sov-trend-2027-pulse {
  animation: sov-trend-2027-velocity-pulse 1.25s ease-in-out infinite;
  font-weight: 800 !important;
}
.sov-trend-foot {
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.7rem !important;
  color: rgba(0, 229, 255, 0.88) !important;
  margin: 0.4rem 0 0 0 !important;
  line-height: 1.45 !important;
}
.sov-trend-foot strong {
  color: #FFD700 !important;
}
[data-testid="stSidebar"] .buffer-20m-gold {
  color: #FFD700 !important;
}
[data-testid="stSidebar"] .buffer-20m-live {
  color: #00F5FF !important;
}

/* Razor-thin SWOT pulse — neon warning orange headers (live intelligence) */
.swot-sidebar-wrap {
  background: #121212 !important;
  border: 1px solid rgba(255, 107, 53, 0.45);
  border-radius: 10px;
  padding: 0.5rem 0.55rem 0.6rem 0.55rem;
  margin: 0.5rem 0 0.55rem 0;
}
[data-testid="stSidebar"] .swot-sidebar-wrap .swot-section-title {
  font-family: 'Goldman', sans-serif !important;
  color: #FF6B35 !important;
  font-size: 0.72rem !important;
  font-weight: 800 !important;
  letter-spacing: 0.12em !important;
  margin: 0 0 0.35rem 0 !important;
  text-align: center !important;
  text-shadow: 0 0 10px rgba(255, 107, 53, 0.55), 0 0 20px rgba(255, 80, 0, 0.25) !important;
}
.swot-benchmark-line {
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.62rem !important;
  color: rgba(0, 229, 255, 0.88) !important;
  text-align: center !important;
  margin: 0 0 0.45rem 0 !important;
  line-height: 1.35 !important;
}
.swot-benchmark-line strong {
  color: #FFD700 !important;
}
.swot-lights-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.35rem 0.5rem;
  align-items: center;
}
.swot-light-row {
  display: flex;
  align-items: center;
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.68rem !important;
  font-weight: 700 !important;
  color: #FFD700 !important;
}
.swot-dot {
  width: 11px;
  height: 11px;
  border-radius: 50%;
  display: inline-block;
  margin-right: 0.4rem;
  flex-shrink: 0;
}
@keyframes swot-pulse-red {
  0%, 100% {
    background: #EF4444;
    box-shadow: 0 0 6px #EF4444, 0 0 14px rgba(239, 68, 68, 0.55);
    transform: scale(1);
  }
  50% {
    background: #DC2626;
    box-shadow: 0 0 14px #F87171, 0 0 26px rgba(248, 113, 113, 0.75);
    transform: scale(1.12);
  }
}
@keyframes swot-pulse-stable {
  0%, 100% { opacity: 0.88; }
  50% { opacity: 1; }
}
.swot-dot-red {
  background: #EF4444;
  animation: swot-pulse-red 1.15s ease-in-out infinite;
}
.swot-dot-stable {
  background: #2DD4BF;
  animation: swot-pulse-stable 2.2s ease-in-out infinite;
  box-shadow: 0 0 6px rgba(45, 212, 191, 0.45);
}
.swot-foot {
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.58rem !important;
  color: rgba(255, 215, 0, 0.72) !important;
  margin: 0.45rem 0 0 0 !important;
  text-align: center !important;
  line-height: 1.35 !important;
}

.swot-main-section {
  border-radius: 14px;
  padding: 3px;
  background: #121212 !important;
  border: 1px solid rgba(255, 107, 53, 0.35);
  margin: 0.85rem 0 0.65rem 0;
}
.swot-main-inner {
  background: #121212 !important;
  border-radius: 11px;
  padding: 0.75rem 0.9rem 0.85rem 0.9rem;
  border: 1px solid rgba(255, 107, 53, 0.22);
}
.swot-main-inner h3 {
  font-family: 'Goldman', sans-serif !important;
  color: #FF6B35 !important;
  margin: 0 0 0.5rem 0 !important;
  font-size: 1rem !important;
  letter-spacing: 0.08em !important;
  text-shadow: none !important;
}
.sovereign-shift-label-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.72rem !important;
  color: #00E5FF !important;
  margin-bottom: 0.35rem !important;
}
.sovereign-shift-track {
  display: flex;
  height: 22px;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid rgba(255, 215, 0, 0.28);
  background: #0a0a0a;
}
.sovereign-shift-seg-pdp {
  background: linear-gradient(90deg, #0891B2, #06B6D4);
  transition: width 0.4s ease;
}
.sovereign-shift-seg-lp {
  background: linear-gradient(90deg, #6366F1, #818CF8);
  transition: width 0.4s ease;
}
.sovereign-shift-seg-apc {
  background: linear-gradient(90deg, #D4AF37, #FBBF24);
  transition: width 0.4s ease;
}
.sovereign-shift-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 0.65rem 1rem;
  margin-top: 0.45rem !important;
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.66rem !important;
  color: rgba(255, 215, 0, 0.85) !important;
}
.sovereign-shift-legend span strong { color: #00E5FF !important; }

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


def _command_loading_shimmer_html(*, compact: bool = False) -> str:
    cls = "cc-load-shimmer" + (" cc-load-shimmer-inline" if compact else "")
    return (
        f'<div class="{cls}" role="status" aria-live="polite">'
        "COMMAND CENTER · HYDRATING VIRTUALIZED HEAD…"
        "</div>"
    )


def _build_lake_roller_html(names: list[str], pool_len: int) -> str:
    esc = html.escape
    if not names:
        return (
            '<p class="lake-roller-meta">LAKE OFFLINE · verify ~/Desktop/KADUNA_Data_2027 exists</p>'
            '<div class="sovereign-roller-feed-outer"><div class="sovereign-roller-feed-track">'
            '<div class="sovereign-roller-line"><code>NO FILES IN BOUNDED SCAN</code></div>'
            '<div class="sovereign-roller-line"><code>NO FILES IN BOUNDED SCAN</code></div>'
            "</div></div>"
        )
    lines = "".join(
        f'<div class="sovereign-roller-line"><span class="lr-idx">[{i + 1:04d}]</span><code>{esc(n)}</code></div>'
        for i, n in enumerate(names)
    )
    dup = lines + lines
    meta = (
        f'<p class="lake-roller-meta">VIRTUALIZED · showing {len(names)} / pool {pool_len} '
        f"(cap {KADUNA_LAKE_SCAN_CAP}) · {esc(str(KADUNA_DATA_2027_DIR))}</p>"
    )
    return meta + (
        f'<div class="sovereign-roller-feed-outer"><div class="sovereign-roller-feed-track">{dup}</div></div>'
    )


def _render_kaduna_lake_virtualized_expander() -> None:
    """Bounded filename roller — slider widens window; folder never fully loaded into session."""
    st.session_state.setdefault("cien_lake_roller_n", 72)
    st.session_state.setdefault("cien_lake_roller_tail", False)
    with st.expander("1.5M virtualized roller · KADUNA_Data_2027", expanded=False):
        st.caption(
            f"Single-source lock: {KADUNA_DATA_2027_DIR} · repo voter_db.csv ignored unless GCSLC_VOTER_DB is set."
        )
        st.slider(
            "Names in feed (head / head+tail)",
            min_value=50,
            max_value=200,
            value=72,
            step=5,
            key="cien_lake_roller_n",
            help="Only a bounded scan (2k files max) is held in cache — not the full lake.",
        )
        st.checkbox("Head + tail slice", value=False, key="cien_lake_roller_tail")
        ph = st.empty()
        ph.markdown(_command_loading_shimmer_html(compact=True), unsafe_allow_html=True)
        t0 = time.perf_counter()
        pool = _kaduna_lake_preview_pool()
        elapsed = time.perf_counter() - t0
        ph.empty()
        vis = int(st.session_state.get("cien_lake_roller_n", 72))
        use_tail = bool(st.session_state.get("cien_lake_roller_tail", False))
        shown = _lake_display_slice(pool, vis, use_tail)
        st.markdown(_build_lake_roller_html(shown, len(pool)), unsafe_allow_html=True)
        if elapsed > 0.5:
            st.caption(f"Lake index pull {elapsed:.2f}s — loading shimmer shown while indexing.")


def _live_achievement_monitor_sidebar_html() -> str:
    """Uba Sani Hospital Pulse — verification thumbnails + achievement lines (OLED / #121212)."""
    imgs_html: list[str] = []
    for i, name in enumerate(VERIFY_IMG_NAMES):
        p = _resolve_verification_png(name)
        if p is not None:
            try:
                uri = _png_data_uri(p)
                delay = "0s" if i == 0 else "0.45s"
                imgs_html.append(
                    f'<img class="live-verify-img" style="animation-delay:{delay}" '
                    f'src="{html.escape(uri, quote=True)}" alt="" />'
                )
            except OSError:
                imgs_html.append('<span class="live-verify-fallback" title="Add image_0.png">◇</span>')
        else:
            tag = "0" if i == 0 else "1"
            imgs_html.append(
                f'<span class="live-verify-fallback" title="Place {html.escape(name)} in assets/">V{tag}</span>'
            )
    verify_col = '<div class="live-achievement-verify">' + "".join(imgs_html) + "</div>"
    return (
        '<div class="live-achievement-wrap">'
        '<div class="live-achievement-head">'
        '<p class="live-achievement-title">LIVE ACHIEVEMENT MONITOR (2023-DATE)<br/>'
        "<span style=\"color:#00E5FF;font-weight:800;\">Uba Sani Hospital Pulse</span></p>"
        f"{verify_col}"
        "</div>"
        '<p class="live-achievement-line">Bola Tinubu Specialist Hospital (300 Beds)</p>'
        '<p class="live-achievement-line">23 LGAs Road Projects (785km)</p>'
        '<p class="live-achievement-line">300k Children Back in School</p>'
        '<p class="live-achievement-sub">Visual verification nodes · pulse active</p>'
        "</div>"
    )


def _nodal_stream_rail_html() -> str:
    return (
        '<div class="nodal-stream-rail" aria-label="Nodal stream">'
        '<span class="nodal-stream-label">NODAL STREAM: ACTIVE</span>'
        '<span class="nodal-stream-bars" aria-hidden="true">'
        '<span class="nodal-stream-bar"></span><span class="nodal-stream-bar"></span>'
        '<span class="nodal-stream-bar"></span><span class="nodal-stream-bar"></span>'
        '<span class="nodal-stream-bar"></span>'
        "</span></div>"
    )


def _ticker_column_map(df: pd.DataFrame) -> dict[str, str]:
    return {str(c).strip().lower().replace(" ", "_"): c for c in df.columns}


_PHONE_COL_CANDIDATES: tuple[str, ...] = (
    "phone",
    "mobile",
    "telephone",
    "tel",
    "msisdn",
    "gsm",
    "phone_number",
    "phone_no",
    "mobile_no",
    "contact",
    "whatsapp",
    "number",
)

_PU_COL_CANDIDATES: tuple[str, ...] = (
    "pu_id",
    "polling_unit",
    "polling_unit_id",
    "polling_unit_code",
    "polling_unit_name",
    "pu_code",
    "pu",
    "unit",
    "unit_id",
)


def _ticker_resolve_phone_column(norm: dict[str, str]) -> str | None:
    for k in _PHONE_COL_CANDIDATES:
        if k in norm:
            return norm[k]
    for nk, orig in norm.items():
        if any(x in nk for x in ("phone", "mobile", "tel", "gsm", "msisdn", "contact", "whatsapp")):
            return orig
    return None


def _ticker_resolve_pu_column(norm: dict[str, str]) -> str | None:
    for k in _PU_COL_CANDIDATES:
        if k in norm:
            return norm[k]
    for nk, orig in norm.items():
        if any(x in nk for x in ("pu", "polling_unit", "unit_id", "polling", "poll_unit")):
            return orig
    return None


def _ticker_resolve_name_parts(norm: dict[str, str], row: pd.Series) -> str:
    def pick(*keys: str) -> str | None:
        for k in keys:
            if k in norm:
                v = str(row[norm[k]]).strip()
                if v:
                    return v
        return None

    fn = pick("first_name", "firstname", "fname", "first")
    ln = pick("last_name", "lastname", "surname", "lname", "last")
    if fn and ln:
        return f"{fn} {ln}"
    one = pick("full_name", "name", "voter_name", "fullname")
    if one:
        return one
    if fn:
        return fn
    if ln:
        return ln
    return "—"


def _ticker_resolve_lga(norm: dict[str, str], row: pd.Series) -> str:
    for k in ("lga", "lga_name", "ward_lga", "local_government", "lga_name_", "__audit_source_lga"):
        if k in norm:
            v = str(row[norm[k]]).strip()
            if v:
                return v
    for nk, orig in norm.items():
        if "lga" in nk:
            v = str(row[orig]).strip()
            if v:
                return v
    return "—"


def _obfuscate_phone_ticker(raw: object) -> str:
    """Sovereign display: first 6 digits + masked middle + last 2 (e.g. 234803XXX64)."""
    digits = "".join(c for c in str(raw) if c.isdigit())
    if not digits:
        return "—"
    if len(digits) <= 6:
        return "X" * len(digits)
    if len(digits) < 8:
        return digits[:6] + "XX"
    return digits[:6] + "X" * (len(digits) - 8) + digits[-2:]


def _is_verified_phone(raw: object) -> bool:
    digits = "".join(c for c in str(raw) if c.isdigit())
    return len(digits) >= 10


def _phone_integrity_status(raw: object) -> tuple[str, str]:
    """
    Nodal Integrity status lock:
    - ACTIVE: >= 10 digits
    - WEAK SIGNAL: 7-9 digits
    - REVIEW: < 7 digits or missing
    """
    digits = "".join(c for c in str(raw) if c.isdigit())
    n = len(digits)
    if n >= 10:
        return ("ACTIVE", "lt-verified")
    if n >= 7:
        return ("WEAK SIGNAL", "lt-weak")
    return ("REVIEW", "lt-unverified")


def _logistics_ticker_line(name: str, lga: str, pu_id: str, phone_obf: str, status: str, status_cls: str) -> str:
    """National model: [NAME] | [LGA] | PU-ID:[ID] | VERIFIED:[PHONE] | [STATUS]."""
    safe_name = name or "UNKNOWN NAME"
    safe_lga = lga or "UNKNOWN LGA"
    safe_pu = pu_id or "PU-UNMAPPED"
    safe_phone = phone_obf or "000000XXX00"
    return (
        '<div class="logistics-line">'
        f'<span class="lt-name">{html.escape(safe_name)}</span>'
        '<span class="lt-sep">|</span>'
        f'<span class="lt-lga">{html.escape(safe_lga)}</span>'
        '<span class="lt-sep">|</span>'
        f'<span class="lt-pu">PU-ID: {html.escape(safe_pu)}</span>'
        '<span class="lt-sep">|</span>'
        f'<span class="lt-phone">VERIFIED: +{html.escape(safe_phone)}</span>'
        '<span class="lt-sep">|</span>'
        f'<span class="{status_cls}">{html.escape(status)}</span>'
        "</div>"
    )


@st.cache_data(ttl=90, show_spinner=False)
def _load_lga_cien_realtime_audit_rows(max_rows_per_file: int = 50) -> pd.DataFrame:
    """Deep-scan: read first 50 rows from each LGA .xlsx file via openpyxl."""
    d = KADUNA_DATA_2027_DIR
    if not d.is_dir():
        return pd.DataFrame()
    frames: list[pd.DataFrame] = []
    files = sorted(p for p in d.iterdir() if p.is_file() and p.suffix.lower() == ".xlsx")
    # Sovereign sync priority: critical LGAs first, then the rest of the lake.
    priority_lgas = [x[0] for x in LGA_ROWS]
    priority_map = {
        "".join(ch for ch in name.lower() if ch.isalnum()): idx
        for idx, name in enumerate(priority_lgas)
    }

    def _priority_key(p: Path) -> tuple[int, int, str]:
        stem_norm = "".join(ch for ch in p.stem.lower() if ch.isalnum())
        best_idx = len(priority_map)
        for lga_norm, idx in priority_map.items():
            if lga_norm and lga_norm in stem_norm:
                best_idx = min(best_idx, idx)
        is_non_priority = 0 if best_idx < len(priority_map) else 1
        return (is_non_priority, best_idx, p.name.lower())

    files = sorted(files, key=_priority_key)
    for p in files:
        try:
            raw = pd.read_excel(p, nrows=max_rows_per_file, engine="openpyxl")
        except Exception:
            continue
        if raw.empty:
            continue
        raw["__audit_source_file"] = p.name
        raw["__audit_source_lga"] = p.stem.replace("_", " ").strip()
        frames.append(raw)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def _read_ticker_sample_from_active_file(n_sample: int = 10) -> pd.DataFrame:
    """
    National handshake ticker source:
    - Preferred: deep-scan first 50 rows per LGA .xlsx (openpyxl), then sample.
    - Fallback: active bound file sample.
    """
    deep = _load_lga_cien_realtime_audit_rows(50)
    if not deep.empty:
        k = min(max(1, int(n_sample)), len(deep))
        return deep.sample(n=k, random_state=None)
    p = VOTER_DB_CSV
    if not p.is_file():
        return pd.DataFrame()
    if p.resolve() == _REPO_VOTER_DB_CSV and not os.environ.get("GCSLC_VOTER_DB"):
        return pd.DataFrame()
    try:
        if p.suffix.lower() == ".csv":
            raw = pd.read_csv(p, nrows=12_000)
        elif p.suffix.lower() in (".xlsx", ".xls"):
            try:
                raw = pd.read_excel(p, nrows=12_000, engine="openpyxl")
            except TypeError:
                raw = pd.read_excel(p, engine="openpyxl").iloc[:12_000]
            except ImportError:
                return pd.DataFrame()
        else:
            return pd.DataFrame()
    except Exception:
        return pd.DataFrame()
    if raw.empty:
        return pd.DataFrame()
    k = min(max(1, int(n_sample)), len(raw))
    return raw.sample(n=k, random_state=None)


def _build_lake_master_ingest_ticker(n_lines: int = 32) -> str:
    """Deep nodal extraction: 10-row random sample from active file; sovereign phone mask."""
    sample = _read_ticker_sample_from_active_file(10)
    lines: list[str] = []
    if sample.empty:
        pool = _kaduna_lake_preview_pool()
        for _ in range(max(n_lines, 12)):
            if pool:
                mid = f"AUTO-INGEST · {html.escape(random.choice(pool))}"
            else:
                mid = f"MASTER INGESTION · {html.escape(str(KADUNA_DATA_2027_DIR))}"
            lines.append(_logistics_ticker_line(mid, "KADUNA STATE", "PU-UNMAPPED", "000000XXX00", "REVIEW", "lt-unverified"))
        body = "".join(lines)
        return f'<div class="logistics-feed-outer"><div class="logistics-feed-track">{body + body}</div></div>'

    rows: list[pd.Series] = [sample.iloc[i] for i in range(len(sample))]
    norm = _ticker_column_map(sample)
    phone_col = _ticker_resolve_phone_column(norm)
    pu_col = _ticker_resolve_pu_column(norm)

    for _ in range(n_lines):
        r = random.choice(rows)
        name = _ticker_resolve_name_parts(norm, r)
        lga = _ticker_resolve_lga(norm, r)
        pu_id = str(r[pu_col]).strip() if pu_col is not None else "PU-UNKNOWN"
        if not pu_id:
            pu_id = "PU-UNKNOWN"
        if phone_col is not None:
            raw_phone = r[phone_col]
            phone_disp = _obfuscate_phone_ticker(raw_phone)
            if phone_disp == "—":
                phone_disp = "000000XXX00"
            status, status_cls = _phone_integrity_status(raw_phone)
        else:
            phone_disp = "000000XXX00"
            status, status_cls = ("REVIEW", "lt-unverified")
        lines.append(_logistics_ticker_line(name, lga, pu_id, phone_disp, status, status_cls))

    body = "".join(lines)
    dup = body + body
    return f'<div class="logistics-feed-outer"><div class="logistics-feed-track">{dup}</div></div>'


def _build_logistics_feed_html(df: pd.DataFrame, n_lines: int = 28) -> str:
    rail = _nodal_stream_rail_html() if KADUNA_DATA_2027_DIR.is_dir() else ""
    lines: list[str] = []
    if df.empty:
        return rail + _build_lake_master_ingest_ticker(n_lines=max(n_lines, 28))
    for _ in range(n_lines):
        r = df.sample(n=1).iloc[0]
        fn = str(r["first_name"]).strip()
        ln = str(r["last_name"]).strip()
        name = " ".join(x for x in (fn, ln) if x).strip() or "UNKNOWN NAME"
        lga = str(r["lga"]).strip() if "lga" in r.index else "UNKNOWN LGA"
        pu_id = str(r["pu_id"]).strip() if "pu_id" in r.index else "PU-UNKNOWN"
        if not pu_id:
            pu_id = "PU-UNKNOWN"
        if "number" in r.index:
            phone_raw = r["number"]
            phone_disp = _obfuscate_phone_ticker(phone_raw)
            if phone_disp == "—":
                phone_disp = "000000XXX00"
            status, status_cls = _phone_integrity_status(phone_raw)
        else:
            phone_disp = "000000XXX00"
            status, status_cls = ("REVIEW", "lt-unverified")
        lines.append(_logistics_ticker_line(name, lga, pu_id, phone_disp, status, status_cls))
    body = "".join(lines)
    dup = body + body
    return rail + f'<div class="logistics-feed-outer"><div class="logistics-feed-track">{dup}</div></div>'


@st.fragment(run_every=timedelta(seconds=5))
def _render_live_outreach_panel() -> None:
    ph = st.empty()
    ph.markdown(_command_loading_shimmer_html(), unsafe_allow_html=True)
    t0 = time.perf_counter()
    vdf = _load_voter_db(str(VOTER_DB_CSV), nrows=_VOTER_DB_HEAD_DEFAULT)
    elapsed = time.perf_counter() - t0
    ph.empty()
    n = len(vdf)
    src = html.escape(VOTER_DB_CSV.name)
    live_row = (
        f'<span class="status-live">AUTO-INGEST</span> · bound <code>{src}</code> · head {n:,} rows · '
        '<span class="status-synced">MASTER LOOP</span>'
        if n
        else (
            f'<span class="status-live">AUTO-INGEST</span> · scanning '
            f"<code>{html.escape(str(KADUNA_DATA_2027_DIR))}</code> for first valid CSV · "
            f"<code>{src}</code>"
        )
    )
    pu_path = html.escape(str(KADUNA_DATA_2027_DIR))
    path_tag = "PATH OK" if KADUNA_DATA_2027_DIR.is_dir() else "FOLDER PENDING"
    slow_note = ""
    if elapsed > 0.5:
        slow_note = (
            f'<p class="outreach-csv-note" style="margin:0 0 0.45rem 0;">'
            f"<strong>Loading</strong> shimmer armed — CSV head took {elapsed:.2f}s.</p>"
        )
    st.markdown(
        '<div class="outreach-command-wrap"><div class="outreach-command-inner">'
        "<h3>1.5M Voter Tactical Outreach · Multi-Channel Hub</h3>"
        '<p class="live-audit-tag"><span class="status-live">LIVE</span> Nodal Audit · AUTO-INGEST registry head</p>'
        f'{slow_note}'
        f'<p class="pu-tactical-line">Tactical Pulse (PU level · <span class="kaduna-anchor-emerald">Kaduna anchor</span>) · '
        f'<strong class="kaduna-anchor-emerald">{PU_COUNT_KADUNA:,}</strong> PUs · '
        f'<strong>Consolidation constant {CONSOLIDATION_CONSTANT:,}</strong> · '
        f'<strong>{VOTERS_PER_PU_D3_REQUIREMENT}</strong> voters/PU (D3) · '
        f'<code>~/Desktop/KADUNA_Data_2027</code> · <code>{pu_path}</code> · '
        f'<span class="status-synced">{html.escape(path_tag)}</span></p>'
        f'<p class="outreach-csv-note">CSV payload: <strong>{src}</strong> · {live_row}</p>'
        '<p class="outreach-csv-note" style="margin-bottom:0.5rem;">'
        "Logistics ticker: monospace gold · names · LGA · nodal integrity — 12s scroll glide · "
        "5s panel refresh (live data). NODAL STREAM rail when PATH OK."
        "</p>"
        f"{_build_logistics_feed_html(vdf)}"
        "</div></div>",
        unsafe_allow_html=True,
    )


@st.fragment(run_every=timedelta(milliseconds=450))
def _render_outreach_velocity_block() -> None:
    """Real-time outreach velocity after manual PUSH — 1.5M voters across 8,012 Kaduna PU nodes."""
    t0 = st.session_state.get("cien_push_velocity_t0")
    st.markdown('<div class="outreach-velocity-wrap">', unsafe_allow_html=True)
    if t0 is None:
        st.metric(
            "Outreach Velocity (voters/min)",
            "—",
            help="Authorize PUSH TO 1.5M NODES to arm live velocity toward 1.5M voters / 8,012 PUs",
        )
        st.caption(
            f"D3 + Sovereign Trend baselines · standby · consolidation constant {CONSOLIDATION_CONSTANT:,} · "
            f"{PU_COUNT_KADUNA:,} PUs · {VOTERS_PER_PU_D3_REQUIREMENT} voters/PU · "
            f"nominal calc {_VOTERS_PER_PU_KADUNA:,.1f}"
        )
        st.markdown("</div>", unsafe_allow_html=True)
        return
    elapsed = time.monotonic() - float(t0)
    ramp = 1.0 - math.exp(-elapsed / 5.0)
    peak_pu_per_min = min(float(PU_COUNT_KADUNA) * 0.08, 640.0)
    pu_per_min = max(0, int(peak_pu_per_min * ramp + random.uniform(0, 7)))
    voters_per_min = max(0, int(pu_per_min * _VOTERS_PER_PU_KADUNA))
    st.metric(
        "Outreach Velocity",
        f"{voters_per_min:,} voters/min",
        delta=f"{pu_per_min:,} PU handshakes/min · LIVE",
    )
    st.caption(
        f"D3 lock · consolidation constant {CONSOLIDATION_CONSTANT:,} · {PU_COUNT_KADUNA:,} PUs · "
        f"{VOTERS_PER_PU_D3_REQUIREMENT} voters/PU · KADUNA_Data_2027 · multi-channel switchboard"
    )
    st.markdown("</div>", unsafe_allow_html=True)


def _victory_donut_figure() -> go.Figure:
    """
    Victory Donut: 1.5M verified database anchor vs consolidated 2027 opposition nodes
    (MASTER_2027 PDP/LP + micro ADC/SDP tail). OLED: #121212, monospace gold + cyan.
    """
    m = MASTER_2027
    mono = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"
    apc_anchor = int(KADUNA_VOTER_TARGET)
    pdp_v = int(m["PDP"])
    lp_v = int(m["LP"])
    adc_v = max(1, pdp_v // 88)
    sdp_v = max(1, lp_v // 42)
    labels = [
        "APC · 1.5M DB lock",
        "PDP",
        "LP",
        "ADC",
        "SDP",
    ]
    values = [apc_anchor, pdp_v, lp_v, adc_v, sdp_v]
    colors = ["#FFD700", "#00B8D9", "#5EEAD4", "#8899AA", "#64748B"]
    pull = [0.0, 0.07, 0.07, 0.14, 0.14]
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.58,
                sort=False,
                direction="clockwise",
                rotation=68,
                pull=pull,
                domain=dict(x=[0.0, 0.52], y=[0.08, 0.92]),
                marker=dict(colors=colors, line=dict(color="#121212", width=2)),
                textinfo="none",
                hovertemplate="<b>%{label}</b><br>%{value:,} votes · %{percent}<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        title=dict(
            text="Victory Donut · 2027 Command Target<br><sup>1.5M DB anchor vs zone-projected opposition (PDP · LP · micro)</sup>",
            font=dict(family=mono, size=13, color="#FFD700"),
        ),
        paper_bgcolor="#121212",
        plot_bgcolor="#121212",
        font=dict(family=mono, color="#FFD700"),
        uniformtext=dict(minsize=8, mode="hide"),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            x=0.555,
            xanchor="left",
            font=dict(family=mono, size=10, color="#FFD700"),
            bgcolor="rgba(18,18,18,0.9)",
            bordercolor="rgba(0,229,255,0.28)",
            borderwidth=1,
        ),
        margin=dict(t=56, b=20, l=22, r=24),
        height=300,
        annotations=[
            dict(
                text=(
                    f"<b style='color:#FFD700;font-size:17px'>{KADUNA_VOTER_TARGET:,}</b><br>"
                    "<span style='color:#00E5FF;font-size:9px;letter-spacing:0.12em'>COMMAND · DB</span>"
                ),
                x=0.26,
                y=0.5,
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="middle",
                showarrow=False,
            )
        ],
    )
    return fig


def _render_2027_kaduna_anchor_gauge() -> None:
    """2027 Command Target → Victory Donut (1.5M anchor vs consolidated opposition nodes)."""
    st.markdown(
        '<div class="clinical-2027-gauge-wrap"><div class="clinical-2027-gauge-inner">',
        unsafe_allow_html=True,
    )
    st.plotly_chart(
        _victory_donut_figure(),
        use_container_width=True,
        key="cien_kaduna_anchor_2027_victory_donut",
        config={"displayModeBar": False, "responsive": True},
    )
    st.caption(
        f"OLED lock · Matte #121212 · 1.5M database anchor vs MASTER_2027 opposition "
        f"(density ×{DENSITY_FACTOR:.4f}) · {CONSOLIDATION_CONSTANT:,} ÷ {PU_COUNT_KADUNA:,} PUs = "
        f"{VOTERS_PER_PU_D3_REQUIREMENT} voters/PU"
    )
    st.markdown("</div></div>", unsafe_allow_html=True)


def _render_national_contribution_gauge() -> None:
    """15/15 national sync — Kaduna share of 20.7M mandate."""
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=KADUNA_NATIONAL_CONTRIBUTION_PCT,
            number={"suffix": "%", "valueformat": ".2f"},
            title={
                "text": "15/15 NATIONAL SYNC<br><sup>KADUNA → 7.25% OF 20.7M NATIONAL</sup>",
                "font": {"size": 13, "color": GOLD, "family": "Goldman"},
            },
            gauge={
                "axis": {"range": [0, 15], "tickwidth": 1, "tickcolor": "rgba(212,175,55,0.45)"},
                "bar": {"color": KADUNA_EMERALD},
                "bgcolor": "rgba(18,18,18,0.92)",
                "borderwidth": 1,
                "bordercolor": "rgba(212,175,55,0.35)",
                "steps": [
                    {"range": [0, KADUNA_NATIONAL_CONTRIBUTION_PCT], "color": "rgba(4, 106, 56, 0.35)"},
                ],
                "threshold": {
                    "line": {"color": CYAN, "width": 3},
                    "thickness": 0.85,
                    "value": KADUNA_NATIONAL_CONTRIBUTION_PCT,
                },
            },
        )
    )
    fig.update_layout(
        height=268,
        paper_bgcolor="#121212",
        plot_bgcolor="#121212",
        margin=dict(t=56, b=24, l=28, r=28),
        font=dict(family="Goldman", color=GOLD),
    )
    st.plotly_chart(
        fig,
        use_container_width=True,
        key="cien_national_contribution_gauge",
        config={"displayModeBar": False, "responsive": True},
    )
    st.caption(
        f"Matte black (#121212) clinical readout · {BUFFER_20_7M_LABEL} national envelope · "
        f"Kaduna sovereign contribution {KADUNA_NATIONAL_CONTRIBUTION_PCT}%"
    )


def _render_pu_box_pack_sync_block() -> None:
    """Live Nodal Audit — PU box-pack status; SEALED after Ward Captain acknowledgment."""
    st.session_state.setdefault("cien_ward_acknowledged", False)
    ack = bool(st.session_state.get("cien_ward_acknowledged"))
    status_html = (
        '<span class="pu-box-sealed">SEALED</span>'
        if ack
        else '<span class="pu-box-await">AWAITING WARD ACK</span>'
    )
    st.markdown(
        '<p class="pu-box-pack-line kaduna-emerald-label">PU Box-Pack Status · ' + status_html + "</p>",
        unsafe_allow_html=True,
    )
    if not ack:
        if st.button(
            "Ward Captain · acknowledge synchronization",
            key="cien_ward_ack_btn",
            use_container_width=True,
        ):
            st.session_state["cien_ward_acknowledged"] = True
            st.rerun()


@st.fragment(run_every=timedelta(seconds=5))
def _render_live_nodal_sidebar_line() -> None:
    vdf = _load_voter_db(str(VOTER_DB_CSV), nrows=96)
    if vdf.empty:
        st.markdown(
            '<p class="dt-handshake">Live Nodal Audit: <span class="status-live">AUTO-INGEST</span> — '
            f"master loop · <code>{html.escape(VOTER_DB_CSV.name)}</code> · "
            f"<span class=\"status-synced\">NODAL STREAM: ACTIVE</span></p>",
            unsafe_allow_html=True,
        )
        return
    r = vdf.sample(n=1).iloc[0]
    fn = str(r["first_name"]).strip()
    ln = str(r["last_name"]).strip()
    lga = str(r["lga"]).strip()
    ward = str(r["ward"]).strip() if "ward" in r.index else ""
    pu_id = 1 + (abs(hash((fn, ln, lga))) % PU_COUNT_KADUNA)
    ward_bit = f" · <span class=\"kaduna-pu-node\">{html.escape(ward)}</span>" if ward else ""
    st.markdown(
        '<p class="dt-handshake">Live Nodal Audit · <span class="status-synced">SYNCED</span> · '
        f'<span class="kaduna-pu-node">PU-{pu_id:05d}</span> · '
        f"{html.escape(fn)} {html.escape(ln)} · "
        f"{html.escape(lga)}"
        f"{ward_bit}</p>",
        unsafe_allow_html=True,
    )


@st.fragment(run_every=timedelta(milliseconds=400))
def _render_sentiment_sidebar() -> None:
    t0 = st.session_state.get("cien_poll_mono_t0")
    targets = st.session_state.get("cien_poll_targets")
    if t0 is None or targets is None:
        y, n_, u = 34.0, 33.0, 33.0
        subtitle = "NODAL STREAM: ACTIVE · Awaiting PUSH to 1.5M nodes"
        bar_colors = ["#22D3EE", "#06B6D4", "#67E8F9"]
        bar_lines = ["#0e7490", "#0e7490", "#0e7490"]
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
        bar_colors = [TURQ, "#D4AF37", "#8899aa"]
        bar_lines = ["#000033", "#000033", "#000033"]
    fig = go.Figure(
        data=[
            go.Bar(
                x=["Yes", "No", "Undecided"],
                y=[y, n_, u],
                marker=dict(
                    color=bar_colors,
                    line=dict(color=bar_lines, width=1),
                ),
            )
        ]
    )
    fig.update_layout(
        title=dict(text="Live Sentiment Analysis", font=dict(family="Goldman", size=12, color=GOLD)),
        paper_bgcolor="#121212",
        plot_bgcolor="#121212",
        font=dict(family="Goldman", color=GOLD),
        height=210,
        margin=dict(t=32, b=28, l=36, r=12),
        yaxis=dict(range=[0, 100], title="%", gridcolor="rgba(34, 211, 238, 0.18)"),
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


def _html_opposition_threat_radar() -> str:
    """Kinetic SWOT: PDP deep red, LP cyan vibrational, ADC/SDP amber static; margin shield redline."""
    shield = f"{MARGIN_2023_APC_PDP:,}"
    pu = f"{PU_COUNT_KADUNA:,}"
    sync = VOTERS_PER_PU_D3_REQUIREMENT
    tgt = f"{KADUNA_VOTER_TARGET:,}"
    return (
        '<div class="threat-radar-wrap threat-radar-oled">'
        '<p class="threat-radar-title">OPPOSITION THREAT RADAR</p>'
        '<div class="sovereign-margin-shield">'
        '<span class="sms-label">SOVEREIGN MARGIN SHIELD</span>'
        f'<span class="sms-val">{shield}</span>'
        '<span class="sms-sub">Permanent redline · 2023 APC−PDP razor corridor</span>'
        "</div>"
        '<div class="threat-radar-row">'
        '<span class="radar-led radar-led-pdp-kinetic" aria-hidden="true"></span>'
        '<div><span class="radar-row-text">PDP · deep red · kinetic threat</span>'
        '<span class="radar-row-sub">11k-class margin pressure · governorship lock</span></div>'
        "</div>"
        '<div class="threat-radar-row">'
        '<span class="radar-led radar-led-lp-vibe" aria-hidden="true"></span>'
        '<div><span class="radar-row-text">LP · cyan · vibrational pulse</span>'
        '<span class="radar-row-sub">Youth node · harmonic watch</span></div>'
        "</div>"
        '<div class="threat-radar-row">'
        '<span class="radar-led radar-led-spoiler-static" aria-hidden="true"></span>'
        '<div><span class="radar-row-text">ADC · amber · static spoiler</span>'
        '<span class="radar-row-sub">Spoiler lane · fragmentation</span></div>'
        "</div>"
        '<div class="threat-radar-row">'
        '<span class="radar-led radar-led-spoiler-static" aria-hidden="true"></span>'
        '<div><span class="radar-row-text">SDP · amber · static spoiler</span>'
        '<span class="radar-row-sub">Spoiler lane · coalition drift</span></div>'
        "</div>"
        '<div class="sovereign-2027-anchor">'
        '<span class="s27-head">2027 PROJECTION ANCHOR</span>'
        f'<span class="s27-line">{pu} PU target · {sync} syncs/node → {tgt} voters</span>'
        '<span class="s27-line">Command: align every node to 187 handshakes per PU lattice</span>'
        "</div>"
        "</div>"
    )


@st.fragment(run_every=timedelta(seconds=6))
def _render_opposition_threat_radar_sidebar() -> None:
    st.markdown(_html_opposition_threat_radar(), unsafe_allow_html=True)


def _render_razor_thin_swot_shift_block() -> None:
    """Main-panel matte black block: Sovereign Shift / node capture velocity bar."""
    pdp_l, lp_l, apc_g, hint = _sovereign_shift_velocity_parts()
    tot = pdp_l + lp_l + apc_g
    if tot <= 0:
        w_pdp = w_lp = w_apc = 0.0
    else:
        w_pdp = 100.0 * pdp_l / tot
        w_lp = 100.0 * lp_l / tot
        w_apc = 100.0 * apc_g / tot
    src = html.escape(VOTER_DB_CSV.name)
    st.markdown(
        '<div class="swot-main-section"><div class="swot-main-inner">'
        "<h3>RAZOR-THIN SWOT · NODE CAPTURE VELOCITY</h3>"
        '<div class="sovereign-shift-label-row"><span>Sovereign Shift</span>'
        '<span style="color:rgba(255,107,53,0.92);font-size:0.68rem;letter-spacing:0.06em;">LIVE INTELLIGENCE</span></div>'
        '<div class="sovereign-shift-label-row" style="margin-bottom:0.3rem;"><span>1.5M database → razor-thin peel</span>'
        f"<span>{src}</span></div>"
        '<div class="sovereign-shift-track">'
        f'<div class="sovereign-shift-seg-pdp" style="width:{w_pdp:.2f}%;"></div>'
        f'<div class="sovereign-shift-seg-lp" style="width:{w_lp:.2f}%;"></div>'
        f'<div class="sovereign-shift-seg-apc" style="width:{w_apc:.2f}%;"></div>'
        "</div>"
        '<div class="sovereign-shift-legend">'
        f"<span><strong>PDP node peel</strong> · {pdp_l:,.0f}</span>"
        f"<span><strong>LP node peel</strong> · {lp_l:,.0f}</span>"
        f"<span><strong>APC capture</strong> · {apc_g:,.0f}</span>"
        "</div>"
        "</div></div>",
        unsafe_allow_html=True,
    )
    if hint:
        st.caption(hint)


def _d3_lead_total_bar_figure() -> go.Figure:
    """Gold (total) + cyan (lead) — D3 locked historical audit."""
    years = [str(r["year"]) for r in HIST_D3_AUDIT_ROWS]
    totals = [r["total"] for r in HIST_D3_AUDIT_ROWS]
    leads = [r["lead"] for r in HIST_D3_AUDIT_ROWS]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            name="Total votes",
            x=years,
            y=totals,
            marker=dict(color="#D4AF37", line=dict(color="#FFD700", width=1)),
        )
    )
    fig.add_trace(
        go.Bar(
            name="Lead votes",
            x=years,
            y=leads,
            marker=dict(color="#00E5FF", line=dict(color="#00F5FF", width=1)),
        )
    )
    fig.update_layout(
        barmode="group",
        paper_bgcolor=NAVY_DEEP,
        plot_bgcolor=NAVY_DEEP,
        font=dict(family="Goldman", color=GOLD),
        title=dict(
            text="D3 Historical Audit — Lead vs Total (verified baselines)",
            font=dict(size=14, color=GOLD),
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0.5, xanchor="center"),
        yaxis=dict(title="Votes", gridcolor="#003350", tickformat=","),
        xaxis=dict(title=""),
        height=360,
        margin=dict(t=56, b=40, l=48, r=24),
    )
    return fig


def _d3_fragmentation_gap_figure() -> go.Figure:
    """300k vote leakage 2019→2023 as red variance (waterfall)."""
    fig = go.Figure(
        go.Waterfall(
            name="Fragmentation",
            orientation="v",
            measure=["absolute", "relative", "total"],
            x=["2019 total (baseline)", "2019→2023 fragmentation", "2023 total (certified)"],
            y=[
                HIST_D3_2019["total"],
                -D3_FRAGMENTATION_LEAKAGE_2019_2023,
                HIST_D3_2023["total"],
            ],
            text=[
                f"{HIST_D3_2019['total'] / 1e6:.2f}M",
                f"-{D3_FRAGMENTATION_LEAKAGE_2019_2023 // 1000}k",
                f"{HIST_D3_2023['total'] / 1e6:.2f}M",
            ],
            textposition="outside",
            decreasing={"marker": {"color": "#DC2626"}},
            increasing={"marker": {"color": "#22C55E"}},
            totals={"marker": {"color": "#D4AF37"}},
            connector={"line": {"color": "rgba(212,175,55,0.4)"}},
        )
    )
    fig.update_layout(
        title=dict(
            text="Gap Analysis · 300k vote leakage (red variance)",
            font=dict(family="Goldman", size=14, color=GOLD),
        ),
        paper_bgcolor=NAVY_DEEP,
        plot_bgcolor=NAVY_DEEP,
        font=dict(family="Goldman", color=GOLD),
        height=360,
        yaxis=dict(title="Votes", gridcolor="#003350", tickformat=","),
        showlegend=False,
        margin=dict(t=52, b=40, l=48, r=24),
    )
    return fig


def _render_d3_historical_audit() -> None:
    """D3 locked figures + consolidation goal + gap chart."""
    rows_html = "".join(
        f"<tr><td><strong>{r['year']}</strong></td>"
        f"<td>{r['lead']:,}</td><td>{r['total']:,}</td></tr>"
        for r in HIST_D3_AUDIT_ROWS
    )
    leak_k = D3_FRAGMENTATION_LEAKAGE_2019_2023 // 1000
    st.markdown(
        '<div class="d3-audit-wrap"><div class="d3-audit-inner">'
        "<h3>D3 · OFFICIAL HISTORICAL AUDIT (LOCKED)</h3>"
        '<table class="d3-audit-table">'
        "<thead><tr><th>Year</th><th>Lead</th><th>Total</th></tr></thead>"
        f"<tbody>{rows_html}</tbody></table>"
        f'<p class="d3-red-variance">Fragmentation indicator · {leak_k}k vote leakage (2019→2023 total decline)</p>'
        f"<p class=\"d3-consolidation-callout\"><strong>2027 Consolidation Constant:</strong> "
        f"{CONSOLIDATION_CONSTANT:,} voters · <strong>{PU_COUNT_KADUNA:,}</strong> Kaduna PUs · "
        f"<strong>{VOTERS_PER_PU_D3_REQUIREMENT}</strong> voters/PU (command lock)</p>"
        "</div></div>",
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            _d3_lead_total_bar_figure(),
            use_container_width=True,
            key="cien_d3_lead_total",
            config={"displayModeBar": False, "responsive": True},
        )
    with c2:
        st.plotly_chart(
            _d3_fragmentation_gap_figure(),
            use_container_width=True,
            key="cien_d3_gap_waterfall",
            config={"displayModeBar": False, "responsive": True},
        )


def _lead_share_pct(lead: int, total: int) -> str:
    if total <= 0:
        return "—"
    return f"{100.0 * lead / total:.2f}%"


def _sov_trend_dual_bars_figure() -> go.Figure:
    """Presidential (gold) vs Governorship (cyan); 2027 projection bars = shimmering green pair."""
    years = ["2015", "2019", "2023", "2027"]
    pres_totals = [
        PRES_TREND_AUDIT[2015]["total"],
        PRES_TREND_AUDIT[2019]["total"],
        PRES_TREND_AUDIT[2023]["total"],
        CONSOLIDATION_CONSTANT,
    ]
    gov_totals = [
        GOV_TREND_AUDIT[2015]["total"],
        GOV_TREND_AUDIT[2019]["total"],
        GOV_TREND_AUDIT[2023]["total"],
        CONSOLIDATION_CONSTANT,
    ]
    pres_colors = ["#D4AF37", "#D4AF37", "#D4AF37", "#4ADE80"]
    gov_colors = ["#00E5FF", "#00E5FF", "#00E5FF", "#34D399"]
    pres_lines = ["#FFD700", "#FFD700", "#FFD700", "#22C55E"]
    gov_lines = ["#00F5FF", "#00F5FF", "#00F5FF", "#16A34A"]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            name="Presidential · total valid",
            x=years,
            y=pres_totals,
            marker=dict(color=pres_colors, line=dict(color=pres_lines, width=1)),
        )
    )
    fig.add_trace(
        go.Bar(
            name="Governorship · total valid",
            x=years,
            y=gov_totals,
            marker=dict(color=gov_colors, line=dict(color=gov_lines, width=1)),
        )
    )
    fig.update_layout(
        barmode="group",
        paper_bgcolor=NAVY_DEEP,
        plot_bgcolor=NAVY_DEEP,
        font=dict(family="Goldman", color=GOLD),
        title=dict(
            text="Dual-track totals · 2027 = clinical anchor (green projection)",
            font=dict(size=13, color=GOLD),
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0.5, xanchor="center"),
        yaxis=dict(title="Total valid votes", gridcolor="#003350", tickformat=","),
        xaxis=dict(title=""),
        height=360,
        margin=dict(t=56, b=40, l=52, r=24),
    )
    return fig


def _render_sovereign_trend_audit() -> None:
    """2015/2019/2023 dual-track table + 2023 Sovereign Gap row; charts carry 2027 projection."""
    rows_parts: list[str] = []
    for y in (2015, 2019, 2023):
        p = PRES_TREND_AUDIT[y]
        g = GOV_TREND_AUDIT[y]
        rows_parts.append(
            f"<tr><td><strong>{y}</strong></td><td class=\"sov-trend-pres-cell\">Presidential</td>"
            f"<td class=\"sov-trend-pres-cell\">{p['total']:,}</td>"
            f"<td class=\"sov-trend-pres-cell\">{p['lead']:,}</td>"
            f"<td class=\"sov-trend-pres-cell\">{_lead_share_pct(p['lead'], p['total'])}</td></tr>"
            f"<tr><td><strong>{y}</strong></td><td class=\"sov-trend-gov-cell\">Governorship</td>"
            f"<td class=\"sov-trend-gov-cell\">{g['total']:,}</td>"
            f"<td class=\"sov-trend-gov-cell\">{g['lead']:,}</td>"
            f"<td class=\"sov-trend-gov-cell\">{_lead_share_pct(g['lead'], g['total'])}</td></tr>"
        )
    gap = DUAL_TRACK_2023_PRES_GOV_TURNOUT_GAP
    assert PRES_TREND_AUDIT[2023]["total"] - GOV_TREND_AUDIT[2023]["total"] == gap
    rows_parts.append(
        "<tr class=\"sov-trend-gap-row\">"
        "<td><strong>2023</strong></td>"
        "<td class=\"sov-trend-gap-label\">Sovereign Gap (Pres − Gov total valid)</td>"
        f"<td class=\"sov-trend-gap-number\">+{gap:,}</td>"
        '<td colspan="2" class="sov-trend-gap-opp">OPPORTUNITY FOR CONSOLIDATION</td>'
        "</tr>"
    )
    rows_html = "".join(rows_parts)
    st.markdown(
        '<div class="sov-trend-wrap"><div class="sov-trend-inner">'
        "<h3>Sovereign Trend Audit · Presidential vs Governorship</h3>"
        '<table class="sov-trend-table">'
        "<thead><tr><th>Year</th><th>Office</th><th>Total valid votes</th>"
        "<th>Lead votes</th><th>Lead party share</th></tr></thead>"
        f"<tbody>{rows_html}</tbody></table>"
        f'<p class="sov-trend-foot"><strong>2027 clinical projection</strong> (1.5M anchor · {PU_COUNT_KADUNA:,} PUs · '
        f"{VOTERS_PER_PU_D3_REQUIREMENT} voters/PU) lives in the <strong>high-velocity gauge</strong> below.</p>"
        "</div></div>",
        unsafe_allow_html=True,
    )
    st.metric(
        "Sovereign Gap 2023 · OPPORTUNITY FOR CONSOLIDATION",
        f"+{gap:,}",
        help="Presidential minus Governorship total valid votes, 2023 — consolidation upside",
    )
    st.plotly_chart(
        _sov_trend_dual_bars_figure(),
        use_container_width=True,
        key="cien_sov_trend_dual",
        config={"displayModeBar": False, "responsive": True},
    )


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
    pu_df = _pu_swot_registry_cached()
    n_bg = int(pu_df["battleground"].sum())
    lga_texts = [
        (
            f"<b>{row.LGA}</b><br>Golden Coordinates: {row.lat:.4f}°N, {row.lon:.4f}°E<br>"
            f"Nodal Strength: {row.nodal}/25 Ballot Box targets<br>"
            f"Ballot boxes (ward density): {row.ballot_boxes}"
        )
        for _, row in df.iterrows()
    ]
    bg = pu_df.loc[pu_df["battleground"]].copy()
    bg_hover = [
        (
            f"<b>PU-{int(r.pu_id):05d}</b> · {html.escape(str(r.LGA))}<br>"
            f"Razor margin: {int(r.margin_votes)} votes<br>"
            f"<span style='color:{NEON_WARNING_ORANGE}'>BATTLEGROUND (&lt;50)</span>"
        )
        for r in bg.itertuples(index=False)
    ]
    fig = go.Figure()
    fig.add_trace(
        go.Scattergeo(
            lat=pu_df["lat"],
            lon=pu_df["lon"],
            mode="markers",
            marker=dict(size=2, color="rgba(0, 229, 255, 0.18)", line=dict(width=0)),
            hoverinfo="skip",
            name=f"{PU_COUNT_KADUNA:,} PU lattice",
        )
    )
    fig.add_trace(
        go.Scattergeo(
            lat=bg["lat"],
            lon=bg["lon"],
            mode="markers",
            text=bg_hover,
            hoverinfo="text",
            marker=dict(
                size=5,
                color=NEON_WARNING_ORANGE,
                line=dict(width=1, color=GOLD),
            ),
            name=f"Battleground PUs (margin &lt; 50) · {n_bg:,}",
        )
    )
    fig.add_trace(
        go.Scattergeo(
            lat=df["lat"],
            lon=df["lon"],
            mode="markers",
            text=lga_texts,
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
            text=(
                f"Micro-Strike Map · {PU_COUNT_KADUNA:,} PU SWOT overlay · "
                f"neon orange = battleground (margin &lt; 50) · {n_bg:,} flagged"
            ),
            font=dict(family="Goldman", size=14, color=GOLD),
        ),
        paper_bgcolor=NAVY_DEEP,
        font=dict(family="Goldman", color=GOLD),
        legend=dict(orientation="h", yanchor="bottom", y=-0.08, x=0.5, xanchor="center"),
        height=560,
        margin=dict(l=0, r=0, t=52, b=36),
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
    st.session_state.setdefault("cien_mc_channels", list(CHANNEL_OPTIONS))
    _migrate_mc_channels_session()

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
        _render_pu_box_pack_sync_block()
        st.markdown("</div></div>", unsafe_allow_html=True)
        st.markdown(
            '<div class="buffer-20m-matte"><p class="buffer-20m-gold">'
            f"{BUFFER_20_7M_LABEL} Buffer · <span class=\"buffer-20m-live\">SECURE · LIVE</span></p></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="polling-prism-wrap"><div class="polling-prism-inner broadcast-switchboard-inner">',
            unsafe_allow_html=True,
        )
        st.markdown("<h4>Broadcast Switchboard</h4>", unsafe_allow_html=True)
        st.caption("CSV payload")
        st.markdown(
            f'<p class="csv-payload-compact"><code>{html.escape(VOTER_DB_CSV.name)}</code></p>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="channel-strike-board">', unsafe_allow_html=True)
        st.markdown('<div class="channel-selector-gold-label">', unsafe_allow_html=True)
        st.multiselect(
            "Strike lanes (select active channels)",
            CHANNEL_OPTIONS,
            key="cien_mc_channels",
            placeholder="Choose lanes for outbound routing",
        )
        st.markdown("</div>", unsafe_allow_html=True)
        _mc_sel = st.session_state.get("cien_mc_channels")
        st.markdown(
            _channel_lane_tiles_html(_mc_sel if isinstance(_mc_sel, list) else None),
            unsafe_allow_html=True,
        )
        st.caption("Active lanes: cyan border · primed for broadcast kinetics.")
        st.markdown("</div>", unsafe_allow_html=True)
        st.text_area(
            "Master Election Day Reminder",
            key="cien_master_reminder",
            height=80,
            placeholder="Chairman reminder — preview below formats for all three strike lanes at once.",
        )
        _rem = (st.session_state.get("cien_master_reminder") or "").strip()
        _all_fm = _format_master_reminder_all_lanes(_rem)
        with st.expander("Multi-channel payloads (preview)", expanded=bool(_rem)):
            if not _rem:
                st.caption("Type a reminder above to generate channel-ready copy.")
            else:
                st.caption("All three strike lanes — SMS/WA, Grassroots, Sovereign — formatted simultaneously.")
                for lab, body in _all_fm.items():
                    st.markdown(
                        f'<p class="payload-preview-head">{html.escape(lab)}</p>',
                        unsafe_allow_html=True,
                    )
                    st.code(body, language=None)
        st.markdown('<div class="execute-master-strike-wrap">', unsafe_allow_html=True)
        _exec_strike = st.button(
            "🚀 EXECUTE MASTER STRIKE",
            disabled=not bool(_rem),
            key="cien_execute_master_strike",
            use_container_width=True,
            help="Requires Chairman reminder text. Activates broadcast kinetics for selected strike lanes.",
        )
        st.markdown("</div>", unsafe_allow_html=True)
        if _exec_strike:
            _lanes = st.session_state.get("cien_mc_channels")
            _lane_txt = ", ".join(_lanes) if isinstance(_lanes, list) and _lanes else "—"
            st.session_state["cien_last_master_strike_ts"] = time.monotonic()
            st.session_state["cien_last_master_strike_reminder"] = _rem
            st.success(
                f"Master strike executed · primed lanes: {_lane_txt}. "
                "Payloads above are ready for outbound routing."
            )
        _render_opposition_threat_radar_sidebar()
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
            st.session_state["cien_push_velocity_t0"] = time.monotonic()
            st.session_state["cien_poll_targets"] = {
                "Yes": float(y),
                "No": float(n),
                "Undecided": u,
            }
        _render_sentiment_sidebar()
        st.markdown("</div></div>", unsafe_allow_html=True)
        st.markdown(_live_achievement_monitor_sidebar_html(), unsafe_allow_html=True)
        st.markdown(_executive_handshake_gateway_sidebar_html(), unsafe_allow_html=True)
        _render_kaduna_lake_virtualized_expander()
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

    _render_d3_historical_audit()
    _render_sovereign_trend_audit()

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

    st.markdown(
        '<div class="section-prism"><h3>OUTREACH VELOCITY · 2027 KADUNA ANCHOR · 15/15 NATIONAL SYNC</h3></div>',
        unsafe_allow_html=True,
    )
    _ov_l, _ov_m, _ov_r = st.columns([1, 1, 1])
    with _ov_l:
        _render_outreach_velocity_block()
    with _ov_m:
        _render_2027_kaduna_anchor_gauge()
    with _ov_r:
        _render_national_contribution_gauge()

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

    _render_razor_thin_swot_shift_block()
    st.markdown(
        '<div class="swot-main-section" style="margin-top:0.2rem;"><div class="swot-main-inner" style="padding:0.5rem 0.85rem 0.6rem 0.85rem;">'
        "<h3 style=\"margin:0 !important;\">MICRO-STRIKE MAP · 2027 PROJECTIONS</h3>"
        '<p style="margin:0.35rem 0 0 0;font-size:0.72rem;color:#00E5FF;font-family:Goldman,sans-serif;">'
        "SWOT lattice: all 8,012 PUs (cyan mist) · battleground = razor margin &lt; 50 votes (neon orange).</p>"
        "</div></div>",
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

    _render_live_outreach_panel()

    _render_executive_variance_forensic()

    st.caption(
        f"CIEN Kaduna 2027 · virtualized voter head · {VOTER_DB_CSV.name} @ {VOTER_DB_CSV.parent} "
        f"(GCSLC_VOTER_DB overrides; repo voter_db.csv not auto-mounted) · "
        f"lake ~/Desktop/KADUNA_Data_2027 · port {os.environ.get('STREAMLIT_SERVER_PORT', '9099')} · "
        "Scientific model narrative for strategic planning only."
    )


if __name__ == "__main__":
    main()
