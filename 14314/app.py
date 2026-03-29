YELLOW_GOLD = "#D4AF37"

import hashlib
import html
from typing import Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pytz
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, time, timedelta, timezone
import json
import urllib.error
import urllib.request
import os
import base64
from urllib.parse import quote

from dateutil.relativedelta import relativedelta

from data_engine import ALL_LGA_RECORDS, STATE_COORDS, records_as_dicts

OFFICE_IDENTITY = "OFFICE OF THE DG/RHGI"
# Bump to force sovereign log wipe + executive 0/8 on next session attach (Management 8 STRIKE).
_STRIKE_SESSION_EPOCH = "14314-EXEC-142-M8-20260328"

st.set_page_config(
    page_title=OFFICE_IDENTITY,
    layout="wide",
    initial_sidebar_state="expanded",
)
if st.session_state.get("_strike_session_epoch") != _STRIKE_SESSION_EPOCH:
    st.session_state._strike_session_epoch = _STRIKE_SESSION_EPOCH
    st.session_state.sovereign_feed_log = [
        f"[INIT] {OFFICE_IDENTITY} · Management 8 · delivery 0/8 · sovereign log cleared.",
    ]
    st.session_state.executive_sync_delivered = False
    st.session_state.executive_sync_handoff_ack = False
    st.session_state.executive_sync_recipient_count = 0
    st.session_state.last_wa_urls = []
    st.session_state.strike_sequential_active = False
    st.session_state.strike_urls_pending = []
    st.session_state.strike_open_index = 0
if "corridor_zone" not in st.session_state:
    st.session_state.corridor_zone = None
if "_prev_corridor_state_key" not in st.session_state:
    st.session_state._prev_corridor_state_key = None
if "cien_tick_idx" not in st.session_state:
    st.session_state.cien_tick_idx = 0
if "map_view" not in st.session_state:
    st.session_state.map_view = None
if "cien_map_candidate" not in st.session_state:
    st.session_state.cien_map_candidate = None
if "dg_corridor" not in st.session_state:
    st.session_state.dg_corridor = None  # None = all Nigeria; else full zone name e.g. "North West"
if "opposition_heatmap" not in st.session_state:
    st.session_state.opposition_heatmap = False
if "threat_monitor" not in st.session_state:
    st.session_state.threat_monitor = bool(st.session_state.get("opposition_heatmap", False))
if "sovereign_feed_log" not in st.session_state:
    st.session_state.sovereign_feed_log = [
        f"[INIT] {OFFICE_IDENTITY} · Management 8 · 144,000-cell / 15/15 model.",
    ]
if "mgmt_demo_phones_text" not in st.session_state:
    st.session_state.mgmt_demo_phones_text = ""
if "mgmt_demo_msg" not in st.session_state:
    st.session_state.mgmt_demo_msg = (
        "RHGI Management/Demonstration — please acknowledge this outreach sync."
    )
if "executive_sync_delivered" not in st.session_state:
    st.session_state.executive_sync_delivered = False
if "executive_sync_handoff_ack" not in st.session_state:
    st.session_state.executive_sync_handoff_ack = False
if "executive_sync_recipient_count" not in st.session_state:
    st.session_state.executive_sync_recipient_count = 0
if "last_wa_urls" not in st.session_state:
    st.session_state.last_wa_urls = []
if "strike_sequential_active" not in st.session_state:
    st.session_state.strike_sequential_active = False
if "strike_urls_pending" not in st.session_state:
    st.session_state.strike_urls_pending = []
if "strike_open_index" not in st.session_state:
    st.session_state.strike_open_index = 0

# RHGI-SWAT-OPPOSITION-77 — global colors (strict DG / SWAT palette).
# RHGI-GOLDMAN palette (mirrors :root CSS variables).
METALLIC_GOLD = YELLOW_GOLD
NAVY_CSS = "#000080"
GOLD = METALLIC_GOLD
NAVY = NAVY_CSS
# Deep Prism Navy (video match — RHGI ABSOLUTE RESTORE-39).
PRISM_NAVY = "#000080"
# RHGI-DG-UNASSAILABLE-MASTER-76 — INEC baseline structure (2023 anchor).
POLLING_UNITS_BASELINE = 176_846
WARDS_BASELINE = 8_809
# Legacy 2023 ward reference (pre–2027 forensic anchor).
AVG_BALLOT_BOXES_PER_WARD = 25
# Statutory 2027 federation-wide ballot-box anchor (SSMI-FORENSIC-2027-106).
BALLOT_BOXES_FEDERATION_2027 = 202_225
BALLOT_BOXES_LEGACY_PRODUCT = AVG_BALLOT_BOXES_PER_WARD * WARDS_BASELINE
FORENSIC_2027_BALLOT_SCALE = BALLOT_BOXES_FEDERATION_2027 / float(BALLOT_BOXES_LEGACY_PRODUCT)
FORENSIC_2027_BALLOT_BASELINE_CAPTION = (
    "Projected 202,225 Ballot Boxes across 8,809 Wards (2027 Baseline)."
)
CANVASSER_BUDGET_ANCHOR_NGN = 30_000
# RHGI TOTAL RESTORE-30 — Sovereign Budget Engine (personnel lines per mandate brief).
SOVEREIGN_CANVASSERS_LINE = 144_000
SOVEREIGN_EDAY_STAFF_LINE = 144_000
# SSMI-PURE-1515-SYNC-137 — single mandate geometry: 144k cells × 15/15 (no legacy “unit rep” tiers).
RHGI_CELL_MODEL_1515 = SOVEREIGN_CANVASSERS_LINE
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
PU_TOTAL = POLLING_UNITS_BASELINE
HARVEST_FOOD_INFLATION_PCT = 12.12
HARVEST_GROWTH_PCT = 4.4
HARVEST_RESERVES_BN_USD = 50.0
# Drill-down order: abbrev → full zone name (matches dff["zone"]).
CORRIDOR_NODES = (
    ("NW", "North West"),
    ("NE", "North East"),
    ("NC", "North Central"),
    ("SW", "South West"),
    ("SS", "South South"),
    ("SE", "South East"),
)
# Decider / Election-Day simulation — Kaduna record anchor (Suleiman node).
KADUNA_SOVEREIGN_RECORD_ANCHOR = 276_060
SULEIMAN_DECIDER_LABEL = f"Suleiman — Kaduna · {KADUNA_SOVEREIGN_RECORD_ANCHOR:,} records (15/15 sync)"
NAT_DECIDER_LABEL = "National coordinator (clear corridor lock)"
DECIDER_RADIO_OPTIONS = (SULEIMAN_DECIDER_LABEL, NAT_DECIDER_LABEL)


def _sync_decider_facilitator_corridor() -> None:
    sel = st.session_state.get("decider_facilitator_radio")
    if sel == SULEIMAN_DECIDER_LABEL:
        st.session_state.dg_corridor = "North West"
        st.session_state.corridor_zone = "North West"
        st.session_state["state_drill_North West"] = "Kaduna"
        st.session_state._prev_corridor_state_key = None
    elif sel == NAT_DECIDER_LABEL:
        st.session_state.dg_corridor = None
        st.session_state.corridor_zone = None
        st.session_state._prev_corridor_state_key = None
# 2027 general election countdown anchor (WAT); adjust if INEC publishes a firm date.
_LAGOS_TZ = pytz.timezone("Africa/Lagos")
_LONDON_TZ = pytz.timezone("Europe/London")
_NYC_TZ = pytz.timezone("America/New_York")
_DUBAI_TZ = pytz.timezone("Asia/Dubai")
# SSMI-SIGNATURE-SYNC-139 — general election: Saturday 16 January 2027 (WAT), 08:00 ballot anchor.
ELECTION_DATETIME_WAT = _LAGOS_TZ.localize(datetime(2027, 1, 16, 8, 0, 0))
ELECTION_TARGET_WAT = _LAGOS_TZ.localize(datetime(2027, 1, 16, 0, 0, 0))
# SSMI-NIGHT-DEPLOY-141 — 20.7M mandate Zero-Hour (general election midnight anchor, WAT).
MANDATE_ZERO_HOUR_WAT = ELECTION_TARGET_WAT
STATIC_CALIBRATION_MONTHS = 9
# Hard research anchor: Mar 26, 2026 → Jan 16, 2027.
ELECTION_CALIBRATION_START_WAT = _LAGOS_TZ.localize(datetime(2026, 3, 26, 0, 0, 0))
PRIMARIES_START_WAT = _LAGOS_TZ.localize(datetime(2026, 4, 23, 0, 0, 0))
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


# SSMI-SIGNATURE-SYNC-139 — real newlines so WhatsApp/SMS render as separate lines on mobile.
RHGI_OUTREACH_SIGNATURE = "From Dr. Sa'ad\nDG/RHGI"
# Verified DG/RHGI E.164 (digits). Used with leadership.json master_command_node_e164.
DG_VERIFIED_E164 = "2348099111515"
# 14314-EXECUTIVE-LOAD-142 — exact directive payload (Unicode apostrophe in Sa’ad); hardcoded for all STRIKE wa.me links.
PRECISION_STRIKE_MESSAGE = (
    "RHGI-SSMI 15/15 sync. Presidential Date: 16-01-2027. All nodes report status. From Dr. Sa\u2019ad, DG/RHGI"
)
EXEC_SYNC_MESSAGE = PRECISION_STRIKE_MESSAGE
STRIKE_LOAD_ID = "14314-EXECUTIVE-LOAD-142"
# Precision Strike — Dr. Ikechukwu (OFFICE OF THE DG/RHGI · STRIKE_LOAD_ID).
PRECISION_STRIKE_IKECHUKWU_E164 = "2348068378633"
# Management 8 strike roster (fallback if executive_sync_recipients.json is unreadable).
_MANAGEMENT_8_E164_FALLBACK: tuple[str, ...] = (
    "2348036948675",
    "2348037910012",
    "2349124572108",
    "2348180649337",
    "13473231693",
    "2348054113010",
    "2348099111515",
    "2348079000900",
)


def _append_outreach_signature(body: str) -> str:
    b = (body or "").rstrip()
    if not b:
        return RHGI_OUTREACH_SIGNATURE
    return f"{b}\n\n{RHGI_OUTREACH_SIGNATURE}"


def _normalize_ng_e164_digits(phone: str) -> str:
    raw = "".join(c for c in (phone or "") if c.isdigit())
    if not raw:
        return ""
    if raw.startswith("234"):
        return raw
    if raw.startswith("0") and len(raw) >= 11:
        return "234" + raw[1:]
    if len(raw) == 10:
        return "234" + raw
    return raw


def _quote_wa_message(message: str) -> str:
    """Percent-encode wa.me ?text= payload (UTF-8 via urllib.parse.quote); required for Unicode / specials (no 404/break)."""
    return quote(message or "", safe="")


def _wa_me_url(phone_e164_digits: str, text: str) -> str:
    """HTTPS https://wa.me/<digits>?text=<quote(message)> — NANP + NG; no whatsapp://."""
    d = _normalize_ng_e164_digits(phone_e164_digits)
    if not d or len(d) < 10:
        d = DG_VERIFIED_E164
    return f"https://wa.me/{d}?text={_quote_wa_message(text)}"


def _wa_me_popup_html(urls: list[str], stagger_ms: int = 550) -> str:
    """Open https://wa.me/ URLs in top window; stagger_ms delays between opens (popup-blocker mitigation)."""
    if not urls:
        return ""
    return (
        "<script>\n"
        "(function(){\n"
        f"var urls={json.dumps(urls)};\n"
        f"var delay={int(stagger_ms)};\n"
        "var root=function(){try{return window.top||window.parent||window;}catch(e){return window;}}();\n"
        "urls.forEach(function(u,i){\n"
        "setTimeout(function(){\n"
        "try{root.open(u,'_blank','noopener,noreferrer');}catch(e){}\n"
        "},i*delay);\n"
        "});\n"
        "})();\n"
        "</script>"
    )


def _sovereign_whatsapp_dm_url(state: str, lga: str) -> str:
    msg = _append_outreach_signature(
        "RHGI Sovereign Direct · "
        f"{state} / {lga}: Apathy conversion reminder — 2023 turnout benchmark locked. "
        "18/25 box target · PU mobilisation."
    )
    return _wa_me_url(DG_VERIFIED_E164, msg)


def _append_sovereign_feed(channel: str, message: str) -> None:
    _ts = datetime.now(_LAGOS_TZ).strftime("%H:%M:%S")
    line = f"[{_ts}] {channel}: {message}"
    _log = st.session_state.get("sovereign_feed_log", [])
    _log.insert(0, line)
    st.session_state.sovereign_feed_log = _log[:100]


# Automated Executive Loop: one https://wa.me/ open per fragment tick, 2s apart (panel + counter in fragment).
_STRIKE_EXEC_LOOP_INTERVAL_SEC = 2
_STRIKE_SEQUENTIAL_INTERVAL = timedelta(seconds=_STRIKE_EXEC_LOOP_INTERVAL_SEC)


def _strike_exec_sidebar_fragment_inner() -> None:
    if st.session_state.get("strike_sequential_active"):
        urls = list(st.session_state.get("strike_urls_pending") or [])
        idx = int(st.session_state.get("strike_open_index", 0))
        total = len(urls)
        if total == 0:
            st.session_state.strike_sequential_active = False
        elif idx >= total:
            st.session_state.strike_sequential_active = False
            st.session_state.executive_sync_delivered = True
            st.session_state.executive_sync_recipient_count = total
            st.session_state.last_wa_urls = list(urls)
            _append_sovereign_feed(
                "Executive Sync",
                f"STRIKE {STRIKE_LOAD_ID} · {total} https://wa.me/ link(s) · RHGI-SSMI sync.",
            )
        else:
            components.html(_wa_me_popup_html([urls[idx]]), height=0)
            st.session_state.strike_open_index = idx + 1
            st.session_state.executive_sync_recipient_count = idx + 1
            if idx + 1 >= total:
                st.session_state.strike_sequential_active = False
                st.session_state.executive_sync_delivered = True
                st.session_state.last_wa_urls = list(urls)
                _append_sovereign_feed(
                    "Executive Sync",
                    f"STRIKE {STRIKE_LOAD_ID} · {total} https://wa.me/ link(s) · RHGI-SSMI sync.",
                )
    _mgmt_total = len(_strike_command_phones())
    active = bool(st.session_state.get("strike_sequential_active"))
    done = bool(st.session_state.get("executive_sync_delivered"))
    _n = int(st.session_state.get("executive_sync_recipient_count", 0))
    if active or done:
        _handoff_ok = bool(st.session_state.get("executive_sync_handoff_ack"))
        _sub = (
            f"Automated Executive Loop — one https://wa.me/ tab every {_STRIKE_EXEC_LOOP_INTERVAL_SEC}s…"
            if active
            else "Executive sync (JAN 16, 2027)"
        )
        _inner = (
            "<div style='font-size:0.78rem;letter-spacing:0.06em;opacity:0.95;'>"
            f"STRIKE {STRIKE_LOAD_ID} — {_sub}</div>"
            f"<div style='font-size:1.05rem;margin-top:8px;'>{_n}/{_mgmt_total} DIRECTIVES DELIVERED</div>"
        )
        if _handoff_ok:
            st.markdown(
                "<div class='rhgi-exec-sync-success-panel' style='border-radius:10px;padding:14px 12px;"
                "text-align:center;font-family:Goldman,sans-serif;color:#ffffff;font-weight:800;'>"
                f"{_inner}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<div style='background:#198754;border:2px solid #146c43;border-radius:10px;padding:14px 12px;"
                "text-align:center;font-family:Goldman,sans-serif;color:#ffffff;font-weight:800;'>"
                f"{_inner}</div>",
                unsafe_allow_html=True,
            )


_LEADERSHIP_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leadership.json")
_EXEC_SYNC_RECIPIENTS_JSON = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "executive_sync_recipients.json"
)


def _load_leadership_config() -> dict:
    with open(_LEADERSHIP_JSON, "r", encoding="utf-8") as fp:
        return json.load(fp)


def _load_management_8_phones() -> list[str]:
    """Management 8 roster from executive_sync_recipients.json (https://wa.me/ digits only)."""
    try:
        with open(_EXEC_SYNC_RECIPIENTS_JSON, "r", encoding="utf-8") as fp:
            data = json.load(fp)
        out: list[str] = []
        seen: set[str] = set()
        for row in data.get("recipients") or []:
            p = str(row.get("phone_e164") or "").strip()
            d = "".join(c for c in p if c.isdigit())
            if len(d) < 10 or d in seen:
                continue
            seen.add(d)
            out.append(d)
        if out:
            return out
    except Exception:
        pass
    return list(_MANAGEMENT_8_E164_FALLBACK)


def _strike_command_phones() -> list[str]:
    """STRIKE_LOAD_ID — full Management 8 list for prefilled https://wa.me/ opens."""
    return list(_load_management_8_phones())


def _build_executive_strike_wa_urls() -> tuple[list[str], Optional[str]]:
    """Python loop: Node 1..N → https://wa.me/?text=… with EXEC_SYNC_MESSAGE (DG/RHGI verified on roster)."""
    roster = _strike_command_phones()
    if DG_VERIFIED_E164 not in roster:
        return [], "Safety hold: DG/RHGI master E.164 (2348099111515) must be present on the Management 8 roster."
    urls: list[str] = []
    for _node_n, _e164 in enumerate(roster, start=1):
        urls.append(_wa_me_url(_e164, EXEC_SYNC_MESSAGE))
    return urls, None


def _post_executive_sync_handoff(phones: list[str], full_message: str) -> tuple[bool, str]:
    """POST handoff to webhooks.executive_sync_handoff or GCSLC_EXEC_SYNC_HANDOFF_URL; empty URL = skip (demo OK)."""
    try:
        cfg = _load_leadership_config()
    except Exception as e:
        return False, str(e)
    wh = (cfg.get("webhooks") or {}).get("executive_sync_handoff", "")
    url = (os.environ.get("GCSLC_EXEC_SYNC_HANDOFF_URL") or wh or "").strip()
    if not url:
        return True, ""
    payload_obj = {
        "tier": "Tier 1: Strategic Management",
        "office_identity": OFFICE_IDENTITY,
        "sender_metadata": OFFICE_IDENTITY,
        "recipients_e164": phones,
        "message": full_message,
        "ts_utc": datetime.now(timezone.utc).isoformat(),
        "push_notification_metadata": {
            "office_identity": OFFICE_IDENTITY,
            "header": OFFICE_IDENTITY,
            "signature": "From Dr. Sa'ad\nDG/RHGI",
            "signature_line_1": "From Dr. Sa'ad",
            "signature_line_2": "DG/RHGI",
        },
    }
    payload = json.dumps(payload_obj).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=payload, method="POST")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=22) as resp:
            code = int(resp.getcode())
            if 200 <= code < 300:
                return True, ""
            return False, f"HTTP {code}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, str(e)


def _dispatch_sovereign_notepad(text: str) -> tuple[list[str], list[str]]:
    """POST notepad payload only to S24 and Convener webhook URLs (env overrides file)."""
    text = (text or "").strip()
    if not text:
        return [], ["empty message"]
    try:
        cfg = _load_leadership_config()
    except Exception as e:
        return [], [f"leadership.json: {e}"]
    wh = cfg.get("webhooks") or {}
    s24_url = (os.environ.get("GCSLC_LEADERSHIP_S24_URL") or wh.get("s24") or "").strip()
    conv_url = (os.environ.get("GCSLC_LEADERSHIP_CONVENER_URL") or wh.get("convener") or "").strip()
    names = [c.get("display_name") for c in cfg.get("contacts", []) if c.get("display_name")]
    payload_obj = {
        "channel": "sovereign_notepad",
        "office_identity": OFFICE_IDENTITY,
        "sender_metadata": OFFICE_IDENTITY,
        "message": _append_outreach_signature(text),
        "ts_utc": datetime.now(timezone.utc).isoformat(),
        "leadership_contacts": names,
        "push_notification_metadata": {
            "office_identity": OFFICE_IDENTITY,
            "header": OFFICE_IDENTITY,
            "signature": "From Dr. Sa'ad\nDG/RHGI",
            "signature_line_1": "From Dr. Sa'ad",
            "signature_line_2": "DG/RHGI",
            "mandate_zero_hour_wat": MANDATE_ZERO_HOUR_WAT.isoformat(),
            "mandate_anchor_votes": NATIONAL_VOTE_TARGET,
        },
    }
    payload = json.dumps(payload_obj).encode("utf-8")
    ok: list[str] = []
    err: list[str] = []
    targets = (("S24 (Dr. Sa'ad)", s24_url), ("Convener", conv_url))
    for label, url in targets:
        if not url:
            err.append(f"{label}: no webhook URL (set in leadership.json or GCSLC_LEADERSHIP_S24_URL / GCSLC_LEADERSHIP_CONVENER_URL)")
            continue
        try:
            req = urllib.request.Request(url, data=payload, method="POST")
            req.add_header("Content-Type", "application/json")
            with urllib.request.urlopen(req, timeout=15) as resp:
                code = getattr(resp, "status", resp.getcode())
                if 200 <= int(code) < 300:
                    ok.append(label)
                else:
                    err.append(f"{label}: HTTP {code}")
        except urllib.error.HTTPError as e:
            err.append(f"{label}: HTTP {e.code}")
        except Exception as e:
            err.append(f"{label}: {e}")
    return ok, err


def _lga_daily_apathy_target(
    registered: float, turnout_2023_rate: float, election_dt: datetime
) -> int:
    """Apathy pool from 2023 benchmark; equal daily slice to election anchor."""
    apathy_pool = max(0.0, float(registered) * (1.0 - min(1.0, max(0.0, float(turnout_2023_rate)))))
    now = datetime.now(_LAGOS_TZ)
    days_left = max(1, int((election_dt - now).total_seconds() / 86400.0))
    return max(1, int(apathy_pool / float(days_left)))


def _sovereign_directive_wa_url(state: str, lga: str, daily_apathy: int) -> str:
    msg = _append_outreach_signature(
        "RHGI SOVEREIGN DIRECTIVE · 15/15 NODE\n"
        f"{state} / {lga}\n"
        f"2023 turnout benchmark: convert {daily_apathy:,} apathy voters TODAY "
        f"(RHGI geometry: {RHGI_CELL_MODEL_1515:,} cells @ 15/15; no alternate rep tier)."
    )
    return _wa_me_url(DG_VERIFIED_E164, msg)


def _rose_heading(text: str) -> None:
    """Corridor section titles — Yellow Gold (strict video / COMPLIANCE-45)."""
    st.markdown(f'<p class="rhgi-corridor-gold-heading">{html.escape(text)}</p>', unsafe_allow_html=True)


def filter_by_corridor(dff: pd.DataFrame, zone: Optional[str]) -> pd.DataFrame:
    """DG Command Hub: None = national; else filter to one geopolitical zone."""
    if zone is None or zone == "":
        return dff
    return dff[dff["zone"] == zone].copy()


def sovereign_budget_engine_breakdown() -> tuple[int, int, int]:
    """(144k + 144k) × ₦30k + 15% misc + 10% contingency → returns (base, after_misc, total) in ₦."""
    base = (SOVEREIGN_CANVASSERS_LINE + SOVEREIGN_EDAY_STAFF_LINE) * SOVEREIGN_UNIT_NGN
    after_misc = round(base * (1.0 + SOVEREIGN_MISC_PCT))
    total = round(after_misc * (1.0 + SOVEREIGN_CONTINGENCY_PCT))
    return base, after_misc, total


def _format_election_countdown(now: datetime) -> str:
    """Months : Days : Hours : Minutes : Seconds until general election anchor (WAT)."""
    now = now.astimezone(_LAGOS_TZ)
    tgt = ELECTION_DATETIME_WAT
    if now >= tgt:
        return "[0] : [0] : [00] : [00] : [00]"
    rd = relativedelta(tgt, now)
    months = rd.years * 12 + rd.months
    days = rd.days
    h = rd.hours
    m = rd.minutes
    s = rd.seconds
    return f"[{months}] : [{days}] : [{h:02d}] : [{m:02d}] : [{s:02d}]"


def _compute_pu_messages_sent_from_payload(payload_df: pd.DataFrame) -> int:
    """Compute reached PU count from Image 11 CSV payload.

    Heuristics:
    - Prefer `pu_lat` + `pu_lon` unique pairs.
    - Else prefer `lat` + `lon` unique pairs.
    - Else fall back to row count.
    """
    if payload_df is None or payload_df.empty:
        return 0

    cols = {str(c).lower(): c for c in payload_df.columns}
    pu_lat = cols.get("pu_lat")
    pu_lon = cols.get("pu_lon")
    if pu_lat is not None and pu_lon is not None:
        unique_pus = payload_df[[pu_lat, pu_lon]].drop_duplicates().shape[0]
        return int(min(unique_pus, PU_TOTAL))

    lat = cols.get("lat")
    lon = cols.get("lon")
    if lat is not None and lon is not None:
        unique_pus = payload_df[[lat, lon]].drop_duplicates().shape[0]
        return int(min(unique_pus, PU_TOTAL))

    unique_pus = payload_df.shape[0]
    return int(min(unique_pus, PU_TOTAL))


def _threshold_gong_data_url() -> Optional[str]:
    """Return assets/threshold_gong.mp3 as a data URL, if present."""
    # Expected location: repo_root/assets/threshold_gong.mp3
    candidates = [
        os.path.join(os.path.dirname(__file__), "..", "assets", "threshold_gong.mp3"),
        os.path.join(os.path.dirname(__file__), "assets", "threshold_gong.mp3"),
    ]
    for p in candidates:
        if os.path.exists(p):
            with open(p, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("ascii")
            return f"data:audio/mpeg;base64,{b64}"
    return None


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
    df["logistics_alert"] = df["canvasser_ratio"] < 16.0
    # Strike priority: high PVC + low 2023 turnout → high-priority strike zones.
    df["strike_priority"] = df["pvc_collection_rate"] * (1.0 - df["turnout_2023_rate"])
    # Ground 2027 party projections to statutory 202,225 ballot-box federation anchor.
    for c in ("apc_2027", "pdp_2027", "lp_2027", "adc_2027"):
        df[c] = (df[c].astype(float) * FORENSIC_2027_BALLOT_SCALE).round().astype(int)
    df["winner_2027"] = df[["apc_2027", "pdp_2027", "lp_2027", "adc_2027"]].max(axis=1)
    df["projected_total"] = df[["apc_2027", "pdp_2027", "lp_2027", "adc_2027"]].sum(axis=1)
    df["winning_margin"] = df["apc_2027"] - df[["pdp_2027", "lp_2027", "adc_2027"]].max(
        axis=1
    )
    df["apc_share_2027"] = (df["apc_2027"] / df["projected_total"].replace(0, 1)) * 100
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


def build_pu_sync_payload(dff: pd.DataFrame) -> pd.DataFrame:
    """Build outreach sync payload: voter identifiers aligned to PU coordinates."""
    cols = ["state", "lga", "zone", "canvassers"]
    out = dff[cols].copy()
    out["voter_name"] = out.apply(
        lambda r: f"VOTER-{str(r['state']).upper()}-{str(r['lga']).upper()}",
        axis=1,
    )
    coords = out.apply(
        lambda r: _lga_lat_lon(str(r["state"]), str(r["lga"])),
        axis=1,
        result_type="expand",
    )
    out["pu_lat"] = coords[0].round(6)
    out["pu_lon"] = coords[1].round(6)
    out = out.rename(columns={"canvassers": "assigned_canvassers"})
    return out[
        ["voter_name", "state", "lga", "zone", "pu_lat", "pu_lon", "assigned_canvassers"]
    ]


def build_heritage_spine_layers() -> tuple[pd.DataFrame, pd.DataFrame, set[str]]:
    """Road layer traces + active states used by SWAT audio gate."""
    route_rows = [
        {"corridor": "AKK Road Section 1", "state": "Abuja", "lat": 9.0765, "lon": 7.3986, "completion_pct": 80},
        {"corridor": "AKK Road Section 1", "state": "Kaduna", "lat": 10.5222, "lon": 7.4384, "completion_pct": 80},
        {"corridor": "AKK Road Section 1", "state": "Kano", "lat": 12.0022, "lon": 8.5920, "completion_pct": 80},
        {"corridor": "Coastal Highway", "state": "Lagos", "lat": 6.5244, "lon": 3.3792, "completion_pct": 62},
        {"corridor": "Coastal Highway", "state": "Ogun", "lat": 6.9094, "lon": 3.2580, "completion_pct": 62},
        {"corridor": "Coastal Highway", "state": "Ondo", "lat": 7.2508, "lon": 5.2103, "completion_pct": 62},
    ]
    route_df = pd.DataFrame(route_rows)
    active_states = set(route_df.loc[route_df["completion_pct"] >= 60, "state"].astype(str).tolist())
    pulse_rows = []
    for _, r in route_df.iterrows():
        pulse_rows.append(
            {
                "state": r["state"],
                "lat": r["lat"],
                "lon": r["lon"],
                "crime_drop_pct": 18.0 + (float(r["completion_pct"]) / 100.0 * 15.0),
            }
        )
    stability_df = pd.DataFrame(pulse_rows)
    return route_df, stability_df, active_states


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
        canvasser_ratio=("canvasser_ratio", "mean"),
        canvassers=("canvassers", "sum"),
    )
    g["lat"] = g["state"].map(lambda s: STATE_COORDS.get(s, (9.0, 8.0))[0])
    g["lon"] = g["state"].map(lambda s: STATE_COORDS.get(s, (9.0, 8.0))[1])
    return g


_SUNSET_SCALE = [[0, "#1A0033"], [0.5, "#B87333"], [1.0, "#FFD700"]]
_LGA_MARKER_INNER = 8 * 1.15
_LGA_MARKER_OUTLINE = 10 * 1.15


def build_k3_nw_triangle_trace() -> go.Scattermapbox:
    """North West Villa — K3 Geopolitical Corridor triangle (Katsina · Kano · Kaduna)."""
    kt, kn, kd = STATE_COORDS["Katsina"], STATE_COORDS["Kano"], STATE_COORDS["Kaduna"]
    lats = [kt[0], kn[0], kd[0], kt[0]]
    lons = [kt[1], kn[1], kd[1], kt[1]]
    return go.Scattermapbox(
        lat=lats,
        lon=lons,
        mode="lines",
        fill="toself",
        fillcolor="rgba(212,175,55,0.16)",
        line=dict(color="#D4AF37", width=2),
        hoverinfo="text",
        hovertext="K3 Triangle (Katsina · Kano · Kaduna) — North West Villa",
        showlegend=False,
        name="K3 Triangle",
    )


def build_cien_audit_rows(dff: pd.DataFrame) -> list[dict]:
    """K3 priority: North West corridor first, then remaining zones; deterministic CIEN status."""
    hmap = build_lga_heatmap_df(dff)
    _k3_order = {"Katsina": 0, "Kano": 1, "Kaduna": 2}
    hmap["_nw"] = (hmap["zone"] == "North West").astype(int)
    hmap["_k3"] = hmap["state"].map(lambda s: _k3_order.get(str(s), 99)).astype(int)
    hmap = hmap.sort_values(
        ["_nw", "_k3", "state", "lga"],
        ascending=[False, True, True, True],
    )
    rows: list[dict] = []
    for _, r in hmap.iterrows():
        h = int(
            hashlib.sha256(f"{r['state']}:{r['lga']}".encode("utf-8")).hexdigest()[:12],
            16,
        )
        verified = (h % 7) != 0
        _cr = float(r.get("canvasser_ratio", 0.0))
        rows.append(
            {
                "state": str(r["state"]),
                "lga": str(r["lga"]),
                "zone": str(r["zone"]),
                "status": "VERIFIED" if verified else "PENDING",
                "verified": verified,
                "swat_15_15": _cr >= 15.0,
                "lat": float(r["lat"]),
                "lon": float(r["lon"]),
            }
        )
    return rows


def enrich_lga_map_metrics(lga_map_df: pd.DataFrame) -> pd.DataFrame:
    out = lga_map_df.copy()
    out["winning_margin"] = pd.to_numeric(out["winning_margin"], errors="coerce")
    out = out.dropna(subset=["lat", "lon", "winning_margin"])
    out["mandate_status"] = out["canvasser_ratio"].apply(
        lambda r: f"{min(15, max(0, int(round(float(r)))) )}/15 Voters Secured"
    )
    out["logistics_fuel"] = (out["canvassers"].astype(float) * CANVASSER_BUDGET_ANCHOR_NGN).round()
    out["opposition_heat"] = (
        pd.to_numeric(out["pdp_2027"], errors="coerce").fillna(0)
        + pd.to_numeric(out["lp_2027"], errors="coerce").fillna(0)
        + pd.to_numeric(out["adc_2027"], errors="coerce").fillna(0)
    )
    _pt = pd.to_numeric(out["projected_total"], errors="coerce").replace(0, 1)
    out["threat_adc_lp_pct"] = (
        100.0
        * (
            pd.to_numeric(out["adc_2027"], errors="coerce").fillna(0)
            + pd.to_numeric(out["lp_2027"], errors="coerce").fillna(0)
        )
        / _pt
    )
    return out


def build_lga_winning_margin_figure(
    lga_map_df: pd.DataFrame,
    zoom: float,
    center: dict,
    threat_monitor: bool = False,
) -> go.Figure:
    _color_col = "threat_adc_lp_pct" if threat_monitor else "winning_margin"
    _cseries = _SUNSET_SCALE
    wm = lga_map_df[_color_col].astype(float)
    wm_min = float(wm.min()) if len(wm) else 0.0
    wm_max = float(wm.max()) if len(wm) else 1.0
    if wm_min == wm_max:
        wm_max = wm_min + 1.0
    fig_lga = px.scatter_mapbox(
        lga_map_df,
        lat="lat",
        lon="lon",
        color=_color_col,
        color_continuous_scale=_cseries,
        range_color=(wm_min, wm_max),
        hover_name="lga",
        hover_data={"state": False, "zone": False, "margin_zone": False, "projected_total": False},
        custom_data=["mandate_status", "logistics_fuel"],
        mapbox_style="carto-positron",
        zoom=zoom,
        center=center,
    )
    fig_lga.update_traces(
        marker=dict(
            size=_LGA_MARKER_INNER,
            color=lga_map_df[_color_col].astype(float).tolist(),
            colorscale=_cseries,
            opacity=0.8,
        ),
        hovertemplate=(
            "<b>%{hovertext}</b>"
            "<br>Mandate Status: %{customdata[0]}"
            "<br>Logistics Fuel: ₦%{customdata[1]:,.0f}"
            "<extra></extra>"
        ),
    )
    _lga_inner = fig_lga.data[0]
    _lga_outline = go.Scattermapbox(
        lat=_lga_inner.lat,
        lon=_lga_inner.lon,
        mode="markers",
        marker=dict(size=_LGA_MARKER_OUTLINE, color="#000080"),
        hoverinfo="skip",
        showlegend=False,
    )
    _k3 = build_k3_nw_triangle_trace()
    fig_lga = go.Figure(
        data=[_lga_outline] + list(fig_lga.data) + [_k3],
        layout=fig_lga.layout,
    )
    _cb_title = (
        "ADC + LP activity (NNPP proxy) · % of LGA vote"
        if threat_monitor
        else "Winning margin"
    )
    fig_lga.update_layout(
        template=None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Goldman, sans-serif", color="#ffffff", size=13),
        font_color="#ffffff",
        hoverlabel=dict(font=dict(family="Goldman, sans-serif", color="#ffffff", size=12)),
        margin=dict(l=0, r=0, t=12, b=0),
        coloraxis_colorbar=dict(
            title=dict(text=_cb_title, font=dict(family="Goldman, sans-serif", color=GOLD, size=12)),
            tickfont=dict(family="Goldman, sans-serif", color="#ffffff", size=11),
            bgcolor="rgba(0,0,128,0.55)",
            bordercolor="rgba(212,175,55,0.35)",
            len=0.72,
        ),
    )
    return fig_lga


df = load_df()
if "decider_facilitator_radio" not in st.session_state:
    st.session_state.decider_facilitator_radio = SULEIMAN_DECIDER_LABEL
if "_decider_kaduna_bootstrapped" not in st.session_state:
    st.session_state._decider_kaduna_bootstrapped = True
    st.session_state.dg_corridor = "North West"
    st.session_state.corridor_zone = "North West"
    st.session_state["state_drill_North West"] = "Kaduna"
    st.session_state._prev_corridor_state_key = None
NATIONAL_TURNOUT_2023_PCT = 100.0 * float(
    df[["apc_2023", "pdp_2023", "lp_2023", "adc_2023"]].sum().sum()
) / max(float(df["registered_voters"].sum()), 1.0)
df_hub_pre = filter_by_corridor(df, st.session_state.get("dg_corridor"))
sovereign_total = float(df["sovereign_yield_gap"].sum())

lagos_tz = _LAGOS_TZ

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap');
    :root {
      --metallic-gold: #D4AF37;
      --rose-gold: #D4AF37;
      --navy: #000080;
      --stark-white: #ffffff;
      --command-box-height: 62px;
      --command-box-radius: 14px;
      --command-gold: #D4AF37;
      --command-silver: #C0C0C0;
      --command-white: #FFFFFF;
      --sec-glow-px: 12px;
      --sec-glow-alpha: 0.26;
      /* SSMI-109 — slow-motion prism ring (DG hub + 8R) */
      --prism-border-rotate: 32s;
    }
    /* SSMI-103 — silver + white border sweep (1.5s cycle) */
    @keyframes rhgiMetalShimmer {
      0% { background-position: 0% 50%; }
      100% { background-position: 200% 50%; }
    }
    /* Yellow Gold inner-pulse + tactical scale (1.0 → 1.03) — non-Seconds countdown cells */
    @keyframes rhgiClockBreathe {
      0%, 100% {
        transform: scale(1);
        box-shadow:
          0 0 calc(var(--sec-glow-px) * 0.35) rgba(212, 175, 55, calc(var(--sec-glow-alpha) * 0.65)),
          inset 0 0 16px rgba(212, 175, 55, 0.18);
      }
      50% {
        transform: scale(1.03);
        box-shadow:
          0 0 calc(var(--sec-glow-px) * 0.85) rgba(212, 175, 55, var(--sec-glow-alpha)),
          inset 0 0 26px rgba(212, 175, 55, 0.32);
      }
    }
    /* DG Corridor + Seconds box — 1s pulse (clock-second sync) */
    @keyframes rhgiSecSyncPulse {
      0%, 100% {
        transform: scale(1);
        box-shadow:
          0 0 8px rgba(212, 175, 55, 0.22),
          inset 0 0 14px rgba(212, 175, 55, 0.14);
      }
      50% {
        transform: scale(1.05);
        box-shadow:
          0 0 20px rgba(212, 175, 55, 0.48),
          inset 0 0 24px rgba(212, 175, 55, 0.26);
      }
    }
    /* Prism corridor — conic silver/gold border rotates in 1.5s */
    @keyframes rhgiCorridorBorderRotate {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    /* Anti-Blue Strike — strip default Streamlit / BaseWeb blues */
    html, body { background: #000080 !important; }
    [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] > .main {
      background: #000080 !important;
    }
    [data-testid="stHeader"], header[data-testid="stHeader"] {
      background: rgba(0, 0, 128, 0.97) !important;
      border-bottom: 1px solid rgba(212, 175, 55, 0.25) !important;
    }
    [data-testid="stDecoration"] { background: #000080 !important; }
    [data-testid="stToolbar"] { background: transparent !important; }
    [data-testid="stSidebarNav"] { background: transparent !important; }
    div[data-testid="stVerticalBlockBorderWrapper"] { border-color: rgba(212,175,55,0.2) !important; }
    [data-baseweb="slider"] [role="slider"] { background: var(--metallic-gold) !important; }
    [data-baseweb="slider"] [data-testid="stThumbValue"] { color: var(--metallic-gold) !important; }
    [data-baseweb="slider"] [style*="background"] { background: rgba(0,0,128,0.6) !important; }
    [data-testid="stSlider"], [data-testid="stSlider"] > label,
    [data-testid="stSlider"] + div { background: transparent !important; }
    .stMetric, [data-testid="stMetricContainer"], [data-testid="stMetricContainer"] > div {
      background: rgba(0,0,128,0.55) !important;
      background-image: none !important;
      border: 1px solid rgba(212,175,55,0.3) !important;
      border-radius: 10px !important;
      box-shadow: none !important;
    }
    .stMetric [data-testid="stMetricValue"] { color: var(--stark-white) !important; }
    .stMetric [data-testid="stMetricLabel"] { color: var(--metallic-gold) !important; }
    [data-testid="stMetricDelta"] { color: var(--metallic-gold) !important; }
    .stAlert, [data-testid="stNotification"], [data-testid="stAlert"] {
      background: rgba(0,0,128,0.65) !important;
      background-image: none !important;
      border: 1px solid rgba(212,175,55,0.35) !important;
      box-shadow: none !important;
    }
    .stInfo { color: var(--stark-white) !important; }
    [data-testid="stAlert"] { color: var(--stark-white) !important; font-family: 'Goldman', sans-serif !important; }
    a, a:visited { color: var(--metallic-gold) !important; }
    a:hover { color: var(--metallic-gold) !important; }
    iframe { background: #000080 !important; }
    /* Kill residual Streamlit / BaseWeb light surfaces */
    [data-testid="stVerticalBlock"] > div,
    [data-testid="stVerticalBlockBorderWrapper"] > div { background-color: transparent !important; }
    div[data-baseweb="select"] > div,
    [data-baseweb="popover"],
    ul[data-testid="stSelectboxVirtualDropdown"],
    [data-baseweb="menu"] { background-color: #000080 !important; color: var(--stark-white) !important; }
    [data-baseweb="menu"] li { font-family: 'Goldman', sans-serif !important; color: var(--stark-white) !important; }
    .stCodeBlock, [data-testid="stCode"] { background: rgba(0,0,128,0.5) !important; }
    /* No white cards: selectbox, popover, expanders, columns */
    [data-testid="stSelectbox"] > div,
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
      background-color: #000080 !important;
      color: var(--stark-white) !important;
      border-color: rgba(212,175,55,0.35) !important;
    }
    [data-testid="stExpander"] details { background: #000080 !important; border: 1px solid rgba(212,175,55,0.25) !important; }
    [data-testid="stExpander"] summary { background: rgba(0,0,128,0.5) !important; color: var(--stark-white) !important; }
    [data-testid="stVerticalBlock"] > div { background-color: transparent !important; }
    div[data-testid="column"] > div { background-color: transparent !important; }
    .stApp {
      background-color: #000080 !important;
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
      background: transparent !important;
      background-color: transparent !important;
      background-image: none !important;
    }
    /* SSMI-COMMAND-PALETTE-FINAL-126 — transparent sidebar internals + no shadows */
    [data-testid="stSidebar"] [data-testid="stSidebarContent"],
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"],
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div,
    [data-testid="stSidebar"] [data-testid="element-container"],
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] [data-testid="stDataFrame"],
    [data-testid="stSidebar"] [data-testid="stDataFrame"] > div,
    [data-testid="stSidebar"] [data-testid="stAlert"],
    [data-testid="stSidebar"] [data-testid="stNotification"],
    [data-testid="stSidebar"] div[data-testid="stVerticalBlockBorderWrapper"] {
      background-color: transparent !important;
      background-image: none !important;
      box-shadow: none !important;
      color: #FFFFFF !important;
      -webkit-text-fill-color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] section,
    [data-testid="stSidebar"] article {
      background: transparent !important;
      background-color: transparent !important;
      background-image: none !important;
    }
    [data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] div,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] [data-baseweb="file-uploader"] div {
      background-color: transparent !important;
      background-image: none !important;
      box-shadow: none !important;
      color: #FFFFFF !important;
      -webkit-text-fill-color: #FFFFFF !important;
    }
    /* SSMI-108 — Category 1–3: brilliant #FFFFFF, no dimming (category titles use SSMI-119 palettes) */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p:not(.rhgi-sidebar-cat--harvest):not(.rhgi-sidebar-cat--infra):not(.rhgi-sidebar-cat--outreach),
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] li,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] strong,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] label span,
    [data-testid="stSidebar"] [data-testid="stCaption"],
    [data-testid="stSidebar"] [data-testid="stCaption"] p,
    [data-testid="stSidebar"] [data-testid="stCaption"] span,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
      color: #ffffff !important;
      opacity: 1 !important;
      -webkit-text-fill-color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stMetric [data-testid="stMetricLabel"],
    [data-testid="stSidebar"] .stMetric [data-testid="stMetricValue"],
    [data-testid="stSidebar"] [data-testid="stMetricDelta"] {
      color: #ffffff !important;
      opacity: 1 !important;
      -webkit-text-fill-color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stMetric,
    [data-testid="stSidebar"] [data-testid="stMetricContainer"] > div {
      background: transparent !important;
      box-shadow: none !important;
      opacity: 1 !important;
    }
    [data-testid="stSidebar"] [data-testid="stSlider"] label,
    [data-testid="stSidebar"] [data-testid="stSlider"] + div,
    [data-testid="stSidebar"] [data-baseweb="slider"] [data-testid="stThumbValue"] {
      color: #ffffff !important;
      opacity: 1 !important;
    }
    /* SSMI-109 — kill sidebar markdown ghosting (Category 1–3) */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
      color: #ffffff !important;
      color: white !important;
      background: transparent !important;
      box-shadow: none !important;
      opacity: 1 !important;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] * {
      color: #ffffff !important;
      color: white !important;
      opacity: 1 !important;
    }
    [data-testid="stSidebar"] [data-testid="stSubheader"],
    [data-testid="stSidebar"] [data-testid="stSubheader"] * {
      color: #FFFFFF !important;
      -webkit-text-fill-color: #FFFFFF !important;
      opacity: 1 !important;
    }
    /* SSMI-COMMAND-CALIBRATION-121 + SSMI-ACCESS-RESTORE-122 — Category 1–3 heading palettes */
    @keyframes rhgiSidebarSilverShimmer {
      0% { background-position: 0% 50%; }
      100% { background-position: 220% 50%; }
    }
    @keyframes rhgiSidebarGoldShimmer {
      0% { background-position: 0% 50%; }
      100% { background-position: 220% 50%; }
    }
    @keyframes rhgiSidebarBrilliantWhiteGlowPulse {
      0%, 100% {
        box-shadow:
          0 0 10px rgba(255, 255, 255, 0.55),
          0 0 22px rgba(255, 255, 255, 0.28),
          inset 0 0 14px rgba(255, 255, 255, 0.06);
      }
      50% {
        box-shadow:
          0 0 26px rgba(255, 255, 255, 0.95),
          0 0 48px rgba(255, 255, 255, 0.42),
          inset 0 0 18px rgba(255, 255, 255, 0.12);
      }
    }
    [data-testid="stSidebar"] p.rhgi-sidebar-cat--harvest {
      font-family: 'Goldman', sans-serif !important;
      font-weight: 800 !important;
      font-size: 1.06rem !important;
      letter-spacing: 0.06em !important;
      margin: 0.55rem 0 0.4rem 0 !important;
      padding: 6px 0 !important;
      line-height: 1.3 !important;
      color: transparent !important;
      -webkit-text-fill-color: transparent !important;
      background: linear-gradient(
        90deg,
        #8a8a8a 0%,
        #a8a8a8 18%,
        #C0C0C0 38%,
        #e4e4e4 50%,
        #C0C0C0 62%,
        #a8a8a8 82%,
        #8a8a8a 100%
      ) !important;
      background-size: 240% 100% !important;
      -webkit-background-clip: text !important;
      background-clip: text !important;
      animation: rhgiSidebarSilverShimmer 9s linear infinite !important;
      opacity: 1 !important;
      filter: none !important;
      text-shadow: none !important;
    }
    [data-testid="stSidebar"] p.rhgi-sidebar-cat--infra {
      font-family: 'Goldman', sans-serif !important;
      font-weight: 800 !important;
      font-size: 1.06rem !important;
      letter-spacing: 0.06em !important;
      margin: 0.55rem 0 0.4rem 0 !important;
      padding: 6px 0 !important;
      line-height: 1.3 !important;
      color: transparent !important;
      -webkit-text-fill-color: transparent !important;
      background: linear-gradient(
        90deg,
        #6b5410 0%,
        #a88620 18%,
        #D4AF37 40%,
        #f5e6a8 50%,
        #D4AF37 60%,
        #a88620 82%,
        #6b5410 100%
      ) !important;
      background-size: 240% 100% !important;
      -webkit-background-clip: text !important;
      background-clip: text !important;
      animation: rhgiSidebarGoldShimmer 9s linear infinite !important;
      opacity: 1 !important;
      filter: none !important;
    }
    [data-testid="stSidebar"] p.rhgi-sidebar-cat--outreach {
      font-family: 'Goldman', sans-serif !important;
      font-weight: 800 !important;
      font-size: 1.06rem !important;
      letter-spacing: 0.06em !important;
      margin: 0.55rem 0 0.4rem 0 !important;
      padding: 6px 0 !important;
      line-height: 1.3 !important;
      color: #0B1F5B !important;
      -webkit-text-fill-color: #0B1F5B !important;
      border-radius: 0 !important;
      border: none !important;
      background: transparent !important;
      background-color: transparent !important;
      background-clip: border-box !important;
      -webkit-background-clip: border-box !important;
      text-shadow:
        0 0 2px rgba(255,255,255,0.95),
        0 0 12px rgba(255,255,255,0.45),
        0 0 20px rgba(255,255,255,0.20) !important;
      animation: none !important;
      opacity: 1 !important;
      filter: none !important;
    }
    [data-testid="stSidebar"] ul li,
    [data-testid="stSidebar"] p:not(.rhgi-sidebar-cat--harvest):not(.rhgi-sidebar-cat--infra):not(.rhgi-sidebar-cat--outreach),
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] strong {
      color: #FFFFFF !important;
      -webkit-text-fill-color: #FFFFFF !important;
      opacity: 1 !important;
      text-shadow: none !important;
    }
    /* Sovereign Vault — 126: dark Prism Navy + silver dashed border; no white fill */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] label,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] label span,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] small {
      color: #FFFFFF !important;
      -webkit-text-fill-color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] [data-testid="stFileUploader"] section,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] [data-baseweb="file-uploader"] {
      background: #000080 !important;
      background-color: #000080 !important;
      background-image: none !important;
      border: 2px dashed #C0C0C0 !important;
      border-style: dashed !important;
      border-radius: 12px !important;
      color: #FFFFFF !important;
      box-shadow: none !important;
    }
    [data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"],
    [data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] > div {
      background: #000080 !important;
      background-color: #000080 !important;
      background-image: none !important;
      border: 2px dashed #C0C0C0 !important;
      border-style: dashed !important;
      border-radius: 12px !important;
      color: #FFFFFF !important;
      box-shadow: none !important;
    }
    [data-testid="stSidebar"] [data-testid="stFileUploader"] svg,
    [data-testid="stSidebar"] [data-testid="stFileUploader"] path {
      stroke: #C0C0C0 !important;
      fill: #C0C0C0 !important;
    }
    [data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"]:hover {
      border-color: #C0C0C0 !important;
      box-shadow: 0 0 12px rgba(192, 192, 192, 0.28) !important;
    }
    [data-testid="stSidebar"] [data-testid="stFileUploader"] input[type="file"] {
      color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] *:not(.rhgi-sidebar-cat--harvest):not(.rhgi-sidebar-cat--infra):not(.rhgi-sidebar-cat--outreach) {
      color: #FFFFFF !important;
      -webkit-text-fill-color: #FFFFFF !important;
      opacity: 1 !important;
      filter: none !important;
      transition: none !important;
    }
    [data-testid="stSidebar"] *::before,
    [data-testid="stSidebar"] *::after {
      opacity: 1 !important;
      filter: none !important;
      transition: none !important;
    }
    .rhgi-forensic-baseline-line {
      color: #ffffff !important;
      opacity: 1 !important;
      -webkit-text-fill-color: #ffffff !important;
      font-family: 'Goldman', sans-serif !important;
      font-size: 0.92rem !important;
      margin: 0 0 10px 0 !important;
    }
    .rhgi-ballot-anchor-white {
      color: #FFFFFF !important;
      -webkit-text-fill-color: #FFFFFF !important;
      font-weight: 900 !important;
      text-shadow: 0 0 8px rgba(255,255,255,0.35) !important;
    }
    .rhgi-voter-impact-divider-wrap,
    .rhgi-divider-widget {
      width: 100%;
      max-width: min(1180px, 100%);
      margin: 0 auto 14px auto;
      padding: 0 12px;
      box-sizing: border-box;
    }
    .rhgi-voter-impact-divider {
      height: 3px;
      border-radius: 999px;
      background: linear-gradient(90deg, #000080 0%, #00CED1 32%, #5eead4 50%, #00CED1 68%, #000080 100%);
      background-size: 240% 100%;
      animation: rhgiMandateDividerShimmer 18s ease-in-out infinite;
      box-shadow: 0 0 20px rgba(0, 206, 209, 0.42);
    }
    @keyframes rhgiMandateDividerShimmer {
      0%, 100% { background-position: 0% 50%; filter: brightness(1) saturate(1.05); }
      50% { background-position: 100% 50%; filter: brightness(1.12) saturate(1.1); }
    }
    @keyframes rhgiSwingLiquidFlow {
      0% { background-position: 0% 50%; }
      100% { background-position: 220% 50%; }
    }
    @keyframes rhgiSwingWarningFlash {
      0%, 100% { box-shadow: 0 0 10px rgba(212,175,55,0.55), inset 0 0 16px rgba(212,175,55,0.22); }
      50% { box-shadow: 0 0 26px rgba(212,175,55,0.96), inset 0 0 24px rgba(212,175,55,0.36); }
    }
    @keyframes rhgiSwingSilverShimmer {
      0% { background-position: 0% 50%; }
      100% { background-position: 220% 50%; }
    }
    @keyframes rhgiDeciderLiquidGoldFlow {
      0% { background-position: 0% 50%; }
      50% { background-position: 120% 50%; }
      100% { background-position: 240% 50%; }
    }
    @keyframes rhgiDeciderSlowPulse {
      0%, 100% {
        box-shadow:
          0 0 10px rgba(212,175,55,0.38),
          inset 0 0 12px rgba(250,250,210,0.22);
      }
      50% {
        box-shadow:
          0 0 24px rgba(212,175,55,0.78),
          inset 0 0 24px rgba(250,250,210,0.40);
      }
    }
    @keyframes rhgiSwingGoldPulse {
      0%, 100% {
        box-shadow: 0 0 8px rgba(212,175,55,0.45), inset 0 0 12px rgba(212,175,55,0.20);
      }
      50% {
        box-shadow: 0 0 24px rgba(212,175,55,0.90), inset 0 0 22px rgba(212,175,55,0.38);
      }
    }
    @keyframes rhgiSwingPrismSweep {
      0% { background-position: 0% 50%; }
      100% { background-position: 180% 50%; }
    }
    @keyframes rhgiSovereignMarquee {
      0% { transform: translateX(0%); }
      100% { transform: translateX(-50%); }
    }
    .rhgi-swing-shell {
      margin: 8px 0 12px 0;
      padding: 1px;
      border-radius: 14px;
      background: linear-gradient(90deg, #C0C0C0 0%, #D4AF37 30%, #FFFFFF 55%, #D4AF37 78%, #C0C0C0 100%);
      background-size: 240% 100%;
      animation: rhgiSwingLiquidFlow var(--prism-border-rotate) linear infinite;
    }
    .rhgi-swing-inner {
      border-radius: 13px;
      background:
        linear-gradient(110deg, rgba(212,175,55,0.16) 0%, rgba(255,255,255,0.08) 26%, rgba(0,0,128,0.96) 56%, rgba(0,0,128,0.98) 100%),
        #000080;
      padding: 12px 14px;
      color: #ffffff !important;
    }
    .rhgi-swing-shell.warning .rhgi-swing-inner {
      animation: rhgiSwingWarningFlash 1.15s ease-in-out infinite;
    }
    .rhgi-swing-title {
      margin: 0 0 8px 0;
      color: #ffffff;
      font-weight: 900;
      letter-spacing: 0.04em;
      text-align: center;
      font-size: 1.02rem;
    }
    .rhgi-decider-shell {
      margin: 8px 0 14px 0;
      border-radius: 12px;
      border: 1px solid rgba(250,250,210,0.58);
      background: linear-gradient(
        115deg,
        rgba(212,175,55,0.18) 0%,
        rgba(250,250,210,0.36) 18%,
        rgba(212,175,55,0.22) 36%,
        rgba(250,250,210,0.42) 52%,
        rgba(212,175,55,0.24) 72%,
        rgba(250,250,210,0.30) 100%
      );
      background-size: 240% 240%;
      animation:
        rhgiDeciderLiquidGoldFlow 18s linear infinite,
        rhgiDeciderSlowPulse 6.8s ease-in-out infinite;
      padding: 10px 14px;
    }
    .rhgi-decider-label {
      margin: 0 0 4px 0;
      color: transparent;
      font-size: 0.78rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      font-weight: 800;
      text-align: center;
      background: linear-gradient(90deg, #FAFAD2 0%, #D4AF37 34%, #FFF7CC 50%, #D4AF37 66%, #FAFAD2 100%);
      background-size: 220% 100%;
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
      animation: rhgiDeciderLiquidGoldFlow 10s linear infinite;
    }
    .rhgi-decider-target {
      margin: 0;
      text-align: center;
      color: #ffffff;
      font-weight: 900;
      letter-spacing: 0.04em;
      font-size: 1.02rem;
      text-shadow:
        0 0 8px rgba(250,250,210,0.45),
        0 0 16px rgba(212,175,55,0.32);
    }
    .rhgi-decider-sub {
      margin: 6px 0 0 0;
      text-align: center;
      color: #ffffff;
      font-size: 0.84rem;
      font-weight: 700;
      letter-spacing: 0.02em;
    }
    @keyframes rhgiOutreachSilverShimmer {
      0% { background-position: 0% 50%; }
      100% { background-position: 220% 50%; }
    }
    [data-testid="stSidebar"] .rhgi-outreach-bridge {
      margin-top: 14px;
      padding: 12px 14px;
      border-radius: 12px;
      border: 1px solid rgba(192,192,192,0.65);
      background: linear-gradient(
        115deg,
        rgba(192,192,192,0.28) 0%,
        rgba(255,255,255,0.14) 38%,
        rgba(192,192,192,0.22) 100%
      );
      background-size: 240% 100%;
      animation: rhgiOutreachSilverShimmer 12s linear infinite;
      box-shadow: inset 0 0 14px rgba(255,255,255,0.10);
    }
    [data-testid="stSidebar"] .rhgi-outreach-bridge-title {
      color: #00CED1 !important;
      font-weight: 900;
      letter-spacing: 0.06em;
      text-align: center;
      text-shadow: 0 0 12px rgba(0,255,255,0.55);
      margin: 0 0 8px 0;
      font-size: 0.95rem;
      -webkit-text-fill-color: #00CED1 !important;
    }
    [data-testid="stSidebar"] .rhgi-outreach-bridge-line {
      color: #FFFFFF !important;
      font-weight: 700;
      margin: 5px 0;
      font-size: 0.88rem;
      line-height: 1.35;
      -webkit-text-fill-color: #FFFFFF !important;
    }
    [data-testid="stSidebar"] .rhgi-outreach-bridge--executive {
      border: 1px solid rgba(230, 195, 92, 0.85) !important;
      box-shadow: inset 0 0 16px rgba(139, 0, 0, 0.18);
    }
    /* SSMI-NIGHT-DEPLOY-141 — Executive Sync primary: Cyber Cyan glow (tonight session) */
    @keyframes rhgiExecSyncCyanPulse {
      0%, 100% {
        filter: brightness(1);
        box-shadow:
          0 0 18px rgba(0, 255, 255, 0.78),
          0 0 38px rgba(0, 255, 255, 0.42),
          inset 0 0 12px rgba(0, 255, 255, 0.18);
      }
      50% {
        filter: brightness(1.1);
        box-shadow:
          0 0 28px rgba(0, 255, 255, 0.95),
          0 0 56px rgba(0, 230, 255, 0.55),
          inset 0 0 16px rgba(0, 255, 255, 0.28);
      }
    }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"]:has(.rhgi-exec-sync-cyan-trigger) button[kind="primary"] {
      border: 1px solid #00CED1 !important;
      border-radius: 10px !important;
      background: linear-gradient(180deg, rgba(0, 52, 72, 0.98) 0%, rgba(0, 112, 128, 0.98) 100%) !important;
      color: #E0FFFF !important;
      font-weight: 800 !important;
      text-shadow: 0 0 10px rgba(0, 255, 255, 0.9), 0 0 22px rgba(0, 255, 255, 0.45) !important;
      animation: rhgiExecSyncCyanPulse 2s ease-in-out infinite !important;
    }
    /* SSMI-EXECUTIVE-LOAD-142 — Success shimmer after API handoff ack */
    @keyframes rhgiExecSyncSuccessShimmer {
      0% { background-position: 0% 50%; }
      100% { background-position: 100% 50%; }
    }
    [data-testid="stSidebar"] .rhgi-exec-sync-success-panel {
      background: linear-gradient(
        110deg,
        #146c43 0%,
        #20c997 22%,
        #198754 44%,
        #2dd4bf 56%,
        #198754 78%,
        #157347 100%
      ) !important;
      background-size: 240% 100% !important;
      animation: rhgiExecSyncSuccessShimmer 2.8s ease-in-out infinite !important;
      border: 2px solid rgba(255, 255, 255, 0.38) !important;
      box-shadow:
        0 0 26px rgba(32, 201, 151, 0.55),
        inset 0 0 22px rgba(255, 255, 255, 0.14) !important;
    }
    /* SSMI-EXECUTIVE-BYPASS-138 — Outreach Command: executive gold ring + deep red pulse */
    @keyframes rhgiExecDeepRedPulse {
      0%, 100% {
        box-shadow:
          0 0 0 1px rgba(230, 195, 92, 0.95),
          0 0 18px rgba(139, 0, 0, 0.45),
          inset 0 0 14px rgba(212, 175, 55, 0.12);
      }
      50% {
        box-shadow:
          0 0 0 2px rgba(230, 195, 92, 1),
          0 0 28px rgba(139, 0, 0, 0.72),
          inset 0 0 18px rgba(212, 175, 55, 0.22);
      }
    }
    [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"]:has(.rhgi-outreach-bounded--exec) {
      border: 2px solid #E6C35C !important;
      border-radius: 14px !important;
      background: linear-gradient(
        165deg,
        rgba(0, 0, 128, 0.55) 0%,
        rgba(40, 0, 8, 0.35) 100%
      ) !important;
      animation: rhgiExecDeepRedPulse 2.2s ease-in-out infinite;
    }
    .rhgi-sovereign-notepad-host {
      margin-top: 10px;
      padding: 10px 10px 6px 10px;
      border-radius: 10px;
      border: 1px solid rgba(212, 175, 55, 0.35);
      background: rgba(0, 0, 40, 0.5);
    }
    .rhgi-sovereign-feed-wrap {
      border-radius: 12px;
      border: 1px solid rgba(0,255,255,0.28);
      background: linear-gradient(180deg, rgba(0,0,128,0.96) 0%, rgba(0,10,28,0.92) 100%);
      box-shadow: inset 0 0 24px rgba(0,0,0,0.45);
      padding: 10px 10px 8px 10px;
      min-height: 320px;
      max-height: min(72vh, 620px);
      display: flex;
      flex-direction: column;
    }
    .rhgi-sovereign-feed-title {
      color: #00CED1;
      font-weight: 900;
      letter-spacing: 0.08em;
      font-size: 0.78rem;
      text-align: center;
      margin: 0 0 8px 0;
      text-shadow: 0 0 12px rgba(0,255,255,0.35);
    }
    .rhgi-sovereign-feed-window {
      flex: 1;
      overflow-y: auto;
      font-family: 'Goldman', sans-serif;
      font-size: 0.78rem;
      line-height: 1.45;
    }
    .rhgi-sovereign-feed-line {
      color: #00CED1;
      margin-bottom: 6px;
      text-shadow: 0 0 6px rgba(0,255,255,0.22);
      word-break: break-word;
    }
    .rhgi-sovereign-feed-meta {
      margin-top: 8px;
      padding-top: 6px;
      border-top: 1px solid rgba(0,255,255,0.2);
      color: rgba(0,255,255,0.75);
      font-size: 0.68rem;
      text-align: center;
      letter-spacing: 0.04em;
    }
    .rhgi-narrative-label {
      margin: 8px 0 2px 0;
      font-weight: 800;
      font-size: 0.93rem;
      letter-spacing: 0.02em;
      line-height: 1.25;
    }
    .rhgi-narrative-label--cyan {
      color: #00CED1 !important;
      text-shadow: 0 0 10px rgba(0,255,255,0.36);
    }
    .rhgi-narrative-label--amber {
      color: #FFBF00 !important;
      text-shadow: 0 0 10px rgba(255,191,0,0.36);
    }
    .rhgi-swing-grid {
      display: grid;
      grid-template-columns: repeat(6, minmax(0, 1fr));
      gap: 10px;
    }
    .rhgi-swing-item {
      grid-column: span 2;
      border: 1px solid rgba(192,192,192,0.55);
      border-radius: 10px;
      background: rgba(0,0,128,0.76);
      padding: 10px 12px;
      color: #ffffff;
      min-height: 82px;
      position: relative;
      overflow: hidden;
    }
    .rhgi-swing-item::before {
      content: "";
      position: absolute;
      inset: 0;
      border-radius: 10px;
      pointer-events: none;
      z-index: 0;
    }
    .rhgi-swing-item > * {
      position: relative;
      z-index: 1;
    }
    .rhgi-swing-item--silver::before {
      padding: 1px;
      background: linear-gradient(90deg, #A9A9A9 0%, #C0C0C0 24%, #FFFFFF 50%, #C0C0C0 76%, #A9A9A9 100%);
      background-size: 230% 100%;
      animation: rhgiSwingSilverShimmer 8.8s linear infinite;
      -webkit-mask:
        linear-gradient(#fff 0 0) content-box,
        linear-gradient(#fff 0 0);
      -webkit-mask-composite: xor;
      mask-composite: exclude;
    }
    .rhgi-swing-item--gold {
      border-color: rgba(212,175,55,0.95);
      animation: rhgiSwingGoldPulse 5.4s ease-in-out infinite;
    }
    .rhgi-swing-item--prism::before {
      padding: 1px;
      background: linear-gradient(95deg, #000080 0%, #FFFFFF 26%, #001F66 50%, #FFFFFF 74%, #000080 100%);
      background-size: 200% 100%;
      animation: rhgiSwingPrismSweep 26s linear infinite;
      -webkit-mask:
        linear-gradient(#fff 0 0) content-box,
        linear-gradient(#fff 0 0);
      -webkit-mask-composite: xor;
      mask-composite: exclude;
    }
    .rhgi-swing-k {
      color: #ffffff;
      font-weight: 800;
      font-size: 0.83rem;
      letter-spacing: 0.04em;
      margin-bottom: 6px;
    }
    .rhgi-swing-v {
      color: #ffffff;
      font-weight: 700;
      line-height: 1.35;
      font-size: 0.9rem;
    }
    @media (max-width: 1100px) {
      .rhgi-swing-grid {
        grid-template-columns: 1fr;
      }
      .rhgi-swing-item {
        grid-column: 1 / -1;
        min-height: auto;
        overflow: visible;
      }
    }
    .rhgi-sovereign-marquee-wrap {
      width: 100%;
      overflow: hidden;
      white-space: nowrap;
      position: relative;
    }
    .rhgi-sovereign-marquee-track {
      display: inline-flex;
      min-width: max-content;
      animation: rhgiSovereignMarquee 30s linear infinite;
      will-change: transform;
    }
    .rhgi-sovereign-marquee-seg {
      display: inline-block;
      padding-right: 2.8rem;
      color: #ffffff;
      font-weight: 800;
      letter-spacing: 0.01em;
    }
    .rhgi-corridor-foundation-shell {
      margin: 6px 0 10px 0;
      padding: 1px;
      border-radius: 14px;
      background: linear-gradient(90deg, #D4AF37 0%, #FFFFFF 38%, #001F66 62%, #FFFFFF 82%, #D4AF37 100%);
      background-size: 240% 100%;
      animation: rhgiSwingLiquidFlow 30s linear infinite;
    }
    .rhgi-corridor-foundation-inner {
      border-radius: 13px;
      background: rgba(0, 0, 128, 0.95);
      padding: 8px 12px;
      border: 1px solid rgba(212,175,55,0.45);
    }
    .block-container {
      font-size: 1.1rem;
      position: relative;
      z-index: 2 !important;
      font-family: 'Goldman', sans-serif !important;
      color: var(--stark-white) !important;
      background: #000080 !important;
    }
    section.main [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
      background-color: transparent !important;
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
      color: #D4AF37 !important;
      margin: 4px 0 6px 0;
      letter-spacing: 0.12em;
      text-shadow: 0 0 18px rgba(212, 175, 55, 0.55);
    }
    .rhgi-countdown-keys {
      text-align: center;
      font-size: clamp(0.82rem, 2.2vw, 0.92rem);
      font-weight: 600;
      font-family: 'Goldman', sans-serif !important;
      color: #D4AF37 !important;
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
    .rhgi-creed-block {
      font-size: clamp(1.08rem, 2.9vw, 1.22rem);
      line-height: 1.65;
      color: var(--metallic-gold) !important;
      font-family: 'Goldman', sans-serif !important;
      max-width: 1000px;
      margin: 6px auto 16px auto;
      text-align: center;
      font-weight: 600;
      letter-spacing: 0.01em;
      text-shadow: 0 0 18px rgba(212,175,55,0.15);
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
      color: rgba(212, 175, 55, 0.28);
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
      background: radial-gradient(ellipse at 50% 35%, rgba(212,175,55,0.04) 0%, transparent 60%);
      mix-blend-mode: normal;
      opacity: 0.22;
    }
    button, input, textarea, [data-testid="stMarkdownContainer"], .stMarkdown { user-select: text !important; -webkit-user-select: text !important; }
    /* 8R Strategic row (exactly 8 columns): no white card behind buttons */
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) [data-testid="element-container"],
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) [data-testid="column"] {
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
      color: #ffffff !important;
      border: 1px solid transparent !important;
      border-radius: var(--command-box-radius) !important;
      height: var(--command-box-height) !important;
      min-height: var(--command-box-height) !important;
      max-height: var(--command-box-height) !important;
      width: 100% !important;
      max-width: 100% !important;
      box-sizing: border-box !important;
      transform-origin: center center !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      background: #000080 padding-box,
      linear-gradient(
        90deg,
        var(--command-silver) 0%,
        var(--command-white) 18%,
        var(--command-silver) 36%,
        var(--command-white) 54%,
        var(--command-silver) 72%,
        var(--command-white) 90%,
        var(--command-silver) 100%
      ) border-box !important;
      background-size: 240% 100%;
      background-position: 0% 50%;
      animation: rhgiMetalShimmer 1.5s linear infinite, rhgiClockBreathe 3s ease-in-out infinite;
    }
    /* Strategic 8R — Prism Navy + rotating silver/gold ring (slow-motion sweep) + Seconds-sync pulse */
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) button[kind="secondary"],
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) button[kind="primary"] {
      color: #ffffff !important;
      border: none !important;
      border-radius: var(--command-box-radius) !important;
      height: var(--command-box-height) !important;
      min-height: var(--command-box-height) !important;
      max-height: var(--command-box-height) !important;
      width: 100% !important;
      max-width: 100% !important;
      box-sizing: border-box !important;
      transform-origin: center center !important;
      isolation: isolate !important;
      position: relative !important;
      overflow: hidden !important;
      background: transparent !important;
      background-image: none !important;
      animation: rhgiSecSyncPulse 1s ease-in-out infinite !important;
    }
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) button[kind="secondary"]::before,
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) button[kind="primary"]::before {
      content: "" !important;
      position: absolute !important;
      inset: -2px !important;
      border-radius: calc(var(--command-box-radius) + 2px) !important;
      background: conic-gradient(
        from 0deg,
        #C0C0C0 0%,
        #D4AF37 18%,
        #C0C0C0 36%,
        #D4AF37 54%,
        #C0C0C0 72%,
        #D4AF37 90%,
        #C0C0C0 100%
      ) !important;
      animation: rhgiCorridorBorderRotate var(--prism-border-rotate) linear infinite !important;
      transform-origin: center center !important;
      z-index: 0 !important;
      pointer-events: none !important;
    }
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) button[kind="secondary"]::after,
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) button[kind="primary"]::after {
      content: "" !important;
      position: absolute !important;
      inset: 2px !important;
      border-radius: calc(var(--command-box-radius) - 2px) !important;
      background: #000080 !important;
      z-index: 1 !important;
      pointer-events: none !important;
    }
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) button[kind="primary"]::after {
      box-shadow: inset 0 0 0 2px rgba(212, 175, 55, 0.88) !important;
    }
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) button[kind="secondary"] > div,
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) button[kind="primary"] > div {
      position: relative !important;
      z-index: 2 !important;
    }
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) button[kind="secondary"] p,
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) button[kind="secondary"] span,
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) button[kind="primary"] p,
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) button[kind="primary"] span {
      color: #ffffff !important;
      position: relative !important;
      z-index: 2 !important;
    }
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) button[kind="primary"] p,
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) button[kind="primary"] span {
      text-shadow:
        0 0 10px rgba(212, 175, 55, 0.95),
        0 0 22px rgba(212, 175, 55, 0.55) !important;
    }
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) button[kind="secondary"]:hover p,
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) button[kind="secondary"]:hover span,
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) button[kind="primary"]:hover p,
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) button[kind="primary"]:hover span {
      text-shadow:
        0 0 12px rgba(212, 175, 55, 0.98),
        0 0 28px rgba(212, 175, 55, 0.72),
        0 0 42px rgba(212, 175, 55, 0.4) !important;
      color: #ffffff !important;
    }
    @keyframes r8GoldTextShimmer {
      0%, 100% {
        color: #D4AF37 !important;
        text-shadow: 0 0 8px rgba(212,175,55,0.45), 0 0 14px rgba(0,0,128,0.6);
      }
      50% {
        color: #f0e68c !important;
        text-shadow:
          0 0 22px rgba(212, 175, 55, 0.75),
          0 0 36px rgba(212, 175, 55, 0.35),
          0 0 4px rgba(255, 255, 255, 0.25);
      }
    }
    /* DG Corridor Command Hub — Prism Navy + rotating silver/gold ring + Seconds-sync pulse */
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)):not(:has(> div:nth-child(7))) button[kind="secondary"],
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)):not(:has(> div:nth-child(7))) button[kind="primary"] {
      color: #ffffff !important;
      border: none !important;
      border-radius: var(--command-box-radius) !important;
      height: var(--command-box-height) !important;
      min-height: var(--command-box-height) !important;
      max-height: var(--command-box-height) !important;
      width: 100% !important;
      max-width: 100% !important;
      box-sizing: border-box !important;
      transform-origin: center center !important;
      isolation: isolate !important;
      position: relative !important;
      overflow: hidden !important;
      background: transparent !important;
      background-image: none !important;
      animation: rhgiSecSyncPulse 1s ease-in-out infinite !important;
    }
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)):not(:has(> div:nth-child(7))) button[kind="secondary"]::before,
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)):not(:has(> div:nth-child(7))) button[kind="primary"]::before {
      content: "" !important;
      position: absolute !important;
      inset: -2px !important;
      border-radius: calc(var(--command-box-radius) + 2px) !important;
      background: conic-gradient(
        from 0deg,
        #C0C0C0 0%,
        #D4AF37 18%,
        #C0C0C0 36%,
        #D4AF37 54%,
        #C0C0C0 72%,
        #D4AF37 90%,
        #C0C0C0 100%
      ) !important;
      animation: rhgiCorridorBorderRotate var(--prism-border-rotate) linear infinite !important;
      transform-origin: center center !important;
      z-index: 0 !important;
      pointer-events: none !important;
    }
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)):not(:has(> div:nth-child(7))) button[kind="secondary"]::after,
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)):not(:has(> div:nth-child(7))) button[kind="primary"]::after {
      content: "" !important;
      position: absolute !important;
      inset: 2px !important;
      border-radius: calc(var(--command-box-radius) - 2px) !important;
      background: #000080 !important;
      z-index: 1 !important;
      pointer-events: none !important;
    }
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)):not(:has(> div:nth-child(7))) button[kind="primary"]::after {
      box-shadow: inset 0 0 0 2px rgba(212, 175, 55, 0.88) !important;
    }
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)):not(:has(> div:nth-child(7))) button[kind="secondary"] > div,
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)):not(:has(> div:nth-child(7))) button[kind="primary"] > div {
      position: relative !important;
      z-index: 2 !important;
    }
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)):not(:has(> div:nth-child(7))) button[kind="secondary"] p,
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)):not(:has(> div:nth-child(7))) button[kind="secondary"] span,
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)):not(:has(> div:nth-child(7))) button[kind="primary"] p,
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)):not(:has(> div:nth-child(7))) button[kind="primary"] span {
      color: #ffffff !important;
      position: relative !important;
      z-index: 2 !important;
    }
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)):not(:has(> div:nth-child(7))) button[kind="primary"] p,
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)):not(:has(> div:nth-child(7))) button[kind="primary"] span {
      text-shadow:
        0 0 10px rgba(212, 175, 55, 0.95),
        0 0 22px rgba(212, 175, 55, 0.55) !important;
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
    /* NW Villa + national tabs — Goldman, gold/white only (no red accent) */
    [data-testid="stTabs"] {
      font-family: 'Goldman', sans-serif !important;
    }
    [data-testid="stTabs"] [role="tab"] {
      color: #D4AF37 !important;
      font-family: 'Goldman', sans-serif !important;
      background: rgba(0,0,128,0.55) !important;
    }
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
      color: #ffffff !important;
      border-bottom-color: #D4AF37 !important;
    }
    [data-testid="stTabs"] [data-baseweb="tab-highlight"] {
      background: #D4AF37 !important;
    }
    [data-testid="stRadio"] label,
    [data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {
      color: #D4AF37 !important;
      font-family: 'Goldman', sans-serif !important;
    }
    [data-testid="stRadio"],
    [data-testid="stRadio"] [role="radiogroup"],
    [data-testid="stRadio"] label,
    [data-testid="stRadio"] input {
      pointer-events: auto !important;
    }
    [data-testid="stRadio"] { position: relative !important; z-index: 8 !important; }
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)):not(:has(> div:nth-child(7))) button[kind="secondary"],
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(6)):not(:has(> div:nth-child(7))) button[kind="primary"],
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) button[kind="secondary"],
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)):not(:has(> div:nth-child(9))) button[kind="primary"] {
      pointer-events: auto !important;
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
      border: 1px solid rgba(212, 175, 55, 0.35);
      background: rgba(0, 0, 128, 0.45);
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
      text-shadow: 0 0 14px rgba(212,175,55,0.5), 0 0 28px rgba(0,0,128,0.55);
      margin: 8px 0 6px 0;
    }
    .rhgi-mandate-secured {
      text-align: center;
      padding: 14px 18px;
      margin: 12px 0 16px 0;
      border-radius: 12px;
      border: 3px solid var(--metallic-gold);
      background: #000080 !important;
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
      animation: tickerScroll 30s linear infinite;
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
      background: rgba(0, 0, 128, 0.55);
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
    .rhgi-corridor-table tr:nth-child(even) td { background: rgba(0, 0, 128, 0.35); }
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
      background: #000080;
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
    /* Mapbox Visual Tint — Deep Royal Plum */
    .js-plotly-plot .mapboxgl-map,
    .js-plotly-plot .mapboxgl-canvas { background-color: #ffffff !important; }
    /* CIEN verification widgets (image_4 palette) */
    .rhgi-cien-row {
      display: flex; gap: 16px; flex-wrap: wrap; justify-content: center;
      margin: 6px 0 22px 0;
    }
    .rhgi-cien-card {
      flex: 1 1 240px; max-width: 360px;
      border: 2px solid #D4AF37; border-radius: 14px; padding: 20px 18px;
      background: rgba(0,0,128,0.72);
      text-align: center;
      font-family: 'Goldman', sans-serif !important;
      box-shadow: 0 0 26px rgba(212,175,55,0.22);
    }
    .rhgi-cien-card h3 {
      color: #D4AF37 !important; margin: 0 0 10px 0; font-size: 1.4rem;
      letter-spacing: 0.14em; font-weight: 800;
      text-shadow: 0 0 14px rgba(212,175,55,0.45);
    }
    .rhgi-cien-card .cien-sub { color: #ffffff !important; font-size: 0.98rem; font-weight: 600; line-height: 1.45; }
    .rhgi-cien-card .cien-chip {
      margin-top: 12px; color: #D4AF37; font-size: 0.88rem; font-weight: 700; letter-spacing: 0.06em;
    }
    /* CIEN-Verify Swat Widget — gold cylinder, no red */
    @keyframes rhgiSwatBorderPulse {
      0%, 100% { box-shadow: 0 0 16px rgba(212,175,55,0.45), inset 0 0 22px rgba(212,175,55,0.08); }
      50% { box-shadow: 0 0 38px rgba(212,175,55,0.95), inset 0 0 32px rgba(255,248,220,0.12); }
    }
    @keyframes rhgiSwatFillFlow {
      0%, 100% { filter: brightness(1.02); transform: scaleY(1); }
      50% { filter: brightness(1.18); transform: scaleY(1.02); }
    }
    @keyframes rhgiSwatShimmer {
      0% { background-position: 0% 80%; }
      100% { background-position: 0% 20%; }
    }
    .rhgi-swat-shell {
      font-family: 'Goldman', sans-serif !important;
      border: 2px solid #D4AF37;
      border-radius: 22px;
      padding: 22px 20px 26px 20px;
      margin: 6px 0 26px 0;
      background: rgba(0,0,128,0.72);
      animation: rhgiSwatBorderPulse 2.6s ease-in-out infinite;
      position: relative;
      z-index: 2;
      max-width: 520px;
      margin-left: auto;
      margin-right: auto;
    }
    .rhgi-swat-title {
      color: #D4AF37 !important;
      font-weight: 800;
      font-size: clamp(0.95rem, 2.2vw, 1.12rem);
      text-align: center;
      letter-spacing: 0.06em;
      margin: 0 0 6px 0;
      text-shadow: 0 0 14px rgba(212,175,55,0.45);
    }
    .rhgi-swat-sub {
      color: #ffffff !important;
      font-weight: 600;
      font-size: 0.92rem;
      text-align: center;
      margin: 0 0 10px 0;
      opacity: 0.95;
    }
    .rhgi-swat-target {
      color: #D4AF37 !important;
      font-weight: 900;
      font-size: clamp(1.85rem, 5vw, 2.45rem);
      text-align: center;
      letter-spacing: 0.04em;
      text-shadow: 0 0 22px rgba(212,175,55,0.65), 0 0 44px rgba(212,175,55,0.25);
      margin: 0 0 14px 0;
      line-height: 1.1;
    }
    .rhgi-swat-cylinder-wrap {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 10px;
      margin: 8px 0 16px 0;
    }
    .rhgi-swat-cylinder {
      position: relative;
      width: 112px;
      height: 260px;
      border-radius: 56px;
      border: 2px solid rgba(212,175,55,0.75);
      background: linear-gradient(90deg,
        rgba(0,0,128,0.55) 0%,
        rgba(212,175,55,0.12) 45%,
        rgba(255,250,220,0.08) 50%,
        rgba(212,175,55,0.12) 55%,
        rgba(0,0,128,0.55) 100%);
      box-shadow:
        inset 0 0 36px rgba(255,255,255,0.12),
        inset 0 -20px 50px rgba(212,175,55,0.15),
        0 0 28px rgba(212,175,55,0.35);
      overflow: hidden;
    }
    .rhgi-swat-fill {
      position: absolute;
      left: 4px;
      right: 4px;
      bottom: 4px;
      height: 83.7%;
      border-radius: 0 0 48px 48px;
      background: linear-gradient(180deg,
        rgba(255,248,210,0.95) 0%,
        rgba(212,175,55,0.88) 35%,
        rgba(212,175,55,0.75) 70%,
        rgba(180,140,45,0.85) 100%);
      background-size: 100% 200%;
      animation: rhgiSwatFillFlow 2.4s ease-in-out infinite, rhgiSwatShimmer 3.2s linear infinite;
      box-shadow: inset 0 0 24px rgba(255,255,255,0.35), 0 0 22px rgba(212,175,55,0.55);
    }
    .rhgi-swat-current {
      color: #ffffff !important;
      font-weight: 800;
      font-size: 1.05rem;
      letter-spacing: 0.04em;
    }
    .rhgi-swat-status {
      color: #ffffff !important;
      font-size: clamp(0.78rem, 1.8vw, 0.9rem);
      font-weight: 600;
      line-height: 1.55;
      text-align: center;
      margin: 0 0 16px 0;
      padding: 10px 12px;
      border: 1px solid rgba(212,175,55,0.35);
      border-radius: 12px;
      background: rgba(0,0,128,0.5);
    }
    .rhgi-swat-status .rhgi-swat-gold { color: #D4AF37 !important; font-weight: 800; }
    .rhgi-swat-icons {
      display: flex;
      justify-content: center;
      gap: 14px;
      flex-wrap: wrap;
      margin-top: 4px;
    }
    .rhgi-swat-icon {
      flex: 1 1 90px;
      max-width: 140px;
      text-align: center;
      color: #D4AF37 !important;
      font-weight: 800;
      font-size: 0.82rem;
      letter-spacing: 0.04em;
      padding: 10px 8px;
      border: 1px solid rgba(212,175,55,0.45);
      border-radius: 12px;
      background: rgba(0,0,128,0.45);
    }
    .rhgi-swat-icon small {
      display: block;
      color: #ffffff !important;
      font-weight: 600;
      font-size: 0.72rem;
      margin-top: 4px;
      opacity: 0.92;
    }
    .rhgi-forensic-shadow {
      font-family: 'Goldman', sans-serif !important;
      text-align: center;
      color: #D4AF37 !important;
      font-weight: 800;
      letter-spacing: 0.06em;
      padding: 14px 16px;
      margin: 0 0 14px 0;
      border: 1px solid rgba(212,175,55,0.4);
      border-radius: 14px;
      background: rgba(0,0,128,0.55);
      text-shadow: 0 0 14px rgba(212,175,55,0.45);
    }
    .rhgi-swat-grant-alert {
      margin-top: 10px;
      padding: 8px 10px;
      border-radius: 10px;
      border: 1px solid #D4AF37;
      color: #ffffff !important;
      font-size: 0.82rem;
      font-weight: 700;
      letter-spacing: 0.03em;
      box-shadow: 0 0 14px rgba(212,175,55,0.35);
      background: rgba(0,0,128,0.72);
    }
    .rhgi-glossary-shell {
      margin: 22px 0 10px 0;
      padding: 1px;
      border-radius: 14px;
      background: linear-gradient(90deg, #C0C0C0 0%, #FFFFFF 50%, #C0C0C0 100%);
    }
    .rhgi-glossary-inner {
      background: #000080;
      border-radius: 13px;
      padding: 12px 14px;
      color: #ffffff;
    }
    .rhgi-glossary-title {
      margin: 0 0 10px 0;
      color: #ffffff;
      font-weight: 900;
      letter-spacing: 0.05em;
      text-align: center;
    }
    .rhgi-glossary-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }
    .rhgi-glossary-item {
      border: 1px solid rgba(192,192,192,0.55);
      border-radius: 10px;
      padding: 10px 12px;
      background: rgba(0,0,128,0.84);
      color: #ffffff !important;
    }
    .rhgi-glossary-item b {
      color: #ffffff !important;
      letter-spacing: 0.03em;
    }
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
    st.markdown(
        '<p class="rhgi-sidebar-cat rhgi-sidebar-cat--harvest">Category 1: Harvest Metrics</p>',
        unsafe_allow_html=True,
    )
    st.subheader("Sovereign Budget Engine (Tranche 1)")
    st.metric(
        "Global Logistics Fuel:",
        "₦108.96B",
        help="Tranche 1 anchor: ₦108,961,000,000",
    )
    st.metric("Efficiency Gauge", "1:15 Canvasser Ratio")
    st.markdown(
        "₦8.64B (Canvassers) + ₦86.32B (Logistics) + ₦14B (Contingency)"
    )
    turnout_lift = st.slider(
        "Scientific turnout lift (%)",
        min_value=1,
        max_value=15,
        value=15,
        key="scientific_turnout_lift_pct",
        help="Increases projected 2027 vote totals across all parties proportionally. Uses its own session key so it does not collide with the Sovereign Notepad form.",
    )
    _dff_yield_sidebar = apply_turnout_lift(df, turnout_lift)
    _projected_lifted_nat = int(_dff_yield_sidebar["projected_total"].sum())
    _anchor_m = NATIONAL_VOTE_TARGET / 1_000_000.0
    _projected_m = _projected_lifted_nat / 1_000_000.0
    _delta_vs_anchor = _projected_lifted_nat - NATIONAL_VOTE_TARGET
    st.metric(
        "Sovereign Voter Yield",
        f"{_anchor_m:.1f}M Anchor vs {_projected_m:.1f}M Projected Yield",
        delta=f"{_delta_vs_anchor / 1_000_000.0:+.1f}M projected delta",
        help=(
            f"Anchor: {NATIONAL_VOTE_TARGET:,} sovereign mandate baseline. "
            f"Projected yield at +{turnout_lift}% scientific turnout lift: {_projected_lifted_nat:,}."
        ),
    )
    st.caption("PVC & turnout rates are forensic anchors per LGA in data_engine.")
    st.markdown(
        f'<p class="rhgi-forensic-baseline-line">Baseline structure: {POLLING_UNITS_BASELINE:,} PUs · '
        f"{FORENSIC_2027_BALLOT_BASELINE_CAPTION}</p>",
        unsafe_allow_html=True,
    )
    st.metric(
        "Forensic Vault",
        f"Projected {BALLOT_BOXES_FEDERATION_2027:,} EC8A Digital Twins",
        delta="Sovereign Proof-Load",
        help="Forensic Vault sync status for projected EC8A digital twins.",
    )
    projected_national = int(df[["apc_2027", "pdp_2027", "lp_2027", "adc_2027"]].sum().sum())
    st.metric(
        "National anchor (2027 base)",
        f"{NATIONAL_VOTE_TARGET:,}",
        delta=f"Base projection {projected_national:,}",
        help="Mandate reference total; live yield updates with turnout lift.",
    )
    st.markdown(
        '<p class="rhgi-sidebar-cat rhgi-sidebar-cat--infra">Category 2: Infrastructure Layer</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "- **Heritage Spine**: AKK Section 1 at **80% completion**\n"
        "- **Non-Oil Sector Opportunities**: Innovation Heritage sub-layer targeting **100k+ high-tech roles** "
        "for the **60% youth demographic**."
    )
    st.subheader("Cyber-Sovereignty Node")
    st.metric("AI Deepfake Detection", "ACTIVE", delta="Rapid-Response Verification ARMED")
    st.markdown(
        "<span style='color:#ffffff;font-weight:800;'>Rapid-Response Verification protocol is active for sovereign validation.</span>",
        unsafe_allow_html=True,
    )
    with st.container(border=True):
        _exec = st.checkbox(
            "Leadership Only",
            key="leadership_only",
            help="Executive mode: polished gold frame with deep-red pulse. Sovereign Notepad POSTs only to S24 + Convener webhooks from leadership.json (or env overrides).",
        )
        st.markdown(
            f'<div class="rhgi-outreach-bounded{" rhgi-outreach-bounded--exec" if _exec else ""}" aria-hidden="true"></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p class="rhgi-sidebar-cat rhgi-sidebar-cat--outreach">Category 3: Outreach Command</p>',
            unsafe_allow_html=True,
        )
        default_outreach_velocity_pct = 46.63
        pu_messages_sent = int(
            st.session_state.get(
                "pu_messages_sent",
                int(round((default_outreach_velocity_pct / 100.0) * PU_TOTAL)),
            )
        )
        st.session_state["pu_messages_sent"] = pu_messages_sent
        velocity_pct = 100.0 * float(pu_messages_sent) / float(PU_TOTAL)

        uploaded_img11 = st.file_uploader(
            "Load PU Reminder CSV payload (Image 11)",
            type=["csv"],
            key="img11_pu_csv_uploader",
            help="CSV should include PU coordinates (e.g. `pu_lat` + `pu_lon`) or `lat` + `lon`.",
        )
        if uploaded_img11 is not None:
            try:
                df_img11 = pd.read_csv(uploaded_img11)
                st.session_state["pu_payload_image11"] = df_img11
                st.session_state["pu_sync_payload"] = df_img11
                reached_pus = _compute_pu_messages_sent_from_payload(df_img11)
                st.session_state["pu_messages_sent"] = reached_pus
                pu_messages_sent = reached_pus
                velocity_pct = 100.0 * float(reached_pus) / float(PU_TOTAL)
                st.success(
                    f"Image 11 payload loaded. Reached PUs: {reached_pus:,} / {PU_TOTAL:,}"
                )
            except Exception as e:
                st.error(f"Failed to load Image 11 CSV: {e}")

        st.metric("Outreach Velocity", f"{velocity_pct:.2f}% coverage")
        st.metric(
            "SMS/WhatsApp Tracker",
            f"{pu_messages_sent:,} / {PU_TOTAL:,}",
            delta="Direct PU messages sent",
        )
        if st.button("PUSH PU REMINDERS", use_container_width=True, key="push_pu_reminders_btn"):
            if isinstance(st.session_state.get("pu_payload_image11"), pd.DataFrame):
                pu_payload = st.session_state["pu_payload_image11"]
                st.session_state["pu_messages_sent"] = _compute_pu_messages_sent_from_payload(pu_payload)
            else:
                pu_payload = build_pu_sync_payload(df)
            st.session_state["pu_sync_payload"] = pu_payload
            _append_sovereign_feed(
                "SMS",
                _append_outreach_signature(
                    f"PU reminder batch · {len(pu_payload):,} rows · 20.7M buffer · 15/15 cell bridge "
                    f"(2023 turnout floor {NATIONAL_TURNOUT_2023_PCT:.2f}%)."
                ),
            )
            st.success(
                f"PU Reminder Engine synced {len(pu_payload):,} voter records with PU coordinates. "
                f"Gap analysis for apathy reminders uses the 2023 turnout benchmark ({NATIONAL_TURNOUT_2023_PCT:.2f}% national) as the conversion floor."
            )
        pu_payload = st.session_state.get("pu_sync_payload")
        if isinstance(pu_payload, pd.DataFrame) and not pu_payload.empty:
            st.caption("PU Reminder Engine payload preview (first 10 rows).")
            st.dataframe(pu_payload.head(10), use_container_width=True, hide_index=True)
            st.download_button(
                "Download PU sync payload (CSV)",
                data=pu_payload.to_csv(index=False).encode("utf-8"),
                file_name="pu_reminder_sync_payload.csv",
                mime="text/csv",
                use_container_width=True,
            )
        st.caption("Outreach hub tracks direct SMS/WhatsApp pushes to all 176,846 PUs.")
        _bridge_cls = "rhgi-outreach-bridge" + (" rhgi-outreach-bridge--executive" if _exec else "")
        st.markdown(
            f'<div class="{_bridge_cls}">'
            '<p class="rhgi-outreach-bridge-title">ACTIVE OUTREACH</p>'
            "<p class='rhgi-outreach-bridge-line'>WhatsApp Status: <b>ACTIVE</b></p>"
            "<p class='rhgi-outreach-bridge-line'>SMS Credits: <b>20.7M Buffer</b></p>"
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            '<p class="rhgi-sidebar-cat rhgi-sidebar-cat--outreach" style="margin-top:14px;">'
            "Executive Sync</p>",
            unsafe_allow_html=True,
        )
        _mgmt_roster = _strike_command_phones()
        _mgmt_total = len(_mgmt_roster)
        st.caption(
            f"**{OFFICE_IDENTITY}** · **Automated Executive Loop** ({STRIKE_LOAD_ID}). "
            f"Sender text: **DG/RHGI** directive (master **{DG_VERIFIED_E164}** on roster). "
            f"One **https://wa.me/** handshake every **{_STRIKE_EXEC_LOOP_INTERVAL_SEC} seconds**; "
            "**Delivered** updates after each node. Engine port **8505** (see `.streamlit/config.toml`). "
            f"**Open WhatsApp** (below): Precision Strike → Dr. Ikechukwu **{PRECISION_STRIKE_IKECHUKWU_E164}** · `{STRIKE_LOAD_ID}`. "
            "Expanders for Management 8. Allow pop-ups."
        )
        _strike_wa_urls_all = "\n".join(_wa_me_url(p, EXEC_SYNC_MESSAGE) for p in _mgmt_roster)
        _precision_strike_wa_url = _wa_me_url(PRECISION_STRIKE_IKECHUKWU_E164, PRECISION_STRIKE_MESSAGE)
        st.checkbox(
            "Debug Mode (show exact wa.me URLs)",
            key="wa_debug_mode",
            help="Shows full https://wa.me/…?text=… lines for all Management 8 targets and last fired URLs.",
        )
        if st.session_state.get("wa_debug_mode"):
            st.caption("DEBUG — Precision Strike (Dr. Ikechukwu, quote-encoded ?text=)")
            st.code(_precision_strike_wa_url, language="text")
            st.caption("DEBUG — STRIKE URLs (Management 8, exact, copy if needed)")
            st.code(_strike_wa_urls_all, language="text")
            if st.session_state.get("last_wa_urls"):
                st.caption("Last fired wa.me URLs")
                st.code("\n".join(st.session_state.last_wa_urls), language="text")
        st.link_button(
            f"Open WhatsApp — Precision Strike (Dr. Ikechukwu · {STRIKE_LOAD_ID})",
            _precision_strike_wa_url,
            use_container_width=True,
            help=(
                f"{OFFICE_IDENTITY} · Full https://wa.me/?text=… with urllib.parse.quote-encoded payload "
                f"(Dr. Sa\u2019ad line)."
            ),
        )
        with st.expander("Management 8 — direct https://wa.me/ handshake (one link per number)", expanded=False):
            st.caption(
                f"Each button opens **https://wa.me/** with E.164 digits and the STRIKE text "
                f"({OFFICE_IDENTITY} payload)."
            )
            _wm_cols = st.columns(2)
            for _wi, _wp in enumerate(_mgmt_roster):
                with _wm_cols[_wi % 2]:
                    st.link_button(
                        f"wa.me/{_wp}",
                        _wa_me_url(_wp, EXEC_SYNC_MESSAGE),
                        use_container_width=True,
                        help=f"https://wa.me/…?text=… — STRIKE {STRIKE_LOAD_ID} directive.",
                    )
        _strike_idle = not st.session_state.get("strike_sequential_active") and not st.session_state.get(
            "executive_sync_delivered"
        )
        if _strike_idle:
            with st.container():
                st.markdown(
                    '<div class="rhgi-exec-sync-cyan-trigger" style="display:none" aria-hidden="true"></div>',
                    unsafe_allow_html=True,
                )
                if st.button(
                    f"STRIKE {STRIKE_LOAD_ID}",
                    use_container_width=True,
                    key="executive_sync_activate_btn",
                    type="primary",
                    help=(
                        f"Automated Executive Loop: Node 1→8 via Python-built https://wa.me/ URLs, "
                        f"{_STRIKE_EXEC_LOOP_INTERVAL_SEC}s apart (st.fragment); Delivered counter steps each open."
                    ),
                ):
                    _urls, _url_err = _build_executive_strike_wa_urls()
                    if _url_err:
                        st.error(_url_err)
                    else:
                        st.session_state.executive_sync_handoff_ack = False
                        st.session_state.last_wa_urls = []
                        if hasattr(st, "fragment"):
                            st.session_state.strike_urls_pending = _urls
                            st.session_state.strike_open_index = 0
                            st.session_state.strike_sequential_active = True
                            st.session_state.executive_sync_delivered = False
                            st.session_state.executive_sync_recipient_count = 0
                        else:
                            components.html(
                                _wa_me_popup_html(_urls, stagger_ms=_STRIKE_EXEC_LOOP_INTERVAL_SEC * 1000),
                                height=0,
                            )
                            st.session_state.executive_sync_delivered = True
                            st.session_state.executive_sync_recipient_count = len(_urls)
                            st.session_state.last_wa_urls = list(_urls)
                            _append_sovereign_feed(
                                "Executive Sync",
                                f"STRIKE {STRIKE_LOAD_ID} · {len(_urls)} https://wa.me/ link(s) · RHGI-SSMI sync.",
                            )
                        st.rerun()
        if hasattr(st, "fragment"):
            _strike_seq_runner = st.fragment(run_every=_STRIKE_SEQUENTIAL_INTERVAL)(
                _strike_exec_sidebar_fragment_inner
            )
            _strike_seq_runner()
        elif not _strike_idle:
            st.warning("Upgrade Streamlit for automated STRIKE sequencing (st.fragment).")

        st.markdown(
            '<p class="rhgi-sidebar-cat rhgi-sidebar-cat--outreach" style="margin-top:14px;">'
            "Management/Demonstration</p>",
            unsafe_allow_html=True,
        )
        st.caption(
            "Optional broadcast: up to 10 lines — only **Management 8** roster numbers are accepted; other lines are ignored. "
            "Opens **https://wa.me/** with signature appended."
        )
        st.text_area(
            "Colleague phone numbers",
            key="mgmt_demo_phones_text",
            height=132,
            help="One mobile number per line. Outbound WhatsApp text uses real line breaks in the signature block.",
        )
        st.text_input(
            "Broadcast message (RHGI signature appended automatically)",
            key="mgmt_demo_msg",
        )
        if st.button(
            "Open WhatsApp — Management 8 (https://wa.me/ sequence)",
            use_container_width=True,
            key="mgmt_demo_wa_all_btn",
            help="Opens https://wa.me/…?text=… for each accepted Management 8 line (prefilled message).",
        ):
            _allowed = frozenset(_load_management_8_phones())
            _lines = [
                ln.strip()
                for ln in str(st.session_state.get("mgmt_demo_phones_text", "")).splitlines()
                if ln.strip()
            ][:10]
            _base = str(st.session_state.get("mgmt_demo_msg", "")).strip() or (
                "RHGI Management/Demonstration — please acknowledge this outreach sync."
            )
            _full = _append_outreach_signature(_base)
            _urls: list[str] = []
            _skipped: list[str] = []
            for _ln in _lines:
                _d = _normalize_ng_e164_digits(_ln)
                if len(_d) >= 12 and _d in _allowed:
                    _urls.append(f"https://wa.me/{_d}?text={_quote_wa_message(_full)}")
                else:
                    _skipped.append(_ln)
            if _skipped:
                st.warning(
                    "Ignored lines (not on Management 8 roster / invalid format): "
                    + ", ".join(_skipped[:5])
                    + ("…" if len(_skipped) > 5 else "")
                )
            if _urls:
                st.session_state.last_wa_urls = list(_urls)
                components.html(_wa_me_popup_html(_urls), height=0)
                _append_sovereign_feed(
                    "WhatsApp",
                    f"Management 8 · https://wa.me/ sequence · {len(_urls)} tab(s) · signature lines embedded.",
                )
                st.info("Opening WhatsApp — if blocked, enable Debug Mode and copy the wa.me URL.")
            elif not _skipped:
                if not _lines:
                    st.warning("Add at least one Management 8 roster line (E.164 / local NG format) to send.")
                else:
                    st.warning("No accepted numbers — use roster digits only (e.g. 2348036948675 or local 080…).")

    st.markdown(
        '<p class="rhgi-sovereign-notepad-host" style="margin:12px 0 4px 0;color:#E6C35C;font-weight:800;font-size:0.82rem;letter-spacing:0.06em;">'
        "Sovereign Notepad · internal dashboard</p>",
        unsafe_allow_html=True,
    )
    components.html(
        """
        <div style="font-family:Goldman,Georgia,serif;color:#C9A227;font-size:0.7rem;letter-spacing:0.12em;
        margin:0 0 6px 0;font-weight:800;padding:2px 0;">
          PRIVATE COMPONENT · LIVE
          <span style="color:#8B0000;margin-left:6px;animation:rhgiSnLive 1.15s ease-in-out infinite;">●</span>
        </div>
        <style>
          @keyframes rhgiSnLive { 0%,100% { opacity:1; } 50% { opacity:0.32; } }
        </style>
        """,
        height=44,
    )
    with st.form("sovereign_notepad_form", clear_on_submit=True):
        _sn_text = st.text_area(
            "Sovereign Notepad",
            height=120,
            placeholder="Type here — Send dispatches JSON POSTs only to S24 + Convener endpoints (leadership.json / env).",
            label_visibility="collapsed",
            key="sovereign_notepad_text",
        )
        _sn_send = st.form_submit_button("Send", use_container_width=True, type="primary")
    if _sn_send:
        _ok, _bad = _dispatch_sovereign_notepad(_sn_text)
        if _ok:
            st.success("Sovereign Notepad dispatched to: " + " · ".join(_ok))
            _append_sovereign_feed(
                "NOTEPAD",
                "Executive notepad · " + " · ".join(_ok),
            )
        if _bad:
            st.warning("\n".join(_bad))

dff = apply_turnout_lift(df, turnout_lift)
dff_hub = filter_by_corridor(dff, st.session_state.get("dg_corridor"))
states_25, fct_validated, constitutional_ok = constitutional_sentinel(dff)
fct_pct = fct_apc_percent(dff)
projected_yield_nat = int(dff["projected_total"].sum())
PROJECTED_TOTAL = projected_yield_nat
projected_yield_hub = int(dff_hub["projected_total"].sum())
projected_yield = projected_yield_nat
apc_national = int(dff["apc_2027"].sum())
national_apc_share = 100.0 * apc_national / max(PROJECTED_TOTAL, 1)
remittance_gap = NATIONAL_VOTE_TARGET - PROJECTED_TOTAL
abuja_strobe = fct_pct < 25.0
total_winning_margin = float(dff_hub["winning_margin"].sum())

_cien_audit_rows = build_cien_audit_rows(dff_hub)
st.session_state._cien_rows_full = _cien_audit_rows
_heritage_layer_df, _stability_heat_df, _infra_active_states = build_heritage_spine_layers()

with st.sidebar:
    _cien_sidebar_box = st.container()
    with _cien_sidebar_box:
        st.markdown(
            '<p style="font-family:Goldman,sans-serif;color:#FFFFFF;font-weight:800;font-size:1.02rem;'
            'margin:18px 0 8px 0;letter-spacing:0.04em;">LGA-CIEN REAL-TIME AUDIT & LOGISTICS FEED</p>',
            unsafe_allow_html=True,
        )
        st.caption(
            "Swat-to-Grant ticker: 1 LGA / 3.0s · K3 Triangle priority · Swat = 15/15 activation threshold."
        )

        def _cien_sidebar_pulse_inner() -> None:
            rows = st.session_state.get("_cien_rows_full") or []
            if not rows:
                st.caption("No LGA rows.")
                return
            n = len(rows)
            i = st.session_state.cien_tick_idx % n
            st.session_state.cien_tick_idx = (st.session_state.cien_tick_idx + 1) % n
            r = rows[i]
            st.session_state.cien_map_candidate = {
                "lat": r["lat"],
                "lon": r["lon"],
                "zoom": 10.2,
            }
            _n = "N"
            _n_style = (
                "display:inline-block;width:22px;height:22px;line-height:22px;text-align:center;"
                "border-radius:4px;margin-right:8px;font-weight:800;font-size:0.75rem;"
            )
            if r["verified"]:
                _n_html = (
                    f'<span style="{_n_style}background:rgba(212,175,55,0.35);color:#D4AF37;'
                    'border:1px solid #D4AF37;box-shadow:0 0 12px rgba(212,175,55,0.85);">{_n}</span>'
                )
            else:
                _n_html = (
                    f'<span style="{_n_style}background:transparent;color:#ffffff;'
                    'border:1px solid rgba(255,255,255,0.75);">{_n}</span>'
                )
            st.markdown(
                f'<div style="font-family:Goldman,sans-serif;font-size:0.88rem;line-height:1.5;color:#ffffff;">'
                f"{_n_html}"
                f'<span style="color:#ffffff;">{html.escape(r["lga"])} : {html.escape(r["state"])} : '
                f'<span style="color:#FFFFFF;font-weight:700;">{html.escape(r["status"])}</span></span></div>',
                unsafe_allow_html=True,
            )
            if r.get("swat_15_15"):
                st.markdown(
                    "<div class='rhgi-swat-grant-alert'>"
                    f"LGA: {html.escape(r['lga'])} SWAT COMPLETE &gt; COMMUNITY GRANT ACTIVATED"
                    "</div>",
                    unsafe_allow_html=True,
                )
            _infra_active = str(r["state"]) in _infra_active_states
            _swat_gate = bool(r.get("swat_15_15") and _infra_active)
            _prev_gate = bool(st.session_state.get("swat_audio_gate_prev", False))
            if _swat_gate and not _prev_gate:
                components.html(
                    """
                    <script>
                      const Ctx = window.AudioContext || window.webkitAudioContext;
                      const ctx = new Ctx();
                      function hit(freq, t0, t1, gainVal){
                        const o = ctx.createOscillator();
                        const g = ctx.createGain();
                        o.type = "triangle";
                        o.frequency.setValueAtTime(freq, t0);
                        g.gain.setValueAtTime(0.0001, t0);
                        g.gain.exponentialRampToValueAtTime(gainVal, t0 + 0.01);
                        g.gain.exponentialRampToValueAtTime(0.0001, t1);
                        o.connect(g); g.connect(ctx.destination);
                        o.start(t0); o.stop(t1);
                      }
                      const now = ctx.currentTime;
                      hit(1046, now, now + 0.12, 0.2);
                      hit(1318, now + 0.14, now + 0.28, 0.18);
                    </script>
                    """,
                    height=0,
                )
            st.session_state.swat_audio_gate_prev = _swat_gate
            if st.button(
                f"Focus Map 2: {r['lga']}, {r['state']}",
                key="cien_zoom_map_btn",
                use_container_width=True,
            ):
                mc = st.session_state.get("cien_map_candidate")
                if mc:
                    st.session_state.map_view = dict(mc)

        if hasattr(st, "fragment"):
            _cien_pulse = st.fragment(run_every=timedelta(seconds=3.0))(_cien_sidebar_pulse_inner)
            _cien_pulse()
        else:
            _cien_sidebar_pulse_inner()

abuja_now = datetime.now(lagos_tz)
st.markdown(
    """
    <style>
      @keyframes rhgiPrismZoom {
        0%, 100% { transform: scale(1.0); }
        50% { transform: scale(1.05); }
      }
      :root {
        --command-box-height: 62px;
        --command-box-radius: 14px;
        --command-gold: #D4AF37;
        --command-silver: #C0C0C0;
        --command-white: #FFFFFF;
        --command-navy: #000080;
        --sec-glow-px: 12px;
        --sec-glow-alpha: 0.26;
        --prism-border-rotate: 32s;
      }
      .rhgi-prism-frames-row {
        display: flex;
        gap: 14px;
        justify-content: center;
        align-content: center;
        flex-wrap: wrap;
        margin: 6px auto 10px auto;
        padding: 0 8px;
        width: 100%;
        max-width: 1200px;
        align-items: center;
      }
      .rhgi-prism-frame {
        padding: 1px;
        border-radius: 16px;
        background: linear-gradient(
          90deg,
          #C0C0C0 0%,
          #FFFFFF 20%,
          #C0C0C0 40%,
          #FFFFFF 60%,
          #C0C0C0 80%,
          #FFFFFF 100%
        );
        background-size: 220% 100%;
        background-position: 0% 50%;
        animation: rhgiMetalShimmer 1.5s linear infinite;
      }
      .rhgi-prism-frame-inner {
        background: #000080;
        border-radius: 15px;
        padding: 10px 16px;
        min-width: 360px;
        text-align: center;
        animation: rhgiPrismZoom 5s ease-in-out infinite;
      }
      .rhgi-prism-frame-title {
        color: #ffffff;
        font-weight: 900;
        letter-spacing: 0.03em;
      }

      .rhgi-metal-grid {
        width: 100%;
        display: grid;
        grid-template-columns: repeat(6, minmax(0, 1fr));
        gap: 10px;
        margin: 8px 0 14px 0;
        box-sizing: border-box;
      }
      .rhgi-metal-box {
        height: var(--command-box-height);
        min-height: var(--command-box-height);
        max-height: var(--command-box-height);
        width: 100%;
        max-width: 100%;
        box-sizing: border-box;
        padding: 1px;
        border-radius: var(--command-box-radius);
        border: 0;
        background: transparent;
        text-align: center;
        display: flex;
        justify-content: center;
        align-items: stretch;
        transform-origin: center center;
        position: relative;
        overflow: hidden;
      }
      .rhgi-metal-box:not(.rhgi-seconds-box) {
        animation: rhgiClockBreathe 3s ease-in-out infinite;
      }
      .rhgi-metal-box.rhgi-seconds-box {
        animation: rhgiSecSyncPulse 1s ease-in-out infinite;
      }
      .rhgi-metal-box::before {
        content: "";
        position: absolute;
        inset: -2px;
        border-radius: calc(var(--command-box-radius) + 2px);
        background: linear-gradient(
          90deg,
          #C0C0C0 0%,
          #FFFFFF 18%,
          #C0C0C0 36%,
          #FFFFFF 54%,
          #C0C0C0 72%,
          #FFFFFF 90%,
          #C0C0C0 100%
        );
        background-size: 240% 100%;
        background-position: 0% 50%;
        animation: rhgiMetalShimmer 1.5s linear infinite;
        z-index: 0;
        opacity: 1;
      }
      .rhgi-metal-box-inner {
        width: 100%;
        height: 100%;
        min-height: 0;
        border-radius: calc(var(--command-box-radius) - 1px);
        background: #000080;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 2px;
        position: relative;
        z-index: 1;
      }
      .rhgi-metal-label {
        color: #ffffff;
        font-weight: 900;
        letter-spacing: 0.06em;
        font-size: 0.88rem;
      }
      .rhgi-metal-number {
        color: var(--command-gold);
        font-weight: 950;
        font-size: 1.45rem;
        margin-top: 2px;
      }
      .rhgi-prism-narrative-frame {
        background: #000080;
        border: 1px solid rgba(212,175,55,0.45);
        border-radius: 14px;
        padding: 10px 14px;
        color: #ffffff;
        font-weight: 900;
        letter-spacing: 0.02em;
        box-shadow: none;
        text-align: center;
        text-shadow: 0 1px 2px rgba(0,0,0,0.85);
      }
      .rhgi-prism-narrative-frame * { color: #ffffff !important; text-shadow: 0 1px 2px rgba(0,0,0,0.85) !important; }
      .rhgi-prism-narrative-frame, .rhgi-prism-narrative-frame * {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
      }
      /* Sovereign Seal — DG office digital validation (turquoise prism + slow breath) */
      .rhgi-sovereign-seal-breathe {
        display: flex;
        justify-content: center;
        margin: 0 auto 14px auto;
        max-width: min(960px, 100%);
        animation: rhgiSovereignSealBreath 7.5s cubic-bezier(0.42, 0, 0.45, 1) infinite;
        transform-origin: center center;
      }
      @keyframes rhgiSovereignSealBreath {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
      }
      .rhgi-sovereign-seal-prism {
        width: 100%;
        box-sizing: border-box;
        padding: 3px;
        border-radius: 16px;
        background: linear-gradient(
          118deg,
          #0f766e 0%,
          #99f6e4 12%,
          #134e4a 26%,
          #ccfbf1 38%,
          #2dd4bf 50%,
          #e0f2f1 62%,
          #0d9488 74%,
          #5eead4 86%,
          #115e59 100%
        );
        background-size: 320% 320%;
        animation: rhgiSovereignSealPrismShimmer 5.5s ease-in-out infinite;
        box-shadow:
          0 0 22px rgba(45, 212, 191, 0.55),
          0 0 46px rgba(13, 148, 136, 0.32),
          inset 0 0 14px rgba(240, 253, 250, 0.12);
      }
      @keyframes rhgiSovereignSealPrismShimmer {
        0%, 100% { background-position: 0% 50%; filter: saturate(1.06) brightness(1); }
        50% { background-position: 100% 50%; filter: saturate(1.18) brightness(1.1); }
      }
      .rhgi-sovereign-seal-inner {
        border-radius: 13px;
        background: linear-gradient(185deg, #042f2e 0%, #022c2c 42%, #134e4a 100%);
        padding: 11px 18px;
        text-align: center;
        border: 1px solid rgba(94, 234, 212, 0.4);
        box-shadow: inset 0 0 26px rgba(13, 148, 136, 0.28);
      }
      .rhgi-sovereign-seal-label {
        font-family: 'Goldman', system-ui, sans-serif !important;
        font-weight: 800;
        font-size: clamp(0.8rem, 1.6vw, 1.06rem);
        letter-spacing: 0.07em;
        color: #5eead4 !important;
        text-shadow:
          0 0 16px rgba(94, 234, 212, 0.95),
          0 0 32px rgba(45, 212, 191, 0.55),
          0 1px 0 rgba(0, 0, 0, 0.9);
        line-height: 1.38;
        display: inline-block;
      }
      /* RHGI Sovereign Test — Election Day simulation notice */
      .rhgi-sovereign-test-shell {
        font-family: 'Goldman', system-ui, sans-serif !important;
        max-width: min(920px, 100%);
        margin: 18px auto 8px auto;
        padding: 16px 20px 18px 20px;
        border-radius: 14px;
        border: 2px solid rgba(212, 175, 55, 0.85);
        background: linear-gradient(180deg, rgba(0, 0, 128, 0.97) 0%, rgba(10, 30, 45, 0.98) 100%);
        box-shadow: 0 0 24px rgba(212, 175, 55, 0.25), inset 0 0 20px rgba(251, 191, 36, 0.06);
        text-align: left;
      }
      .rhgi-sovereign-test-title {
        margin: 0 0 10px 0;
        font-size: clamp(0.95rem, 2vw, 1.15rem);
        font-weight: 900;
        letter-spacing: 0.14em;
        color: #D4AF37 !important;
        text-shadow: 0 0 14px rgba(212, 175, 55, 0.5);
        text-align: center;
      }
      .rhgi-sovereign-test-notice {
        margin: 0 0 14px 0;
        padding: 8px 12px;
        border-radius: 8px;
        background: rgba(251, 191, 36, 0.12);
        border: 1px solid rgba(251, 191, 36, 0.45);
        color: #fde68a !important;
        font-weight: 800;
        font-size: clamp(0.82rem, 1.5vw, 0.95rem);
        letter-spacing: 0.04em;
        text-align: center;
      }
      .rhgi-sovereign-test-line {
        margin: 0 0 8px 0;
        color: #ffffff !important;
        font-size: clamp(0.8rem, 1.45vw, 0.94rem);
        font-weight: 600;
        line-height: 1.5;
      }
      .rhgi-sovereign-test-line:last-child { margin-bottom: 0; }
      .rhgi-sovereign-test-line b {
        color: #5eead4 !important;
        font-weight: 800;
        letter-spacing: 0.03em;
      }
    </style>
    <div class="rhgi-prism-frames-row">
      <div class="rhgi-prism-frame">
        <div class="rhgi-prism-frame-inner">
          <div class="rhgi-prism-frame-title">PRESIDENTIAL PRIMARIES: APRIL 23, 2026</div>
        </div>
      </div>
      <div class="rhgi-prism-frame">
        <div class="rhgi-prism-frame-inner">
          <div class="rhgi-prism-frame-title">PRESIDENTIAL ELECTION: SATURDAY, JANUARY 16, 2027</div>
        </div>
      </div>
    </div>
    <div class="rhgi-brand-block">
      <div class="rhgi-sovereign-seal-breathe" role="img" aria-label="Sovereign Seal — Digital Validation of RHGI Policy Document.">
        <div class="rhgi-sovereign-seal-prism">
          <div class="rhgi-sovereign-seal-inner">
            <span class="rhgi-sovereign-seal-label">Digital Validation of RHGI Policy Document.</span>
          </div>
        </div>
      </div>
      <h1 class="rhgi-brand-title">OFFICE OF THE DG/RHGI</h1>
      <p class="rhgi-creed-block">Securing the 20.7M Mandate through Scientific Precision.</p>
      <p class="rhgi-creed-block" style="font-size:0.88rem;color:#00CED1;margin-top:6px;font-weight:700;">Zero-Hour · 16 January 2027 (WAT) — 20.7M mandate execution anchor</p>
      <div class="rhgi-emblem-wrap"><div class="rhgi-emblem">RHGI</div></div>
    </div>
    <div class="rhgi-sovereign-test-shell" role="region" aria-label="RHGI Sovereign Test Election Day simulation">
      <p class="rhgi-sovereign-test-title">RHGI SOVEREIGN TEST | 15/15 SYNC</p>
      <p class="rhgi-sovereign-test-notice">NOTICE: This is an Election Day Simulation.</p>
      <p class="rhgi-sovereign-test-line"><b>Voter Node:</b> [Simulated Name]</p>
      <p class="rhgi-sovereign-test-line"><b>Primary Location:</b> Aba South / Adamawa Corridor</p>
      <p class="rhgi-sovereign-test-line"><b>Polling Unit:</b> [Simulated PU Name]</p>
      <p class="rhgi-sovereign-test-line"><b>Directive:</b> Proceed to your PU for 15/15 Validation. Your Facilitator is synced.</p>
      <p class="rhgi-sovereign-test-line"><b>ID:</b> 14314-TEST-STRIKE</p>
      <p class="rhgi-sovereign-test-line"><b>Auth:</b> OFFICE OF THE DG/RHGI</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="rhgi-voter-impact-divider-wrap rhgi-divider-widget" role="presentation" aria-hidden="true">'
    '<div class="rhgi-voter-impact-divider"></div></div>',
    unsafe_allow_html=True,
)
_decider_box_projection = int(round((18.0 / 25.0) * BALLOT_BOXES_FEDERATION_2027))
_decider_mandate_progress_pct = 100.0 * float(PROJECTED_TOTAL) / float(max(NATIONAL_VOTE_TARGET, 1))
_decider_gap_to_target = int(NATIONAL_VOTE_TARGET - PROJECTED_TOTAL)
_decider_gap_to_target = max(0, _decider_gap_to_target)
_decider_kaduna_html = ""
if st.session_state.get("decider_facilitator_radio") == SULEIMAN_DECIDER_LABEL:
    _decider_kaduna_html = (
        f" · <b>Kaduna node (Suleiman): {KADUNA_SOVEREIGN_RECORD_ANCHOR:,} records mapped — 15/15 sync</b>"
    )
st.markdown(
    f"""
    <div class='rhgi-decider-shell'>
      <p class='rhgi-decider-label'>Decider • Suleiman / Coordinator</p>
      <p class='rhgi-decider-target'>Target: 18/25 Boxes per PU</p>
      <p class='rhgi-decider-sub'>
        18/25 projection: <b>{_decider_box_projection:,}</b> of {BALLOT_BOXES_FEDERATION_2027:,} ballot boxes
        · Mandate flow: <b>{_decider_mandate_progress_pct:.2f}%</b> of 20.7M
        · Gap: <b>{_decider_gap_to_target:,}</b>
        · Apathy comms floor: <b>{NATIONAL_TURNOUT_2023_PCT:.2f}%</b> (2023 turnout benchmark)
        {_decider_kaduna_html}
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.radio(
    "Decider · 15/15 facilitator sync",
    options=list(DECIDER_RADIO_OPTIONS),
    key="decider_facilitator_radio",
    horizontal=True,
    on_change=_sync_decider_facilitator_corridor,
    help=(
        "Suleiman: North West corridor lock + Kaduna state drill-down with the 276,060-record sovereign anchor. "
        "National coordinator clears the corridor filter."
    ),
)
metal_countdown_live_ph = st.empty()

_primaries_start_ms = int(PRIMARIES_START_WAT.timestamp() * 1000)
_gong_data_url = _threshold_gong_data_url() or ""

components.html(
    f"""
    <script>
      (function() {{
        if (window.__primaries_gong_listener_setup) return;
        window.__primaries_gong_listener_setup = true;

        const PRIMARIES_START_MS = {_primaries_start_ms};
        const GONG_DATA_URL = {_gong_data_url!r};

        function playGongFallback() {{
          try {{
            const Ctx = window.AudioContext || window.webkitAudioContext;
            const ctx = new Ctx();
            if (ctx.state === 'suspended') ctx.resume();

            const now = ctx.currentTime;
            const o = ctx.createOscillator();
            const g = ctx.createGain();
            o.type = 'sine';
            o.frequency.setValueAtTime(55, now);
            o.frequency.exponentialRampToValueAtTime(22, now + 0.8);
            g.gain.setValueAtTime(0.0001, now);
            g.gain.exponentialRampToValueAtTime(0.28, now + 0.02);
            g.gain.exponentialRampToValueAtTime(0.0001, now + 0.95);
            o.connect(g); g.connect(ctx.destination);
            o.start(now);
            o.stop(now + 1.0);
            setTimeout(() => {{ try {{ ctx.close(); }} catch(e){{}} }}, 1200);
          }} catch (e) {{}}
        }}

        function playGong() {{
          if (GONG_DATA_URL && GONG_DATA_URL.length > 20) {{
            try {{
              const a = new Audio(GONG_DATA_URL);
              a.volume = 0.65;
              const p = a.play();
              if (p && p.catch) p.catch(function(){{ playGongFallback(); }});
            }} catch(e) {{
              playGongFallback();
            }}
          }} else {{
            playGongFallback();
          }}
        }}

        function checkCountdown() {{
          const remMs = PRIMARIES_START_MS - Date.now();
          const remSec = Math.floor(remMs / 1000);

          if (remSec === 86400) {{
            if (!window.__primaries_gong_fired_24h) {{
              window.__primaries_gong_fired_24h = true;
              playGong();
            }}
          }}
        }}

        setInterval(checkCountdown, 250);
      }})();
    </script>
    """,
    height=0,
)


def _live_primaries_metal_clock_inner() -> None:
    now = datetime.now(_LAGOS_TZ)
    # Months are hard-anchored for Jan 16, 2027.
    months = "09"
    # Live sync: Weeks/Days/Hours/Minutes/Seconds pulse based on remaining time
    # within the Mar 26, 2026 → Jan 16, 2027 research window.
    # Static 09-month calibration window clamp:
    # - If we're before the calibration start, hold full 09-month window.
    # - Otherwise, count down from "now" to Jan 16, 2027.
    rem = (
        (ELECTION_TARGET_WAT - ELECTION_CALIBRATION_START_WAT)
        if now < ELECTION_CALIBRATION_START_WAT
        else (ELECTION_TARGET_WAT - now)
    )
    total_seconds = int(rem.total_seconds()) if rem.total_seconds() > 0 else 0
    weeks = total_seconds // 604_800
    total_seconds %= 604_800
    days = total_seconds // 86_400
    total_seconds %= 86_400
    hours = total_seconds // 3_600
    total_seconds %= 3_600
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    seconds_val = f"{seconds:02d}"

    metal_countdown_live_ph.markdown(
        f"""
        <div class="rhgi-metal-grid">
          <div class="rhgi-metal-box"><div class="rhgi-metal-box-inner"><div class="rhgi-metal-label">Months</div><div class="rhgi-metal-number">{months}</div></div></div>
          <div class="rhgi-metal-box"><div class="rhgi-metal-box-inner"><div class="rhgi-metal-label">Weeks</div><div class="rhgi-metal-number">{weeks}</div></div></div>
          <div class="rhgi-metal-box"><div class="rhgi-metal-box-inner"><div class="rhgi-metal-label">Days</div><div class="rhgi-metal-number">{days}</div></div></div>
          <div class="rhgi-metal-box"><div class="rhgi-metal-box-inner"><div class="rhgi-metal-label">Hours</div><div class="rhgi-metal-number">{hours:02d}</div></div></div>
          <div class="rhgi-metal-box"><div class="rhgi-metal-box-inner"><div class="rhgi-metal-label">Minutes</div><div class="rhgi-metal-number">{minutes:02d}</div></div></div>
          <div class="rhgi-metal-box rhgi-seconds-box"><div class="rhgi-metal-box-inner"><div class="rhgi-metal-label">Seconds</div><div class="rhgi-metal-number">{seconds_val}</div></div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

if hasattr(st, "fragment"):
    _live_cd = st.fragment(run_every=timedelta(milliseconds=100))(_live_primaries_metal_clock_inner)
    _live_cd()
else:
    _live_primaries_metal_clock_inner()

st.markdown(
    '<p class="rhgi-signature">Prepared by Galadiman Ruwa Center for Strategic Leadership and Communication GCSLC LTD/GTE.</p>',
    unsafe_allow_html=True,
)

# Sovereign Swing Illuminator (top horizontal strip above DG Corridor Hub).
_state_agg = dff.groupby("state", as_index=False).agg(
    apc_2023=("apc_2023", "sum"),
    pdp_2023=("pdp_2023", "sum"),
    lp_2023=("lp_2023", "sum"),
    adc_2023=("adc_2023", "sum"),
    registered_voters=("registered_voters", "sum"),
)
_state_agg["reg_2027_proxy"] = (_state_agg["registered_voters"].astype(float) * FORENSIC_2027_BALLOT_SCALE)
_state_agg["mov_2023"] = _state_agg[["apc_2023", "pdp_2023", "lp_2023", "adc_2023"]].apply(
    lambda r: sorted([float(r["apc_2023"]), float(r["pdp_2023"]), float(r["lp_2023"]), float(r["adc_2023"])], reverse=True)[0]
    - sorted([float(r["apc_2023"]), float(r["pdp_2023"]), float(r["lp_2023"]), float(r["adc_2023"])], reverse=True)[1],
    axis=1,
)
_state_agg["volatility"] = (_state_agg["reg_2027_proxy"] / (_state_agg["mov_2023"].abs() + 1.0))
_top5_states = ", ".join(_state_agg.sort_values("volatility", ascending=False).head(5)["state"].tolist())

_eastern_states = ["Enugu", "Abia", "Ebonyi", "Anambra", "Imo"]
_eastern_registered_total = float(
    dff.loc[dff["state"].isin(_eastern_states), "registered_voters"].sum()
)
_eastern_yield_potential = int(round((_eastern_registered_total * 0.73) * FORENSIC_2027_BALLOT_SCALE))

_registered_total = float(dff["registered_voters"].sum())
_votes_2023_total = float(dff[["apc_2023", "pdp_2023", "lp_2023", "adc_2023"]].sum().sum())
_non_voter_2023_total = max(0.0, _registered_total - _votes_2023_total)
_now_wat = datetime.now(_LAGOS_TZ)
_months_since_calibration = max(0.0, ((_now_wat - ELECTION_CALIBRATION_START_WAT).total_seconds()) / (30.4375 * 24 * 3600))
_engagement_factor_pct = min(15.0, _months_since_calibration * 1.5)
_apathy_adjusted_non_voters = max(0.0, _non_voter_2023_total * (1.0 - (_engagement_factor_pct / 100.0)))
_apathy_potential_votes = int(round(_apathy_adjusted_non_voters * FORENSIC_2027_BALLOT_SCALE))
_turnout_2027_dynamic_pct = 0.0 if _registered_total <= 0 else (100.0 - ((_apathy_adjusted_non_voters / _registered_total) * 100.0))
_turnout_2027_dynamic_pct = max(0.0, min(100.0, _turnout_2027_dynamic_pct))
_turnout_floor_2023 = 26.7
_turnout_target_2027 = 50.0
_window_total_s = max((ELECTION_TARGET_WAT - ELECTION_CALIBRATION_START_WAT).total_seconds(), 1.0)
_window_elapsed_s = (_now_wat - ELECTION_CALIBRATION_START_WAT).total_seconds()
_turnout_progress = max(0.0, min(1.0, _window_elapsed_s / _window_total_s))
_turnout_live_meter_pct = _turnout_floor_2023 + ((_turnout_target_2027 - _turnout_floor_2023) * _turnout_progress)
_engaged_youth_votes = max(0.0, _non_voter_2023_total - _apathy_adjusted_non_voters)
_youth_conversion_pu_equiv = int(round(min(POLLING_UNITS_BASELINE, (_engaged_youth_votes / max(_registered_total, 1.0)) * POLLING_UNITS_BASELINE)))
_youth_conversion_pct = 0.0 if POLLING_UNITS_BASELINE <= 0 else (100.0 * _youth_conversion_pu_equiv / POLLING_UNITS_BASELINE)

_zone_surge = dff.groupby("zone", as_index=False).agg(
    strike_priority=("strike_priority", "mean"),
    canvasser_ratio=("canvasser_ratio", "mean"),
    projected_total=("projected_total", "sum"),
)
_zone_surge["undecided_youth_surge"] = (
    (1.0 - (_zone_surge["canvasser_ratio"] / 15.0).clip(0, 1))
    * _zone_surge["strike_priority"].clip(lower=0)
    * (_zone_surge["projected_total"] * 0.60)
)
_resource_zone = str(_zone_surge.sort_values("undecided_youth_surge", ascending=False).iloc[0]["zone"]) if not _zone_surge.empty else "North West"

_deepfake_alert = any(not bool(r.get("verified", True)) for r in (_cien_audit_rows or []))
_swing_warn_cls = " warning" if _deepfake_alert else ""
_swing_status = "DEEPFAKE ALERT - WARNING GOLD" if _deepfake_alert else "CYBER-SHIELD STABLE"
_affected_states = sorted(
    {
        str(r.get("state", "")).strip()
        for r in (_cien_audit_rows or [])
        if (not bool(r.get("verified", True))) and str(r.get("state", "")).strip()
    }
)
_affected_state_label = _affected_states[0] if _affected_states else _resource_zone
_resource_vector_advice = (
    f"Target: Non-Oil Sector Youth Engagement in {html.escape(_affected_state_label)}"
    if _deepfake_alert
    else f"Target: Non-Oil Sector Youth Engagement in {html.escape(_resource_zone)}"
)
_sovereign_ticker_segments = [
    "20.7M MANDATE ZERO-HOUR: SATURDAY 16 JANUARY 2027 (WAT) — ELECTION ANCHOR LOCKED.",
    "GENERAL ELECTION DATE LOCK: SATURDAY 16 JANUARY 2027 (WAT) — SOVEREIGN TICKER ANCHOR.",
    "OIL IS THE PAST. YOUR SKILLS ARE THE NEW OIL: Powering the Non-Oil Future.",
    "YOUR VOTE IS A DIGITAL RECEIPT: The Forensic Vault is Open and Synced.",
    "WE AREN'T JUST VOTING. WE ARE RE-ENGINEERING: The 8R Paradigm in Action.",
]
_sovereign_ticker_text = "  ✦  ".join(_sovereign_ticker_segments)
_sovereign_ticker_html = (
    "<div class='rhgi-sovereign-marquee-wrap'>"
    "<div class='rhgi-sovereign-marquee-track'>"
    f"<span class='rhgi-sovereign-marquee-seg'>{html.escape(_sovereign_ticker_text)}</span>"
    f"<span class='rhgi-sovereign-marquee-seg'>{html.escape(_sovereign_ticker_text)}</span>"
    "</div>"
    "</div>"
)

st.markdown(
    f"""
    <div class='rhgi-swing-shell{_swing_warn_cls}'>
      <div class='rhgi-swing-inner'>
        <p class='rhgi-swing-title'>SOVEREIGN SWING HEADER • <span class='rhgi-ballot-anchor-white'>202,225 BALLOT-BOX BASELINE</span> • {_swing_status}</p>
        <div class='rhgi-swing-grid'>
          <div class='rhgi-swing-item rhgi-swing-item--silver'>
            <div class='rhgi-swing-k'>EASTERN STATES YIELD POTENTIAL</div>
            <div class='rhgi-swing-v'>
              Enugu, Abia, Ebonyi, Anambra, Imo (73% Apathy Target): <b>{(_eastern_yield_potential):,} votes</b>
            </div>
          </div>
          <div class='rhgi-swing-item rhgi-swing-item--gold'>
            <div class='rhgi-swing-k'>APATHY CONVERSION METER</div>
            <div class='rhgi-swing-v'>
              Gap analysis: 2023 national turnout benchmark <b>{NATIONAL_TURNOUT_2023_PCT:.2f}%</b> — apathy pool anchored to registered − 2023 votes.<br>
              Youth Conversion: {_youth_conversion_pct:.2f}% ({_youth_conversion_pu_equiv:,} / {POLLING_UNITS_BASELINE:,} PUs)<br>
              Turnout Meter: {_turnout_live_meter_pct:.2f}% (Floor 26.7% → Target 50.0%)
            </div>
          </div>
          <div class='rhgi-swing-item rhgi-swing-item--prism'>
            <div class='rhgi-swing-k'>RESOURCE VECTOR</div>
            <div class='rhgi-swing-v'>{_sovereign_ticker_html}<div style='margin-top:6px;'>{_resource_vector_advice}</div></div>
          </div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

_vol_df = dff_hub.copy()
_decider_factor = 18.0 / 25.0
_vol_df["decider_projected_total"] = _vol_df["projected_total"].astype(float) * _decider_factor
_vol_df["volatility_score"] = (
    _vol_df["decider_projected_total"] / (_vol_df["winning_margin"].abs().astype(float) + 1.0)
)
_vol_df = _vol_df.sort_values("volatility_score", ascending=False).reset_index(drop=True)
_loc_count = len(_vol_df)
_top20_count = max(1, int(_loc_count * 0.2 + 0.9999))
_vol_df["rank"] = _vol_df.index + 1
_vol_df["is_top20"] = _vol_df["rank"] <= _top20_count
_total_proj = float(_vol_df["decider_projected_total"].sum())
_mandate_80_cut = 0.8 * _total_proj
_vol_df["cum_projected"] = _vol_df["decider_projected_total"].cumsum()
_vol_df["in_80_mandate"] = _vol_df["cum_projected"] <= _mandate_80_cut
if not _vol_df.empty:
    _first_cross = int((_vol_df["cum_projected"] >= _mandate_80_cut).idxmax())
    _vol_df.loc[_first_cross, "in_80_mandate"] = True
_vol_focus = _vol_df[_vol_df["is_top20"]].copy()
if not _vol_focus.empty:
    _vol_focus["ward_box_target"] = 18
    _vol_focus["est_wards"] = (
        (_vol_focus["decider_projected_total"].astype(float) / max(_total_proj, 1.0)) * WARDS_BASELINE
    ).round().clip(lower=1).astype(int)
    _vol_focus["est_polling_units"] = (
        (_vol_focus["decider_projected_total"].astype(float) / max(_total_proj, 1.0)) * POLLING_UNITS_BASELINE
    ).round().clip(lower=1).astype(int)
    _vol_focus["est_boxes_2027"] = (
        (_vol_focus["decider_projected_total"].astype(float) / max(_total_proj, 1.0)) * BALLOT_BOXES_FEDERATION_2027
    ).round().clip(lower=1).astype(int)
    _vol_focus["target_boxes_18_of_25"] = (_vol_focus["est_boxes_2027"].astype(float) * _decider_factor).round().astype(int)
    _vol_focus["mandate_share_pct"] = (
        100.0 * _vol_focus["decider_projected_total"].astype(float) / max(_total_proj, 1.0)
    ).round(2)
    _vol_focus["Send Direct Message"] = _vol_focus.apply(
        lambda r: _sovereign_whatsapp_dm_url(str(r["state"]), str(r["lga"])),
        axis=1,
    )
    _vol_focus = _vol_focus.rename(
        columns={
            "state": "State",
            "lga": "High-Volatility Location",
            "volatility_score": "Volatility Score",
            "est_wards": "Est. High-Volatility Wards",
            "est_polling_units": "Est. High-Volatility PUs",
            "est_boxes_2027": "Est. 2027 Ballot Boxes",
            "target_boxes_18_of_25": "18/25 Target Boxes",
            "ward_box_target": "Decider Boxes/PU Target",
            "decider_projected_total": "Projected Votes (18/25 Sync)",
            "mandate_share_pct": "Mandate Share (%)",
        }
    )
    _vol_focus = _vol_focus[
        [
            "State",
            "High-Volatility Location",
            "Volatility Score",
            "Est. High-Volatility Wards",
            "Est. High-Volatility PUs",
            "Est. 2027 Ballot Boxes",
            "18/25 Target Boxes",
            "Decider Boxes/PU Target",
            "Projected Votes (18/25 Sync)",
            "Mandate Share (%)",
            "Send Direct Message",
        ]
    ]
    _top20_share = (100.0 * float(_vol_focus["Projected Votes (18/25 Sync)"].sum()) / max(_total_proj, 1.0))
    _gold_heading("Deciding States Table — High-Volatility Wards & Polling Units")
    st.caption(
        f"20/80 forensic filter anchored to the 18/25 box target from {BALLOT_BOXES_FEDERATION_2027:,} baseline boxes: "
        f"top 20% locations ({len(_vol_focus):,}/{_loc_count:,}) currently carry {_top20_share:.2f}% "
        f"of synced mandate flow."
    )
    _dm_col = st.column_config.LinkColumn(
        "Send Direct Message",
        help="Opens https://wa.me/2348099111515?text=… (sovereign apathy-reminder template, 18/25 target).",
        display_text="Send DM",
    )
    st.dataframe(
        _vol_focus.style.format(
            {
                "Volatility Score": "{:,.2f}",
                "Mandate Share (%)": "{:,.2f}",
                "Projected Votes (18/25 Sync)": "{:,.0f}",
            }
        ),
        use_container_width=True,
        hide_index=True,
        column_config={"Send Direct Message": _dm_col},
    )

_gold_heading("DG Corridor Command Hub")
st.markdown(
    f"""
    <div class='rhgi-corridor-foundation-shell'>
      <div class='rhgi-corridor-foundation-inner'>
        {_sovereign_ticker_html}
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
_hub_cols = st.columns(6)
for _hi, (_abbr, _zname) in enumerate(CORRIDOR_NODES):
    _btn_label = "NW (K3)" if _abbr == "NW" else _abbr
    _hub_active = st.session_state.get("dg_corridor") == _zname
    with _hub_cols[_hi]:
        if st.button(
            _btn_label,
            key=f"dg_hub_{_abbr}",
            use_container_width=True,
            help=_zname,
            type="primary" if _hub_active else "secondary",
        ):
            st.session_state.dg_corridor = _zname
            st.session_state.corridor_zone = _zname
            if _zname == "North West":
                st.session_state.decider_facilitator_radio = SULEIMAN_DECIDER_LABEL
                st.session_state["state_drill_North West"] = "Kaduna"
            st.session_state._prev_corridor_state_key = None
            st.rerun()
_hub_lbl = st.session_state.get("dg_corridor") or "ALL NIGERIA"
st.markdown(
    f'<p class="rhgi-forensic-baseline-line">Active command filter: {_hub_lbl} · Baseline '
    f"{POLLING_UNITS_BASELINE:,} PUs · {FORENSIC_2027_BALLOT_BASELINE_CAPTION}</p>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h3 style='color: #D4AF37; text-align: center; text-shadow: 0 0 10px #D4AF37;'>National overview • all corridors</h3>",
    unsafe_allow_html=True,
)
_nr1, _nr2, _nr3 = st.columns([1, 2, 1])
with _nr2:
    if st.button(
        "Reset national scope",
        key="dg_hub_nat",
        use_container_width=True,
    ):
        st.session_state.dg_corridor = None
        st.session_state.corridor_zone = None
        st.session_state.decider_facilitator_radio = NAT_DECIDER_LABEL
        st.session_state._prev_corridor_state_key = None
        st.rerun()
_r8_cols = st.columns(8)
for _ri, (_r8_label, _r8_det) in enumerate(EIGHT_R_DETERMINANTS):
    with _r8_cols[_ri]:
        st.button(
            _r8_label,
            key=f"r8_btn_{_ri}",
            help=_r8_det,
            use_container_width=True,
            type="secondary",
        )

c1, c2, c3 = st.columns(3)
# Global clock strip (updates every 1s) in header.
_pulse_cls = "rhgi-kpi rhgi-abuja-strobe" if abuja_strobe else "rhgi-kpi"
_c1_clock = c1.empty()


def _live_header_clocks_inner() -> None:
    _abuja_now = datetime.now(lagos_tz)
    _london_now = datetime.now(_LONDON_TZ)
    _ny_now = datetime.now(_NYC_TZ)
    _dubai_now = datetime.now(_DUBAI_TZ)
    _c1_clock.markdown(
        f"<div class='{_pulse_cls}'>"
        f"<b>Global Clocks</b><br>"
        f"Abuja (WAT): <span class='rhgi-glow'>{_abuja_now.strftime('%I:%M:%S %p WAT')}</span><br>"
        f"London: <span class='rhgi-glow'>{_london_now.strftime('%I:%M:%S %p %Z')}</span><br>"
        f"NY: <span class='rhgi-glow'>{_ny_now.strftime('%I:%M:%S %p %Z')}</span><br>"
        f"Dubai: <span class='rhgi-glow'>{_dubai_now.strftime('%I:%M:%S %p %Z')}</span>"
        f"<br><small style='color:#ffffff;font-weight:600;'>FCT APC (proj): {fct_pct:.2f}%</small>"
        f"</div>",
        unsafe_allow_html=True,
    )


if hasattr(st, "fragment"):
    _hdr_clocks = st.fragment(run_every=timedelta(seconds=1))(_live_header_clocks_inner)
    _hdr_clocks()
else:
    _live_header_clocks_inner()
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

_py_line = (
    f"{projected_yield_hub:,} <small>(corridor)</small>"
    if st.session_state.get("dg_corridor")
    else f"{projected_yield_nat:,}"
)
st.markdown(
    f"<div class='rhgi-kpi' style='margin-bottom:12px;'><b>20.7M mandate anchor</b> — Target: <span class='rhgi-glow'>{NATIONAL_VOTE_TARGET:,}</span> · "
    f"Projected yield: <span class='rhgi-glow'>{_py_line}</span> · "
    f"<b>Remittance gap:</b> <span class='rhgi-glow'>{remittance_gap:,}</span></div>",
    unsafe_allow_html=True,
)

(tab_global,) = st.tabs(["GLOBAL OVERVIEW (ACTIVE)"])
with tab_global:
    # POSITION 1 (Top): charts
    _axis_title_font = dict(family="Goldman, sans-serif", size=14, color=GOLD)
    _tick_font = dict(family="Goldman, sans-serif", size=12, color="#ffffff")

    _zone_l, _zone_r = st.columns([1.7, 1])
    with _zone_r:
        _feed_lines = "".join(
            f'<div class="rhgi-sovereign-feed-line">{html.escape(line)}</div>'
            for line in st.session_state.get("sovereign_feed_log", [])[:45]
        )
        st.markdown(
            f'<div class="rhgi-sovereign-feed-wrap"><div class="rhgi-sovereign-feed-title">SOVEREIGN FEED</div>'
            f'<div class="rhgi-sovereign-feed-window">{_feed_lines}</div>'
            f'<div class="rhgi-sovereign-feed-meta">{RHGI_CELL_MODEL_1515:,} cells · 15/15 · live directive bridge</div></div>',
            unsafe_allow_html=True,
        )
    with _zone_l:
        _gold_heading("Winning Margin by Geopolitical Zone (turnout-adjusted)")
        st.caption(
            "Opposition Merger Tracker overlay: ADC Coalition Strength vs RHGI 15/15 Density (by zone)."
        )
        zone_margin = (
            dff_hub.groupby("zone", as_index=False)["winning_margin"].sum().sort_values("winning_margin")
        )
        fig_zone = px.bar(
            zone_margin,
            x="zone",
            y="winning_margin",
            color_discrete_sequence=[GOLD],
        )
        fig_zone.update_layout(
            template=None,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Goldman, sans-serif", color="#ffffff", size=13),
            font_color="#ffffff",
            showlegend=True,
            margin=dict(t=52, b=52, l=72, r=88),
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
                zeroline=True,
                zerolinecolor="rgba(255,255,255,0.22)",
                zerolinewidth=1,
                linecolor="rgba(255,255,255,0.4)",
            ),
            legend=dict(
                font=dict(family="Goldman, sans-serif", color="#ffffff", size=11),
                bgcolor="rgba(0,0,128,0.45)",
                bordercolor="rgba(212,175,55,0.35)",
                borderwidth=1,
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
            ),
        )
        fig_zone.update_traces(marker=dict(color=YELLOW_GOLD))
        _pt_z = dff_hub["projected_total"].replace(0, 1)
        _merger_share = 100.0 * (dff_hub["adc_2027"] + dff_hub["lp_2027"]) / _pt_z
        _tmp_m = dff_hub.assign(_merger_share=_merger_share)
        _merger_zone = _tmp_m.groupby("zone", as_index=False).agg(
            adc_coalition_strength=("_merger_share", "mean"),
            rhgi_15_15_density=(
                "canvasser_ratio",
                lambda s: float((s.clip(upper=15.0) / 15.0 * 100.0).mean()),
            ),
        )
        _mzone = zone_margin.merge(_merger_zone, on="zone", how="left")
        fig_zone.add_trace(
            go.Scatter(
                x=_mzone["zone"],
                y=_mzone["adc_coalition_strength"],
                name="ADC Coalition Strength",
                yaxis="y2",
                mode="lines+markers",
                line=dict(color="#ffffff", width=2),
                marker=dict(size=8, color="#ffffff"),
            )
        )
        fig_zone.add_trace(
            go.Scatter(
                x=_mzone["zone"],
                y=_mzone["rhgi_15_15_density"],
                name="RHGI 15/15 Density",
                yaxis="y2",
                mode="lines+markers",
                line=dict(color=YELLOW_GOLD, width=2),
                marker=dict(size=8, color=YELLOW_GOLD),
            )
        )
        fig_zone.update_layout(
            yaxis2=dict(
                title=dict(
                    text="Opposition Merger Tracker · 0–100",
                    font=dict(family="Goldman, sans-serif", color="#ffffff", size=11),
                ),
                overlaying="y",
                side="right",
                range=[0, 100],
                showgrid=False,
                tickfont=dict(family="Goldman, sans-serif", color="#ffffff", size=10),
            ),
        )
        st.plotly_chart(fig_zone, use_container_width=True)

    _gold_heading("Harvest Trendline")
    st.caption("Food Inflation (12.12%) vs Growth (4.4%) vs Reserves ($50B+).")
    st.markdown(
        "<div class='rhgi-prism-narrative-frame'>"
        "CATEGORY 1 NARRATIVE: Harvest Trendline anchors Food Inflation (12.12%) versus Growth (4.4%) "
        "and reserves ($50B+), keeping the mandate resilient under price pressure."
        "</div>",
        unsafe_allow_html=True,
    )
    harvest = pd.DataFrame(
        {
            "Epoch": ["Q1", "Q2", "Q3", "Q4"],
            "Food Inflation (%)": [12.12, 12.45, 12.20, HARVEST_FOOD_INFLATION_PCT],
            "Growth (%)": [3.80, 4.00, 4.20, HARVEST_GROWTH_PCT],
            "Reserves (USD Bn)": [46.0, 47.5, 49.2, HARVEST_RESERVES_BN_USD],
        }
    )
    fig_harvest = go.Figure()
    fig_harvest.add_trace(
        go.Scatter(
            x=harvest["Epoch"],
            y=harvest["Food Inflation (%)"],
            mode="lines+markers",
            name="Food Inflation",
            line=dict(color="#ffffff", width=2),
            marker=dict(size=7, color="#ffffff"),
        )
    )
    fig_harvest.add_trace(
        go.Scatter(
            x=harvest["Epoch"],
            y=harvest["Growth (%)"],
            mode="lines+markers",
            name="Growth",
            line=dict(color=YELLOW_GOLD, width=3),
            marker=dict(size=8, color=YELLOW_GOLD),
        )
    )
    fig_harvest.add_trace(
        go.Scatter(
            x=harvest["Epoch"],
            y=harvest["Reserves (USD Bn)"],
            mode="lines+markers",
            name="Reserves ($B+)",
            yaxis="y2",
            line=dict(color="#b8962e", width=2),
            marker=dict(size=7, color="#b8962e"),
        )
    )
    fig_harvest.update_layout(
        template=None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Goldman, sans-serif", color="#ffffff", size=13),
        font_color="#ffffff",
        legend=dict(
            title=dict(text="Harvest metrics", font=dict(family="Goldman, sans-serif", color=GOLD, size=13)),
            font=dict(family="Goldman, sans-serif", color="#ffffff", size=12),
            bgcolor="rgba(0,0,128,0.5)",
            bordercolor="rgba(212,175,55,0.35)",
            borderwidth=1,
        ),
        xaxis=dict(
            title=dict(text="Quarter", font=_axis_title_font),
            tickfont=_tick_font,
            showgrid=False,
            linecolor="rgba(255,255,255,0.4)",
            zeroline=False,
        ),
        yaxis=dict(
            title=dict(text="Inflation / Growth (%)", font=dict(family="Goldman, sans-serif", size=14, color=GOLD)),
            tickfont=_tick_font,
            showgrid=True,
            gridcolor="rgba(255,255,255,0.12)",
            zerolinecolor="rgba(255,255,255,0.22)",
            linecolor="rgba(255,255,255,0.4)",
        ),
        yaxis2=dict(
            title=dict(text="Reserves (USD Bn)", font=dict(family="Goldman, sans-serif", color="#ffffff", size=12)),
            overlaying="y",
            side="right",
            showgrid=False,
            tickfont=dict(family="Goldman, sans-serif", color="#ffffff", size=10),
        ),
        margin=dict(t=36, b=48, l=72, r=36),
    )
    st.plotly_chart(fig_harvest, use_container_width=True)

    # POSITION 2 — Forensic audit shadow (independent 15/15 node counter)
    _forensic_verified = int((dff_hub["canvasser_ratio"] >= 15.0).sum())
    st.markdown(
        f'<div class="rhgi-forensic-shadow">RHGI FORENSIC SHADOW: {_forensic_verified:,} Verified 15/15 Nodes<br>'
        f'<small style="color:#ffffff;font-weight:600;opacity:0.92;">Independent receipt of the 20.7M Mandate — forensic chain silences skeptics.</small></div>',
        unsafe_allow_html=True,
    )

    # POSITION 2b — 15/15 Sovereign Directive bridge (WhatsApp handshake; 2023 apathy floor)
    _nodes1515 = dff_hub.loc[dff_hub["canvasser_ratio"] >= 15.0].copy()
    _nodes1515 = _nodes1515.sort_values("strike_priority", ascending=False).head(24)
    st.caption(
        f"Pure model: {RHGI_CELL_MODEL_1515:,} RHGI cells @ 15/15 — daily apathy quota from 2023 turnout benchmark (spread to election anchor). "
        "No alternate rep-tier geometry."
    )
    _dir_cols = st.columns(3)
    for _ni, (_, _nr) in enumerate(_nodes1515.iterrows()):
        _s = str(_nr["state"])
        _l = str(_nr["lga"])
        _daily = _lga_daily_apathy_target(
            float(_nr["registered_voters"]),
            float(_nr["turnout_2023_rate"]),
            ELECTION_TARGET_WAT,
        )
        _wa_u = _sovereign_directive_wa_url(_s, _l, _daily)
        with _dir_cols[_ni % 3]:
            st.markdown(
                f"<div style='color:#ffffff;font-size:0.8rem;font-weight:700;'>{html.escape(_s)} · {html.escape(_l[:26])}</div>"
                f"<div style='color:#00CED1;font-size:0.74rem;margin-bottom:6px;'>Apathy TODAY (2023 benchmark): <b>{_daily:,}</b></div>",
                unsafe_allow_html=True,
            )
            st.link_button(
                "Send Sovereign Directive",
                _wa_u,
                use_container_width=True,
                help="Opens https://wa.me/2348099111515?text=… with the sovereign template (2023 turnout → daily apathy quota).",
            )

    # POSITION 3a — Constitutional mandate banner
    if constitutional_ok:
        st.markdown(
            "<div class='rhgi-mandate-secured'><span class='rhgi-glow' style='font-size:1.35rem;font-weight:800;'>"
            "CONSTITUTIONAL MANDATE: SECURED</span><br>"
            "<small style='color:#ffffff;'>Legal Gatekeeper — ≥24 of 36 states at ≥25% APC and FCT ≥25%</small></div>",
            unsafe_allow_html=True,
        )

    # POSITION 3b — Sovereign Mirror Map (carto-positron) + opposition threat toggle
    st.markdown(
        "<p class='rhgi-narrative-label rhgi-narrative-label--cyan'>Threat Monitor (high ADC + LP / NNPP activity proxy)</p>",
        unsafe_allow_html=True,
    )
    _tm = st.checkbox(
        "Threat Monitor (high ADC + LP / NNPP activity proxy)",
        value=st.session_state.get("threat_monitor", False),
        key="threat_monitor_toggle",
        label_visibility="collapsed",
    )
    st.markdown(
        "<p class='rhgi-narrative-label rhgi-narrative-label--amber'>Heritage Spine layer (AKK + Coastal Highway)</p>",
        unsafe_allow_html=True,
    )
    _heritage_toggle = st.checkbox(
        "Heritage Spine layer (AKK + Coastal Highway)",
        value=True,
        key="heritage_spine_toggle",
        label_visibility="collapsed",
    )
    st.markdown(
        "<p class='rhgi-narrative-label rhgi-narrative-label--cyan'>Stability Heatmap (Operation Kukan Kura)</p>",
        unsafe_allow_html=True,
    )
    _stability_toggle = st.checkbox(
        "Stability Heatmap (Operation Kukan Kura)",
        value=True,
        key="stability_heat_toggle",
        label_visibility="collapsed",
    )
    st.session_state.threat_monitor = _tm
    st.session_state.opposition_heatmap = _tm
    st.markdown(
        "<div class='rhgi-prism-narrative-frame' style='margin-top:8px;'>"
        "CATEGORY 2 NARRATIVE: Concrete Heritage tracks AKK Road Section 1 at <span style='color:#ffffff;font-weight:900;'>80%</span> "
        "completion alongside Non-Oil Sector Opportunities via Innovation Heritage (100k+ high-tech roles for the "
        "60% youth demographic), while the Stability Heatmap reflects Operation Kukan Kura crime-drop pulse across "
        "mapped LGAs."
        "</div>",
        unsafe_allow_html=True,
    )
    _gold_heading(
        "774 LGA heatmap — threat monitor (ADC + LP)" if _tm else "774 LGA heatmap — winning margin (rugged)"
    )
    lga_map_df = enrich_lga_map_metrics(build_lga_heatmap_df(dff_hub))
    _mv = st.session_state.get("map_view")
    if _mv and isinstance(_mv, dict) and "lat" in _mv and "lon" in _mv:
        _fig_center = {"lat": float(_mv["lat"]), "lon": float(_mv["lon"])}
        _fig_zoom = float(_mv.get("zoom", 10.2))
    else:
        _fig_center = {"lat": 9.082, "lon": 8.6753}
        _fig_zoom = 4.9
    fig_lga = build_lga_winning_margin_figure(
        lga_map_df,
        zoom=_fig_zoom,
        center=_fig_center,
        threat_monitor=st.session_state.threat_monitor,
    )
    if _heritage_toggle:
        for _corr, _g in _heritage_layer_df.groupby("corridor"):
            fig_lga.add_trace(
                go.Scattermapbox(
                    lat=_g["lat"],
                    lon=_g["lon"],
                    mode="lines+markers",
                    line=dict(color=YELLOW_GOLD, width=3),
                    marker=dict(size=9, color=YELLOW_GOLD),
                    name=f"Heritage Spine · {_corr}",
                    hovertemplate=f"{_corr}<br>Completion: %{{customdata[0]}}%<extra></extra>",
                    customdata=_g[["completion_pct"]].values,
                )
            )
    if _stability_toggle:
        fig_lga.add_trace(
            go.Scattermapbox(
                lat=_stability_heat_df["lat"],
                lon=_stability_heat_df["lon"],
                mode="markers",
                marker=dict(
                    size=16,
                    color=_stability_heat_df["crime_drop_pct"],
                    colorscale=[[0, "#1A0033"], [0.5, "#B87333"], [1.0, "#FFD700"]],
                    opacity=0.46,
                    showscale=False,
                ),
                name="Stability Heatmap",
                hovertemplate="Crime drop: %{customdata[0]:.1f}%<extra></extra>",
                customdata=_stability_heat_df[["crime_drop_pct"]].values,
            )
        )
    st.plotly_chart(fig_lga, use_container_width=True)
    if st.session_state.get("map_view"):
        if st.button("Reset map to national (carto‑positron) view", key="reset_map_national_btn"):
            st.session_state.map_view = None
            st.rerun()

    # POSITION 3 (Below map): CIEN widgets
    st.markdown(
        """
        <div class="rhgi-cien-row">
          <div class="rhgi-cien-card">
            <h3>CIEN-C</h3>
            <div class="cien-sub">GeoCanvasser verification node — field geometry and corridor activation integrity.</div>
            <div class="cien-chip">STATUS · ACTIVE</div>
          </div>
          <div class="rhgi-cien-card">
            <h3>CIEN-I</h3>
            <div class="cien-sub">Data Integrity verification — PVC, turnout, and sovereign yield attestation.</div>
            <div class="cien-chip">STATUS · ACTIVE</div>
          </div>
          <div class="rhgi-cien-card">
            <h3>CIEN-E</h3>
            <div class="cien-sub">Logistics Fuel verification — deployment chain and remittance discipline lock.</div>
            <div class="cien-chip">STATUS · ACTIVE</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Remaining sections — LGA drill-down (uses DG hub corridor selection)
    _rose_heading("Corridor LGA drill-down (774 LGAs)")
    st.caption(
        "LGA roll-up ≈ one row every 0.5s (slow-mo); hover the marquee to pause. "
        "Canvasser budget = ₦30,000 × canvasser headcount per LGA."
    )
    if not st.session_state.get("dg_corridor"):
        st.session_state._prev_corridor_state_key = None
        st.markdown(
            '<p class="rhgi-creed" style="margin-top:8px;">Select a corridor in the DG Command Hub to open state / LGA drill-down.</p>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<p class="rhgi-corridor-gold-heading" style="font-size:1.12rem;margin-top:6px;">Active corridor · '
            f'<span style="color:#ffffff;">{html.escape(st.session_state.dg_corridor)}</span></p>',
            unsafe_allow_html=True,
        )
        _states_in_zone = sorted(dff_hub["state"].unique())
        _sel_state = st.selectbox(
            "State (drill-down)",
            options=_states_in_zone,
            index=0,
            key=f"state_drill_{st.session_state.dg_corridor}",
        )
        _corridor_state_key = f"{st.session_state.dg_corridor}|{_sel_state}"
        _state_just_changed = st.session_state._prev_corridor_state_key != _corridor_state_key
        st.session_state._prev_corridor_state_key = _corridor_state_key
        _mat = build_state_lga_matrix_df(dff_hub, _sel_state)
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
              ({RHGI_CELL_MODEL_1515:,} canvassers + {RHGI_CELL_MODEL_1515:,} E-day staff) × ₦30,000 → ₦{_sb_base/1e9:.2f}B;
              +15% misc → ₦{_sb_after_misc/1e9:.2f}B; +10% contingency → line-model subtotal <b>₦{_sb_line_total:,}</b> (₦{_sb_line_bn:.2f}B).
              RHGI sovereign headline total: <b>₦{_sb_mandate_bn:,.2f} billion</b>.
            </p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _gold_heading("Turnout heatmap — Nigeria (strike priority)")
    state_hm = build_state_heatmap_df(dff_hub)
    state_hm["mandate_status"] = state_hm["canvasser_ratio"].apply(
        lambda r: f"{min(15, max(0, int(round(float(r)))) )}/15 Voters Secured"
    )
    state_hm["logistics_fuel"] = (
        state_hm["canvassers"].astype(float) * CANVASSER_BUDGET_ANCHOR_NGN
    ).round()
    fig_scatter = px.scatter_mapbox(
        state_hm,
        lat="lat",
        lon="lon",
        color="strike_priority",
        size="strike_priority",
        hover_name="state",
        hover_data={"pvc_collection_rate": False, "turnout_2023_rate": False},
        custom_data=["mandate_status", "logistics_fuel"],
        color_continuous_scale=[[0, "#1A0033"], [0.5, "#B87333"], [1.0, "#FFD700"]],
        mapbox_style="carto-positron",
        zoom=4.85,
        center={"lat": 9.082, "lon": 8.6753},
    )
    fig_scatter.update_traces(
        marker=dict(
            size=_LGA_MARKER_INNER,
            color=state_hm["strike_priority"].astype(float).tolist(),
            colorscale=[[0, "#1A0033"], [0.5, "#B87333"], [1.0, "#FFD700"]],
            opacity=0.8,
        ),
        hovertemplate=(
            "<b>%{hovertext}</b>"
            "<br>Mandate Status: %{customdata[0]}"
            "<br>Logistics Fuel: ₦%{customdata[1]:,.0f}"
            "<extra></extra>"
        ),
    )
    _state_outline_color = "#000080"  # Prism Navy sharp outline
    _state_inner = fig_scatter.data[0]
    _state_outline = go.Scattermapbox(
        lat=_state_inner.lat,
        lon=_state_inner.lon,
        mode="markers",
        marker=dict(size=_LGA_MARKER_OUTLINE, color=_state_outline_color),
        hoverinfo="skip",
        showlegend=False,
    )
    fig_scatter = go.Figure(data=[_state_outline] + list(fig_scatter.data), layout=fig_scatter.layout)
    fig_scatter.update_layout(
        template=None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Goldman, sans-serif", color="#ffffff", size=13),
        font_color="#ffffff",
        hoverlabel=dict(font=dict(family="Goldman, sans-serif", color="#ffffff", size=12)),
        margin=dict(l=0, r=0, t=12, b=0),
        coloraxis_colorbar=dict(
            title=dict(text="Strike priority", font=dict(family="Goldman, sans-serif", color=GOLD, size=12)),
            tickfont=dict(family="Goldman, sans-serif", color="#ffffff", size=11),
            bgcolor="rgba(0,0,128,0.55)",
            bordercolor="rgba(212,175,55,0.35)",
            len=0.72,
        ),
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    _ticker = (
        f"20.7M MANDATE ZERO-HOUR — Saturday 16 January 2027 (WAT) · ELECTION ANCHOR · "
        f"NATIONAL PROJECTION — APC votes {apc_national:,} · Total projected {projected_yield_nat:,} · "
        f"APC share {national_apc_share:.2f}% · Legal Gatekeeper {states_25}/36 states ≥25% APC · "
        f"FCT APC {fct_pct:.2f}% · Remittance gap {remittance_gap:,} vs 20.7M anchor · "
        f"Turnout lift +{turnout_lift}% (live) · "
    )
    st.markdown(
        f"<div class='rhgi-ticker-wrap'><div class='rhgi-ticker'><span>{_ticker}</span><span>{_ticker}</span></div></div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class='rhgi-glossary-shell'>
          <div class='rhgi-glossary-inner'>
            <p class='rhgi-glossary-title'>SOVEREIGN GLOSSARY</p>
            <div class='rhgi-glossary-grid'>
              <div class='rhgi-glossary-item'><b>SSMI:</b> Scientific Support Model Initiative — geofences Nigeria&apos;s 176,846 PUs into 15/15 canvasser cells under the {RHGI_CELL_MODEL_1515:,}-cell RHGI geometry (no alternate &quot;unit rep&quot; layer).</div>
              <div class='rhgi-glossary-item'><b>CSV Payload:</b> Standardized PU dataset (e.g., Abia State PUs), ingested to ground the Heritage Spine to physical coordinates.</div>
              <div class='rhgi-glossary-item'><b>8R Paradigm:</b> Refine, Reset, Research... The 8-stage strategic engine driving the mandate.</div>
              <div class='rhgi-glossary-item'><b>Cyber-Sovereignty Node:</b> The Digital Shield for rapid-response verification of AI-driven deepfakes and misinformation.</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
