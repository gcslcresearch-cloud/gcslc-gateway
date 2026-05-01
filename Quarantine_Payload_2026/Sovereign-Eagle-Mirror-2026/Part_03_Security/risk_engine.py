"""
Real-world risk correlation engine:
combines telecom blackout pressure with vandalism proximity.
"""

from __future__ import annotations

import math
from typing import Any


EARTH_RADIUS_KM = 6371.0


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    return EARTH_RADIUS_KM * (2 * math.asin(min(1.0, math.sqrt(a))))


def _max_proximity_weight(lat: float, lon: float, points: list[dict[str, Any]]) -> float:
    if not points:
        return 0.0
    weights = []
    for point in points:
        km = haversine_km(lat, lon, point["lat"], point["lon"])
        # Nearer events have stronger effect; decays with distance.
        weights.append(1.0 / (1.0 + km))
    return max(weights, default=0.0)


def correlate_blackout_vandalism_risk(
    *,
    lat: float,
    lon: float,
    blackout_events: list[dict[str, Any]],
    vandalism_incidents: list[dict[str, Any]],
) -> dict[str, Any]:
    blackout_proximity = _max_proximity_weight(lat, lon, blackout_events)
    vandal_proximity = _max_proximity_weight(lat, lon, vandalism_incidents)

    blackout_intensity = max(
        (
            (event["severity"] * min(event["downtime_minutes"], 240) / 240.0)
            / (1.0 + haversine_km(lat, lon, event["lat"], event["lon"]))
        )
        for event in blackout_events
    ) if blackout_events else 0.0

    vandal_intensity = max(
        (
            (incident["severity"] * min(incident["cases_30d"], 8) / 8.0)
            / (1.0 + haversine_km(lat, lon, incident["lat"], incident["lon"]))
        )
        for incident in vandalism_incidents
    ) if vandalism_incidents else 0.0

    # Correlation pressure rises when both vectors are present in same locality.
    correlation_pressure = math.sqrt(max(0.0, blackout_intensity * vandal_intensity))
    risk_score = min(100.0, 100.0 * (0.42 * blackout_proximity + 0.33 * vandal_proximity + 0.25 * correlation_pressure))

    tier = "LOW"
    if risk_score >= 70:
        tier = "CRITICAL"
    elif risk_score >= 50:
        tier = "HIGH"
    elif risk_score >= 30:
        tier = "MEDIUM"

    return {
        "risk_score": round(risk_score, 2),
        "risk_tier": tier,
        "blackout_proximity": round(blackout_proximity, 4),
        "vandal_proximity": round(vandal_proximity, 4),
        "correlation_pressure": round(correlation_pressure, 4),
    }
