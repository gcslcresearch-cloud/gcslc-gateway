"""
KYSAH — Know Your Student to his Area and Home.

Alphabet DNA (implementation contract):
  A — Anchor: Termii proves handset control before a ping becomes a Sovereign Alert.
  B — Bin: federation-scale rollups (state / hex) so the UI never plots thousands of raw dots.
  C — Correlate: each alert inherits National Resonance (NTW corridor) + logistics void pressure.
  D — Duty: distress elevates sentinel mode; aggregate display preserves youth privacy.

Sentinel copy order: **Area** (campus / LGA vicinage) first, **Home** (ward / residence mesh) second.

Termii is the verification rail; K-GEC is the geographic and institutional truth layer.
"""

from __future__ import annotations

import json
import os
import re
from collections import Counter
from pathlib import Path
from typing import Any

from sovereign_active_intel import build_total_reality_summary, dominant_ntw_operator

BASE_DIR = Path(__file__).resolve().parent
KYSAH_SAFETY_STUB_JSON = BASE_DIR / "Part_04_Social" / "data" / "kysah_safety_ingest_stub.json"

TIER_STATE_GOLD = "state_gold"
TIER_AREA_CYAN = "area_cyan"
TIER_HOME_WHITE = "home_white"
TIER_PU_RED = "pu_red"
# Legacy ingest slugs (still accepted)
_LEGACY_AREA_KEYS = ("area_token", "lga_token")
_LEGACY_HOME_KEYS = ("home_token", "ward_token")


def load_kysah_stub_records(path: Path | None = None) -> list[dict[str, Any]]:
    p = path or KYSAH_SAFETY_STUB_JSON
    if not p.is_file():
        return []
    try:
        blob = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    rows = [r for r in (blob.get("records") or []) if isinstance(r, dict)]
    return rows


def kysah_area_token(rec: dict[str, Any]) -> str:
    """Chairman protocol: Area before Home — campus / LGA vicinage label."""
    for k in _LEGACY_AREA_KEYS:
        v = rec.get(k)
        if v is not None and str(v).strip():
            return str(v).strip()
    return "?"


def kysah_home_token(rec: dict[str, Any]) -> str:
    """Residence / ward-home mesh label."""
    for k in _LEGACY_HOME_KEYS:
        v = rec.get(k)
        if v is not None and str(v).strip():
            return str(v).strip()
    return "?"


def _normalize_admin_tier_slug(raw: str) -> str:
    s = (raw or "").strip().lower()
    aliases = {
        "lga_cyan": TIER_AREA_CYAN,
        "ward_white": TIER_HOME_WHITE,
        "home_white": TIER_HOME_WHITE,
    }
    return aliases.get(s, s)


def kysah_escalation_patrol_sniffs(
    records: list[dict[str, Any]],
    *,
    limit: int = 4,
) -> list[str]:
    """Parent-window sniff lines — Area first, then Home, only for safety escalation pings."""
    out: list[str] = []
    for rec in records:
        if str(rec.get("ping_type") or "").strip().lower() != "distress":
            continue
        area = kysah_area_token(rec)
        home = kysah_home_token(rec)
        st = str(rec.get("state") or "?").strip()
        eid = str(rec.get("event_id") or "?").strip()
        inst = str(rec.get("institution_id") or "").strip()
        tail = f" · {inst}" if inst else ""
        out.append(
            f"K-GEC Sentinel · KYSAH · Area {area} · Home {home} · {st} · Sovereign Alert {eid}{tail} "
            "— duty-of-care escalation (Area → Home bind)"
        )
        if len(out) >= limit:
            break
    return out


def kysah_distress_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Rows eligible for Sentinel patrol override (distress + lat/lon)."""
    out: list[dict[str, Any]] = []
    for rec in records:
        if str(rec.get("ping_type") or "").strip().lower() != "distress":
            continue
        try:
            float(rec["lat"])
            float(rec["lon"])
        except (KeyError, TypeError, ValueError):
            continue
        out.append(rec)
    return out


def kysah_escalation_shout_rows(
    records: list[dict[str, Any]],
    *,
    limit: int = 4,
) -> list[dict[str, Any]]:
    """Eagle ticker rows — headline carries Area; detail carries Home (Chairman order)."""
    from datetime import datetime, timezone

    out: list[dict[str, Any]] = []
    for rec in records:
        if str(rec.get("ping_type") or "").strip().lower() != "distress":
            continue
        area = kysah_area_token(rec)
        home = kysah_home_token(rec)
        st = str(rec.get("state") or "?").strip()
        eid = str(rec.get("event_id") or "?").strip()
        out.append(
            {
                "ts_iso": str(rec.get("ts_iso") or datetime.now(timezone.utc).isoformat())[:32],
                "ts_sort": 9e6,
                "pulse": "friction",
                "headline": f"K-GEC Sentinel · KYSAH · Area {area}",
                "detail": f"Home {home} · {st} · Sovereign Alert {eid} — escalation",
                "weight": 1.85,
            }
        )
        if len(out) >= limit:
            break
    return out


def kysah_admin_cell_id(lat: float, lon: float, *, precision: int = 3) -> str:
    """Stable coarse bin for federation rollups (not a geohash — intentional simplicity)."""
    return f"{round(lat, precision)}:{round(lon, precision)}"


def termii_normalize_callback(body: dict[str, Any]) -> dict[str, Any]:
    """
    Map Termii delivery / OTP callback JSON to an internal KYSAH verification fact.

    Live integrations should POST Termii webhooks to your ingress (mirror consumes normalized rows only).
    Canonical geography keys on ingest rows: `area_token`, `home_token` (Area and Home).
    Field names vary by product — we accept common aliases.
    """
    pin_id = str(
        body.get("pinId")
        or body.get("pin_id")
        or body.get("message_id")
        or body.get("messageId")
        or ""
    ).strip()
    phone = str(body.get("phone_number") or body.get("phone") or body.get("to") or "").strip()
    status = str(body.get("status") or body.get("message_status") or "unknown").strip().lower()
    verified = status in ("verified", "success", "sent", "delivered", "confirmed")
    return {
        "termii_pin_id": pin_id,
        "termii_phone_tail": _phone_tail(phone),
        "termii_status": status,
        "termii_verified_ok": verified,
        "source_chain": ["termii_callback", "termii_normalize_callback"],
    }


def _phone_tail(phone: str) -> str:
    d = re.sub(r"\D+", "", phone or "")
    return d[-4:] if len(d) >= 4 else ""


def correlate_kysah_sovereign_alert(
    event: dict[str, Any],
    *,
    state: str,
    ntw_audit_blob: dict[str, Any],
    ntw_operator: str,
    reality: dict[str, Any],
) -> dict[str, Any]:
    """
    Promote a student ping from 'dot' to Sovereign Alert: fuse National Resonance + void context.

    `reality` should be build_total_reality_summary(...) for the student's state.
    """
    from ntw_regional_audit import _operator_corridor_means

    cov_m, sim_m = _operator_corridor_means(ntw_audit_blob, ntw_operator)
    fin = float(reality.get("financial_inclusion_score") or 50.0)
    fr = reality.get("friction") if isinstance(reality.get("friction"), dict) else {}
    ncc_n = int(fr.get("ncc_incidents_in_state") or 0)
    void_n = int(fr.get("signal_void_events_in_state") or 0)
    void_pressure = min(
        1.0,
        max(0.0, (100.0 - fin) / 100.0 * 0.55 + min(0.45, 0.09 * ncc_n + 0.06 * void_n)),
    )
    tier = _normalize_admin_tier_slug(str(event.get("admin_tier_resolution") or TIER_HOME_WHITE))
    ping_type = str(event.get("ping_type") or "check_in").strip().lower()
    severity = 0.35 + 0.45 * void_pressure + (0.35 if ping_type == "distress" else 0.0)
    severity = min(1.0, severity)
    envelope = {
        "sovereign_alert_id": str(event.get("event_id") or "KYSAH-UNKNOWN"),
        "kysah_tier": tier,
        "ping_type": ping_type,
        "state": state,
        "national_resonance": {
            "operator": ntw_operator,
            "corridor_ran_mu_pct": round(cov_m, 2),
            "corridor_sim_mu_pct": round(sim_m, 2),
            "note": "Bound to NTW regional audit — same chamber as National Resonance sniffs.",
        },
        "logistics_void_context": {
            "financial_inclusion_score": fin,
            "financial_inclusion_verdict": str(reality.get("financial_inclusion_verdict") or ""),
            "ncc_incidents_in_state": ncc_n,
            "signal_void_events_in_state": void_n,
            "void_pressure_index": round(void_pressure, 4),
            "friction_summary": str(fr.get("friction_summary") or ""),
        },
        "sentinel_escalation": ping_type == "distress" or severity >= 0.82,
        "severity": round(severity, 4),
        "source_chain": list(event.get("source_chain") or [])
        + ["kysah_sovereign_correlation", "national_resonance_bind", "logistics_void_bind"],
    }
    return envelope


def federated_kysah_rollup(
    records: list[dict[str, Any]],
    *,
    top_states: int = 8,
    priority_queue: int = 8,
) -> dict[str, Any]:
    """
    Masterpiece logic at federation scale: never render N raw pings — aggregate + priority slice.

    Thousands of pings collapse to state histogram + hex-adjacent counts + highest-severity queue keys only.
    """
    by_state: Counter[str] = Counter()
    by_cell: Counter[str] = Counter()
    distress = 0
    for rec in records:
        st = str(rec.get("state") or "").strip()
        if st:
            by_state[st] += 1
        try:
            la, lo = float(rec["lat"]), float(rec["lon"])
            by_cell[kysah_admin_cell_id(la, lo)] += 1
        except (KeyError, TypeError, ValueError):
            pass
        if str(rec.get("ping_type") or "").lower() == "distress":
            distress += 1
    state_facets = [s for s, _ in by_state.most_common(top_states)]
    hot_cells = [c for c, _ in by_cell.most_common(12)]
    pq = sorted(
        records,
        key=lambda r: (
            1 if str(r.get("ping_type") or "").lower() == "distress" else 0,
            str(r.get("ts_iso") or ""),
        ),
        reverse=True,
    )[:priority_queue]
    return {
        "total_records": len(records),
        "distress_count": distress,
        "state_facets": state_facets,
        "state_histogram": dict(by_state.most_common(37)),
        "hot_admin_cells": hot_cells,
        "priority_event_ids": [str(x.get("event_id") or "") for x in pq if x.get("event_id")],
    }


def build_kysah_sovereign_bundle_for_state(
    state: str,
    *,
    records_for_state: list[dict[str, Any]],
    fused_df: Any,
    national_pu_df: Any,
    ncc_rows: list[dict],
    signal_rows: list[dict],
    fin_points: list[dict],
    states_geojson: dict[str, Any] | None,
    ntw_proxy: dict[str, Any],
    ntw_audit_blob: dict[str, Any],
) -> dict[str, Any]:
    """One state's reality summary + rollup + one correlated sample envelope (for ribbon proof)."""
    dom_op, _ = dominant_ntw_operator(state, ntw_proxy)
    reality = build_total_reality_summary(
        state,
        fused_df=fused_df,
        national_pu_df=national_pu_df,
        ncc_rows=ncc_rows,
        signal_rows=signal_rows,
        fin_points=fin_points,
        states_geojson=states_geojson,
        ntw_proxy=ntw_proxy,
    )
    rollup = federated_kysah_rollup(records_for_state)
    sample_env: dict[str, Any] | None = None
    if records_for_state:
        sample_env = correlate_kysah_sovereign_alert(
            records_for_state[0],
            state=state,
            ntw_audit_blob=ntw_audit_blob,
            ntw_operator=dom_op,
            reality=reality,
        )
    return {
        "state": state,
        "dominant_ntw_operator": dom_op,
        "reality": reality,
        "rollup": rollup,
        "sample_envelope": sample_env,
    }
