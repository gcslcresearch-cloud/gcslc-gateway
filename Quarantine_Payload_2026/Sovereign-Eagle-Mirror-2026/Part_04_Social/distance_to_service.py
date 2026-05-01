"""
Distance-to-Service analytics for Human Residence nodes.
Computes nearest bank/network service gap per village.
"""

from __future__ import annotations

import math
from typing import Iterable

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
    c = 2 * math.asin(min(1.0, math.sqrt(a)))
    return EARTH_RADIUS_KM * c


def nearest_service(village: dict, facilities: Iterable[dict]) -> dict:
    nearest = None
    nearest_distance = float("inf")

    for facility in facilities:
        dist = haversine_km(village["lat"], village["lon"], facility["lat"], facility["lon"])
        if dist < nearest_distance:
            nearest_distance = dist
            nearest = facility

    return {
        "village": village["name"],
        "lat": village["lat"],
        "lon": village["lon"],
        "nearest_service": nearest["name"] if nearest else "N/A",
        "service_kind": nearest["kind"] if nearest else "unknown",
        "distance_km": round(nearest_distance, 2) if nearest else None,
    }
