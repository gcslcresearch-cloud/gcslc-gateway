"""
Sovereign Eagle Mirror 2026 — Initialization (clean slate).
Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026
"""

from __future__ import annotations

import hashlib
import html
import json
from datetime import timedelta
from time import time as _wall_time
from pathlib import Path
from typing import Any

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
from folium.plugins import AntPath, Fullscreen, HeatMap

from forensic_intel import (
    DOUBLE_ZERO_GREY_GRADIENT,
    LAGOS_MAINLAND_POP_PER_POS_REF,
    build_double_zero_triples,
    komi_popup_html,
    nearest_azk_node,
)

from atomic_spie import (
    build_national_pu_geodataframe,
    parse_st_folium_bounds,
    parse_st_folium_zoom,
    subset_pus_for_viewport,
)
from sovereign_nl_query import ngecc_discovery_hit, resolve_sovereign_nl_query
from sovereign_strategic_cells import strategic_cells_banner
from generative_eagle import collect_eagle_shouts, friction_alert_active
# Load fused catalog before sovereign_active_intel (same gcslc_deep_join dep) — avoids rare Streamlit loader KeyError.
from gcslc_deep_join import NATIONAL_WARD_TOTAL, build_fused_catalog
from sovereign_active_intel import (
    build_total_reality_summary,
    load_ntw_operator_proxy,
    resolve_state_from_click,
)
from vigil_feed import load_recent_events, merge_vigil_sources
from ntw_regional_audit import _kgec_marquee_pair
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
# Lattice FIN pivot — high contrast vs navy basemap / Deep Blue shell
GOLD_PIVOT_FILL = "#FFDF66"
GOLD_PIVOT_STROKE = "#FFFEF5"
# Friction audit — NCC vulnerability vs Deep Blue shell
CRIMSON_VULN = "#DC143C"
CBN_ACCESS_ACCENT = "#C9A227"
SOCIAL_HUB_ACCENT = "#7FD4B8"

BASE_DIR = Path(__file__).resolve().parent
COAL_NODES_JSON = BASE_DIR / "Part_02_Finance" / "data" / "coal_reserve_nodes.json"
NGECC_INDUSTRIAL_PU_JSON = (
    BASE_DIR / "Part_02_Finance" / "data" / "ngecc_strategic_industrial_pu.json"
)
VANDALISM_INCIDENTS_JSON = (
    BASE_DIR / "Part_03_Security" / "data" / "vandalism_incidents.json"
)
CBN_FINANCIAL_JSON = BASE_DIR / "Part_02_Finance" / "data" / "cbn_financial_access_points.json"
SOCIAL_SERVICE_HUBS_JSON = BASE_DIR / "Part_04_Social" / "data" / "social_service_hubs.json"
TRADE_COMMERCE_JSON = BASE_DIR / "Part_02_Finance" / "data" / "trade_commerce_nodes.json"
FIN_INCLUSION_POS_JSON = BASE_DIR / "Part_02_Finance" / "data" / "financial_inclusion_pos.json"
MICRO_ASSETS_JSON = BASE_DIR / "Part_04_Social" / "data" / "micro_assets_capillaries.json"
SIGNAL_BLACKOUTS_JSON = BASE_DIR / "Part_01_Telecom" / "data" / "signal_blackouts.json"
VIGIL_FEED_JSON = BASE_DIR / "Part_01_Telecom" / "data" / "vigil_feed_events.json"
NTW_OPERATOR_PROXY_JSON = (
    BASE_DIR / "Part_01_Telecom" / "data" / "state_ntw_operator_proxy.json"
)
NTW_REGIONAL_AUDIT_JSON = (
    BASE_DIR / "Part_01_Telecom" / "data" / "ntw_regional_corridor_audit.json"
)
LAGOS_STRIKE_JSON = BASE_DIR / "Part_02_Finance" / "data" / "lagos_mainland_strike_points.json"
NORTHERN_MARKET_VECTORS_JSON = (
    BASE_DIR / "Part_02_Finance" / "data" / "northern_market_azk_vectors.json"
)
VECTOR_GREEN = "#2ECC71"

# Financial inclusion gap palette (commerce high · formal thin → warm)
FIN_GAP_SEVERE = "#E85D04"
FIN_GAP_MODERATE = "#F4A261"
FIN_GAP_NARROW = "#2DC6A4"

ESRI_WORLD_IMAGERY = (
    "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/"
    "tile/{z}/{y}/{x}"
)
ESRI_REF_LABELS = (
    "https://server.arcgisonline.com/ArcGIS/rest/services/Reference/"
    "World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}"
)


def _parse_azk_alignment_flag(raw: object) -> bool:
    """Registry `azk_alignment`: strict boolean (legacy prose maps to false)."""
    if raw is True:
        return True
    if raw is False or raw is None:
        return False
    if isinstance(raw, str):
        return raw.strip().lower() in {"true", "1", "yes"}
    return False


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


def _ensure_gv_viewport_defaults() -> None:
    """Lock national viewport in session so smart-click reruns do not snap to defaults."""
    if "gv_zoom" not in st.session_state:
        st.session_state["gv_zoom"] = 6.2
    if "gv_center" not in st.session_state:
        clat = sum(n["lat"] for n in AZK_CORRIDOR_NODES) / len(AZK_CORRIDOR_NODES)
        clon = sum(n["lon"] for n in AZK_CORRIDOR_NODES) / len(AZK_CORRIDOR_NODES)
        st.session_state["gv_center"] = (clat, clon)


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
def _load_ngecc_industrial_registry() -> dict:
    """Phase 3 NGECC strategic PU codes → Sovereign Gold industrial nodes on the atomic lattice."""
    if not NGECC_INDUSTRIAL_PU_JSON.is_file():
        return {
            "codes": frozenset(),
            "labels": {},
            "azk_codes": frozenset(),
            "meta": {},
            "search_aliases": [],
            "nodes": [],
            "bulk_entries_count": 0,
        }
    raw = json.loads(NGECC_INDUSTRIAL_PU_JSON.read_text(encoding="utf-8"))
    primary = raw.get("industrial_nodes") or []
    bulk = raw.get("industrial_nodes_bulk") or []
    seen: set[str] = set()
    nodes: list[dict] = []
    for block in (primary, bulk):
        for n in block:
            if not isinstance(n, dict):
                continue
            c = str(n.get("code", "")).strip()
            if not c or c in seen:
                continue
            seen.add(c)
            nodes.append(n)
    codes = frozenset(str(n.get("code", "")).strip() for n in nodes if n.get("code"))
    labels = {
        str(n.get("code", "")).strip(): str(n.get("label", "Industrial node")).strip()
        for n in nodes
        if n.get("code")
    }
    azk_codes = frozenset(
        str(n.get("code", "")).strip()
        for n in nodes
        if n.get("code") and _parse_azk_alignment_flag(n.get("azk_alignment"))
    )
    meta = raw.get("meta") or {}
    sa_raw = meta.get("search_aliases")
    search_aliases: list[str] = (
        [str(x).strip() for x in sa_raw if str(x).strip()] if isinstance(sa_raw, list) else []
    )
    return {
        "codes": codes,
        "labels": labels,
        "azk_codes": azk_codes,
        "meta": meta,
        "search_aliases": search_aliases,
        "nodes": nodes,
        "bulk_entries_count": len(bulk),
    }


@st.cache_data(ttl=86400, show_spinner=False)
def _load_ncc_vulnerability_incidents() -> list[dict]:
    """NCC-aligned ICT vandalization nodes → crimson friction layer."""
    if not VANDALISM_INCIDENTS_JSON.is_file():
        return []
    raw = json.loads(VANDALISM_INCIDENTS_JSON.read_text(encoding="utf-8"))
    out: list[dict] = []
    for row in raw.get("incidents") or []:
        if not isinstance(row, dict):
            continue
        try:
            float(row["lat"])
            float(row["lon"])
        except (KeyError, TypeError, ValueError):
            continue
        out.append(row)
    return out


@st.cache_data(ttl=86400, show_spinner=False)
def _load_cbn_financial_points() -> list[dict]:
    if not CBN_FINANCIAL_JSON.is_file():
        return []
    raw = json.loads(CBN_FINANCIAL_JSON.read_text(encoding="utf-8"))
    return _validate_lat_lon_points(raw.get("points") or [])


@st.cache_data(ttl=86400, show_spinner=False)
def _load_social_service_points() -> list[dict]:
    if not SOCIAL_SERVICE_HUBS_JSON.is_file():
        return []
    raw = json.loads(SOCIAL_SERVICE_HUBS_JSON.read_text(encoding="utf-8"))
    return _validate_lat_lon_points(raw.get("points") or [])


def _validate_lat_lon_points(rows: list) -> list[dict]:
    out: list[dict] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        try:
            float(row["lat"])
            float(row["lon"])
        except (KeyError, TypeError, ValueError):
            continue
        out.append(row)
    return out


def _fin_inclusion_gap_style(row: dict) -> tuple[str, str]:
    """Map inclusion_gap → stroke/fill color + CSS class (POS matrix)."""
    gap = str(row.get("inclusion_gap", "moderate")).strip().lower()
    if gap == "severe":
        return FIN_GAP_SEVERE, "gcslc-fin-gap-severe"
    if gap == "narrow":
        return FIN_GAP_NARROW, "gcslc-fin-gap-narrow"
    return FIN_GAP_MODERATE, "gcslc-fin-gap-moderate"


@st.cache_data(ttl=86400, show_spinner=False)
def _load_trade_commerce_nodes() -> list[dict]:
    if not TRADE_COMMERCE_JSON.is_file():
        return []
    raw = json.loads(TRADE_COMMERCE_JSON.read_text(encoding="utf-8"))
    return _validate_lat_lon_points(raw.get("nodes") or [])


@st.cache_data(ttl=86400, show_spinner=False)
def _load_financial_inclusion_pos() -> list[dict]:
    if not FIN_INCLUSION_POS_JSON.is_file():
        return []
    raw = json.loads(FIN_INCLUSION_POS_JSON.read_text(encoding="utf-8"))
    return _validate_lat_lon_points(raw.get("points") or [])


@st.cache_data(ttl=86400, show_spinner=False)
def _load_micro_assets_capillaries() -> list[dict]:
    if not MICRO_ASSETS_JSON.is_file():
        return []
    raw = json.loads(MICRO_ASSETS_JSON.read_text(encoding="utf-8"))
    return _validate_lat_lon_points(raw.get("micro_assets") or [])


@st.cache_data(ttl=86400, show_spinner=False)
def _load_signal_blackout_events() -> list[dict]:
    if not SIGNAL_BLACKOUTS_JSON.is_file():
        return []
    raw = json.loads(SIGNAL_BLACKOUTS_JSON.read_text(encoding="utf-8"))
    out: list[dict] = []
    for row in raw.get("events") or []:
        if not isinstance(row, dict):
            continue
        try:
            float(row["lat"])
            float(row["lon"])
        except (KeyError, TypeError, ValueError):
            continue
        out.append(row)
    return out


@st.cache_data(ttl=45, show_spinner=False)
def _load_vigil_registry_events() -> list[dict]:
    return load_recent_events(VIGIL_FEED_JSON, limit=120)


@st.cache_data(ttl=3600, show_spinner=False)
def _load_ntw_operator_proxy_cached() -> dict:
    return load_ntw_operator_proxy(NTW_OPERATOR_PROXY_JSON)


def _load_ntw_regional_audit_live() -> dict[str, Any]:
    """Always read `ntw_regional_corridor_audit.json` from disk (no cache) — Chairman sees live data on click."""
    from ntw_regional_audit import load_ntw_regional_audit

    return load_ntw_regional_audit(NTW_REGIONAL_AUDIT_JSON)


@st.cache_data(ttl=86400, show_spinner=False)
def _load_lagos_strike_points() -> list[dict]:
    if not LAGOS_STRIKE_JSON.is_file():
        return []
    raw = json.loads(LAGOS_STRIKE_JSON.read_text(encoding="utf-8"))
    return _validate_lat_lon_points(raw.get("points") or [])


@st.cache_data(ttl=86400, show_spinner=False)
def _load_northern_market_vectors() -> list[dict]:
    if not NORTHERN_MARKET_VECTORS_JSON.is_file():
        return []
    raw = json.loads(NORTHERN_MARKET_VECTORS_JSON.read_text(encoding="utf-8"))
    rows = raw.get("markets") or []
    out: list[dict] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        try:
            float(row["lat"])
            float(row["lon"])
        except (KeyError, TypeError, ValueError):
            continue
        out.append(row)
    return out


def _binji_void_points(fin_rows: list[dict]) -> list[dict]:
    """POS anchors for Binji–Lagos strike (Binji + Danchadi corridor)."""
    out: list[dict] = []
    for row in fin_rows:
        z = str(row.get("zone", "")).strip().lower()
        if z in {"binji", "danchadi"}:
            out.append(row)
    return out


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


def _atomic_viewport_feature_group(
    viewport_df: pd.DataFrame,
    industrial_codes: frozenset[str],
    industrial_labels: dict[str, str],
    industrial_azk_codes: frozenset[str],
    *,
    show_industrial_overlay: bool,
) -> folium.FeatureGroup:
    """Viewport PU batch — cyan lattice; NGECC registry codes as Sovereign Gold (#BF953F) when overlay on."""
    fg = folium.FeatureGroup(
        name=f"176,846 PU · viewport ({len(viewport_df):,} shown)",
    )
    if viewport_df is None or len(viewport_df) == 0:
        return fg
    for _, row in viewport_df.iterrows():
        loc = str(row.get("location", ""))[:180]
        code = str(row.get("code", "")).strip()
        is_industrial = bool(
            show_industrial_overlay and industrial_codes and code in industrial_codes
        )
        if is_industrial:
            lbl = industrial_labels.get(code, "NGECC industrial node")
            tip = f"{code} · {lbl} · {loc}"[:240]
            is_azk = bool(industrial_azk_codes and code in industrial_azk_codes)
            cls = (
                "gcslc-atom-node gcslc-atom-industrial gcslc-atom-azk-spine"
                if is_azk
                else "gcslc-atom-node gcslc-atom-industrial"
            )
            folium.CircleMarker(
                location=[float(row["lat"]), float(row["lon"])],
                radius=5 if is_azk else 4,
                pane="atomicLattice",
                color=GOLD_HEARTBEAT,
                weight=1.55 if is_azk else 1.25,
                fill=True,
                fillColor=GOLD_HEARTBEAT,
                fillOpacity=0.52 if is_azk else 0.42,
                opacity=0.88 if is_azk else 0.72,
                className=cls,
                tooltip=folium.Tooltip(tip, sticky=True),
            ).add_to(fg)
        else:
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
                tooltip=folium.Tooltip(f"{code} · {loc}", sticky=True),
            ).add_to(fg)
    return fg


def _build_strike_audit_map(
    *,
    center_lat: float,
    center_lon: float,
    zoom_start: int,
    points: list[dict],
    circle_class: str,
    komi_intel: bool,
) -> folium.Map:
    """Split-panel Lagos vs Binji audit — saturated blue fabric vs gold-in-void POS."""
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles=None,
        width="100%",
        height="520px",
        max_zoom=22,
    )
    folium.TileLayer(
        tiles="CartoDB dark_matter",
        attr="© OSM © CARTO",
        name="Basemap",
        overlay=False,
        control=True,
        max_zoom=22,
    ).add_to(m)
    strike_css = """
@keyframes gcs-strike-gold-pulse {
  0%,100% { filter: drop-shadow(0 0 5px rgba(191,149,63,0.55)); }
  50% { filter: drop-shadow(0 0 16px rgba(191,149,63,0.92)); }
}
circle.gcslc-strike-binji {
  animation: gcs-strike-gold-pulse 2.1s ease-in-out infinite !important;
  stroke: #00E5FF !important;
  fill: #BF953F !important;
}
circle.gcslc-strike-lagos {
  stroke: #0066CC !important;
  fill: rgba(0,229,255,0.55) !important;
}
@media (prefers-reduced-motion: reduce) {
  circle.gcslc-strike-binji { animation: none !important; }
}
"""
    m.get_root().header.add_child(
        Element(
            f"<style>"
            f".leaflet-container{{background:{SHELL}!important;}}"
            f"{strike_css}"
            f"</style>"
        )
    )
    for row in points:
        lbl = str(row.get("label") or row.get("name", "Audit node"))[:160]
        tip = lbl[:220]
        popup = None
        if komi_intel:
            popup = folium.Popup(
                komi_popup_html(
                    lbl,
                    row,
                    lagos_pop_per_pos_ref=LAGOS_MAINLAND_POP_PER_POS_REF,
                ),
                max_width=300,
            )
        cm_kw: dict = {
            "location": [float(row["lat"]), float(row["lon"])],
            "radius": 8,
            "color": CYAN,
            "weight": 2,
            "fill": True,
            "fillOpacity": 0.55,
            "opacity": 0.95,
            "tooltip": folium.Tooltip(tip, sticky=True),
            "className": f"gcslc-friction-node {circle_class}",
        }
        if popup is not None:
            cm_kw["popup"] = popup
        folium.CircleMarker(**cm_kw).add_to(m)
    folium.LayerControl(collapsed=True).add_to(m)
    return m


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
      var opG = 0.35 + t * 0.62;
      var rpxG = 2.5 + t * 8;
      var swG = 0.75 + t * 2.1;
      var cyanN = root.querySelectorAll("circle.gcslc-atom-node:not(.gcslc-atom-industrial)");
      for (var i = 0; i < cyanN.length; i++) {{
        var p = cyanN[i];
        if (p.tagName.toLowerCase() === "circle") {{
          p.setAttribute("r", rpx);
          p.setAttribute("stroke-width", sw);
          p.setAttribute("stroke-opacity", op);
          p.setAttribute("fill-opacity", op * 0.85);
        }}
      }}
      var azkN = root.querySelectorAll("circle.gcslc-atom-azk-spine");
      var goldN = root.querySelectorAll("circle.gcslc-atom-industrial:not(.gcslc-atom-azk-spine)");
      for (var j = 0; j < goldN.length; j++) {{
        var g = goldN[j];
        if (g.tagName.toLowerCase() === "circle") {{
          g.setAttribute("r", rpxG);
          g.setAttribute("stroke-width", swG);
          g.setAttribute("stroke-opacity", opG);
          g.setAttribute("fill-opacity", opG * 0.88);
        }}
      }}
      var rpxA = rpxG * 1.18, swA = swG * 1.12, opA = Math.min(1, opG * 1.08);
      for (var k = 0; k < azkN.length; k++) {{
        var a = azkN[k];
        if (a.tagName.toLowerCase() === "circle") {{
          a.setAttribute("r", rpxA);
          a.setAttribute("stroke-width", swA);
          a.setAttribute("stroke-opacity", opA);
          a.setAttribute("fill-opacity", opA * 0.9);
        }}
      }}
    }}
    function sync() {{
      var z = mp.getZoom();
      pl.style.opacity = (z >= zL) ? "1" : "0";
      pl.style.pointerEvents = "none";
      pw.style.opacity = (z >= zW) ? "1" : "0";
      pw.style.pointerEvents = "none";
      ps.style.opacity = "1";
      ps.style.pointerEvents = "none";
      if (pa) {{
        pa.style.opacity = (z >= zA) ? "1" : "0";
        pa.style.pointerEvents = "none";
      }}
      var pazk = mp.getPane("azkSpine");
      if (pazk) pazk.style.pointerEvents = "none";
      var pkg = mp.getPane("komiTotalReality");
      if (pkg) pkg.style.pointerEvents = "auto";
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


def _html_total_reality_card(summary: dict) -> str:
    """Typewriter-cyan Total Reality card (escaped)."""
    st_name = html.escape(str(summary.get("state", "")))
    lg = int(summary.get("lgas") or 0)
    wd = int(summary.get("wards_forensic") or summary.get("wards") or 0)
    n_wd_nat = int(summary.get("national_ward_total") or 8806)
    pu = int(summary.get("pu_forensic") or 0)
    n_pu_nat = int(summary.get("national_pu_total") or 176_846)
    atom_note = html.escape(str(summary.get("atomic_attribution_note", "")))
    fs = summary.get("financial_inclusion_score")
    fs_txt = html.escape(str(fs))
    fv = html.escape(str(summary.get("financial_inclusion_verdict", "")))
    fr = summary.get("friction") or {}
    dom = html.escape(str(summary.get("ntw_dominant_operator", "")))
    dist = summary.get("ntw_distribution") or {}
    dist_bits: list[str] = []
    for k, v in sorted(dist.items(), key=lambda x: -x[1]):
        try:
            pct = float(v) * 100.0
        except (TypeError, ValueError):
            pct = 0.0
        dist_bits.append(f"{html.escape(str(k))} {pct:.0f}%")
    dist_html = " · ".join(dist_bits)
    fr_txt = html.escape(str(fr.get("friction_summary", "")))
    return (
        "<div class='gcslc-total-reality gcslc-tr-handshake-front'>"
        f"<div class='gcslc-tr-h'>Total Reality Summary · {st_name}</div>"
        "<div class='gcslc-tr-line'><span class='gcslc-tr-k'>Administrative drill-down</span> "
        f"LGAs {lg} · Wards {wd:,} / {n_wd_nat:,} national · "
        f"Polling units {pu:,} / {n_pu_nat:,} (INEC lattice)</div>"
        "<div class='gcslc-tr-line' style='font-size:0.78em;opacity:0.9;'><span class='gcslc-tr-k'>"
        f"Forensic note</span> {atom_note}</div>"
        "<div class='gcslc-tr-line'><span class='gcslc-tr-k'>Financial inclusion score</span> "
        f"{fs_txt} / 100 — {fv}</div>"
        "<div class='gcslc-tr-line'><span class='gcslc-tr-k'>Friction audit</span> "
        f"NCC nodes in-state {fr.get('ncc_incidents_in_state', 0)} · "
        f"Telecom voids {fr.get('signal_void_events_in_state', 0)} · "
        f"severity avg {fr.get('ncc_severity_avg', 0)} — {fr_txt}</div>"
        "<div class='gcslc-tr-line'><span class='gcslc-tr-k'>NTW coverage (proxy)</span> "
        f"Strongest modeled subscriber base → <strong>{dom}</strong> · {dist_html}</div>"
        "</div>"
    )


def _ntw_pulse_click(op: str) -> None:
    """Instant Big-4 ignition — session + nonce so forensic rain remounts on every click."""
    st.session_state["ntw_resonance_pick"] = op
    st.session_state["ntw_resonance_nonce"] = int(st.session_state.get("ntw_resonance_nonce", 0)) + 1
    st.session_state["ntw_push_ts"] = _wall_time()


def _render_ntw_sovereign_control_panel(ntw_proxy: dict[str, Any] | None = None) -> None:
    """High-pedestal Resonance Chamber — meter bars + pulsing operator keys + typewriter stream (main only)."""
    from ntw_regional_audit import (
        html_ntw_meter_strip_row,
        html_ntw_resonance_typewriter_stream,
    )

    if ntw_proxy is None:
        ntw_proxy = _load_ntw_operator_proxy_cached()

    st.session_state.setdefault("ntw_resonance_pick", "MTN")
    st.session_state.setdefault("ntw_push_ts", _wall_time())
    st.session_state.setdefault("ntw_resonance_nonce", 1)
    st.markdown(
        "<div class='national-resonance-chamber-outer sovereign-ntw-strip sovereign-ntw-resonance "
        "sovereign-ntw-pedestal'>"
        "<p class='sovereign-ntw-panel-head national-rc-title kgec-rc-ticker-line'>"
        "<span class='kgec-mq' style='--kgec-mq-dur:32s'><span class='kgec-mq-track'><span>"
        "K-GEC · National Resonance Chamber · Big 4 · Secured Anchor · GCSLC forensic soul"
        "</span><span aria-hidden='true'>"
        "K-GEC · National Resonance Chamber · Big 4 · Secured Anchor · GCSLC forensic soul"
        "</span></span></span></p>"
        "<p class='sovereign-ntw-sub kgec-rc-ticker-line'>"
        "<span class='kgec-mq' style='--kgec-mq-dur:36s'><span class='kgec-mq-track'><span>"
        "Komi-Generative Cloud · meter deck · pulse keys · Subscriber Base · Spectrum · Broadband"
        "</span><span aria-hidden='true'>"
        "Komi-Generative Cloud · meter deck · pulse keys · Subscriber Base · Spectrum · Broadband"
        "</span></span></span></p>"
        "<hr class='sovereign-ntw-hr'/>"
        "</div>",
        unsafe_allow_html=True,
    )
    _blob = _load_ntw_regional_audit_live()
    st.markdown(html_ntw_meter_strip_row(_blob), unsafe_allow_html=True)
    _ops = ["MTN", "Airtel", "Glo", "9mobile"]
    _pr = st.columns(4)
    for _i, _op in enumerate(_ops):
        with _pr[_i]:
            st.button(
                f"{_op}",
                key=f"ntw_pulse_{_op}",
                use_container_width=True,
                help="Ignite forensic rain — Subscriber Base · Spectrum · Broadband",
                on_click=_ntw_pulse_click,
                args=(_op,),
            )
    _pick = str(st.session_state.get("ntw_resonance_pick") or "").strip()
    if _pick in _ops:
        _nonce = int(st.session_state.get("ntw_resonance_nonce", 0))
        _tw = html_ntw_resonance_typewriter_stream(
            _pick,
            _blob,
            ntw_proxy,
            audit_path=NTW_REGIONAL_AUDIT_JSON,
        )
        _push = float(st.session_state.get("ntw_push_ts") or 0)
        st.markdown(
            f"<div class='kgec-ntw-stream-root' data-kgec-ntw-nonce='{_nonce}' "
            f"data-kgec-ntw-push='{_push:.6f}'>{_tw}</div>",
            unsafe_allow_html=True,
        )
    else:
        _kgec_kinetic_note(
            "Select a Big-4 network pulse above — stream unlocks subscriber base, spectrum layer, "
            "corridor broadband — sovereign chamber IDLE.",
            seconds=34.0,
        )


def _build_federation_map(
    states_geojson: dict | None,
    phase2: dict | None,
    asset_states: frozenset[str],
    *,
    show_ncc_vulnerability: bool = False,
    ncc_incidents: list[dict] | None = None,
    show_cbn_access: bool = False,
    cbn_points: list[dict] | None = None,
    show_social_hubs: bool = False,
    social_points: list[dict] | None = None,
    show_trade_commerce: bool = False,
    trade_nodes: list[dict] | None = None,
    show_financial_inclusion_pos: bool = False,
    financial_inclusion_points: list[dict] | None = None,
    show_micro_assets: bool = False,
    micro_asset_points: list[dict] | None = None,
    show_double_zero: bool = False,
    double_zero_triples: list[list[float]] | None = None,
    show_azk_vectors: bool = False,
    northern_markets: list[dict] | None = None,
    show_komi_intel: bool = False,
    fin_inclusion_gold_highlight: bool = False,
) -> folium.Map:
    center_lat = sum(n["lat"] for n in AZK_CORRIDOR_NODES) / len(AZK_CORRIDOR_NODES)
    center_lon = sum(n["lon"] for n in AZK_CORRIDOR_NODES) / len(AZK_CORRIDOR_NODES)

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=6,
        tiles=None,
        width="100%",
        height="560px",
        prefer_canvas=False,
        zoom_control=True,
        max_zoom=22,
    )

    # Polygon / lattice panes: pointer_events False so map fires last_clicked on touch (smart click).
    CustomPane("federationStates", z_index=380, pointer_events=False).add_to(m)
    CustomPane("lgaHeartbeat", z_index=430, pointer_events=False).add_to(m)
    CustomPane("wardReveal", z_index=468, pointer_events=False).add_to(m)
    CustomPane("atomicLattice", z_index=490, pointer_events=False).add_to(m)
    CustomPane("microCapillary", z_index=501, pointer_events=False).add_to(m)
    CustomPane("tradeCommerce", z_index=502, pointer_events=False).add_to(m)
    CustomPane("frictionFinInclusion", z_index=503, pointer_events=False).add_to(m)
    # Friction overlays — above lattice mist, below AZK spine (compact markers; sidebar toggles)
    CustomPane("frictionSocial", z_index=504, pointer_events=False).add_to(m)
    CustomPane("frictionCBN", z_index=505, pointer_events=False).add_to(m)
    CustomPane("frictionVulnerability", z_index=508, pointer_events=False).add_to(m)
    # AZK Million Steel Rods — always above atomic cyan mist (national PU viewport layer)
    CustomPane("azkSpine", z_index=620, pointer_events=False).add_to(m)
    # Komi · Total Reality — above spine so cyan popups / village taps win when enabled
    CustomPane("komiTotalReality", z_index=850, pointer_events=True).add_to(m)

    folium.TileLayer(
        tiles=ESRI_WORLD_IMAGERY,
        attr="Tiles © Esri — Source: Esri, Maxar, Earthstar Geographics · Default for village audit",
        name="Esri · World Imagery (default · hyper-zoom)",
        overlay=False,
        control=True,
        max_zoom=22,
        max_native_zoom=19,
    ).add_to(m)
    folium.TileLayer(
        tiles="CartoDB dark_matter",
        attr="© OpenStreetMap © CARTO · Sovereign Navy basemap",
        name="Sovereign Navy · Dark Matter",
        overlay=False,
        control=True,
        max_zoom=22,
    ).add_to(m)
    folium.TileLayer(
        tiles=ESRI_REF_LABELS,
        attr="© Esri · Reference labels · streets / settlements",
        name="Esri · Hybrid labels (overlay · ON by default)",
        overlay=True,
        control=True,
        show=True,
        max_zoom=22,
        max_native_zoom=19,
    ).add_to(m)

    pulse_css = """
@keyframes gcs-sovereign-heartbeat {
  0%, 100% {
    stroke: #BF953F;
    stroke-opacity: 0.48;
    stroke-width: 1.05px;
    fill-opacity: 0.035;
    filter: brightness(1) drop-shadow(0 0 2px rgba(191,149,63,0.22));
  }
  50% {
    stroke: #FFF8DC;
    stroke-opacity: 0.68;
    stroke-width: 1.55px;
    fill-opacity: 0.065;
    filter: brightness(1.1) drop-shadow(0 0 4px rgba(191,149,63,0.32));
  }
}
path.gcslc-lga-sovereign-heartbeat {
  animation: gcs-sovereign-heartbeat 18s ease-in-out infinite !important;
  stroke-linejoin: round !important;
  stroke-linecap: round !important;
  transform: translateZ(0);
}
@keyframes gcs-eightrec-aura {
  0%, 100% { stroke-opacity: 0.65; filter: drop-shadow(0 0 3px rgba(0,229,255,0.22)); }
  50% { stroke-opacity: 0.88; filter: drop-shadow(0 0 7px rgba(0,229,255,0.38)); }
}
path.gcslc-ward-eightrec-asset {
  animation: gcs-eightrec-aura 5.5s ease-in-out infinite !important;
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
@keyframes gcs-industrial-node-shimmer {
  0%, 100% {
    stroke-opacity: 0.58;
    fill-opacity: 0.36;
    filter: brightness(1.03) drop-shadow(0 0 3px rgba(191,149,63,0.28));
  }
  50% {
    stroke-opacity: 0.88;
    fill-opacity: 0.52;
    filter: brightness(1.08) drop-shadow(0 0 8px rgba(191,149,63,0.42));
  }
}
@keyframes gcs-industrial-node-shimmer-azk {
  0%, 100% {
    stroke-opacity: 0.68;
    fill-opacity: 0.44;
    filter: brightness(1.06) drop-shadow(0 0 5px rgba(191,149,63,0.38));
  }
  50% {
    stroke-opacity: 0.92;
    fill-opacity: 0.62;
    filter: brightness(1.12) drop-shadow(0 0 12px rgba(191,149,63,0.52));
  }
}
circle.gcslc-atom-industrial, path.gcslc-atom-industrial {
  stroke: #BF953F !important;
  fill: #BF953F !important;
  animation: gcs-industrial-node-shimmer 5s ease-in-out infinite !important;
}
circle.gcslc-atom-industrial.gcslc-atom-azk-spine,
path.gcslc-atom-industrial.gcslc-atom-azk-spine {
  animation: gcs-industrial-node-shimmer-azk 4.2s ease-in-out infinite !important;
}
@keyframes gcs-friction-crimson-vibrate {
  0%, 100% {
    stroke-opacity: 0.72;
    fill-opacity: 0.4;
    filter: brightness(1.05) drop-shadow(0 0 4px rgba(220,20,60,0.38));
  }
  50% {
    stroke-opacity: 0.92;
    fill-opacity: 0.58;
    filter: brightness(1.12) drop-shadow(0 0 10px rgba(220,20,60,0.48));
  }
}
circle.gcslc-friction-ncc-vuln, path.gcslc-friction-ncc-vuln {
  stroke: #DC143C !important;
  fill: #DC143C !important;
  animation: gcs-friction-crimson-vibrate 3.2s ease-in-out infinite !important;
}
circle.gcslc-friction-cbn, path.gcslc-friction-cbn {
  stroke: #C9A227 !important;
  fill: #C9A227 !important;
}
circle.gcslc-friction-social, path.gcslc-friction-social {
  stroke: #7FD4B8 !important;
  fill: #7FD4B8 !important;
}
circle.gcslc-trade-livestock, path.gcslc-trade-livestock {
  stroke: #00E5FF !important;
  fill: #BF953F !important;
  stroke-width: 2px !important;
  filter: drop-shadow(0 0 6px rgba(191,149,63,0.55));
}
circle.gcslc-fin-gap-severe, path.gcslc-fin-gap-severe {
  stroke: #E85D04 !important;
  fill: #E85D04 !important;
}
circle.gcslc-fin-gap-moderate, path.gcslc-fin-gap-moderate {
  stroke: #F4A261 !important;
  fill: #F4A261 !important;
}
circle.gcslc-fin-gap-narrow, path.gcslc-fin-gap-narrow {
  stroke: #2DC6A4 !important;
  fill: #2DC6A4 !important;
}
@keyframes gcs-fin-pivot-handshake {
  0%, 100% {
    stroke-opacity: 1;
    fill-opacity: 0.94;
    filter: brightness(1.05) drop-shadow(0 0 8px rgba(255, 223, 102, 0.95)) drop-shadow(0 0 3px rgba(255, 255, 255, 0.45));
  }
  50% {
    stroke-opacity: 1;
    fill-opacity: 1;
    filter: brightness(1.18) drop-shadow(0 0 16px rgba(255, 223, 102, 1)) drop-shadow(0 0 6px rgba(255, 255, 255, 0.55));
  }
}
circle.gcslc-fin-pivot-sovereign, path.gcslc-fin-pivot-sovereign {
  stroke: #FFFEF5 !important;
  fill: #FFDF66 !important;
  stroke-width: 3.25px !important;
  animation: gcs-fin-pivot-handshake 2.4s ease-in-out infinite !important;
}
circle.gcslc-micro-capillary, path.gcslc-micro-capillary {
  stroke: rgba(240,244,255,0.85) !important;
  fill: rgba(0,229,255,0.35) !important;
  stroke-width: 1px !important;
}
@media (prefers-reduced-motion: reduce) {
  path.gcslc-lga-sovereign-heartbeat, path.gcslc-ward-eightrec-asset,
  circle.gcslc-atom-industrial, path.gcslc-atom-industrial,
  circle.gcslc-atom-azk-spine, path.gcslc-atom-azk-spine,
  circle.gcslc-friction-ncc-vuln, path.gcslc-friction-ncc-vuln,
  circle.gcslc-fin-pivot-sovereign, path.gcslc-fin-pivot-sovereign { animation: none !important; }
}
path.gcslc-atom-node {
  transition: fill-opacity 0.35s ease, stroke-opacity 0.35s ease;
}
.leaflet-popup-content .gcslc-komi-card {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  font-size: 11px !important;
  color: #00E5FF !important;
  background: rgba(0,0,128,0.94) !important;
  padding: 10px 12px !important;
  border-radius: 10px !important;
  border: 1px solid #BF953F !important;
  max-width: 280px !important;
}
.leaflet-popup-content .gcslc-komi-h {
  font-weight: 700 !important;
  letter-spacing: 0.06em !important;
  margin-bottom: 6px !important;
  color: #00E5FF !important;
}
.leaflet-popup-content .gcslc-komi-k {
  color: rgba(240,244,255,0.78) !important;
  margin-right: 6px !important;
}
/* iPhone portrait · Komi popups + layer picker stay inside safe area / readable */
.leaflet-popup-content-wrapper {
  max-width: min(280px, 92vw) !important;
}
.leaflet-popup-content {
  margin: 12px 14px !important;
  touch-action: manipulation !important;
  -webkit-text-size-adjust: 100% !important;
}
@media screen and (max-width: 430px) {
  .leaflet-popup-content .gcslc-komi-card {
    font-size: clamp(10px, 3.2vw, 12px) !important;
    max-width: min(280px, 90vw) !important;
    padding: 12px 14px !important;
  }
  .leaflet-control-layers {
    font-size: 11px !important;
    max-width: min(240px, 85vw) !important;
  }
  .leaflet-control-layers-expanded {
    max-height: min(360px, 55vh) !important;
    overflow-y: auto !important;
    -webkit-overflow-scrolling: touch !important;
  }
}
"""
    m.get_root().header.add_child(
        Element(
            f"<style>"
            f".leaflet-container{{background:{SHELL}!important;}}"
            f".leaflet-tile-pane img,.leaflet-tile-pane canvas{{opacity:0.97!important;}}"
            f"/* Crisp Esri imagery + hybrid labels at max zoom (portrait iPhone); Deep Blue shell stays on container */"
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

    if show_trade_commerce and trade_nodes:
        fg_trade = folium.FeatureGroup(
            name="Trade & Commerce · livestock / exchange anchors",
            show=True,
        ).add_to(m)
        for row in trade_nodes:
            lbl = str(row.get("label", "Trade node"))[:160]
            stt = str(row.get("state", ""))[:48]
            mc = str(row.get("market_class", ""))[:48]
            tip = f"{lbl}" + (f" · {stt}" if stt else "") + (f" · {mc}" if mc else "")
            tip = tip[:240]
            pop_tr = None
            if show_komi_intel:
                pop_tr = folium.Popup(
                    komi_popup_html(
                        lbl,
                        row,
                        lagos_pop_per_pos_ref=LAGOS_MAINLAND_POP_PER_POS_REF,
                    ),
                    max_width=300,
                )
            mk_tr = dict(
                location=[float(row["lat"]), float(row["lon"])],
                radius=9,
                color=CYAN,
                weight=2,
                fill=True,
                fillColor=GOLD_HEARTBEAT,
                fillOpacity=0.62,
                opacity=0.95,
                pane="komiTotalReality" if show_komi_intel else "tradeCommerce",
                className="gcslc-friction-node gcslc-trade-livestock",
                tooltip=folium.Tooltip(tip, sticky=True),
            )
            if pop_tr is not None:
                mk_tr["popup"] = pop_tr
            folium.CircleMarker(**mk_tr).add_to(fg_trade)

    if show_financial_inclusion_pos and financial_inclusion_points:
        fg_fin = folium.FeatureGroup(
            name="Financial inclusion · POS matrix (Binji / Bayelsa)",
            show=True,
        ).add_to(m)
        for row in financial_inclusion_points:
            col, css_gap = _fin_inclusion_gap_style(row)
            lbl = str(row.get("name", "POS cluster"))[:140]
            zon = str(row.get("zone", ""))[:64]
            stt = str(row.get("state", ""))[:48]
            gap = str(row.get("inclusion_gap", ""))[:24]
            ag = row.get("agents")
            ag_s = f" · agents ~{int(ag)}" if ag is not None else ""
            tip = f"{lbl} · {zon}, {stt} · gap {gap}{ag_s}"[:260]
            rad = 6
            try:
                if ag is not None:
                    rad = min(11, 5 + float(ag) / 14.0)
            except (TypeError, ValueError):
                rad = 6
            _fin_w = 1.45
            _fin_fo = 0.58
            _fin_cls = f"gcslc-friction-node {css_gap}"
            if fin_inclusion_gold_highlight:
                col = GOLD_PIVOT_STROKE
                rad = min(20.0, float(rad) * 1.42)
                _fin_w = 3.25
                _fin_fo = 0.94
                _fin_cls += " gcslc-fin-pivot-sovereign"
            pop_fin = None
            if show_komi_intel:
                pop_fin = folium.Popup(
                    komi_popup_html(
                        str(row.get("name", "POS")),
                        row,
                        lagos_pop_per_pos_ref=LAGOS_MAINLAND_POP_PER_POS_REF,
                    ),
                    max_width=300,
                )
            _fill_c = GOLD_PIVOT_FILL if fin_inclusion_gold_highlight else col
            _stroke_c = col
            mk_fin = dict(
                location=[float(row["lat"]), float(row["lon"])],
                radius=float(rad),
                color=_stroke_c,
                weight=_fin_w,
                fill=True,
                fillColor=_fill_c,
                fillOpacity=_fin_fo,
                opacity=1.0,
                pane="komiTotalReality" if show_komi_intel else "frictionFinInclusion",
                className=_fin_cls,
                tooltip=folium.Tooltip(tip, sticky=True),
            )
            if pop_fin is not None:
                mk_fin["popup"] = pop_fin
            folium.CircleMarker(**mk_fin).add_to(fg_fin)

    if show_micro_assets and micro_asset_points:
        fg_micro = folium.FeatureGroup(
            name="Micro-assets · capillaries",
            show=True,
        ).add_to(m)
        for row in micro_asset_points:
            lbl = str(row.get("label", "Micro-asset"))[:140]
            ac = str(row.get("asset_class", ""))[:56]
            tag = str(row.get("tag", ""))[:48]
            tip = f"{lbl}" + (f" · {ac}" if ac else "") + (f" · {tag}" if tag else "")
            tip = tip[:240]
            _r_micro = (
                4
                if str(row.get("asset_class", "")).strip().lower() == "sovereign_anchor"
                else 3
            )
            pop_mi = None
            if show_komi_intel:
                pop_mi = folium.Popup(
                    komi_popup_html(
                        lbl,
                        row,
                        lagos_pop_per_pos_ref=LAGOS_MAINLAND_POP_PER_POS_REF,
                    ),
                    max_width=300,
                )
            mk_mi = dict(
                location=[float(row["lat"]), float(row["lon"])],
                radius=_r_micro,
                color=CYAN,
                weight=1,
                fill=True,
                fillColor=CYAN,
                fillOpacity=0.38,
                opacity=0.72,
                pane="komiTotalReality" if show_komi_intel else "microCapillary",
                className="gcslc-friction-node gcslc-micro-capillary",
                tooltip=folium.Tooltip(tip, sticky=True),
            )
            if pop_mi is not None:
                mk_mi["popup"] = pop_mi
            folium.CircleMarker(**mk_mi).add_to(fg_micro)

    if show_double_zero and double_zero_triples:
        fg_dz = folium.FeatureGroup(
            name="Forensic · Double-Zero disconnected void (grey heat)",
            show=True,
        ).add_to(m)
        HeatMap(
            data=double_zero_triples,
            min_opacity=0.42,
            max_zoom=19,
            radius=34,
            blur=28,
            gradient=DOUBLE_ZERO_GREY_GRADIENT,
        ).add_to(fg_dz)

    if show_azk_vectors and northern_markets:
        fg_vec = folium.FeatureGroup(
            name="Forensic · Northern markets → AZK livestock vectors",
            show=True,
        ).add_to(m)
        for mk in northern_markets:
            try:
                lat_m = float(mk["lat"])
                lon_m = float(mk["lon"])
            except (KeyError, TypeError, ValueError):
                continue
            target, _dist = nearest_azk_node(lat_m, lon_m, AZK_CORRIDOR_NODES)
            flow = float(mk.get("daily_livestock_units_proxy") or 12.0)
            wvec = 2.0 + min(flow / 70.0, 5.5)
            AntPath(
                locations=[
                    [lat_m, lon_m],
                    [float(target["lat"]), float(target["lon"])],
                ],
                color=VECTOR_GREEN,
                weight=wvec,
                opacity=0.58,
                delay=280,
                dash_array=[12, 16],
            ).add_to(fg_vec)

    if show_ncc_vulnerability and ncc_incidents:
        fg_vuln = folium.FeatureGroup(
            name="Friction · NCC infrastructure vulnerability",
            show=True,
        ).add_to(m)
        for row in ncc_incidents:
            rid = str(row.get("id", ""))[:64]
            asset = str(row.get("asset", "Infrastructure"))[:120]
            tip = f"{rid} · {asset}"[:220]
            folium.CircleMarker(
                location=[float(row["lat"]), float(row["lon"])],
                radius=6,
                color=CRIMSON_VULN,
                weight=1.35,
                fill=True,
                fillColor=CRIMSON_VULN,
                fillOpacity=0.52,
                opacity=0.9,
                pane="frictionVulnerability",
                className="gcslc-friction-node gcslc-friction-ncc-vuln",
                tooltip=folium.Tooltip(tip, sticky=True),
            ).add_to(fg_vuln)

    if show_cbn_access and cbn_points:
        fg_cbn = folium.FeatureGroup(
            name="Friction · CBN financial access",
            show=True,
        ).add_to(m)
        for row in cbn_points:
            lbl = str(row.get("label", "Financial access"))[:140]
            rid = str(row.get("id", ""))[:48]
            tip = f"{lbl}" + (f" · {rid}" if rid else "")
            tip = tip[:220]
            folium.CircleMarker(
                location=[float(row["lat"]), float(row["lon"])],
                radius=4,
                color=CBN_ACCESS_ACCENT,
                weight=1,
                fill=True,
                fillColor=CBN_ACCESS_ACCENT,
                fillOpacity=0.45,
                opacity=0.82,
                pane="frictionCBN",
                className="gcslc-friction-node gcslc-friction-cbn",
                tooltip=folium.Tooltip(tip, sticky=True),
            ).add_to(fg_cbn)

    if show_social_hubs and social_points:
        fg_soc = folium.FeatureGroup(
            name="Friction · Social service hubs",
            show=True,
        ).add_to(m)
        for row in social_points:
            lbl = str(row.get("label", "Social hub"))[:140]
            cls = str(row.get("hub_class", ""))[:64]
            tip = f"{lbl}" + (f" · {cls}" if cls else "")
            tip = tip[:220]
            folium.CircleMarker(
                location=[float(row["lat"]), float(row["lon"])],
                radius=4,
                color=SOCIAL_HUB_ACCENT,
                weight=1,
                fill=True,
                fillColor=SOCIAL_HUB_ACCENT,
                fillOpacity=0.42,
                opacity=0.8,
                pane="frictionSocial",
                className="gcslc-friction-node gcslc-friction-social",
                tooltip=folium.Tooltip(tip, sticky=True),
            ).add_to(fg_soc)

    Fullscreen(
        position="topright",
        title="Full screen (mobile)",
        title_cancel="Exit full screen",
    ).add_to(m)
    folium.LayerControl(collapsed=True).add_to(m)
    _inject_drill_panes_atomic_fps(
        m,
        ZOOM_LGA_EMERGE,
        ZOOM_WARD_EMERGE,
        ZOOM_ATOM_EMERGE,
        True,
    )
    return m


# Nigeria sovereign viewport lock — fractional overlay on the federation hero canvas (774 LGA lattice lives here).
# Sentinel XY fractions are clamped to this rectangle (Python patrol + parent-window KGE_NG must stay identical).
_NG_FRAC_X0 = 0.20
_NG_FRAC_X1 = 0.78
_NG_FRAC_Y0 = 0.22
_NG_FRAC_Y1 = 0.74


def _kgec_clamp_nigeria_fraction(pt: dict[str, float]) -> dict[str, float]:
    """Geofence — K-GEC sentinel stays inside sovereign canvas (no Chad/Niger drift)."""
    x = max(_NG_FRAC_X0, min(_NG_FRAC_X1, float(pt["x"])))
    y = max(_NG_FRAC_Y0, min(_NG_FRAC_Y1, float(pt["y"])))
    return {"x": round(x, 4), "y": round(y, 4)}


def _kgec_sniff_lines_from_shouts(shouts: list[dict]) -> list[str]:
    """Cyan typewriter payloads: Trade velocity · infra voids · security friction — ward keyed."""
    lines: list[str] = []
    for s in shouts[:22]:
        pulse = str(s.get("pulse") or "liquidity")
        if pulse == "friction":
            cat = "Security / infrastructure friction"
        elif pulse == "liquidity":
            cat = "Trade velocity"
        else:
            cat = "Opportunity corridor"
        h = str(s.get("headline", ""))[:82]
        d = str(s.get("detail", ""))[:102]
        wid = hashlib.sha256(f"{h}|{d}".encode()).hexdigest()[:6].upper()
        lines.append(
            f"K-GEC · Komi-Generative Cloud · sovereign ward W-{wid} · {cat} · {h} — {d}"
        )
    if not lines:
        lines = [
            "K-GEC · Komi-Generative Cloud · national lattice · Trade velocity standby — mount trade_commerce_nodes.",
            "K-GEC · Komi-Generative Cloud · infrastructure void sniff — telecom / signal registries idle.",
            "K-GEC · Komi-Generative Cloud · security friction channel — NCC / vigil rows pending.",
        ]
    return lines


def _kgec_ntw_resonance_sniffs(operator: str) -> list[str]:
    """Bind eagle sniff line to National Resonance corridor audit for the active Big-4 operator."""
    from ntw_regional_audit import _operator_corridor_means

    blob = _load_ntw_regional_audit_live()
    cov_m, sim_m = _operator_corridor_means(blob, operator)
    n_corr = len(blob.get("corridors") or [])
    return [
        f"K-GEC Sentinel · National Resonance · {operator} · corridor RAN μ {cov_m:.1f}% · "
        f"SIM μ {sim_m:.1f}% · audit rows {n_corr} — forensic soul LIVE",
    ]


def _kgec_patrol_bundle(
    shouts: list[dict],
    *,
    extra_sniffs: list[str] | None = None,
) -> dict[str, Any]:
    """Parent-window patrol: geofenced targets + sniff lines for eagle typewriter."""
    raw = _kgec_hover_targets(shouts)
    sniffs = list(extra_sniffs or []) + _kgec_sniff_lines_from_shouts(shouts)
    return {
        "targets": [_kgec_clamp_nigeria_fraction(p) for p in raw],
        "sniffs": sniffs,
    }


def _kgec_ward_patrol_grid(*, cols: int = 9, rows: int = 7) -> list[dict[str, float]]:
    """Normalized iframe fractions — dense ward-by-ward patrol mesh over the national canvas."""
    out: list[dict[str, float]] = []
    for r in range(rows):
        for c in range(cols):
            x = 0.05 + (c + 0.5) / cols * 0.90
            y = 0.07 + (r + 0.5) / rows * 0.86
            out.append(_kgec_clamp_nigeria_fraction({"x": x, "y": y}))
    return out


def _kgec_nav_targets_from_shouts(shouts: list[dict], *, n: int = 14) -> list[dict[str, float]]:
    """Fractional map positions (0–1) derived from shout text — K-GEC hover sentinel glides ward-to-ward."""
    out: list[dict[str, float]] = []
    for i, s in enumerate(shouts[: max(1, n)]):
        blob = f"{s.get('headline', '')}|{s.get('detail', '')}|{i}"
        h = int(hashlib.sha256(blob.encode()).hexdigest()[:12], 16)
        x = 0.08 + (h % 840) / 1000.0
        y = 0.10 + ((h // 840) % 820) / 1000.0
        out.append(_kgec_clamp_nigeria_fraction({"x": x, "y": y}))
    if not out:
        out = [_kgec_clamp_nigeria_fraction({"x": 0.52, "y": 0.44})]
    return out


def _kgec_azk_corridor_fractional() -> list[dict[str, float]]:
    """
    Abuja → Kaduna → Zaria → Kano as normalized fractions over the Folium iframe (north-up; y grows downward).
    """
    raw = [
        {"x": 0.38, "y": 0.55},
        {"x": 0.41, "y": 0.48},
        {"x": 0.44, "y": 0.40},
        {"x": 0.47, "y": 0.33},
        {"x": 0.51, "y": 0.24},
    ]
    return [_kgec_clamp_nigeria_fraction(p) for p in raw]


def _kgec_hover_targets(shouts: list[dict]) -> list[dict[str, float]]:
    """Ward mesh first — AZK + shout pockets interleaved — sentinel banks lattice cell-by-cell."""
    corridor = _kgec_azk_corridor_fractional()
    grid = _kgec_ward_patrol_grid(cols=11, rows=9)
    pockets = _kgec_nav_targets_from_shouts(shouts, n=max(28, min(len(shouts), 32)))
    out: list[dict[str, float]] = []
    n_steps = min(220, max(len(grid) * 2, 48))
    for i in range(n_steps):
        out.append(grid[i % len(grid)])
        if i % 2 == 0:
            out.append(corridor[i % len(corridor)])
        if pockets and i % 3 == 0:
            out.append(pockets[(i // 3) % len(pockets)])
    return [_kgec_clamp_nigeria_fraction(p) for p in (out[:140] if out else grid[:40])]


def _kgec_cell_head(title: str) -> None:
    """Mono-terminal section title — slow kinetic ticker (no static glyphs)."""
    mq = _kgec_marquee_pair(title, seconds=52.0)
    st.markdown(
        f'<p class="kgec-mono-head kgec-rc-ticker-line">{mq}</p>',
        unsafe_allow_html=True,
    )


def _kgec_sidebar_cap_mq(text: str, *, seconds: float = 42.0) -> None:
    """Sidebar explanatory line as horizontal slow-motion ticker (replaces static caption)."""
    inner = _kgec_marquee_pair(text, seconds=seconds)
    st.markdown(
        f"<div class='kgec-sidebar-cap-line kgec-rc-ticker-line'>{inner}</div>",
        unsafe_allow_html=True,
    )


def _kgec_kinetic_note(text: str, *, seconds: float = 38.0) -> None:
    """Main-column kinetic line (strike banner, Streamlit hints, NTW fallback)."""
    st.markdown(
        f"<div class='kgec-kinetic-note kgec-rc-ticker-line'>{_kgec_marquee_pair(text, seconds=seconds)}</div>",
        unsafe_allow_html=True,
    )


def _kgec_sidebar_section() -> Any:
    """Bordered mono-terminal cell (Streamlit ≥1.33); plain container fallback."""
    try:
        return st.sidebar.container(border=True)
    except TypeError:
        return st.sidebar.container()


def _html_eagle_ticker(shouts: list[dict], *, alert_pulse: bool) -> str:
    parts: list[str] = []
    for s in (shouts or [])[:14]:
        pulse = str(s.get("pulse") or "")
        cls = (
            "p-friction"
            if pulse == "friction"
            else "p-opportunity"
            if pulse == "opportunity"
            else "p-liquidity"
        )
        h = html.escape(str(s.get("headline", ""))[:92])
        d = html.escape(str(s.get("detail", ""))[:118])
        parts.append(f"<span class='eagle-shout {cls}'><b>{h}</b> — {d}</span>")
    if not parts:
        parts.append(
            "<span class='eagle-shout p-opportunity'><b>K-GEC · Komi-Generative Cloud</b> — "
            "national lattice armed · mount vigil / trade / NCC rows for live shouts</span>"
        )
    inner = "<span class='eagle-sep'> · </span>".join(parts)
    shell_cls = (
        "eagle-ticker-shell eagle-stable-sky"
        + (" eagle-alert-pulse" if alert_pulse else "")
    )
    mq_mark = _kgec_marquee_pair(
        "◆ K-GEC · Komi-Generative Cloud ◆ sovereign sentinel ◆ Nigerian lattice LIVE ◆",
        seconds=84.0,
    )
    _crest_anchor = (
        "<span class='kgec-crest-anchor'>K-GEC · Komi-Generative Cloud</span>"
        "<span class='kgec-crest-anchor-sub'> intelligence crest · ward-sniff patrol</span>"
    )
    mq_sub = _kgec_marquee_pair(
        "K-GEC · Komi-Generative Cloud · trade velocity · infrastructure voids · security friction · kinetic only",
        seconds=96.0,
    )
    mq_live = _kgec_marquee_pair(
        "K-GEC · Komi-Generative Cloud · HOVER · PATROL · SNIFF · LIVE",
        seconds=78.0,
    )
    mq_lbl = _kgec_marquee_pair(
        "K-GEC · Komi-Generative Cloud · intelligence stream · cinematic cyan cadence",
        seconds=88.0,
    )
    return (
        "<div class='kgec-sentinel-stack'>"
        "<div class='kgec-sentinel-crest' aria-hidden='true'>"
        f"<span class='kgec-crest-mark kgec-crest-mq'>{mq_mark}</span>"
        f"<span class='kgec-crest-title kgec-crest-anchor-wrap'>{_crest_anchor}</span>"
        f"<span class='kgec-crest-sub kgec-crest-mq'>{mq_sub}</span>"
        f"<span class='kgec-crest-live kgec-crest-mq'>{mq_live}</span>"
        "</div>"
        f"<div class='{shell_cls}'>"
        "<div id='kgec-eagle-sniff-line' class='kgec-eagle-sniff-typewriter' "
        "aria-live='polite' aria-atomic='true'></div>"
        f"<span class='eagle-ticker-label'><span class='kgec-eagle-lbl-mq'>{mq_lbl}</span></span>"
        f"<div class='eagle-ticker-scroll eagle-typewriter-cyan'>{inner}</div>"
        "</div></div>"
    )


EAGLE_VOICE_INTERVAL = timedelta(seconds=28)


def _eagle_voice_fragment_body() -> None:
    _ntw_op = str(st.session_state.get("ntw_resonance_pick") or "MTN").strip()
    if not st.session_state.get("generative_eagle_ticker", True):
        st.components.v1.html(
            "<script>try{var p=window.parent;var d="
            + json.dumps(
                _kgec_patrol_bundle([], extra_sniffs=_kgec_ntw_resonance_sniffs(_ntw_op))
            )
            + ";if(p&&p.__kgecSetPatrol)p.__kgecSetPatrol(d);}catch(e){}</script>",
            height=0,
            width=0,
        )
        return
    vr = _load_vigil_registry_events()
    se = _load_signal_blackout_events()
    ncc = _load_ncc_vulnerability_incidents()
    cbn = _load_cbn_financial_points()
    trade = _load_trade_commerce_nodes()
    fin = _load_financial_inclusion_pos()
    vf = merge_vigil_sources(vr, se, fuse_blackouts=True, limit=100)
    shouts = collect_eagle_shouts(
        vigil_rows=vf,
        ncc_rows=ncc,
        cbn_rows=cbn,
        trade_rows=trade,
        signal_rows=se,
        fin_rows=fin,
        limit=16,
    )
    pulse = bool(st.session_state.get("eagle_friction_pulse", True)) and friction_alert_active(shouts)
    tick_html = _html_eagle_ticker(shouts, alert_pulse=pulse)
    _patrol = _kgec_patrol_bundle(
        shouts,
        extra_sniffs=_kgec_ntw_resonance_sniffs(_ntw_op),
    )
    st.components.v1.html(
        "<script>try{var p=window.parent;var d="
        + json.dumps(_patrol)
        + ";if(p&&p.__kgecSetPatrol)p.__kgecSetPatrol(d);}catch(e){}</script>",
        height=0,
        width=0,
    )
    if tick_html:
        st.markdown(tick_html, unsafe_allow_html=True)


_eagle_frag = getattr(st, "fragment", None)
if _eagle_frag:
    _eagle_voice_live = _eagle_frag(run_every=EAGLE_VOICE_INTERVAL)(_eagle_voice_fragment_body)
else:
    _eagle_voice_live = _eagle_voice_fragment_body


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
  var resizeT = null;
  function pulseResize(){
    try { topWin.dispatchEvent(new Event('resize')); } catch (e1) {}
    try {
      var doc = topWin.document;
      var fol = doc.querySelector('[data-testid="stIFrame"]')
        || doc.querySelector('iframe[title*="folium"], iframe[title*="streamlit_folium"]');
      if (fol) {
        try {
          var w = fol.contentWindow;
          if (w) w.dispatchEvent(new Event('resize'));
        } catch (e2) {}
      }
    } catch (e3) {}
  }
  function debouncedResize(){
    if (resizeT) clearTimeout(resizeT);
    resizeT = setTimeout(pulseResize, 420);
  }
  topWin.addEventListener('orientationchange', function(){ setTimeout(pulseResize, 420); });
  topWin.addEventListener('resize', debouncedResize);
})();
(function kgecHoverSentinel(){
  try {
    var p = window.parent;
    var doc = p.document;
    if (p.__kgecHoverEngine) return;
    p.__kgecHoverEngine = true;
    p.__kgecTargets = [{x:0.5,y:0.45}];
    p.__kgecSniffs = [];
    /* National canvas residency — mirrors app.py _NG_FRAC_* (federation / 774 LGA mirror, not neighbor drift). */
    var KGE_NG = { xmin: 0.20, xmax: 0.78, ymin: 0.22, ymax: 0.74 };
    function kgecClampNG(pt){
      return {
        x: Math.min(KGE_NG.xmax, Math.max(KGE_NG.xmin, Number(pt.x))),
        y: Math.min(KGE_NG.ymax, Math.max(KGE_NG.ymin, Number(pt.y)))
      };
    }
    p.__kgecSetPatrol = function(obj){
      try {
        if (!obj || typeof obj !== 'object') return;
        if (Array.isArray(obj.targets) && obj.targets.length)
          p.__kgecTargets = obj.targets.map(kgecClampNG);
        if (Array.isArray(obj.sniffs))
          p.__kgecSniffs = obj.sniffs.map(function(s){ return String(s); });
      } catch (ePat) {}
    };
    p.__kgecSetTargets = function(arr){
      try {
        if (Array.isArray(arr) && arr.length) p.__kgecTargets = arr.map(kgecClampNG);
      } catch (eTgt) {}
    };
    p.__kgecIdx = 0;
    p.__kgecSvgUid = 0;
    var sniffTw = null;
    if (!doc.getElementById('kgec-eagle-keyframes')){
      var st = doc.createElement('style');
      st.id = 'kgec-eagle-keyframes';
      st.textContent = '@keyframes kgecEagleIdle{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-1.2px) scale(1.01)}}'
        + '@keyframes kgecEagleSniffPulse{0%,100%{filter:drop-shadow(0 0 16px rgba(255,215,80,0.95)) drop-shadow(0 0 8px rgba(0,229,255,0.45));}'
        + '50%{filter:drop-shadow(0 0 28px rgba(255,236,140,1)) drop-shadow(0 0 14px rgba(0,229,255,0.6)) brightness(1.08);}}'
        + '.kgec-eagle-float{animation:kgecEagleIdle 5.8s ease-in-out infinite;transform-origin:180px 95px;}'
        + '.kgec-eagle-svg.kgec-eagle-sniff-pulse{animation:kgecEagleSniffPulse 1.15s ease-in-out 1;}';
      doc.head.appendChild(st);
    }
    function eagleMarkup(uid){
      return '<defs>'
        + '<linearGradient id="'+uid+'_gld" x1="0%" y1="0%" x2="100%" y2="100%">'
        + '<stop offset="0%" stop-color="#FFF4BD"/><stop offset="28%" stop-color="#E8C547"/>'
        + '<stop offset="62%" stop-color="#BF953F"/><stop offset="100%" stop-color="#4a3706"/></linearGradient>'
        + '<linearGradient id="'+uid+'_wng" x1="0%" y1="50%" x2="100%" y2="50%">'
        + '<stop offset="0%" stop-color="#8B6914"/><stop offset="50%" stop-color="#D4AF37"/>'
        + '<stop offset="100%" stop-color="#3d2e08"/></linearGradient>'
        + '<linearGradient id="'+uid+'_brz" x1="50%" y1="0%" x2="50%" y2="100%">'
        + '<stop offset="0%" stop-color="#C9A227"/><stop offset="100%" stop-color="#5c4308"/></linearGradient>'
        + '<filter id="'+uid+'_hl"><feGaussianBlur stdDeviation="1.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        + '<filter id="'+uid+'_sh"><feDropShadow dx="0" dy="3" stdDeviation="2" flood-color="#000" flood-opacity="0.55"/></filter>'
        + '</defs>'
        + '<g class="kgec-eagle-float">'
        + '<g class="kgec-eagle-bank" filter="url(#'+uid+'_sh)">'
        + '<path fill="url(#'+uid+'_wng)" stroke="#1a1408" stroke-width="1.4" '
        + 'd="M18 118 Q44 72 72 88 Q52 108 38 124 Q26 122 18 118 Z"/>'
        + '<path fill="url(#'+uid+'_wng)" stroke="#1a1408" stroke-width="1.4" '
        + 'd="M282 122 Q248 78 220 90 Q242 110 258 128 Q272 126 282 122 Z"/>'
        + '<path fill="url(#'+uid+'_gld)" stroke="#1a1408" stroke-width="1.9" filter="url(#'+uid+'_hl)" '
        + 'd="M48 98 Q58 52 128 44 Q198 38 252 68 Q238 96 188 108 Q128 118 78 110 Q52 104 48 98 Z"/>'
        + '<path fill="url(#'+uid+'_brz)" stroke="#1a1408" stroke-width="1.5" opacity="0.95" '
        + 'd="M72 58 Q110 24 188 30 Q232 36 244 64 Q200 52 140 58 Q96 60 72 58 Z"/>'
        + '<path fill="url(#'+uid+'_wng)" stroke="#1a1408" stroke-width="1.3" opacity="0.92" '
        + 'd="M84 78 Q128 58 210 66 Q228 78 198 92 Q152 86 100 94 Z"/>'
        + '<path fill="url(#'+uid+'_gld)" stroke="#1a1408" stroke-width="1.6" '
        + 'd="M248 70 Q272 58 302 78 Q292 98 264 92 Q252 80 248 70 Z"/>'
        + '<path fill="#2a1f0a" stroke="#D4AF37" stroke-width="1.2" '
        + 'd="M285 78 L318 84 L302 98 Q292 90 285 78 Z"/>'
        + '<circle cx="278" cy="82" r="5" fill="#0a1628" stroke="#FFD966" stroke-width="1.5"/>'
        + '<circle cx="276" cy="80" r="1.6" fill="#E8F4FF"/>'
        + '<path fill="none" stroke="#4a3706" stroke-width="2.2" stroke-linecap="round" opacity="0.88" '
        + 'd="M124 98 Q168 108 208 88"/>'
        + '<path fill="none" stroke="#D4AF37" stroke-width="1" stroke-linecap="round" opacity="0.45" '
        + 'd="M56 108 Q96 124 140 118"/>'
        + '</g>'
        + '<text x="6" y="188" fill="#D4AF37" font-size="10" font-weight="800" font-family="ui-monospace,monospace">K-GEC · Sentinel</text>'
        + '<text x="168" y="188" fill="#00E5FF" font-size="9" font-weight="700" font-family="ui-monospace,monospace">National Resonance · geofenced</text>'
        + '</g>';
    }
    function mapHost(){
      var main = doc.querySelector('section.main') || doc.body;
      var inner = main.querySelector('iframe[title*="folium"], iframe[title*="streamlit_folium"], iframe[title*="Folium"]');
      if (inner) return inner;
      var shell = main.querySelector('[data-testid="stIFrame"]');
      if (shell) {
        var nested = shell.querySelector('iframe');
        if (nested) return nested;
        return shell;
      }
      return doc.querySelector('iframe[title*="folium"], iframe[title*="streamlit_folium"]');
    }
    function ensureLayer(){
      var host = mapHost();
      if (!host) return null;
      var par = host.parentElement;
      if (!par) return null;
      par.style.position = 'relative';
      var layer = doc.getElementById('kgec-eagle-hover-layer');
      if (layer && !par.contains(layer)) {
        try { layer.remove(); } catch (eR) {}
        layer = null;
        p.__kgecEagleEl = null;
        p.__kgecEagleBank = null;
      }
      if (!layer) {
        layer = doc.createElement('div');
        layer.id = 'kgec-eagle-hover-layer';
        layer.setAttribute('aria-hidden','true');
        layer.style.cssText = 'position:absolute;left:0;top:0;right:0;bottom:0;pointer-events:none;overflow:visible;z-index:950;border-radius:14px;transform:translateZ(0);backface-visibility:hidden;-webkit-backface-visibility:hidden;';
        par.appendChild(layer);
        var svg = doc.createElementNS('http://www.w3.org/2000/svg','svg');
        svg.setAttribute('class','kgec-eagle-svg');
        svg.setAttribute('viewBox','0 0 340 200');
        svg.setAttribute('preserveAspectRatio','xMidYMid meet');
        svg.style.cssText = 'position:absolute;width:min(168px,34vw);height:min(102px,21vw);min-width:132px;min-height:80px;left:45%;top:40%;'
          + 'filter:drop-shadow(0 0 20px rgba(255,215,80,0.98)) drop-shadow(0 0 10px rgba(0,0,0,0.92)) drop-shadow(0 6px 18px rgba(0,0,0,0.68));'
          + 'transition:left 2.1s cubic-bezier(0.22,0.08,0.18,1),top 2.1s cubic-bezier(0.22,0.08,0.18,1);will-change:transform,left,top;'
          + 'transform:translate3d(-50%,-50%,0);opacity:1;visibility:visible;';
        p.__kgecSvgUid = (p.__kgecSvgUid || 0) + 1;
        svg.innerHTML = eagleMarkup('kgec'+p.__kgecSvgUid);
        layer.appendChild(svg);
        p.__kgecEagleEl = svg;
        p.__kgecEagleBank = svg.querySelector('.kgec-eagle-bank');
      }
      return layer;
    }
    var GLIDE_MS = 2100;
    var DWELL_MS = 3400;
    var KGE_CYCLE = GLIDE_MS + DWELL_MS;
    function clearSniffAnim(){
      var svg0 = p.__kgecEagleEl;
      if (svg0) svg0.classList.remove('kgec-eagle-sniff-pulse');
      if (sniffTw) { clearInterval(sniffTw); sniffTw = null; }
    }
    function fireSniffLine(stepIdx){
      var sniffs = p.__kgecSniffs || [];
      if (!sniffs.length) return;
      var msg = String(sniffs[Math.max(0, stepIdx) % sniffs.length] || '');
      var el = doc.getElementById('kgec-eagle-sniff-line');
      if (!el) return;
      el.textContent = '';
      var i = 0;
      if (sniffTw) clearInterval(sniffTw);
      sniffTw = setInterval(function(){
        if (i > msg.length) { clearInterval(sniffTw); sniffTw = null; return; }
        el.textContent = msg.slice(0, i);
        i++;
      }, 17);
    }
    function majesticStep(){
      clearSniffAnim();
      var svg = p.__kgecEagleEl;
      if (!svg || !doc.body.contains(svg)) {
        p.__kgecEagleEl = null;
        p.__kgecEagleBank = null;
        ensureLayer();
        svg = p.__kgecEagleEl;
      }
      if (!svg) {
        p.__kgecMajestyT = setTimeout(majestyLoop, 600);
        return;
      }
      var tg = p.__kgecTargets || [{x:0.5,y:0.45}];
      var idx = p.__kgecIdx % tg.length;
      var w = kgecClampNG(tg[idx]);
      p.__kgecIdx++;
      svg.style.transition = 'left '+ (GLIDE_MS/1000) +'s cubic-bezier(0.22,0.06,0.18,1), top '+ (GLIDE_MS/1000) +'s cubic-bezier(0.22,0.06,0.18,1)';
      svg.style.opacity = '1';
      svg.style.visibility = 'visible';
      svg.style.left = (w.x * 100) + '%';
      svg.style.top = (w.y * 100) + '%';
      var bank = p.__kgecEagleBank || svg.querySelector('.kgec-eagle-bank');
      if (bank) bank.setAttribute('transform','rotate('+ (Math.sin(p.__kgecIdx * 0.42) * 14) +' 180 95)');
      var stepForSniff = p.__kgecIdx - 1;
      setTimeout(function(){
        var svg2 = p.__kgecEagleEl;
        if (!svg2 || !doc.body.contains(svg2)) return;
        svg2.classList.add('kgec-eagle-sniff-pulse');
        fireSniffLine(stepForSniff);
      }, GLIDE_MS);
    }
    function majestyLoop(){
      majesticStep();
      p.__kgecMajestyT = setTimeout(majestyLoop, KGE_CYCLE);
    }
    function mountRetries(){
      var n = 0;
      function tick(){
        ensureLayer();
        if (!p.__kgecEagleEl && n < 14) { n++; setTimeout(tick, 420); }
      }
      tick();
    }
    mountRetries();
    setTimeout(function(){ majestyLoop(); }, 500);
    setInterval(function(){
      var host = mapHost();
      var layer = doc.getElementById('kgec-eagle-hover-layer');
      if (host && (!layer || !host.parentElement || !host.parentElement.contains(layer))) ensureLayer();
    }, 1600);
  } catch (e) {}
})();
</script>
""",
    height=0,
    width=0,
)

# First main paint · Eagle nav targets + ticker (fragment updates AZK hover even when ticker off)
_eagle_voice_live()

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
  animation: mirror-pulse-zoom 4.5s ease-in-out infinite;
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
  animation: mirror-manifesto-shimmer 10s linear infinite;
}}
@keyframes mirror-pulse-zoom {{
  0%, 100% {{ transform: scale(1); filter: brightness(1); }}
  50% {{ transform: scale(1.025); filter: brightness(1.08); }}
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
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  font-size: 0.65rem;
  letter-spacing: 0.06em;
  word-spacing: 0.35em;
  color: rgba(212, 175, 55, 0.62) !important;
}}
/* K-GEC sentinel stack — first paint on iPhone · stable strip */
.kgec-sentinel-stack {{
  position: sticky !important;
  top: 0 !important;
  z-index: 5200 !important;
  padding-top: max(6px, env(safe-area-inset-top, 0px)) !important;
  margin: 0 0 22px 0 !important;
  padding-left: 4px !important;
  padding-right: 4px !important;
  isolation: isolate !important;
  overflow: visible !important;
}}
.kgec-crest-mq {{
  flex: 1 1 120px !important;
  min-width: 0 !important;
  max-width: 100% !important;
}}
.kgec-crest-mq .kgec-mq {{
  max-width: 100% !important;
}}
.kgec-eagle-lbl-mq {{
  display: block !important;
  overflow: hidden !important;
  margin-bottom: 6px !important;
}}
.kgec-sentinel-crest {{
  display: flex !important;
  flex-wrap: wrap !important;
  align-items: center !important;
  gap: 8px 12px !important;
  margin-bottom: 8px !important;
  padding: 6px 10px !important;
  border-radius: 10px !important;
  background: linear-gradient(90deg, rgba(0,0,0,0.95) 0%, rgba(0,20,80,0.75) 50%, rgba(0,0,0,0.92) 100%) !important;
  border: 1px solid rgba(212, 175, 55, 0.5) !important;
  box-shadow: 0 0 24px rgba(0, 229, 255, 0.12), inset 0 1px 0 rgba(255,255,255,0.08) !important;
}}
.kgec-crest-mark {{ color: #D4AF37 !important; font-size: 0.95rem !important; }}
.kgec-crest-anchor-wrap {{
  flex: 2 1 200px !important;
  min-width: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 2px !important;
}}
.kgec-crest-anchor {{
  font-weight: 800 !important;
  letter-spacing: 0.1em !important;
  font-size: clamp(0.74rem, 2.4vw, 0.95rem) !important;
  color: #D4AF37 !important;
  text-shadow: 0 1px 2px rgba(0,0,0,0.85) !important;
}}
.kgec-crest-anchor-sub {{
  font-weight: 600 !important;
  letter-spacing: 0.06em !important;
  font-size: clamp(0.62rem, 1.85vw, 0.78rem) !important;
  color: rgba(212, 175, 55, 0.78) !important;
}}
.kgec-crest-title {{
  font-weight: 800 !important;
  letter-spacing: 0.12em !important;
  font-size: clamp(0.72rem, 2.35vw, 0.92rem) !important;
  color: #D4AF37 !important;
}}
.kgec-crest-sub {{
  font-family: ui-monospace, monospace !important;
  font-size: clamp(0.68rem, 2.1vw, 0.86rem) !important;
  color: #00E5FF !important;
  letter-spacing: 0.07em !important;
}}
.kgec-crest-live {{
  margin-left: auto !important;
  font-size: clamp(0.65rem, 2vw, 0.8rem) !important;
  font-weight: 800 !important;
  color: #2ECC71 !important;
  letter-spacing: 0.2em !important;
  border: 1px solid rgba(46, 204, 113, 0.45) !important;
  padding: 3px 8px !important;
  border-radius: 6px !important;
  opacity: 0.96 !important;
  box-shadow: 0 0 10px rgba(46,204,113,0.22) !important;
  animation: none !important;
}}
@keyframes eagle-live-breathe {{
  0%, 100% {{ opacity: 0.85; box-shadow: 0 0 0 0 rgba(46,204,113,0); }}
  50% {{ opacity: 1; box-shadow: 0 0 14px rgba(46,204,113,0.35); }}
}}
/* Inner ticker strip (outer .kgec-sentinel-stack is the sticky anchor) */
.eagle-stable-sky {{
  position: relative !important;
  margin: 0 !important;
  padding: 8px 10px 10px !important;
  background: #000000 !important;
  border-radius: 12px !important;
  border: 1px solid rgba(212, 175, 55, 0.42) !important;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.55) !important;
  overflow: visible !important;
}}
.kgec-eagle-sniff-typewriter {{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  font-size: clamp(0.72rem, 2.2vw, 0.9rem) !important;
  font-weight: 600 !important;
  color: #00E5FF !important;
  letter-spacing: 0.06em !important;
  line-height: 1.45 !important;
  min-height: 2.35em !important;
  margin: 0 0 8px 0 !important;
  padding: 8px 10px !important;
  border-radius: 8px !important;
  border-left: 3px solid rgba(0, 229, 255, 0.55) !important;
  background: rgba(0, 20, 60, 0.55) !important;
  text-shadow: 0 0 12px rgba(0, 229, 255, 0.25) !important;
  word-break: break-word !important;
}}
.eagle-typewriter-cyan .eagle-shout,
.eagle-typewriter-cyan .eagle-shout b {{
  color: #00E5FF !important;
  font-weight: 600 !important;
}}
.eagle-typewriter-cyan .eagle-shout.p-friction {{
  text-shadow: 0 0 12px rgba(255, 80, 80, 0.35) !important;
}}
.eagle-typewriter-cyan .eagle-shout.p-opportunity {{
  text-shadow: 0 0 12px rgba(46, 204, 113, 0.35) !important;
}}
.eagle-typewriter-cyan .eagle-shout.p-liquidity {{
  text-shadow: 0 0 12px rgba(201, 162, 39, 0.35) !important;
}}
.eagle-typewriter-cyan .eagle-sep {{
  color: rgba(0, 229, 255, 0.45) !important;
}}
/* Full-canvas Folium host — fluid width + viewport height (MacBook / iPhone) */
section.main .gcslc-map-canvas-host,
section.main [data-testid="stIFrame"] {{
  position: relative !important;
  z-index: 2 !important;
}}
.gcslc-map-canvas-host {{
  width: 100% !important;
  margin: 0 !important;
  padding: 0 !important;
}}
.gcslc-map-canvas-host iframe,
iframe[title*="folium"],
iframe[title*="streamlit_folium"] {{
  width: 100% !important;
  min-height: min(560px, 82vh) !important;
  height: min(560px, 82vh) !important;
  min-height: min(560px, 82dvh) !important;
  height: min(560px, 82dvh) !important;
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
  min-height: min(560px, 82vh) !important;
  min-height: min(560px, 82dvh) !important;
}}
/* iPhone / narrow — cap hero map so NTW Big 4 stays above the fold */
@media (max-width: 900px) {{
  .gcslc-map-canvas-host iframe,
  iframe[title*="folium"],
  iframe[title*="streamlit_folium"] {{
    min-height: 70vh !important;
    height: 70vh !important;
    max-height: 70vh !important;
  }}
  [data-testid="stIFrame"] {{
    min-height: 70vh !important;
    max-height: 70vh !important;
  }}
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
.sovereign-detail-widget .sdw-metric-lbl.kgec-rc-ticker-line {{
  overflow: hidden !important;
  max-width: 100% !important;
  min-height: 2.35em !important;
}}
.sovereign-detail-widget .sdw-meta {{
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px solid rgba(212, 175, 55, 0.2);
  font-size: clamp(0.68rem, 2vw, 0.78rem);
  line-height: 1.45;
  color: rgba(240, 244, 255, 0.78) !important;
}}
.kgec-sdw-strong {{
  margin-bottom: 6px !important;
}}
.sdw-meta-line {{
  margin-top: 8px !important;
  overflow: hidden !important;
  width: 100% !important;
}}
.kgec-kinetic-note {{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  font-size: 0.65rem !important;
  letter-spacing: 0.05em !important;
  word-spacing: 0.35em !important;
  margin: 8px 0 12px 0 !important;
  color: rgba(200, 245, 255, 0.9) !important;
}}
.footer-sovereign-row {{
  margin: 8px 0 !important;
  overflow: hidden !important;
  width: 100% !important;
}}
.block-container {{
  max-width: 100% !important;
  padding-top: 0.1rem !important;
  padding-left: 0.25rem !important;
  padding-right: 0.25rem !important;
}}
section.main .block-container {{
  padding-top: 0.15rem !important;
}}
.sdw-handshake {{
  margin-bottom: 14px;
  padding: 12px 14px;
  border-radius: 12px;
  border: 1px solid rgba(212, 175, 55, 0.35);
  background: rgba(0, 0, 128, 0.42);
  text-align: left;
}}
.sdw-handshake .sdw-hs-row {{
  display: block !important;
  overflow: hidden !important;
  width: 100% !important;
  margin-top: 12px !important;
}}
.sdw-handshake .sdw-hs-row:first-child {{
  margin-top: 0 !important;
}}
.sdw-handshake .kgec-mq-track span {{
  color: rgba(235, 248, 255, 0.96) !important;
  font-weight: 600 !important;
  font-size: clamp(0.64rem, 1.85vw, 0.88rem) !important;
  letter-spacing: 0.04em !important;
}}
.sdw-handshake .sdw-hs-brand {{
  display: block;
  color: #00E5FF !important;
  font-weight: 700;
  font-size: clamp(0.72rem, 2.2vw, 0.95rem);
  line-height: 1.45;
  text-shadow: 0 1px 5px rgba(0,0,0,0.85);
}}
.sdw-handshake .sdw-hs-rc {{
  display: block;
  margin-top: 10px;
  color: {GOLD} !important;
  font-weight: 700;
  font-size: clamp(0.78rem, 2.4vw, 1rem);
  text-shadow: 0 1px 6px rgba(0,0,0,0.8);
}}
.sdw-handshake .sdw-hs-man {{
  display: block;
  margin-top: 10px;
  font-size: clamp(0.65rem, 2vw, 0.78rem);
  line-height: 1.5;
  color: rgba(240, 244, 255, 0.88) !important;
}}
/* Total Reality · Smart click — handshake layer above resonance chamber */
.gcslc-total-reality.gcslc-tr-handshake-front {{
  position: relative !important;
  z-index: 100 !important;
  isolation: isolate !important;
}}
/* Total Reality · Smart click (Typewriter Cyan) */
.gcslc-total-reality {{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  background: rgba(0, 0, 128, 0.92) !important;
  border: 1px solid rgba(212, 175, 55, 0.48);
  border-radius: 12px;
  padding: 14px 16px;
  margin: 10px 0 14px 0;
  color: #00E5FF !important;
  box-shadow: 0 6px 20px rgba(0,0,0,0.35);
  touch-action: manipulation;
}}
.gcslc-total-reality .gcslc-tr-h {{
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-size: clamp(0.7rem, 2vw, 0.85rem);
  margin-bottom: 10px;
  color: #00E5FF !important;
  text-shadow: 0 1px 4px rgba(0,0,0,0.85);
}}
.gcslc-total-reality .gcslc-tr-line {{
  font-size: clamp(0.65rem, 1.9vw, 0.8rem);
  line-height: 1.5;
  margin-top: 6px;
  color: rgba(240, 244, 255, 0.9) !important;
}}
.gcslc-total-reality .gcslc-tr-k {{
  color: rgba(240, 244, 255, 0.65) !important;
  margin-right: 6px;
}}
/* Generative Eagle · ticker (iPhone scroll-safe · black strip inside Stable Sky) */
.eagle-ticker-shell {{
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: nowrap;
  margin: 0 !important;
  padding: 10px 12px;
  border-radius: 10px;
  background: #000000 !important;
  border: 1px solid rgba(212, 175, 55, 0.35) !important;
  max-width: 100%;
}}
.eagle-ticker-shell.eagle-alert-pulse {{
  animation: eagle-friction-warn 1.8s ease-in-out infinite;
  border-color: rgba(220, 20, 60, 0.55);
  box-shadow: 0 0 0 1px rgba(220, 20, 60, 0.25);
}}
@keyframes eagle-friction-warn {{
  0%, 100% {{ box-shadow: 0 0 0 0 rgba(220, 20, 60, 0.0); }}
  50% {{ box-shadow: 0 0 16px 2px rgba(220, 20, 60, 0.45); }}
}}
.eagle-ticker-label {{
  flex: 0 0 auto;
  font-size: clamp(0.68rem, 2vw, 0.82rem);
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: {GOLD} !important;
  text-shadow: 0 1px 3px rgba(0,0,0,0.8);
}}
.eagle-ticker-scroll {{
  flex: 1 1 auto;
  min-width: 0;
  overflow-x: auto;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
  white-space: nowrap;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: clamp(0.72rem, 2.15vw, 0.88rem);
  line-height: 1.4;
  padding-bottom: 2px;
}}
/* NTW — surface above map iframe stacking; never clipped by resize chrome */
.sovereign-ntw-big4 {{
  position: relative !important;
  z-index: 50 !important;
  isolation: isolate !important;
  margin: 6px 0 10px !important;
  padding: 12px 10px 14px !important;
  border-radius: 14px !important;
  background: linear-gradient(180deg, rgba(0,0,128,0.95) 0%, rgba(0,10,90,0.88) 100%) !important;
  border: 2px solid rgba(212,175,55,0.55) !important;
  box-shadow: 0 8px 28px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.12) !important;
  scroll-margin-top: 8px !important;
}}
.sovereign-ntw-big4-inner {{
  display: flex !important;
  flex-direction: row !important;
  flex-wrap: nowrap !important;
  align-items: stretch !important;
  justify-content: space-between !important;
  gap: 8px !important;
  width: 100% !important;
  box-sizing: border-box !important;
}}
@media (max-width: 420px) {{
  .sovereign-ntw-big4-inner {{
    flex-wrap: wrap !important;
    justify-content: center !important;
  }}
  .sovereign-ntw-chip {{
    flex: 1 1 calc(50% - 6px) !important;
    min-width: calc(50% - 6px) !important;
  }}
}}
/* NTW Sovereign Control Panel — below hero map */
.sovereign-ntw-panel-head {{
  font-family: inherit !important;
  font-size: clamp(0.72rem, 2vw, 0.88rem) !important;
  font-weight: 700 !important;
  letter-spacing: 0.06em !important;
  text-transform: uppercase !important;
  color: #D4AF37 !important;
  margin: 8px 0 6px !important;
  text-shadow: 0 1px 4px rgba(0,0,0,0.75);
}}
.sovereign-ntw-panel-head span {{
  color: rgba(240,244,255,0.88) !important;
  font-weight: 600 !important;
}}
.sovereign-ntw-sub {{
  font-size: clamp(0.62rem, 1.6vw, 0.72rem) !important;
  color: rgba(240,244,255,0.55) !important;
  margin: 0 0 8px 0 !important;
  letter-spacing: 0.06em !important;
}}
.sovereign-ntw-pedestal {{
  position: relative !important;
  z-index: 28 !important;
}}
.national-resonance-chamber-outer {{
  background: radial-gradient(120% 90% at 50% 0%, rgba(0,55,140,0.5) 0%, rgba(0,0,48,0.95) 52%, #000010 100%) !important;
  border: 1px solid rgba(212, 175, 55, 0.5) !important;
  box-shadow: 0 0 32px rgba(0, 229, 255, 0.08), inset 0 1px 0 rgba(255,255,255,0.07) !important;
}}
.national-rc-title {{
  letter-spacing: 0.1em !important;
  text-shadow: 0 0 20px rgba(212, 175, 55, 0.25) !important;
}}
.national-resonance-meterdeck {{
  margin: 0 0 8px 0 !important;
}}
/* NTW meter strip — National Resonance · meter deck */
.ntw-meter-strip {{
  display: grid !important;
  grid-template-columns: repeat(4, 1fr) !important;
  gap: 10px !important;
  margin: 0 0 14px 0 !important;
  padding: 14px 12px !important;
  border-radius: 12px !important;
  background: linear-gradient(180deg, rgba(0,0,0,0.75) 0%, rgba(0,15,60,0.55) 100%) !important;
  border: 1px solid rgba(212,175,55,0.4) !important;
  box-shadow: inset 0 2px 24px rgba(0, 229, 255, 0.06) !important;
}}
@media (max-width: 700px) {{
  .ntw-meter-strip {{ grid-template-columns: repeat(2, 1fr) !important; }}
}}
.ntw-meter-cell {{ min-width: 0 !important; }}
.ntw-meter-label {{
  font-family: ui-monospace, monospace !important;
  font-size: clamp(0.65rem, 2.4vw, 0.78rem) !important;
  font-weight: 800 !important;
  margin-bottom: 6px !important;
}}
.ntw-meter-label-mq {{
  overflow: hidden !important;
  width: 100% !important;
  max-width: 100% !important;
  min-height: 1.35em !important;
}}
.ntw-meter-track {{
  height: 12px !important;
  border-radius: 8px !important;
  background: linear-gradient(180deg, rgba(255,255,255,0.12) 0%, rgba(0,0,0,0.5) 100%) !important;
  overflow: hidden !important;
  border: 1px solid rgba(212,175,55,0.3) !important;
  box-shadow: inset 0 1px 3px rgba(0,0,0,0.65) !important;
}}
.ntw-meter-fill {{
  height: 100% !important;
  border-radius: 6px !important;
  transition: width 0.35s ease !important;
}}
.ntw-meter-sub {{
  font-family: ui-monospace, monospace !important;
  font-size: clamp(0.55rem, 1.5vw, 0.65rem) !important;
  color: rgba(240,244,255,0.72) !important;
  margin-top: 6px !important;
}}
.ntw-meter-mq-shell {{
  overflow: hidden !important;
  width: 100% !important;
  max-width: 100% !important;
}}
.kgec-rc-ticker-line {{
  overflow: hidden !important;
  width: 100% !important;
  display: block !important;
}}
.kgec-mq {{
  display: block !important;
  overflow: hidden !important;
  max-width: 100% !important;
}}
.kgec-mq-track {{
  display: inline-flex !important;
  gap: clamp(1.75rem, 5vw, 3.5rem) !important;
  white-space: nowrap !important;
  animation: kgecMqScroll var(--kgec-mq-dur, 52s) linear infinite !important;
  will-change: transform !important;
}}
@keyframes kgecMqScroll {{
  0% {{ transform: translate3d(0, 0, 0); }}
  100% {{ transform: translate3d(-50%, 0, 0); }}
}}
.ntw-push-inject {{
  display: flex !important;
  flex-wrap: wrap !important;
  align-items: flex-start !important;
  gap: 10px 14px !important;
  margin: 0 0 14px 0 !important;
  padding: 12px 14px !important;
  border-radius: 10px !important;
  background: linear-gradient(90deg, rgba(0,42,62,0.96) 0%, rgba(0,18,48,0.94) 100%) !important;
  border: 1px solid rgba(0, 229, 255, 0.42) !important;
  box-shadow: 0 0 28px rgba(46, 204, 113, 0.18), inset 0 1px 0 rgba(255,255,255,0.06) !important;
  min-height: 3.2rem !important;
}}
.ntw-push-inject-op {{
  flex: 0 0 auto !important;
  font-weight: 900 !important;
  font-size: clamp(0.68rem, 2vw, 0.82rem) !important;
  color: var(--ntw-push-accent, #D4AF37) !important;
  letter-spacing: 0.14em !important;
  font-family: ui-monospace, monospace !important;
}}
.ntw-push-inject-body {{
  flex: 1 1 220px !important;
  min-width: 0 !important;
}}
.ntw-push-inject-body .kgec-mq-track span {{
  color: rgba(230, 248, 255, 0.94) !important;
}}
.ntw-tw-v .kgec-mq {{
  display: inline-block !important;
  vertical-align: bottom !important;
  max-width: min(100%, 52rem) !important;
}}
/* Pulsing operator keys (Streamlit buttons — match label) */
@keyframes ntw-op-pulse {{
  0%, 100% {{ box-shadow: 0 0 0 0 rgba(0, 229, 255, 0.0); filter: brightness(1); transform: scale(1); }}
  50% {{ box-shadow: 0 0 26px 5px rgba(46, 204, 113, 0.42), 0 0 16px rgba(0, 229, 255, 0.5); filter: brightness(1.12); transform: scale(1.03); }}
}}
section.main button[aria-label="MTN"],
section.main button[aria-label="Airtel"],
section.main button[aria-label="Glo"],
section.main button[aria-label="9mobile"] {{
  animation: ntw-op-pulse 2.2s ease-in-out infinite !important;
  font-family: ui-monospace, monospace !important;
  font-weight: 700 !important;
  letter-spacing: 0.12em !important;
  word-spacing: 0.35em !important;
  will-change: transform, box-shadow !important;
}}
.sovereign-ntw-big4-inner {{
  contain: layout style !important;
}}
/* Cyan–green stream — always legible (no opacity blackout); motion = glide only */
@keyframes ntw-line-glide {{
  from {{ transform: translate3d(-14px, 0, 0); opacity: 0.82; }}
  to {{ transform: translate3d(0, 0, 0); opacity: 1; }}
}}
.ntw-tw-instant {{
  opacity: 1 !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 8px !important;
  margin: 0 0 12px 0 !important;
  padding: 10px 12px !important;
  border-radius: 8px !important;
  background: linear-gradient(90deg, rgba(0,50,40,0.9) 0%, rgba(0,25,60,0.88) 100%) !important;
  border: 1px solid rgba(46, 204, 113, 0.65) !important;
  box-shadow: 0 0 20px rgba(0, 229, 255, 0.2), inset 0 1px 0 rgba(255,255,255,0.08) !important;
  line-height: 1.5 !important;
  animation: none !important;
}}
.ntw-tw-instant .ntw-tw-k-mq,
.ntw-tw-instant .ntw-tw-v-mq {{
  display: block !important;
  overflow: hidden !important;
  width: 100% !important;
  max-width: 100% !important;
}}
.ntw-tw-instant .ntw-tw-k-mq .kgec-mq-track span {{
  color: #2ECC71 !important;
}}
.ntw-tw-instant .ntw-tw-v-mq .kgec-mq-track span {{
  color: #00E5FF !important;
}}
.ntw-cyan-green-stream {{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  background: radial-gradient(100% 120% at 0% 0%, rgba(0,72,88,0.42) 0%, rgba(0,18,42,0.94) 55%) !important;
  border: 1px solid rgba(46, 204, 113, 0.55) !important;
  border-radius: 10px !important;
  padding: 14px 14px 16px !important;
  margin-top: 12px !important;
  min-height: 140px !important;
  box-shadow: inset 0 0 48px rgba(0, 229, 255, 0.1), 0 8px 28px rgba(0,0,0,0.45) !important;
}}
.ntw-tw-rain.kgec-forensic-rain .ntw-tw-line,
.ntw-tw-rain .ntw-tw-line {{
  opacity: 1 !important;
  animation: ntw-line-glide 0.72s cubic-bezier(0.22, 1, 0.36, 1) both !important;
  animation-delay: calc((var(--tw-i, 1) - 1) * 28ms) !important;
}}
.kgec-ntw-stream-root[data-kgec-ntw-push] .ntw-tw-rain .ntw-tw-line {{
  animation-duration: 0.68s !important;
}}
.ntw-tw-line {{
  line-height: 1.55 !important;
  margin-bottom: 8px !important;
  font-size: clamp(0.62rem, 1.8vw, 0.76rem) !important;
}}
.ntw-tw-idx {{
  color: rgba(212, 175, 55, 0.65) !important;
  font-size: 0.62em !important;
  margin-right: 6px !important;
  font-family: inherit !important;
}}
.ntw-tw-k {{
  color: #2ECC71 !important;
  font-weight: 700 !important;
  margin-right: 8px !important;
}}
.ntw-tw-v {{
  color: #00E5FF !important;
}}
.ntw-tw-r {{
  color: #D4AF37 !important;
  font-weight: 700 !important;
  margin-right: 8px !important;
}}
.ntw-tw-head .ntw-tw-v {{ color: #00ffd9 !important; }}
.ntw-tw-div {{ border-top: 1px solid rgba(212,175,55,0.25) !important; padding-top: 10px !important; margin-top: 10px !important; }}
.ntw-tw-region {{ margin-left: 4px !important; border-left: 2px solid rgba(0,229,255,0.35) !important; padding-left: 10px !important; }}
.ntw-tw-line.ntw-audit-feed {{
  border-left: 3px solid rgba(212, 175, 55, 0.55) !important;
  padding-left: 12px !important;
  margin-bottom: 10px !important;
}}
@keyframes kgec-sovereign-ntw-hr-flow {{
  0%, 100% {{ opacity: 0.72; box-shadow: 0 0 0 rgba(0,229,255,0); }}
  50% {{ opacity: 1; box-shadow: 0 0 14px rgba(0,229,255,0.28); }}
}}
.sovereign-ntw-hr {{
  border: none !important;
  border-top: 1px solid rgba(212,175,55,0.38) !important;
  margin: 0 0 12px !important;
  height: 1px !important;
  background: linear-gradient(90deg, transparent, rgba(212,175,55,0.55), transparent) !important;
  animation: kgec-sovereign-ntw-hr-flow 3.8s ease-in-out infinite !important;
}}
.sovereign-ntw-strip {{
  contain: layout style !important;
  position: relative !important;
  z-index: 40 !important;
  margin: 10px 0 16px;
  padding: 14px 12px 18px;
  border-radius: 14px;
  border: 1px solid rgba(212,175,55,0.42);
  background: rgba(0, 0, 128, 0.52);
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.06), 0 6px 20px rgba(0,0,0,0.22);
}}
.kgec-ntw-stream-root {{
  position: relative !important;
  z-index: 48 !important;
  min-height: min(280px, 52vh) !important;
  margin-bottom: 16px !important;
  padding: 12px 10px 14px !important;
  border-radius: 12px !important;
  background: radial-gradient(120% 100% at 50% 0%, rgba(0, 90, 70, 0.28) 0%, rgba(0, 0, 0, 0.9) 55%) !important;
  border: 1px solid rgba(46, 204, 113, 0.38) !important;
  box-shadow: inset 0 0 36px rgba(0, 229, 255, 0.06), 0 8px 22px rgba(0, 0, 0, 0.42) !important;
  overflow: visible !important;
  isolation: isolate !important;
  contain: style !important;
}}
@media (prefers-reduced-motion: reduce) {{
  .eagle-ticker-shell.eagle-alert-pulse {{ animation: none !important; }}
  .kgec-crest-live {{ animation: none !important; }}
  #kgec-eagle-hover-layer {{ display: none !important; }}
  section.main button[aria-label="MTN"],
  section.main button[aria-label="Airtel"],
  section.main button[aria-label="Glo"],
  section.main button[aria-label="9mobile"] {{ animation: none !important; }}
  .ntw-tw-rain .ntw-tw-line {{ animation: none !important; transform: none !important; }}
  .kgec-mq-track {{ animation: none !important; transform: none !important; }}
  .sovereign-ntw-hr {{ animation: none !important; }}
}}
/* Beautiful Mirror · GCSLC mono-terminal (stacked cells · zero overlap · 0.65rem cadence) */
[data-testid="stSidebar"] {{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  font-size: 0.65rem !important;
  line-height: 1.55 !important;
  letter-spacing: 0.04em !important;
  word-spacing: 0.35em !important;
  background-color: {SHELL} !important;
  background-image: linear-gradient(180deg, rgba(0,0,128,0.98) 0%, rgba(0,0,64,0.99) 100%) !important;
  border-right: 1px solid rgba(212, 175, 55, 0.38) !important;
  isolation: isolate !important;
  contain: none !important;
  overflow-x: hidden !important;
  overflow-y: auto !important;
  -webkit-overflow-scrolling: touch !important;
  -webkit-font-smoothing: antialiased !important;
  box-sizing: border-box !important;
}}
[data-testid="stSidebar"] *, [data-testid="stSidebar"] *::before, [data-testid="stSidebar"] *::after {{
  box-sizing: border-box !important;
}}
[data-testid="stSidebar"] [data-testid="stSidebarContent"] {{
  display: flex !important;
  flex-direction: column !important;
  gap: 10px !important;
  padding-top: 10px !important;
  padding-bottom: 20px !important;
  padding-left: 10px !important;
  padding-right: 10px !important;
  max-width: 100% !important;
}}
[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"] {{
  position: relative !important;
  z-index: 1 !important;
  flex: 0 0 auto !important;
  width: 100% !important;
  max-width: 100% !important;
  border: none !important;
  border-radius: 10px !important;
  background: rgba(0, 0, 48, 0.55) !important;
  padding: 12px 12px 14px !important;
  margin: 0 0 0 0 !important;
  box-sizing: border-box !important;
  box-shadow: inset 0 0 0 1px rgba(212, 175, 55, 0.42) !important;
  overflow: visible !important;
}}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
  gap: 0.4rem !important;
}}
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > [data-testid="element-container"] {{
  margin-bottom: 0.25rem !important;
  max-width: 100% !important;
}}
.kgec-sidebar-cap-line {{
  margin: 4px 0 10px 0 !important;
  min-height: 1.4rem !important;
}}
[data-testid="stSidebar"] p.kgec-mono-head {{
  font-family: ui-monospace, monospace !important;
  font-size: 0.65rem !important;
  font-weight: 700 !important;
  color: #00E5FF !important;
  text-transform: none !important;
  letter-spacing: 0.14em !important;
  word-spacing: 0.55em !important;
  margin: 0 0 1.1rem 0 !important;
  padding: 0 4px 12px 4px !important;
  border-bottom: 1px solid rgba(212, 175, 55, 0.32) !important;
  line-height: 1.65 !important;
}}
[data-testid="stSidebar"] .kgec-mono-head .kgec-mq-track span[aria-hidden="true"],
[data-testid="stSidebar"] .kgec-sidebar-cap-line .kgec-mq-track span[aria-hidden="true"] {{
  display: none !important;
}}
[data-testid="stSidebar"] .kgec-mono-head .kgec-mq-track,
[data-testid="stSidebar"] .kgec-sidebar-cap-line .kgec-mq-track {{
  animation: none !important;
  transform: none !important;
  white-space: normal !important;
  display: block !important;
  gap: 0 !important;
}}
[data-testid="stSidebar"] .kgec-sidebar-cap-line {{
  word-break: break-word !important;
  overflow-wrap: anywhere !important;
}}
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {{
  color: rgba(200, 245, 255, 0.94) !important;
  font-size: 0.65rem !important;
  line-height: 1.55 !important;
  letter-spacing: 0.05em !important;
  word-spacing: 0.28em !important;
}}
[data-testid="stSidebar"] label {{
  margin-top: 8px !important;
  margin-bottom: 2px !important;
  display: block !important;
  clear: both !important;
  max-width: 100% !important;
  word-break: break-word !important;
  overflow-wrap: anywhere !important;
}}
[data-testid="stSidebar"] [data-baseweb="checkbox"] {{
  max-width: 100% !important;
}}
[data-testid="stSidebar"] [data-baseweb="checkbox"] label {{
  white-space: normal !important;
}}
[data-testid="stSidebar"] [data-testid="stCaption"] {{
  font-size: 0.62rem !important;
  opacity: 0.88 !important;
  line-height: 1.6 !important;
  word-spacing: 0.45em !important;
  margin-top: 6px !important;
  margin-bottom: 12px !important;
}}
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea {{
  font-family: inherit !important;
  font-size: 0.65rem !important;
  line-height: 1.45 !important;
  margin-top: 6px !important;
  width: 100% !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
}}
[data-testid="stSidebar"] [data-testid="stMetricValue"] {{
  font-size: 0.65rem !important;
  letter-spacing: 0.08em !important;
}}
[data-testid="stSidebar"] [data-testid="stMetricLabel"] {{
  font-size: 0.65rem !important;
  word-spacing: 0.4em !important;
}}
[data-testid="stSidebar"] [data-baseweb="button"],
[data-testid="stSidebar"] button {{
  margin-top: 8px !important;
  max-width: 100% !important;
}}
[data-testid="stSidebar"] hr {{
  margin: 14px 0 !important;
  border-color: rgba(212, 175, 55, 0.25) !important;
}}
[data-testid="stSidebar"] [data-testid="stExpander"] svg,
[data-testid="stSidebar"] [data-testid="stExpander"] button svg,
[data-testid="stSidebar"] [data-testid="StyledExpanderIcon"],
[data-testid="stSidebar"] details summary svg,
[data-testid="stSidebar"] [data-testid="stIconMaterial"],
[data-testid="stSidebar"] .material-icons,
[data-testid="stSidebar"] [class*="keyboard_arrow"],
[data-testid="stSidebar"] [class*="KeyboardArrow"],
[data-testid="stSidebar"] [class*="ExpandMore"] {{
  display: none !important;
  width: 0 !important;
  height: 0 !important;
  opacity: 0 !important;
  overflow: hidden !important;
  pointer-events: none !important;
}}
/* iPhone / narrow — sidebar stable while main NTW kinetic reveal runs (scroll anchoring off · own layer) */
@media (max-width: 900px) {{
  [data-testid="stSidebar"] {{
    overflow-anchor: none !important;
    overscroll-behavior-y: contain !important;
    transform: translate3d(0, 0, 0) !important;
    -webkit-transform: translate3d(0, 0, 0) !important;
    max-height: 100vh !important;
    max-height: 100dvh !important;
    padding-bottom: max(14px, env(safe-area-inset-bottom, 0px)) !important;
    padding-top: max(8px, env(safe-area-inset-top, 0px)) !important;
  }}
  [data-testid="stSidebar"] [data-testid="stSidebarContent"] {{
    overflow-anchor: none !important;
  }}
  section.main .kgec-ntw-stream-root {{
    isolation: isolate !important;
    contain: style !important;
  }}
}}
</style>
""",
    unsafe_allow_html=True,
)

_trade_nodes = _load_trade_commerce_nodes()
_fin_pos_pts = _load_financial_inclusion_pos()
_signal_ev = _load_signal_blackout_events()
_vigil_registry = _load_vigil_registry_events()

with st.sidebar:
    with _kgec_sidebar_section():
        _kgec_cell_head("Sovereign discovery")
        _kgec_sidebar_cap_mq(
            "Lattice filter + heuristic NL pivot — no cloud LLM — Lux-class latency on mobile — sovereign search LIVE."
        )
        st.text_input(
            "Filter Sovereign Nodes on map",
            key="village_lattice_search",
            placeholder="binji · NGECC · NGEEC · green energy chemicals · village name",
            help="Trade/micro: label, village, id, passage_segment, search_aliases. "
            "Financial inclusion: matches financial_inclusion_pos.json (zone, name, state, id, …). "
            "NGECC / NGEEC / Nigerian Green Energy & Chemicals: pivots industrial PU cluster + locks viewport. "
            "Sovereign-gold POS applies when FIN lattice matches even if the FIN toggle is off.",
        )
        st.text_area(
            "Natural language query",
            key="sovereign_nl_query_text",
            height=72,
            placeholder="Where is the highest POS density in Binji?",
        )
        if st.button("Pivot map", key="sovereign_nl_pivot"):
            _qn = str(st.session_state.get("sovereign_nl_query_text") or "")
            try:
                _nat_pivot_df, _ = _national_pu_frame_cached()
            except Exception:
                _nat_pivot_df = None
            _nl = resolve_sovereign_nl_query(
                _qn,
                _fin_pos_pts,
                trade_points=_trade_nodes,
                ngecc_reg=_load_ngecc_industrial_registry(),
                national_pu_df=_nat_pivot_df,
            )
            if _nl:
                st.session_state["gv_center"] = (_nl["lat"], _nl["lon"])
                st.session_state["gv_zoom"] = _nl["zoom"]
                st.session_state["sovereign_nl_last"] = _nl
                if str(_nl.get("intent") or "") == "top_pos_density":
                    _zt_nl = str(_nl.get("zone_token") or "").strip().lower()
                    if _zt_nl:
                        st.session_state["_nl_fin_zone_token"] = _zt_nl
                else:
                    st.session_state.pop("_nl_fin_zone_token", None)
                st.success(f"{_nl['headline']} — {_nl['detail']}")
            else:
                st.warning(
                    "No match — try zone + POS wording, NGECC / NGEEC / green energy chemicals, "
                    "or expand `financial_inclusion_pos.json` / `trade_commerce_nodes.json`."
                )
    with _kgec_sidebar_section():
        _kgec_cell_head("K-GEC · Komi-Generative Cloud")
        _kgec_sidebar_cap_mq(
            "Smart click · ADM1 boundaries + gcslc_deep_join ward mass · K-GEC sniffs mounted registries · "
            "co-resident 24/7 Streamlit vigil — kinetic Total Reality."
        )
        st.toggle(
            "Smart click · state Total Reality (cyan)",
            value=True,
            key="smart_click_total_reality",
            help="Click **inside** a state polygon on the national map; summary appears under the canvas.",
        )
        st.toggle(
            "K-GEC intelligence stream (ticker)",
            value=True,
            key="generative_eagle_ticker",
            help="Vigil + NCC + telecom void + trade velocity + POS liquidity — scrollable on iPhone.",
        )
        st.toggle(
            "High-friction pulse (visual alert)",
            value=True,
            key="eagle_friction_pulse",
            help="Crimson rim when the top shout is high-friction. Visual only on iOS (no autoplay audio).",
        )
        _kgec_sidebar_cap_mq(
            "NTW Resonance Chamber below national map — Sovereign Control Panel — charts visible while "
            "smart-clicking states or lattice search — ignition armed."
        )
    with _kgec_sidebar_section():
        _kgec_cell_head("Sovereign ingestion monitor")
        _kgec_sidebar_cap_mq(
            "Phase 3 · NGECC strategic registry ↔ AZK Million Steel Rods — industrial lattice ticker LIVE.",
            seconds=36.0,
        )
        _ngecc_sidebar_reg = _load_ngecc_industrial_registry()
        st.metric("Industrial PU registry", len(_ngecc_sidebar_reg["codes"]))
        _bulk_n = int(_ngecc_sidebar_reg.get("bulk_entries_count") or 0)
        _bulk_hint = f" · tier-2 bulk rows: {_bulk_n}" if _bulk_n else ""
        _kgec_sidebar_cap_mq(
            f"AZK spine PUs peak gold {len(_ngecc_sidebar_reg['azk_codes'])} · "
            f"registry Part_02_Finance/data/ngecc_strategic_industrial_pu.json{_bulk_hint}",
            seconds=40.0,
        )
        st.toggle(
            "Industrial Assets (NGECC)",
            value=True,
            key="show_industrial_assets",
            help="Sovereign Gold (#BF953F) shimmer on registered PUs; off = cyan-only lattice for fluid compare.",
        )
    with _kgec_sidebar_section():
        _kgec_cell_head("Friction · sovereign audit")
        _kgec_sidebar_cap_mq(
            "Industrial wealth ↔ social delivery — friction layers off hero canvas until you enable — sovereign discipline.",
        )
        st.toggle(
            "NCC · infrastructure vulnerability",
            value=True,
            key="show_ncc_vulnerability",
            help="Pulsing crimson (#DC143C) — NCC ICT vandalization pressure (security intervention).",
        )
        st.toggle(
            "CBN · financial access points",
            value=False,
            key="show_cbn_access",
            help="Tier-2 registry: Part_02_Finance/data/cbn_financial_access_points.json",
        )
        st.toggle(
            "Social · service hubs",
            value=False,
            key="show_social_hubs",
            help="Tier-2 registry: Part_04_Social/data/social_service_hubs.json",
        )
        st.toggle(
            "Financial inclusion · POS (Binji / Bayelsa)",
            value=False,
            key="show_financial_inclusion_pos",
            help="Commerce vs formal finance gap — Part_02_Finance/data/financial_inclusion_pos.json",
        )
    with _kgec_sidebar_section():
        _kgec_cell_head("Trade & Commerce")
        _kgec_sidebar_cap_mq(
            "Livestock exchange anchors + village lattice — trade_commerce_nodes.json — "
            "each village Sovereign Node + search_aliases — velocity LIVE.",
        )
        st.toggle(
            "Trade & Commerce markets",
            value=False,
            key="show_trade_commerce",
            help="Mubi · Wudil · Mai'Adua livestock markets (high-fidelity markers).",
        )
    with _kgec_sidebar_section():
        _kgec_cell_head("Territory · capillaries")
        _kgec_sidebar_cap_mq(
            "Human shield · informal trade nodes national capillaries — "
            "Zaria GRA ↔ Danchadi POS ↔ coastal relays — ward pulse.",
        )
        st.toggle(
            "Micro-assets (capillaries)",
            value=False,
            key="show_micro_assets",
            help="Part_04_Social/data/micro_assets_capillaries.json",
        )
    with _kgec_sidebar_section():
        _kgec_cell_head("Forensic Intelligence · Soul")
        _kgec_sidebar_cap_mq(
            "NCC × telecom void × finance friction → Double-Zero synthesis · "
            "schema Part_03_Security/data/forensic_relational_schema.json — soul stream.",
        )
        st.toggle(
            "Double-Zero · disconnected void (grey heat)",
            value=False,
            key="show_double_zero_heatmap",
            help="NCC vandalism + signal blackouts + inclusion friction — Deep Shadow Grey intensities.",
        )
        st.toggle(
            "Northern markets → AZK livestock vectors",
            value=False,
            key="show_azk_livestock_vectors",
            help="42 northern markets · daily flow proxies → AZK spine (`northern_market_azk_vectors.json`).",
        )
        st.toggle(
            "Komi · Total Reality popups (cyan)",
            value=False,
            key="show_komi_intel",
            help="POS · Trade · Micro-assets — sector density, infrastructure health, Wahala Index.",
        )
        st.toggle(
            "Binji–Lagos strike audit (split)",
            value=False,
            key="binji_lagos_strike",
            help="Lagos Mainland (saturated blue) vs Binji/Danchadi void (pulsing gold). Replaces hero map.",
        )
    with _kgec_sidebar_section():
        _kgec_cell_head("National Vigil · signal pulse")
        _kgec_sidebar_cap_mq(
            "Append Part_01_Telecom/data/vigil_feed_events.json from SOC/NMS webhooks — "
            "vigil_feed.py normalizes — fuse legacy blackout registry optional — ONSA cadence.",
        )
        st.toggle(
            "Show vigil pulse strip",
            value=False,
            key="show_vigil_feed_strip",
            help="Deep Blue command — newest-first incident lines for ONSA situational awareness.",
        )
        st.toggle(
            "Fuse telecom blackout registry",
            value=True,
            key="vigil_fuse_blackouts",
            help="Merge `signal_blackouts.json` events into the same pulse sort (dedupe not applied).",
        )
        if st.session_state.get("show_vigil_feed_strip"):
            _vf = merge_vigil_sources(
                _vigil_registry,
                _signal_ev,
                fuse_blackouts=bool(st.session_state.get("vigil_fuse_blackouts")),
                limit=10,
            )
            if _vf:
                for _vi, _row in enumerate(_vf):
                    _lbl = str(_row.get("label") or "Event")[:72]
                    _k = str(_row.get("kind") or "")
                    _ts = str(_row.get("ts_iso") or "")[:19]
                    _zv = str(_row.get("zone") or "").strip()
                    _tail = f" · {_zv}" if _zv else ""
                    _vline = f"{_k} · {_ts} · {_lbl}{_tail}"
                    _vmq = _kgec_marquee_pair(_vline, seconds=26.0 + (_vi % 5))
                    st.markdown(
                        "<div class='kgec-sidebar-cap-line kgec-rc-ticker-line' style='border-left:3px solid rgba(212,175,55,0.45);"
                        "padding-left:10px;margin-bottom:8px;color:rgba(200,245,255,0.92);'>"
                        f"<span style='color:#00E5FF;'>{html.escape(_k)}</span> · {_vmq}</div>",
                        unsafe_allow_html=True,
                    )
            else:
                _kgec_sidebar_cap_mq(
                    "No vigil rows — populate vigil_feed_events.json or enable telecom fuse — strip IDLE.",
                    seconds=28.0,
                )
    with _kgec_sidebar_section():
        _kgec_cell_head("AZK spine")
        _kgec_sidebar_cap_mq(
            "Abuja FCT → Keffi → Kaduna → Zaria → Kano — azk_alignment true = peak gold — eagle corridor.",
        )

_states_geojson = _load_nigeria_states_geojson()
_phase2 = _load_phase2_spine_bundle()
_asset_states = _coal_asset_state_names()

_fuse_caption = ""
_fused_df = None
try:
    _fused_df = _load_fused_lga_ward_partition()
    _fuse_ok = len(_fused_df) == 774 and int(_fused_df["ward_count"].sum()) == NATIONAL_WARD_TOTAL
    _fuse_caption = (
        f"gcslc_deep_join · {_fused_df.shape[0]} LGAs · Σ wards "
        f"{int(_fused_df['ward_count'].sum()):,} · {'CHECKSUM LOCKED' if _fuse_ok else 'CHECKSUM REVIEW'}"
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

_ngecc_reg = _load_ngecc_industrial_registry()
_show_industrial = bool(st.session_state.get("show_industrial_assets", True))

_ncc_incidents = _load_ncc_vulnerability_incidents()
_cbn_pts = _load_cbn_financial_points()
_social_pts = _load_social_service_points()
_show_ncc = bool(st.session_state.get("show_ncc_vulnerability", True))
_show_cbn = bool(st.session_state.get("show_cbn_access", False))
_show_soc = bool(st.session_state.get("show_social_hubs", False))
_show_fin_pos = bool(st.session_state.get("show_financial_inclusion_pos", False))
_show_trade = bool(st.session_state.get("show_trade_commerce", False))
_show_micro = bool(st.session_state.get("show_micro_assets", False))

_micro_pts = _load_micro_assets_capillaries()


def _match_village_query(query: str, row: dict) -> bool:
    if not query.strip():
        return True
    qv = query.strip().lower()
    parts = [
        str(row.get("label", "")),
        str(row.get("village", "")),
        str(row.get("id", "")),
        str(row.get("passage_segment", "")),
    ]
    als = row.get("search_aliases")
    if isinstance(als, list):
        parts.extend(str(a) for a in als)
    blob = " ".join(parts).lower()
    return qv in blob


def _match_fin_lattice_query(query: str, row: dict) -> bool:
    """Sovereign discovery substring match across financial_inclusion_pos.json keywords."""
    if not query.strip():
        return False
    qv = query.strip().lower()
    parts = [
        str(row.get("name", "")),
        str(row.get("zone", "")),
        str(row.get("state", "")),
        str(row.get("id", "")),
        str(row.get("commercial_activity", "")),
        str(row.get("formal_finance_penetration", "")),
        str(row.get("inclusion_gap", "")),
        str(row.get("node_kind", "")),
    ]
    als = row.get("search_aliases")
    if isinstance(als, list):
        parts.extend(str(a) for a in als)
    blob = " ".join(parts).lower()
    return qv in blob


def _fin_zone_token_match(zone_token: str, row: dict) -> bool:
    """NL pivot zone_token ⊆ FIN row zone/state/name (strategic cell illumination)."""
    z = zone_token.strip().lower()
    if not z:
        return False
    blob = (
        str(row.get("zone", "")) + " " + str(row.get("state", "")) + " " + str(row.get("name", ""))
    ).lower()
    return z in blob


def _fin_centroid_zoom(rows: list[dict]) -> tuple[tuple[float, float], float]:
    """Pivot viewport to FIN cluster — zoom scales with geographic spread."""
    if not rows:
        clat = sum(n["lat"] for n in AZK_CORRIDOR_NODES) / len(AZK_CORRIDOR_NODES)
        clon = sum(n["lon"] for n in AZK_CORRIDOR_NODES) / len(AZK_CORRIDOR_NODES)
        return (clat, clon), 6.2
    lats = [float(r["lat"]) for r in rows]
    lons = [float(r["lon"]) for r in rows]
    clat = sum(lats) / len(lats)
    clon = sum(lons) / len(lons)
    span = max(max(lats) - min(lats), max(lons) - min(lons), 0.018)
    if span < 0.045:
        zm = 12.0
    elif span < 0.09:
        zm = 11.0
    elif span < 0.18:
        zm = 10.0
    elif span < 0.38:
        zm = 9.0
    else:
        zm = 8.2
    return (clat, clon), zm


_village_q = str(st.session_state.get("village_lattice_search") or "").strip()
_fin_matched = [r for r in _fin_pos_pts if _match_fin_lattice_query(_village_q, r)]
_ngecc_lattice_active = bool(_village_q and ngecc_discovery_hit(_village_q, _ngecc_reg))
_fin_lattice_active = bool(_village_q and _fin_matched and not _ngecc_lattice_active)
_lattice_geo_lock = False
if _ngecc_lattice_active:
    _sig_ngecc = _village_q.casefold()
    if st.session_state.get("_ngecc_lattice_sig") != _sig_ngecc:
        _nl_lat = resolve_sovereign_nl_query(
            _village_q,
            _fin_pos_pts,
            trade_points=_trade_nodes,
            ngecc_reg=_ngecc_reg,
            national_pu_df=_national_df,
        )
        if _nl_lat:
            st.session_state["gv_center"] = (_nl_lat["lat"], _nl_lat["lon"])
            st.session_state["gv_zoom"] = _nl_lat["zoom"]
        st.session_state["_ngecc_lattice_sig"] = _sig_ngecc
    _lattice_geo_lock = True
elif _fin_lattice_active:
    _sig_fin = _village_q.casefold()
    if st.session_state.get("_fin_lattice_sig") != _sig_fin:
        _fp_ctr, _fp_zm = _fin_centroid_zoom(_fin_matched)
        st.session_state["gv_center"] = _fp_ctr
        st.session_state["gv_zoom"] = _fp_zm
        st.session_state["_fin_lattice_sig"] = _sig_fin
    _lattice_geo_lock = True
else:
    st.session_state.pop("_fin_lattice_sig", None)
    st.session_state.pop("_ngecc_lattice_sig", None)

_show_industrial_effective = bool(_show_industrial or _ngecc_lattice_active)

_nl_fin_z = str(st.session_state.get("_nl_fin_zone_token") or "").strip().lower()
_fin_nl_matched = (
    [r for r in _fin_pos_pts if _fin_zone_token_match(_nl_fin_z, r)] if _nl_fin_z else []
)
_fin_nl_active = bool(
    _fin_nl_matched and not _fin_lattice_active and not _ngecc_lattice_active
)

_show_fin_pos_effective = bool(_show_fin_pos or _fin_lattice_active or _fin_nl_active)
if _fin_lattice_active:
    _fin_points_map = _fin_matched
elif _fin_nl_active:
    _fin_points_map = _fin_nl_matched
else:
    _fin_points_map = _fin_pos_pts
_fin_gold_pulse = bool(_fin_lattice_active or _fin_nl_active or _ngecc_lattice_active)

_trade_disp = [r for r in _trade_nodes if _match_village_query(_village_q, r)]
_micro_disp = [r for r in _micro_pts if _match_village_query(_village_q, r)]
_lagos_audit_pts = _load_lagos_strike_points()
_north_mk = _load_northern_market_vectors()
_double_zero_triples = build_double_zero_triples(
    _ncc_incidents,
    _signal_ev,
    _fin_pos_pts,
)
_binji_audit_pts = _binji_void_points(_fin_pos_pts)
_show_dz = bool(st.session_state.get("show_double_zero_heatmap", False))
_show_vec = bool(st.session_state.get("show_azk_livestock_vectors", False))
_show_komi = bool(st.session_state.get("show_komi_intel", False))
_strike_mode = bool(st.session_state.get("binji_lagos_strike", False))

_federation_map = _build_federation_map(
    _states_geojson,
    _phase2,
    _asset_states,
    show_ncc_vulnerability=_show_ncc,
    ncc_incidents=_ncc_incidents,
    show_cbn_access=_show_cbn,
    cbn_points=_cbn_pts,
    show_social_hubs=_show_soc,
    social_points=_social_pts,
    show_trade_commerce=_show_trade,
    trade_nodes=_trade_disp,
    show_financial_inclusion_pos=_show_fin_pos_effective,
    financial_inclusion_points=_fin_points_map,
    fin_inclusion_gold_highlight=_fin_gold_pulse,
    show_micro_assets=_show_micro,
    micro_asset_points=_micro_disp,
    show_double_zero=_show_dz,
    double_zero_triples=_double_zero_triples,
    show_azk_vectors=_show_vec,
    northern_markets=_north_mk,
    show_komi_intel=_show_komi,
)
_fg_atom = _atomic_viewport_feature_group(
    _viewport_df,
    _ngecc_reg["codes"],
    _ngecc_reg["labels"],
    _ngecc_reg["azk_codes"],
    show_industrial_overlay=_show_industrial_effective,
)

if st_folium is None:
    st.error(
        "Install streamlit-folium inside the project venv: "
        "`pip install streamlit-folium` — required for viewport atomic lattice."
    )
    st.components.v1.html(_federation_map._repr_html_(), height=520, scrolling=False)
elif _strike_mode:
    _kgec_kinetic_note(
        "Strike audit mode — split panels replace national hero map — toggle off for 176k PU viewport — Lagos vs Binji LIVE.",
        seconds=36.0,
    )
    _lag_map = _build_strike_audit_map(
        center_lat=6.5244,
        center_lon=3.3792,
        zoom_start=12,
        points=_lagos_audit_pts,
        circle_class="gcslc-strike-lagos",
        komi_intel=_show_komi,
    )
    _bin_map = _build_strike_audit_map(
        center_lat=12.238,
        center_lon=4.897,
        zoom_start=11,
        points=_binji_audit_pts,
        circle_class="gcslc-strike-binji",
        komi_intel=_show_komi,
    )
    _sc1, _sc2 = st.columns(2)
    with _sc1:
        _kgec_kinetic_note(
            "Lagos Mainland — saturated commercial fabric — cyan blue strike lattice — LIVE panel.",
            seconds=32.0,
        )
        st_folium(_lag_map, height=520, use_container_width=True, key="strike_lagos")
    with _sc2:
        _kgec_kinetic_note(
            "Binji Danchadi void — informal POS velocity — pulsing gold sovereign audit — LIVE panel.",
            seconds=34.0,
        )
        st_folium(_bin_map, height=520, use_container_width=True, key="strike_binji")
else:
    _ntw_blob = _load_ntw_operator_proxy_cached()
    if getattr(st, "fragment", None) is None and st.session_state.get(
        "generative_eagle_ticker", True
    ):
        _kgec_kinetic_note(
            "Install Streamlit ≥1.33 for isolated Eagle fragment ticks — Stable Sky — recommended for majesty loop.",
            seconds=40.0,
        )

    _ensure_gv_viewport_defaults()
    _gv_zoom = st.session_state.get("gv_zoom")
    _gv_center = st.session_state.get("gv_center")
    _out = st_folium(
        _federation_map,
        key="gv_map",
        height=560,
        use_container_width=True,
        returned_objects=["bounds", "zoom", "center", "last_clicked"],
        zoom=_gv_zoom,
        center=_gv_center,
        feature_group_to_add=_fg_atom if len(_viewport_df) > 0 else None,
    )
    _prev_map = st.session_state.get("gv_map_out") or {}
    if isinstance(_out, dict):
        _merged = dict(_out)
        if _merged.get("zoom") is None and _prev_map.get("zoom") is not None:
            _merged["zoom"] = _prev_map["zoom"]
        if _merged.get("center") is None and _prev_map.get("center") is not None:
            _merged["center"] = _prev_map["center"]
        _lc_handshake = _merged.get("last_clicked")
        if (
            _lc_handshake
            and isinstance(_lc_handshake, dict)
            and _prev_map.get("zoom") is not None
        ):
            # Smart-click return: lock viewport — prevents national zoom-out / iframe flicker
            _merged["zoom"] = _prev_map["zoom"]
            if _prev_map.get("center") is not None:
                _merged["center"] = _prev_map["center"]
        if _lattice_geo_lock:
            _gvz_hold = st.session_state.get("gv_zoom")
            _gvc_hold = st.session_state.get("gv_center")
            if _gvz_hold is not None:
                _merged["zoom"] = _gvz_hold
            if isinstance(_gvc_hold, (list, tuple)) and len(_gvc_hold) >= 2:
                try:
                    _merged["center"] = {
                        "lat": float(_gvc_hold[0]),
                        "lng": float(_gvc_hold[1]),
                    }
                except (TypeError, ValueError):
                    pass
        _out = _merged
    if isinstance(_out, dict):
        st.session_state["gv_map_out"] = _out
        if not _lattice_geo_lock:
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
        if st.session_state.get("smart_click_total_reality", True) and _states_geojson:
            _lc = _out.get("last_clicked")
            if _lc and isinstance(_lc, dict):
                try:
                    _clat = float(_lc["lat"])
                    _clng = float(_lc["lng"] if _lc.get("lng") is not None else _lc.get("lon"))
                except (KeyError, TypeError, ValueError):
                    _clat = _clng = None
                if _clat is not None and _clng is not None:
                    _hit = resolve_state_from_click(_clat, _clng, _states_geojson, _fused_df)
                    if _hit:
                        _st_key = str(_hit[0]).strip()
                        st.session_state["total_reality_last"] = build_total_reality_summary(
                            _hit[0],
                            fused_df=_fused_df,
                            national_pu_df=_national_df,
                            ncc_rows=_ncc_incidents,
                            signal_rows=_signal_ev,
                            fin_points=_fin_pos_pts,
                            states_geojson=_states_geojson,
                            ntw_proxy=_ntw_blob,
                        )
                        _toast_sig = (_st_key, round(_clat, 4), round(_clng, 4))
                        if st.session_state.get("_total_reality_toast_sig") != _toast_sig:
                            st.session_state["_total_reality_toast_sig"] = _toast_sig
                            _toast = getattr(st, "toast", None)
                            if callable(_toast):
                                _toast(f"Total Reality · {_st_key}", icon="🟦")
                    else:
                        st.session_state.pop("total_reality_last", None)
                        st.session_state.pop("_total_reality_toast_sig", None)
    if (
        st.session_state.get("smart_click_total_reality", True)
        and st.session_state.get("total_reality_last")
    ):
        st.markdown(
            _html_total_reality_card(st.session_state["total_reality_last"]),
            unsafe_allow_html=True,
        )
    _render_ntw_sovereign_control_panel(_ntw_blob)
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
_atomic_meta_lines.append(
    f"Phase 3 NGECC · {len(_ngecc_reg['codes'])} industrial codes · "
    f"gold overlay {'on' if _show_industrial_effective else 'off (cyan-only)'}"
)
_atomic_meta_lines.append(strategic_cells_banner(_fused_df))
_len_ncc = len(_ncc_incidents)
_len_cbn = len(_cbn_pts)
_len_soc = len(_social_pts)
_atomic_meta_lines.append(
    f"Friction audit · NCC {_len_ncc} ({'on' if _show_ncc else 'off'}) · "
    f"CBN {_len_cbn} ({'on' if _show_cbn else 'off'}) · "
    f"Social {_len_soc} ({'on' if _show_soc else 'off'})"
)
_atomic_meta_lines.append(
    f"Territory · Trade & Commerce {len(_trade_disp)}/{len(_trade_nodes)} ({'on' if _show_trade else 'off'}) · "
    f"Fin inclusion POS {len(_fin_points_map)}/{len(_fin_pos_pts)} "
    f"({'lattice gold' if _fin_lattice_active else ('on' if _show_fin_pos else 'off')}) · "
    f"Micro-assets {len(_micro_disp)}/{len(_micro_pts)} ({'on' if _show_micro else 'off'}) · "
    f"basemap max_zoom 22 + Esri imagery"
)
_atomic_meta_lines.append(
    f"Forensic soul · Double-Zero {len(_double_zero_triples)} cells ({'on' if _show_dz else 'off'}) · "
    f"AZK vectors {len(_north_mk)} markets ({'on' if _show_vec else 'off'}) · "
    f"Komi popups {'on' if _show_komi else 'off'} · "
    f"Strike split {'on' if _strike_mode else 'off'}"
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
_sdw_ml1 = _kgec_marquee_pair(
    "States + FCT · 37 shells · constitutional administrative lattice LIVE",
    seconds=36.0,
)
_sdw_ml2 = _kgec_marquee_pair(
    "774 LGAs · national heartbeat · gcslc_deep_join cadence", seconds=34.0
)
_sdw_ml3 = _kgec_marquee_pair(
    "8,806 wards · forensic ward tokens · pinch-to-reveal", seconds=38.0
)
_sdw_ml4 = _kgec_marquee_pair(
    "176,846 polling units · INEC atomic lattice · sovereign scale-3", seconds=40.0
)
_sdw_scale_mq = _kgec_marquee_pair(
    f"Sovereign record · Scale 1 States + AZK · Scale 2 LGAs ≥ {ZOOM_LGA_EMERGE} wards ≥ {ZOOM_WARD_EMERGE} · "
    f"Scale 3 atomic ≥ {ZOOM_ATOM_EMERGE} · FPS HUD · pinch atomize · orientation resize armed",
    seconds=58.0,
)
_detail_mq = _kgec_marquee_pair(
    _detail_meta if _detail_meta else "Forensic spine loaded — map is the vigil — ignition stable.",
    seconds=max(44.0, min(92.0, 14.0 + len(_detail_meta) / 6.5)),
)
_foot_mq1 = _kgec_marquee_pair(
    "SCUML Certificate · SC 151653884 · Copyright Registration LW15954 — compliance ticker",
    seconds=48.0,
)
_foot_mq2 = _kgec_marquee_pair(
    "© 2026 Galadiman Ruwa Center (GCSLC) LTD/GTE · Sovereign-by-Design · national instrument LIVE",
    seconds=56.0,
)

st.markdown(
    f"""
<div class="sovereign-detail-widget">
  <div class="sdw-handshake">
    <div class="sdw-hs-row kgec-rc-ticker-line"><span class="kgec-mq" style="--kgec-mq-dur:52s"><span class="kgec-mq-track"><span>Goldman Ruwa Center for Strategic Leadership and Communication GCSLC LTD/GTE · Majestic K-GEC · Sovereign mirror</span><span aria-hidden="true">Goldman Ruwa Center for Strategic Leadership and Communication GCSLC LTD/GTE · Majestic K-GEC · Sovereign mirror</span></span></span></div>
    <div class="sdw-hs-row kgec-rc-ticker-line"><span class="kgec-mq" style="--kgec-mq-dur:44s"><span class="kgec-mq-track"><span>Galadiman Ruwa Nigeria Ltd RC 1871418 · Zaria GRA cadence · national lattice</span><span aria-hidden="true">Galadiman Ruwa Nigeria Ltd RC 1871418 · Zaria GRA cadence · national lattice</span></span></span></div>
    <div class="sdw-hs-row kgec-rc-ticker-line"><span class="kgec-mq" style="--kgec-mq-dur:56s"><span class="kgec-mq-track"><span>8R Paradigm Convergence and Determinants — decode · understand · the nation never sleeps</span><span aria-hidden="true">8R Paradigm Convergence and Determinants — decode · understand · the nation never sleeps</span></span></span></div>
  </div>
  <div class="sdw-metrics">
    <div class="sdw-metric"><div class="sdw-metric-val">37</div><div class="sdw-metric-lbl kgec-rc-ticker-line">{_sdw_ml1}</div></div>
    <div class="sdw-metric"><div class="sdw-metric-val">774</div><div class="sdw-metric-lbl kgec-rc-ticker-line">{_sdw_ml2}</div></div>
    <div class="sdw-metric"><div class="sdw-metric-val">8,806</div><div class="sdw-metric-lbl kgec-rc-ticker-line">{_sdw_ml3}</div></div>
    <div class="sdw-metric"><div class="sdw-metric-val">176,846</div><div class="sdw-metric-lbl kgec-rc-ticker-line">{_sdw_ml4}</div></div>
  </div>
  <div class="sdw-meta">
    <div class="kgec-sdw-strong"><strong style="color:{GOLD};">Sovereign record</strong></div>
    <div class="sdw-meta-line kgec-rc-ticker-line">{_sdw_scale_mq}</div>
    <div class="sdw-meta-line kgec-rc-ticker-line">{_detail_mq}</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)


st.markdown(
    f"""
<div class="footer-sovereign kgec-rc-ticker-line">
  <div class="footer-sovereign-row">{_foot_mq1}</div>
  <div class="footer-sovereign-row">{_foot_mq2}</div>
</div>
""",
    unsafe_allow_html=True,
)
