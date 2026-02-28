# GCSLC Sovereign Retention Protocol - D8 Logic
# Galadiman Ruwa Center For Strategic Leadership and Communication LTD/GTE — GCSLC
# © GCSLC. Proprietary.

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
