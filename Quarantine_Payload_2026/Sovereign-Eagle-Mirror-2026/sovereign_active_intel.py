"""
Active Intelligence — state hit-testing on federation GeoJSON and Total Reality summaries.
Sovereign Eagle Mirror 2026 — GCSLC © 2026
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from gcslc_deep_join import NATIONAL_WARD_TOTAL, STATE_CODE_TO_STATE

NATIONAL_PU_TOTAL = 176_846


def _ring_contains(lon: float, lat: float, ring: list) -> bool:
    """Ray casting; ring is list of [lon, lat]."""
    if len(ring) < 3:
        return False
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        xi, yi = float(ring[i][0]), float(ring[i][1])
        xj, yj = float(ring[j][0]), float(ring[j][1])
        intersect = ((yi > lat) != (yj > lat)) and (
            lon < (xj - xi) * (lat - yi) / (yj - yi + 1e-18) + xi
        )
        if intersect:
            inside = not inside
        j = i
    return inside


def _coords_polygon_contains(lon: float, lat: float, coords: list) -> bool:
    """GeoJSON Polygon coordinates: [ exterior, holes... ]."""
    if not coords:
        return False
    exterior = coords[0]
    return _ring_contains(lon, lat, exterior)


def _geometry_contains(lon: float, lat: float, geom: dict[str, Any]) -> bool:
    gtype = str(geom.get("type") or "")
    coords = geom.get("coordinates")
    if gtype == "Polygon" and isinstance(coords, list):
        return _coords_polygon_contains(lon, lat, coords)
    if gtype == "MultiPolygon" and isinstance(coords, list):
        for poly in coords:
            if isinstance(poly, list) and poly and _coords_polygon_contains(lon, lat, poly):
                return True
    return False


def state_label_from_props(props: dict[str, Any]) -> str:
    for key in ("shapeName", "ADM1_EN", "NAME_1", "STATE_NAME", "name"):
        v = props.get(key)
        if v is not None and str(v).strip():
            return str(v).strip()
    return "Unknown"


def canonical_state_name(raw: str, catalog_states: list[str]) -> str:
    r = raw.strip().lower().replace("state", "").strip()
    aliases = {
        "federal capital territory": "FCT",
        "fct abuja": "FCT",
        "abuja": "FCT",
    }
    if r in aliases:
        r = aliases[r].lower()
    for c in catalog_states:
        cl = c.lower()
        if cl == r or r == cl.replace(" ", ""):
            return c
    for c in catalog_states:
        cl = c.lower()
        if r in cl or cl in r:
            return c
    return raw.strip()


def resolve_state_from_click(
    lat: float,
    lon: float,
    states_geojson: dict[str, Any] | None,
    fused_df: pd.DataFrame | None,
) -> tuple[str, dict[str, Any]] | None:
    """Return (canonical_state_name, feature_props) or None."""
    if not states_geojson or not states_geojson.get("features"):
        return None
    catalog_states: list[str] = []
    if fused_df is not None and "state" in fused_df.columns:
        catalog_states = sorted(fused_df["state"].astype(str).unique().tolist())
    if not catalog_states:
        catalog_states = list(STATE_CODE_TO_STATE.values())

    for feat in states_geojson["features"]:
        if not isinstance(feat, dict):
            continue
        geom = feat.get("geometry")
        if not isinstance(geom, dict):
            continue
        if not _geometry_contains(lon, lat, geom):
            continue
        props = feat.get("properties") or {}
        if not isinstance(props, dict):
            props = {}
        raw = state_label_from_props(props)
        canon = canonical_state_name(raw, catalog_states)
        return (canon, props)
    return None


def _pu_mask_for_state(state: str, df: pd.DataFrame) -> pd.Series:
    sn = state.strip().lower()
    col = df["state"].astype(str).str.strip().str.lower()
    mask = col == sn
    if sn == "fct":
        mask = mask | col.isin(["federal capital territory", "abuja", "fct abuja"])
    return mask


def forensic_admin_atomic(
    state: str,
    fused_df: pd.DataFrame | None,
    national_pu_df: pd.DataFrame | None,
) -> dict[str, Any]:
    """
    Ward mass from gcslc_deep_join (Σ = 8,806 nationally).
    PU count from canonical 176,846 lattice state column when loaded; else proportional fallback.
    """
    lgas, wards = admin_counts_for_state(state, fused_df)
    pu_n: int = 0
    note = ""
    pu_from_csv: int | None = None
    if national_pu_df is not None and not national_pu_df.empty and "state" in national_pu_df.columns:
        pu_from_csv = int(_pu_mask_for_state(state, national_pu_df).sum())
    if pu_from_csv is not None and pu_from_csv > 0:
        pu_n = pu_from_csv
        note = (
            f"Forensic PU attribution: {pu_n:,} rows matched to this state in the canonical "
            f"{NATIONAL_PU_TOTAL:,}-row INEC lattice (national atomic inventory)."
        )
    elif wards > 0:
        pu_n = int(round(wards / float(NATIONAL_WARD_TOTAL) * float(NATIONAL_PU_TOTAL)))
        note = (
            f"PU staging proportional to ward mass ({wards:,} / {NATIONAL_WARD_TOTAL:,} national wards) — "
            "mount full lattice online for row-accurate PU IDs per state."
        )
    else:
        note = "No ward mass for this label — expand fused catalog alignment."

    return {
        "lgas": lgas,
        "wards_forensic": wards,
        "national_ward_total": NATIONAL_WARD_TOTAL,
        "pu_forensic": pu_n,
        "national_pu_total": NATIONAL_PU_TOTAL,
        "atomic_attribution_note": note,
    }


def admin_counts_for_state(state: str, fused_df: pd.DataFrame | None) -> tuple[int, int]:
    if fused_df is None or fused_df.empty or "state" not in fused_df.columns:
        return 0, 0
    sub = fused_df[fused_df["state"].astype(str).str.strip().str.lower() == state.lower()]
    if sub.empty:
        return 0, 0
    lgas = len(sub)
    wards = int(sub["ward_count"].sum()) if "ward_count" in sub.columns else 0
    return lgas, wards


def _gap_weight(gap: str | None) -> float:
    g = (gap or "").strip().lower()
    if g == "severe":
        return 28.0
    if g == "moderate":
        return 52.0
    if g == "narrow":
        return 82.0
    return 48.0


def financial_inclusion_score_state(state: str, fin_points: list[dict]) -> tuple[float, str]:
    """0–100 composite from POS inclusion_gap + agents (registry telemetry)."""
    rows = [
        p
        for p in fin_points
        if isinstance(p, dict) and str(p.get("state", "")).strip().lower() == state.lower()
    ]
    if not rows:
        return 52.0, "Sparse POS telemetry — national void staging (20.7M scale narrative)."
    parts: list[float] = []
    for p in rows:
        base = _gap_weight(str(p.get("inclusion_gap")))
        try:
            ag = float(p.get("agents") or 0)
        except (TypeError, ValueError):
            ag = 0.0
        boost = min(18.0, (ag / 95.0) * 18.0)
        parts.append(min(96.0, base + boost))
    avg = sum(parts) / max(len(parts), 1)
    verdict = (
        "Formal fabric thin vs commerce — escalate CBN relay sightlines."
        if avg < 45
        else "Mixed relay economy — monitor POS velocity vs population pressure."
        if avg < 72
        else "Narrower inclusion gap vs severe void peers — sustain staging."
    )
    return round(min(100.0, max(12.0, avg)), 1), verdict


def friction_audit_state(
    state: str,
    ncc_rows: list[dict],
    signal_rows: list[dict],
    states_geojson: dict[str, Any] | None,
) -> dict[str, Any]:
    """Incident counts / severity proxy inside state polygon."""
    st_lo = state.strip().lower()
    n_hit = 0
    sev_sum = 0.0
    for row in ncc_rows:
        if not isinstance(row, dict):
            continue
        try:
            la, lo = float(row["lat"]), float(row["lon"])
        except (KeyError, TypeError, ValueError):
            continue
        hit = resolve_state_from_click(la, lo, states_geojson, None)
        if hit and hit[0].strip().lower() == st_lo:
            n_hit += 1
            try:
                sev_sum += float(row.get("severity") or 0.5)
            except (TypeError, ValueError):
                sev_sum += 0.5
    s_hit = 0
    for row in signal_rows:
        if not isinstance(row, dict):
            continue
        try:
            la, lo = float(row["lat"]), float(row["lon"])
        except (KeyError, TypeError, ValueError):
            continue
        hit = resolve_state_from_click(la, lo, states_geojson, None)
        if hit and hit[0].strip().lower() == st_lo:
            s_hit += 1
    sev_avg = (sev_sum / n_hit) if n_hit else 0.0
    friction_label = (
        "Elevated ICT perimeter friction — Double-Zero vigil priority."
        if n_hit >= 2 or sev_avg > 0.75
        else "Measured perimeter stress — routine vigil."
        if n_hit or s_hit
        else "No indexed NCC / telecom void nodes in-canvas for this state boundary."
    )
    return {
        "ncc_incidents_in_state": n_hit,
        "signal_void_events_in_state": s_hit,
        "ncc_severity_avg": round(sev_avg, 3),
        "friction_summary": friction_label,
    }


def load_ntw_operator_proxy(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {
            "default": {"MTN": 0.36, "Airtel": 0.28, "Glo": 0.24, "9mobile": 0.12},
            "by_state": {},
        }
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {
            "default": {"MTN": 0.36, "Airtel": 0.28, "Glo": 0.24, "9mobile": 0.12},
            "by_state": {},
        }


def dominant_ntw_operator(state: str, proxy_blob: dict[str, Any]) -> tuple[str, dict[str, float]]:
    by_state = proxy_blob.get("by_state") or {}
    default = proxy_blob.get("default") or {
        "MTN": 0.36,
        "Airtel": 0.28,
        "Glo": 0.24,
        "9mobile": 0.12,
    }
    dist: dict[str, float]
    if isinstance(by_state, dict) and state in by_state and isinstance(by_state[state], dict):
        dist = {k: float(v) for k, v in by_state[state].items()}
    elif isinstance(by_state, dict):
        # fuzzy key
        sl = state.lower()
        found = None
        for k, v in by_state.items():
            if str(k).lower() == sl:
                found = v
                break
        dist = {k: float(v) for k, v in found.items()} if isinstance(found, dict) else dict(default)
    else:
        dist = dict(default)
    if not dist:
        dist = dict(default)
    top = max(dist.items(), key=lambda x: x[1])
    return top[0], dist


def build_total_reality_summary(
    state: str,
    *,
    fused_df: pd.DataFrame | None,
    national_pu_df: pd.DataFrame | None = None,
    ncc_rows: list[dict],
    signal_rows: list[dict],
    fin_points: list[dict],
    states_geojson: dict[str, Any] | None,
    ntw_proxy: dict[str, Any],
) -> dict[str, Any]:
    atomic = forensic_admin_atomic(state, fused_df, national_pu_df)
    fin_score, fin_verdict = financial_inclusion_score_state(state, fin_points)
    friction = friction_audit_state(state, ncc_rows, signal_rows, states_geojson)
    dom_op, dist = dominant_ntw_operator(state, ntw_proxy)
    return {
        "state": state,
        "financial_inclusion_score": fin_score,
        "financial_inclusion_verdict": fin_verdict,
        "friction": friction,
        "ntw_dominant_operator": dom_op,
        "ntw_distribution": dist,
        **atomic,
    }
