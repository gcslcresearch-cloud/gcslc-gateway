"""
African Wealth Cloud (AWC) — 8R Stealth Paradigm Convergence
AWC asset dictionary for Nigeria: Minerals, Gems, Energy.
D1: Refine (high-purity corridors), D2: Reset (SPV → SSMV), D3: Research (rare earth coordinates).

Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026 GCSLC. Proprietary.
"""

import os
import sys
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple, Optional

# Ensure project root is on path for d8_logic and ssmv
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from d8_logic import apply_talon_lock, WEALTH_RETENTION_LOCK
from ssmv import SSMV

# --- 8R Stealth Paradigm Determinants ---
DETERMINANTS_8R = [
    "D1: Refine",
    "D2: Reset",
    "D3: Research",
    "D4: Restructure",
    "D5: Resuscitate",
    "D6: Revitalize",
    "D7: Re-engineer",
    "D8: Retain",
]

# --- African Wealth Cloud (AWC) asset dictionary for Nigeria ---
AWC_NIGERIA_ASSETS: Dict[str, Dict[str, Any]] = {
    "Minerals": {
        "items": ["Gold", "Bauxite", "Iron Ore", "Lead-Zinc"],
        "d_primary": "D1: Refine",
        "base_value_b_usd": 4.2,
        "corridors": [
            {"name": "North Central Gold", "purity_pct": 92, "lat": 9.08, "lon": 8.67},
            {"name": "South West Bauxite", "purity_pct": 78, "lat": 7.16, "lon": 3.35},
            {"name": "North West Iron Ore", "purity_pct": 65, "lat": 11.75, "lon": 7.08},
            {"name": "South East Lead-Zinc", "purity_pct": 88, "lat": 6.45, "lon": 7.50},
        ],
    },
    "Gems": {
        "items": ["Sapphire", "Tourmaline", "Aquamarine", "Emerald"],
        "d_primary": "D1: Refine",
        "base_value_b_usd": 1.8,
        "corridors": [
            {"name": "Jos Sapphire Belt", "purity_pct": 95, "lat": 9.90, "lon": 8.90},
            {"name": "Kaduna Tourmaline", "purity_pct": 89, "lat": 10.52, "lon": 7.44},
            {"name": "Oyo Aquamarine", "purity_pct": 82, "lat": 8.15, "lon": 4.25},
            {"name": "Niger Emerald Corridor", "purity_pct": 91, "lat": 9.60, "lon": 6.55},
        ],
    },
    "Energy": {
        "items": ["Oil", "Natural Gas", "NGECC Transition Logic"],
        "d_primary": "D1: Refine",
        "base_value_b_usd": 58.0,
        "corridors": [
            {"name": "Niger Delta Oil", "purity_pct": 85, "lat": 5.20, "lon": 6.75},
            {"name": "Offshore Gas", "purity_pct": 90, "lat": 4.50, "lon": 6.20},
            {"name": "NGECC Coal-to-Nuclear Bridge", "purity_pct": 88, "lat": 9.08, "lon": 8.67},
        ],
    },
}

# Legacy SPV model marker (D2 Reset decouples from this)
LEGACY_SPV_MODEL = "Legacy SPV"

# Rare earth deposit coordinates (D3 Research)
RARE_EARTH_DEPOSITS: List[Dict[str, Any]] = [
    {"name": "Bauchi Rare Earth Belt", "lat": 10.315, "lon": 9.844, "elements": ["Nb", "Ta", "REE"]},
    {"name": "Plateau Lithium-REE", "lat": 9.90, "lon": 8.90, "elements": ["Li", "REE", "Sn"]},
    {"name": "Nasarawa Coltan-REE", "lat": 8.50, "lon": 8.50, "elements": ["Nb", "Ta", "REE"]},
    {"name": "Kogi Rare Earth Corridor", "lat": 7.80, "lon": 6.75, "elements": ["REE", "Y", "Sc"]},
]


@dataclass
class DigitalSSMV:
    """Special Strategic Mission Vehicle (digital): output of 8R convergence; decoupled from legacy SPV."""
    code: str
    asset_source: str
    asset_category: str  # Minerals | Gems | Energy
    d1_refine_yield: float
    d2_reset_yield: float
    d3_research_yield: float
    retained_value_usd: float
    high_purity_corridors: List[str] = field(default_factory=list)
    rare_earth_coords: List[Dict[str, Any]] = field(default_factory=list)
    mandate: str = "Strategic Asset Defense and Resuscitation"


# --- D1: Refine — Filter for high-purity gem/mineral corridors ---
PURITY_THRESHOLD_HIGH = 80  # percent


def d1_refine_filter_corridors(category: str, min_purity_pct: float = PURITY_THRESHOLD_HIGH) -> List[Dict[str, Any]]:
    """D1 (Refine): Filter for high-purity gem/mineral corridors in the given category."""
    cat = AWC_NIGERIA_ASSETS.get(category)
    if not cat:
        return []
    corridors = cat.get("corridors", [])
    return [c for c in corridors if c.get("purity_pct", 0) >= min_purity_pct]


def d1_refine(raw_value_b_usd: float) -> float:
    """D1: Refine — transform raw asset value into refined sovereign value (Talon Lock)."""
    return apply_talon_lock(raw_value_b_usd * 1e9)


# --- D2: Reset — Decouple assets from legacy SPV models to SSMV structures ---
def d2_reset_decouple_to_ssmv(asset_name: str, category: str, base_value_b_usd: float) -> Tuple[float, str]:
    """
    D2 (Reset): Decouple from legacy SPV to SSMV structure.
    Returns (retained_value_usd, ssmv_code).
    """
    retained = apply_talon_lock(base_value_b_usd * 0.85 * 1e9)
    code = f"SSMV-{asset_name.upper().replace(' ', '_')[:14]}-8R"
    return retained, code


def d2_reset(raw_value_b_usd: float) -> float:
    """D2: Reset — baseline for sovereign re-allocation (95% retained)."""
    return apply_talon_lock(raw_value_b_usd * 0.85 * 1e9)


# --- D3: Research — Map coordinates for rare earth mineral deposits ---
def d3_research_rare_earth_coords() -> List[Dict[str, Any]]:
    """D3 (Research): Return mapped coordinates for rare earth mineral deposits."""
    return list(RARE_EARTH_DEPOSITS)


def d3_research(raw_value_b_usd: float) -> float:
    """D3: Research — scientific profit center multiplier."""
    try:
        from d8_logic import D3_WEALTH_MULTIPLIER
        return apply_talon_lock(raw_value_b_usd * D3_WEALTH_MULTIPLIER * 1e8)
    except Exception:
        return apply_talon_lock(raw_value_b_usd * 9.6 * 1e8)


def run_8r_convergence(asset_name: str, category: str, base_value_b_usd: float) -> DigitalSSMV:
    """
    Execute D1: Refine, D2: Reset, D3: Research on an AWC asset;
    return a digital SSMV (decoupled from legacy SPV).
    """
    d1 = d1_refine(base_value_b_usd)
    d2_val, ssmv_code = d2_reset_decouple_to_ssmv(asset_name, category, base_value_b_usd)
    d3 = d3_research(base_value_b_usd)
    total_retained = d1 + d2_val + d3
    corridors = d1_refine_filter_corridors(category)
    coords = d3_research_rare_earth_coords()
    return DigitalSSMV(
        code=ssmv_code,
        asset_source=asset_name,
        asset_category=category,
        d1_refine_yield=d1,
        d2_reset_yield=d2_val,
        d3_research_yield=d3,
        retained_value_usd=total_retained,
        high_purity_corridors=[c["name"] for c in corridors],
        rare_earth_coords=coords,
    )


def get_awc_flat_assets() -> List[Tuple[str, str, float]]:
    """Flatten AWC Nigeria assets to (asset_name, category, base_value_b_usd). Value split by item count."""
    out: List[Tuple[str, str, float]] = []
    for category, meta in AWC_NIGERIA_ASSETS.items():
        items = meta.get("items", [])
        base = meta.get("base_value_b_usd", 0)
        share = base / len(items) if items else 0
        for name in items:
            out.append((name, category, share))
    return out


def get_nigeria_ssmvs() -> List[DigitalSSMV]:
    """
    Map Nigeria AWC assets (Minerals, Gems, Energy) to 8R;
    D1 Refine (high-purity corridors), D2 Reset (SPV → SSMV), D3 Research (rare earth coords).
    """
    ssmvs: List[DigitalSSMV] = []
    for asset_name, category, base_value_b_usd in get_awc_flat_assets():
        ssmvs.append(run_8r_convergence(asset_name, category, base_value_b_usd))
    return ssmvs


def get_convergence_summary() -> Dict[str, Any]:
    """Summary of 8R convergence across all Nigeria AWC assets."""
    ssmvs = get_nigeria_ssmvs()
    total_retained = sum(s.retained_value_usd for s in ssmvs)
    d3_coords = d3_research_rare_earth_coords()
    return {
        "determinants": DETERMINANTS_8R,
        "awc_categories": list(AWC_NIGERIA_ASSETS.keys()),
        "nigeria_assets": [t[0] for t in get_awc_flat_assets()],
        "ssmv_count": len(ssmvs),
        "total_retained_value_usd": total_retained,
        "wealth_retention_lock_pct": int(WEALTH_RETENTION_LOCK * 100),
        "d1_high_purity_threshold_pct": PURITY_THRESHOLD_HIGH,
        "d3_rare_earth_deposits": d3_coords,
        "ssmvs": [
            {
                "code": s.code,
                "asset_source": s.asset_source,
                "asset_category": s.asset_category,
                "d1_refine_yield": s.d1_refine_yield,
                "d2_reset_yield": s.d2_reset_yield,
                "d3_research_yield": s.d3_research_yield,
                "retained_value_usd": s.retained_value_usd,
                "high_purity_corridors": s.high_purity_corridors,
            }
            for s in ssmvs
        ],
    }


# --- Triple-D3: CEO Audit ---
# D3-Alpha (Geopolitical): Nigeria Rare Earths → Big Tech supply chains
GLOBAL_TECH_ALIGNMENT: List[Dict[str, Any]] = [
    {"nigeria_asset": "Bauchi Rare Earth Belt", "elements": "Nb, Ta, REE", "big_tech": "Apple", "use_case": "iPhone / Mac power modules, sensors"},
    {"nigeria_asset": "Plateau Lithium-REE", "elements": "Li, REE, Sn", "big_tech": "Apple", "use_case": "Battery supply chain"},
    {"nigeria_asset": "Nasarawa Coltan-REE", "elements": "Nb, Ta, REE", "big_tech": "Alphabet", "use_case": "Data center / chip packaging"},
    {"nigeria_asset": "Kogi Rare Earth Corridor", "elements": "REE, Y, Sc", "big_tech": "Alphabet", "use_case": "EV / clean tech minerals"},
]

# D3-Beta (Temporal): Wealth Retention Timeline 2026–2050 ($170.85B unlock cycle)
WEALTH_UNLOCK_TOTAL_B = 170.85
TIMELINE_START_YEAR = 2026
TIMELINE_END_YEAR = 2050


def get_wealth_retention_timeline(year: int) -> float:
    """D3-Beta: Unlock value (B USD) in a given year. Equal annual unlock over 2026–2050."""
    if year < TIMELINE_START_YEAR or year > TIMELINE_END_YEAR:
        return 0.0
    span = TIMELINE_END_YEAR - TIMELINE_START_YEAR + 1
    return round(WEALTH_UNLOCK_TOTAL_B / span, 2)


def get_timeline_cumulative(year: int) -> float:
    """Cumulative unlock by end of given year."""
    return sum(get_wealth_retention_timeline(y) for y in range(TIMELINE_START_YEAR, year + 1))


# D3-Gamma (Security): 8R Paradigm vs market volatility — risk defense strength (0–100)
RISK_DEFENSE_HEATMAP: List[Dict[str, Any]] = [
    {"determinant": "D1: Refine", "volatility_risk": "Commodity price", "defense_score": 88},
    {"determinant": "D2: Reset", "volatility_risk": "FX / sovereign default", "defense_score": 92},
    {"determinant": "D3: Research", "volatility_risk": "Tech supply chain", "defense_score": 85},
    {"determinant": "D4: Restructure", "volatility_risk": "Regulatory", "defense_score": 78},
    {"determinant": "D5: Resuscitate", "volatility_risk": "Asset stranding", "defense_score": 90},
    {"determinant": "D6: Revitalize", "volatility_risk": "Demand shock", "defense_score": 82},
    {"determinant": "D7: Re-engineer", "volatility_risk": "Operational", "defense_score": 86},
    {"determinant": "D8: Retain", "volatility_risk": "Capital flight", "defense_score": 95},
]


def get_global_tech_alignment() -> List[Dict[str, Any]]:
    """D3-Alpha (Geopolitical): Nigeria Rare Earths → Apple/Alphabet supply chains."""
    return list(GLOBAL_TECH_ALIGNMENT)


def get_risk_defense_heatmap() -> List[Dict[str, Any]]:
    """D3-Gamma (Security): Risk Defense Heatmap — 8R protection vs market volatility."""
    return list(RISK_DEFENSE_HEATMAP)


# Backwards compatibility: expose asset dict under old name for any existing callers
NIGERIA_RAW_ASSETS = AWC_NIGERIA_ASSETS
