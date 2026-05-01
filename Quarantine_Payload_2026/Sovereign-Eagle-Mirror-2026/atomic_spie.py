"""
Atomic federation — canonical PU inventory + ward-cluster lattice placement.

National rollout uses GeoJSON-per-ward semantics at the data layer (grouped by INEC
ward triple), rendered only inside the current viewport FeatureGroup for mobile Lux.
"""

from __future__ import annotations

import functools
import math
import re
from typing import Any

import pandas as pd

CANONICAL_PU_CSV_URL = (
    "https://raw.githubusercontent.com/Emeka-Onwuepe/Polling_Units_in_Nigeria/main/"
    "Nigeria_polling_units.csv"
)

WARD_REF_URL = (
    "https://raw.githubusercontent.com/temikeezy/nigeria-geojson-data/main/data/wards.json"
)

NATIONAL_PU_EXPECTED = 176_846
MAX_VIEWPORT_ATOMS = 10_000


def _norm(s: Any) -> str:
    t = str(s).strip().lower()
    t = re.sub(r"\s+", " ", t)
    return t


@functools.lru_cache(maxsize=1)
def _centroid_lookup_tables() -> tuple[
    dict[tuple[str, str, str], tuple[float, float]],
    dict[tuple[str, str], tuple[float, float]],
    dict[str, tuple[float, float]],
]:
    import requests

    data = requests.get(WARD_REF_URL, timeout=120).json()
    ward_pt: dict[tuple[str, str, str], tuple[float, float]] = {}
    lga_acc: dict[tuple[str, str], list[tuple[float, float]]] = {}
    st_acc: dict[str, list[tuple[float, float]]] = {}
    for x in data:
        st = _norm(x["State"])
        lg = _norm(x["LGA"])
        wd = _norm(x["Ward"])
        lat, lon = float(x["Latitude"]), float(x["Longitude"])
        ward_pt[(st, lg, wd)] = (lat, lon)
        lga_acc.setdefault((st, lg), []).append((lat, lon))
        st_acc.setdefault(st, []).append((lat, lon))

    def mean_ll(pts: list[tuple[float, float]]) -> tuple[float, float]:
        return (
            sum(p[0] for p in pts) / len(pts),
            sum(p[1] for p in pts) / len(pts),
        )

    lga_c = {k: mean_ll(v) for k, v in lga_acc.items()}
    st_c = {k: mean_ll(v) for k, v in st_acc.items()}
    return ward_pt, lga_c, st_c


def resolve_ward_seed_latlon(wkey: tuple[str, str, str]) -> tuple[float, float]:
    """Forensic anchor: temikeezy centroid → LGA mean → state mean → federation hub."""
    ward_pt, lga_c, st_c = _centroid_lookup_tables()
    if wkey in ward_pt:
        return ward_pt[wkey]
    st, lg, _ = wkey
    if (st, lg) in lga_c:
        return lga_c[(st, lg)]
    if st in st_c:
        return st_c[st]
    return 9.082, 8.675


def ward_token_from_pu_code(code: str) -> str:
    parts = str(code).strip().split("/")
    if len(parts) < 3:
        return ""
    return "/".join(parts[:3])


def golden_disk_positions(
    lat0: float,
    lon0: float,
    n: int,
    radius_deg: float,
) -> list[tuple[float, float]]:
    if n <= 0:
        return []
    golden_angle = math.pi * (3.0 - math.sqrt(5.0))
    out: list[tuple[float, float]] = []
    for i in range(n):
        rr = radius_deg * math.sqrt((i + 0.5) / max(n, 1))
        theta = i * golden_angle
        out.append((lat0 + rr * math.cos(theta), lon0 + rr * math.sin(theta)))
    return out


def _radius_deg_for_group(n: int, matched_ward: bool) -> float:
    base = 0.0038 if matched_ward else 0.012
    return min(0.14, base * math.sqrt(max(n, 1)))


def build_national_pu_geodataframe() -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Full federation lattice: 176,846 rows with deterministic lat/lon per PU code.
    Placement = golden disk around resolved ward/LGA/state centroid (CSV has no coords).
    """
    ward_pt, _, _ = _centroid_lookup_tables()

    df = pd.read_csv(CANONICAL_PU_CSV_URL)
    if len(df) != NATIONAL_PU_EXPECTED:
        raise RuntimeError(
            f"Canonical PU cardinality {len(df)} != expected {NATIONAL_PU_EXPECTED}"
        )

    df["wkey"] = list(zip(df["state"].map(_norm), df["lg"].map(_norm), df["ward"].map(_norm)))
    df["ward_token"] = df["code"].map(ward_token_from_pu_code)

    frames: list[pd.DataFrame] = []
    matched_wards = 0
    groups = df.groupby("wkey", sort=False)
    for wkey, g in groups:
        n = len(g)
        seed = resolve_ward_seed_latlon(wkey)
        matched = wkey in ward_pt
        if matched:
            matched_wards += 1
        rd = _radius_deg_for_group(n, matched)
        coords = golden_disk_positions(seed[0], seed[1], n, rd)
        gg = g.sort_values("code").reset_index(drop=True)
        gg["lat"] = [c[0] for c in coords]
        gg["lon"] = [c[1] for c in coords]
        frames.append(gg)

    out = pd.concat(frames, ignore_index=True)
    if len(out) != NATIONAL_PU_EXPECTED:
        raise RuntimeError("National PU lattice row count mismatch after group placement.")

    distinct_tokens = int(out["ward_token"].nunique())
    report = {
        "pu_rows": int(len(out)),
        "distinct_ward_tokens": distinct_tokens,
        "temikeezy_ward_key_matches": matched_wards,
        "canonical_url": CANONICAL_PU_CSV_URL,
        "ward_ref": WARD_REF_URL,
        "placement": "golden_disk_per_ward_cluster",
    }
    return out, report


def subset_pus_for_viewport(
    df: pd.DataFrame,
    bounds: tuple[float, float, float, float] | None,
    zoom: float | int | None,
    z_atom: int,
    max_pts: int = MAX_VIEWPORT_ATOMS,
) -> pd.DataFrame:
    """Return PU rows inside map bounds; empty if zoom below atom gate."""
    if bounds is None or zoom is None:
        return df.iloc[0:0].copy()
    try:
        zf = float(zoom)
    except (TypeError, ValueError):
        return df.iloc[0:0].copy()
    if zf < float(z_atom):
        return df.iloc[0:0].copy()

    south, west, north, east = bounds
    if south >= north or west >= east:
        return df.iloc[0:0].copy()

    sub = df[
        (df["lat"] >= south)
        & (df["lat"] <= north)
        & (df["lon"] >= west)
        & (df["lon"] <= east)
    ]
    if len(sub) <= max_pts:
        return sub.copy()

    step = max(len(sub) // max_pts, 1)
    return sub.iloc[::step].copy()


def parse_st_folium_bounds(b: Any) -> tuple[float, float, float, float] | None:
    if not isinstance(b, dict):
        return None
    sw = b.get("_southWest") or {}
    ne = b.get("_northEast") or {}
    try:
        south, west = float(sw["lat"]), float(sw["lng"])
        north, east = float(ne["lat"]), float(ne["lng"])
    except (KeyError, TypeError, ValueError):
        return None
    if south >= north or west >= east:
        return None
    return (south, west, north, east)


def parse_st_folium_zoom(z: Any) -> float | None:
    if z is None:
        return None
    if isinstance(z, dict):
        for k in ("level", "zoom", "_zoom"):
            if k in z and z[k] is not None:
                try:
                    return float(z[k])
                except (TypeError, ValueError):
                    continue
        return None
    try:
        return float(z)
    except (TypeError, ValueError):
        return None
