"""
Sovereign Eagle Mirror 2026 — Initialization (clean slate).
Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026
"""

from __future__ import annotations

import hashlib
import html
import json
import os
from datetime import timedelta
from time import time as _wall_time
from pathlib import Path
from typing import Any

import folium
import pandas as pd
import requests
import streamlit as st

from sovereign_bridge.env_socket import load_gateway_ingress_env

load_gateway_ingress_env()

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
from kysah_sovereign_alert import (
    build_kysah_sovereign_bundle_for_state,
    federated_kysah_rollup,
    kysah_area_token,
    kysah_distress_records,
    kysah_escalation_patrol_sniffs,
    kysah_escalation_shout_rows,
    kysah_home_token,
    load_kysah_stub_records,
)
from sovereign_logistics_joint import (
    build_approved_logistics_bundle,
    logistics_joint_cache_buster,
    merge_patrol_with_logistics,
)
from generative_eagle import collect_eagle_shouts, friction_alert_active
# Load fused catalog before sovereign_active_intel (same gcslc_deep_join dep) — avoids rare Streamlit loader KeyError.
from gcslc_deep_join import NATIONAL_WARD_TOTAL, build_fused_catalog
from dapi_traditional_weld import (
    TRADITIONAL_PRINCIPAL_ROLES,
    ensure_browser_session_id,
    fetch_oauth_token,
    haraji_cdc_recent_rows,
    init_verification_store,
    leaderboard_for_state_wards,
    principal_jurisdiction_stats,
    record_haraji_cdc_line,
    record_verification,
    verification_ledger_recent,
    ward_verification_counts,
)
from katsina_kano_forensic import (
    is_kano_state,
    is_katsina_state,
    kano_forensic_mophi_glass_html,
    katsina_forensic_mophi_glass_html,
)
from kaduna_sovereign_pilot import (
    ZAZZAU_APEX,
    ZAZZAU_ELEVEN_SOURCE_NOTE,
    ZAZZAU_THIRTY_ONE_DISTRICTS,
    DISTRICT_LEDGER_NOTE,
    KADUNA_CHIEFS_COUNCIL_PRECEDENCE,
    KADUNA_INSTITUTIONS,
    KADUNA_MODERN_STATUTORY_LATTICE,
    KADUNA_SPT_FRONTIER_LGA_EN,
    RIGASA_DISTRICT_ID,
    STRANGER_VETTING_DISTANCE_KM,
    DAPI_PARENT_FACING_PRIVACY,
    build_zazzau_eleven_lga_weld_rows,
    find_ward_pcode_rigasa_igabi,
    is_kaduna_state,
    kaduna_state_ward_total,
    lga_pcode_lookup,
    ward_count_for_lga,
)
from kaduna_student_deep_weld import (
    compute_ward_overload_wpcodes,
    kaduna_me_anguwa_pressure_summary,
    nuba_campus_inference_text,
)
from kaduna_map_twin_portrait import render_kaduna_map_twin_portrait
from nafc_student_load_pipeline import fallback_live_student_pulse_snapshot, live_student_pulse_snapshot
from sovereign_enrollment_ledger import (
    NATIONAL_NOTIONAL_TOTAL_STUDENTS,
    SOVEREIGN_ALBASA_SPEC,
    albasa_commander_benchmark_rows,
    bind_albasa_monthly_pool_to_ledger_rows,
    bind_albasa_pool_to_kaduna_institution_rows,
    build_sovereign_enrollment_ledger_rows,
    html_albasa_commander_benchmark_table,
    kaduna_headline_enrollment_counts,
    national_ledger_population_sum,
)
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


@st.fragment(run_every=timedelta(seconds=2.1))
def _sovereign_telegram_bridge_tick() -> None:
    """Telegram → SQLite queue → session_state (map + Gold Man); Sam-Sam replies via Bot API."""
    if not st.session_state.get("_sovereign_bridge_armed"):
        return
    ctx = st.session_state.get("_sovereign_bridge_ctx")
    if not isinstance(ctx, dict):
        return
    try:
        from sovereign_bridge.telegram_apply import apply_pending_bridge_commands

        n = apply_pending_bridge_commands(
            fused_df=ctx.get("fused_df"),
            national_pu_df=ctx.get("national_df"),
            fin_points=ctx.get("fin_points") or [],
            trade_nodes=ctx.get("trade_nodes") or [],
            ngecc_reg=ctx.get("ngecc_reg") or {},
            states_geojson=ctx.get("states_geojson"),
            ncc_rows=ctx.get("ncc_rows") or [],
            signal_rows=ctx.get("signal_rows") or [],
            ntw_proxy=ctx.get("ntw_proxy") or {},
        )
    except Exception:
        return
    if n:
        if not st.session_state.get("_sovereign_first_telegram_echo"):
            st.session_state["_sovereign_first_telegram_echo"] = True
            st.success(
                "Telegram Sovereign Bridge ignited · first remote order echoed on K-GEC "
                "(map + Gold Man + Sentinel)."
            )
        _toast = getattr(st, "toast", None)
        if callable(_toast):
            _toast("Sovereign Bridge · Telegram order applied", icon="📡")


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


def _ward_pcode_from_feature(feature: dict) -> str:
    p = feature.get("properties") or {}
    for k in ("ADM3_PCODE", "adm3_pcode", "WARD PCODE", "WARD_PCODE"):
        v = p.get(k)
        if v not in (None, ""):
            return str(v).strip()
    return ""


def _verification_heatmap_color(t: float) -> str:
    """Deep matter (#030818) → institutional cyan (#00E5FF)."""
    t = max(0.0, min(1.0, float(t)))
    r1, g1, b1 = 3, 8, 24
    r2, g2, b2 = 0, 229, 255
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


def _ward_style_verification_heatmap(
    feature: dict,
    counts: dict[str, int],
    vmax: int,
    *,
    overload_wpcodes: frozenset[str] | None = None,
) -> dict:
    wp = _ward_pcode_from_feature(feature)
    c = int(counts.get(wp, 0))
    if vmax <= 0:
        t = 0.0
    else:
        t = min(1.0, c / float(max(vmax, 1)))
    fill = _verification_heatmap_color(t)
    fill_op = 0.05 + 0.55 * t
    style: dict[str, Any] = {
        "color": CYAN if t > 0.12 else "#141428",
        "weight": 0.85 + 1.55 * t,
        "fillColor": fill,
        "fillOpacity": fill_op,
        "opacity": 0.45 + 0.48 * t,
        "className": "gcslc-ward-verify-heat leaflet-interactive",
    }
    if overload_wpcodes and wp in overload_wpcodes:
        style["color"] = CRIMSON_VULN
        style["weight"] = max(float(style["weight"]), 2.35)
        style["className"] = str(style.get("className") or "") + " gcslc-ward-overloaded"
    return style


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


def _kysah_distress_focus_for_state(state: str) -> dict[str, str] | None:
    """KYSAH distress row for this ADM1 — Area (LGA token) + Home (PU mesh) for monument synergy."""
    key = str(state or "").strip().lower()
    if not key:
        return None
    for rec in kysah_distress_records(load_kysah_stub_records()):
        if str(rec.get("state") or "").strip().lower() == key:
            return {
                "area_token": str(kysah_area_token(rec) or "").strip(),
                "home_token": str(kysah_home_token(rec) or "").strip(),
                "event_id": str(rec.get("event_id") or "").strip(),
            }
    return None


def _html_total_reality_card(summary: dict) -> str:
    """Gold Man Monument — prism shell, metallic state inscription, LGA→Ward→PU tier cascade."""
    st_name = html.escape(str(summary.get("state", "")))
    lg = int(summary.get("lgas") or 0)
    wd = int(summary.get("wards_forensic") or summary.get("wards") or 0)
    n_wd_nat = int(summary.get("national_ward_total") or 8806)
    pu = int(summary.get("pu_forensic") or 0)
    n_pu_nat = int(summary.get("national_pu_total") or 176_846)
    fs = summary.get("financial_inclusion_score")
    fs_txt = html.escape(str(fs) if fs is not None else "—")
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
    _raw_atom = str(summary.get("atomic_attribution_note") or "").strip()
    _pct_pu_nat = (100.0 * float(pu) / float(max(n_pu_nat, 1))) if n_pu_nat else 0.0
    _pct_pu_s = f"{_pct_pu_nat:.2f}%"
    _kys = _kysah_distress_focus_for_state(str(summary.get("state") or ""))
    _kys_mod = " kgec-gmm--kysah-focus" if _kys else ""
    _gold_tier_cls = "kgec-prism-tier kgec-prism-tier-gold" + (
        " kgec-gmm-tier--kysah-pulse" if _kys else ""
    )
    _red_tier_cls = "kgec-prism-tier kgec-prism-tier-red" + (
        " kgec-gmm-tier--kysah-pulse-intense" if _kys else ""
    )
    _lbl_lga = "Local Governments · administrative shell · state lattice"
    _lbl_pu = "Polling units · INEC atomic · Chairman forensic heart"
    if _kys:
        _at = html.escape(_kys["area_token"] or "?")
        _hm = html.escape(_kys["home_token"] or "?")
        _lbl_lga += f" · KYSAH Area (LGA) bind · {_at}"
        _lbl_pu += f" · KYSAH Home (PU) bind · {_hm}"
        if _kys.get("event_id"):
            _eid = html.escape(_kys["event_id"])
            _lbl_pu += f" · {_eid}"
    _forensic_lines: list[str] = []
    if _raw_atom:
        _forensic_lines.append(f"Atomic attribution · {html.escape(_raw_atom)}")
    if _kys:
        _forensic_lines.append(
            "KYSAH Sentinel · distress Area→Home escalation — duty-of-care pulse on gold + red tiers"
        )
    _forensic_lines.extend(
        [
            f"Financial inclusion · {fs_txt} / 100 — {fv}",
            (
                f"Friction audit · NCC in-state {fr.get('ncc_incidents_in_state', 0)} · "
                f"Telecom voids {fr.get('signal_void_events_in_state', 0)} · "
                f"severity avg {fr.get('ncc_severity_avg', 0)} — {fr_txt}"
            ),
            (
                f"NTW coverage (proxy) · Strongest modeled base → {dom}"
                + (f" · {dist_html}" if dist_html else "")
            ),
        ]
    )
    _forensic_pre = "\n".join(_forensic_lines)
    return f"""<div class="kgec-prism-terminal kgec-gold-man-monument gcslc-total-reality gcslc-tr-handshake-front{_kys_mod}" role="region" aria-label="Gold Man monument · state telemetry">
  <div class="kgec-gmm-cap">Total Reality · Gold Man monument</div>
  <header class="kgec-gold-man-header">
    <span class="kgec-gold-man-state">{st_name}</span>
    <p class="kgec-gold-man-sub kgec-prism-mono">Sovereign ADM1 · vertical cascade · forensic clarity</p>
  </header>
  <div class="kgec-prism-stack kgec-gmm-stack">
    <div class="{_gold_tier_cls}">
      <span class="kgec-prism-tier-val">{lg:,}</span>
      <span class="kgec-prism-tier-lbl">{_lbl_lga}</span>
    </div>
    <div class="kgec-prism-tier kgec-prism-tier-cyan">
      <span class="kgec-prism-tier-val">{wd:,}</span>
      <span class="kgec-prism-tier-lbl">Wards · forensic mass · {n_wd_nat:,} national comparator</span>
    </div>
    <div class="kgec-prism-tier kgec-prism-tier-white">
      <span class="kgec-prism-tier-val">{_pct_pu_s}</span>
      <span class="kgec-prism-tier-lbl">National PU lattice share · {pu:,} of {n_pu_nat:,} polling units · Chairman forensic heart</span>
    </div>
    <div class="{_red_tier_cls}">
      <span class="kgec-prism-tier-val">{pu:,}</span>
      <span class="kgec-prism-tier-lbl">{_lbl_pu} · {n_pu_nat:,} national lattice</span>
    </div>
  </div>
  <div class="kgec-gmm-forensic">
    <div class="kgec-gmm-forensic-h">Forensic observation</div>
    <pre class="kgec-prism-pre kgec-gmm-pre">{_forensic_pre}</pre>
  </div>
</div>"""


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
    # One-shot boot — guarantees high-velocity rain CSS animates on first paint (Streamlit double-run safe).
    if not st.session_state.get("_ntw_rain_bootstrapped"):
        st.session_state["_ntw_rain_bootstrapped"] = True
        st.session_state["ntw_resonance_nonce"] = int(
            st.session_state.get("ntw_resonance_nonce", 1)
        ) + 1
        st.session_state["ntw_push_ts"] = _wall_time()
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
    ward_verify_counts: dict[str, int] | None = None,
    verification_heatmap: bool = False,
    ward_overload_wpcodes: frozenset[str] | None = None,
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
path.gcslc-ward-verify-heat.gcslc-ward-overloaded {
  stroke: #DC143C !important;
  stroke-width: 2.45px !important;
  filter: drop-shadow(0 0 7px rgba(220,20,60,0.42)) !important;
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
        _wv = ward_verify_counts or {}
        _vmax = max(_wv.values()) if _wv else 0
        _overload_fc = ward_overload_wpcodes or frozenset()
        _ol_note = (
            f" — {len(_overload_fc)} ward(s) · Me Anguwa overload (crimson ring · tooltip detail on ward)"
            if verification_heatmap and _overload_fc
            else ""
        )
        _ward_layer_name = (
            (
                "8,806 Wards · DAPI verification heatmap (cyan = verified mass)"
                if verification_heatmap
                else "8,806 Wards · HDX spine + 8REC asset aura"
            )
            + _ol_note
        )
        fg_ward = folium.FeatureGroup(name=_ward_layer_name).add_to(m)
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

            def _style_ward(feat: dict) -> dict:
                if verification_heatmap:
                    return _ward_style_verification_heatmap(
                        feat, _wv, _vmax, overload_wpcodes=_overload_fc
                    )
                return _ward_style_with_asset(feat, asset_states)

            folium.GeoJson(
                wards_fc,
                pane="wardReveal",
                style_function=_style_ward,
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
# Stricter federation inset — 774 LGA hero canvas (Alphabet / Prism terminal geofence).
_NG_FRAC_X0 = 0.22
_NG_FRAC_X1 = 0.76
_NG_FRAC_Y0 = 0.24
_NG_FRAC_Y1 = 0.685
# Inset patrol centers so the Golden Eagle SVG (translate -50%/-50%) stays visually inside the frame.
_NG_PAD_X = 0.068
_NG_PAD_Y = 0.058
# Federation hero ↔ lat/lon (approx Nigeria bounding box; clamped to sovereign viewport).
_NG_LAT_MIN = 4.2
_NG_LAT_MAX = 13.95
_NG_LON_MIN = 2.65
_NG_LON_MAX = 14.68
# Temporal Hierarchy Lamp outer ring + KYSAH ribbon forensic cadence (+40% duration vs 16s baseline).
_KGEC_FORENSIC_CYCLE_S = 22.4


def _kgec_clamp_nigeria_fraction(pt: dict[str, float]) -> dict[str, float]:
    """Geofence — K-GEC sentinel stays inside sovereign canvas (no Chad/Niger drift)."""
    x = max(
        _NG_FRAC_X0 + _NG_PAD_X,
        min(_NG_FRAC_X1 - _NG_PAD_X, float(pt["x"])),
    )
    y = max(
        _NG_FRAC_Y0 + _NG_PAD_Y,
        min(_NG_FRAC_Y1 - _NG_PAD_Y, float(pt["y"])),
    )
    return {"x": round(x, 4), "y": round(y, 4)}


def _kgec_latlon_to_nigeria_fraction(lat: float, lon: float) -> dict[str, float]:
    """Map WGS84 point to Folium-normalized fractions, then sovereign clamp (KYSAH distress patrol)."""
    la = float(lat)
    lo = float(lon)
    x = (lo - _NG_LON_MIN) / (_NG_LON_MAX - _NG_LON_MIN)
    y = 1.0 - (la - _NG_LAT_MIN) / (_NG_LAT_MAX - _NG_LAT_MIN)
    return _kgec_clamp_nigeria_fraction({"x": x, "y": y})


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
    """Parent-window patrol: logistics joint unless KYSAH distress overrides (Crimson Sentinel)."""
    joint = _sovereign_joint_bundle_cached(logistics_joint_cache_buster())
    raw = _kgec_hover_targets(shouts)
    base_w = [0.42] * len(raw)
    lt = list(joint.get("logistics_targets") or [])
    lw = list(joint.get("logistics_weights") or [])
    joint_sniffs = list(joint.get("sniffs") or [])
    distress = kysah_distress_records(load_kysah_stub_records())
    kysah_sentinel = bool(distress)
    if kysah_sentinel:
        lt = []
        lw = []
        joint_sniffs = []
        for rec in distress:
            pt = _kgec_latlon_to_nigeria_fraction(float(rec["lat"]), float(rec["lon"]))
            for _ in range(14):
                lt.append(dict(pt))
                lw.append(0.97)
    merged_t, merged_w = merge_patrol_with_logistics(raw, base_w, lt, lw)
    clamped = [_kgec_clamp_nigeria_fraction(p) for p in merged_t]
    sniffs: list[str] = []
    if kysah_sentinel:
        sniffs.append(
            "KYSAH SENTINEL OVERRIDE · BUA/Dangote logistics patrol suspended · "
            "Eagle bound to distress Area→Home coordinates · Crimson Sentinel LIVE"
        )
    sniffs.extend(list(extra_sniffs or []))
    sniffs.extend(joint_sniffs)
    sniffs.extend(_kgec_sniff_lines_from_shouts(shouts))
    return {
        "targets": clamped,
        "targetWeights": merged_w[: len(clamped)],
        "sniffs": sniffs,
        "kysahSentinelOverride": kysah_sentinel,
    }


def _render_sovereign_joint_strip() -> None:
    """Honest milestone UI — ingest spine status + Temporal Hierarchy Lamp (demo)."""
    j = _sovereign_joint_bundle_cached(logistics_joint_cache_buster())
    evs = j.get("approved_events") or []
    rej = j.get("rejected") or []
    meta = j.get("manifest_meta") or {}
    purpose = html.escape(str(meta.get("purpose") or "fleet corridor monitoring"))[:72]
    mode = html.escape(str(j.get("ingest_mode") or "merge"))[:24]
    live_n = int(j.get("live_ingest_rows") or 0)
    proto = j.get("production_msisdn_protocol") or {}
    proto_meta = proto.get("meta") if isinstance(proto.get("meta"), dict) else {}
    residency = html.escape(str(proto_meta.get("data_residency") or ""))[:280]
    counsel = html.escape(str(proto_meta.get("counsel_approval") or meta.get("counsel_lock") or ""))[:220]
    rows_li = ""
    for e in evs[:4]:
        if not isinstance(e, dict):
            continue
        src = html.escape(str(e.get("source") or "?"))[:32]
        rows_li += (
            "<li>"
            f"{html.escape(str(e.get('fleet_operator') or '?'))} · "
            f"AZK seg {html.escape(str(e.get('azk_segment_index') or '?'))} · "
            f"jc {float(e.get('joint_confidence') or 0):.2f} · <span class='kgec-joint-src'>{src}</span>"
            "</li>"
        )
    if not rows_li:
        rows_li = "<li>No approved rows — check consent manifest + stub JSON + gantry JSONL</li>"
    rej_txt = (
        html.escape(", ".join(f"{a}:{b}" for a, b in rej[:5]))[:220] if rej else "none"
    )
    legal_body = (
        "<strong>Legal line</strong> · Fleet-owned SIM registration only — "
        "<code>fleet_consent_manifest.json</code> · "
        "<code>production_msisdn_protocol.json</code> locks residency / MSISDN handling."
    )
    if residency:
        legal_body += f"<br/><span class='kgec-joint-residency'>{residency}</span>"
    if counsel:
        legal_body += f"<br/><span class='kgec-joint-counsel'>{counsel}</span>"
    st.markdown(
        "<div class='kgec-joint-strip'>"
        "<div class='kgec-joint-strip-hdr'>Sovereign Joint · forensic spine · ingest "
        f"<span class='kgec-joint-ingest'>{mode}</span> · JSONL lines {live_n} · "
        f"<span class='kgec-joint-purpose'>{purpose}</span></div>"
        "<div class='kgec-joint-grid'>"
        "<div class='kgec-joint-status'>"
        f"<p><b>Approved</b> · {len(evs)} event(s) · <b>Gate</b> · {len(rej)} rejected</p>"
        f"<ul class='kgec-joint-ul'>{rows_li}</ul>"
        f"<p class='kgec-joint-rej'>Held / rejected: {rej_txt}</p>"
        "</div>"
        "<div class='kgec-joint-lamp-wrap'>"
        "<div class='kgec-temporal-lamp' aria-hidden='true' "
        "title='State Gold · Area Cyan · Home White · PU Red · forensic cadence'>"
        "<div class='kgec-roll kgec-roll-gold'></div>"
        "<div class='kgec-roll kgec-roll-cyan'></div>"
        "<div class='kgec-roll kgec-roll-white'></div>"
        "<div class='kgec-roll kgec-roll-red'></div>"
        "<div class='kgec-roll-core'></div>"
        "</div></div>"
        f"<div class='kgec-joint-legal-box'><p class='kgec-joint-legal'>{legal_body}</p></div>"
        "</div></div>",
        unsafe_allow_html=True,
    )


def _render_kysah_sovereign_ribbon() -> None:
    """
    KYSAH (Know Your Student to his Area and Home) — Student Safety Grid.
    Termii-verified pings as Sovereign Alerts correlated with National Resonance + logistics void pressure.
    Federation rollups keep the ribbon legible at any N.
    """
    recs = load_kysah_stub_records()
    rollup = federated_kysah_rollup(recs)
    if not recs:
        st.markdown(
            "<div class='kysah-sovereign-ribbon kysah-sovereign-ribbon--idle'>"
            "<div class='kysah-protocol-line'>Know Your Student to his <b>Area</b> and <b>Home</b></div>"
            "<div class='kysah-fed-line'>KYSAH · Student Safety Grid · ingest IDLE — "
            "mount <code>kysah_safety_ingest_stub.json</code> · keys <code>area_token</code> · "
            "<code>home_token</code> · Termii verification rail.</div>"
            "<div class='kysah-tier-legend'><span class='kysah-tier kysah-gold'>State Gold</span> · "
            "<span class='kysah-tier kysah-cyan'>Area Cyan</span> · "
            "<span class='kysah-tier kysah-white'>Home White</span> · "
            "<span class='kysah-tier kysah-red'>PU Red</span></div></div>",
            unsafe_allow_html=True,
        )
        return
    hist = rollup.get("state_histogram") or {}
    top_state = max(hist, key=lambda s: hist.get(s, 0)) if hist else str(recs[0].get("state") or "FCT")
    st_recs = [r for r in recs if str(r.get("state") or "").strip().lower() == str(top_state).lower()]
    if not st_recs:
        st_recs = recs[: max(1, len(recs))]
    bundle = build_kysah_sovereign_bundle_for_state(
        str(top_state),
        records_for_state=st_recs,
        fused_df=None,
        national_pu_df=None,
        ncc_rows=_load_ncc_vulnerability_incidents(),
        signal_rows=_load_signal_blackout_events(),
        fin_points=_load_financial_inclusion_pos(),
        states_geojson=_load_nigeria_states_geojson(),
        ntw_proxy=_load_ntw_operator_proxy_cached(),
        ntw_audit_blob=_load_ntw_regional_audit_live(),
    )
    env = bundle.get("sample_envelope") or {}
    nr = env.get("national_resonance") if isinstance(env.get("national_resonance"), dict) else {}
    lv = env.get("logistics_void_context") if isinstance(env.get("logistics_void_context"), dict) else {}
    facets = ", ".join(rollup.get("state_facets") or [])[:220]
    fed_line = (
        f"Federation · {rollup.get('total_records', 0)} ping(s) · "
        f"{rollup.get('distress_count', 0)} distress · "
        f"facets: {facets or '—'}"
    )
    res_line = (
        f"Sovereign Alert · {html.escape(str(env.get('sovereign_alert_id') or '?'))} · "
        f"{html.escape(str(env.get('kysah_tier') or '?'))} · "
        f"Resonance {html.escape(str(nr.get('operator') or '?'))} "
        f"RAN μ {float(nr.get('corridor_ran_mu_pct') or 0):.1f}% · SIM μ {float(nr.get('corridor_sim_mu_pct') or 0):.1f}%"
    )
    void_line = (
        f"Logistics void pressure {float(lv.get('void_pressure_index') or 0):.2f} · "
        f"FIN score {float(lv.get('financial_inclusion_score') or 0):.1f} · "
        f"NCC nodes {int(lv.get('ncc_incidents_in_state') or 0)} · "
        f"signal voids {int(lv.get('signal_void_events_in_state') or 0)}"
    )
    esc = "SENTINEL" if env.get("sentinel_escalation") else "MONITOR"
    st.markdown(
        "<div class='kysah-sovereign-ribbon'>"
        "<div class='kysah-protocol-line'>Know Your Student to his <b>Area</b> and <b>Home</b></div>"
        "<div class='kysah-fed-line'>" + html.escape(fed_line) + "</div>"
        "<div class='kysah-alert-line kysah-mode-" + html.escape(esc.lower()) + "'>"
        "<span class='kysah-mode-pill'>" + html.escape(esc) + "</span> " + res_line + "</div>"
        "<div class='kysah-void-line'>" + html.escape(void_line) + "</div>"
        "<div class='kysah-dna-line'>Alphabet DNA · A=Termii anchor · B=Federation bin · "
        "C=Resonance+void correlate · D=duty-of-care escalation · "
        "Sentinel order=<b>Area→Home</b></div>"
        "<div class='kysah-tier-legend'><span class='kysah-tier kysah-gold'>State Gold</span> · "
        "<span class='kysah-tier kysah-cyan'>Area Cyan</span> · "
        "<span class='kysah-tier kysah-white'>Home White</span> · "
        "<span class='kysah-tier kysah-red'>PU Red</span></div>"
        "</div>",
        unsafe_allow_html=True,
    )


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


@st.cache_data(ttl=15, show_spinner=False)
def _sovereign_joint_bundle_cached(_cache_key: str) -> dict[str, Any]:
    """Live JSONL + stub → AZK spine + fleet consent gate — feeds Sentinel weights + sniffs."""
    return build_approved_logistics_bundle(AZK_CORRIDOR_NODES, _kgec_azk_corridor_fractional())


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


def _html_sovereign_enrollment_forensic_strip(
    *,
    headline: dict[str, int],
    meta_ledger: dict[str, Any],
    national_sum: int,
    state_row_count: int,
) -> str:
    """Always-on forensic strip — ABU / KASU / NUBA + national Σ (36 states + FCT)."""
    abu = int(headline.get("ABU") or 0)
    kasu = int(headline.get("KASU") or 0)
    nuba = int(headline.get("NUBA") or 0)
    kd_tot = int(meta_ledger.get("kaduna_total") or 0)
    cy = html.escape(str(meta_ledger.get("academic_cycle") or ""))
    return (
        '<div class="kgec-sovereign-enrollment-forensic" role="region" '
        'aria-label="Sovereign enrollment forensic headline">'
        '<p class="kgec-sovereign-enrollment-cap">Sovereign Enrollment Ledger · forensic headline</p>'
        f'<p class="kgec-sovereign-enrollment-cycle">Academic cycle <strong>{cy}</strong> · '
        f'<span class="kgec-sovereign-enrollment-sum">National Σ (36 states + FCT): {national_sum:,}</span></p>'
        '<div class="kgec-sovereign-enrollment-grid">'
        f'<span class="kgec-sov-cell"><abbr title="Ahmadu Bello University">ABU</abbr> Zaria · <strong>{abu:,}</strong></span>'
        f'<span class="kgec-sov-cell"><abbr title="Kaduna State University">KASU</abbr> · <strong>{kasu:,}</strong></span>'
        f'<span class="kgec-sov-cell"><abbr title="Nuhu Bamalli Polytechnic">NUBA</abbr> total · <strong>{nuba:,}</strong></span>'
        f'<span class="kgec-sov-cell kgec-sov-cell--kaduna">Kaduna pilot Σ · <strong>{kd_tot:,}</strong></span>'
        f'<span class="kgec-sov-cell kgec-sov-cell--meta">{state_row_count} jurisdiction rows · expander below</span>'
        "</div></div>"
    )


def _html_live_student_pulse_strip(snap: dict[str, Any]) -> str:
    """NAFC header meter — Mophi Glass: dense numbers + long copy only in native title tooltips."""
    th = html.escape(str(snap.get("tooltip_historical") or ""))
    tp = html.escape(str(snap.get("tooltip_predictive") or ""))
    tl = html.escape(str(snap.get("tooltip_live") or ""))
    tn = html.escape(str(snap.get("tooltip_nuba") or "").strip())
    cy = html.escape(str(snap.get("academic_cycle_label") or ""))
    seed = int(snap.get("kaduna_seed_enrolment_notional") or 0)
    wn = int(snap.get("dapi_wards_indexed") or 0)
    vt = int(snap.get("dapi_verification_events_total") or 0)
    _nuba_chip = ""
    if tn:
        _nuba_chip = (
            '<span class="kgec-mophi-glass-tip kgec-live-pulse-metric kgec-live-pulse-nuba" '
            f'title="{tn}">NUBA · Zaria / Kafanchan</span>'
        )
    _degraded = ""
    if snap.get("pulse_degraded"):
        _degraded = (
            '<span class="kgec-live-pulse-degraded" title="Pulse snapshot degraded — see tooltips / logs">'
            "· degraded</span>"
        )
    return (
        '<div class="kgec-live-student-pulse-strip" role="region" aria-label="Live student pulse NAFC">'
        '<span class="kgec-live-pulse-label">Live Student Pulse</span>'
        f'<span class="kgec-live-pulse-cycle">{cy}</span>'
        f'{_degraded}'
        f'<span class="kgec-mophi-glass-tip kgec-live-pulse-metric" title="{th}">Kaduna seed · {seed:,}</span>'
        f'<span class="kgec-mophi-glass-tip kgec-live-pulse-metric" title="{tp}">Nowcast lane</span>'
        f'<span class="kgec-mophi-glass-tip kgec-live-pulse-metric" title="{tl}">'
        f"DAPI · {wn:,} wards · {vt:,} events</span>"
        f"{_nuba_chip}"
        "</div>"
    )


def _html_eagle_ticker(shouts: list[dict], *, alert_pulse: bool) -> str:
    parts: list[str] = []
    for s in (shouts or [])[:14]:
        pulse = str(s.get("pulse") or "")
        if pulse == "friction":
            cls = "p-friction"
        elif pulse == "opportunity":
            cls = "p-opportunity"
        else:
            cls = "p-liquidity"
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
        seconds=158.0,
    )
    _crest_anchor = (
        "<span class='kgec-crest-anchor'>K-GEC · Komi-Generative Cloud</span>"
        "<span class='kgec-crest-anchor-sub'> intelligence crest · ward-sniff patrol</span>"
    )
    mq_sub = _kgec_marquee_pair(
        "K-GEC · Komi-Generative Cloud · trade velocity · infrastructure voids · security friction · kinetic only",
        seconds=182.0,
    )
    mq_live = _kgec_marquee_pair(
        "K-GEC · Komi-Generative Cloud · HOVER · PATROL · SNIFF · LIVE",
        seconds=152.0,
    )
    mq_lbl = _kgec_marquee_pair(
        "K-GEC · Komi-Generative Cloud · intelligence stream · cinematic cyan cadence",
        seconds=168.0,
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
    _kysah_sniffs = kysah_escalation_patrol_sniffs(load_kysah_stub_records())
    _kysah_ntw_sniffs = _kgec_ntw_resonance_sniffs(_ntw_op) + _kysah_sniffs
    if not st.session_state.get("generative_eagle_ticker", True):
        st.components.v1.html(
            "<script>try{var p=window.parent;var d="
            + json.dumps(
                _kgec_patrol_bundle([], extra_sniffs=_kysah_ntw_sniffs)
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
    _kysah_rows = kysah_escalation_shout_rows(load_kysah_stub_records())
    shouts = _kysah_rows + list(shouts)
    shouts.sort(key=lambda r: (-float(r.get("weight") or 0), -float(r.get("ts_sort") or 0)))
    shouts = shouts[:16]
    pulse = bool(st.session_state.get("eagle_friction_pulse", True)) and (
        friction_alert_active(shouts) or bool(_kysah_rows)
    )
    tick_html = _html_eagle_ticker(shouts, alert_pulse=pulse)
    _patrol = _kgec_patrol_bundle(
        shouts,
        extra_sniffs=_kysah_ntw_sniffs,
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
    try:
        init_verification_store()
        _ev_pulse = ward_verification_counts()
        _vk_p = len(_ev_pulse)
        _vt_p = sum(int(v) for v in _ev_pulse.values())
        _student_pulse_snap = live_student_pulse_snapshot(
            verification_ward_keys=_vk_p,
            verification_event_total=_vt_p,
        )
    except Exception:
        _student_pulse_snap = fallback_live_student_pulse_snapshot()
    try:
        st.markdown(
            '<div class="kgec-eagle-voice-pulse-rail">'
            + _html_live_student_pulse_strip(_student_pulse_snap)
            + "</div>",
            unsafe_allow_html=True,
        )
    except Exception:
        st.caption(
            "Live Student Pulse strip degraded — NAFC snapshot or HTML render failed; "
            "verify nafc_student_load_pipeline and kaduna pilot JSON."
        )


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
    p.__kgecGlideMs = null;
    p.__kgecTargets = [{x:0.5,y:0.45}];
    p.__kgecSniffs = [];
    p.__kgecTargetWeights = null;
    /* National canvas — mirrors app.py _NG_FRAC_* + footprint inset (_NG_PAD_*); glide ~3.25s cinematic ease. */
    var KGE_NG = { xmin: 0.22, xmax: 0.76, ymin: 0.24, ymax: 0.685 };
    var KGE_PAD = { x: 0.068, y: 0.058 };
    function kgecClampNG(pt){
      var x = Number(pt.x), y = Number(pt.y);
      return {
        x: Math.min(KGE_NG.xmax - KGE_PAD.x, Math.max(KGE_NG.xmin + KGE_PAD.x, x)),
        y: Math.min(KGE_NG.ymax - KGE_PAD.y, Math.max(KGE_NG.ymin + KGE_PAD.y, y))
      };
    }
    p.__kgecSetPatrol = function(obj){
      try {
        if (!obj || typeof obj !== 'object') return;
        p.__kgecKysahSentinel = !!obj.kysahSentinelOverride;
        if (Array.isArray(obj.targets) && obj.targets.length)
          p.__kgecTargets = obj.targets.map(kgecClampNG);
        if (Array.isArray(obj.sniffs))
          p.__kgecSniffs = obj.sniffs.map(function(s){ return String(s); });
        if (Array.isArray(obj.targetWeights) && obj.targetWeights.length === p.__kgecTargets.length){
          p.__kgecTargetWeights = obj.targetWeights.map(function(v){
            var n = Number(v);
            if (!isFinite(n)) n = 0.42;
            return Math.max(0.18, Math.min(1, n));
          });
        } else {
          p.__kgecTargetWeights = null;
        }
        var svgEl = p.__kgecEagleEl;
        if (svgEl && svgEl.classList){
          if (p.__kgecKysahSentinel) svgEl.classList.add('kgec-eagle-kysah-sentinel');
          else svgEl.classList.remove('kgec-eagle-kysah-sentinel');
        }
        if ('glideMs' in obj) {
          if (obj.glideMs === null || obj.glideMs === undefined) {
            p.__kgecGlideMs = null;
          } else {
            var gv = Number(obj.glideMs);
            p.__kgecGlideMs = (isFinite(gv) && gv >= 800 && gv <= 8000) ? gv : null;
          }
        } else {
          p.__kgecGlideMs = null;
        }
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
        + '<text x="6" y="188" fill="#D4AF37" font-size="8" font-weight="800" font-family="ui-monospace,monospace">K-GEC · Sentinel</text>'
        + '<text x="168" y="188" fill="#00E5FF" font-size="7.5" font-weight="700" font-family="ui-monospace,monospace">774 LGA · geofenced</text>'
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
        layer.style.cssText = 'position:absolute;left:0;top:0;right:0;bottom:0;pointer-events:none;overflow:visible;z-index:6;border-radius:14px;transform:translateZ(0);backface-visibility:hidden;-webkit-backface-visibility:hidden;';
        par.appendChild(layer);
        var svg = doc.createElementNS('http://www.w3.org/2000/svg','svg');
        svg.setAttribute('class','kgec-eagle-svg');
        svg.setAttribute('viewBox','0 0 340 200');
        svg.setAttribute('preserveAspectRatio','xMidYMid meet');
        svg.style.cssText = 'position:absolute;width:min(104px,23vw);height:min(62px,13.5vw);min-width:88px;min-height:52px;left:45%;top:40%;'
          + 'filter:drop-shadow(0 0 12px rgba(255,215,80,0.92)) drop-shadow(0 0 6px rgba(0,229,255,0.28)) drop-shadow(0 4px 12px rgba(0,0,0,0.72));'
          + 'transition:left 3.25s cubic-bezier(0.18,0.82,0.22,1),top 3.25s cubic-bezier(0.18,0.82,0.22,1);will-change:transform,left,top;'
          + 'transform:translate3d(-50%,-50%,0);opacity:1;visibility:visible;';
        p.__kgecSvgUid = (p.__kgecSvgUid || 0) + 1;
        svg.innerHTML = eagleMarkup('kgec'+p.__kgecSvgUid);
        layer.appendChild(svg);
        p.__kgecEagleEl = svg;
        p.__kgecEagleBank = svg.querySelector('.kgec-eagle-bank');
      }
      return layer;
    }
    function currentGlideMs(){
      var g = Number(p.__kgecGlideMs);
      return (isFinite(g) && g >= 800 && g <= 8000) ? Math.round(g) : 3250;
    }
    var DWELL_BASE = 3600;
    function dwellForIndex(idx){
      var tg = p.__kgecTargets || [{x:0.5,y:0.45}];
      var L = tg.length || 1;
      var i = ((idx % L) + L) % L;
      var wt = 0.52;
      if (p.__kgecTargetWeights && p.__kgecTargetWeights.length === L){
        var rv = Number(p.__kgecTargetWeights[i]);
        wt = isFinite(rv) ? rv : 0.52;
      }
      wt = Math.max(0.22, Math.min(1, wt));
      return Math.round(DWELL_BASE * (0.52 + 0.92 * wt));
    }
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
      var glide = currentGlideMs();
      svg.style.transition = 'left '+ (glide/1000) +'s cubic-bezier(0.18,0.82,0.22,1), top '+ (glide/1000) +'s cubic-bezier(0.18,0.82,0.22,1)';
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
      }, glide);
    }
    function majestyLoop(){
      majesticStep();
      var tg = p.__kgecTargets || [{x:0.5,y:0.45}];
      var L = tg.length || 1;
      var destIdx = ((p.__kgecIdx - 1) % L + L) % L;
      var glide = currentGlideMs();
      var nextDelay = glide + dwellForIndex(destIdx);
      p.__kgecMajestyT = setTimeout(majestyLoop, nextDelay);
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

# First main paint · Eagle Voice + ticker (fragment updates AZK hover even when ticker off)
_eagle_voice_live()
_render_sovereign_joint_strip()
_render_kysah_sovereign_ribbon()

_sov_lr, _sov_m = build_sovereign_enrollment_ledger_rows()
_nat_sum = national_ledger_population_sum(_sov_lr)
_headline_counts = kaduna_headline_enrollment_counts()
st.markdown(
    _html_sovereign_enrollment_forensic_strip(
        headline=_headline_counts,
        meta_ledger=_sov_m,
        national_sum=_nat_sum,
        state_row_count=len(_sov_lr),
    ),
    unsafe_allow_html=True,
)

_fee_bind = float(st.session_state.get("sov_rev_ngn_per_v", 1000))
_vpm_bind = float(st.session_state.get("sov_rev_vpm", 1.0))
_sov_lr_albasa = bind_albasa_monthly_pool_to_ledger_rows(
    _sov_lr,
    ngn_per_verification=_fee_bind,
    verifications_per_student_per_month=_vpm_bind,
)
_kd_rows_albasa = bind_albasa_pool_to_kaduna_institution_rows(
    list(_sov_m.get("kaduna_institution_rows") or []),
    ngn_per_verification=_fee_bind,
    verifications_per_student_per_month=_vpm_bind,
)

with st.expander(
    "Sovereign Audit · National Ledger & Albasa (₦1k economics fused)",
    expanded=True,
):
    st.caption(
        "Enrollment ledger and Albasa ₦1k pool stay on this Intelligent Map Page — comma-separated display rows."
    )
    _tab_led, _tab_spec = st.tabs(
        ("Enrollment · 36+1 + Albasa pool", "Albasa specification (reference JSON)"),
    )
    with _tab_led:
        st.markdown('<div class="kgec-sovereign-audit-led">', unsafe_allow_html=True)
        st.caption(
            f"Cycle {_sov_m['academic_cycle']} · national envelope **{NATIONAL_NOTIONAL_TOTAL_STUDENTS:,}** · "
            "fee × intensity follow **`sov_rev_ngn_per_v`** / **`sov_rev_vpm`** (session defaults below)."
        )
        _led_display = [
            {
                "State": r["state_en"],
                "Code": r["state_code"],
                "Students": f'{int(r.get("notional_students") or 0):,}',
                "Albasa pool (₦/mo)": f'₦{int(r.get("albasa_monthly_pool_ngn") or 0):,}',
                "Pilot highlight": r.get("pilot_highlight") or "",
                "Source": r.get("source_note") or "",
            }
            for r in _sov_lr_albasa
        ]
        st.dataframe(
            _led_display,
            column_config={
                "State": st.column_config.TextColumn("State", width=130),
                "Code": st.column_config.TextColumn("Code", width=70),
                "Students": st.column_config.TextColumn("Students", width=110),
                "Albasa pool (₦/mo)": st.column_config.TextColumn("Albasa ₦/mo", width=145),
                "Pilot highlight": st.column_config.TextColumn("Pilot highlight", width=300),
                "Source": st.column_config.TextColumn("Source", width=340),
            },
            hide_index=True,
            use_container_width=True,
            height=440,
        )
        st.markdown("**Kaduna pilot · institutions + Albasa pool per row**")
        _kd_disp = [
            {
                "abbr": str(x.get("abbr") or ""),
                "institution": str(x.get("institution") or ""),
                "students": f'{int(x.get("students") or 0):,}',
                "Albasa (₦/mo)": f'₦{int(x.get("albasa_monthly_pool_ngn") or 0):,}',
                "note": str(x.get("note") or ""),
            }
            for x in _kd_rows_albasa
        ]
        st.dataframe(
            _kd_disp,
            column_config={
                "abbr": st.column_config.TextColumn("abbr", width=72),
                "institution": st.column_config.TextColumn("Institution", width=260),
                "students": st.column_config.TextColumn("Students", width=100),
                "Albasa (₦/mo)": st.column_config.TextColumn("Albasa ₦/mo", width=130),
                "note": st.column_config.TextColumn("note / LGA", width=380),
            },
            hide_index=True,
            use_container_width=True,
            height=280,
        )
        st.markdown("</div>", unsafe_allow_html=True)
        with st.expander("Albasa ₦1k · commander benchmarks (reference)", expanded=False):
            _fee_b = float(st.session_state.get("sov_rev_ngn_per_v", 1000))
            _vpm_b = float(st.session_state.get("sov_rev_vpm", 1.0))
            st.markdown(
                html_albasa_commander_benchmark_table(
                    albasa_commander_benchmark_rows(fee_ngn=_fee_b, verifications_per_student_per_month=_vpm_b)
                ),
                unsafe_allow_html=True,
            )
        st.info(
            "**Albasa revenue MOU** (60 / 25 / 15) — Kaduna **Zazzau 31** & institutional lattice render "
            "on-map below when Total Reality selects Kaduna."
        )
    with _tab_spec:
        st.markdown(
            "**Embedded Commander's specification** — JSON contract for auditors."
        )
        st.json(SOVEREIGN_ALBASA_SPEC)

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600&display=swap');
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
  --kgec-forensic-cycle: {_KGEC_FORENSIC_CYCLE_S}s !important;
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
  margin: 0 0 32px 0 !important;
  padding-left: 4px !important;
  padding-right: 4px !important;
  isolation: isolate !important;
  overflow: visible !important;
  transform: translateZ(0) !important;
  -webkit-transform: translateZ(0) !important;
}}
@media (orientation: portrait), (max-width: 960px) {{
  .kgec-sentinel-crest {{
    flex-direction: column !important;
    align-items: stretch !important;
    gap: 10px !important;
  }}
  .kgec-crest-live {{ margin-left: 0 !important; align-self: flex-start !important; }}
  .kgec-crest-mq .kgec-mq-track {{
    animation-timing-function: cubic-bezier(0.35, 0.02, 0.2, 1) !important;
  }}
}}
/* Smoke protocol — sticky crest: no clipping ancestors on resize (mobile ↔ desktop) */
section.main [data-testid="element-container"]:has(.kgec-sentinel-stack),
section.main [data-testid="element-container"]:has(.kgec-sentinel-stack) > div {{
  overflow: visible !important;
}}
section.main [data-testid="stVerticalBlock"]:has(.kgec-sentinel-stack),
section.main [data-testid="column"]:has(.kgec-sentinel-stack) {{
  overflow-x: visible !important;
  overflow-y: visible !important;
}}
section.main [data-testid="block-container"]:has(.kgec-sentinel-stack) {{
  overflow-x: visible !important;
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
  margin: 14px 0 0 0 !important;
  padding: 8px 10px 10px !important;
  background: #000000 !important;
  border-radius: 12px !important;
  border: 1px solid rgba(212, 175, 55, 0.42) !important;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.55) !important;
  overflow: visible !important;
}}
/* Sovereign Joint — ingest spine + Determinants-4 Temporal Hierarchy Lamp */
.kgec-joint-strip {{
  margin: 0 0 16px 0 !important;
  padding: 12px 14px !important;
  border-radius: 12px !important;
  border: 1px solid rgba(0, 229, 255, 0.28) !important;
  background: linear-gradient(135deg, rgba(0, 28, 72, 0.88) 0%, rgba(0, 12, 40, 0.92) 100%) !important;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.06), 0 6px 22px rgba(0,0,0,0.35) !important;
}}
.kgec-joint-strip-hdr {{
  font-family: ui-monospace, monospace !important;
  font-size: clamp(0.62rem, 1.8vw, 0.74rem) !important;
  font-weight: 800 !important;
  letter-spacing: 0.12em !important;
  color: #D4AF37 !important;
  margin-bottom: 10px !important;
}}
.kgec-joint-purpose {{ color: rgba(0, 229, 255, 0.92) !important; font-weight: 600 !important; }}
.kgec-joint-ingest {{ color: rgba(180, 255, 200, 0.95) !important; font-weight: 700 !important; }}
.kgec-joint-src {{ color: rgba(0, 229, 255, 0.55) !important; font-weight: 500 !important; }}
.kgec-joint-grid {{
  display: flex !important;
  flex-wrap: wrap !important;
  gap: 14px 22px !important;
  align-items: flex-start !important;
  justify-content: space-between !important;
}}
.kgec-joint-status {{
  flex: 2 1 240px !important;
  min-width: 0 !important;
  font-family: ui-monospace, monospace !important;
  font-size: 0.62rem !important;
  line-height: 1.5 !important;
  color: rgba(230, 245, 255, 0.9) !important;
}}
.kgec-joint-lamp-wrap {{
  flex: 0 0 auto !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}}
.kgec-joint-ul {{ margin: 6px 0 0 1rem !important; padding: 0 !important; }}
.kgec-joint-rej {{ color: rgba(255, 180, 120, 0.85) !important; margin-top: 8px !important; }}
.kgec-joint-legal-box {{
  flex: 1 1 100% !important;
  min-width: 0 !important;
  margin-top: 12px !important;
  padding: 0 !important;
  width: 100% !important;
  box-sizing: border-box !important;
}}
.kgec-joint-legal {{
  color: rgba(200, 220, 255, 0.78) !important;
  margin: 0 !important;
  font-size: clamp(0.58rem, 2.4vw, 0.68rem) !important;
  line-height: 1.55 !important;
  word-break: break-word !important;
  overflow-wrap: anywhere !important;
}}
.kgec-joint-residency {{ color: rgba(255, 235, 200, 0.72) !important; }}
.kgec-joint-counsel {{ color: rgba(255, 200, 120, 0.82) !important; }}
.kgec-temporal-lamp {{
  position: relative !important;
  flex: 0 0 auto !important;
  width: 118px !important;
  height: 118px !important;
  margin: 4px auto !important;
}}
@media (max-width: 720px) {{
  .kgec-joint-strip {{ padding: 14px 12px !important; }}
  .kgec-joint-strip-hdr {{
    line-height: 1.38 !important;
    letter-spacing: 0.08em !important;
    margin-bottom: 12px !important;
  }}
  .kgec-joint-grid {{
    flex-direction: column !important;
    align-items: stretch !important;
    gap: 14px !important;
  }}
  .kgec-joint-status {{ flex: 1 1 auto !important; max-width: 100% !important; order: 1 !important; }}
  .kgec-joint-legal-box {{ order: 2 !important; margin-top: 4px !important; }}
  .kgec-joint-lamp-wrap {{ width: 100% !important; order: 3 !important; }}
  .kgec-temporal-lamp {{
    width: 104px !important;
    height: 104px !important;
    margin: 6px auto 2px auto !important;
  }}
  .kgec-joint-legal {{
    padding: 10px 10px !important;
    background: rgba(0, 0, 0, 0.35) !important;
    border-radius: 8px !important;
    border-left: 3px solid rgba(212, 175, 55, 0.55) !important;
  }}
}}
/* KYSAH ribbon — Sam-Sam iPhone: un-clipped parents + forensic kinetic (synced via --kgec-forensic-cycle) */
section.main div[data-testid="stMarkdownContainer"]:has(.kysah-sovereign-ribbon),
section.main div[data-testid="stMarkdown"]:has(.kysah-sovereign-ribbon) {{
  overflow: visible !important;
  max-height: none !important;
}}
section.main .block-container:has(.kysah-sovereign-ribbon) {{
  overflow-x: visible !important;
  overflow-y: visible !important;
}}
@keyframes kysahRibbonForensic {{
  0%, 100% {{
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.05), 0 6px 20px rgba(0,0,0,0.4) !important;
    border-color: rgba(191, 149, 63, 0.42) !important;
  }}
  50% {{
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.08), 0 8px 26px rgba(0, 229, 255, 0.09) !important;
    border-color: rgba(191, 149, 63, 0.58) !important;
  }}
}}
section.main .kysah-sovereign-ribbon,
section.main [data-testid="stMarkdown"] .kysah-sovereign-ribbon {{
  overflow: visible !important;
  contain: none !important;
  box-sizing: border-box !important;
  width: 100% !important;
  max-width: 100% !important;
  margin: 0 0 14px 0 !important;
  padding: 12px 12px max(12px, env(safe-area-inset-bottom)) 12px !important;
  border-radius: 12px !important;
  border: 1px solid rgba(191, 149, 63, 0.42) !important;
  background: linear-gradient(165deg, rgba(20, 40, 72, 0.95) 0%, rgba(0, 18, 48, 0.98) 100%) !important;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.05), 0 6px 20px rgba(0,0,0,0.4) !important;
  -webkit-text-size-adjust: 100% !important;
  text-size-adjust: 100% !important;
  position: relative !important;
  z-index: 6 !important;
  animation: kysahRibbonForensic var(--kgec-forensic-cycle, 22.4s) ease-in-out infinite !important;
}}
.kysah-protocol-line {{
  font-family: ui-monospace, monospace !important;
  font-size: clamp(0.56rem, 2.5vw, 0.66rem) !important;
  font-weight: 700 !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
  color: rgba(212, 175, 55, 0.95) !important;
  margin-bottom: 8px !important;
  line-height: 1.45 !important;
  word-break: break-word !important;
}}
.kysah-fed-line {{
  font-family: ui-monospace, monospace !important;
  font-size: clamp(0.58rem, 2.6vw, 0.68rem) !important;
  line-height: 1.55 !important;
  color: rgba(220, 245, 255, 0.92) !important;
  word-break: break-word !important;
  overflow-wrap: anywhere !important;
  margin-bottom: 8px !important;
}}
.kysah-alert-line {{
  font-family: ui-monospace, monospace !important;
  font-size: clamp(0.58rem, 2.5vw, 0.66rem) !important;
  line-height: 1.5 !important;
  color: rgba(0, 229, 255, 0.95) !important;
  margin-bottom: 6px !important;
  word-break: break-word !important;
}}
.kysah-mode-sentinel {{ color: rgba(255, 120, 100, 0.98) !important; }}
.kysah-mode-pill {{
  display: inline-block !important;
  padding: 2px 8px !important;
  margin-right: 6px !important;
  border-radius: 6px !important;
  font-weight: 800 !important;
  letter-spacing: 0.06em !important;
  background: rgba(220, 38, 38, 0.35) !important;
  border: 1px solid rgba(255, 160, 140, 0.45) !important;
}}
.kysah-mode-monitor .kysah-mode-pill {{
  background: rgba(46, 204, 113, 0.22) !important;
  border-color: rgba(120, 255, 200, 0.35) !important;
  color: rgba(200, 255, 220, 0.95) !important;
}}
.kysah-void-line {{
  font-family: ui-monospace, monospace !important;
  font-size: clamp(0.55rem, 2.4vw, 0.64rem) !important;
  line-height: 1.5 !important;
  color: rgba(255, 210, 160, 0.88) !important;
  margin-bottom: 8px !important;
  word-break: break-word !important;
}}
.kysah-dna-line {{
  font-size: clamp(0.52rem, 2.2vw, 0.6rem) !important;
  line-height: 1.45 !important;
  color: rgba(180, 200, 230, 0.72) !important;
  margin-bottom: 8px !important;
}}
.kysah-tier-legend {{
  font-size: clamp(0.52rem, 2.2vw, 0.6rem) !important;
  letter-spacing: 0.04em !important;
}}
.kysah-tier {{ font-weight: 700 !important; }}
.kysah-gold {{ color: #D4AF37 !important; }}
.kysah-cyan {{ color: #00E5FF !important; }}
.kysah-white {{ color: rgba(248, 252, 255, 0.95) !important; }}
.kysah-red {{ color: #DC2626 !important; }}
.kysah-sovereign-ribbon--idle {{
  border-color: rgba(0, 229, 255, 0.28) !important;
}}
@media (max-width: 720px) {{
  section.main .kysah-sovereign-ribbon {{
    padding-left: max(12px, env(safe-area-inset-left)) !important;
    padding-right: max(12px, env(safe-area-inset-right)) !important;
  }}
}}
.kgec-roll {{
  position: absolute !important;
  left: 50% !important;
  top: 50% !important;
  transform: translate(-50%, -50%) !important;
  border-radius: 50% !important;
  box-sizing: border-box !important;
  pointer-events: none !important;
}}
.kgec-roll-gold {{
  width: 100% !important;
  height: 100% !important;
  border: 3px solid rgba(212, 175, 55, 0.9) !important;
  box-shadow: 0 0 18px rgba(212, 175, 55, 0.25) !important;
  animation: kgecLampGold var(--kgec-forensic-cycle, 22.4s) ease-in-out infinite !important;
}}
.kgec-roll-cyan {{
  width: 78% !important;
  height: 78% !important;
  border: 2px solid rgba(0, 229, 255, 0.8) !important;
  box-shadow: 0 0 14px rgba(0, 229, 255, 0.2) !important;
  animation: kgecLampCyan 17.5s ease-in-out infinite !important;
  animation-delay: 0.22s !important;
}}
.kgec-roll-white {{
  width: 56% !important;
  height: 56% !important;
  border: 2px solid rgba(248, 252, 255, 0.92) !important;
  box-shadow: 0 0 12px rgba(255, 255, 255, 0.12) !important;
  animation: kgecLampWhite 12.88s ease-in-out infinite !important;
  animation-delay: 0.38s !important;
}}
.kgec-roll-red {{
  width: 36% !important;
  height: 36% !important;
  border: 2px solid rgba(220, 38, 38, 0.92) !important;
  box-shadow: 0 0 14px rgba(220, 38, 38, 0.28) !important;
  animation: kgecLampRed 8.96s ease-in-out infinite !important;
  animation-delay: 0.52s !important;
}}
.kgec-roll-core {{
  width: 14% !important;
  height: 14% !important;
  background: radial-gradient(circle at 35% 35%, #fff 0%, rgba(212,175,55,0.55) 45%, rgba(0,20,60,0.95) 100%) !important;
  animation: kgecLampCore 7s ease-in-out infinite !important;
}}
@keyframes kgecLampGold {{
  0%, 100% {{ opacity: 0.38; transform: translate(-50%, -50%) scale(0.94); }}
  28% {{ opacity: 1; transform: translate(-50%, -50%) scale(1); }}
  62% {{ opacity: 0.48; transform: translate(-50%, -50%) scale(1.03); }}
}}
@keyframes kgecLampCyan {{
  0%, 100% {{ opacity: 0.35; transform: translate(-50%, -50%) scale(0.93); }}
  32% {{ opacity: 0.95; transform: translate(-50%, -50%) scale(1); }}
  68% {{ opacity: 0.42; transform: translate(-50%, -50%) scale(1.04); }}
}}
@keyframes kgecLampWhite {{
  0%, 100% {{ opacity: 0.32; transform: translate(-50%, -50%) scale(0.92); }}
  36% {{ opacity: 0.92; transform: translate(-50%, -50%) scale(1); }}
  72% {{ opacity: 0.38; transform: translate(-50%, -50%) scale(1.05); }}
}}
@keyframes kgecLampRed {{
  0%, 100% {{ opacity: 0.28; transform: translate(-50%, -50%) scale(0.9); }}
  40% {{ opacity: 1; transform: translate(-50%, -50%) scale(1); }}
  78% {{ opacity: 0.35; transform: translate(-50%, -50%) scale(1.06); }}
}}
@keyframes kgecLampCore {{
  0%, 100% {{ opacity: 0.55; }}
  50% {{ opacity: 1; }}
}}
/* KYSAH Crimson Sentinel — Eagle SVG when logistics patrol is overridden */
.kgec-eagle-svg.kgec-eagle-kysah-sentinel .kgec-eagle-bank {{
  filter: drop-shadow(0 0 20px rgba(220, 38, 38, 0.88)) drop-shadow(0 0 12px rgba(255, 99, 71, 0.55))
    drop-shadow(0 3px 2px rgba(0, 0, 0, 0.55)) !important;
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
  z-index: 0 !important;
}}
.gcslc-map-canvas-host {{
  width: 100% !important;
  margin: 12px 0 0 0 !important;
  padding: 0 !important;
  scroll-margin-top: 14px !important;
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
/* Prism Terminal — vertical roll-up Gold→Cyan→White→Red · clamped monospace · shimmer prism shell */
.kgec-prism-terminal.sovereign-detail-widget {{
  position: relative !important;
  margin-top: 18px !important;
  margin-bottom: 12px !important;
  padding: 16px 14px 18px !important;
  border-radius: 16px !important;
  border: 2px solid rgba(212, 175, 55, 0.55) !important;
  background: linear-gradient(165deg, rgba(0, 12, 56, 0.97) 0%, rgba(0, 0, 128, 0.94) 42%, rgba(0, 22, 72, 0.98) 100%) !important;
  box-shadow:
    inset 0 1px 0 rgba(255, 248, 220, 0.12),
    inset 0 -1px 0 rgba(0, 229, 255, 0.06),
    0 10px 36px rgba(0, 0, 0, 0.45),
    0 0 42px rgba(212, 175, 55, 0.07) !important;
  overflow: hidden !important;
  isolation: isolate !important;
  touch-action: manipulation !important;
}}
.kgec-prism-terminal::before {{
  content: "" !important;
  position: absolute !important;
  inset: -3px !important;
  background: linear-gradient(
    118deg,
    transparent 0%,
    rgba(212, 175, 55, 0.24) 38%,
    rgba(0, 229, 255, 0.14) 50%,
    rgba(212, 175, 55, 0.2) 62%,
    transparent 100%
  ) !important;
  background-size: 240% 240% !important;
  animation: kgecPrismShimmer 14s ease-in-out infinite !important;
  opacity: 0.5 !important;
  pointer-events: none !important;
  z-index: 0 !important;
}}
@keyframes kgecPrismShimmer {{
  0%, 100% {{ background-position: 0% 40%; }}
  50% {{ background-position: 100% 60%; }}
}}
.kgec-prism-terminal > * {{
  position: relative !important;
  z-index: 1 !important;
}}
.kgec-prism-cap {{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  font-size: clamp(0.64rem, 2.6vw, 0.76rem) !important;
  font-weight: 800 !important;
  letter-spacing: 0.14em !important;
  text-transform: uppercase !important;
  color: #D4AF37 !important;
  margin-bottom: 12px !important;
  padding-bottom: 8px !important;
  border-bottom: 1px solid rgba(212, 175, 55, 0.38) !important;
}}
.kgec-prism-mono {{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  font-variant-numeric: tabular-nums !important;
  -webkit-text-size-adjust: 100% !important;
  text-size-adjust: 100% !important;
}}
.kgec-prism-handshake {{
  margin-bottom: 14px !important;
  padding: 12px !important;
  border-radius: 12px !important;
  background: rgba(0, 0, 0, 0.4) !important;
  border: 1px solid rgba(0, 229, 255, 0.24) !important;
}}
.kgec-prism-handshake p {{
  margin: 0 0 10px 0 !important;
  line-height: 1.55 !important;
  font-size: clamp(0.68rem, 3.1vw, 0.84rem) !important;
  color: rgba(235, 248, 255, 0.94) !important;
}}
.kgec-prism-handshake p:last-child {{
  margin-bottom: 0 !important;
}}
.kgec-prism-stack {{
  display: flex !important;
  flex-direction: column !important;
  gap: 10px !important;
  margin-bottom: 14px !important;
}}
.kgec-prism-tier {{
  display: flex !important;
  flex-direction: column !important;
  gap: 6px !important;
  padding: 12px 12px 12px 14px !important;
  border-radius: 10px !important;
  background: rgba(0, 18, 48, 0.75) !important;
  border: 1px solid rgba(255, 255, 255, 0.07) !important;
  animation: kgecPrismTierRise 0.88s ease-out both !important;
}}
.kgec-prism-tier:nth-child(1) {{ animation-delay: 0.05s !important; }}
.kgec-prism-tier:nth-child(2) {{ animation-delay: 0.14s !important; }}
.kgec-prism-tier:nth-child(3) {{ animation-delay: 0.23s !important; }}
.kgec-prism-tier:nth-child(4) {{ animation-delay: 0.32s !important; }}
@keyframes kgecPrismTierRise {{
  from {{ opacity: 0; transform: translateY(14px); }}
  to {{ opacity: 1; transform: translateY(0); }}
}}
.kgec-prism-tier-gold {{ border-left: 5px solid #D4AF37 !important; }}
.kgec-prism-tier-cyan {{ border-left: 5px solid #00E5FF !important; }}
.kgec-prism-tier-white {{ border-left: 5px solid rgba(248, 252, 255, 0.95) !important; }}
.kgec-prism-tier-red {{ border-left: 5px solid #DC2626 !important; }}
.kgec-prism-tier-val {{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  font-size: clamp(1.32rem, 5.2vw, 1.82rem) !important;
  font-weight: 800 !important;
  color: #D4AF37 !important;
  letter-spacing: 0.03em !important;
}}
.kgec-prism-tier-cyan .kgec-prism-tier-val {{ color: #00E5FF !important; }}
.kgec-prism-tier-white .kgec-prism-tier-val {{ color: rgba(248, 252, 255, 0.98) !important; }}
.kgec-prism-tier-red .kgec-prism-tier-val {{ color: #FCA5A5 !important; }}
.kgec-prism-tier-lbl {{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  font-size: clamp(0.66rem, 2.9vw, 0.8rem) !important;
  line-height: 1.52 !important;
  color: rgba(220, 235, 255, 0.9) !important;
}}
.kgec-prism-record {{
  padding-top: 12px !important;
  border-top: 1px solid rgba(212, 175, 55, 0.3) !important;
}}
.kgec-prism-record-h {{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  font-weight: 800 !important;
  font-size: clamp(0.68rem, 2.7vw, 0.8rem) !important;
  letter-spacing: 0.1em !important;
  text-transform: uppercase !important;
  color: #D4AF37 !important;
  margin-bottom: 8px !important;
}}
.kgec-prism-record-lead {{
  margin: 0 0 10px 0 !important;
  font-size: clamp(0.66rem, 2.85vw, 0.78rem) !important;
  line-height: 1.55 !important;
  color: rgba(0, 229, 255, 0.92) !important;
}}
.kgec-prism-pre {{
  margin: 0 !important;
  padding: 12px !important;
  max-height: min(280px, 42vh) !important;
  overflow: auto !important;
  white-space: pre-wrap !important;
  word-break: break-word !important;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  font-size: clamp(0.64rem, 2.75vw, 0.76rem) !important;
  line-height: 1.55 !important;
  color: rgba(230, 242, 255, 0.92) !important;
  background: rgba(0, 0, 0, 0.38) !important;
  border-radius: 10px !important;
  border: 1px solid rgba(212, 175, 55, 0.22) !important;
}}
@media (orientation: landscape) and (min-width: 720px) {{
  .kgec-prism-terminal.sovereign-detail-widget {{
    max-width: 460px !important;
    margin-left: auto !important;
    margin-right: auto !important;
  }}
  .kgec-prism-terminal.kgec-gold-man-monument {{
    max-width: 420px !important;
    margin-left: auto !important;
    margin-right: auto !important;
  }}
}}
/* Gold Man Monument · smart-click · metallic inscription + prism cascade */
.kgec-prism-terminal.kgec-gold-man-monument.gcslc-total-reality {{
  margin-top: 12px !important;
  margin-bottom: 18px !important;
}}
.kgec-gmm-cap {{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  font-size: clamp(0.62rem, 2.55vw, 0.74rem) !important;
  font-weight: 800 !important;
  letter-spacing: 0.16em !important;
  text-transform: uppercase !important;
  color: #D4AF37 !important;
  margin-bottom: 10px !important;
  padding-bottom: 8px !important;
  border-bottom: 1px solid rgba(212, 175, 55, 0.42) !important;
}}
.kgec-gold-man-header {{
  text-align: center !important;
  padding: 4px 6px 14px !important;
  margin-bottom: 10px !important;
  border-bottom: 1px solid rgba(0, 229, 255, 0.18) !important;
}}
.kgec-gold-man-state {{
  display: block !important;
  font-family: ui-serif, Georgia, Cambria, "Times New Roman", Times, serif !important;
  font-weight: 800 !important;
  font-size: clamp(1.28rem, 5.8vw, 1.95rem) !important;
  line-height: 1.18 !important;
  letter-spacing: 0.035em !important;
  margin: 0 0 8px 0 !important;
  padding: 0 2px !important;
  background: linear-gradient(
    105deg,
    #5c4a12 0%,
    #b8860b 14%,
    #d4af37 28%,
    #fffef0 40%,
    #f0e68c 48%,
    #d4af37 56%,
    #8a7220 72%,
    #ffe9a8 86%,
    #5c4a12 100%
  ) !important;
  background-size: 300% 100% !important;
  -webkit-background-clip: text !important;
  background-clip: text !important;
  color: transparent !important;
  -webkit-text-fill-color: transparent !important;
  animation: kgecGoldManMetallic 11s ease-in-out infinite !important;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.58)) drop-shadow(0 0 28px rgba(212, 175, 55, 0.18)) !important;
}}
@keyframes kgecGoldManMetallic {{
  0%, 100% {{ background-position: 5% 50%; }}
  50% {{ background-position: 95% 50%; }}
}}
.kgec-gold-man-sub {{
  margin: 0 !important;
  font-weight: 700 !important;
  color: rgba(0, 229, 255, 0.88) !important;
  opacity: 0.95 !important;
}}
.kgec-gmm-stack {{
  margin-bottom: 12px !important;
}}
.kgec-gmm-forensic {{
  padding-top: 12px !important;
  border-top: 1px solid rgba(212, 175, 55, 0.32) !important;
}}
.kgec-gmm-forensic-h {{
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  font-weight: 800 !important;
  font-size: clamp(0.65rem, 2.6vw, 0.76rem) !important;
  letter-spacing: 0.14em !important;
  text-transform: uppercase !important;
  color: #D4AF37 !important;
  margin-bottom: 8px !important;
}}
.kgec-gmm-pre {{
  max-height: min(320px, 48vh) !important;
}}
/* Mophi Glass — Goldman tooltips: long rivalry / chancellery notes in native title, not inline clutter */
.kgec-katsina-forensic-mophi,
.kgec-kano-forensic-mophi {{
  margin: 10px 0 14px 0 !important;
  padding: 10px 12px !important;
  border-radius: 10px !important;
  border: 1px solid rgba(212, 175, 55, 0.35) !important;
  background: linear-gradient(135deg, rgba(8, 12, 22, 0.92), rgba(18, 28, 44, 0.88)) !important;
  max-width: min(720px, 100%) !important;
  position: relative !important;
  z-index: 2198 !important;
}}
.kgec-katsina-forensic-cap {{
  margin: 0 0 8px 0 !important;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  font-size: clamp(0.62rem, 2.4vw, 0.72rem) !important;
  font-weight: 800 !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  color: rgba(212, 175, 55, 0.95) !important;
}}
.kgec-katsina-forensic-ul {{
  margin: 0 !important;
  padding-left: 1.1rem !important;
  color: rgba(200, 245, 255, 0.88) !important;
  font-size: clamp(0.72rem, 2.8vw, 0.82rem) !important;
  line-height: 1.45 !important;
}}
.kgec-mophi-glass-tip {{
  cursor: help !important;
  text-decoration: underline dotted rgba(212, 175, 55, 0.75) !important;
  text-underline-offset: 3px !important;
}}
.kgec-mophi-revenue-wrap {{
  margin: 8px 0 4px 0 !important;
  padding: 10px 12px !important;
  border-radius: 12px !important;
  border: 1px solid rgba(212, 175, 55, 0.38) !important;
  background: linear-gradient(145deg, rgba(6, 14, 32, 0.94) 0%, rgba(12, 28, 48, 0.9) 100%) !important;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.06), 0 6px 20px rgba(0, 0, 0, 0.42) !important;
  max-width: 100% !important;
  overflow-x: auto !important;
}}
.kgec-mophi-revenue-table {{
  width: 100% !important;
  border-collapse: collapse !important;
  font-family: 'Cormorant Garamond', Georgia, serif !important;
  font-size: clamp(12px, 2.8vw, 15px) !important;
  color: rgba(236, 248, 255, 0.94) !important;
}}
.kgec-mophi-revenue-table th,
.kgec-mophi-revenue-table td {{
  border-bottom: 1px solid rgba(0, 229, 255, 0.18) !important;
  padding: 8px 10px !important;
  text-align: right !important;
}}
.kgec-mophi-revenue-table th:first-child,
.kgec-mophi-revenue-table td:first-child {{
  text-align: left !important;
}}
.kgec-mophi-revenue-table th {{
  font-family: 'Goldman', sans-serif !important;
  font-size: clamp(10px, 2.2vw, 11px) !important;
  letter-spacing: 0.08em !important;
  text-transform: uppercase !important;
  color: #ffdf66 !important;
}}
.kgec-mophi-revenue-table .kgec-mophi-num {{
  font-variant-numeric: tabular-nums !important;
  white-space: nowrap !important;
}}
.kgec-sovereign-enrollment-forensic {{
  margin: 10px 0 14px 0 !important;
  padding: 12px 14px !important;
  border-radius: 12px !important;
  border: 1px solid rgba(0, 229, 255, 0.35) !important;
  background: linear-gradient(168deg, rgba(8, 18, 42, 0.95) 0%, rgba(4, 22, 38, 0.9) 100%) !important;
  box-shadow: inset 0 1px 0 rgba(255, 248, 220, 0.08), 0 8px 24px rgba(0, 0, 0, 0.38) !important;
}}
.kgec-sovereign-enrollment-cap {{
  font-family: 'Goldman', sans-serif !important;
  font-size: clamp(11px, 2.5vw, 12px) !important;
  letter-spacing: 0.14em !important;
  text-transform: uppercase !important;
  color: #ffdf66 !important;
  margin: 0 0 6px 0 !important;
}}
.kgec-sovereign-enrollment-cycle {{
  font-family: 'Cormorant Garamond', Georgia, serif !important;
  font-size: clamp(13px, 3vw, 16px) !important;
  color: rgba(236, 248, 255, 0.94) !important;
  margin: 0 0 10px 0 !important;
}}
.kgec-sovereign-enrollment-sum {{
  color: #7fe8ff !important;
  font-weight: 700 !important;
}}
.kgec-sovereign-enrollment-grid {{
  display: flex !important;
  flex-wrap: wrap !important;
  gap: 8px 14px !important;
  align-items: center !important;
}}
.kgec-sov-cell {{
  font-family: 'Cormorant Garamond', Georgia, serif !important;
  font-size: clamp(12px, 2.85vw, 15px) !important;
  color: rgba(240, 248, 255, 0.92) !important;
  padding: 6px 10px !important;
  border-radius: 8px !important;
  border: 1px solid rgba(212, 175, 55, 0.28) !important;
  background: rgba(0, 16, 40, 0.45) !important;
}}
.kgec-sov-cell--kaduna {{
  border-color: rgba(0, 229, 255, 0.42) !important;
}}
.kgec-sov-cell--meta {{
  font-size: clamp(11px, 2.5vw, 13px) !important;
  opacity: 0.88 !important;
  border-style: dashed !important;
}}
.kgec-live-pulse-degraded {{
  font-family: ui-monospace, monospace !important;
  font-size: clamp(10px, 2.2vw, 11px) !important;
  color: #ffb4b4 !important;
  letter-spacing: 0.06em !important;
}}
section.main .kgec-sovereign-audit-led {{
  max-width: 100% !important;
  overflow-x: auto !important;
  box-sizing: border-box !important;
}}
section.main .kgec-albasa-commander-benchmark .kgec-albasa-fee-foot {{
  margin: 10px 0 0 0 !important;
  font-size: clamp(11px, 2.5vw, 13px) !important;
  line-height: 1.45 !important;
  color: rgba(200, 245, 255, 0.9) !important;
  font-family: 'Cormorant Garamond', Georgia, serif !important;
}}
/* KYSAH synergy — distress bind: LGA (gold) + PU (red) tier pulse intensity */
.kgec-gmm--kysah-focus .kgec-gmm-tier--kysah-pulse {{
  animation: kgecGmmKysahLgaPulse 1.55s ease-in-out infinite !important;
}}
.kgec-gmm--kysah-focus .kgec-gmm-tier--kysah-pulse-intense {{
  animation: kgecGmmKysahPuPulse 1.08s ease-in-out infinite !important;
}}
@keyframes kgecGmmKysahLgaPulse {{
  0%, 100% {{
    box-shadow:
      inset 0 0 0 1px rgba(212, 175, 55, 0.2),
      0 0 10px rgba(212, 175, 55, 0.12) !important;
  }}
  50% {{
    box-shadow:
      inset 0 0 0 2px rgba(212, 175, 55, 0.65),
      0 0 26px rgba(212, 175, 55, 0.42) !important;
  }}
}}
@keyframes kgecGmmKysahPuPulse {{
  0%, 100% {{
    box-shadow:
      inset 0 0 0 1px rgba(220, 38, 38, 0.25),
      0 0 12px rgba(220, 38, 38, 0.18) !important;
  }}
  50% {{
    box-shadow:
      inset 0 0 0 2px rgba(252, 165, 165, 0.85),
      0 0 32px rgba(220, 38, 38, 0.55) !important;
  }}
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
/* Total Reality · Smart click — Gold Man above map sentinel overlay (eagle stays inside iframe host only) */
.gcslc-total-reality.gcslc-tr-handshake-front {{
  position: relative !important;
  z-index: 2200 !important;
  isolation: isolate !important;
}}
/* Generative Eagle · ticker (iPhone scroll-safe · black strip inside Stable Sky) */
.eagle-ticker-shell {{
  display: flex;
  flex-direction: column !important;
  align-items: stretch !important;
  gap: 10px !important;
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
  flex: 0 0 auto !important;
  width: 100% !important;
  font-size: clamp(0.7rem, 2.6vw, 0.84rem);
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: {GOLD} !important;
  text-shadow: 0 1px 3px rgba(0,0,0,0.8);
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
}}
.eagle-ticker-scroll {{
  flex: 1 1 auto !important;
  min-width: 0 !important;
  overflow-x: hidden !important;
  overflow-y: visible !important;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
  white-space: normal !important;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  font-size: clamp(0.72rem, 2.8vw, 0.86rem);
  line-height: 1.55 !important;
  padding-bottom: 2px;
  word-break: break-word !important;
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
  .kgec-roll, .kgec-roll-core {{ animation: none !important; opacity: 0.85 !important; }}
  section.main .kysah-sovereign-ribbon {{ animation: none !important; }}
  .kgec-eagle-svg.kgec-eagle-kysah-sentinel .kgec-eagle-bank {{ filter: none !important; }}
  .kgec-prism-terminal::before {{ animation: none !important; opacity: 0.28 !important; }}
  .kgec-prism-tier {{ animation: none !important; }}
  .kgec-gold-man-state {{
    animation: none !important;
    background: none !important;
    color: #E8D589 !important;
    -webkit-text-fill-color: #E8D589 !important;
    filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.5)) !important;
  }}
  .kgec-gmm--kysah-focus .kgec-gmm-tier--kysah-pulse,
  .kgec-gmm--kysah-focus .kgec-gmm-tier--kysah-pulse-intense {{
    animation: none !important;
    box-shadow: inset 0 0 0 1px rgba(212, 175, 55, 0.45) !important;
  }}
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
_dapi_wards_fc_gate = _phase2.get("wards_fc") if _phase2 else None
_asset_states = _coal_asset_state_names()

init_verification_store()
_dapi_browser_session = ensure_browser_session_id(st.session_state)
_dapi_verify_counts = ward_verification_counts()
_rigasa_wp_pulse = find_ward_pcode_rigasa_igabi(_dapi_wards_fc_gate)
_dapi_overload_wpcodes = compute_ward_overload_wpcodes(
    _dapi_verify_counts, rigasa_ward_pcode=_rigasa_wp_pulse
)
try:
    _student_pulse_snap = live_student_pulse_snapshot(
        verification_ward_keys=len(_dapi_verify_counts),
        verification_event_total=sum(int(v) for v in _dapi_verify_counts.values()),
    )
except Exception:
    _student_pulse_snap = fallback_live_student_pulse_snapshot()
st.session_state.setdefault("dapi_verification_heatmap", True)
st.session_state.setdefault("dapi_traditional_role", "observer")

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

_oauth_hdr_pre = st.session_state.get("_dapi_oauth_blob")
_auth_html_pre = "Idle · handshake not run"
if isinstance(_oauth_hdr_pre, dict):
    if str(_oauth_hdr_pre.get("access_token") or "").strip():
        _auth_html_pre = (
            f"Authenticated · {html.escape(str(_oauth_hdr_pre.get('token_type') or 'Bearer'))} · armed"
        )
    elif str(_oauth_hdr_pre.get("error") or "").strip():
        _auth_html_pre = html.escape(str(_oauth_hdr_pre.get("error")))

st.markdown(
    """
<style>
/* KYSAH ribbon runway — never overlap the DAPI weld block below (forensic vertical separation) */
section.main .kysah-sovereign-ribbon {
  margin-bottom: 2rem !important;
}
/* DAPI column — isolated stack (1004337372: no summary/telemetry collision bleeding) */
section.main div[data-testid="stVerticalBlock"]:has(.kgec-dapi-ledger-stack-root) {
  display: flex !important;
  flex-direction: column !important;
  gap: 2.5rem !important;
  padding-top: 2rem !important;
  position: relative !important;
  isolation: isolate !important;
  contain: layout style !important;
  z-index: 3 !important;
  overflow: visible !important;
}
section.main .kgec-dapi-ledger-stack-root {
  display: block !important;
  height: 0 !important;
  margin: 0 !important;
  padding: 0 !important;
  overflow: hidden !important;
  pointer-events: none !important;
}
/* Expander summary — DAPI-only scope (no global expander collision / GWALO bleed) */
section.main div[data-testid="stVerticalBlock"]:has(.kgec-dapi-ledger-stack-root) section[data-testid="stExpander"] {
  margin-bottom: 2rem !important;
  position: relative !important;
  z-index: 4 !important;
}
section.main div[data-testid="stVerticalBlock"]:has(.kgec-dapi-ledger-stack-root) [data-testid="stExpander"] details > summary,
section.main div[data-testid="stVerticalBlock"]:has(.kgec-dapi-ledger-stack-root) [data-testid="stExpander"] summary,
section.main div[data-testid="stVerticalBlock"]:has(.kgec-dapi-ledger-stack-root) [data-testid="stExpander"] button[data-testid="baseButton-header"],
section.main div[data-testid="stVerticalBlock"]:has(.kgec-dapi-ledger-stack-root) [data-testid="stExpander"] div[data-testid="stExpanderDetails"] summary {
  display: flex !important;
  flex-direction: column !important;
  align-items: flex-start !important;
  justify-content: flex-start !important;
  gap: 1rem !important;
  padding-top: 1.35rem !important;
  padding-bottom: 1.1rem !important;
  padding-left: 0.35rem !important;
  padding-right: 0.35rem !important;
  margin-bottom: 1rem !important;
  min-height: unset !important;
  line-height: 1.5 !important;
  white-space: normal !important;
  font-family: 'Goldman', 'Georgia', serif !important;
  letter-spacing: 0.03em !important;
  text-rendering: geometricPrecision !important;
  -webkit-font-smoothing: antialiased !important;
  -moz-osx-font-smoothing: grayscale !important;
}
section.main div[data-testid="stVerticalBlock"]:has(.kgec-dapi-ledger-stack-root) [data-testid="stExpander"] summary *,
section.main div[data-testid="stVerticalBlock"]:has(.kgec-dapi-ledger-stack-root) [data-testid="stExpander"] button[data-testid="baseButton-header"] * {
  position: relative !important;
}
/* Inner ledger — sovereign air below Goldman summary chevron row */
section.main div[data-testid="stVerticalBlock"]:has(.kgec-dapi-ledger-stack-root) [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
  padding-top: 1.55rem !important;
  padding-bottom: 0.65rem !important;
  margin-top: 0.35rem !important;
}
section.main div[data-testid="stVerticalBlock"]:has(.kgec-dapi-ledger-stack-root) .kgec-dapi-form-decreed-title {
  margin-top: 1.15rem !important;
  margin-bottom: 0.9rem !important;
  font-family: 'Goldman', Georgia, serif !important;
  font-weight: 700 !important;
  font-size: clamp(12px, 2.65vw, 14px) !important;
  letter-spacing: 0.06em !important;
  color: rgba(240, 244, 255, 0.96) !important;
  line-height: 1.45 !important;
  text-rendering: geometricPrecision !important;
  -webkit-font-smoothing: antialiased !important;
}
section.main .kgec-traditional-human-api-cap {
  font-family: 'Goldman', Georgia, serif !important;
  font-weight: 700 !important;
  font-size: clamp(11px, 2.5vw, 13px) !important;
  letter-spacing: 0.08em !important;
  color: #ffdf66 !important;
  margin: 0 0 8px 0 !important;
}
/* Digital palace — Traditional Portrait warmth (D6 · not a cold database row) */
section.main div[data-testid="stVerticalBlock"]:has(.kgec-traditional-portrait-soul) {
  background: linear-gradient(
    168deg,
    rgba(52, 22, 18, 0.42) 0%,
    rgba(8, 14, 36, 0.78) 48%,
    rgba(6, 28, 42, 0.72) 100%
  ) !important;
  border: 1px solid rgba(212, 175, 55, 0.48) !important;
  border-radius: 14px !important;
  padding: 14px 14px 10px 14px !important;
  margin-bottom: 12px !important;
  box-shadow:
    inset 0 1px 0 rgba(255, 236, 210, 0.14),
    0 6px 22px rgba(0, 0, 0, 0.35) !important;
}
section.main .kgec-traditional-portrait-soul {
  display: none !important;
}
section.main .kgec-digital-palace-subline {
  font-family: 'Cormorant Garamond', Georgia, serif !important;
  font-weight: 500 !important;
  font-style: italic !important;
  font-size: clamp(13px, 3.1vw, 17px) !important;
  line-height: 1.45 !important;
  color: rgba(255, 248, 238, 0.9) !important;
  margin: 0 0 14px 0 !important;
  letter-spacing: 0.02em !important;
}
section.main .kgec-kaduna-palace-chamber {
  padding: 12px 14px 10px 14px !important;
  border-radius: 14px !important;
  border: 1px solid rgba(212, 175, 55, 0.42) !important;
  background: linear-gradient(
    152deg,
    rgba(38, 20, 14, 0.5) 0%,
    rgba(0, 16, 48, 0.75) 55%,
    rgba(4, 32, 40, 0.68) 100%
  ) !important;
  box-shadow:
    inset 0 1px 0 rgba(255, 230, 190, 0.1),
    0 8px 26px rgba(0, 0, 0, 0.38) !important;
  margin-bottom: 14px !important;
}
section.main .kgec-kaduna-palace-chamber .kgec-kaduna-pilot-cap {
  margin-bottom: 6px !important;
}
section.main .kgec-parent-trust-strip {
  font-family: 'Cormorant Garamond', Georgia, serif !important;
  font-size: clamp(12px, 2.85vw, 15px) !important;
  color: rgba(230, 248, 255, 0.92) !important;
  margin: 0 0 12px 0 !important;
  line-height: 1.5 !important;
}
section.main .kgec-cert-digest-steel {
  font-family: 'Cormorant Garamond', Georgia, serif !important;
  font-size: clamp(12px, 2.75vw, 15px) !important;
  color: rgba(220, 245, 255, 0.9) !important;
  margin: 8px 0 0 0 !important;
}
section.main .kgec-cert-digest-steel code {
  color: #7fe8ff !important;
  font-size: 0.95em !important;
}
section.main .kgec-locked-steel-pill {
  display: inline-block !important;
  padding: 1px 8px 2px 8px !important;
  border-radius: 999px !important;
  border: 1px solid rgba(212, 175, 55, 0.45) !important;
  background: rgba(0, 24, 48, 0.55) !important;
  font-family: 'Goldman', Georgia, serif !important;
  font-size: 0.82em !important;
  letter-spacing: 0.06em !important;
}
/* ZD01 success simulation — contained prose (1004337372 · no collision with Zazzau-31 scroll) */
section.main .kgec-zd01-success-demo {
  padding: 4px 2px 2px 2px !important;
  max-width: 100% !important;
}
section.main .kgec-zd01-success-kicker {
  font-family: 'Goldman', sans-serif !important;
  font-size: clamp(10px, 2.2vw, 11px) !important;
  letter-spacing: 0.14em !important;
  text-transform: uppercase !important;
  color: #ffdf66 !important;
  margin: 0 0 6px 0 !important;
}
section.main .kgec-zd01-success-lede {
  font-family: 'Cormorant Garamond', Georgia, serif !important;
  font-size: clamp(14px, 3.2vw, 18px) !important;
  font-style: italic !important;
  color: rgba(255, 245, 230, 0.92) !important;
  margin: 0 0 12px 0 !important;
  line-height: 1.4 !important;
}
section.main .kgec-zd01-success-demo ol {
  margin: 0 !important;
  padding-left: 1.2rem !important;
  color: rgba(230, 244, 255, 0.9) !important;
}
section.main .kgec-zd01-success-step-title {
  font-family: 'Goldman', Georgia, serif !important;
  font-weight: 700 !important;
  font-size: clamp(11px, 2.4vw, 13px) !important;
  letter-spacing: 0.05em !important;
  color: #d4af37 !important;
  margin: 10px 0 4px 0 !important;
}
section.main .kgec-zd01-success-step-body {
  font-family: 'Cormorant Garamond', Georgia, serif !important;
  font-size: clamp(13px, 2.9vw, 16px) !important;
  line-height: 1.48 !important;
  margin: 0 0 6px 0 !important;
  color: rgba(235, 248, 255, 0.88) !important;
}
section.main .kgec-zd01-success-foot {
  font-family: 'Goldman', Georgia, serif !important;
  font-size: clamp(9px, 2vw, 10px) !important;
  letter-spacing: 0.06em !important;
  color: rgba(0, 229, 255, 0.75) !important;
  margin: 14px 0 0 0 !important;
  line-height: 1.4 !important;
}
section.main .kgec-sovereign-clearance-banner {
  font-family: 'Goldman', Georgia, serif !important;
  font-weight: 700 !important;
  font-size: clamp(11px, 2.45vw, 13px) !important;
  letter-spacing: 0.05em !important;
  color: #0a1432 !important;
  background: linear-gradient(90deg, #bf953f 0%, #ffdf66 48%, #bf953f 100%) !important;
  border: 1px solid rgba(212, 175, 55, 0.85) !important;
  border-radius: 10px !important;
  padding: 12px 14px !important;
  margin: 10px 0 14px 0 !important;
  box-shadow: 0 2px 14px rgba(0, 0, 0, 0.35) !important;
}
section.main .kgec-sovereign-clearance-banner--compact {
  padding: 9px 12px !important;
  margin: 6px 0 12px 0 !important;
  font-size: clamp(10px, 2.2vw, 12px) !important;
}
section.main .kgec-stranger-vetting-alert {
  font-family: 'Goldman', Georgia, serif !important;
  font-weight: 700 !important;
  font-size: clamp(11px, 2.35vw, 13px) !important;
  letter-spacing: 0.04em !important;
  color: #fffef8 !important;
  background: rgba(180, 60, 30, 0.92) !important;
  border: 1px solid rgba(255, 223, 102, 0.65) !important;
  border-radius: 10px !important;
  padding: 11px 13px !important;
  margin: 10px 0 12px 0 !important;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.38) !important;
}
section.main .kgec-eagle-voice-pulse-rail {
  display: block !important;
  margin-top: 18px !important;
  padding-top: 6px !important;
  box-sizing: border-box !important;
  border-top: 1px solid rgba(212, 175, 55, 0.22) !important;
}
section.main .kgec-live-student-pulse-strip {
  display: flex !important;
  flex-wrap: wrap !important;
  align-items: center !important;
  gap: 8px 14px !important;
  margin: 22px 0 22px 0 !important;
  padding: 8px 12px !important;
  border-radius: 10px !important;
  border: 1px solid rgba(212, 175, 55, 0.38) !important;
  background: rgba(0, 8, 32, 0.62) !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
}
section.main .kgec-live-pulse-label {
  font-family: 'Goldman', sans-serif !important;
  font-weight: 700 !important;
  font-size: clamp(10px, 2.2vw, 11px) !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  color: #ffdf66 !important;
}
section.main .kgec-live-pulse-cycle {
  font-family: 'Goldman', Georgia, serif !important;
  font-size: clamp(10px, 2.1vw, 11px) !important;
  color: rgba(0, 229, 255, 0.9) !important;
  letter-spacing: 0.06em !important;
}
section.main .kgec-live-pulse-metric {
  font-family: 'Cormorant Garamond', Georgia, serif !important;
  font-size: clamp(12px, 2.75vw, 15px) !important;
  color: rgba(240, 248, 255, 0.92) !important;
}
section.main .kgec-sovereign-air-96 {
  display: block !important;
  width: 100% !important;
  min-height: 96px !important;
  height: 96px !important;
  margin: 0 !important;
  padding: 0 !important;
  pointer-events: none !important;
}
section.main .kgec-inst-ownership-fed {
  font-family: 'Goldman', sans-serif !important;
  font-weight: 700 !important;
  font-size: clamp(10px, 2.2vw, 11px) !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  color: #7fd4b8 !important;
  margin: 0 0 8px 0 !important;
}
section.main .kgec-inst-ownership-sta {
  font-family: 'Goldman', sans-serif !important;
  font-weight: 700 !important;
  font-size: clamp(10px, 2.2vw, 11px) !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  color: #ffdf66 !important;
  margin: 0 0 8px 0 !important;
}
section.main .kgec-nuba-heritage-head {
  font-family: 'Goldman', Georgia, serif !important;
  font-weight: 700 !important;
  font-size: clamp(13px, 3vw, 16px) !important;
  letter-spacing: 0.04em !important;
  color: #ffdf66 !important;
  margin: 6px 0 4px 0 !important;
}
section.main .kgec-nuba-abbr {
  color: rgba(0, 229, 255, 0.92) !important;
  font-weight: 700 !important;
}
section.main .kgec-nuba-sub {
  font-family: 'Cormorant Garamond', Georgia, serif !important;
  font-size: clamp(12px, 2.7vw, 14px) !important;
  color: rgba(235, 245, 255, 0.88) !important;
  margin: 0 0 10px 0 !important;
}
section.main .kgec-nuba-campus-card {
  border: 1px solid rgba(212, 175, 55, 0.35) !important;
  border-radius: 10px !important;
  padding: 10px 12px !important;
  margin: 0 0 12px 0 !important;
  background: rgba(0, 12, 40, 0.45) !important;
}
section.main .kgec-nuba-campus-title {
  font-family: 'Goldman', Georgia, serif !important;
  font-weight: 700 !important;
  font-size: clamp(11px, 2.5vw, 13px) !important;
  color: #d4af37 !important;
  margin: 0 0 6px 0 !important;
}
section.main .kgec-nuba-pulse-note {
  font-size: clamp(11px, 2.45vw, 13px) !important;
  color: rgba(220, 245, 255, 0.9) !important;
  margin: 8px 0 0 0 !important;
  line-height: 1.45 !important;
}
section.main .kgec-ancestral-command-row {
  border-left: 3px solid #bf953f !important;
  padding: 8px 10px 8px 12px !important;
  margin: 0 0 10px 0 !important;
  background: rgba(191, 149, 63, 0.07) !important;
  border-radius: 0 8px 8px 0 !important;
}
section.main .kgec-modern-statutory-card {
  border-left: 3px solid #00e5ff !important;
  padding: 8px 10px 8px 12px !important;
  margin: 0 0 10px 0 !important;
  background: rgba(0, 229, 255, 0.06) !important;
  border-radius: 0 8px 8px 0 !important;
  font-family: system-ui, 'Segoe UI', sans-serif !important;
}
section.main .kgec-modern-statutory-cap {
  font-size: clamp(9px, 2vw, 10px) !important;
  font-weight: 800 !important;
  letter-spacing: 0.14em !important;
  text-transform: uppercase !important;
  color: #7fd4b8 !important;
  margin-bottom: 6px !important;
}
/* Session telemetry isolated from ledger form — outer stack (no overlap with expander summary) */
section.main .kgec-dapi-session-stack {
  display: flex !important;
  flex-direction: column !important;
  gap: 0 !important;
  margin-top: 3rem !important;
  margin-bottom: 0 !important;
  padding-top: 0 !important;
  scroll-margin-top: 1.25rem !important;
  position: relative !important;
  z-index: 5 !important;
  isolation: isolate !important;
}
section.main .kgec-dapi-pre-session-airgap {
  display: block !important;
  height: 2rem !important;
  min-height: 2rem !important;
  width: 100% !important;
  clear: both !important;
  pointer-events: none !important;
  flex-shrink: 0 !important;
}
section.main .kgec-dapi-map-strip {
  display: flex !important;
  flex-wrap: wrap !important;
  gap: 10px !important;
  align-items: center !important;
  position: relative !important;
  z-index: 2 !important;
  isolation: isolate !important;
  contain: layout style paint !important;
  margin-top: 0 !important;
  margin-bottom: 12px !important;
  padding: 15px 14px !important;
  box-sizing: border-box !important;
  font-family: 'Goldman', sans-serif !important;
  font-size: clamp(10px, 2.4vw, 12px) !important;
  font-weight: 700 !important;
  color: #00e5ff !important;
  background: rgba(0, 0, 128, 0.94) !important;
  background-clip: padding-box !important;
  border: 1px solid rgba(212, 175, 55, 0.55) !important;
  border-radius: 10px !important;
  box-shadow: 0 3px 14px rgba(0, 0, 0, 0.42) !important;
}
section.main .kgec-dapi-map-strip .kgec-dapi-pill {
  position: relative !important;
  z-index: 3 !important;
  display: inline-flex !important;
  align-items: center !important;
  line-height: 1.35 !important;
  max-width: 100% !important;
}
section.main .kgec-dapi-map-strip code {
  color: #f0f4ff !important;
  font-size: 0.95em !important;
  background: rgba(0, 0, 40, 0.62) !important;
  padding: 3px 7px !important;
  border-radius: 5px !important;
  border: 1px solid rgba(0, 229, 255, 0.28) !important;
}
section.main .kgec-dapi-auth {
  color: #f0f4ff !important;
}
/* 1004337372.jpg — crystalline Goldman + final sovereign airway (ledger ↔ session strip) */
section.main .kgec-dapi-ledger-air-50 {
  display: block !important;
  height: 0 !important;
  margin-bottom: 96px !important;
  margin-top: 0 !important;
  padding: 0 !important;
  clear: both !important;
  pointer-events: none !important;
}
section.main .kgec-dapi-sovereign-air-crystal {
  display: block !important;
  width: 100% !important;
  min-height: 72px !important;
  height: 72px !important;
  margin: 0 !important;
  padding: 0 !important;
  clear: both !important;
  pointer-events: none !important;
  flex-shrink: 0 !important;
}
section.main .kgec-dapi-pilot-column {
  width: 100% !important;
}
/* Rigasa + NUBA pressure copy — single stack (1004337372 · no caption overlap vs sovereign air) */
section.main div[data-testid="stVerticalBlock"]:has(.kgec-dapi-ledger-stack-root) .kgec-dapi-kaduna-caption-stack {
  display: block !important;
  max-width: 100% !important;
  box-sizing: border-box !important;
  margin-top: 4px !important;
  margin-bottom: 14px !important;
  padding-right: 2px !important;
}
section.main div[data-testid="stVerticalBlock"]:has(.kgec-dapi-ledger-stack-root) .kgec-dapi-kaduna-caption-stack .kgec-dapi-cap-line {
  margin: 0 0 10px 0 !important;
  line-height: 1.5 !important;
  font-size: 0.82rem !important;
  color: rgba(240, 244, 255, 0.86) !important;
  word-wrap: break-word !important;
  overflow-wrap: anywhere !important;
}
section.main div[data-testid="stVerticalBlock"]:has(.kgec-dapi-ledger-stack-root) .kgec-dapi-kaduna-caption-stack .kgec-dapi-cap-nuba {
  margin-bottom: 0 !important;
  color: rgba(224, 242, 254, 0.92) !important;
}
section.main .kgec-kaduna-pilot-cap {
  font-family: 'Goldman', sans-serif !important;
  font-weight: 700 !important;
  font-size: clamp(12px, 2.8vw, 14px) !important;
  color: #00e5ff !important;
  margin: 0 0 12px 0 !important;
  letter-spacing: 0.05em !important;
}
section.main .kgec-kaduna-twin-portrait {
  margin-top: 14px !important;
  margin-bottom: 8px !important;
  isolation: isolate !important;
  contain: layout style !important;
}
/* NCAT / sovereign aviation node — Hanwa ZD02 lattice lock */
section.main .kgec-sovereign-inst-node {
  border-left: 3px solid #bf953f !important;
  padding: 10px 12px 10px 14px !important;
  margin: 0 0 14px 0 !important;
  background: rgba(191, 149, 63, 0.12) !important;
  border-radius: 0 10px 10px 0 !important;
  box-sizing: border-box !important;
}
section.main .kgec-sovereign-inst-node .kgec-sovereign-asset-cap {
  font-family: 'Goldman', sans-serif !important;
  font-size: clamp(10px, 2.2vw, 11px) !important;
  font-weight: 700 !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  color: #ffdf66 !important;
  margin: 0 0 6px 0 !important;
}
/* Zazzau 31 — vertical scroll cascade (red-circle protocol · no collision with ledger) */
section.main .kgec-zazzau-31-scroll {
  max-height: min(42vh, 480px) !important;
  overflow-y: auto !important;
  overflow-x: hidden !important;
  -webkit-overflow-scrolling: touch !important;
  padding: 12px 14px !important;
  margin-top: 18px !important;
  margin-bottom: 16px !important;
  border: 1px solid rgba(212, 175, 55, 0.42) !important;
  border-radius: 10px !important;
  background: rgba(0, 6, 40, 0.55) !important;
  box-sizing: border-box !important;
}
section.main .kgec-zazzau-31-scroll ol.kgec-zazzau-31-ol {
  margin: 0 !important;
  padding-left: 1.35rem !important;
  font-family: 'Goldman', Georgia, serif !important;
  font-size: clamp(10px, 2.15vw, 12px) !important;
  font-weight: 600 !important;
  line-height: 1.55 !important;
  color: rgba(240, 244, 255, 0.94) !important;
}
section.main .kgec-zazzau-31-scroll li {
  margin-bottom: 0.35rem !important;
}
section.main .kgec-zazzau-31-scroll code {
  color: #00e5ff !important;
  font-size: 0.92em !important;
}
</style>
""",
    unsafe_allow_html=True,
)

_pc_dapi = st.columns((1,))
with _pc_dapi[0]:
    with st.container():
        st.markdown(
            '<div class="kgec-dapi-ledger-stack-root" aria-hidden="true"></div>',
            unsafe_allow_html=True,
        )
        with st.expander("DAPI weld · verification ledger", expanded=False):
            st.toggle(
                "Ward verification heatmap (cyan = verified · deep matter = cold)",
                key="dapi_verification_heatmap",
                help="Choropleth on 8,806 ward polygons — density from local SQLite event store.",
            )
            _c1, _c2 = st.columns(2)
            with _c1:
                st.selectbox(
                    "Traditional principal role",
                    options=["observer", "me_anguwa", "village_head", "district_head"],
                    key="dapi_traditional_role",
                    help="When Me Anguwa or Village Head is active, jurisdiction counts use the DAPI event store.",
                )
                st.text_input(
                    "Principal ID (DAPI subject / node id)",
                    key="dapi_principal_id",
                    placeholder="e.g. MEANGUWA-KD-RIGASA-01",
                )
            with _c2:
                if st.button(
                    "DAPI OAuth2 handshake",
                    key="dapi_oauth_handshake",
                    help="client_credentials via DAPI_TOKEN_URL",
                ):
                    _blob = fetch_oauth_token()
                    st.session_state["_dapi_oauth_blob"] = _blob
                    _err = str(_blob.get("error") or "").strip()
                    _tok = str(_blob.get("access_token") or "").strip()
                    if _tok:
                        st.success("Access token acquired — DAPI session armed.")
                    elif _err:
                        st.warning(_err)
                    else:
                        st.info("No token returned — check environment variables.")
            _oauth = st.session_state.get("_dapi_oauth_blob")
            if isinstance(_oauth, dict) and str(_oauth.get("access_token") or "").strip():
                st.caption(
                    f"Token · {str(_oauth.get('token_type') or 'Bearer')} · "
                    f"expires epoch {_oauth.get('expires_at', 0):.0f}"
                )
            _tr_dapi_kd = ""
            if st.session_state.get("total_reality_last"):
                _tr_dapi_kd = str(st.session_state["total_reality_last"].get("state") or "").strip()
            if _tr_dapi_kd and is_kaduna_state(_tr_dapi_kd):
                _fz_list = ", ".join(sorted(KADUNA_SPT_FRONTIER_LGA_EN))
                st.caption(
                    f"Security Proximity Tag (SPT) — frontier belt: {_fz_list}. "
                    "Verification on those LGAs with a ward/ZD weld breach alerts the District Head "
                    "node under the 24-hour criminal-trace protocol."
                )
                if not _dapi_wards_fc_gate:
                    st.caption(
                        "HDX spine not mounted — lattice gate offline; reconnect for production "
                        "Sovereign Clearance + SPT steel."
                    )
                _kd_press = kaduna_me_anguwa_pressure_summary(
                    _dapi_verify_counts, rigasa_ward_pcode=_rigasa_wp_pulse
                )
                _nuba_line = nuba_campus_inference_text()
                _kd_copy = html.escape(str(_kd_press.get("copy_line") or ""))
                _nuba_esc = html.escape(_nuba_line) if _nuba_line else ""
                _cap_parts = [f'<p class="kgec-dapi-cap-line">{_kd_copy}</p>']
                if _nuba_esc:
                    _cap_parts.append(f'<p class="kgec-dapi-cap-line kgec-dapi-cap-nuba">{_nuba_esc}</p>')
                st.markdown(
                    '<div class="kgec-dapi-kaduna-caption-stack">'
                    + "".join(_cap_parts)
                    + "</div>",
                    unsafe_allow_html=True,
                )
            _registry_inst_opt = (
                "— Select institution —",
                "Ahmadu Bello University (ABU · Samaru)",
                "Kaduna State University (KASU · Kaduna North)",
                "Kaduna Polytechnic [FED] · Kaduna South",
                "Nuhu Bamalli Polytechnic (NUBA [STA] · Main · Zaria)",
                "Nuhu Bamalli Polytechnic (NUBA [STA] · Kafanchan · Jema'a)",
                "Other lattice enrollee",
            )
            _registry_res_opt = (
                "— Residence district node —",
                "Rigasa · ZD22 · Igabi",
                "Doka · ZD26 · Kaduna North",
                "Samaru belt · ZD09 · Sabon Gari",
                "Shika · ZD07 · Sabon Gari",
                "Hanwa · ZD02 · Zaria",
            )
            st.markdown(
                '<p class="kgec-traditional-human-api-cap">Registry of Strangers · digital vetting line</p>',
                unsafe_allow_html=True,
            )
            st.caption(
                "Every stranger once reported their mission at the ward gate; DAPI OAuth + this ledger "
                "bind ABU, KASU, Kaduna Polytechnic [FED], and Nuhu Bamalli Polytechnic (NUBA) [STA] "
                "to residential district nodes (Rigasa, Doka, Samaru belt)."
            )
            st.selectbox(
                "Student intake institution (pilot)",
                options=list(_registry_inst_opt),
                key="dapi_registry_institution",
                help=(
                    "Lattice enrollee — binds sovereign clearance to ABU, KASU, Kaduna Polytechnic [FED], "
                    "or Nuhu Bamalli Polytechnic (NUBA) [STA] campus choice."
                ),
            )
            st.selectbox(
                "Residential district node (Me Anguwa jurisdiction anchor)",
                options=list(_registry_res_opt),
                key="dapi_registry_residence",
                help="Must reconcile with Zazzau district + ward_pcode on submit.",
            )
            st.markdown(
                '<p class="kgec-traditional-human-api-cap">Haraji ledger simulation · Community Development Contribution</p>',
                unsafe_allow_html=True,
            )
            st.caption(
                "Indirect Rule steel — historical haraji sat at the ward gate with vetting efficiency; "
                "this CDC tracker binds DAPI principals to the same accountability rhythm "
                "(₦ lines are audit artefacts, not legal tax assessment)."
            )
            with st.form("dapi_haraji_cdc"):
                _hz_labels = ["— Zazzau district —"] + [
                    f"{d['district_id']} · {d['district_en']}" for d in ZAZZAU_THIRTY_ONE_DISTRICTS
                ]
                st.selectbox("ZD anchor (optional)", options=_hz_labels, key="dapi_haraji_zd")
                st.text_input(
                    "ward_pcode (ADM3 spine)",
                    key="dapi_haraji_ward",
                    placeholder="same lattice as verification",
                )
                st.number_input(
                    "Amount (₦)",
                    min_value=0.0,
                    step=500.0,
                    key="dapi_haraji_amount",
                )
                st.selectbox(
                    "Levy class",
                    options=(
                        "Haraji-class levy (pilot)",
                        "Community Development Contribution",
                        "Special ward assessment",
                    ),
                    key="dapi_haraji_class",
                )
                st.text_input("Narrative (optional)", key="dapi_haraji_note")
                if st.form_submit_button("Post CDC line to Haraji ledger"):
                    _hpid = str(st.session_state.get("dapi_principal_id") or "").strip()
                    _hz = str(st.session_state.get("dapi_haraji_zd") or "").strip()
                    _hz_id = ""
                    if _hz and not _hz.startswith("—"):
                        _hz_id = _hz.split(" · ")[0].strip()
                    _hw = str(st.session_state.get("dapi_haraji_ward") or "").strip()
                    _ha = float(st.session_state.get("dapi_haraji_amount") or 0.0)
                    _hc = str(st.session_state.get("dapi_haraji_class") or "").strip()
                    _hn = str(st.session_state.get("dapi_haraji_note") or "").strip()
                    if not _hpid:
                        st.warning("Set Principal ID above — CDC lines bind to the Human API node.")
                    elif not _hw:
                        st.warning("ward_pcode required — lattice weld.")
                    else:
                        _hok, _hmsg = record_haraji_cdc_line(
                            principal_id=_hpid,
                            ward_pcode=_hw,
                            zazzau_district_id=_hz_id or None,
                            naira_amount=_ha,
                            levy_class=_hc,
                            narrative=_hn,
                        )
                        if _hok:
                            st.success(_hmsg)
                        else:
                            st.error(_hmsg)
            with st.form("dapi_record_verification", clear_on_submit=True):
                st.markdown(
                    '<p class="kgec-dapi-form-decreed-title">'
                    "<strong>Record verification (ghost-proof <code>UNIQUE(student_uid)</code>)</strong>"
                    "</p>",
                    unsafe_allow_html=True,
                )
                _priv_sha = html.escape(DAPI_PARENT_FACING_PRIVACY["sha256_digest"])
                _priv_enc = html.escape(DAPI_PARENT_FACING_PRIVACY["encryption_steel"])
                st.markdown(
                    '<p class="kgec-parent-trust-strip">For parents and palace stewards · hover each cue: '
                    f'<span class="kgec-mophi-glass-tip" title="{_priv_sha}">What is the SHA-256 seal?</span>'
                    " · "
                    f'<span class="kgec-mophi-glass-tip kgec-locked-steel-pill" title="{_priv_enc}">'
                    "Locked in Steel</span></p>",
                    unsafe_allow_html=True,
                )
                _zd_labels = ["— Select Zazzau district (ZD) —"] + [
                    f"{d['district_id']} · {d['district_en']} · {d['parent_lga_en']}"
                    for d in ZAZZAU_THIRTY_ONE_DISTRICTS
                ]
                st.selectbox(
                    "Zazzau district node (required for Me Anguwa / Village Head / District Head)",
                    options=_zd_labels,
                    key="dapi_form_zazzau_district",
                    help="Kaduna pilot — every traditional verification binds ward spine + ZD** ancestral ledger.",
                )
                _rsu = st.text_input(
                    "student_uid",
                    key="dapi_form_student",
                    help=(
                        "Unique child / enrollee key on this pilot ledger. "
                        "Parents: your child’s row is sealed with cryptography—see SHA-256 + Locked in Steel cues above."
                    ),
                )
                _rwp = st.text_input("ward_pcode (ADM3_PCODE from spine)", key="dapi_form_ward")
                _rpu = st.text_input("pu_code (optional)", key="dapi_form_pu")
                st.text_input(
                    "NIN (optional — stranger registry)",
                    key="dapi_form_nin",
                    placeholder="11-digit reference",
                )
                st.caption(
                    f"Stranger vetting — compare NIN / claimed address (WGS84) to Zazzau district anchor; "
                    f"threshold {STRANGER_VETTING_DISTANCE_KM:.0f} km."
                )
                _cla, _clb = st.columns(2)
                with _cla:
                    st.text_input(
                        "Claim latitude (optional)",
                        key="dapi_form_claim_lat",
                        placeholder="e.g. 11.095",
                    )
                with _clb:
                    st.text_input(
                        "Claim longitude (optional)",
                        key="dapi_form_claim_lon",
                        placeholder="e.g. 7.710",
                    )
                _sub = st.form_submit_button("Commit sovereign certificate")
                if _sub:
                    _pid = str(st.session_state.get("dapi_principal_id") or "").strip()
                    _role = str(st.session_state.get("dapi_traditional_role") or "observer").strip()
                    _zd_pick = str(st.session_state.get("dapi_form_zazzau_district") or "").strip()
                    _zd_id = ""
                    if _zd_pick and not _zd_pick.startswith("—"):
                        _zd_id = _zd_pick.split(" · ")[0].strip()
                    if _role in TRADITIONAL_PRINCIPAL_ROLES and not _zd_id:
                        st.error(
                            "Traditional principal weld blocked — select a Zazzau district node (ZD01–ZD31)."
                        )
                    else:
                        _clat = None
                        _clon = None
                        _lt = str(st.session_state.get("dapi_form_claim_lat") or "").strip()
                        _ln = str(st.session_state.get("dapi_form_claim_lon") or "").strip()
                        if _lt:
                            try:
                                _clat = float(_lt)
                            except ValueError:
                                _clat = None
                        if _ln:
                            try:
                                _clon = float(_ln)
                            except ValueError:
                                _clon = None
                        _nin_f = str(st.session_state.get("dapi_form_nin") or "").strip()
                        _ok, _msg, _meta = record_verification(
                            student_uid=_rsu,
                            ward_pcode=_rwp,
                            principal_id=_pid or "UNASSIGNED",
                            traditional_role=_role,
                            pu_code=_rpu or None,
                            zazzau_district_id=_zd_id or None,
                            wards_fc=_dapi_wards_fc_gate,
                            nin=_nin_f or None,
                            claimant_lat=_clat,
                            claimant_lon=_clon,
                        )
                        if _ok:
                            st.success(_msg)
                            if _meta.get("vetting_required_alert"):
                                _vn = str(_meta.get("vetting_note") or "").strip()
                                if _vn:
                                    st.markdown(
                                        '<div class="kgec-stranger-vetting-alert" role="alert">'
                                        f"{html.escape(_vn)}"
                                        "</div>",
                                        unsafe_allow_html=True,
                                    )
                            if _meta.get("sovereign_clearance"):
                                _cm = str(_meta.get("clearance_message") or "").strip()
                                if _cm:
                                    st.markdown(
                                        '<div class="kgec-sovereign-clearance-banner" role="status">'
                                        f"{html.escape(_cm)}"
                                        "</div>",
                                        unsafe_allow_html=True,
                                    )
                            _ri = str(
                                st.session_state.get("dapi_registry_institution") or ""
                            ).strip()
                            _rr = str(
                                st.session_state.get("dapi_registry_residence") or ""
                            ).strip()
                            if _ri and not _ri.startswith("—"):
                                st.caption(
                                    f"Registry of Strangers line · `{html.escape(_ri)}` · "
                                    f"`{html.escape(_rr)}` — bound to this sovereign certificate."
                                )
                        else:
                            st.error(_msg)
            _pid_show = str(st.session_state.get("dapi_principal_id") or "").strip()
            _role_show = str(st.session_state.get("dapi_traditional_role") or "").strip()
            if _pid_show and _role_show in TRADITIONAL_PRINCIPAL_ROLES:
                _pj = principal_jurisdiction_stats(_pid_show)
                st.markdown(
                    '<div class="kgec-traditional-portrait-soul" aria-hidden="true"></div>'
                    '<p class="kgec-traditional-human-api-cap">Traditional Portrait · Human API</p>'
                    '<p class="kgec-digital-palace-subline">A chamber for trust and ancestral care—'
                    "titles and seals first; the database whispers behind the curtain.</p>",
                    unsafe_allow_html=True,
                )
                if _role_show == "me_anguwa":
                    _scs = str(_pj.get("sovereign_clearance_status") or "").strip()
                    if _scs:
                        st.markdown(
                            '<div class="kgec-sovereign-clearance-banner '
                            'kgec-sovereign-clearance-banner--compact" role="status">'
                            f"{html.escape(_scs)}"
                            "</div>",
                            unsafe_allow_html=True,
                        )
                _mx_a, _mx_b = st.columns(2)
                with _mx_a:
                    st.metric(
                        "Jurisdiction verifications (this principal)",
                        f"{int(_pj['verified_total']):,}",
                    )
                with _mx_b:
                    _har = float(_pj.get("haraji_cdc_total_naira") or 0.0)
                    st.metric(
                        "Haraji / CDC total (₦)",
                        f"₦{_har:,.2f}",
                        help="Community Development Contribution lines for this principal_id.",
                    )
                _br = _pj.get("by_role") or {}
                if _br:
                    st.caption(
                        "Attestations by role · "
                        + " · ".join(
                            f"{html.escape(str(k))}: {int(v):,}" for k, v in _br.items()
                        )
                    )
                if _pj.get("by_ward"):
                    st.dataframe(
                        [
                            {
                                "ward_pcode": k,
                                "verified": f"{int(v):,}",
                            }
                            for k, v in _pj["by_ward"].items()
                        ],
                        hide_index=True,
                        use_container_width=True,
                        column_config={
                            "ward_pcode": st.column_config.TextColumn("ward_pcode", width=140),
                            "verified": st.column_config.TextColumn("verified", width=100),
                        },
                    )
                if _pj.get("recent_digest"):
                    _rd = html.escape(str(_pj["recent_digest"]))
                    _tip_sha = html.escape(DAPI_PARENT_FACING_PRIVACY["sha256_digest"])
                    _tip_enc = html.escape(DAPI_PARENT_FACING_PRIVACY["encryption_steel"])
                    st.markdown(
                        '<p class="kgec-cert-digest-steel">Latest certificate fingerprint · '
                        f'<code class="kgec-mophi-glass-tip" title="{_tip_sha}">{_rd[:16]}…</code>'
                        ' · <span class="kgec-mophi-glass-tip kgec-locked-steel-pill" '
                        f'title="{_tip_enc}">Locked in Steel</span></p>',
                        unsafe_allow_html=True,
                    )
            if _tr_dapi_kd and is_kaduna_state(_tr_dapi_kd):
                with st.expander("Student ledger · Stranger Vetting Status (recent)", expanded=False):
                    _vrows = verification_ledger_recent(45)
                    if _vrows:
                        st.dataframe(_vrows, hide_index=True, use_container_width=True)
                    else:
                        st.caption("No verification rows yet.")
                with st.expander("Haraji / CDC ledger (recent lines)", expanded=False):
                    _hrows = haraji_cdc_recent_rows(35)
                    if _hrows:
                        st.dataframe(_hrows, hide_index=True, use_container_width=True)
                    else:
                        st.caption("No CDC lines posted.")

        _tr_state_name = ""
        if st.session_state.get("total_reality_last"):
            _tr_state_name = str(st.session_state["total_reality_last"].get("state") or "").strip()
        if _tr_state_name and is_kaduna_state(_tr_state_name):
            _board_rows = leaderboard_for_state_wards(
                _tr_state_name,
                wards_fc=_phase2.get("wards_fc") if _phase2 else None,
            )
            if _board_rows:
                with st.expander(f"Verification leaderboard · Kaduna (pilot)", expanded=False):
                    st.dataframe(
                        [
                            {
                                "ward_pcode": a,
                                "ward": b,
                                "lga": c,
                                "verified": f"{int(d):,}",
                            }
                            for a, b, c, d in _board_rows[:40]
                        ],
                        hide_index=True,
                        use_container_width=True,
                        column_config={
                            "ward_pcode": st.column_config.TextColumn("ward_pcode", width=130),
                            "ward": st.column_config.TextColumn("ward", width=160),
                            "lga": st.column_config.TextColumn("lga", width=120),
                            "verified": st.column_config.TextColumn("verified", width=100),
                        },
                    )

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="kgec-dapi-sovereign-air-crystal" aria-hidden="true"></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="kgec-dapi-ledger-air-50" aria-hidden="true"></div>',
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown(
            f"""
<div class="kgec-dapi-session-stack">
  <div class="kgec-dapi-map-strip" role="region" aria-label="DAPI session telemetry">
    <span class="kgec-dapi-pill">Session <code>{html.escape(_dapi_browser_session)}</code></span>
    <span class="kgec-dapi-pill kgec-dapi-auth">{_auth_html_pre}</span>
    <span class="kgec-dapi-pill">Ward events indexed · {len(_dapi_verify_counts):,} wards · max {max(_dapi_verify_counts.values()) if _dapi_verify_counts else 0}</span>
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

    _wards_fc_kd = _phase2.get("wards_fc") if _phase2 else None
    _kd_sel = ""
    if st.session_state.get("total_reality_last"):
        _kd_sel = str(st.session_state["total_reality_last"].get("state") or "").strip()
    if _kd_sel and is_kaduna_state(_kd_sel):
        st.markdown(
            '<div class="kgec-kaduna-twin-portrait kgec-kaduna-palace-chamber" role="region" '
            'aria-label="Kaduna digital palace twin portrait">'
            '<p class="kgec-kaduna-pilot-cap">Kaduna sovereign pilot · Twin Portrait</p>'
            '<p class="kgec-digital-palace-subline">Institutional steel meets ancestral command in one chamber—'
            "not a remote server farm.</p>"
            "</div>",
            unsafe_allow_html=True,
        )
        render_kaduna_map_twin_portrait()
        _rig_wp = find_ward_pcode_rigasa_igabi(_wards_fc_kd)
        if st.button(
            "Simulate DAPI · Me Anguwa Rigasa (Igabi) handshake",
            key="kaduna_rigasa_sim",
            help=(
                "Writes one verification on Rigasa-class ward · cyan pulse on heatmap · "
                "SHA-256 palace seal on the ledger row. Parents: treat this as a street-level rehearsal of Locked in Steel."
            ),
        ):
            if not _rig_wp:
                st.error("HDX ward spine missing — cannot resolve Rigasa ADM3_PCODE.")
            else:
                _su = f"SIM-KD-RIGASA-{int(_wall_time() * 1e9)}"
                _ok_sim, _msg_sim, _meta_sim = record_verification(
                    student_uid=_su,
                    ward_pcode=_rig_wp,
                    principal_id="MEANGUWA-KD-RIGASA-01",
                    traditional_role="me_anguwa",
                    pu_code=None,
                    zazzau_district_id=RIGASA_DISTRICT_ID,
                    wards_fc=_dapi_wards_fc_gate,
                )
                if _ok_sim:
                    st.success(f"{_msg_sim} · ward `{_rig_wp}` — heatmap updates on rerun.")
                    if _meta_sim.get("sovereign_clearance"):
                        _cms = str(_meta_sim.get("clearance_message") or "").strip()
                        if _cms:
                            st.markdown(
                                '<div class="kgec-sovereign-clearance-banner" role="status">'
                                f"{html.escape(_cms)}"
                                "</div>",
                                unsafe_allow_html=True,
                            )
                else:
                    st.warning(_msg_sim)
        if _rig_wp:
            st.caption(f"Rigasa spine target · ADM3_PCODE `{_rig_wp}` (Igabi) · ledger `{RIGASA_DISTRICT_ID}`")
        else:
            st.caption("Rigasa ward pcode unresolved — load HDX wards online.")

_dapi_heatmap = bool(st.session_state.get("dapi_verification_heatmap", True))

_federation_map = _build_federation_map(
    _states_geojson,
    _phase2,
    _asset_states,
    ward_verify_counts=_dapi_verify_counts,
    verification_heatmap=_dapi_heatmap,
    ward_overload_wpcodes=_dapi_overload_wpcodes,
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
    st.session_state["_sovereign_bridge_armed"] = False
    st.error(
        "Install streamlit-folium inside the project venv: "
        "`pip install streamlit-folium` — required for viewport atomic lattice."
    )
    st.components.v1.html(_federation_map._repr_html_(), height=520, scrolling=False)
elif _strike_mode:
    st.session_state["_sovereign_bridge_armed"] = False
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
    st.session_state["_sovereign_bridge_armed"] = True
    st.session_state["_sovereign_bridge_ctx"] = {
        "fused_df": _fused_df,
        "national_df": _national_df,
        "fin_points": _fin_pos_pts,
        "trade_nodes": _trade_nodes,
        "ngecc_reg": _ngecc_reg,
        "states_geojson": _states_geojson,
        "ncc_rows": _ncc_incidents,
        "signal_rows": _signal_ev,
        "ntw_proxy": _ntw_blob,
    }
    if getattr(st, "fragment", None):
        _sovereign_telegram_bridge_tick()
    elif (os.environ.get("TELEGRAM_BOT_TOKEN") or "").strip():
        try:
            from sovereign_bridge.telegram_apply import apply_pending_bridge_commands

            if apply_pending_bridge_commands(
                fused_df=_fused_df,
                national_pu_df=_national_df,
                fin_points=_fin_pos_pts,
                trade_nodes=_trade_nodes,
                ngecc_reg=_ngecc_reg,
                states_geojson=_states_geojson,
                ncc_rows=_ncc_incidents,
                signal_rows=_signal_ev,
                ntw_proxy=_ntw_blob,
            ):
                _tb = getattr(st, "toast", None)
                if callable(_tb):
                    _tb("Sovereign Bridge · Telegram order applied", icon="📡")
        except Exception:
            pass
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
        _tr_last = st.session_state.get("total_reality_last") or {}
        _tr_state = str(_tr_last.get("state") or "")
        if is_katsina_state(_tr_state):
            st.markdown(katsina_forensic_mophi_glass_html(), unsafe_allow_html=True)
        elif is_kano_state(_tr_state):
            st.markdown(kano_forensic_mophi_glass_html(), unsafe_allow_html=True)
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
_prism_scale_line = (
    f"Sovereign record · Scale 1 States + AZK · Scale 2 LGAs ≥ {ZOOM_LGA_EMERGE} wards ≥ {ZOOM_WARD_EMERGE} · "
    f"Scale 3 atomic ≥ {ZOOM_ATOM_EMERGE} · FPS HUD · pinch atomize · orientation resize armed"
)
_prism_scale_esc = html.escape(_prism_scale_line)
_detail_pre = html.escape(
    _detail_meta if _detail_meta else "Forensic spine loaded — map is the vigil — ignition stable."
)
_foot_mq1 = _kgec_marquee_pair(
    "SCUML Certificate · SC 151653884 · Copyright Registration LW15954 — compliance ticker",
    seconds=96.0,
)
_foot_mq2 = _kgec_marquee_pair(
    "© 2026 Galadiman Ruwa Center (GCSLC) LTD/GTE · Sovereign-by-Design · national instrument LIVE",
    seconds=112.0,
)

st.markdown(
    f"""
<div class="kgec-prism-terminal sovereign-detail-widget" role="region" aria-label="Prism terminal telemetry">
  <div class="kgec-prism-cap">Prism Terminal · 774 LGA geometry · portrait roll-up</div>
  <div class="kgec-prism-handshake">
    <p class="kgec-prism-mono">Goldman Ruwa Center for Strategic Leadership and Communication GCSLC LTD/GTE · Majestic K-GEC · Sovereign mirror</p>
    <p class="kgec-prism-mono">Galadiman Ruwa Nigeria Ltd RC 1871418 · Zaria GRA cadence · national lattice</p>
    <p class="kgec-prism-mono">8R Paradigm Convergence and Determinants — decode · understand · the nation never sleeps</p>
  </div>
  <div class="kgec-prism-stack">
    <div class="kgec-prism-tier kgec-prism-tier-gold">
      <span class="kgec-prism-tier-val">37</span>
      <span class="kgec-prism-tier-lbl">States + FCT · constitutional administrative lattice</span>
    </div>
    <div class="kgec-prism-tier kgec-prism-tier-cyan">
      <span class="kgec-prism-tier-val">774</span>
      <span class="kgec-prism-tier-lbl">LGAs · gcslc_deep_join national heartbeat</span>
    </div>
    <div class="kgec-prism-tier kgec-prism-tier-white">
      <span class="kgec-prism-tier-val">8,806</span>
      <span class="kgec-prism-tier-lbl">Wards · forensic ward tokens · pinch-to-reveal</span>
    </div>
    <div class="kgec-prism-tier kgec-prism-tier-red">
      <span class="kgec-prism-tier-val">176,846</span>
      <span class="kgec-prism-tier-lbl">Polling units · INEC atomic lattice · scale-3 sovereign</span>
    </div>
  </div>
  <div class="kgec-prism-record">
    <div class="kgec-prism-record-h">Sovereign record</div>
    <p class="kgec-prism-mono kgec-prism-record-lead">{_prism_scale_esc}</p>
    <pre class="kgec-prism-pre">{_detail_pre}</pre>
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
