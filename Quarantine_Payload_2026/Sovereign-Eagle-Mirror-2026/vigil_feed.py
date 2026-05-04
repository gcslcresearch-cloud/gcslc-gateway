"""
National Vigil — live sabotage / signal-drop feed (architecture).

Prepared wiring:
  1. Authoritative stream (NMS, OSS, field SOC) → webhook / queue (Kafka optional).
  2. Normalizer writes append-only JSON (`vigil_feed_events.json`) or JSONL for audit.
  3. Streamlit reads via `load_recent_events` (short TTL cache in app) or future SSE/WebSocket pane.

This module stays transport-agnostic — no network calls here.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1

VALID_KINDS = frozenset(
    {
        "signal_drop",
        "sabotage",
        "fiber_cut",
        "ransom_pressure",
        "site_intrusion",
        "coordination_pulse",
    }
)


def _parse_iso(ts: str | None) -> datetime | None:
    if not ts or not isinstance(ts, str):
        return None
    ts = ts.strip()
    if not ts:
        return None
    try:
        if ts.endswith("Z"):
            return datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return datetime.fromisoformat(ts)
    except ValueError:
        return None


def normalize_event(row: dict[str, Any]) -> dict[str, Any] | None:
    """Validate minimal fields for map/sidebar display."""
    if not isinstance(row, dict):
        return None
    kind = str(row.get("kind") or row.get("event_type") or "").strip().lower()
    if kind:
        kind = kind.replace(" ", "_")
    if kind not in VALID_KINDS:
        kind = "signal_drop"
    try:
        lat = float(row["lat"])
        lon = float(row["lon"])
    except (KeyError, TypeError, ValueError):
        return None
    label = str(row.get("label") or row.get("site") or "Vigil event")[:200]
    sev = row.get("severity")
    try:
        severity = float(sev) if sev is not None else 0.55
    except (TypeError, ValueError):
        severity = 0.55
    severity = max(0.0, min(1.0, severity))
    ts_raw = row.get("ts_iso") or row.get("timestamp") or row.get("ts")
    dt = _parse_iso(ts_raw) if isinstance(ts_raw, str) else None
    ts_iso = dt.isoformat() if dt else datetime.now(timezone.utc).isoformat()
    source = str(row.get("source") or "registry")[:80]
    zone = str(row.get("zone") or row.get("lga") or "")[:80]
    return {
        "kind": kind,
        "lat": lat,
        "lon": lon,
        "label": label,
        "severity": severity,
        "ts_iso": ts_iso,
        "source": source,
        "zone": zone,
        "schema_version": SCHEMA_VERSION,
    }


def load_recent_events(path: Path, *, limit: int = 50) -> list[dict[str, Any]]:
    """
    Load newest-first vigil rows from JSON `{ "events": [ ... ] }`.
    Missing file → empty list (mirror stays up).
    """
    if not path.is_file():
        return []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    rows = raw.get("events") if isinstance(raw, dict) else None
    if not isinstance(rows, list):
        return []
    normalized: list[dict[str, Any]] = []
    for row in rows:
        n = normalize_event(row) if isinstance(row, dict) else None
        if n:
            normalized.append(n)

    def sort_key(r: dict[str, Any]) -> float:
        dt = _parse_iso(str(r.get("ts_iso") or ""))
        return dt.timestamp() if dt else 0.0

    normalized.sort(key=sort_key, reverse=True)
    return normalized[: max(1, min(limit, 500))]


def merge_vigil_sources(
    registry: list[dict[str, Any]],
    blackout_rows: list[dict] | None,
    *,
    fuse_blackouts: bool,
    limit: int = 24,
) -> list[dict[str, Any]]:
    """Registry-first fusion for sidebar pulse strip."""
    out: list[dict[str, Any]] = list(registry)
    if fuse_blackouts and blackout_rows:
        out.extend(signal_blackout_rows_as_vigil(blackout_rows))
    out.sort(
        key=lambda r: (
            _parse_iso(str(r.get("ts_iso") or "")) or datetime(1970, 1, 1, tzinfo=timezone.utc)
        ).timestamp(),
        reverse=True,
    )
    return out[: max(1, min(limit, 200))]


def signal_blackout_rows_as_vigil(rows: list[dict]) -> list[dict[str, Any]]:
    """Optional fusion: map legacy telecom blackout rows into vigil-shaped dicts."""
    out: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        sev = row.get("severity", 0.5)
        try:
            sev_f = float(sev)
        except (TypeError, ValueError):
            sev_f = 0.5
        n = normalize_event(
            {
                "kind": "signal_drop",
                "lat": row.get("lat"),
                "lon": row.get("lon"),
                "label": str(row.get("label") or row.get("site") or "Signal void"),
                "severity": max(0.0, min(1.0, sev_f)),
                "ts_iso": row.get("ts_iso") or row.get("timestamp"),
                "source": "signal_blackouts_registry",
                "zone": str(row.get("zone") or ""),
            }
        )
        if n:
            out.append(n)
    return out
