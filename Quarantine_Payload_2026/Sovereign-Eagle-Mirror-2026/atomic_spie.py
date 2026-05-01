"""
Atomic Spie — single-ward polling-unit spike (Phase 2 mirror scope only).

Canonical PU inventory (176,846 rows): scrapped IREV-derived open CSV with forensic
join keys carried in `code` (unique PU) and ward cluster from first three segments.

Placement: Emeka CSV has no lat/lon — Rigasa spike uses golden-angle disk around the
temikeezy ward centroid for deterministic lattice coordinates until national PU coords ship.
"""

from __future__ import annotations

import math
from typing import Any

import pandas as pd

CANONICAL_PU_CSV_URL = (
    "https://raw.githubusercontent.com/Emeka-Onwuepe/Polling_Units_in_Nigeria/main/"
    "Nigeria_polling_units.csv"
)

# AZK-adjacent spike: Kaduna · Igabi · Rigasa (electoral ward token 18/04/12)
SPIKE_STATE = "kaduna"
SPIKE_LGA = "igabi"
SPIKE_WARD = "rigasa"
SPIKE_EXPECTED_ROWS = 153
SPIKE_WARD_TOKEN_EXPECTED = "18/04/12"

# Referenced ward centroid (community geo inventory — not INEC geometry)
WARD_CENTROID_REF = {
    "source": "https://raw.githubusercontent.com/temikeezy/nigeria-geojson-data/"
    "main/data/wards.json",
    "state": "Kaduna",
    "lga": "Igabi",
    "ward": "Rigasa",
    "lat": 10.5213754,
    "lon": 7.316590247,
}


def ward_token_from_pu_code(code: str) -> str:
    """INE ward cluster: first three segments of PU `code` (state/lg/ward)."""
    parts = str(code).strip().split("/")
    if len(parts) < 3:
        return ""
    return "/".join(parts[:3])


def golden_disk_positions(
    lat0: float,
    lon0: float,
    n: int,
    radius_deg: float = 0.0065,
) -> list[tuple[float, float]]:
    """Deterministic quasi-uniform disk — sovereign lattice envelope around ward centroid."""
    if n <= 0:
        return []
    golden_angle = math.pi * (3.0 - math.sqrt(5.0))
    out: list[tuple[float, float]] = []
    for i in range(n):
        rr = radius_deg * math.sqrt((i + 0.5) / max(n, 1))
        theta = i * golden_angle
        out.append((lat0 + rr * math.cos(theta), lon0 + rr * math.sin(theta)))
    return out


def build_rigasa_spike_bundle() -> dict[str, Any]:
    """
    Filter canonical CSV to Rigasa · Igabi · Kaduna; validate ward token integrity (no orphans).
    """
    chunks: list[pd.DataFrame] = []
    for chunk in pd.read_csv(CANONICAL_PU_CSV_URL, chunksize=65536):
        m = (
            chunk["state"].astype(str).str.strip().str.lower().eq(SPIKE_STATE)
            & chunk["lg"].astype(str).str.strip().str.lower().eq(SPIKE_LGA)
            & chunk["ward"].astype(str).str.strip().str.lower().eq(SPIKE_WARD)
        )
        if bool(m.any()):
            chunks.append(chunk.loc[m].copy())

    if not chunks:
        raise RuntimeError("Atomic Spie: no rows matched Rigasa filter — upstream CSV drift.")

    df = pd.concat(chunks, ignore_index=True)
    df["ward_token"] = df["code"].map(ward_token_from_pu_code)
    utoks = df["ward_token"].unique().tolist()
    if len(utoks) != 1:
        raise RuntimeError(f"Atomic Spie: multiple ward tokens in Rigasa slice: {utoks}")
    if utoks[0] != SPIKE_WARD_TOKEN_EXPECTED:
        raise RuntimeError(
            f"Atomic Spie: ward token {utoks[0]} != expected {SPIKE_WARD_TOKEN_EXPECTED}"
        )
    if len(df) != SPIKE_EXPECTED_ROWS:
        raise RuntimeError(
            f"Atomic Spie: Rigasa row count {len(df)} != expected {SPIKE_EXPECTED_ROWS}"
        )

    df = df.sort_values("code").reset_index(drop=True)
    coords = golden_disk_positions(
        WARD_CENTROID_REF["lat"],
        WARD_CENTROID_REF["lon"],
        len(df),
    )
    df["lat"] = [c[0] for c in coords]
    df["lon"] = [c[1] for c in coords]

    report = {
        "ward_token": utoks[0],
        "pu_rows": int(len(df)),
        "orphan_rows": 0,
        "canonical_url": CANONICAL_PU_CSV_URL,
        "placement": "golden_disk",
        "centroid_ref": WARD_CENTROID_REF,
        "cod_note": (
            "COD HDX nga_admin3 layer (714 units) is not the electoral 8,806 ward set; "
            "ADM3_PCODE crosswalk to INEC ward_token is maintained at national rollout."
        ),
    }
    return {"frame": df, "report": report}
