"""
African Wealth Cloud (AWC) — The Sovereign Glass
Africa map renderer: 85% transparency, glitter effects, Nigeria Sovereign Pulse.

Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026 GCSLC. Proprietary.
"""

from typing import List, Tuple, Any, Optional

# GCSLC Sovereign palette
NAVY_DEEP = [0, 33, 71]
GCSLC_GOLD = [212, 175, 55]
GCSLC_GOLD_SHIMMER = [255, 215, 0]  # #FFD700
NIGERIA_GREEN = [0, 135, 81]
NIGERIA_WHITE = [255, 255, 255]
SOVEREIGN_PULSE_GREEN = [0, 135, 81]
GLITTER_GOLD = [255, 229, 92]

# Simplified Nigeria boundary (WGS84) — approximate polygon for map layer
# Order: closed polygon [lon, lat] per GeoJSON convention
NIGERIA_POLYGON: List[Tuple[float, float]] = [
    (2.69, 4.27),   # SW
    (5.90, 4.30),
    (8.50, 4.25),
    (9.60, 6.50),
    (12.00, 9.60),
    (13.90, 10.90),
    (14.68, 13.89),
    (13.50, 13.50),
    (11.70, 11.00),
    (10.40, 11.80),
    (8.90, 12.80),
    (7.00, 10.20),
    (5.30, 7.00),
    (3.40, 6.50),
    (2.69, 4.27),
]

# Africa continental outline (simplified) — key points for visual context
AFRICA_OUTLINE: List[Tuple[float, float]] = [
    (-17.5, 14.5), (11.0, 23.5), (43.0, 11.5), (51.2, 12.0),
    (40.5, -4.0), (30.5, -28.0), (20.0, -35.0), (14.0, -34.0),
    (10.0, -18.0), (-17.5, 14.5),
]


def _polygon_to_geojson(coords: List[Tuple[float, float]]) -> dict:
    """Convert [(lon, lat), ...] to GeoJSON Polygon geometry."""
    ring = [[c[0], c[1]] for c in coords]
    if ring[0] != ring[-1]:
        ring.append(ring[0])
    return {"type": "Polygon", "coordinates": [ring]}


def get_nigeria_geojson() -> dict:
    """GeoJSON Feature for Nigeria boundary."""
    return {
        "type": "Feature",
        "properties": {"name": "Nigeria", "iso": "NG"},
        "geometry": _polygon_to_geojson(NIGERIA_POLYGON),
    }


def get_africa_geojson() -> dict:
    """GeoJSON Feature for simplified Africa outline."""
    return {
        "type": "Feature",
        "properties": {"name": "Africa"},
        "geometry": _polygon_to_geojson(AFRICA_OUTLINE),
    }


def get_glitter_points(count: int = 80) -> List[dict]:
    """Generate scatter points for elegant glitter over the map (Africa/Nigeria region)."""
    import random
    random.seed(42)
    points = []
    for _ in range(count):
        # Spread over Africa and especially Nigeria
        lat = random.uniform(-35, 37)
        lon = random.uniform(-18, 52)
        # Bias toward Nigeria (approx 3–14°N, 3–15°E)
        if random.random() < 0.4:
            lat = random.uniform(4, 14)
            lon = random.uniform(3, 15)
        points.append({"lon": lon, "lat": lat, "size": random.uniform(0.5, 2.0)})
    return points


def build_africa_deck(
    nigeria_selected: bool = False,
    opacity: float = 0.85,
    map_style: Optional[str] = None,
) -> Any:
    """
    Build a pydeck Deck for the Sovereign Glass: Africa map at 85% transparency
    with glitter layer. When nigeria_selected is True, Nigeria is drawn with
    Sovereign Pulse colors (caller should apply Green-White-Green then GCSLC Gold via UI).
    """
    try:
        import pydeck as pdk
        import pandas as pd
    except ImportError:
        return None

    # Africa outline layer — 85% transparency, subtle stroke
    africa_feat = get_africa_geojson()

    africa_layer = pdk.Layer(
        "GeoJsonLayer",
        [africa_feat],
        id="africa-outline",
        get_fill_color=GCSLC_GOLD + [int(255 * 0.15)],  # very transparent fill
        get_line_color=GCSLC_GOLD + [int(255 * opacity)],
        get_line_width=40,
        line_width_min_pixels=1,
        opacity=opacity,
        pickable=False,
    )

    # Nigeria fill — When selected: pulse (Green→White→Green) is container CSS; fill settles to GCSLC Gold Shimmer (#FFD700)
    nigeria_feat = get_nigeria_geojson()
    fill_rgb = GCSLC_GOLD_SHIMMER if nigeria_selected else GCSLC_GOLD
    nigeria_layer = pdk.Layer(
        "GeoJsonLayer",
        [nigeria_feat],
        id="nigeria-sovereign",
        get_fill_color=fill_rgb + [int(255 * opacity)],
        get_line_color=GCSLC_GOLD_SHIMMER + [255],
        get_line_width=60,
        line_width_min_pixels=2,
        opacity=opacity,
        pickable=True,
    )

    # Glitter scatter layer
    glitter_df = pd.DataFrame(get_glitter_points())
    glitter_layer = pdk.Layer(
        "ScatterplotLayer",
        glitter_df,
        id="glitter",
        get_position=["lon", "lat"],
        get_radius="size",
        get_fill_color=GLITTER_GOLD + [int(255 * 0.9)],
        get_line_color=GCSLC_GOLD + [180],
        radius_min_pixels=1,
        radius_max_pixels=4,
        pickable=False,
    )

    view_state = pdk.ViewState(
        latitude=8.0,
        longitude=9.0,
        zoom=2.8,
        pitch=0,
        bearing=0,
    )

    deck = pdk.Deck(
        layers=[africa_layer, nigeria_layer, glitter_layer],
        initial_view_state=view_state,
        map_style=map_style or "light",
        tooltip={"text": "{name}"},
    )
    return deck


def get_glassmorphism_css() -> str:
    """
    CSS for 85% transparent Glassmorphism map container.
    Backdrop blur + semi-transparent fill for "frosted glass" effect.
    """
    return """
    .awc-map-glass {
        background: rgba(0, 26, 51, 0.15);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 215, 0, 0.25);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.08);
        opacity: 0.85;
    }
    """


def get_sovereign_pulse_css() -> str:
    """
    Sovereign Pulse: 3-second animation Green → White → Green,
    then transition to GCSLC Gold Shimmer (#FFD700) with glitter overlay.
    Apply to the map container when Nigeria is selected.
    """
    return """
    @keyframes sovereign-pulse {
        0%   { box-shadow: 0 0 24px #008751, 0 0 48px rgba(0,135,81,0.7); border-color: #008751; }
        33%  { box-shadow: 0 0 28px #ffffff, 0 0 56px rgba(255,255,255,0.6); border-color: #ffffff; }
        66%  { box-shadow: 0 0 24px #008751, 0 0 48px rgba(0,135,81,0.7); border-color: #008751; }
        100% { box-shadow: 0 0 32px #FFD700, 0 0 64px rgba(255,215,0,0.6); border-color: #FFD700; }
    }
    .sovereign-pulse-active {
        animation: sovereign-pulse 3s ease-in-out 1 forwards;
        border: 2px solid #FFD700;
        position: relative;
    }
    .sovereign-pulse-active::after {
        content: '';
        position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        pointer-events: none;
        border-radius: inherit;
        background: radial-gradient(circle at 30% 30%, rgba(255,215,0,0.12) 0%, transparent 50%),
                    radial-gradient(circle at 70% 70%, rgba(255,215,0,0.08) 0%, transparent 45%);
    }
    """
