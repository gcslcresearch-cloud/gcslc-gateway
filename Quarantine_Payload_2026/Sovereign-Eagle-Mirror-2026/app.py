"""
Sovereign Eagle Mirror 2026 — Initialization (clean slate).
Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026
"""

from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path

import folium
import pandas as pd
import requests
import streamlit as st

try:
    from streamlit_folium import st_folium
except ImportError:
    st_folium = None  # type: ignore[misc, assignment]
from branca.element import Element
from folium.map import CustomPane
from folium.plugins import AntPath, Fullscreen

from atomic_spie import (
    build_national_pu_geodataframe,
    parse_st_folium_bounds,
    parse_st_folium_zoom,
    subset_pus_for_viewport,
)
from gcslc_deep_join import NATIONAL_WARD_TOTAL, build_fused_catalog
from ng_connectivity import (
    GEOBOUNDARIES_API_NGA_ADM2,
    build_spine_table,
    fetch_geo_boundary_geojson,
    load_hdx_nga_geojson_zip_layers,
    prefer_hdx_or_geo_lga_geojson,
)

SHELL = "#000080"
GLASS = "rgba(255, 255, 255, 0.08)"
GOLD = "#D4AF37"
CYAN = "#00E5FF"
# Sovereign Heartbeat — LGA pulse (mandate)
GOLD_HEARTBEAT = "#BF953F"

BASE_DIR = Path(__file__).resolve().parent
COAL_NODES_JSON = BASE_DIR / "Part_02_Finance" / "data" / "coal_reserve_nodes.json"

# Mobile pinch drill-down: states → LGAs → wards + labels
ZOOM_LGA_EMERGE = 8
ZOOM_WARD_EMERGE = 11
ZOOM_WARD_LABELS = 12
# Pinch-to-atomize (Rigasa spike): cyan mist → solid nodes as zoom deepens
ZOOM_ATOM_EMERGE = 13

GEOBOUNDARIES_API_NGA_ADM1 = "https://www.geoboundaries.org/api/current/gbOpen/NGA/ADM1/"
# Abuja–Zaria–Kano pilot spine (“Million Steel Rods” corridor nodes)
AZK_CORRIDOR_NODES = [
    {"name": "Abuja FCT · Eagle Hub", "lat": 9.0765, "lon": 7.3986},
    {"name": "Keffi · Corridor Gate", "lat": 8.8467, "lon": 7.8736},
    {"name": "Kaduna · Steel Exchange", "lat": 10.5105, "lon": 7.4165},
    {"name": "Zaria · AZK Spine", "lat": 11.0676, "lon": 7.7107},
    {"name": "Kano · Northern Anchor", "lat": 12.0022, "lon": 8.5920},
]

st.set_page_config(
    page_title="Sovereign Eagle Mirror 2026",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def _tooltip_field(geojson: dict | None) -> str | None:
    if not geojson or not geojson.get("features"):
        return None
    props = geojson["features"][0].get("properties") or {}
    for key in ("shapeName", "shapeISO", "shapeGroup"):
        if key in props:
            return key
    return next(iter(props.keys()), None)


def _lga_tooltip_fc(lgas_fc: dict | None) -> folium.GeoJsonTooltip | None:
    if not lgas_fc or not lgas_fc.get("features"):
        return None
    p0 = lgas_fc["features"][0].get("properties") or {}
    if "ADM2_EN" in p0 and "ADM1_EN" in p0:
        return folium.GeoJsonTooltip(
            fields=["ADM2_EN", "ADM1_EN"], aliases=["LGA", "State"], sticky=True
        )
    if "shapeName" in p0 and "shapeGroup" in p0:
        return folium.GeoJsonTooltip(
            fields=["shapeName", "shapeGroup"],
            aliases=["LGA", "Boundary group"],
            sticky=True,
        )
    return None


@st.cache_data(ttl=86400, show_spinner="Mounting federation boundaries…")
def _load_nigeria_states_geojson() -> dict | None:
    """geoBoundaries gbOpen NGA ADM1 — resolves real GeoJSON (GitHub raw is Git LFS)."""
    try:
        meta = requests.get(GEOBOUNDARIES_API_NGA_ADM1, timeout=45).json()
        url = meta.get("gjDownloadURL")
        if not url:
            return None
        res = requests.get(url, timeout=180, allow_redirects=True)
        res.raise_for_status()
        return res.json()
    except Exception:
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def _load_fused_lga_ward_partition() -> pd.DataFrame:
    return build_fused_catalog()


@st.cache_data(ttl=86400, show_spinner=False)
def _coal_asset_state_names() -> frozenset[str]:
    if not COAL_NODES_JSON.is_file():
        return frozenset()
    data = json.loads(COAL_NODES_JSON.read_text(encoding="utf-8"))
    return frozenset(str(n.get("state", "")).strip() for n in data.get("nodes", []) if n.get("state"))


@st.cache_data(
    ttl=604800,
    show_spinner="Loading HDX COD administrative bundle + LGA ADM2…",
)
def _load_phase2_spine_bundle() -> dict:
    gb_lgas = fetch_geo_boundary_geojson(GEOBOUNDARIES_API_NGA_ADM2)
    hdx = load_hdx_nga_geojson_zip_layers()
    wards_fc = hdx.get("wards")
    lgas_fc = prefer_hdx_or_geo_lga_geojson(hdx.get("lgas"), gb_lgas)
    spine_df, spine_report = build_spine_table(wards_fc)
    return {
        "wards_fc": wards_fc,
        "lgas_fc": lgas_fc,
        "hdx": hdx,
        "spine_df": spine_df,
        "spine_report": spine_report,
    }


@st.cache_data(ttl=86400, show_spinner="National atomic lattice — 176,846 PU…")
def _national_pu_frame_cached() -> tuple[pd.DataFrame, dict]:
    df, rep = build_national_pu_geodataframe()
    return df, rep


def _atomic_viewport_feature_group(viewport_df: pd.DataFrame) -> folium.FeatureGroup:
    """GeoJSON-per-ward data model; one FeatureGroup = current viewport batch (mobile screen)."""
    fg = folium.FeatureGroup(
        name=f"176,846 PU · viewport ({len(viewport_df):,} shown)",
    )
    if viewport_df is None or len(viewport_df) == 0:
        return fg
    for _, row in viewport_df.iterrows():
        loc = str(row.get("location", ""))[:180]
        folium.CircleMarker(
            location=[float(row["lat"]), float(row["lon"])],
            radius=3,
            pane="atomicLattice",
            color=CYAN,
            weight=1,
            fill=True,
            fillColor=CYAN,
            fillOpacity=0.28,
            opacity=0.48,
            className="gcslc-atom-node",
            tooltip=folium.Tooltip(f"{row['code']} · {loc}", sticky=True),
        ).add_to(fg)
    return fg


def _ward_style_with_asset(
    feature: dict,
    asset_states: frozenset[str],
) -> dict:
    p = feature.get("properties") or {}
    stn = (p.get("ADM1_EN") or p.get("adm1_en") or "").strip()
    is_asset = stn in asset_states
    if is_asset:
        return {
            "color": CYAN,
            "weight": 1.15,
            "fillColor": CYAN,
            "fillOpacity": 0.06,
            "opacity": 0.75,
            "className": "gcslc-ward-eightrec-asset leaflet-interactive",
        }
    return {
        "color": CYAN,
        "weight": 0.9,
        "fillColor": CYAN,
        "fillOpacity": 0.02,
        "opacity": 0.55,
        "className": "gcslc-ward-base leaflet-interactive",
    }


def _inject_drill_panes_atomic_fps(
    m: folium.Map,
    z_lga: int,
    z_ward: int,
    z_atom: int,
    has_atomic: bool,
) -> None:
    """Pinch tiers + Atom pane + RAF FPS HUD (desktop / mobile glass reference)."""
    mn = m.get_name()
    atom_js = "1" if has_atomic else "0"
    m.get_root().html.add_child(
        Element(
            f"""
<script>
(function() {{
  var zL = {int(z_lga)}, zW = {int(z_ward)}, zA = {int(z_atom)};
  var hasAtom = {atom_js} === "1";
  function arm() {{
    var mp = window["{mn}"];
    if (!mp || !mp.getPane) {{ requestAnimationFrame(arm); return; }}
    var ps = mp.getPane("federationStates");
    var pl = mp.getPane("lgaHeartbeat");
    var pw = mp.getPane("wardReveal");
    var pa = hasAtom ? mp.getPane("atomicLattice") : null;
    if (!ps || !pl || !pw) {{ requestAnimationFrame(arm); return; }}
    if (hasAtom && !pa) {{ requestAnimationFrame(arm); return; }}
    [pl, pw].forEach(function(p) {{
      p.style.transition = "opacity 0.45s cubic-bezier(0.33,1,0.68,1)";
    }});
    if (pa) {{
      pa.style.transition = "opacity 0.5s cubic-bezier(0.33,1,0.68,1)";
    }}
    var root = mp.getContainer();
    var hud = document.createElement("div");
    hud.setAttribute("aria-hidden", "true");
    hud.style.cssText = "position:absolute;bottom:10px;left:10px;z-index:900;font-size:11px;font-weight:700;padding:6px 10px;border-radius:8px;pointer-events:none;background:rgba(0,0,128,0.88);color:#00E5FF;border:1px solid #BF953F;box-shadow:0 2px 10px rgba(0,0,0,0.45);";
    hud.textContent = "FPS · …";
    root.appendChild(hud);
    var fc = 0, lt = performance.now(), fpsVal = 0;
    function fpsLoop(t) {{
      fc++;
      if (t - lt >= 1000) {{ fpsVal = fc; fc = 0; lt = t; }}
      requestAnimationFrame(fpsLoop);
    }}
    requestAnimationFrame(fpsLoop);
    function atomMist(z) {{
      if (!hasAtom || !pa || pa.style.opacity === "0") return;
      var t = Math.min(1, Math.max(0, (z - zA) / 4.5));
      var op = 0.18 + t * 0.78;
      var rpx = 2 + t * 7;
      var sw = 0.6 + t * 1.8;
      var nodes = root.querySelectorAll("circle.gcslc-atom-node, path.gcslc-atom-node");
      for (var i = 0; i < nodes.length; i++) {{
        var p = nodes[i];
        if (p.tagName.toLowerCase() === "circle") {{
          p.setAttribute("r", rpx);
          p.setAttribute("stroke-width", sw);
          p.setAttribute("stroke-opacity", op);
          p.setAttribute("fill-opacity", op * 0.85);
        }}
      }}
    }}
    function sync() {{
      var z = mp.getZoom();
      pl.style.opacity = (z >= zL) ? "1" : "0";
      pl.style.pointerEvents = (z >= zL) ? "auto" : "none";
      pw.style.opacity = (z >= zW) ? "1" : "0";
      pw.style.pointerEvents = (z >= zW) ? "auto" : "none";
      ps.style.opacity = "1";
      if (pa) {{
        pa.style.opacity = (z >= zA) ? "1" : "0";
        pa.style.pointerEvents = (z >= zA) ? "auto" : "none";
      }}
      atomMist(z);
      hud.textContent = "FPS · " + fpsVal + " · z " + z.toFixed(1) + " · Atom ≥" + zA;
    }}
    mp.on("zoomend", sync);
    mp.on("zoom", sync);
    mp.on("moveend", sync);
    sync();
  }}
  arm();
}})();
</script>
"""
        )
    )


def _build_federation_map(
    states_geojson: dict | None,
    phase2: dict | None,
    asset_states: frozenset[str],
) -> folium.Map:
    center_lat = sum(n["lat"] for n in AZK_CORRIDOR_NODES) / len(AZK_CORRIDOR_NODES)
    center_lon = sum(n["lon"] for n in AZK_CORRIDOR_NODES) / len(AZK_CORRIDOR_NODES)

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=6,
        tiles=None,
        width="100%",
        height="800px",
        prefer_canvas=False,
        zoom_control=True,
    )

    CustomPane("federationStates", z_index=380, pointer_events=True).add_to(m)
    CustomPane("lgaHeartbeat", z_index=430, pointer_events=True).add_to(m)
    CustomPane("wardReveal", z_index=468, pointer_events=False).add_to(m)
    CustomPane("atomicLattice", z_index=490, pointer_events=True).add_to(m)
    # AZK Million Steel Rods — always above atomic cyan mist (national PU viewport layer)
    CustomPane("azkSpine", z_index=620, pointer_events=False).add_to(m)

    folium.TileLayer(
        tiles="CartoDB dark_matter",
        attr="© OpenStreetMap © CARTO · Sovereign Navy basemap",
        name="Sovereign Navy · Dark Matter",
        overlay=False,
        control=True,
    ).add_to(m)

    pulse_css = """
@keyframes gcs-sovereign-heartbeat {
  0%, 100% {
    stroke: #BF953F;
    stroke-opacity: 0.42;
    stroke-width: 1.1px;
    fill-opacity: 0.03;
    filter: brightness(1) drop-shadow(0 0 1px rgba(191,149,63,0.35));
  }
  50% {
    stroke: #FFF8DC;
    stroke-opacity: 0.82;
    stroke-width: 2.05px;
    fill-opacity: 0.09;
    filter: brightness(1.28) drop-shadow(0 0 5px rgba(191,149,63,0.45));
  }
}
path.gcslc-lga-sovereign-heartbeat {
  animation: gcs-sovereign-heartbeat 10.25s ease-in-out infinite !important;
  stroke-linejoin: round !important;
  stroke-linecap: round !important;
  transform: translateZ(0);
}
@keyframes gcs-eightrec-aura {
  0%, 100% { stroke-opacity: 0.72; filter: drop-shadow(0 0 4px rgba(0,229,255,0.35)); }
  50% { stroke-opacity: 1; filter: drop-shadow(0 0 14px rgba(0,229,255,0.65)); }
}
path.gcslc-ward-eightrec-asset {
  animation: gcs-eightrec-aura 3.2s ease-in-out infinite !important;
}
path.gcslc-ward-base:hover, path.gcslc-ward-eightrec-asset:hover {
  stroke: #FFFFFF !important;
  stroke-width: 2px !important;
}
.leaflet-tooltip.gcs-ward-lbl {
  background: rgba(0,0,128,0.94) !important;
  color: #F8FAFC !important;
  border: 1px solid #BF953F !important;
  font-weight: 700 !important;
  font-size: 10px !important;
  text-shadow: 0 1px 2px #000;
  box-shadow: 0 2px 8px rgba(0,0,0,0.55) !important;
}
@media (prefers-reduced-motion: reduce) {
  path.gcslc-lga-sovereign-heartbeat, path.gcslc-ward-eightrec-asset { animation: none !important; }
}
path.gcslc-atom-node {
  transition: fill-opacity 0.35s ease, stroke-opacity 0.35s ease;
}
"""
    m.get_root().header.add_child(
        Element(
            f"<style>"
            f".leaflet-container{{background:{SHELL}!important;}}"
            f".leaflet-tile-pane img,.leaflet-tile-pane canvas{{opacity:0.85!important;}}"
            f".leaflet-control-attribution{{background:rgba(0,0,128,0.72)!important;"
            f"color:{GOLD}!important;font-size:10px!important;}}"
            f"{pulse_css}"
            f"</style>"
        )
    )

    fg_spine = folium.FeatureGroup(name="37 · States + FCT (country scale)").add_to(m)
    field = _tooltip_field(states_geojson)
    if states_geojson and states_geojson.get("features"):
        tt = (
            folium.GeoJsonTooltip(
                fields=[field],
                aliases=["State / Territory"],
                sticky=True,
            )
            if field
            else None
        )
        folium.GeoJson(
            states_geojson,
            pane="federationStates",
            style_function=lambda _f: {
                "fillColor": "transparent",
                "color": CYAN,
                "weight": 1,
                "opacity": 0.5,
                "fillOpacity": 0,
            },
            highlight_function=lambda _f: {
                "weight": 2,
                "color": GOLD,
                "opacity": 0.95,
                "fillOpacity": 0.1,
                "fillColor": GOLD,
            },
            tooltip=tt,
        ).add_to(fg_spine)

    if phase2:
        lgas_fc = phase2.get("lgas_fc")
        fg_lga = folium.FeatureGroup(name="774 LGAs · Sovereign Heartbeat").add_to(m)
        if lgas_fc and lgas_fc.get("features"):
            folium.GeoJson(
                lgas_fc,
                pane="lgaHeartbeat",
                style_function=lambda _f: {
                    "color": GOLD_HEARTBEAT,
                    "weight": 1.15,
                    "fillColor": GOLD_HEARTBEAT,
                    "fillOpacity": 0.045,
                    "opacity": 0.62,
                    "className": "gcslc-lga-sovereign-heartbeat leaflet-interactive",
                },
                highlight_function=lambda _f: {
                    "weight": 2.4,
                    "color": "#FFF8DC",
                    "opacity": 0.98,
                    "fillOpacity": 0.11,
                    "fillColor": "#FFF8DC",
                },
                tooltip=_lga_tooltip_fc(lgas_fc),
            ).add_to(fg_lga)

        wards_fc = phase2.get("wards_fc")
        fg_ward = folium.FeatureGroup(name="8,806 Wards · HDX spine + 8REC asset aura").add_to(
            m
        )
        if wards_fc and wards_fc.get("features"):
            w0 = wards_fc["features"][0].get("properties") or {}
            tip_fields = [k for k in ("ADM3_EN", "ADM2_EN", "ADM1_EN") if k in w0]
            tip = (
                folium.GeoJsonTooltip(
                    fields=tip_fields,
                    aliases=["Ward", "LGA", "State"][: len(tip_fields)],
                    sticky=True,
                )
                if tip_fields
                else None
            )
            folium.GeoJson(
                wards_fc,
                pane="wardReveal",
                style_function=lambda f: _ward_style_with_asset(f, asset_states),
                highlight_function=lambda _f: {
                    "weight": 2.2,
                    "color": "#FFFFFF",
                    "opacity": 1,
                    "fillOpacity": 0.12,
                },
                tooltip=tip,
                smooth_factor=0.5,
            ).add_to(fg_ward)

    fg_azk = folium.FeatureGroup(name="AZK · Million Steel Rods").add_to(m)
    azk_ll = [[n["lat"], n["lon"]] for n in AZK_CORRIDOR_NODES]

    folium.PolyLine(
        azk_ll,
        color=GOLD,
        weight=14,
        opacity=0.12,
        smooth_factor=1,
        pane="azkSpine",
    ).add_to(fg_azk)
    for i in range(-4, 5):
        if i == 0:
            continue
        off = i * 0.018
        shifted = [[p[0] + off * 0.4, p[1] + off * 0.55] for p in azk_ll]
        folium.PolyLine(
            shifted,
            color=GOLD,
            weight=2,
            opacity=0.2 + abs(i) * 0.025,
            smooth_factor=1,
            pane="azkSpine",
        ).add_to(fg_azk)

    AntPath(
        locations=azk_ll,
        color=GOLD,
        weight=5,
        opacity=0.92,
        delay=480,
        dash_array=[16, 22],
        pane="azkSpine",
    ).add_to(fg_azk)

    for node in AZK_CORRIDOR_NODES:
        folium.CircleMarker(
            location=[node["lat"], node["lon"]],
            radius=9,
            color=CYAN,
            weight=2,
            fill=True,
            fill_color=GOLD,
            fill_opacity=0.88,
            popup=folium.Popup(node["name"], max_width=240),
            pane="azkSpine",
        ).add_to(fg_azk)

    Fullscreen(
        position="topright",
        title="Full screen (mobile)",
        title_cancel="Exit full screen",
    ).add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    _inject_drill_panes_atomic_fps(
        m,
        ZOOM_LGA_EMERGE,
        ZOOM_WARD_EMERGE,
        ZOOM_ATOM_EMERGE,
        True,
    )
    return m


# --- Viewport: 1:1 scaling for mobile (injected into parent document) ---
st.components.v1.html(
    """
<script>
(function(){
  try {
    var p = window.parent.document;
    if (!p.getElementById('mirror-viewport-meta')) {
      var m = p.createElement('meta');
      m.id = 'mirror-viewport-meta';
      m.name = 'viewport';
      m.content = 'width=device-width, initial-scale=1.0, maximum-scale=5.0, viewport-fit=cover';
      p.head.appendChild(m);
    }
  } catch (e) {}
})();
(function gcslcFullCanvasResize(){
  var topWin = window;
  try { if (window.top) topWin = window.top; } catch (e0) {}
  function pulseResize(){
    try { topWin.dispatchEvent(new Event('resize')); } catch (e1) {}
    try {
      var doc = topWin.document;
      var ifr = doc.querySelectorAll('iframe');
      for (var i = 0; i < ifr.length; i++) {
        try {
          var w = ifr[i].contentWindow;
          if (w) w.dispatchEvent(new Event('resize'));
        } catch (e2) {}
      }
    } catch (e3) {}
  }
  topWin.addEventListener('orientationchange', function(){ setTimeout(pulseResize, 380); });
  topWin.addEventListener('resize', function(){ setTimeout(pulseResize, 120); });
})();
</script>
""",
    height=0,
    width=0,
)

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap');
/* Kill default Streamlit lavender / theme tint — anchor Eagle Cloud navy everywhere */
html, body {{
  background-color: {SHELL} !important;
  background-image: none !important;
  min-height: 100vh;
}}
.stApp {{
  background-color: {SHELL} !important;
  background-image: none !important;
  color: #f0f4ff !important;
  --background-color: {SHELL} !important;
  --secondary-background-color: {SHELL} !important;
  font-family: 'Goldman', sans-serif !important;
}}
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > section,
[data-testid="stAppViewContainer"] section.main,
section.main,
div.main {{
  background-color: {SHELL} !important;
  background-image: none !important;
}}
[data-testid="block-container"],
[data-testid="stVerticalBlockBorderWrapper"],
.stMainBlockContainer,
[data-testid="stMain"] {{
  background-color: {SHELL} !important;
  background-image: none !important;
}}
[data-testid="stBottomBlockContainer"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] {{
  background-color: {SHELL} !important;
  background: {SHELL} !important;
}}
[data-testid="stHeader"] {{
  background-color: {SHELL} !important;
  background: {SHELL} !important;
}}
[data-testid="stSidebar"] {{
  background-color: {SHELL} !important;
}}
.handshake-wrap {{
  font-family: 'Goldman', sans-serif !important;
  text-align: center;
  padding: 1.25rem 0.75rem 1.5rem;
  touch-action: manipulation;
}}
.layer-typewriter {{
  font-weight: 700;
  font-size: clamp(0.85rem, 2.8vw, 1.15rem);
  color: {CYAN} !important;
  letter-spacing: 0.04em;
  line-height: 1.45;
  min-height: 3.2em;
  text-shadow:
    0 0 1px rgba(0, 0, 0, 0.95),
    0 2px 6px rgba(0, 0, 0, 0.9),
    0 0 18px rgba(0, 0, 0, 0.55),
    0 0 2px rgba(0, 0, 128, 0.9) !important;
}}
.layer-rc {{
  font-weight: 700;
  font-size: clamp(1rem, 3.2vw, 1.35rem);
  color: {GOLD} !important;
  margin-top: 1rem;
  animation: mirror-pulse-zoom 2.4s ease-in-out infinite;
  text-shadow:
    0 0 1px rgba(0, 0, 0, 0.95),
    0 2px 8px rgba(0, 0, 0, 0.88),
    0 0 14px rgba(0, 0, 0, 0.5) !important;
}}
.layer-manifesto {{
  margin-top: 1.25rem;
  font-size: clamp(0.8rem, 2.4vw, 1rem);
  line-height: 1.5;
  font-weight: 700;
  background: linear-gradient(90deg, #001a4d 0%, {GOLD} 35%, #FFE566 50%, {GOLD} 65%, #001a4d 100%);
  background-size: 220% auto;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent !important;
  animation: mirror-manifesto-shimmer 5s linear infinite;
}}
@keyframes mirror-pulse-zoom {{
  0%, 100% {{ transform: scale(1); filter: brightness(1); }}
  50% {{ transform: scale(1.06); filter: brightness(1.25); }}
}}
@keyframes mirror-manifesto-shimmer {{
  0% {{ background-position: 0% 50%; }}
  100% {{ background-position: 200% 50%; }}
}}
/* Map Lux (frost + metallic rim + tam) is inlined in the st.components iframe — see _MAP_GLASS_HTML */
.mirror-phase-panel {{
  border: 1px solid rgba(212, 175, 55, 0.45);
  border-radius: 12px;
  padding: 12px 14px;
  background: rgba(255, 255, 255, 0.04);
  margin-bottom: 10px;
  touch-action: manipulation !important;
}}
h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown,
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
  font-family: 'Goldman', sans-serif !important;
}}
h1, h2, h3, h4, h5, h6 {{
  color: {GOLD} !important;
  text-shadow:
    0 0 1px rgba(0, 0, 0, 0.9),
    0 2px 6px rgba(0, 0, 0, 0.85) !important;
}}
[data-testid="stMetricValue"] {{
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.75) !important;
}}
[data-testid="stTabs"] {{
  background-color: {SHELL} !important;
}}
[data-testid="stTabs"] [data-baseweb="tab-list"] {{
  background-color: rgba(0, 0, 128, 0.35) !important;
}}
[data-baseweb="tab-panel"] {{
  background-color: {SHELL} !important;
}}
.footer-sovereign {{
  text-align: center;
  padding: 1rem 0.5rem 2rem;
  font-family: 'Goldman', sans-serif !important;
  font-size: 0.72rem;
  letter-spacing: 0.06em;
  color: rgba(212, 175, 55, 0.55) !important;
}}
/* Full-canvas Folium host — fluid width + viewport height (MacBook / iPhone) */
.gcslc-map-canvas-host {{
  width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
}}
.gcslc-map-canvas-host iframe,
iframe[title*="folium"],
iframe[title*="streamlit_folium"] {{
  width: 100% !important;
  min-height: min(800px, 92vh) !important;
  height: min(800px, 92vh) !important;
  min-height: min(800px, 92dvh) !important;
  height: min(800px, 92dvh) !important;
  max-height: none !important;
  touch-action: manipulation !important;
  border-radius: 14px !important;
  border: 2px solid rgba(212, 175, 55, 0.38) !important;
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.38) !important;
  background: {SHELL} !important;
  display: block !important;
  vertical-align: top !important;
}}
[data-testid="stIFrame"] {{
  width: 100% !important;
  min-height: min(800px, 92vh) !important;
  min-height: min(800px, 92dvh) !important;
}}
/* Sovereign Detail Widget — record strip below the vigil */
.sovereign-detail-widget {{
  margin-top: 14px;
  margin-bottom: 8px;
  padding: 14px 18px;
  border-radius: 14px;
  border: 1px solid rgba(212, 175, 55, 0.42);
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.22), 0 6px 24px rgba(0, 0, 0, 0.28);
  touch-action: manipulation;
}}
.sovereign-detail-widget .sdw-metrics {{
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: stretch;
  gap: 12px 16px;
}}
.sovereign-detail-widget .sdw-metric {{
  flex: 1 1 120px;
  text-align: center;
  padding: 8px 10px;
  border-radius: 10px;
  background: rgba(0, 0, 128, 0.35);
  border: 1px solid rgba(212, 175, 55, 0.22);
}}
.sovereign-detail-widget .sdw-metric-val {{
  font-size: clamp(1.1rem, 3.5vw, 1.45rem);
  font-weight: 700;
  color: {GOLD} !important;
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.65);
}}
.sovereign-detail-widget .sdw-metric-lbl {{
  font-size: clamp(0.62rem, 1.8vw, 0.72rem);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: rgba(240, 244, 255, 0.82) !important;
  margin-top: 4px;
}}
.sovereign-detail-widget .sdw-meta {{
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px solid rgba(212, 175, 55, 0.2);
  font-size: clamp(0.68rem, 2vw, 0.78rem);
  line-height: 1.45;
  color: rgba(240, 244, 255, 0.78) !important;
}}
.block-container {{
  max-width: 100% !important;
  padding-top: 0.35rem !important;
  padding-left: 0.35rem !important;
  padding-right: 0.35rem !important;
}}
</style>
""",
    unsafe_allow_html=True,
)

# --- Layer 1–3: Handshake (typewriter + pulse + manifesto via single animated HTML host) ---
_HANDSHAKE_HTML = """
<link href="https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap" rel="stylesheet">
<style>
.hroot { font-family: 'Goldman', sans-serif; text-align: center; padding: 8px 6px 16px; color: #D4AF37;
  background: #000080; }
.tw-line { color: #00E5FF !important; font-weight: 700; font-size: clamp(11px, 2.8vw, 15px); letter-spacing: 0.03em; min-height: 4.5em; line-height: 1.45;
  text-shadow: 0 0 1px rgba(0,0,0,0.95), 0 2px 6px rgba(0,0,0,0.9), 0 0 16px rgba(0,0,0,0.45); }
.rc-line { margin-top: 14px; font-weight: 700; font-size: clamp(13px, 3.2vw, 17px); color: #D4AF37 !important;
  animation: pz 2.4s ease-in-out infinite;
  text-shadow: 0 0 1px rgba(0,0,0,0.95), 0 2px 8px rgba(0,0,0,0.88); }
@keyframes pz { 0%,100%{ transform: scale(1); } 50%{ transform: scale(1.07); } }
.man-line { margin-top: 16px; font-weight: 700; font-size: clamp(10px, 2.4vw, 13px); line-height: 1.55;
  background: linear-gradient(90deg,#001a4d,#D4AF37,#FFE566,#D4AF37,#001a4d); background-size: 220% auto;
  -webkit-background-clip: text; background-clip: text; color: transparent;
  animation: sh 5s linear infinite; }
@keyframes sh { 0%{background-position:0% 50%} 100%{background-position:200% 50%} }
</style>
<div class="hroot">
  <div class="tw-line" id="tw-out"></div>
  <div class="rc-line" id="rc-out" style="opacity:0;">Galadiman Ruwa Nigeria Ltd RC 1871418</div>
  <div class="man-line" id="man-out" style="opacity:0;">Proponent of 8R Paradigm Convergence and its Determinants—come in for you to decode and understand.</div>
</div>
<script>
(function(){
  var full = "Goldman Ruwa Center for Strategic Leadership and Communication GCSLC LTD/GTE";
  var el = document.getElementById("tw-out");
  var rc = document.getElementById("rc-out");
  var mn = document.getElementById("man-out");
  var i = 0;
  var slow = 95;
  function tick(){
    if (i <= full.length) {
      el.textContent = full.slice(0, i);
      i++;
      setTimeout(tick, slow);
    } else {
      setTimeout(function(){ rc.style.opacity = "1"; rc.style.transition = "opacity 1.2s ease"; }, 400);
      setTimeout(function(){ mn.style.opacity = "1"; mn.style.transition = "opacity 1.4s ease"; }, 2200);
    }
  }
  tick();
})();
</script>
"""

st.components.v1.html(_HANDSHAKE_HTML, height=220)

_states_geojson = _load_nigeria_states_geojson()
_phase2 = _load_phase2_spine_bundle()
_asset_states = _coal_asset_state_names()

_fuse_caption = ""
try:
    _fused = _load_fused_lga_ward_partition()
    _fuse_ok = len(_fused) == 774 and int(_fused["ward_count"].sum()) == NATIONAL_WARD_TOTAL
    _fuse_caption = (
        f"gcslc_deep_join · {_fused.shape[0]} LGAs · Σ wards "
        f"{int(_fused['ward_count'].sum()):,} · {'CHECKSUM LOCKED' if _fuse_ok else 'CHECKSUM REVIEW'}"
    )
except Exception:
    _fuse_caption = "gcslc_deep_join manifest unreachable — HDX spine still mounts when online."

_spine = _phase2["spine_report"]
_spine_caption = ""
if _spine.get("ward_rows"):
    _spine_caption = (
        f"HDX spine · {_spine['ward_rows']} ward rows · {_spine.get('distinct_lgas')} LGA facets · "
        f"{_spine.get('distinct_states')} state facets · {'VALID' if _spine.get('valid') else 'REVIEW'}"
    )

_nat_err = ""
try:
    _national_df, _nat_rep = _national_pu_frame_cached()
except Exception as _nat_exc:
    _national_df = None
    _nat_rep = {}
    _nat_err = str(_nat_exc)

_map_prev = st.session_state.get("gv_map_out") or {}
_bounds = parse_st_folium_bounds(_map_prev.get("bounds"))
_zoom_ui = parse_st_folium_zoom(_map_prev.get("zoom"))

_viewport_df = pd.DataFrame()
if _national_df is not None:
    _viewport_df = subset_pus_for_viewport(
        _national_df,
        _bounds,
        _zoom_ui,
        ZOOM_ATOM_EMERGE,
    )

_federation_map = _build_federation_map(_states_geojson, _phase2, _asset_states)
_fg_atom = _atomic_viewport_feature_group(_viewport_df)

if st_folium is None:
    st.error(
        "Install streamlit-folium inside the project venv: "
        "`pip install streamlit-folium` — required for viewport atomic lattice."
    )
    st.components.v1.html(_federation_map._repr_html_(), height=520, scrolling=False)
else:
    _gv_zoom = st.session_state.get("gv_zoom")
    _gv_center = st.session_state.get("gv_center")
    _out = st_folium(
        _federation_map,
        key="gv_map",
        height=800,
        use_container_width=True,
        returned_objects=["bounds", "zoom", "center"],
        zoom=_gv_zoom,
        center=_gv_center,
        feature_group_to_add=_fg_atom if len(_viewport_df) > 0 else None,
    )
    if isinstance(_out, dict):
        st.session_state["gv_map_out"] = _out
        _zz = parse_st_folium_zoom(_out.get("zoom"))
        if _zz is not None:
            st.session_state["gv_zoom"] = _zz
        _ctr = _out.get("center")
        if isinstance(_ctr, dict) and "lat" in _ctr:
            _lng = _ctr.get("lng")
            if _lng is None:
                _lng = _ctr.get("lon")
            if _lng is not None:
                try:
                    st.session_state["gv_center"] = (
                        float(_ctr["lat"]),
                        float(_lng),
                    )
                except (TypeError, ValueError):
                    pass
_states_warn = ""
if not _states_geojson:
    _states_warn = (
        "Federation boundary layer could not be fetched — AZK corridor and basemap remain live. "
        "Retry with network access for full state outlines."
    )

_atomic_meta_lines: list[str] = []
if _nat_err:
    _atomic_meta_lines.append(f"National lattice error: {_nat_err}")
elif _national_df is not None and _nat_rep:
    _atomic_meta_lines.append(
        f"National atomic · {_nat_rep.get('pu_rows', '—'):,} PU · "
        f"{_nat_rep.get('distinct_ward_tokens', '—')} ward clusters · "
        f"temikeezy matches {_nat_rep.get('temikeezy_ward_key_matches', '—')} · "
        f"viewport ≤ {len(_viewport_df):,} (cap 10k) · Z_atom={ZOOM_ATOM_EMERGE}"
    )

_detail_meta = " · ".join(
    filter(
        None,
        [
            _fuse_caption,
            _spine_caption if _spine_caption else None,
            _states_warn if _states_warn else None,
            *_atomic_meta_lines,
        ],
    )
)
_detail_meta_safe = html.escape(_detail_meta) if _detail_meta else ""

st.markdown(
    f"""
<div class="sovereign-detail-widget">
  <div class="sdw-metrics">
    <div class="sdw-metric"><div class="sdw-metric-val">37</div><div class="sdw-metric-lbl">States + FCT</div></div>
    <div class="sdw-metric"><div class="sdw-metric-val">774</div><div class="sdw-metric-lbl">LGAs · heartbeat</div></div>
    <div class="sdw-metric"><div class="sdw-metric-val">8,806</div><div class="sdw-metric-lbl">Wards</div></div>
    <div class="sdw-metric"><div class="sdw-metric-val">176,846</div><div class="sdw-metric-lbl">Polling units</div></div>
  </div>
  <div class="sdw-meta">
    <strong style="color:{GOLD};">Sovereign record</strong> · Scale 1 country: States + AZK · Scale 2: LGAs ≥ {ZOOM_LGA_EMERGE}, wards ≥ {ZOOM_WARD_EMERGE} ·
    Scale 3: atomic viewport ≥ {ZOOM_ATOM_EMERGE} · FPS HUD on map · pinch to atomize · orientation resize armed.<br/>
    {_detail_meta_safe if _detail_meta_safe else "Forensic spine loaded — map is the vigil."}
  </div>
</div>
""",
    unsafe_allow_html=True,
)


@st.fragment(run_every=60)
def _eagle_vigil_fragment():
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    st.caption(f"Eagle vigil · 60s autonomous scan · last tick {ts}")


if hasattr(st, "fragment"):
    _eagle_vigil_fragment()
else:
    st.caption("Eagle vigil · enable Streamlit ≥1.33 for 60s autonomous scans.")

st.markdown(
    """
<div class="footer-sovereign">
  SCUML Certificate · SC 151653884 · Copyright Registration LW15954<br/>
  © 2026 Galadiman Ruwa Center (GCSLC) LTD/GTE · Sovereign-by-Design
</div>
""",
    unsafe_allow_html=True,
)
