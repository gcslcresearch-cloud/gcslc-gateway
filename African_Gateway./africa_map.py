"""
African Wealth Cloud (AWC) — The Sovereign Glass
Continental nodes: Nigeria, Ghana, South Africa, Egypt; Strategic Partner: Dubai (UAE).
Interactive map with regional sovereign pulses.

Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026 GCSLC. Proprietary.
"""

from typing import List, Tuple, Any, Optional, Dict

# GCSLC Sovereign palette
NAVY_DEEP = [0, 33, 71]
GCSLC_GOLD = [212, 175, 55]
GCSLC_GOLD_SHIMMER = [255, 215, 0]  # #FFD700
NIGERIA_GREEN = [0, 135, 81]
NIGERIA_WHITE = [255, 255, 255]
SOVEREIGN_PULSE_GREEN = [0, 135, 81]
GLITTER_GOLD = [255, 229, 92]

# Continental nodes: id -> { name, lat, lon, polygon (optional), pulse_type }
CONTINENTAL_NODES: Dict[str, Dict[str, Any]] = {
    "nigeria": {"name": "Nigeria", "lat": 8.0, "lon": 9.0, "pulse_type": "nigeria"},
    "ghana": {"name": "Ghana", "lat": 7.95, "lon": -1.02, "pulse_type": "ghana"},
    "south_africa": {"name": "South Africa", "lat": -29.0, "lon": 24.0, "pulse_type": "south_africa"},
    "egypt": {"name": "Egypt", "lat": 26.8, "lon": 30.8, "pulse_type": "egypt"},
    "dubai": {"name": "Dubai (UAE)", "lat": 25.2, "lon": 55.3, "pulse_type": "dubai", "strategic_partner": True},
}


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

# Simplified Ghana boundary (approx)
GHANA_POLYGON: List[Tuple[float, float]] = [
    (-3.25, 5.0), (-2.0, 5.0), (1.2, 6.0), (1.1, 11.2), (0.0, 11.0), (-3.0, 10.0), (-3.25, 5.0),
]

# Simplified South Africa boundary (approx)
SOUTH_AFRICA_POLYGON: List[Tuple[float, float]] = [
    (16.5, -22.0), (32.8, -22.0), (32.8, -26.8), (27.0, -33.0), (18.5, -34.8), (16.5, -22.0),
]

# Simplified Egypt boundary (approx)
EGYPT_POLYGON: List[Tuple[float, float]] = [
    (24.7, 22.0), (36.9, 22.0), (36.0, 31.6), (32.3, 31.4), (25.0, 31.5), (24.7, 22.0),
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
        "properties": {"name": "Nigeria", "iso": "NG", "node_id": "nigeria"},
        "geometry": _polygon_to_geojson(NIGERIA_POLYGON),
    }


def get_ghana_geojson() -> dict:
    """GeoJSON Feature for Ghana boundary."""
    return {
        "type": "Feature",
        "properties": {"name": "Ghana", "iso": "GH", "node_id": "ghana"},
        "geometry": _polygon_to_geojson(GHANA_POLYGON),
    }


def get_south_africa_geojson() -> dict:
    """GeoJSON Feature for South Africa boundary."""
    return {
        "type": "Feature",
        "properties": {"name": "South Africa", "iso": "ZA", "node_id": "south_africa"},
        "geometry": _polygon_to_geojson(SOUTH_AFRICA_POLYGON),
    }


def get_egypt_geojson() -> dict:
    """GeoJSON Feature for Egypt boundary."""
    return {
        "type": "Feature",
        "properties": {"name": "Egypt", "iso": "EG", "node_id": "egypt"},
        "geometry": _polygon_to_geojson(EGYPT_POLYGON),
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


def _node_fill_color(node_id: Optional[str], selected_node: Optional[str]) -> List[int]:
    """Return fill color [r,g,b,a] for a country layer; highlight when selected."""
    if node_id and node_id == selected_node:
        return GCSLC_GOLD_SHIMMER + [int(255 * 0.85)]
    return GCSLC_GOLD + [int(255 * 0.25)]


def build_africa_deck(
    selected_node: Optional[str] = None,
    nigeria_selected: Optional[bool] = None,
    opacity: float = 0.85,
    map_style: Optional[str] = None,
) -> Any:
    """
    Build a pydeck Deck: Africa outline + Nigeria, Ghana, South Africa, Egypt (GeoJSON),
    Dubai (UAE) Strategic Partner point, glitter. selected_node centers view and highlights that node.
    D7: update_triggers so map redraws only when GE snips (selected_node / data change).
    """
    try:
        import time
        import pydeck as pdk
        import pandas as pd
    except ImportError:
        return None
    if nigeria_selected is not None:
        selected_node = "nigeria" if nigeria_selected else None
    # GE snip bucket: map redraws only when this or selected_node changes (D7 thermal relief)
    snip_bucket = int(time.time() // 60)

    # Africa outline
    africa_layer = pdk.Layer(
        "GeoJsonLayer",
        [get_africa_geojson()],
        id="africa-outline",
        get_fill_color=GCSLC_GOLD + [int(255 * 0.15)],
        get_line_color=GCSLC_GOLD + [int(255 * opacity)],
        get_line_width=40,
        line_width_min_pixels=1,
        opacity=opacity,
        pickable=False,
        update_triggers={"get_fill_color": snip_bucket},
    )

    # Continental country layers (interactive)
    nigeria_layer = pdk.Layer(
        "GeoJsonLayer",
        [get_nigeria_geojson()],
        id="nigeria-sovereign",
        get_fill_color=_node_fill_color("nigeria", selected_node) + [int(255 * opacity)],
        get_line_color=GCSLC_GOLD_SHIMMER + [255],
        get_line_width=60,
        line_width_min_pixels=2,
        opacity=opacity,
        pickable=True,
        update_triggers={"get_fill_color": (selected_node or "", snip_bucket)},
    )
    ghana_layer = pdk.Layer(
        "GeoJsonLayer",
        [get_ghana_geojson()],
        id="ghana-node",
        get_fill_color=_node_fill_color("ghana", selected_node) + [int(255 * opacity)],
        get_line_color=GCSLC_GOLD_SHIMMER + [200],
        get_line_width=50,
        line_width_min_pixels=2,
        opacity=opacity,
        pickable=True,
        update_triggers={"get_fill_color": (selected_node or "", snip_bucket)},
    )
    south_africa_layer = pdk.Layer(
        "GeoJsonLayer",
        [get_south_africa_geojson()],
        id="south_africa-node",
        get_fill_color=_node_fill_color("south_africa", selected_node) + [int(255 * opacity)],
        get_line_color=GCSLC_GOLD_SHIMMER + [200],
        get_line_width=50,
        line_width_min_pixels=2,
        opacity=opacity,
        pickable=True,
        update_triggers={"get_fill_color": (selected_node or "", snip_bucket)},
    )
    egypt_layer = pdk.Layer(
        "GeoJsonLayer",
        [get_egypt_geojson()],
        id="egypt-node",
        get_fill_color=_node_fill_color("egypt", selected_node) + [int(255 * opacity)],
        get_line_color=GCSLC_GOLD_SHIMMER + [200],
        get_line_width=50,
        line_width_min_pixels=2,
        opacity=opacity,
        pickable=True,
        update_triggers={"get_fill_color": (selected_node or "", snip_bucket)},
    )

    # Dubai (UAE) — Strategic Partner node (point); D7: updateTriggers so redraw only on snip/selection
    dubai_df = pd.DataFrame([{"lon": CONTINENTAL_NODES["dubai"]["lon"], "lat": CONTINENTAL_NODES["dubai"]["lat"], "name": "Dubai (UAE) Strategic Partner"}])
    dubai_layer = pdk.Layer(
        "ScatterplotLayer",
        dubai_df,
        id="dubai-node",
        get_position=["lon", "lat"],
        get_radius=80000,
        get_fill_color=GCSLC_GOLD_SHIMMER + [255] if selected_node == "dubai" else GCSLC_GOLD + [200],
        get_line_color=GCSLC_GOLD_SHIMMER + [255],
        radius_min_pixels=12,
        radius_max_pixels=24,
        pickable=True,
        update_triggers={"get_fill_color": (selected_node or "", snip_bucket)},
    )

    # Glitter — D7: redraw only when GE snips (snip_bucket)
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
        update_triggers={"get_position": snip_bucket, "get_radius": snip_bucket},
    )

    # View: center on selected node for Eagle's Global Strike
    if selected_node and selected_node in CONTINENTAL_NODES:
        node = CONTINENTAL_NODES[selected_node]
        lat, lon = node["lat"], node["lon"]
        zoom = 3.5 if selected_node == "dubai" else 3.0
    else:
        lat, lon, zoom = 8.0, 9.0, 2.8
    view_state = pdk.ViewState(latitude=lat, longitude=lon, zoom=zoom, pitch=0, bearing=0)

    deck = pdk.Deck(
        layers=[africa_layer, nigeria_layer, ghana_layer, south_africa_layer, egypt_layer, dubai_layer, glitter_layer],
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
