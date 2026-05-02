"""
Sovereign Search · heuristic NL → map pivot (beta).
No external LLM — pattern match on POS density / zone hints for March 7th Lux latency on mobile.
"""

from __future__ import annotations

import re
from typing import Any


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def resolve_sovereign_nl_query(
    query: str,
    fin_points: list[dict],
    *,
    trade_points: list[dict] | None = None,
) -> dict[str, Any] | None:
    """
    Returns pivot dict: lat, lon, zoom, headline, detail — or None if unresolved.

    Supported intents (examples):
      - "Where is the highest POS density in Binji?"
      - "most POS agents Danchadi"
      - "show strongest informal cluster Jega"
    """
    q = _norm(query)
    if len(q) < 4:
        return None

    trade_points = trade_points or []

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
        return {
            "lat": lat,
            "lon": lon,
            "zoom": 14,
            "headline": headline,
            "detail": detail,
            "intent": "top_pos_density",
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
