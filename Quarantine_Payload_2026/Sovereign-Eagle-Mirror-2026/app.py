"""
Sovereign Eagle Mirror 2026 — Initialization (clean slate).
Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026
"""

from __future__ import annotations

from datetime import datetime

import folium
import requests
import streamlit as st
from branca.element import Element
from folium.plugins import AntPath, Fullscreen

SHELL = "#000080"
GLASS = "rgba(255, 255, 255, 0.08)"
GOLD = "#D4AF37"
CYAN = "#00E5FF"

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


def _build_federation_map(states_geojson: dict | None) -> folium.Map:
    center_lat = sum(n["lat"] for n in AZK_CORRIDOR_NODES) / len(AZK_CORRIDOR_NODES)
    center_lon = sum(n["lon"] for n in AZK_CORRIDOR_NODES) / len(AZK_CORRIDOR_NODES)

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=6,
        tiles=None,
        width="100%",
        height="460px",
        prefer_canvas=True,
        zoom_control=True,
    )
    folium.TileLayer(
        tiles="CartoDB dark_matter",
        attr="© OpenStreetMap © CARTO · Sovereign Navy basemap",
        name="Sovereign Navy · Dark Matter",
        overlay=False,
        control=True,
    ).add_to(m)

    m.get_root().header.add_child(
        Element(
            f"<style>"
            f".leaflet-container{{background:{SHELL}!important;}}"
            f".leaflet-tile-pane img,.leaflet-tile-pane canvas{{opacity:0.85!important;}}"
            f".leaflet-control-attribution{{background:rgba(0,0,128,0.72)!important;"
            f"color:{GOLD}!important;font-size:10px!important;}}"
            f"</style>"
        )
    )

    fg_spine = folium.FeatureGroup(name="Federation · 36 + FCT").add_to(m)
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
            style_function=lambda _f: {
                "fillColor": "transparent",
                "color": CYAN,
                "weight": 1,
                "opacity": 0.45,
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

tab_tel, tab_fin, tab_sec, tab_soc = st.tabs(
    ["① Telecom (NCC)", "② Finance (CBN / Banks)", "③ Security (ONSA)", "④ Social & Logistics"]
)

with tab_tel:
    st.markdown(
        '<div class="mirror-phase-panel"><strong>Telecom</strong> — NCC overlays · AZK corridor · signal / fiber bind.</div>',
        unsafe_allow_html=True,
    )
with tab_fin:
    st.markdown(
        '<div class="mirror-phase-panel"><strong>Finance</strong> — CBN / inclusion · ward-gated aggregates.</div>',
        unsafe_allow_html=True,
    )
with tab_sec:
    st.markdown(
        '<div class="mirror-phase-panel"><strong>Security</strong> — ONSA correlation windows · policy automation.</div>',
        unsafe_allow_html=True,
    )
with tab_soc:
    st.markdown(
        '<div class="mirror-phase-panel"><strong>Social & logistics</strong> — Trade pulse · services · fleet contracts.</div>',
        unsafe_allow_html=True,
    )

st.markdown("### National map host — Federation glass")
_states_geojson = _load_nigeria_states_geojson()
_federation_map = _build_federation_map(_states_geojson)
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
      <p class="mgh1">GOOGLE OF NIGERIA — LIVE SOCKET</p>
      <p class="mgh2">Sovereign Navy basemap (tiles 85% · navy bleed) · Federation spine · AZK Million Steel Rods</p>
    </div>
    <div class="mirror-folium-host">"""
    + _map_embed
    + """</div>
    <div class="tam-layer-map" aria-hidden="true">
      <span class="tam-bubble-map" style="top:10%;left:6%;">Tam-Tam · Sovereign</span>
      <span class="tam-bubble-map b2" style="top:62%;right:8%;">Dam-Dam · GCSLC</span>
      <span class="tam-bubble-map b3" style="bottom:14%;left:18%;">Proprietary Methodology</span>
      <span class="tam-bubble-map b4" style="top:38%;right:22%;">176,846 Units · Vigil</span>
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

c1, c2, c3, c4 = st.columns(4)
c1.metric("States", "36")
c2.metric("LGAs", "774")
c3.metric("Wards", "8,806")
c4.metric("Polling units", "176,846")


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
