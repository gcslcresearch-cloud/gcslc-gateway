"""
Sovereign Search · heuristic NL → map pivot (beta).
No external LLM — pattern match on POS density / zone hints for March 7th Lux latency on mobile.
"""

from __future__ import annotations

import re
from typing import Any

try:
    import pandas as pd
except ImportError:
    pd = None  # type: ignore[misc, assignment]


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def _ngecc_nl_tokens_hit(q: str, reg: dict[str, Any]) -> bool:
    """Explicit NGECC / NGEEC / Green Energy & Chemicals intents — avoids stealing generic zones."""
    if not q or not reg:
        return False
    needles = (
        "ngecc",
        "ngeec",
        "green energy",
        "chemicals corporation",
        "chemical corporation",
        "strategic industrial",
        "industrial pu",
        "million steel",
        "ngecc intake",
        "sovereign gold industrial",
        "nigerian green energy",
    )
    if any(n in q for n in needles):
        return True
    for a in reg.get("search_aliases") or []:
        als = _norm(str(a))
        if len(als) >= 4 and (als in q or (len(q) >= 4 and q in als)):
            return True
    meta = reg.get("meta") or {}
    prog = _norm(str(meta.get("program_extended") or "") + " " + str(meta.get("program") or ""))
    return len(q) >= 8 and q in prog


def _ngecc_pivot_from_registry(
    q: str,
    reg: dict[str, Any],
    national_pu_df: Any,
) -> dict[str, Any] | None:
    """Pivot to NGECC / NGEEC industrial PU cluster via canonical national lattice."""
    if not reg or not _ngecc_nl_tokens_hit(q, reg):
        return None
    nodes_all = [n for n in (reg.get("nodes") or []) if isinstance(n, dict) and n.get("code")]
    if not nodes_all:
        return None
    qn = _norm(q)
    narrowed = [
        n
        for n in nodes_all
        if len(qn) >= 3 and qn in _norm(str(n.get("label", "")))
    ]
    use_nodes = narrowed if narrowed else nodes_all
    codes = {str(n.get("code", "")).strip() for n in use_nodes if n.get("code")}
    rows_latlon: list[dict[str, Any]] = []
    if pd is not None and national_pu_df is not None:
        try:
            sub = national_pu_df[national_pu_df["code"].isin(list(codes))]
            for _, r in sub.iterrows():
                rows_latlon.append({"lat": float(r["lat"]), "lon": float(r["lon"])})
        except Exception:
            rows_latlon = []
    labels = reg.get("labels") or {}
    if not rows_latlon:
        azk = [
            {"lat": 9.0765, "lon": 7.3986},
            {"lat": 8.8467, "lon": 7.8736},
            {"lat": 10.5105, "lon": 7.4165},
            {"lat": 11.0676, "lon": 7.7107},
            {"lat": 12.0022, "lon": 8.5920},
        ]
        clat = sum(p["lat"] for p in azk) / len(azk)
        clon = sum(p["lon"] for p in azk) / len(azk)
        return {
            "lat": clat,
            "lon": clon,
            "zoom": 7,
            "headline": "NGECC / NGEEC · lattice pivot (offline PU frame)",
            "detail": "AZK corridor anchoring — reload national lattice for exact PU nodes.",
            "intent": "ngecc_registry_azk_fallback",
        }
    clat = sum(p["lat"] for p in rows_latlon) / len(rows_latlon)
    clon = sum(p["lon"] for p in rows_latlon) / len(rows_latlon)
    lats = [p["lat"] for p in rows_latlon]
    lons = [p["lon"] for p in rows_latlon]
    span = max(max(lats) - min(lats), max(lons) - min(lons), 0.018)
    if span < 0.045:
        zm = 12.0
    elif span < 0.09:
        zm = 11.0
    elif span < 0.18:
        zm = 10.0
    elif span < 0.38:
        zm = 9.0
    else:
        zm = 8.2
    sample_code = next(iter(codes)) if codes else ""
    lbl = str(labels.get(sample_code, "NGECC industrial node"))[:120]
    return {
        "lat": clat,
        "lon": clon,
        "zoom": zm,
        "headline": "Nigerian Green Energy & Chemicals (NGECC / NGEEC) · industrial PU cluster",
        "detail": f"{len(rows_latlon)} lattice nodes · {lbl}",
        "intent": "ngecc_registry_pivot",
    }


def ngecc_discovery_hit(query: str, reg: dict[str, Any] | None) -> bool:
    """True when lattice / NL text should bind to the NGECC strategic registry (explicit tokens only)."""
    return _ngecc_nl_tokens_hit(_norm(query), reg or {})


def resolve_sovereign_nl_query(
    query: str,
    fin_points: list[dict],
    *,
    trade_points: list[dict] | None = None,
    ngecc_reg: dict[str, Any] | None = None,
    national_pu_df: Any = None,
) -> dict[str, Any] | None:
    """
    Returns pivot dict: lat, lon, zoom, headline, detail — or None if unresolved.

    Supported intents (examples):
      - "Where is the highest POS density in Binji?"
      - "most POS agents Danchadi"
      - "show strongest informal cluster Jega"
      - "NGEEC green energy industrial pivot"
    """
    q = _norm(query)
    if len(q) < 4:
        return None

    trade_points = trade_points or []

    _ng = _ngecc_pivot_from_registry(q, ngecc_reg or {}, national_pu_df)
    if _ng is not None:
        return _ng

    wants_top_pos = bool(
        (("pos" in q or "agents" in q or "terminal" in q or "paypoint" in q)
         and (
             "highest" in q
             or "most" in q
             or "max" in q
             or "dense" in q
             or "density" in q
             or "strongest" in q
             or "busiest" in q
         ))
        or (q.startswith("where") and "pos" in q)
    )

    zone_tokens = (
        "binji",
        "danchadi",
        "jega",
        "yenagoa",
        "bayelsa",
        "lagos",
        "sokoto",
        "kebbi",
        "zaria",
        "kaduna",
        "kano",
        "southern ijaw",
        "brass",
        "ekeremor",
    )
    zone_hint: str | None = None
    for z in zone_tokens:
        if z in q:
            zone_hint = z
            break

    def zone_match(row: dict) -> bool:
        if zone_hint is None:
            return True
        blob = (
            str(row.get("zone", ""))
            + " "
            + str(row.get("state", ""))
            + " "
            + str(row.get("name", ""))
        ).lower()
        return zone_hint in blob

    if wants_top_pos and fin_points:
        pool = [p for p in fin_points if isinstance(p, dict) and zone_match(p)]
        if not pool:
            pool = list(fin_points)
        ranked = sorted(
            pool,
            key=lambda p: float(p.get("agents") or 0),
            reverse=True,
        )
        top = ranked[0]
        try:
            lat, lon = float(top["lat"]), float(top["lon"])
        except (KeyError, TypeError, ValueError):
            return None
        agents = top.get("agents")
        zm = str(top.get("zone", ""))
        nm = str(top.get("name", "POS cluster"))
        headline = f"Highest POS proxy · {zm or 'national pool'}"
        detail = f"{nm} · agents ~{agents}" if agents is not None else nm
        zt = (zone_hint or str(top.get("zone") or "").strip()).lower()
        return {
            "lat": lat,
            "lon": lon,
            "zoom": 14,
            "headline": headline,
            "detail": detail,
            "intent": "top_pos_density",
            "zone_token": zt,
        }

    # Trade / village node — substring over label + village + aliases
    if trade_points and len(q) >= 5:
        best = None
        best_score = -1
        for row in trade_points:
            if not isinstance(row, dict):
                continue
            parts = [str(row.get("label", "")), str(row.get("village", ""))]
            als = row.get("search_aliases")
            if isinstance(als, list):
                parts.extend(str(a) for a in als)
            blob = _norm(" ".join(parts))
            if q in blob:
                score = len(q)
                if score > best_score:
                    best_score = score
                    best = row
        if best:
            try:
                lat, lon = float(best["lat"]), float(best["lon"])
            except (KeyError, TypeError, ValueError):
                return None
            return {
                "lat": lat,
                "lon": lon,
                "zoom": 15,
                "headline": "Village / trade node",
                "detail": str(best.get("label", ""))[:180],
                "intent": "trade_lookup",
            }

    return None
