"""
Generative Eagle — 24/7 telemetry sniff (CBN / NCC / vandalism / vigil / trade velocity).

Runs in-process with Streamlit when the mirror is live (`scripts/run_streamlit_vigil.sh`).
No outbound network — operates on registries already mounted by the app.

Sovereign Eagle Mirror 2026 — GCSLC © 2026
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def _parse_ts(v: Any) -> float:
    if not v:
        return 0.0
    s = str(v).strip()
    if not s:
        return 0.0
    try:
        if s.endswith("Z"):
            s = s.replace("Z", "+00:00")
        return datetime.fromisoformat(s).timestamp()
    except ValueError:
        return 0.0


def _trade_velocity(row: dict) -> float:
    try:
        pc = float(row.get("pos_count") or 0)
    except (TypeError, ValueError):
        pc = 0.0
    try:
        pop = float(row.get("population_estimate") or 0)
    except (TypeError, ValueError):
        pop = 0.0
    tier = str(row.get("anchor_tier") or "").lower()
    bump = 18.0 if tier == "primary" else 8.0 if tier == "secondary" else 0.0
    return pc * 2.2 + pop / 950.0 + bump


def collect_eagle_shouts(
    *,
    vigil_rows: list[dict[str, Any]],
    ncc_rows: list[dict],
    cbn_rows: list[dict],
    trade_rows: list[dict],
    signal_rows: list[dict],
    fin_rows: list[dict],
    limit: int = 16,
) -> list[dict[str, Any]]:
    """
    Build merged 'Eagle Shouts' for ticker + alert styling.
    pulse ∈ friction | opportunity | liquidity
    """
    rows: list[dict[str, Any]] = []

    for v in vigil_rows:
        if not isinstance(v, dict):
            continue
        kind = str(v.get("kind") or "signal")
        sev = float(v.get("severity") or 0.55)
        rows.append(
            {
                "ts_iso": str(v.get("ts_iso") or "")[:32],
                "ts_sort": _parse_ts(v.get("ts_iso")),
                "pulse": "friction",
                "headline": f"Vigil · {kind.replace('_', ' ')}",
                "detail": str(v.get("label") or "National pulse event"),
                "weight": sev + 0.35,
            }
        )

    for row in ncc_rows:
        if not isinstance(row, dict):
            continue
        try:
            sev = float(row.get("severity") or 0.5)
        except (TypeError, ValueError):
            sev = 0.5
        aid = str(row.get("id") or "")
        rows.append(
            {
                "ts_iso": datetime.now(timezone.utc).isoformat(),
                "ts_sort": _parse_ts(aid) + sev * 1e-6,
                "pulse": "friction",
                "headline": "NCC · infrastructure vandalism pressure",
                "detail": str(row.get("asset") or "ICT perimeter")[:120],
                "weight": sev + 0.22,
            }
        )

    for row in signal_rows:
        if not isinstance(row, dict):
            continue
        try:
            sev = float(row.get("severity") or 0.45)
        except (TypeError, ValueError):
            sev = 0.45
        rows.append(
            {
                "ts_iso": datetime.now(timezone.utc).isoformat(),
                "ts_sort": 1e6 + sev,
                "pulse": "friction",
                "headline": "Telecom void · signal dropout footprint",
                "detail": str(row.get("site") or row.get("label") or "Backhaul / relay")[:120],
                "weight": sev * 0.95 + 0.15,
            }
        )

    ranked_trade = sorted(
        [t for t in trade_rows if isinstance(t, dict)],
        key=_trade_velocity,
        reverse=True,
    )[:6]
    for t in ranked_trade:
        vel = _trade_velocity(t)
        rows.append(
            {
                "ts_iso": datetime.now(timezone.utc).isoformat(),
                "ts_sort": 3e6 + vel,
                "pulse": "opportunity",
                "headline": "Trade velocity · sovereign node pulse",
                "detail": f"{str(t.get('label', ''))[:80]} · POS weight {_trade_velocity_hint(t)}",
                "weight": min(5.0, vel / 28.0),
            }
        )

    liq = sorted(
        [f for f in fin_rows if isinstance(f, dict)],
        key=lambda p: float(p.get("agents") or 0),
        reverse=True,
    )[:4]
    for f in liq:
        try:
            ag = float(f.get("agents") or 0)
        except (TypeError, ValueError):
            ag = 0.0
        gap = str(f.get("inclusion_gap") or "")
        rows.append(
            {
                "ts_iso": datetime.now(timezone.utc).isoformat(),
                "ts_sort": 4e6 + ag,
                "pulse": "liquidity",
                "headline": "Financial inclusion · POS relay staging",
                "detail": f"{str(f.get('name', ''))[:72]} · gap {gap} · agents ~{ag:.0f}",
                "weight": min(4.5, ag / 55.0),
            }
        )

    if cbn_rows:
        rows.append(
            {
                "ts_iso": datetime.now(timezone.utc).isoformat(),
                "ts_sort": 5e6,
                "pulse": "liquidity",
                "headline": "CBN footprint · formal access anchors",
                "detail": f"{len(cbn_rows)} registry points mounted — tier-2 bulk lane.",
                "weight": 1.2,
            }
        )

    rows.sort(key=lambda r: (-float(r.get("weight") or 0), -float(r.get("ts_sort") or 0)))
    return rows[: max(4, min(limit, 40))]


def _trade_velocity_hint(t: dict) -> str:
    try:
        pc = float(t.get("pos_count") or 0)
    except (TypeError, ValueError):
        pc = 0.0
    return f"~{pc:.0f}"


def ticker_signature(shouts: list[dict[str, Any]]) -> str:
    if not shouts:
        return ""
    top = shouts[0]
    return "|".join(
        [
            str(top.get("pulse")),
            str(top.get("headline"))[:48],
            str(top.get("detail"))[:48],
        ]
    )


def friction_alert_active(shouts: list[dict[str, Any]]) -> bool:
    """Visual / compact alert strip — high friction when top shout is friction & weight high."""
    if not shouts:
        return False
    top = shouts[0]
    return str(top.get("pulse")) == "friction" and float(top.get("weight") or 0) >= 0.72
