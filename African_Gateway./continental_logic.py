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


# --- Opportunity Sniffer & Strike: Determinant reveal per node (word pop-up when talon strikes) ---
NODE_DETERMINANT_REVEAL: Dict[str, str] = {
    "nigeria": "D1: Refine, D2: Reset & D3: Research Applied",
    "ghana": "D1: Refine & D3: Research Applied",
    "south_africa": "D1: Refine, D4: Restructure & D6: Revitalize Applied",
    "egypt": "D3: Research & D8: Retain Applied",
    "dubai": "D3: Research & D8: Retain Applied",
}


def get_determinant_reveal(node_id: Optional[str]) -> str:
    """Return the determinant pop-up text for a struck node (8R Scientific Analysis)."""
    if not node_id:
        return ""
    return NODE_DETERMINANT_REVEAL.get(node_id, "8R Paradigm Applied")


# --- Market Gap Analysis: Demand vs Supply (grounds $170.85B valuation) ---
MARKET_GAP_ANALYSIS: Dict[str, Dict[str, Any]] = {
    "nigeria": {"demand_pct": 94, "supply_pct": 22, "gap_b_usd": 72.0, "asset": "Minerals, Gems, Energy"},
    "ghana": {"demand_pct": 88, "supply_pct": 18, "gap_b_usd": 12.5, "asset": "Gold"},
    "south_africa": {"demand_pct": 91, "supply_pct": 35, "gap_b_usd": 28.0, "asset": "PGM, Minerals"},
    "egypt": {"demand_pct": 85, "supply_pct": 28, "gap_b_usd": 15.0, "asset": "Gas, Logistics"},
    "dubai": {"demand_pct": 96, "supply_pct": 42, "gap_b_usd": 43.35, "asset": "Logistical hubs"},
}


def get_market_gap_for_node(node_id: Optional[str]) -> Dict[str, Any]:
    """Market Gap (Demand vs Supply) for the struck node; supports Sovereign Glass lab display."""
    if not node_id or node_id not in MARKET_GAP_ANALYSIS:
        return {"demand_pct": 90, "supply_pct": 25, "gap_b_usd": WEALTH_UNLOCK_TOTAL_B / 5, "asset": "Continental"}
    return dict(MARKET_GAP_ANALYSIS[node_id])


def is_10b_plus_opportunity(node_id: Optional[str]) -> bool:
    """True if this node has a $10B+ opportunity gap (5km hover → radar sweep before strike)."""
    if not node_id:
        return False
    gap = get_market_gap_for_node(node_id)
    return gap.get("gap_b_usd", 0) >= 10.0


# --- Big Tech Handshake Manifesto (Sovereign Rationale) ---
BIG_TECH_HANDSHAKE_MANIFESTO = (
    "**Big Tech Handshake Manifesto**  \n\n"
    "GCSLC sovereign corridors align national asset revitalization with global tech supply chains. "
    "The handshake is not dependency—it is *structured convergence*: Natural Gas powers data and industry; "
    "Gold anchors value and fintech rails; Rare Earths secure the semiconductor and battery future. "
    "Under the 8R Paradigm, Nigeria and Africa retain the anchor. Big Tech gains stable, ethical supply; "
    "the Sovereign Node retains 95% and deploys D1 Refine, D2 Reset, D3 Research to transform raw corridors "
    "into digital SSMVs. **Natural Gas**, **Gold**, and **Rare Earth** SSMV corridors are the triple lock."
)
SSMV_CORRIDORS_MANIFESTO = ["Natural Gas", "Gold", "Rare Earth"]

# --- Silicon Valley Strategic Intent (sidebar panel) ---
ENERGY_MINERAL_SHIELD = (
    "**Energy & Mineral Shield**  \n\n"
    "Sovereign control of energy and mineral corridors under the 8R Paradigm ensures that "
    "national assets are not exposed to external volatility without a structured handshake. "
    "The Shield protects the $170.85B valuation anchor by aligning supply with sovereign retention (D8: Retain) "
    "and high-purity refinement (D1: Refine) before any external offtake."
)
SANTIAGO_COMPLIANCE = (
    "**Santiago Compliance**  \n\n"
    "All GCSLC sovereign corridors operate in compliance with the Santiago Principles: "
    "transparency, accountability, and alignment with the host nation's economic objectives. "
    "The 8R Scientific Analysis and D1–D3 determinants provide the empirical framework; "
    "the $170.85B valuation anchor is the central metric for sovereign validation."
)

# --- Foundational Intelligence Layer (sidebar) ---
INVESTOR_MANIFESTO = (
    "**Investor Manifesto**  \n\n"
    "GCSLC positions sovereign asset corridors as the anchor for long-term value. "
    "The 8R Paradigm (D1 Refine, D2 Reset, D3 Research) transforms raw minerals, gems, and energy "
    "into digital SSMVs with 95% sovereign retention. The $170.85B valuation anchor is the central "
    "empirical metric. Invest in the node that secures the anchor."
)
DOCTOR_VS_PHARMACIST = (
    "**Doctor vs. Pharmacist**  \n\n"
    "The Doctor diagnoses and prescribes the *structure* (what to refine, reset, research). "
    "The Pharmacist dispenses the *instrument* (how it is executed). GCSLC is the Doctor: "
    "we define the 8R determinants and the sovereign corridors. Execution partners align "
    "to the prescription. Physical asset grounding is the diagnosis; digital SSMVs are the dispensation."
)
STRATEGIC_DOCTRINE_CEO = (
    "**Strategic Doctrine (CEO Brief)**  \n\n"
    "Current AI and tech models are *moribund* without physical asset grounding. "
    "Data and algorithms alone cannot secure supply chains, rare earths, or energy transition. "
    "GCSLC sovereign corridors (Minerals, Gems, Energy) provide the physical anchor; "
    "the 8R Paradigm and $170.85B valuation are the empirical bridge. "
    "When a CEO (e.g. Nvidia, Apple) interacts with this node, the handshake is clear: "
    "ground your stack in sovereign assets or remain structurally exposed."
)

# Scientific reveal: Nigeria Minerals, Gems, Energy — canonical Demand/Supply for display
NIGERIA_SCIENTIFIC_REVEAL = {"demand_pct": 94, "supply_pct": 22, "asset": "Minerals, Gems, and Energy", "valuation_anchor_b": 170.85}


# Backwards compatibility: expose asset dict under old name for any existing callers
NIGERIA_RAW_ASSETS = AWC_NIGERIA_ASSETS
