"""
Security-side quad pillar engine grafted from Alpha.
Zaria anchor remains the fixed sovereign reference.
"""

from __future__ import annotations

import hashlib
import math

from Part_03_Security.risk_engine import correlate_blackout_vandalism_risk

ZARIA_ANCHOR = {
    "id": "anchor-zaria",
    "label": "Sovereign Anchor - Zaria",
    "lat": 11.0855,
    "lon": 7.7200,
}

EARTH_RADIUS_KM = 6371.0


def _to_rad(value: float) -> float:
    return value * math.pi / 180.0


def distance_km_to_anchor(lat: float, lon: float) -> float:
    dlat = _to_rad(ZARIA_ANCHOR["lat"] - lat)
    dlon = _to_rad(ZARIA_ANCHOR["lon"] - lon)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(_to_rad(lat))
        * math.cos(_to_rad(ZARIA_ANCHOR["lat"]))
        * math.sin(dlon / 2) ** 2
    )
    return 2 * EARTH_RADIUS_KM * math.asin(min(1.0, math.sqrt(a)))


def _unit_interval(lat: float, lon: float, salt: str) -> float:
    key = f"{lat:.5f}|{lon:.5f}|{salt}|gcslc-4p".encode("utf-8")
    digest = hashlib.sha256(key).hexdigest()[:8]
    return int(digest, 16) / 0xFFFFFFFF


def buildQuadPillarReality(
    lat: float,
    lon: float,
    blackout_events: list[dict] | None = None,
    vandalism_incidents: list[dict] | None = None,
) -> dict:
    z_km = distance_km_to_anchor(lat, lon)
    signal = round(22 + 68 * _unit_interval(lat, lon, "signal"))
    rsrp = round(-90 - 32 * _unit_interval(lat, lon, "rsrp"))
    mfi = round(18 + 64 * _unit_interval(lat, lon, "mfi"))
    risk = correlate_blackout_vandalism_risk(
        lat=lat,
        lon=lon,
        blackout_events=blackout_events or [],
        vandalism_incidents=vandalism_incidents or [],
    )

    return {
        "commHealth": (
            f"Spine-locked to Zaria ({z_km:.1f} km) with composite {signal}, "
            f"RSRP est. {rsrp} dBm."
        ),
        "financialDepth": (
            f"AZK financial spine active with index {mfi}; "
            f"return legs resolve to Zaria anchor."
        ),
        "securityPresence": (
            f"Lalata risk {risk['risk_score']} ({risk['risk_tier']}) from blackout/vandalism handshake; "
            f"distance pressure from anchor: {z_km:.1f} km."
        ),
        "socialResonance": (
            "PHC-market social coupling remains governed by the Zaria-centered corridor pulse."
        ),
        "raw": {
            "lat": lat,
            "lon": lon,
            "zKm": z_km,
            "anchor": ZARIA_ANCHOR,
            "risk": risk,
        },
    }
