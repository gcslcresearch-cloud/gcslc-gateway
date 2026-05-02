"""
Strategic Cell index — LGAs and wards as addressable lattice keys (inference bridge).

Each ward row in the fused partition is a cell identity for discovery pivots (POS, NTW proxy, PU).
"""

from __future__ import annotations

from typing import Any


NATIONAL_LGA_TARGET = 774
NATIONAL_WARD_TARGET = 8806


def strategic_cells_banner(fused_df: Any | None) -> str:
    """Single forensic line for the sovereign detail widget / atomic HUD."""
    if fused_df is None or getattr(fused_df, "empty", True):
        return (
            "Knowledge graph · strategic cells OFFLINE — mount gcslc_deep_join fuse "
            f"(target {NATIONAL_LGA_TARGET} LGAs · {NATIONAL_WARD_TARGET:,} wards)"
        )
    try:
        n_lga = len(fused_df)
        w_sum = int(fused_df["ward_count"].sum())
    except Exception:
        return "Knowledge graph · ward manifest unreadable — checksum REVIEW"
    return (
        f"Knowledge graph · {n_lga} LGA inference shells · {w_sum:,} ward strategic cells indexed · "
        f"POS / lattice pivots bind to Sovereign Gold emphasis"
    )
