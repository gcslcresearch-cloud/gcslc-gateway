"""
Deep Join: 8,806 electoral wards ↔ 774 LGAs ↔ 36 states + FCT (programmatic spine).

Uses the same upstream LGA manifest as ``14314/data_engine`` with Kazaure injection.
Ward counts distribute the national 8,806 mandate across LGAs deterministically (sorted order).
© GCSLC. Proprietary.
"""

from __future__ import annotations

import hashlib
import json
import math
from typing import Any
from urllib.request import urlopen

import pandas as pd
import plotly.graph_objects as go

LGA_SOURCE_URL = (
    "https://raw.githubusercontent.com/favour121/nigerian-state-lgas/master/lgas.json"
)
LGA_MANUAL_INJECTIONS: list[dict[str, str]] = [
    {"state_code": "JI", "name": "Kazaure"},
]

# National ward mandate (INEC administrative lattice — consolidated target).
NATIONAL_WARD_TOTAL = 8_806
N_LGA_EXPECTED = 774

STATE_CODE_TO_STATE: dict[str, str] = {
    "AB": "Abia",
    "AD": "Adamawa",
    "AK": "Akwa Ibom",
    "AN": "Anambra",
    "BA": "Bauchi",
    "BY": "Bayelsa",
    "BE": "Benue",
    "BO": "Borno",
    "CR": "Cross River",
    "DE": "Delta",
    "EB": "Ebonyi",
    "ED": "Edo",
    "EK": "Ekiti",
    "EN": "Enugu",
    "FC": "FCT",
    "GO": "Gombe",
    "IM": "Imo",
    "JI": "Jigawa",
    "KD": "Kaduna",
    "KN": "Kano",
    "KT": "Katsina",
    "KE": "Kebbi",
    "KO": "Kogi",
    "KW": "Kwara",
    "LA": "Lagos",
    "NA": "Nasarawa",
    "NI": "Niger",
    "OG": "Ogun",
    "ON": "Ondo",
    "OS": "Osun",
    "OY": "Oyo",
    "PL": "Plateau",
    "RI": "Rivers",
    "SO": "Sokoto",
    "TA": "Taraba",
    "YO": "Yobe",
    "ZA": "Zamfara",
}

# Approximate centroids for Mapbox scatter (lat, lon) — aligned with RHGI engine.
STATE_COORDS: dict[str, tuple[float, float]] = {
    "Abia": (5.532, 7.482),
    "Adamawa": (9.326, 12.398),
    "Akwa Ibom": (4.905, 7.853),
    "Anambra": (6.210, 7.074),
    "Bauchi": (10.310, 9.843),
    "Bayelsa": (4.771, 6.070),
    "Benue": (7.190, 8.129),
    "Borno": (11.833, 13.151),
    "Cross River": (5.870, 8.598),
    "Delta": (5.500, 5.748),
    "Ebonyi": (6.325, 8.113),
    "Edo": (6.335, 5.603),
    "Ekiti": (7.623, 5.221),
    "Enugu": (6.441, 7.498),
    "FCT": (9.076, 7.398),
    "Gombe": (10.290, 11.171),
    "Imo": (5.492, 7.026),
    "Jigawa": (12.228, 9.561),
    "Kaduna": (10.510, 7.417),
    "Kano": (12.002, 8.592),
    "Katsina": (12.985, 7.601),
    "Kebbi": (12.450, 4.199),
    "Kogi": (7.800, 6.739),
    "Kwara": (8.494, 4.542),
    "Lagos": (6.524, 3.379),
    "Nasarawa": (8.499, 8.516),
    "Niger": (9.930, 5.598),
    "Ogun": (7.147, 3.361),
    "Ondo": (7.257, 5.205),
    "Osun": (7.587, 4.562),
    "Oyo": (7.377, 3.947),
    "Plateau": (9.896, 8.858),
    "Rivers": (4.815, 7.050),
    "Sokoto": (13.005, 5.247),
    "Taraba": (8.890, 11.360),
    "Yobe": (12.293, 11.439),
    "Zamfara": (12.122, 6.066),
}

# Abuja–Zaria–Kano “Million Steel Rods” pilot corridor (lat/lon waypoints).
AZK_CORRIDOR: tuple[tuple[float, float], ...] = (
    (9.0765, 7.3986),  # Abuja (FCT anchor)
    (11.0671, 7.7197),  # Zaria (Kaduna industrial belt)
    (12.0020, 8.5920),  # Kano
)

GOLD = "#D4AF37"
CYAN = "#00E5FF"
NAVY_DEEP = "#000022"


def _lga_sort_key(row: dict[str, Any]) -> tuple[str, str]:
    return (str(row["state_code"]), str(row["name"]))


def fetch_lga_catalog_raw() -> list[dict[str, Any]]:
    """Fetch upstream LGA JSON and apply Kazaure injection when missing."""
    with urlopen(LGA_SOURCE_URL, timeout=25) as resp:
        payload = resp.read().decode("utf-8")
    data: list[dict[str, Any]] = json.loads(payload)
    seen = {(str(x["state_code"]), str(x["name"])) for x in data}
    for row in LGA_MANUAL_INJECTIONS:
        key = (row["state_code"], row["name"])
        if key not in seen:
            data.append(dict(row))
            seen.add(key)
    data.sort(key=_lga_sort_key)
    return data


def attach_ward_counts(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Assign ward_count per LGA such that sum equals :data:`NATIONAL_WARD_TOTAL`."""
    n = len(rows)
    if n != N_LGA_EXPECTED:
        raise ValueError(f"Deep join expects {N_LGA_EXPECTED} LGAs, got {n}")
    base = NATIONAL_WARD_TOTAL // n
    rem = NATIONAL_WARD_TOTAL % n
    out: list[dict[str, Any]] = []
    for i, row in enumerate(rows):
        wc = base + (1 if i < rem else 0)
        st_name = STATE_CODE_TO_STATE[str(row["state_code"])]
        out.append(
            {
                **row,
                "state": st_name,
                "ward_count": wc,
                "join_index": i,
            }
        )
    return out


def verify_ward_total(rows: list[dict[str, Any]]) -> int:
    return int(sum(int(r["ward_count"]) for r in rows))


def _digest_seed(*parts: str) -> int:
    h = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()
    return int(h[:12], 16)


def lga_centroid_latlon(state: str, lga_name: str) -> tuple[float, float]:
    """Stable synthetic centroid per LGA near its state anchor (for map scatter)."""
    slat, slon = STATE_COORDS[state]
    seed = _digest_seed(state, lga_name)
    u1 = (seed % 10_000) / 10_000.0
    u2 = ((seed // 10_000) % 10_000) / 10_000.0
    dx = (u1 - 0.5) * 1.05
    dy = (u2 - 0.5) * 0.78
    # Contract offsets so points stay inside state-scale bounding visual.
    return slat + dy * 0.42, slon + dx * 0.42


def ward_offsets(i: int, n: int, scale: float = 0.028) -> tuple[float, float]:
    """Golden-angle micro spiral around an LGA centroid (degrees lat / lon-ish)."""
    golden = math.pi * (3.0 - math.sqrt(5.0))
    theta = i * golden
    r = scale * math.sqrt(float(i + 1)) / math.sqrt(float(max(n, 1)))
    return r * math.cos(theta), r * math.sin(theta)


def ward_latlon(state: str, lga_name: str, ward_idx: int, ward_count: int) -> tuple[float, float]:
    lat0, lon0 = lga_centroid_latlon(state, lga_name)
    dlat, dlon = ward_offsets(ward_idx, ward_count)
    # Correct east-west spacing by latitude.
    cl = math.cos(math.radians(lat0))
    cl = max(0.2, min(cl, 1.0))
    return lat0 + dlat, lon0 + dlon / cl


def catalog_to_dataframe(rows: list[dict[str, Any]]) -> pd.DataFrame:
    return pd.DataFrame(rows)


def lgas_in_state(df: pd.DataFrame, state: str) -> list[str]:
    sub = df.loc[df["state"] == state].sort_values("name")
    return [str(x) for x in sub["name"].tolist()]


def build_ward_points_for_lga(df: pd.DataFrame, state: str, lga_name: str) -> pd.DataFrame:
    row = df.loc[(df["state"] == state) & (df["name"] == lga_name)]
    if row.empty:
        return pd.DataFrame(columns=["ward_label", "lat", "lon", "state", "lga"])
    wc = int(row.iloc[0]["ward_count"])
    records = []
    for i in range(wc):
        lat, lon = ward_latlon(state, lga_name, i, wc)
        records.append(
            {
                "ward_label": f"{lga_name} · Ward {i + 1:02d}",
                "lat": lat,
                "lon": lon,
                "state": state,
                "lga": lga_name,
            }
        )
    return pd.DataFrame.from_records(records)


def build_ward_points_for_state(df: pd.DataFrame, state: str) -> pd.DataFrame:
    parts: list[pd.DataFrame] = []
    sub = df.loc[df["state"] == state]
    for _, r in sub.iterrows():
        parts.append(build_ward_points_for_lga(df, state, str(r["name"])))
    if not parts:
        return pd.DataFrame(columns=["ward_label", "lat", "lon", "state", "lga"])
    return pd.concat(parts, ignore_index=True)


def build_deep_join_figure(
    df: pd.DataFrame,
    *,
    selected_state: str | None,
    selected_lga: str | None,
    show_azk: bool = True,
) -> go.Figure:
    """Mapbox: federation nodes + optional AZK corridor + ward reveal by selection."""
    st_lat = [STATE_COORDS[s][0] for s in STATE_COORDS]
    st_lon = [STATE_COORDS[s][1] for s in STATE_COORDS]
    st_text = list(STATE_COORDS.keys())

    fig = go.Figure()

    if show_azk:
        az_lat = [p[0] for p in AZK_CORRIDOR]
        az_lon = [p[1] for p in AZK_CORRIDOR]
        fig.add_trace(
            go.Scattermapbox(
                lat=az_lat,
                lon=az_lon,
                mode="lines",
                line=dict(width=5, color="rgba(255, 215, 0, 0.95)"),
                name="AZK · Million Steel Rods",
                hoverinfo="text",
                hovertext="Abuja → Zaria → Kano · AZK corridor",
            )
        )
        fig.add_trace(
            go.Scattermapbox(
                lat=az_lat,
                lon=az_lon,
                mode="markers",
                marker=dict(size=10, color="rgba(255, 215, 0, 0.95)", symbol="circle-open"),
                showlegend=False,
                hoverinfo="skip",
            )
        )

    fig.add_trace(
        go.Scattermapbox(
            lat=st_lat,
            lon=st_lon,
            mode="markers+text",
            text=st_text,
            textposition="top center",
            textfont=dict(size=9, color="rgba(255,215,0,0.92)"),
            marker=dict(size=12, color="rgba(0, 229, 255, 0.72)"),
            name="36 States + FCT",
            hoverinfo="text",
            hovertext=[f"{s}<br>Sovereign federation anchor" for s in st_text],
        )
    )

    center_lat, center_lon, zoom = 9.05, 8.55, 5.2
    ward_df = pd.DataFrame()
    if selected_state and selected_lga:
        ward_df = build_ward_points_for_lga(df, selected_state, selected_lga)
        if not ward_df.empty:
            center_lat = float(ward_df["lat"].mean())
            center_lon = float(ward_df["lon"].mean())
            zoom = 10.5
    elif selected_state:
        ward_df = build_ward_points_for_state(df, selected_state)
        if not ward_df.empty:
            center_lat = float(ward_df["lat"].mean())
            center_lon = float(ward_df["lon"].mean())
            zoom = 7.85

    if not ward_df.empty:
        wlabs = ward_df["ward_label"].tolist()
        fig.add_trace(
            go.Scattermapbox(
                lat=ward_df["lat"],
                lon=ward_df["lon"],
                mode="markers",
                marker=dict(size=8, color="rgba(255, 215, 0, 0.92)"),
                hoverinfo="text",
                hovertext=wlabs,
                name="Ward lattice (reveal)",
            )
        )

    fig.update_layout(
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=center_lat, lon=center_lon),
            zoom=zoom,
            bearing=0,
            pitch=0,
        ),
        margin=dict(l=0, r=0, t=48, b=0),
        paper_bgcolor=NAVY_DEEP,
        plot_bgcolor=NAVY_DEEP,
        font=dict(family="Goldman, sans-serif", color=GOLD, size=11),
        title=dict(
            text="Deep Join · 8,806 Wards ↔ 774 LGAs ↔ 37 States · pinch-zoom / filter reveal",
            font=dict(size=13, color=GOLD),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=10, color=CYAN),
        ),
        height=520,
        hovermode="closest",
    )
    return fig


def state_options(df: pd.DataFrame) -> list[str]:
    return sorted(df["state"].unique().tolist())
