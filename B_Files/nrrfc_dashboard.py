"""
GEC-COAL-BASE-13 (ID: GEC-8051-NGECC-001)
8R Stealth B_Files — sovereign anchor for the 13-state coal nodal.

This file is designated as the sovereign anchor for the 13-state coal nodal, focusing
specifically on the 9.6× wealth multiplier logic for Germanium (AI Chip Grade) and
Ammonia (Fertilizer Grade) under D3 Scientific Profit Centers. All corridor reserves,
power potential (1,205 MW), and D3 derivative pricing are canonical here.

8R Determinants logic is pulled from the primary 8R Stealth folder (project root) in
real-time so that updates to d8_logic there reflect here instantly on next import/run.

GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION LTD/GTE — CAC: 176917792057.
© GCSLC. Proprietary.
"""
from __future__ import annotations

import os
import sys

# Ensure primary 8R Stealth folder (project root) is on path for real-time 8R logic
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# Real-time pull: every import uses latest d8_logic from primary folder
from d8_logic import (
    DETERMINANTS_8R,
    d_within_d,
    get_d3_synthetic_for_bua_2026,
    CAC_ANCHOR,
    CHAIRMAN_ANCHOR,
    D3_WEALTH_MULTIPLIER,
    D3_GERMANIUM_USD_PER_KG,
    D3_AMMONIA_USD_PER_MT,
    WEALTH_RETENTION_LOCK,
)

# 9.6× wealth multiplier logic — Germanium & Ammonia (sovereign anchor for 13-state coal nodal)
WEALTH_MULTIPLIER_9_6 = D3_WEALTH_MULTIPLIER  # 9.6× per MT coal/diamond throughput
GERMANIUM_USD_PER_KG = D3_GERMANIUM_USD_PER_KG  # AI Chip Grade
AMMONIA_USD_PER_MT = D3_AMMONIA_USD_PER_MT     # Fertilizer Grade

__all__ = [
    "GEC_COAL_BASE_13",
    "GEC_COAL_BASE_13_ID",
    "DETERMINANTS_8R",
    "d_within_d",
    "get_d3_synthetic_for_bua_2026",
    "COAL_CORRIDOR_RESERVES_MT",
    "COAL_CORRIDOR_POWER_MW",
    "TOTAL_RESERVES_MT",
    "TOTAL_POWER_MW",
    "WEALTH_MULTIPLIER_9_6",
    "GERMANIUM_USD_PER_KG",
    "AMMONIA_USD_PER_MT",
]

# Sovereign anchor ID
GEC_COAL_BASE_13_ID = "GEC-8051-NGECC-001"

# 13-state coal corridor (app.html / 8R Stealth canonical)
COAL_CORRIDOR_RESERVES_MT = {
    "Enugu": 168.0,
    "Kogi": 142.0,
    "Gombe": 62.0,
    "Benue": 85.0,
    "Niger": 35.0,
    "Nasarawa": 22.0,
    "Plateau": 28.0,
    "Taraba": 18.0,
    "Adamawa": 12.0,
    "Bauchi": 25.0,
    "Ebonyi": 15.0,
    "Anambra": 27.3,
    "Cross River": 0.0,
}
TOTAL_RESERVES_MT = 639.3

COAL_CORRIDOR_POWER_MW = {
    "Enugu": 340,
    "Kogi": 300,
    "Gombe": 90,
    "Benue": 120,
    "Niger": 70,
    "Nasarawa": 45,
    "Plateau": 55,
    "Taraba": 35,
    "Adamawa": 25,
    "Bauchi": 50,
    "Ebonyi": 30,
    "Anambra": 55,
    "Cross River": 0,
}
TOTAL_POWER_MW = 1205  # 1,205 MW AI-DC — WPC 2026 Roadmap Ready


class GEC_COAL_BASE_13:
    """
    GEC-COAL-BASE-13 (ID: GEC-8051-NGECC-001).
    Sovereign anchor for the 13-state coal nodal. Focus: 9.6× wealth multiplier
    logic for Germanium (AI Chip Grade) and Ammonia (Fertilizer Grade). 8R
    Determinants are read from the primary 8R Stealth folder in real-time.
    """

    ID = GEC_COAL_BASE_13_ID
    TITLE = "GEC-COAL-BASE-13"
    RESERVES_MT = COAL_CORRIDOR_RESERVES_MT
    POWER_MW = COAL_CORRIDOR_POWER_MW
    TOTAL_RESERVES_MT = TOTAL_RESERVES_MT
    TOTAL_POWER_MW = TOTAL_POWER_MW
    # 9.6× wealth multiplier — Germanium & Ammonia (sovereign anchor)
    WEALTH_MULTIPLIER_9_6 = WEALTH_MULTIPLIER_9_6
    GERMANIUM_USD_PER_KG = GERMANIUM_USD_PER_KG
    AMMONIA_USD_PER_MT = AMMONIA_USD_PER_MT
    DETERMINANTS_8R = DETERMINANTS_8R  # real-time from primary folder
    CAC_ANCHOR = CAC_ANCHOR
    CHAIRMAN_ANCHOR = CHAIRMAN_ANCHOR

    @classmethod
    def get_determinants(cls) -> list[str]:
        """8R Determinants from primary 8R Stealth folder; reflects latest on every call (module already imported)."""
        return list(DETERMINANTS_8R)

    @classmethod
    def d_within_d(cls, det_name: str, has_data: bool, context: str = "") -> str:
        """Within-logic from primary folder (real-time)."""
        return d_within_d(det_name, has_data, context)

    @classmethod
    def get_d3_synthetic_for_bua_2026(cls, has_bua_data: bool, has_energy_feed: bool = False) -> dict:
        """D3 Synthetic Intelligence result from primary folder (real-time)."""
        return get_d3_synthetic_for_bua_2026(has_bua_data, has_energy_feed)

    @classmethod
    def wealth_multiplier_germanium_ammonia(cls) -> dict:
        """9.6× wealth multiplier logic for Germanium and Ammonia (sovereign anchor)."""
        return {
            "wealth_multiplier": cls.WEALTH_MULTIPLIER_9_6,
            "germanium_usd_per_kg": cls.GERMANIUM_USD_PER_KG,  # AI Chip Grade
            "ammonia_usd_per_mt": cls.AMMONIA_USD_PER_MT,     # Fertilizer Grade
        }
