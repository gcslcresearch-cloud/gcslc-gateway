"""
Part_02 Finance sovereign yield coupling logic.
Links coal reserve nodes to debt-erasure projections.
"""

from __future__ import annotations

from typing import Any


TOTAL_DEBT_TARGET_NAIRA = 55_000_000_000_000  # NGN 55T


def sovereign_yield_for_state(state: str, reserves_mt: float) -> dict[str, Any]:
    """
    Computes indicative sovereign yield for a coal node.
    Uses a simplified policy model for Phase-1 visualization.
    """
    mw_potential = max(120, int(220 + reserves_mt * 0.95))
    silicon_feedstock_kt = round(reserves_mt * 0.42, 1)
    annual_value_naira = float(mw_potential) * 14_500_000_000 + silicon_feedstock_kt * 95_000_000
    return {
        "state": state,
        "mw_potential": mw_potential,
        "silicon_feedstock_kt": silicon_feedstock_kt,
        "annual_value_naira": annual_value_naira,
        "status": "Moribund / Awaiting Resuscitation",
    }


def debt_erasure_projection(yields: list[dict[str, Any]]) -> dict[str, Any]:
    total_annual_value = sum(y["annual_value_naira"] for y in yields)
    coverage_ratio = (total_annual_value / TOTAL_DEBT_TARGET_NAIRA) if TOTAL_DEBT_TARGET_NAIRA else 0.0
    return {
        "total_annual_value_naira": total_annual_value,
        "debt_target_naira": TOTAL_DEBT_TARGET_NAIRA,
        "debt_coverage_ratio": round(coverage_ratio, 4),
        "debt_coverage_pct": round(coverage_ratio * 100, 2),
    }
