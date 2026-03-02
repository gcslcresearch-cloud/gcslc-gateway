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
