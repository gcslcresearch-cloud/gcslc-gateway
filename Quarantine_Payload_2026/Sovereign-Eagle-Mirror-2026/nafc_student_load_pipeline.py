"""
NAFC Brain Box — student load inference (2025–2026 academic cycle onward).

Steel opinion (architecture, not legal advice):
- **Official truth first:** Prefer regulator-published **bulk** tables (NUC universities, NBTE polytechnics,
  NCCE colleges) via **scheduled download + checksum**, not brittle HTML scraping. Many portals forbid
  scraping in ToS; partner routes include **open data drops**, **licensed third-party aggregators**, and
  **direct MOU APIs** where available.
- **Stale PDF bridge:** OCR + table extraction is a **batch reconciliation lane** only — version every
  PDF by SHA-256, map rows to `lattice_key` (state_code:LGA), and stamp `source_freshness_days`.
- **Real-time student reality:** Treat **DAPI / institutional SIS webhooks** (where consented) as the
  fastest ground truth for *campus presence*; treat **market pulse + social sentiment** as a *bounded
  nowcast multiplier* (e.g. ±15%) on headcount when official rolls are older than N days — never as a
  replacement for statutory enrolment without disclosure in UI metadata.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
KADUNA_DEEP_WELD_JSON = BASE_DIR / "Part_04_Social" / "data" / "kaduna_pilot_student_deep_weld.json"

ACADEMIC_CYCLE_LABEL = "2025–2026"
ACADEMIC_CYCLE_ID = "2025_2026"


@dataclass(frozen=True)
class WardLatticeLatencyProfile:
    """
    D4 — ward-count scaling: denser ADM3 lattices cost more paint + join work at the same zoom.
    Strategy: server-side pre-aggregation by ADM2 + optional ADM3 bucketing, viewport simplification
    (Topojson / zoom-dependent generalisation), and **heat layer decimation** (sample 1:N polygons
    below zoom Z) so Kano-class 484-ward shells do not block the main thread.
    """

    state_en: str
    ward_polygon_count_hint: int
    heatmap_decimation_stride: int  # 1 = all wards, 2 = every other feature index, etc.
    recommended_min_zoom_full_detail: float


def latency_profile_for_state(state_en: str) -> WardLatticeLatencyProfile:
    """Return ward-density / decimation hints for map latency (Kano vs Kaduna vs default)."""
    key = str(state_en or "").strip().lower().replace("state", "").strip()
    if key == "kano":
        return WardLatticeLatencyProfile(
            state_en="Kano",
            ward_polygon_count_hint=484,
            heatmap_decimation_stride=2,
            recommended_min_zoom_full_detail=10.5,
        )
    if key == "kaduna":
        return WardLatticeLatencyProfile(
            state_en="Kaduna",
            ward_polygon_count_hint=255,
            heatmap_decimation_stride=1,
            recommended_min_zoom_full_detail=9.5,
        )
    return WardLatticeLatencyProfile(
        state_en=str(state_en or "Nigeria"),
        ward_polygon_count_hint=300,
        heatmap_decimation_stride=1,
        recommended_min_zoom_full_detail=10.0,
    )


def nowcast_headcount_multiplier(
    *,
    official_age_days: float,
    pulse_index: float,
    sentiment_index: float,
    max_delta: float = 0.15,
) -> float:
    """
    Bounded adjustment when official rolls are stale.

    pulse_index / sentiment_index are expected roughly in [-1, 1] or [0, 1] — caller normalises.
    """
    if official_age_days <= 90.0:
        return 1.0
    # gentle lift when pulse and sentiment agree there is hidden demand
    raw = 1.0 + max_delta * max(-1.0, min(1.0, 0.5 * pulse_index + 0.5 * sentiment_index))
    return float(max(1.0 - max_delta, min(1.0 + max_delta, raw)))


def _fallback_live_student_pulse_snapshot() -> dict[str, Any]:
    """Last-resort payload so Eagle Voice / pulse strip never takes down the Run."""
    return {
        "academic_cycle_label": ACADEMIC_CYCLE_LABEL,
        "kaduna_seed_enrolment_notional": 0,
        "dapi_wards_indexed": 0,
        "dapi_verification_events_total": 0,
        "tooltip_historical": (
            "Pulse degraded: Kaduna weld JSON or verification store failed to load — "
            "check Part_04_Social/data/kaduna_pilot_student_deep_weld.json and logs/dapi_verification.sqlite."
        ),
        "tooltip_predictive": "Nowcast lane offline — pulse snapshot in fallback mode.",
        "tooltip_live": "DAPI lattice counters unavailable — snapshot degraded.",
        "tooltip_nuba": "",
        "pulse_degraded": True,
    }


def _live_student_pulse_snapshot_impl(
    *,
    verification_ward_keys: int | None,
    verification_event_total: int | None,
) -> dict[str, Any]:
    wk = verification_ward_keys
    vt = verification_event_total
    if wk is None or vt is None:
        try:
            from dapi_traditional_weld import init_verification_store, ward_verification_counts

            init_verification_store()
            vc = ward_verification_counts()
            if wk is None:
                wk = len(vc)
            if vt is None:
                vt = sum(int(x) for x in vc.values())
        except Exception:
            if wk is None:
                wk = 0
            if vt is None:
                vt = 0

    seed_total = 0
    raw: dict[str, Any] = {}
    try:
        raw = json.loads(KADUNA_DEEP_WELD_JSON.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        raw = {}
    for row in raw.get("institutions", []) or []:
        try:
            seed_total += int(row.get("notional_students_2025_26") or 0)
        except (TypeError, ValueError):
            pass
        for c in row.get("campus_enrolments", []) or []:
            try:
                seed_total += int(c.get("notional_students_2025_26") or 0)
            except (TypeError, ValueError):
                pass
    out: dict[str, Any] = {
        "academic_cycle_label": ACADEMIC_CYCLE_LABEL,
        "kaduna_seed_enrolment_notional": seed_total,
        "dapi_wards_indexed": int(wk),
        "dapi_verification_events_total": int(vt),
        "tooltip_historical": (
            f"Historical (cycle {ACADEMIC_CYCLE_LABEL}): notional Kaduna pilot enrolment seed "
            "(ABU + KASU + Kaduna Polytechnic [FED] + Nuhu Bamalli Polytechnic (NUBA) [STA] + NCAT) — "
            "replace with regulator bulk ingest when licensed."
        ),
        "tooltip_predictive": (
            "Predictive / nowcast: bounded pulse+sentiment multiplier on stale rolls (see "
            "nafc_student_load_pipeline.nowcast_headcount_multiplier) — live edge is DAPI verification mass "
            "on the ward spine."
        ),
        "tooltip_live": (
            "Live lattice: SQLite-backed DAPI verification counts keyed by ADM3 ward_pcode — "
            "does not yet equal national enrolment; it is the Me Anguwa workload pulse."
        ),
        "pulse_degraded": False,
    }
    try:
        from kaduna_student_deep_weld import nuba_for_pulse_tooltip

        out["tooltip_nuba"] = nuba_for_pulse_tooltip()
    except ImportError:
        out["tooltip_nuba"] = ""
    return out


def live_student_pulse_snapshot(
    *,
    verification_ward_keys: int | None = None,
    verification_event_total: int | None = None,
) -> dict[str, Any]:
    """Header strip payload — historical seed + live DAPI lattice counters.

    Omit ``verification_*`` to pull ward/event totals from the local verification SQLite (same steel as DAPI).
    Never raises: returns a **fallback** dict if weld JSON, SQLite, or imports fail (no red Run).
    """
    try:
        return _live_student_pulse_snapshot_impl(
            verification_ward_keys=verification_ward_keys,
            verification_event_total=verification_event_total,
        )
    except (OSError, ValueError, TypeError, ImportError, RuntimeError):
        return _fallback_live_student_pulse_snapshot()
    except Exception:
        return _fallback_live_student_pulse_snapshot()


def fallback_live_student_pulse_snapshot() -> dict[str, Any]:
    """Explicit export for UI defensive paths (Eagle fragment belt-and-suspenders)."""
    return _fallback_live_student_pulse_snapshot()
