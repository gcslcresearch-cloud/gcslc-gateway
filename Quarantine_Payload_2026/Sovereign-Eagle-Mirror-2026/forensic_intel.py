"""
Forensic intelligence synthesis — Double-Zero void weights, AZK snap, Komi HTML.
Sovereign Eagle Mirror 2026 — GCSLC © 2026
"""

from __future__ import annotations

import html as html_lib
import math
from typing import Any

# Deep Shadow Grey heat ramp (folium HeatMap gradient stops 0–1)
DOUBLE_ZERO_GREY_GRADIENT = {
    0.0: "#0a0a12",
    0.35: "#2a2a38",
    0.65: "#5c5c6e",
    1.0: "#9a9cae",
}

# Lagos Mainland saturated-fabric staging reference (persons per POS agent) — contrast for village Service Gravity
LAGOS_MAINLAND_POP_PER_POS_REF = 380.0


def nearest_azk_node(
    lat: float,
    lon: float,
    azk_nodes: list[dict[str, Any]],
) -> tuple[dict[str, Any], float]:
    """Return nearest AZK corridor anchor and distance (degrees² proxy)."""
    best = azk_nodes[0]
    best_d = 1e9
    for n in azk_nodes:
        dy = float(n["lat"]) - lat
        dx = float(n["lon"]) - lon
        d = dy * dy + dx * dx
        if d < best_d:
            best_d = d
            best = n
    return best, math.sqrt(best_d)


def build_double_zero_triples(
    vandal_rows: list[dict],
    signal_rows: list[dict],
    fin_rows: list[dict],
) -> list[list[float]]:
    """
    Fuse NCC vandalism + telecom blackouts + severe financial friction into [lat, lon, weight].
    Weights are RELATIVE intensities for grey heatmap (not population counts).
    """
    cells: dict[tuple[float, float], float] = {}

    def bump(lat: float, lon: float, w: float) -> None:
        key = (round(lat, 4), round(lon, 4))
        cells[key] = cells.get(key, 0.0) + w

    for row in vandal_rows:
        try:
            sev = float(row.get("severity", 0.5))
            bump(float(row["lat"]), float(row["lon"]), 35.0 * sev + 15.0)
        except (KeyError, TypeError, ValueError):
            continue

    for row in signal_rows:
        try:
            sev = float(row.get("severity", 0.5))
            dm = float(row.get("downtime_minutes", 60))
            bump(float(row["lat"]), float(row["lon"]), 28.0 * sev + min(dm / 12.0, 40.0))
        except (KeyError, TypeError, ValueError):
            continue

    for row in fin_rows:
        try:
            gap = str(row.get("inclusion_gap", "")).strip().lower()
            mult = 1.2 if gap == "severe" else 0.75 if gap == "moderate" else 0.35
            ag = float(row.get("agents") or 10)
            bump(float(row["lat"]), float(row["lon"]), 12.0 * mult + min(ag / 3.0, 25.0))
        except (KeyError, TypeError, ValueError):
            continue

    out: list[list[float]] = []
    for (la, lo), w in cells.items():
        out.append([la, lo, max(8.0, min(w, 220.0))])
    return out


def wahala_index(row: dict) -> float:
    """0–100 composite from available forensic fields."""
    parts: list[float] = []
    if row.get("severity") is not None:
        try:
            parts.append(float(row["severity"]) * 100)
        except (TypeError, ValueError):
            pass
    if row.get("inclusion_gap"):
        g = str(row["inclusion_gap"]).lower()
        parts.append(88 if g == "severe" else 55 if g == "moderate" else 28)
    if row.get("agents") is not None:
        try:
            parts.append(min(100, float(row["agents"])))
        except (TypeError, ValueError):
            pass
    if not parts:
        return 42.0
    return max(5.0, min(99.0, sum(parts) / len(parts)))


def infrastructure_health_score(row: dict) -> str:
    """Plain-language tier from gaps / severity."""
    if row.get("inclusion_gap"):
        g = str(row["inclusion_gap"]).lower()
        if g == "severe":
            return "Strained — formal finance thin vs commerce"
        if g == "moderate":
            return "Mixed — relay-dependent"
        return "Stable — narrower inclusion gap"
    if row.get("severity") is not None:
        try:
            s = float(row["severity"])
            if s > 0.75:
                return "Critical — ICT perimeter stress"
            if s > 0.45:
                return "Elevated — maintenance backlog risk"
        except (TypeError, ValueError):
            pass
    return "Watch — routine vigil"


def economic_potential_line(row: dict) -> str | None:
    """
    Resonance score from informal capillaries (kose stands, shayi proxy) + POS weight.
    Surfaces in Komi for CBN-facing staging when kose_count or shayi_proxy exist.
    """
    kose = row.get("kose_count")
    shayi = row.get("shayi_proxy")
    if kose is None and shayi is None:
        return None
    try:
        k = float(kose) if kose is not None else 0.0
    except (TypeError, ValueError):
        k = 0.0
    try:
        s = float(shayi) if shayi is not None else 0.0
    except (TypeError, ValueError):
        s = 0.0
    if s > 1.0:
        s = min(1.0, s / 100.0)
    s = max(0.0, min(1.0, s))
    pos_raw = row.get("pos_count") or row.get("agents")
    try:
        p = float(pos_raw) if pos_raw is not None else 0.0
    except (TypeError, ValueError):
        p = 0.0
    score = min(100.0, max(0.0, 1.35 * k + 42.0 * s + 0.11 * p))
    tag = (
        "High informal liquidity resonance — priority CBN sightline."
        if score >= 58
        else "Emerging capillary field — monitor informal settlement velocity."
    )
    return (
        f"Resonance index {score:.1f} / 100 · kose {k:.0f} · shayi {s:.2f} · "
        f"POS weight {p:.0f} — {tag}"
    )


def sector_density_blurb(row: dict) -> str:
    if row.get("kose_count") is not None:
        try:
            kose = f"~{int(float(row['kose_count']))}"
        except (TypeError, ValueError):
            kose = str(row.get("kose_density") or "—")
    else:
        kose = row.get("kose_density") or "—"
    pos_raw = row.get("pos_count") or row.get("agents") or row.get("pos_density")
    if pos_raw is None:
        pos_s = "—"
    elif isinstance(pos_raw, str):
        pos_s = pos_raw
    else:
        try:
            pos_s = f"~{float(pos_raw):.0f}"
        except (TypeError, ValueError):
            pos_s = "—"
    okada = row.get("okada_intensity") or "—"
    shayi_s = "—"
    if row.get("shayi_proxy") is not None:
        try:
            sv = float(row["shayi_proxy"])
            shayi_s = f"{sv:.2f}" if sv <= 1.0 else f"{min(1.0, sv / 100.0):.2f}"
        except (TypeError, ValueError):
            shayi_s = "—"
    return f"Kose {kose} · POS agents {pos_s} · Okada {okada} · Shayi {shayi_s}"


def _estimated_pop_per_pos(row: dict) -> tuple[float | None, float | None]:
    """Return (pop/POS, population_estimate) if derivable."""
    pop = row.get("population_estimate")
    pos = row.get("pos_count")
    if pos is None:
        try:
            pos = row.get("agents")
        except (TypeError, ValueError):
            pos = None
    if pop is None or pos is None:
        return None, None
    try:
        p = float(pop)
        n = max(float(pos), 1.0)
        return p / n, p
    except (TypeError, ValueError):
        return None, None


def service_gravity_line(row: dict, lagos_ref: float = LAGOS_MAINLAND_POP_PER_POS_REF) -> str | None:
    """Service gravity = population pressure per POS vs Lagos mainland staging reference."""
    ratio, pop = _estimated_pop_per_pos(row)
    if ratio is None:
        return None
    delta_pct = (ratio - lagos_ref) / max(lagos_ref, 1.0) * 100.0
    if ratio >= lagos_ref * 1.08:
        verdict = "Higher gravity vs Lagos ref — fewer POS per estimated capita (informal strain field)."
    elif ratio <= lagos_ref * 0.92:
        verdict = "Lower gravity vs Lagos ref — denser POS footprint per estimated capita."
    else:
        verdict = "Near Lagos mainland reference band — comparable service density staging."
    pop_s = f"{int(pop):,}" if pop is not None else "—"
    return (
        f"Est. pop/POS: {ratio:.1f} · pop ~{pop_s} · "
        f"Lagos mainland ref: {lagos_ref:.0f} · Δ {delta_pct:+.1f}% vs ref — {verdict}"
    )


def komi_popup_html(
    title: str,
    row: dict,
    *,
    lagos_pop_per_pos_ref: float = LAGOS_MAINLAND_POP_PER_POS_REF,
) -> str:
    """Typewriter-cyan forensic summary card (escaped)."""
    sec = sector_density_blurb(row)
    infra = infrastructure_health_score(row)
    w = wahala_index(row)
    vn = str(row.get("village", "")).strip()
    vn_div = ""
    if vn:
        vn_div = (
            f"<div><span class='gcslc-komi-k'>Village</span> "
            f"{html_lib.escape(vn[:120])}</div>"
        )
    sg = service_gravity_line(row, lagos_ref=lagos_pop_per_pos_ref)
    sg_div = ""
    if sg:
        sg_div = (
            f"<div><span class='gcslc-komi-k'>Service gravity</span> "
            f"{html_lib.escape(sg[:280])}</div>"
        )
    ep = economic_potential_line(row)
    ep_div = ""
    if ep:
        ep_div = (
            f"<div><span class='gcslc-komi-k'>Economic potential</span> "
            f"{html_lib.escape(ep[:320])}</div>"
        )
    lines: list[str] = [
        "<div class='gcslc-komi-card'>",
        "<div class='gcslc-komi-h'>Total Reality Summary</div>",
        f"<div><span class='gcslc-komi-k'>Node</span> {html_lib.escape(title[:120])}</div>",
    ]
    if vn_div:
        lines.append(vn_div)
    lines.append(
        f"<div><span class='gcslc-komi-k'>Sector density</span> {html_lib.escape(sec[:160])}</div>"
    )
    if sg_div:
        lines.append(sg_div)
    if ep_div:
        lines.append(ep_div)
    lines.extend(
        [
            f"<div><span class='gcslc-komi-k'>Infrastructure health</span> {html_lib.escape(infra[:160])}</div>",
            f"<div><span class='gcslc-komi-k'>Wahala Index</span> {w:.1f} / 100</div>",
            "</div>",
        ]
    )
    return "".join(lines)
