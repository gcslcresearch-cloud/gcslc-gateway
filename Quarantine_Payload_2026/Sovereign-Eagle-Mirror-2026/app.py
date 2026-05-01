"""
Sovereign Eagle Mirror 2026 — Initialization (clean slate).
Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import folium
import pandas as pd
import requests
import streamlit as st
from branca.element import Element
from folium.map import CustomPane
from folium.plugins import AntPath, Fullscreen

from atomic_spie import build_rigasa_spike_bundle
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


@st.cache_data(ttl=86400, show_spinner="Atomic Spie · Rigasa lattice mount…")
def _rigasa_spike_bundle_cached() -> dict:
    return build_rigasa_spike_bundle()


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
    atomic_bundle: dict | None,
) -> folium.Map:
    center_lat = sum(n["lat"] for n in AZK_CORRIDOR_NODES) / len(AZK_CORRIDOR_NODES)
    center_lon = sum(n["lon"] for n in AZK_CORRIDOR_NODES) / len(AZK_CORRIDOR_NODES)

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=6,
        tiles=None,
        width="100%",
        height="460px",
        prefer_canvas=False,
        zoom_control=True,
    )

    CustomPane("federationStates", z_index=380, pointer_events=True).add_to(m)
    CustomPane("lgaHeartbeat", z_index=430, pointer_events=True).add_to(m)
    CustomPane("wardReveal", z_index=468, pointer_events=False).add_to(m)
    atom_ok = (
        atomic_bundle is not None
        and isinstance(atomic_bundle.get("frame"), pd.DataFrame)
        and len(atomic_bundle["frame"]) > 0
    )
    if atom_ok:
        CustomPane("atomicLattice", z_index=490, pointer_events=True).add_to(m)

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

    if atom_ok:
        df_atom = atomic_bundle["frame"]
        fg_atom = folium.FeatureGroup(
            name="Atomic Spie · Kaduna Igabi Rigasa (153 PU · AZK corridor)",
        ).add_to(m)
        for _, row in df_atom.iterrows():
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
                tooltip=folium.Tooltip(
                    f"{row['code']} · {row.get('location', '')}"[:220],
                    sticky=True,
                ),
            ).add_to(fg_atom)

    fg_azk = folium.FeatureGroup(name="AZK · Million Steel Rods").add_to(m)
    azk_ll = [[n["lat"], n["lon"]] for n in AZK_CORRIDOR_NODES]

    folium.PolyLine(
        azk_ll,
        color=GOLD,
        weight=14,
        opacity=0.12,
        smooth_factor=1,
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
        ).add_to(fg_azk)

    AntPath(
        locations=azk_ll,
        color=GOLD,
        weight=5,
        opacity=0.92,
        delay=480,
        dash_array=[16, 22],
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
        atom_ok,
    )
    m.fit_bounds([[4.15, 2.55], [13.95, 14.68]])
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
/* Folium / Leaflet inside glass — mobile pinch-zoom; parent Streamlit shell cannot style iframe interior */
.mirror-folium-host {{
  position: relative;
  z-index: 3;
  touch-action: manipulation !important;
  border-radius: 12px;
  overflow: hidden;
}}
.mirror-folium-host iframe {{
  width: 100% !important;
  touch-action: manipulation !important;
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

st.markdown("---")

st.markdown(
    """
<div class="mirror-phase-panel">
  <strong>Phase 2 · Industrial spine</strong> — HDX COD Nigeria boundaries join 8,806 wards → 774 LGAs → 37 states + FCT.
  Programmatic partition cross-check via <code>gcslc_deep_join</code>. NGECC coal / green-gold asset wards: cyan 8REC aura
  (see <code>Part_02_Finance/data/coal_reserve_nodes.json</code>).
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("### National map host — Federation glass · Sovereign Heartbeat")
_states_geojson = _load_nigeria_states_geojson()
_phase2 = _load_phase2_spine_bundle()
_asset_states = _coal_asset_state_names()
try:
    _fused = _load_fused_lga_ward_partition()
    _fuse_ok = len(_fused) == 774 and int(_fused["ward_count"].sum()) == NATIONAL_WARD_TOTAL
    st.caption(
        f"gcslc_deep_join · {_fused.shape[0]} LGAs · Σ wards {int(_fused['ward_count'].sum()):,} · "
        f"{'CHECKSUM LOCKED' if _fuse_ok else 'CHECKSUM REVIEW'}"
    )
except Exception:
    st.caption("gcslc_deep_join manifest unreachable — HDX geometry spine still mounts when online.")

_spine = _phase2["spine_report"]
if _spine.get("ward_rows"):
    st.caption(
        f"HDX spine · {_spine['ward_rows']} ward rows · {_spine.get('distinct_lgas')} LGA facets · "
        f"{_spine.get('distinct_states')} state facets · "
        f"{'VALID' if _spine.get('valid') else 'REVIEW'}"
    )

try:
    _atomic_bundle = _rigasa_spike_bundle_cached()
except Exception as _atom_exc:
    _atomic_bundle = None
    st.caption(f"Atomic Spie unavailable (CSV / validation): {_atom_exc}")
else:
    _ar = _atomic_bundle["report"]
    st.caption(
        f"Atomic Spie · Rigasa Igabi · ward_token {_ar['ward_token']} · {_ar['pu_rows']} PU · "
        f"orphans {_ar['orphan_rows']} · Z_atom={ZOOM_ATOM_EMERGE} · FPS HUD on glass · "
        "pinch past wards to atomize"
    )

_federation_map = _build_federation_map(
    _states_geojson, _phase2, _asset_states, _atomic_bundle
)
_map_embed = _federation_map._repr_html_()
_MAP_GLASS_HTML = (
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap');
html, body { margin: 0; background: transparent !important; }
/* Lux lives here: st.components iframe does not inherit Streamlit markdown CSS */
.mirror-map-glass-map-host {
  border-radius: 18px;
  padding: 2px;
  background: linear-gradient(45deg, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C);
  background-size: 240% 240%;
  animation: gcslc-metal-rim 14s ease-in-out infinite;
  box-shadow: 0 8px 36px rgba(0, 0, 0, 0.48);
  position: relative;
}
@keyframes gcslc-metal-rim {
  0%, 100% { background-position: 0% 40%; }
  50% { background-position: 100% 55%; }
}
.mirror-map-glass-frost-map {
  position: relative;
  border-radius: 16px;
  min-height: 440px;
  padding: 14px;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.4), inset 0 -1px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
  touch-action: manipulation;
}
.mirror-map-glass-header {
  position: relative;
  z-index: 6;
  text-align: center;
  font-family: 'Goldman', sans-serif;
}
.mirror-map-glass-header .mgh1 {
  color: """
    + f"{GOLD}"
    + """; font-weight: 700; margin: 0 0 8px 0;
  font-size: clamp(0.85rem, 2.6vw, 1.05rem);
  text-shadow: 0 1px 6px rgba(0,0,0,0.75);
}
.mirror-map-glass-header .mgh2 {
  color: """
    + f"{GOLD}"
    + """; opacity: 0.92; margin: 0 0 12px 0;
  font-size: clamp(0.74rem, 2vw, 0.88rem);
  text-shadow: 0 1px 4px rgba(0,0,0,0.7);
}
.mirror-folium-host {
  position: relative;
  z-index: 2;
  touch-action: manipulation;
  border-radius: 12px;
  overflow: hidden;
}
.mirror-folium-host iframe {
  width: 100% !important;
  touch-action: manipulation !important;
  border: none !important;
  border-radius: 12px;
  display: block;
  background: """
    + f"{SHELL}"
    + """ !important;
}
.tam-layer-map {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 14;
  overflow: hidden;
  border-radius: 14px;
}
.tam-bubble-map {
  position: absolute;
  font-family: 'Goldman', sans-serif;
  font-weight: 700;
  font-size: clamp(0.62rem, 1.8vw, 0.82rem);
  letter-spacing: 0.14em;
  color: rgba(212, 175, 55, 0.52);
  white-space: nowrap;
  text-transform: uppercase;
  text-shadow: 0 0 16px rgba(0,0,0,0.88), 0 2px 6px rgba(0,0,0,0.95);
  animation: tam-drift-map 22s ease-in-out infinite;
}
.tam-bubble-map.b2 { animation-duration: 28s; animation-delay: -4s; }
.tam-bubble-map.b3 { animation-duration: 18s; animation-delay: -9s; }
.tam-bubble-map.b4 { animation-duration: 26s; animation-delay: -2s; }
@keyframes tam-drift-map {
  0%, 100% { transform: translate(0,0) rotate(-6deg); opacity: 0.45; }
  33% { transform: translate(8px,-6px) rotate(4deg); opacity: 0.62; }
  66% { transform: translate(-6px,8px) rotate(-3deg); opacity: 0.52; }
}
</style>
<div class="mirror-map-glass-map-host">
  <div class="mirror-map-glass-frost-map">
    <div class="mirror-map-glass-header">
      <p class="mgh1">PHASE 2 · INDUSTRIAL SOVEREIGN MIRROR</p>
      <p class="mgh2">March 7 Lux · pinch-zoom: LGAs ≥ zoom """
    + str(ZOOM_LGA_EMERGE)
    + """, wards ≥ zoom """
    + str(ZOOM_WARD_EMERGE)
    + """ · atoms ≥ zoom """
    + str(ZOOM_ATOM_EMERGE)
    + """ (mist→solid) · HDX ward labels (sticky tap) · LGA heartbeat #BF953F · deep blue shell #000080 · AZK spine</p>
    </div>
    <div class="mirror-folium-host">"""
    + _map_embed
    + """</div>
    <div class="tam-layer-map" aria-hidden="true">
      <span class="tam-bubble-map" style="top:10%;left:6%;">Tam-Tam · Sovereign</span>
      <span class="tam-bubble-map b2" style="top:62%;right:8%;">Dam-Dam · GCSLC</span>
      <span class="tam-bubble-map b3" style="bottom:14%;left:18%;">Proprietary Methodology</span>
      <span class="tam-bubble-map b4" style="top:38%;right:22%;">8REC · NGECC asset lattice</span>
    </div>
  </div>
</div>
"""
)
st.components.v1.html(_MAP_GLASS_HTML, height=600, scrolling=False)
if not _states_geojson:
    st.caption(
        "Federation boundary layer could not be fetched — AZK corridor and basemap remain live. "
        "Retry with network access for full state outlines."
    )

c1, c2, c3 = st.columns(3)
c1.metric("States + FCT", "37")
c2.metric("LGAs (heartbeat)", "774")
c3.metric("Wards (HDX + join)", "8,806")
st.caption(
    f"Pinch drill-down · LGAs ≥ {ZOOM_LGA_EMERGE} · wards ≥ {ZOOM_WARD_EMERGE} · "
    f"Atomic Spie (Rigasa) ≥ {ZOOM_ATOM_EMERGE} · FPS HUD bottom-left on map · "
    "sticky tooltips on mobile glass."
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
