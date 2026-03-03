# GCSLC Sovereign Retention Protocol - D8 Logic
# Galadiman Ruwa Center For Strategic Leadership and Communication LTD/GTE — GCSLC
# © GCSLC. Proprietary.
# GEC Sovereign Twins: 8R-within-8R recursive logic — D3 within D3 (Synthetic Intelligence).

# 8R Determinants (Sovereign Twins architecture)
DETERMINANTS_8R = [
    "Refine", "Reset", "Research", "Restructure",
    "Resuscitate", "Revitalize", "Re-engineer", "Retain",
]

# Non-linear, non-transferable anchor (all within-outcomes)
CAC_ANCHOR = "176917792057"
CHAIRMAN_ANCHOR = "Dr. Sa'ad Jaafaru"

WEALTH_RETENTION_LOCK = 0.95
STRATEGIC_FOUNDATION = "1m_x_1m_Steel"

# NWC/C&D Sovereign Retention — 95% National Equity, 5% Global Adoption Pool
TALON_LOCK_NATIONAL_PCT = 0.95
TALON_LOCK_GLOBAL_POOL_PCT = 0.05

# D3 Scientific Profit Centers — 9.6x wealth multiplier (per MT coal/diamond throughput)
D3_WEALTH_MULTIPLIER = 9.6
D3_GERMANIUM_USD_PER_KG = 8597.0      # AI Chip Grade
D3_AMMONIA_USD_PER_MT = 430.0         # Fertilizer Grade
D3_SILICON_MONTHLY_YIELD_M = 6.50     # Semiconductor Grade, $M
D3_COAL_SYNGAS_MONTHLY_REVENUE_M = 15.20  # Sovereign Feedstock, $M

# ——— GEC Sovereign Master: 600M MT Coal-to-Compute Strike ———
# 639.3 million MT coal reserves → primary energy feedstock for Sovereign AI Factories
GEC_COAL_RESERVES_M_MT = 639.3  # 639.3 million MT (total)
ABUJA_ZARIA_KANO_CORRIDOR = "Abuja-Zaria-Kano"  # Primary corridor for Sovereign AI feedstock
POWER_POTENTIAL_GW = 1.2  # 1.2 GW power potential to anchor 2026 Nigerian infrastructure (Cassava, etc.)


def apply_talon_lock(value_generated):
    """Return the sovereign-retained share (95%) of value generated under D8 Logic.
    Returns 0.0 for None or invalid input to avoid unhandled exceptions."""
    if value_generated is None:
        return 0.0
    try:
        return float(value_generated) * WEALTH_RETENTION_LOCK
    except (TypeError, ValueError):
        return 0.0


def apply_95_5_talon_lock(derivative_revenue):
    """Sovereign Retention: 95% National Equity, 5% Global Adoption Pool (Wall Street/Silicon Valley).
    Returns (national_equity, global_pool)."""
    if derivative_revenue is None:
        return 0.0, 0.0
    try:
        v = float(derivative_revenue)
        return v * TALON_LOCK_NATIONAL_PCT, v * TALON_LOCK_GLOBAL_POOL_PCT
    except (TypeError, ValueError):
        return 0.0, 0.0


# ——— GEC Sovereign Twins: Within-Logic (8R-within-8R) ———
def d_within_d(det_name: str, has_data: bool, context: str = "") -> str:
    """For each Determinant, return status or D3 Synthetic Intelligence fallback.
    Anchor: CAC {CAC_ANCHOR} | Chairman: {CHAIRMAN_ANCHOR} (non-transferable)."""
    if has_data:
        return f"{det_name}: empirical data lock established. CAC: {CAC_ANCHOR} | Chairman: {CHAIRMAN_ANCHOR}."
    return (
        f"{det_name} (Within): D3 Synthetic Intelligence activated — "
        "modelling strategic truth from $1.5T legacy infrastructure wealth leakage, "
        "global energy corridors, and NVIDIA-class compute demand. "
        f"Directional prompt: {context or 'Escalate to Sovereign AI / 1,205 MW corridor.'} "
        f"CAC: {CAC_ANCHOR} | Chairman: {CHAIRMAN_ANCHOR} (non-transferable anchor)."
    )


def get_d3_synthetic_for_bua_2026(has_bua_data: bool, has_energy_feed: bool = False) -> dict:
    """First within-D3 result for BUA–NVIDIA Sovereign Strike. Shows how GCSLC out-thinks legacy conglomerates."""
    has_data = has_bua_data and has_energy_feed
    return {
        "active": not has_data,
        "title": "D3 within D3 — BUA 2026 Expansion",
        "message": (
            "D3 Synthetic Intelligence: Strategic truth for BUA industrial nodes and 2026 expansion. "
            "Legacy conglomerates rely on static feasibility studies; GEC models real-time energy friction, "
            "1,205 MW NVIDIA-standard compute hub alignment, and 9.6× wealth multiplier under Talon Lock. "
            "Directional prompt: Align Kogi/Enugu/Benue corridor nodes to Sovereign AI demand; "
            "recalibrate WL ticker every 60s for logistics and energy price shifts."
        ),
        "anchor": f"CAC: {CAC_ANCHOR} | Chairman & Founder: {CHAIRMAN_ANCHOR} — non-linear, non-transferable.",
    }


# ——— Recursive 8R within 8R: D3 within D3 strike — Liquid Intelligent Technologies (West African grid-interaction) ———
# WL = Wealth Lost: D3 Synthetic Intelligence identifies exact WL from grid unreliability, diesel backup cost, foregone AI/DC capacity.
LIQUID_WL_WEST_AFRICA_GRID_USD_M = 72.0   # Estimated annual WL from grid-related outages and backup (D3 modelled)
LIQUID_WL_WEST_AFRICA_POWER_SHORTFALL_MW = 380.0  # MW equivalent shortfall vs. sovereign 1,205 MW anchor
LIQUID_WL_CONTEXT = (
    "Liquid Intelligent Technologies: West African fiber and DC footprint depends on grid stability. "
    "D3 within D3 strike identifies WL from grid-interaction: diesel backup cost, outage-driven revenue loss, "
    "and foregone AI/DC capacity due to unreliable power. Alignment with GEC 1,205 MW Sovereign Energy Node "
    "reduces WL and unlocks 9.6× wealth multiplier on recovered capacity."
)


def get_d3_liquid_wl_west_africa(has_liquid_grid_data: bool = False) -> dict:
    """D3 within D3 strike: exact WL (Wealth Lost) Liquid Intelligent Technologies faces in West African grid-interaction.
    Recursive 8R-within-8R activation for Cassava–NVIDIA Sovereign Strike."""
    return {
        "active": True,
        "title": "D3 within D3 — Liquid Intelligent Technologies (West African grid-interaction)",
        "wl_usd_m": LIQUID_WL_WEST_AFRICA_GRID_USD_M,
        "wl_power_shortfall_mw": LIQUID_WL_WEST_AFRICA_POWER_SHORTFALL_MW,
        "message": LIQUID_WL_CONTEXT if not has_liquid_grid_data else (
            "Liquid: empirical grid data lock established. WL ticker recalibrated. "
            f"CAC: {CAC_ANCHOR} | Chairman: {CHAIRMAN_ANCHOR} (non-transferable)."
        ),
        "anchor": f"CAC: {CAC_ANCHOR} | Chairman & Founder: {CHAIRMAN_ANCHOR} — non-linear, non-transferable.",
    }


# ——— Recursive Intelligence: D3 within D3 — Cassava Technologies 2026 Nigerian infrastructure (1.2 GW anchor) ———
def get_d3_cassava_2026_nigerian_infra(has_cassava_feed: bool = False) -> dict:
    """D3 within D3: How Cassava Technologies can utilize 1.2 GW power potential to anchor their 2026 Nigerian infrastructure.
    Strategic focus: 639.3 M MT coal reserves mapped to Abuja-Zaria-Kano Corridor as primary energy feedstock for Sovereign AI Factories."""
    return {
        "active": True,
        "title": "D3 within D3 — Cassava 2026 Nigerian Infrastructure (1.2 GW anchor)",
        "power_gw": POWER_POTENTIAL_GW,
        "coal_reserves_m_mt": GEC_COAL_RESERVES_M_MT,
        "corridor": ABUJA_ZARIA_KANO_CORRIDOR,
        "message": (
            "Cassava Technologies: Utilize GEC 1.2 GW power potential to anchor 2026 Nigerian infrastructure. "
            "639.3 M MT coal reserves mapped to Abuja-Zaria-Kano Corridor as primary energy feedstock for Sovereign AI Factories. "
            "D3 Synthetic Intelligence: baseload from coal-to-compute strike displaces diesel and grid friction; "
            "9.6× wealth multiplier under Talon Lock. Directional prompt: Align Cassava Nigerian AI Factory to AZK corridor; "
            "lock baseload and scale. CAC: {} | Chairman: {} (non-transferable)."
        ).format(CAC_ANCHOR, CHAIRMAN_ANCHOR) if not has_cassava_feed else (
            "Cassava: empirical feed established. 1.2 GW anchor locked for 2026. "
            f"CAC: {CAC_ANCHOR} | Chairman: {CHAIRMAN_ANCHOR} (non-transferable)."
        ),
        "anchor": f"CAC: {CAC_ANCHOR} | Chairman & Founder: {CHAIRMAN_ANCHOR} — non-linear, non-transferable.",
    }
