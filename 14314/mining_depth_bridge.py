"""
Mining Depth bridge — Port 8506 live_node_audit stream → gauge + national_apathy_extraction_total.

Binds gauge percentage to `national_apathy_extraction_total` when explicit gauge fields are absent:
  gauge_pct = 100 * total / MINING_DEPTH_DENOMINATOR (default 202225 ballot-box baseline).
Override denominator with env MINING_DEPTH_DENOMINATOR.
"""
from __future__ import annotations

import json
import os
from typing import Any, Callable, Dict, Optional, Tuple

_ROOT = os.path.dirname(os.path.abspath(__file__))


def _read_jsonl_last_match(path: str, predicate: Callable[[Dict[str, Any]], bool], max_lines: int = 2500) -> Optional[Dict[str, Any]]:
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            lines = [ln.strip() for ln in fh.readlines() if ln.strip()]
    except OSError:
        return None
    for line in reversed(lines[-max_lines:]):
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(o, dict) and predicate(o):
            return o
    return None


def _live_node_audit_candidates() -> list[str]:
    return [
        os.getenv("LIVE_NODE_AUDIT_STREAM", "").strip(),
        os.path.join(_ROOT, "live_node_audit.jsonl"),
        os.path.join(_ROOT, ".live_node_audit.jsonl"),
    ]


def _national_apathy_candidates() -> list[str]:
    return [
        os.getenv("NATIONAL_APATHY_EXTRACTION_STREAM", "").strip(),
        os.path.join(_ROOT, "national_apathy_extraction.jsonl"),
        os.path.join(_ROOT, ".national_apathy_extraction.jsonl"),
    ]


def _matches_live_node_audit(o: Dict[str, Any]) -> bool:
    ev = str(o.get("event", "")).lower()
    if ev == "live_node_audit":
        return True
    if o.get("national_apathy_extraction_total") is not None:
        return True
    if o.get("gauge_pct") is not None or o.get("mining_depth_pct") is not None:
        return True
    return False


def _matches_national_apathy(o: Dict[str, Any]) -> bool:
    ev = str(o.get("event", "")).lower()
    if ev in {"national_apathy_extraction", "apathy_extraction", "national_apathy_extraction_pulse"}:
        return True
    if o.get("national_apathy_extraction_total") is not None:
        return True
    if o.get("gauge_pct") is not None or o.get("mining_depth_pct") is not None:
        return True
    return False


def _first_resolved_path(candidates: list[str]) -> str:
    return next((p for p in candidates if p and os.path.isfile(p)), "")


def compute_gauge_pct(obj: Optional[Dict[str, Any]]) -> Tuple[float, Optional[float]]:
    """Return (gauge 0–100, national_apathy_extraction_total or None)."""
    if not obj:
        return 0.0, None
    total_raw = obj.get("national_apathy_extraction_total")
    total_f: Optional[float]
    try:
        total_f = float(total_raw) if total_raw is not None else None
    except (TypeError, ValueError):
        total_f = None

    if obj.get("gauge_pct") is not None:
        g = float(obj["gauge_pct"])
    elif obj.get("mining_depth_pct") is not None:
        g = float(obj["mining_depth_pct"])
    elif obj.get("value") is not None and total_f is None:
        g = float(obj["value"])
    elif total_f is not None:
        denom = float(os.getenv("MINING_DEPTH_DENOMINATOR", "202225"))
        g = max(0.0, min(100.0, 100.0 * float(total_f) / max(denom, 1.0)))
    else:
        g = 0.0
    return max(0.0, min(100.0, float(g))), total_f


def load_mining_depth_snapshot() -> Dict[str, Any]:
    """
    Prefer live_node_audit JSONL (8506 pipeline). On stream_path_error, fall back to
    national apathy extraction file; bind gauge to national_apathy_extraction_total.
    """
    err_primary: Optional[str] = None
    audit_path = _first_resolved_path(_live_node_audit_candidates())
    obj: Optional[Dict[str, Any]] = None
    source = "none"

    if audit_path:
        obj = _read_jsonl_last_match(audit_path, _matches_live_node_audit)
        if obj is None:
            obj = _read_jsonl_last_match(audit_path, lambda o: True)
        if obj is None:
            err_primary = "stream_path_error: live_node_audit file empty or unreadable"
        else:
            source = "live_node_audit"
    else:
        err_primary = "stream_path_error: missing live_node_audit (set LIVE_NODE_AUDIT_STREAM or add live_node_audit.jsonl)"

    err_fb: Optional[str] = None
    if obj is None:
        fb_path = _first_resolved_path(_national_apathy_candidates())
        if fb_path:
            obj = _read_jsonl_last_match(fb_path, _matches_national_apathy)
            if obj is None:
                obj = _read_jsonl_last_match(fb_path, lambda o: True)
            if obj is not None:
                source = "national_apathy_extraction_fallback"
            else:
                err_fb = "stream_path_error: national apathy file empty or unreadable"
        else:
            err_fb = "stream_path_error: missing national apathy fallback file"

    gauge_pct, total = compute_gauge_pct(obj)
    path_out = audit_path or _first_resolved_path(_national_apathy_candidates()) or ""
    err_out = None if obj is not None else " · ".join([e for e in (err_primary, err_fb) if e])

    return {
        "gauge_pct": gauge_pct,
        "national_apathy_extraction_total": total,
        "source": source,
        "path": path_out,
        "object": obj,
        "error": err_out,
        "link_active": obj is not None,
    }
