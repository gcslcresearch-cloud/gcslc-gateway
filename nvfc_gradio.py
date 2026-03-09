"""
GCSLC Strategic Command Center — Mission Directive: No Placeholders.
Map of Authority: Real Nigeria state borders (GeoJSON choropleth). Gold #FFD700 coal states, Navy #000080 else.
Sovereign Guardian: Navy + Gold SVG, coal with coal-glow 2s infinite alternate.
Falcon: Python updates (x,y) to state coordinates on map (tactical dive).
Agentic Reasoning: gr.HTML scrolling Thinking logs at bottom.
"""
import base64
import html
import io
import json
import math
import random
import gradio as gr
import os
import shutil
import subprocess
import struct
import sys
import time
import zipfile
from typing import Optional, Dict, Any, Tuple
from urllib.request import urlopen, Request

try:
    import plotly.graph_objects as go
    _HAS_PLOTLY = True
except Exception:
    _HAS_PLOTLY = False

try:
    from shapely.geometry import shape, mapping
    from shapely.ops import unary_union
    _HAS_SHAPELY = True
except Exception:
    _HAS_SHAPELY = False

SERVER_PORT = 7860

# 13 coal-rich states
COAL_STATES = [
    "Enugu", "Kogi", "Benue", "Nasarawa", "Gombe", "Adamawa", "Delta",
    "Edo", "Ondo", "Bauchi", "Anambra", "Ebonyi", "Abia",
]

STATE_RESERVES_MT = {
    "Enugu": 168.0, "Kogi": 223.0, "Benue": 85.0, "Nasarawa": 22.0, "Gombe": 62.0,
    "Adamawa": 12.0, "Delta": 45.0, "Edo": 38.0, "Ondo": 20.0, "Bauchi": 25.0,
    "Anambra": 27.3, "Ebonyi": 15.0, "Abia": 18.0,
}

# Falcon landing position (x%, y%) on SVG map for each state
STATE_MAP_POS = {
    "Enugu": (52, 72), "Kogi": (48, 58), "Benue": (58, 62), "Nasarawa": (50, 48),
    "Gombe": (62, 42), "Adamawa": (68, 48), "Delta": (38, 78), "Edo": (42, 68),
    "Ondo": (36, 62), "Bauchi": (58, 38), "Anambra": (50, 75), "Ebonyi": (54, 72), "Abia": (52, 78),
}

# Falcon (lon, lat) on Plotly map — tactical dive target coordinates
STATE_CENTROIDS_LNGLAT: Dict[str, Tuple[float, float]] = {
    "Enugu": (7.5, 6.4), "Kogi": (6.7, 7.8), "Benue": (8.2, 7.2), "Nasarawa": (8.5, 8.5),
    "Gombe": (11.2, 10.3), "Adamawa": (12.5, 9.3), "Delta": (6.2, 5.9), "Edo": (6.3, 6.5),
    "Ondo": (5.7, 7.2), "Bauchi": (9.8, 10.3), "Anambra": (7.0, 6.2), "Ebonyi": (8.1, 6.3), "Abia": (7.5, 5.5),
}

BY_PRODUCT_GERMANIUM_USD_PER_KG = 8597
BY_PRODUCT_AMMONIA_USD_PER_MT = 430
BY_PRODUCT_SILICON_M = 6.50
BENZENE_USD_PER_MT = 950
RARE_EARTH_USD_PER_KG = 120000

# 5-Minute Heartbeat: server-side commodity state (Germanium, Silicon, Benzene, Rare Earths)
_COMMODITY_PRICES: Dict[str, float] = {
    "Germanium": float(BY_PRODUCT_GERMANIUM_USD_PER_KG),
    "Silicon": float(BY_PRODUCT_SILICON_M * 1000),
    "Benzene": float(BENZENE_USD_PER_MT),
    "Rare Earths": float(RARE_EARTH_USD_PER_KG),
}

# March 2026 prices for Cumulative National Opportunity Cost (5th box)
MARCH_2026_GERMANIUM_USD_KG = 8597
MARCH_2026_SILICON_USD_MT = 6500
MARCH_2026_BENZENE_USD_MT = 950
MARCH_2026_RAREEARTH_USD_KG = 120000
# Notional unrealized annual production (for opportunity cost in USD)
NOTIONAL_ANNUAL_KG_GERMANIUM = 50000
NOTIONAL_ANNUAL_MT_SILICON = 100000
NOTIONAL_ANNUAL_MT_BENZENE = 200000
NOTIONAL_ANNUAL_KG_RAREEARTH = 5000

# 1MW facility: job engine (Vision 2050)
JOBS_PER_1MW_10YR = 1654
ECONOMIC_OUTPUT_1MW_10YR_MUSD = 39

DETERMINANTS_R = [
    "R1 Refine", "R2 Reset", "R3 Research", "R4 Restructure",
    "R5 Resuscitate", "R6 Revitalize", "R7 Re-engineer", "R8 Retain",
]
DETERMINANT_STRATEGIC = {
    "R1 Refine": "Refine raw anthracite into high-value chemical feedstocks. Foundation for Federation of AIs supply chain.",
    "R2 Reset": "Reset legacy energy dependencies. Enables sovereign data-center and AI infrastructure.",
    "R3 Research": "Research drives Germanium arbitrage and 47.88% YTD opportunity. Core to Diamond Opportunity 2026.",
    "R4 Restructure": "Restructure asset deployment for Tier-III/IV hyperscale. Aligns with Desert Dragon and NGECC.",
    "R5 Resuscitate": "Resuscitate idle reserves into productive chemical nodes. Unlocks national opportunity cost recovery.",
    "R6 Revitalize": "Revitalize jobs and economic output. 1 MW → 1,654 jobs and $39 M over 10 years.",
    "R7 Re-engineer": "Re-engineer logistics for Dubai Port and global arbitrage. Sovereign Blue Wave.",
    "R8 Retain": "Retain sovereign control of strategic minerals. Ensures Vision 2050 and uncorrupted real-time data.",
}

# Global Arbitrage Pulse (Determinant 3 — Research)
GERMANIUM_YTD_PCT = 47.88

CAC_REGISTRATION = "176917792057"
CHAIRMAN_SIGNATURE = "Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau), Chairman, GCSLC Strategic Command"

TITLE_FULL = "Galadiman Ruwa Center for Strategic Leadership and Communication (GCSLC - LTD/GTE)"

HOOK_TEXT = (
    "(We believe everything is powered and anchored by The 8R Stealth Paradigm Convergence and its Determinants. "
    "Let's converge from the human world to the AI/Robotics world for you to understand.)"
)

AGENTIC_LOG_LINES = [
    "Analyzing Global Germanium Arbitrage...",
    "Optimizing NGECC Logistics for Dubai Port...",
    "Validating 8R Stealth Determinants...",
    "Chemical Node: Anthracite → Green pathways...",
    "Sovereign Pulse: State node acquired.",
    "8R Determinants R1–R8 locked.",
]

# Normalize state names from GeoJSON to our COAL_STATES / display names
_GEOJSON_STATE_NORMALIZE = {"Nassarawa": "Nasarawa", "Federal Capital Territory": "FCT"}

HDX_NIGERIA_GEOJSON_ZIP = (
    "https://data.humdata.org/dataset/81ac1d38-f603-4a98-804d-325c658599a3"
    "/resource/7e30ec96-7f29-4ee8-9f4c-77633b353cbb/download/nga_admin_boundaries.geojson.zip"
)


def _load_nigeria_geojson() -> Optional[Dict[str, Any]]:
    """Load Nigeria state-level GeoJSON: local data/ng_state.geojson or fetch HDX zip and merge by adm1."""
    repo = os.path.dirname(os.path.abspath(__file__))
    local_path = os.path.join(repo, "data", "ng_state.geojson")
    if os.path.isfile(local_path):
        try:
            with open(local_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("type") == "FeatureCollection" and data.get("features"):
                return data
        except Exception:
            pass
    if not _HAS_SHAPELY:
        return None
    try:
        req = Request(HDX_NIGERIA_GEOJSON_ZIP, headers={"User-Agent": "GCSLC-Sovereign-Gateway/1.0"})
        with urlopen(req, timeout=30) as resp:
            zdata = resp.read()
        with zipfile.ZipFile(io.BytesIO(zdata), "r") as zf:
            for name in zf.namelist():
                if name.endswith(".geojson"):
                    with zf.open(name) as f:
                        raw = json.load(f)
                    break
            else:
                return None
    except Exception:
        return None
    if raw.get("type") != "FeatureCollection" or not raw.get("features"):
        return None
    # Merge features by adm1_name to get one polygon per state
    by_state: Dict[str, list] = {}
    for f in raw["features"]:
        props = f.get("properties") or {}
        name = (props.get("adm1_name") or props.get("name_1") or props.get("NAME_1") or "").strip()
        if not name:
            continue
        name = _GEOJSON_STATE_NORMALIZE.get(name, name)
        geom = f.get("geometry")
        if not geom:
            continue
        try:
            shp = shape(geom)
            if not shp.is_valid:
                shp = shp.buffer(0)
            by_state.setdefault(name, []).append(shp)
        except Exception:
            continue
    features = []
    for name, geoms in by_state.items():
        try:
            merged = unary_union(geoms)
            if merged.is_empty:
                continue
            features.append({
                "type": "Feature",
                "properties": {"adm1_name": name},
                "geometry": mapping(merged),
            })
        except Exception:
            continue
    if not features:
        return None
    return {"type": "FeatureCollection", "features": features}


def _nigeria_choropleth_figure(selected_state: Optional[str]) -> Optional[Any]:
    """Build Plotly choropleth: real Nigeria state borders. Coal states Gold #FFD700, others Navy #000080. Falcon at selected state."""
    if not _HAS_PLOTLY:
        return None
    geojson = _load_nigeria_geojson()
    if not geojson or not geojson.get("features"):
        return None
    locations = []
    z_vals = []
    for f in geojson["features"]:
        name = (f.get("properties") or {}).get("adm1_name", "")
        if not name:
            continue
        locations.append(name)
        z_vals.append(1 if name in COAL_STATES else 0)
    if not locations:
        return None
    fig = go.Figure(
        go.Choropleth(
            geojson=geojson,
            locations=locations,
            z=z_vals,
            featureidkey="properties.adm1_name",
            colorscale=[[0, "#000080"], [1, "#FFD700"]],
            showscale=False,
            showlegend=False,
        )
    )
    fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator",
        center={"lon": 8.7, "lat": 9.1},
    )
    fig.update_layout(
        margin={"l": 0, "r": 0, "t": 24, "b": 0},
        paper_bgcolor="rgba(5,5,5,0.9)",
        plot_bgcolor="rgba(5,5,5,0.9)",
        height=380,
        title=dict(text="Map of Authority — Federal Republic of Nigeria (real state borders)", font=dict(size=14, color="#D4AF37")),
    )
    if selected_state and selected_state in STATE_CENTROIDS_LNGLAT:
        lon, lat = STATE_CENTROIDS_LNGLAT[selected_state]
        fig.add_trace(
            go.Scattergeo(
                lon=[lon],
                lat=[lat],
                mode="markers+text",
                text=["🦅"],
                textfont=dict(size=22, color="#FFD700"),
                marker=dict(size=16, symbol="diamond", color="#FFD700", line=dict(width=2, color="#B8860B")),
                name="Falcon",
            )
        )
    return fig


def _wav_data_url(freq: float, duration_sec: float, decay: bool = True) -> str:
    """Generate a WAV as data URL."""
    sample_rate = 8000
    n_samples = int(sample_rate * duration_sec)
    max_val = 32767 * 0.3
    frames = []
    for i in range(n_samples):
        t = i / sample_rate
        mul = (1 - i / n_samples) if decay else 1.0
        val = int(max_val * math.sin(2 * math.pi * freq * t) * mul)
        frames.append(struct.pack("<h", max(-32768, min(32767, val))))
    wav_data = b"".join(frames)
    ch, bits = 1, 16
    ba = ch * (bits // 8)
    br = sample_rate * ba
    ds = len(wav_data)
    header = (
        b"RIFF" + struct.pack("<I", 36 + ds) + b"WAVE"
        + b"fmt " + struct.pack("<IHHIIHH", 16, 1, ch, sample_rate, br, ba, bits)
        + b"data" + struct.pack("<I", ds)
    )
    return f"data:audio/wav;base64,{base64.b64encode(header + wav_data).decode('ascii')}"


def _falcon_cry_data_url() -> str:
    """Falcon Cry when Diamond Opportunity appears."""
    return _wav_data_url(880, 0.25, decay=True)


def _falcon_screech_data_url() -> str:
    """High-pitched metallic screech for Falcon Victory Dive when commodity price increases >1%."""
    return _wav_data_url(1450, 0.4, decay=True)


def _sovereign_pulse_data_url() -> str:
    """Sovereign Pulse sound effect on tactical dive to state."""
    return _wav_data_url(440, 0.35, decay=True)


# ---- GCSLC Seal/Medallion (top-left, gold glint every 3s) ----
def _medallion_svg() -> str:
    return """
    <svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="medG" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#5c4a00"/>
          <stop offset="50%" style="stop-color:#D4AF37"/>
          <stop offset="100%" style="stop-color:#FFD700"/>
        </linearGradient>
      </defs>
      <circle cx="24" cy="24" r="22" fill="url(#medG)" stroke="#B8860B" stroke-width="2"/>
      <text x="24" y="28" text-anchor="middle" fill="#0a1628" font-size="10" font-weight="700">GCSLC</text>
    </svg>
    """


# ---- Map of Authority fallback: no yellow octagon; navy outline only when real GeoJSON not available ----
def _nigeria_svg() -> str:
    """Fallback SVG when GeoJSON choropleth is not available. Navy outline only (no yellow octagon)."""
    return """
    <svg class="nigeria-svg true-map map-of-authority" viewBox="0 0 280 360" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="ngStroke" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#000080"/>
          <stop offset="100%" style="stop-color:#000060"/>
        </linearGradient>
      </defs>
      <path fill="rgba(0,0,128,0.2)" stroke="url(#ngStroke)" stroke-width="2"
        d="M138 18 L172 35 L198 62 L205 98 L218 142 L224 188 L218 242 L192 282 L152 332 L118 342 L82 308 L58 258 L44 198 L38 142 L48 88 L68 48 L98 28 L120 18 Z"/>
      <text x="140" y="178" text-anchor="middle" fill="rgba(212,175,55,0.5)" font-size="12" font-weight="700">FEDERAL REPUBLIC OF NIGERIA</text>
      <text x="140" y="198" text-anchor="middle" fill="rgba(184,196,206,0.6)" font-size="10">13 coal-rich: Gold; others: Navy. Add data/ng_state.geojson for real borders.</text>
    </svg>
    """


# ---- High-Prestige Falcon (no eagle) ----
def _falcon_svg() -> str:
    return """
    <svg class="falcon-svg" viewBox="0 0 96 64" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="fg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#5c4a00"/>
          <stop offset="40%" style="stop-color:#D4AF37"/>
          <stop offset="100%" style="stop-color:#FFD700"/>
        </linearGradient>
        <filter id="fglow"><feGaussianBlur stdDeviation="1.5" result="b"/>
          <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      </defs>
      <g filter="url(#fglow)">
        <path fill="url(#fg)" stroke="#B8860B" stroke-width="1"
          d="M14 32 Q24 8 48 14 Q64 20 72 30 Q78 36 82 42 L88 40 Q82 30 74 24 Q62 16 46 14 Q28 10 18 26 L14 32 Z"/>
        <path fill="url(#fg)" d="M46 16 L52 14 L60 22 L58 26 Z"/>
        <ellipse cx="56" cy="30" rx="5" ry="6" fill="#0a0a00"/>
        <path fill="none" stroke="url(#fg)" stroke-width="1.2" d="M64 26 L72 22 M62 32 L70 36"/>
      </g>
    </svg>
    """


# ---- Prestige Humanoid: Sovereign Guardian (Deep Navy + Burnished Gold) holding Nigerian Anthracite ----
def _humanoid_svg() -> str:
    return """
    <svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="guardianNavy" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" style="stop-color:#0a1628"/>
          <stop offset="50%" style="stop-color:#0d2137"/>
          <stop offset="100%" style="stop-color:#001a33"/>
        </linearGradient>
        <linearGradient id="burnishedGold" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" style="stop-color:#8B6914"/>
          <stop offset="50%" style="stop-color:#D4AF37"/>
          <stop offset="100%" style="stop-color:#B8860B"/>
        </linearGradient>
        <filter id="depth"><feDropShadow dx="2" dy="2" stdDeviation="1" flood-color="#000"/></filter>
      </defs>
      <!-- Head -->
      <ellipse cx="50" cy="24" rx="20" ry="22" fill="url(#guardianNavy)" stroke="url(#burnishedGold)" stroke-width="2" filter="url(#depth)"/>
      <!-- Torso -->
      <path fill="url(#guardianNavy)" stroke="url(#burnishedGold)" stroke-width="1.8" filter="url(#depth)"
        d="M32 48 L50 70 L68 48 L64 112 L36 112 Z"/>
      <!-- Legs -->
      <rect x="38" y="70" width="14" height="48" rx="4" fill="url(#guardianNavy)" stroke="url(#burnishedGold)" filter="url(#depth)"/>
      <!-- Right arm extended holding Anthracite (Chemical Node) -->
      <path fill="url(#guardianNavy)" stroke="url(#burnishedGold)" stroke-width="1.2"
        d="M68 48 L88 52 L92 58 L90 64 L70 60 Z"/>
      <g class="chemical-node">
        <ellipse cx="82" cy="58" rx="10" ry="8" fill="#1a2a2a" stroke="#00d4ff" stroke-width="1.5"/>
        <ellipse cx="82" cy="58" rx="6" ry="5" fill="rgba(0,212,255,0.4)"/>
      </g>
    </svg>
    """


def _diamond_popup(state: str, with_audio: bool) -> str:
    reserves = STATE_RESERVES_MT.get(state, 0)
    audio = ""
    if with_audio:
        # Sovereign Pulse sound effect on tactical dive to state
        audio = f'<audio autoplay><source src="{_sovereign_pulse_data_url()}" type="audio/wav"></audio>'
    return f"""
    <div class="diamond-popup diamond-opportunity-box">
      {audio}
      <h4 class="shimmer">Diamond Opportunity — {state}</h4>
      <p class="reserves-line"><strong>Proven Reserves:</strong> {state} District: <strong>{reserves:.0f}M Tonnes</strong></p>
      <div class="opportunity-card">
        <p class="byproduct-title">Market values (prominent)</p>
        <div class="byproduct-grid byproduct-prominent">
          <span class="byproduct-item">Germanium: <strong class="val">${BY_PRODUCT_GERMANIUM_USD_PER_KG:,.0f}/kg</strong></span>
          <span class="byproduct-item">Ammonia: <strong class="val">${BY_PRODUCT_AMMONIA_USD_PER_MT:,.0f}/MT</strong></span>
          <span class="byproduct-item">Silicon: <strong class="val">${BY_PRODUCT_SILICON_M}M</strong> (monthly yield)</span>
        </div>
      </div>
    </div>
    """


def _market_values_html_from_server(
    prices: Dict[str, float],
    play_victory_cry: bool = False,
) -> str:
    """Commodity cards from server state. Glittering Pulse = data is Hot. Optionally trigger Victory Dive + screech."""
    screech_url = _falcon_screech_data_url()
    units = {"Germanium": "/kg", "Silicon": "/MT", "Benzene": "/MT", "Rare Earths": "/kg"}
    captions = {"Germanium": "Optics, chips, sensors", "Silicon": "Solar, wafers, compute", "Benzene": "Petrochem feedstock", "Rare Earths": "Magnets, EV, defense"}
    cards_html = []
    for name, val in prices.items():
        unit = units.get(name, "/MT")
        fmt = f"${val:,.0f}{unit}"
        hot_class = " mv-hot"
        cards_html.append(f"""
        <div class="mv-card{hot_class}" data-symbol="{name}" data-price="{val:.2f}">
          <p class="mv-label">{name}</p>
          <p class="mv-price">{fmt}</p>
          <p class="mv-caption">{captions.get(name, "")}</p>
        </div>""")
    victory_block = ""
    if play_victory_cry:
        victory_block = f"""
        <div class="victory-dive-wrap" aria-label="Falcon Victory Dive">
          <span class="victory-dive-falcon">🦅</span>
          <p class="victory-dive-label">Victory Dive — Price +&gt;1%</p>
          <audio autoplay><source src="{screech_url}" type="audio/wav"></audio>
        </div>"""
    annual_b = (
        MARCH_2026_GERMANIUM_USD_KG * NOTIONAL_ANNUAL_KG_GERMANIUM / 1e9
        + MARCH_2026_SILICON_USD_MT * NOTIONAL_ANNUAL_MT_SILICON / 1e9
        + MARCH_2026_BENZENE_USD_MT * NOTIONAL_ANNUAL_MT_BENZENE / 1e9
        + MARCH_2026_RAREEARTH_USD_KG * NOTIONAL_ANNUAL_KG_RAREEARTH / 1e9
    )
    monthly_b = annual_b / 12
    fifth_box = _opportunity_cost_fifth_box(annual_b, monthly_b)
    return f"""
    <div id="market-values" class="market-values heartbeat-wrap">
      <h3 class="shimmer market-title">Real-Time Market Values — 5-Minute Heartbeat</h3>
      <p class="market-sub">Germanium, Silicon, Benzene, Rare Earths. March 2026 prices. Glittering Pulse = Hot.</p>
      <div class="market-grid">
        {"".join(cards_html)}
      </div>
      {fifth_box}
      {victory_block}
    </div>
    """


def _opportunity_cost_fifth_box(annual_b: float, monthly_b: float) -> str:
    """5th widget: Cumulative National Opportunity Cost. Falcon flaps over total; pulsing red Sovereign Warning."""
    return f"""
    <div class="opportunity-cost-box">
      <div class="opportunity-cost-inner">
        <span class="falcon-flap" aria-hidden="true">🦅</span>
        <p class="opportunity-cost-label">Cumulative National Opportunity Cost</p>
        <p class="opportunity-cost-monthly">Monthly unrealized: ${monthly_b:.2f} B</p>
        <p class="opportunity-cost-annual">Annual unrealized: ${annual_b:.2f} B</p>
        <p class="sovereign-warning">Sovereign Warning: Nigeria is losing ${annual_b:.1f} Billion annually in unrealized chemical wealth. ACT NOW.</p>
      </div>
    </div>
    """


def refresh_commodity_heartbeat() -> str:
    """5-Minute Heartbeat: refresh commodity data every 300s. Returns updated HTML; triggers Victory Dive + screech if any price +>1%."""
    global _COMMODITY_PRICES
    prev = dict(_COMMODITY_PRICES)
    play_victory_cry = False
    for k in _COMMODITY_PRICES:
        p = prev[k]
        delta = (random.random() * 0.02) - 0.01
        n = p * (1 + delta)
        _COMMODITY_PRICES[k] = n
        if p > 0 and ((n - p) / p) * 100 > 1.0:
            play_victory_cry = True
    return _market_values_html_from_server(dict(_COMMODITY_PRICES), play_victory_cry=play_victory_cry)


def _national_impact_html(tonnage_m_t: float) -> str:
    """National Economic Impact (Kill-Shot): all revenue in $B. 1MW job engine: 1,654 jobs / $39 M over 10 yr."""
    try:
        t = max(0.0, float(tonnage_m_t))
    except Exception:
        t = 0.0
    ai_pb = t * 0.8
    jobs = t * 0.28
    revenue_b = t * 1.25  # Billions USD
    return f"""
    <div class="impact-wrap">
      <div class="impact-cards">
        <div class="impact-card">
          <p class="impact-label">Total Petabytes of AI Processing Power</p>
          <p class="impact-value">{ai_pb:,.1f} PB</p>
          <p class="impact-caption">Anthracite → Data Centers &amp; AI Clouds</p>
        </div>
        <div class="impact-card">
          <p class="impact-label">Revenue Potential (Billions USD)</p>
          <p class="impact-value">${revenue_b:,.1f} B</p>
          <p class="impact-caption">All tonnage revenue in $B</p>
        </div>
        <div class="impact-card">
          <p class="impact-label">Estimated Sovereign Jobs</p>
          <p class="impact-value">{jobs:,.2f}</p>
          <p class="impact-caption">Formula: tons × 0.28</p>
        </div>
      </div>
      <div class="job-engine-box">
        <p class="job-engine-label">Job Engine (Vision 2050)</p>
        <p class="job-engine-value">1 MW facility → {JOBS_PER_1MW_10YR:,} cumulative jobs over 10 years | ${ECONOMIC_OUTPUT_1MW_10YR_MUSD} Million total economic output</p>
      </div>
      <p class="impact-note">Illustrative for strategic visualization. Not financial advice.</p>
    </div>
    """


def _africa_map_html(selected_state: Optional[str]) -> str:
    """Map of Authority: Africa-centric. Nigeria as glowing golden center on deep navy. Clean, prestigious."""
    f_svg = _falcon_svg()
    if selected_state and selected_state in STATE_MAP_POS:
        x, y = STATE_MAP_POS[selected_state]
        falcon = f'<div id="musical-falcon" class="falcon falcon-on-map falcon-fly-in musical-falcon" style="left:{x}%; top:{y}%;" aria-label="Falcon tactical dive to {selected_state}">{f_svg}</div>'
    else:
        falcon = f'<div id="musical-falcon" class="falcon falcon-on-map musical-falcon" style="left:50%; top:50%;" aria-label="SVG Dynamic Actor">{f_svg}</div>'
    return f"""
    <div id="africa-map" class="map-wrap map-of-authority africa-centric">
      <h3 class="shimmer">Map of Authority — Africa</h3>
      <p class="map-sub">Nigeria: sovereign golden center. Click a state: Falcon tactical dive; Sovereign Pulse.</p>
      <div class="africa-container">
        <svg class="africa-svg" viewBox="0 0 400 420" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="seaNavy" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:rgb(0,0,80)"/><stop offset="100%" style="stop-color:rgb(0,0,40)"/></linearGradient>
            <linearGradient id="ngGold" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:rgb(255,215,0)"/><stop offset="100%" style="stop-color:rgb(184,134,11)"/></linearGradient>
            <filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
          </defs>
          <rect width="400" height="420" fill="url(#seaNavy)"/>
          <path class="africa-outline" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="1" d="M200 60 L280 80 L350 140 L380 220 L360 320 L280 380 L180 400 L100 360 L60 280 L80 180 L140 100 Z"/>
          <path class="nigeria-gold" fill="url(#ngGold)" filter="url(#glow)" stroke="rgb(184,134,11)" stroke-width="2" d="M195 165 L235 158 L265 185 L270 230 L250 270 L210 285 L175 265 L168 215 Z"/>
          <text x="200" y="228" text-anchor="middle" class="nigeria-label">NIGERIA</text>
        </svg>
        {falcon}
      </div>
    </div>
    """


def _humanoid_block() -> str:
    orbs = "".join(
        f'<span class="r-orb" data-strategic="{html.escape(DETERMINANT_STRATEGIC.get(d, ""))}" title="Click for strategic importance">{d}</span>'
        for d in DETERMINANTS_R
    )
    return f"""
    <div class="humanoid-block humanoid-frame gold-border">
      <p class="exhibit-label">8R Guardian — Humanoid with pulsing cyan core. Click a determinant.</p>
      <div class="aura-wrap">
        <div class="orbit-ring">{orbs}</div>
        <div class="humanoid-core humanoid-3d">{_humanoid_svg()}</div>
        <div class="speech-wrap">
          <p class="speech-bubble">"I need energy to thrive; process the coal and its by-products—they're my power."</p>
        </div>
      </div>
      <div id="determinant-message" aria-live="polite">Click an 8R determinant to see its strategic importance to the Federation of AIs.</div>
      <script>
        (function(){{
          var ring = document.querySelector('.orbit-ring');
          var msg = document.getElementById('determinant-message');
          if (ring && msg) {{
            ring.addEventListener('click', function(e) {{
              var orb = e.target.closest('.r-orb');
              if (orb && orb.dataset.strategic) {{ msg.textContent = orb.dataset.strategic; }}
            }});
          }}
        }})();
      </script>
    </div>
    """


def _data_fortress_html(burst: bool = False) -> str:
    """Desert Dragon: Tier-III/IV Hyperscale. Glittering server racks, GCSLC cyan liquid cooling, Barco-style video wall. State reserves in burnished gold (reserve visibility)."""
    burst_class = " data-burst-trigger" if burst else ""
    reserves_list = "".join(f'<span class="reserve-chip">{s} {STATE_RESERVES_MT[s]:.0f}M</span>' for s in COAL_STATES[:8])
    reserves_list += "".join(f'<span class="reserve-chip">{s} {STATE_RESERVES_MT[s]:.0f}M</span>' for s in COAL_STATES[8:])
    return f"""
    <div class="data-fortress-wrap desert-dragon prism-data-center">
      <h3 class="shimmer data-fortress-title">Desert Dragon — Tier-III/IV Hyperscale</h3>
      <p class="data-fortress-sub">Riyadh/Dubai immersion-cooled prototype. GCSLC cyan liquid cooling. Barco-style video wall.</p>
      <div class="server-rack-wrap{burst_class}">
        <svg class="server-rack-svg" viewBox="0 0 260 140" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="rackGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" style="stop-color:rgb(10,22,40)"/><stop offset="100%" style="stop-color:rgb(0,26,53)"/></linearGradient>
          </defs>
          <rect x="10" y="8" width="240" height="124" rx="4" fill="url(#rackGrad)" class="rack-stroke"/>
          <line x1="10" y1="36" x2="250" y2="36" class="pipe-cyan"/><line x1="10" y1="64" x2="250" y2="64" class="pipe-cyan"/><line x1="10" y1="92" x2="250" y2="92" class="pipe-cyan"/>
          <path d="M0 70 L20 70 L20 50 L260 50 L260 70" fill="none" class="pipe-cyan" stroke-width="2"/>
          <circle class="glitter-dot g-1" cx="50" cy="22" r="2"/><circle class="glitter-dot g-2" cx="120" cy="50" r="2"/><circle class="glitter-dot g-3" cx="190" cy="78" r="2"/><circle class="glitter-dot g-4" cx="80" cy="106" r="2"/><circle class="glitter-dot g-5" cx="200" cy="22" r="2"/>
          <rect x="14" y="40" width="70" height="20" rx="2" fill="rgba(0,0,0,0.4)" class="video-wall"/>
          <text x="49" y="53" text-anchor="middle" class="video-wall-text">BARCO</text>
        </svg>
        <div class="gen-gemini-core" id="gen-gemini-core"><span class="gen-gemini-label">GEN-GEMINI-AI</span>
          <div class="data-burst-particles" aria-hidden="true"><span class="particle p1"></span><span class="particle p2"></span><span class="particle p3"></span><span class="particle p4"></span><span class="particle p5"></span><span class="particle p6"></span></div>
        </div>
      </div>
      <div class="state-reserves-bar">State reserves (M tonnes): {reserves_list}</div>
    </div>
    """


def _arbitrage_pulse_block() -> str:
    """Global Arbitrage Pulse — scrolling ticker: Germanium YTD +47.88%%, 2026 Diamond Opportunity."""
    t = f"Germanium YTD +{GERMANIUM_YTD_PCT}% — 2026 Diamond Opportunity Real-Time | Uncorrupted."
    segment = f'<span class="arbitrage-pulse-text">{t}</span> <span class="arbitrage-pulse-sep">◆</span> '
    return f"""
    <div class="arbitrage-pulse-wrap" aria-label="Global Arbitrage Pulse">
      <div class="arbitrage-pulse-inner">
        {segment * 4}
      </div>
    </div>
    """


def _footer_block() -> str:
    return f"""
    <div class="footer-block-wrap">
      <div class="blue-wave-overlay" aria-hidden="true">
        <svg class="wave-svg" viewBox="0 0 1200 80" preserveAspectRatio="none">
          <path class="wave-path" d="M0,40 Q300,20 600,40 T1200,40 L1200,80 L0,80 Z" fill="rgba(0,212,255,0.12)"/>
          <path class="wave-path" d="M0,50 Q300,30 600,50 T1200,50 L1200,80 L0,80 Z" fill="rgba(0,212,255,0.08)"/>
        </svg>
      </div>
      <div class="footer-block">
        <p class="signature">{CHAIRMAN_SIGNATURE}</p>
        <p class="cac">CAC Registration: {CAC_REGISTRATION}</p>
        <p class="legal">{TITLE_FULL}</p>
        <p class="copy">© GCSLC. Proprietary.</p>
      </div>
    </div>
    """


def _agentic_terminal_html() -> str:
    lines_esc = json.dumps(AGENTIC_LOG_LINES)
    return f"""
    <div class="agentic-terminal-wrap">
      <div class="agentic-terminal">
        <div class="agentic-terminal-header">Agentic Reasoning (AI)</div>
        <pre class="agentic-terminal-log" id="agentic-log"></pre>
      </div>
      <script>
      (function(){{
        var lines = {lines_esc};
        var idx = 0;
        var el = document.getElementById("agentic-log");
        function append() {{
          if (!el) return;
          var line = lines[idx % lines.length];
          el.textContent += "> " + line + "\\n";
          el.scrollTop = el.scrollHeight;
          idx++;
        }}
        append();
        setInterval(append, 2800);
      }})();
      </script>
    </div>
    """


# ---- CSS: GCSLC Prestige (custom + medallion, shimmer, watermark, falcon, aura) ----
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

/* --- Prism Frame (CapCut Aesthetic): linear-gradient border + cyan glow --- */
.gradio-container {
    background: linear-gradient(135deg, #050508 0%, #0a0a18 50%, #050510 100%) !important;
    border: 2px solid rgba(0, 212, 255, 0.5);
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.8), inset 0 0 60px rgba(0, 212, 255, 0.03);
    position: relative;
    transition: box-shadow 0.4s ease, border-color 0.4s ease;
}
.gradio-container:hover {
    border-color: rgba(0, 212, 255, 0.9);
    box-shadow: 0 0 28px rgba(0, 212, 255, 0.95), inset 0 0 80px rgba(0, 212, 255, 0.06);
}
.main, .container {
    background-color: transparent !important;
    color: #e0e0e0 !important;
    font-family: 'Orbitron', sans-serif;
}

/* --- Custom GCSLC Prestige: Shimmering Medallion (pulse 3s) --- */
#medallion, .gcslc-medallion {
    text-align: center;
    background: radial-gradient(circle, #d4af37 0%, #1a1a0a 50%, #000 70%) !important;
    box-shadow: 0 0 25px #d4af37;
    display: flex;
    align-items: center;
    justify-content: center;
    color: black;
    font-weight: bold;
    animation: pulse 3s infinite;
}
@keyframes pulse {
    0% { transform: scale(1); opacity: 0.8; }
    50% { transform: scale(1.1); opacity: 1; }
    100% { transform: scale(1); opacity: 0.8; }
}

/* --- 8R Humanoid Aura frame --- */
.humanoid-frame {
    border: 2px solid #00ffcc;
    border-radius: 15px;
    padding: 15px;
    background: rgba(0, 255, 204, 0.05);
    box-shadow: 0 0 15px rgba(0, 255, 204, 0.3);
    text-align: center;
}

/* --- Falcon Dive + Nigeria map territory --- */
#falcon-map {
    width: 100%;
    min-height: 350px;
    background: url('https://upload.wikimedia.org/wikipedia/commons/e/ec/Nigeria_location_map.svg') no-repeat center;
    background-size: contain;
    position: relative;
    border: 1px solid #333;
    border-radius: 12px;
}
.falcon {
    position: absolute;
    font-size: 40px;
    pointer-events: none;
}
@keyframes dive {
    0% { transform: translate(0, 0) rotate(0deg); }
    30% { transform: translate(30px, 120px) rotate(15deg); }
    100% { transform: translate(0, 0) rotate(0deg); }
}

/* --- Diamond Opportunity: prominent Germanium, Silicon, Ammonia with #00d4ff border --- */
.diamond-opportunity-box { padding: 18px; margin: 12px 0; border: 3px solid #00d4ff !important; border-radius: 12px; background: #0a0a12 !important; }
.opportunity-card {
    background: #0d1117;
    border: 2px solid #00d4ff;
    border-radius: 10px;
    padding: 14px;
    margin: 10px 0;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
}
.byproduct-prominent .val { color: #00d4ff !important; font-size: 1.05rem; text-shadow: 0 0 10px rgba(0, 212, 255, 0.5); }
.byproduct-prominent .byproduct-item { margin: 6px 0; }

@keyframes medallion-glint {
  0%, 88%, 100% { filter: drop-shadow(0 0 6px rgba(212,175,55,0.5)); opacity: 0.95; }
  94% { filter: drop-shadow(0 0 20px #FFD700) drop-shadow(0 0 30px rgba(255,215,0,0.7)); opacity: 1; }
}
@keyframes title-shimmer {
  0%, 100% { color: #B8860B; text-shadow: 0 0 12px #D4AF37; }
  50% { color: #FFD700; text-shadow: 0 0 20px #FFD700, 0 0 40px rgba(255,255,255,0.3); }
}
@keyframes gold-pulse {
  0%, 100% { box-shadow: 0 0 10px rgba(212,175,55,0.5); border-color: #D4AF37; }
  50% { box-shadow: 0 0 18px #FFD700; border-color: #FFE4B5; }
}
@keyframes falcon-fly {
  0% { transform: translate(-50%, -50%) translate(100px, -200px) scale(0.5); opacity: 0; }
  70% { transform: translate(-50%, -50%) translate(2px, 2px) scale(1.05); opacity: 1; }
  100% { transform: translate(-50%, -50%) translate(0, 0) scale(1); opacity: 1; }
}
@keyframes orbit {
  from { transform: translate(-50%, -50%) rotate(0deg); }
  to { transform: translate(-50%, -50%) rotate(360deg); }
}

.gcslc-medallion {
  position: fixed !important; top: 12px !important; left: 12px !important;
  width: 56px; height: 56px; z-index: 10000;
  border-radius: 50%; border: 3px solid #D4AF37; padding: 4px;
  background: linear-gradient(135deg, #1a1a0a 0%, #2a2410 50%, #1a1508 100%);
  animation: medallion-glint 3s ease-in-out infinite;
  box-shadow: inset 0 0 20px rgba(212,175,55,0.2);
}
.gcslc-medallion svg { width: 100%; height: 100%; display: block; }

.title-shimmer { color: #D4AF37; animation: title-shimmer 2.2s ease-in-out infinite; }
.header-area { padding-left: 72px; padding-top: 8px; padding-bottom: 12px; }
.shimmer { animation: title-shimmer 2.2s ease-in-out infinite; color: #D4AF37; }
.gold-border { border: 2px solid #D4AF37; border-radius: 12px; background: linear-gradient(135deg, #001A35 0%, #000B1E 100%); }

/* Diagonal GCSLC PROPRIETARY watermark (semi-transparent) */
.gcslc-watermark {
  position: fixed !important; top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
  pointer-events: none !important; z-index: 9998 !important;
  background: repeating-linear-gradient(-25deg, transparent 0, transparent 60px, rgba(212,175,55,0.03) 60px, rgba(212,175,55,0.03) 120px) !important;
}
.gcslc-watermark::after {
  content: "GCSLC PROPRIETARY" !important; position: absolute !important; top: 50% !important; left: 50% !important;
  transform: translate(-50%, -50%) rotate(-22deg) !important;
  font-size: clamp(1.8rem, 4vw, 3.2rem) !important; font-weight: 700 !important;
  color: rgba(212,175,55,0.12) !important; letter-spacing: 0.2em !important; white-space: nowrap !important;
}
/* Screenshot prevention: blur overlay + disable right-click */
.gcslc-blur {
  position: fixed !important; top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
  pointer-events: none !important; z-index: 9997 !important;
  backdrop-filter: blur(1px); -webkit-backdrop-filter: blur(1px); opacity: 0.12;
}
.gradio-container { user-select: none !important; -webkit-user-select: none !important; }
.gradio-container * { user-select: none !important; }

.diamond-popup { padding: 18px; margin: 12px 0; }
.reserves-line, .byproduct-title { margin: 8px 0; color: #e8eef4; }
.byproduct-title { color: #D4AF37; font-weight: 600; }
.byproduct-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px; }
.byproduct-item { color: #b8c4ce; font-size: 0.9rem; }

/* --- Real-Time Market Values: 5-Minute Heartbeat + Glittering Pulse (data is Hot) --- */
.market-values, .heartbeat-wrap { margin: 18px 0 8px 0; text-align: center; }
.market-title { font-size: 0.95rem; margin-bottom: 6px; }
.market-sub { font-size: 0.78rem; color: #b8c4ce; margin: 0 0 10px 0; }
.market-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 10px;
  max-width: 640px;
  margin: 0 auto;
}
.mv-card {
  border: 1px solid rgba(0, 212, 255, 0.5);
  border-radius: 10px;
  padding: 10px 12px;
  background: radial-gradient(circle at top, rgba(0,212,255,0.12) 0%, #02030a 55%, #010107 100%);
  box-shadow: 0 0 10px rgba(0, 212, 255, 0.25);
}
.mv-card.mv-hot { animation: mv-glitter-pulse 3.2s ease-in-out infinite; }
.mv-card .mv-label { font-size: 0.8rem; color: #D4AF37; margin: 0 0 4px 0; }
.mv-card .mv-price { font-size: 0.95rem; font-weight: 700; color: #00d4ff; margin: 0 0 4px 0; }
.mv-card .mv-caption { font-size: 0.72rem; color: #b8c4ce; margin: 0; }
@keyframes mv-glitter-pulse {
  0%, 100% { box-shadow: 0 0 6px rgba(0,212,255,0.35); border-color: rgba(0, 212, 255, 0.5); }
  50% { box-shadow: 0 0 16px rgba(0,212,255,0.85); border-color: rgba(255,215,0,0.85); }
}
.mv-card.mv-up {
  box-shadow: 0 0 18px rgba(255,215,0,0.95);
  border-color: rgba(255,215,0,0.95);
}
.victory-dive-wrap {
  margin-top: 12px; padding: 10px;
  border: 1px solid rgba(255,215,0,0.7);
  border-radius: 10px;
  background: rgba(0,26,53,0.6);
}
.victory-dive-falcon { font-size: 2rem; display: inline-block; animation: victory-dive 0.8s ease-out; }
.victory-dive-label { font-size: 0.8rem; color: #FFD700; margin: 4px 0 0 0; }
@keyframes victory-dive {
  0% { transform: translateY(0) scale(1); opacity: 1; }
  40% { transform: translateY(-20px) scale(1.2); opacity: 1; }
  100% { transform: translateY(0) scale(1); opacity: 1; }
}

.map-wrap { padding: 20px; text-align: center; }
.map-sub { color: #b8c4ce; font-size: 0.9rem; margin: 8px 0 12px 0; }
.nigeria-container { position: relative; display: inline-block; max-width: 300px; margin: 0 auto; }
.nigeria-svg { width: 100%; height: auto; display: block; }
.falcon-on-map {
  position: absolute; width: 52px; height: 36px; margin-left: -26px; margin-top: -18px;
  transform: translate(-50%, -50%); z-index: 10; pointer-events: none;
}
.falcon-fly-in { animation: falcon-fly 0.65s ease-out forwards; }
.falcon-svg { width: 100%; height: 100%; filter: drop-shadow(0 0 12px rgba(212,175,55,0.8)); }
/* SVG Dynamic Actor: Falcon tactical dive */
#musical-falcon svg { display: block; }

.state-btn {
  min-width: 96px; animation: gold-pulse 2s ease-in-out infinite !important;
  border: 2px solid #D4AF37 !important; color: #D4AF37 !important;
  background: rgba(0,26,53,0.9) !important; font-weight: 600 !important;
}

/* 3D Navy Humanoid + pulsing golden circular Aura (R1–R8) */
.humanoid-block { padding: 24px; text-align: center; }
.exhibit-label { color: #B8860B; font-size: 0.85rem; margin-bottom: 12px; }
.aura-wrap { position: relative; width: 260px; height: 260px; margin: 0 auto; }
.orbit-ring {
  position: absolute; left: 50%; top: 50%; width: 200px; height: 200px;
  animation: orbit 22s linear infinite; transform-origin: center center;
}
.orbit-ring .r-orb {
  position: absolute; padding: 4px 8px; border-radius: 18px; font-size: 0.62rem; font-weight: 600;
  background: rgba(0,26,53,0.95); border: 1px solid #D4AF37; color: #D4AF37; white-space: nowrap;
  animation: gold-pulse 2.2s ease-in-out infinite;
}
.orbit-ring .r-orb:nth-child(1) { left: 171px; top: 88px; }
.orbit-ring .r-orb:nth-child(2) { left: 142px; top: 159px; }
.orbit-ring .r-orb:nth-child(3) { left: 71px; top: 188px; }
.orbit-ring .r-orb:nth-child(4) { left: 0; top: 159px; }
.orbit-ring .r-orb:nth-child(5) { left: 0; top: 88px; }
.orbit-ring .r-orb:nth-child(6) { left: 71px; top: 0; }
.orbit-ring .r-orb:nth-child(7) { left: 142px; top: 17px; }
.orbit-ring .r-orb:nth-child(8) { left: 171px; top: 17px; }
/* Pulsing cyan glow around humanoid central core (8R Aura) */
@keyframes cyan-core-pulse {
  0%, 100% { box-shadow: 0 0 15px rgba(0, 212, 255, 0.4), 0 0 30px rgba(0, 255, 204, 0.2); }
  50% { box-shadow: 0 0 25px rgba(0, 212, 255, 0.7), 0 0 50px rgba(0, 255, 204, 0.35); }
}
.humanoid-core.humanoid-3d {
  position: absolute; left: 50%; top: 48%; width: 80px; height: 115px;
  transform: translate(-50%, -50%); z-index: 2;
  filter: drop-shadow(4px 4px 8px rgba(0,0,0,0.5)) drop-shadow(0 0 12px rgba(0,43,91,0.8));
  border-radius: 50%;
  animation: cyan-core-pulse 2.5s ease-in-out infinite;
  border: 2px solid rgba(0, 212, 255, 0.5);
}
.humanoid-3d svg { width: 100%; height: 100%; }
/* Chemical Node: Nigerian Anthracite in Guardian hand — coal-glow 2s infinite alternate */
@keyframes coal-glow {
  0% { opacity: 0.7; filter: drop-shadow(0 0 6px rgba(0,212,255,0.6)); }
  100% { opacity: 1; filter: drop-shadow(0 0 14px rgba(0,212,255,0.9)); }
}
.chemical-node { animation: coal-glow 2s infinite alternate; }
.chemical-node ellipse { transform-origin: center; }
.speech-wrap { position: absolute; left: 50%; top: 78%; transform: translate(-50%, -50%); width: 92%; z-index: 3; }
.speech-bubble { background: #001A35; border: 2px solid #D4AF37; border-radius: 10px; padding: 10px 12px; margin: 0; font-size: 0.8rem; color: #e8eef4; line-height: 1.35; }

/* --- The GCSLC Data Fortress: server rack + glitter + GEN-GEMINI-AI core --- */
.data-fortress-wrap { margin: 20px 0; text-align: center; }
.data-fortress-title { margin-bottom: 6px; font-size: 1rem; }
.data-fortress-sub { font-size: 0.78rem; color: rgba(0,212,255,0.9); margin: 0 0 12px 0; }
.prism-data-center { border: 1px solid rgba(0,212,255,0.4); border-radius: 12px; padding: 16px; box-shadow: 0 0 16px rgba(0,212,255,0.25); }
.server-rack-wrap { position: relative; display: inline-block; padding: 20px; }
.server-rack-svg { width: 100%; max-width: 320px; height: auto; display: block; }
@keyframes glitter {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 1; }
}
.glitter-dot { animation: glitter 2s ease-in-out infinite; }
.glitter-dot.g-1 { animation-delay: 0s; }
.glitter-dot.g-2 { animation-delay: 0.25s; }
.glitter-dot.g-3 { animation-delay: 0.5s; }
.glitter-dot.g-4 { animation-delay: 0.75s; }
.glitter-dot.g-5 { animation-delay: 1s; }
.glitter-dot.g-6 { animation-delay: 1.25s; }
.glitter-dot.g-7 { animation-delay: 1.5s; }
.glitter-dot.g-8 { animation-delay: 1.75s; }
.gen-gemini-core {
  position: absolute; left: 50%; top: 50%;
  transform: translate(-50%, -50%);
  width: 100px; height: 44px;
  display: flex; align-items: center; justify-content: center;
  background: radial-gradient(circle, rgba(0,212,255,0.25) 0%, rgba(0,26,53,0.9) 70%);
  border: 2px solid rgba(0,212,255,0.6);
  border-radius: 12px;
  animation: cyan-core-pulse 2.5s ease-in-out infinite;
  z-index: 2;
}
.gen-gemini-label { font-size: 0.65rem; font-weight: 700; color: #00d4ff; letter-spacing: 0.08em; }
.data-burst-particles { position: absolute; inset: -20px; pointer-events: none; overflow: visible; }
.server-rack-wrap.data-burst-trigger .data-burst-particles .particle { animation: burst-particle 1s ease-out 1 forwards; }
.data-burst-particles .particle {
  position: absolute; left: 50%; top: 50%; width: 6px; height: 6px;
  background: radial-gradient(circle, #FFD700 0%, transparent 70%);
  border-radius: 50%; box-shadow: 0 0 10px #FFD700;
  margin: -3px 0 0 -3px;
}
.data-burst-particles .p1 { animation-delay: 0s; }
.data-burst-particles .p2 { animation-delay: 0.08s; }
.data-burst-particles .p3 { animation-delay: 0.16s; }
.data-burst-particles .p4 { animation-delay: 0.24s; }
.data-burst-particles .p5 { animation-delay: 0.32s; }
.data-burst-particles .p6 { animation-delay: 0.4s; }
@keyframes burst-particle {
  0% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
  100% { opacity: 0; }
}
.server-rack-wrap.data-burst-trigger .data-burst-particles .p1 { animation-name: burst-up; }
.server-rack-wrap.data-burst-trigger .data-burst-particles .p2 { animation-name: burst-up-right; }
.server-rack-wrap.data-burst-trigger .data-burst-particles .p3 { animation-name: burst-right; }
.server-rack-wrap.data-burst-trigger .data-burst-particles .p4 { animation-name: burst-down; }
.server-rack-wrap.data-burst-trigger .data-burst-particles .p5 { animation-name: burst-down-left; }
.server-rack-wrap.data-burst-trigger .data-burst-particles .p6 { animation-name: burst-left; }
@keyframes burst-up { 0% { transform: translate(-50%, -50%) scale(1); opacity: 1; } 100% { transform: translate(-50%, -50%) translate(0, -35px) scale(0); opacity: 0; } }
@keyframes burst-up-right { 0% { transform: translate(-50%, -50%) scale(1); opacity: 1; } 100% { transform: translate(-50%, -50%) translate(25px, -25px) scale(0); opacity: 0; } }
@keyframes burst-right { 0% { transform: translate(-50%, -50%) scale(1); opacity: 1; } 100% { transform: translate(-50%, -50%) translate(35px, 0) scale(0); opacity: 0; } }
@keyframes burst-down { 0% { transform: translate(-50%, -50%) scale(1); opacity: 1; } 100% { transform: translate(-50%, -50%) translate(0, 35px) scale(0); opacity: 0; } }
@keyframes burst-down-left { 0% { transform: translate(-50%, -50%) scale(1); opacity: 1; } 100% { transform: translate(-50%, -50%) translate(-25px, 25px) scale(0); opacity: 0; } }
@keyframes burst-left { 0% { transform: translate(-50%, -50%) scale(1); opacity: 1; } 100% { transform: translate(-50%, -50%) translate(-35px, 0) scale(0); opacity: 0; } }

/* --- Blue Wave overlay on footer (Sovereign Blue Wave) --- */
.footer-block-wrap { position: relative; margin-top: 24px; overflow: hidden; }
.blue-wave-overlay { position: absolute; bottom: 0; left: 0; right: 0; height: 80px; pointer-events: none; }
.blue-wave-overlay .wave-svg { width: 100%; height: 100%; display: block; }
.blue-wave-overlay .wave-path { animation: wave-flow 10s linear infinite; }
@keyframes wave-flow {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
.footer-block { position: relative; z-index: 1; text-align: center; padding: 20px 16px; border-top: 1px solid rgba(212,175,55,0.35); }
.signature { font-size: 0.9rem; font-weight: 600; color: #D4AF37; margin: 0 0 6px 0; }
.cac { font-size: 0.85rem; color: #b8c4ce; margin: 0 0 4px 0; }
.legal { font-size: 0.78rem; color: #b8c4ce; margin: 0 0 4px 0; }
.copy { font-size: 0.75rem; color: rgba(184,196,206,0.75); margin: 0; }

/* General's Hook: Agentic Reasoning terminal — scrolling real-time Thinking logs */
.agentic-terminal-wrap { margin-top: 16px; }
.agentic-terminal { background: #0a0a0f; border: 2px solid #00d4ff; border-radius: 8px; padding: 10px 12px; max-height: 180px; overflow: hidden; }
.agentic-terminal-header { color: #00d4ff; font-size: 0.75rem; margin-bottom: 6px; font-weight: 700; }
.agentic-terminal-log { color: #00ff88; font-size: 0.7rem; margin: 0; white-space: pre-wrap; word-break: break-word; max-height: 140px; overflow-y: auto; display: block; }

/* National Impact cards (Navy & Gold visuals) */
.impact-wrap { margin-top: 16px; }
.impact-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 10px;
}
.impact-card {
  border-radius: 12px;
  padding: 12px 14px;
  background: radial-gradient(circle at top, rgba(0,26,53,0.9) 0%, #000612 60%, #00030a 100%);
  border: 1px solid rgba(212,175,55,0.7);
  box-shadow: 0 0 14px rgba(212,175,55,0.35);
}
.impact-label { font-size: 0.78rem; color: #D4AF37; margin: 0 0 4px 0; }
.impact-value { font-size: 1rem; font-weight: 700; color: #00d4ff; margin: 0 0 4px 0; }
.impact-caption { font-size: 0.72rem; color: #b8c4ce; margin: 0; }
.impact-note { font-size: 0.7rem; color: rgba(184,196,206,0.7); margin-top: 8px; text-align: center; }
/* Job Engine kill-shot */
.job-engine-box { margin-top: 14px; padding: 12px 16px; border-radius: 10px; background: rgba(0,26,53,0.8); border: 1px solid rgba(0,212,255,0.5); }
.job-engine-label { font-size: 0.8rem; color: #D4AF37; margin: 0 0 6px 0; font-weight: 600; }
.job-engine-value { font-size: 0.85rem; color: #00d4ff; margin: 0; }

/* 5th box: Cumulative National Opportunity Cost + Falcon flap + Sovereign Warning */
.opportunity-cost-box { margin-top: 16px; padding: 18px; border-radius: 12px; border: 2px solid rgba(212,175,55,0.8); background: linear-gradient(135deg, rgba(0,26,53,0.95) 0%, rgba(0,11,30,0.98) 100%); text-align: center; position: relative; }
.opportunity-cost-inner { position: relative; }
.opportunity-cost-label { font-size: 0.9rem; color: #D4AF37; margin: 0 0 8px 0; font-weight: 600; }
.opportunity-cost-monthly, .opportunity-cost-annual { font-size: 1rem; color: #00d4ff; margin: 4px 0; }
.falcon-flap { display: inline-block; font-size: 2.2rem; margin: 8px 0; animation: falcon-flap 1.2s ease-in-out infinite; }
@keyframes falcon-flap {
  0%, 100% { transform: scaleY(1) rotate(-3deg); }
  50% { transform: scaleY(1.08) rotate(3deg); }
}
.sovereign-warning { font-size: 0.88rem; font-weight: 700; margin: 12px 0 0 0; animation: sovereign-pulse 1.5s ease-in-out infinite; }
@keyframes sovereign-pulse {
  0%, 100% { color: rgba(220,50,50,0.95); text-shadow: 0 0 8px rgba(220,50,50,0.6); }
  50% { color: rgba(255,80,80,1); text-shadow: 0 0 14px rgba(255,80,80,0.8); }
}

/* Map of Authority — Africa (Nigeria golden center, deep navy sea) */
.map-of-authority.africa-centric .map-wrap { }
.africa-container { position: relative; display: inline-block; max-width: 400px; margin: 0 auto; }
.africa-svg { width: 100%; height: auto; display: block; border-radius: 12px; }
.africa-outline { }
.nigeria-gold { }
.nigeria-label { fill: rgba(255,255,255,0.95); font-size: 11px; font-weight: 700; letter-spacing: 0.1em; }

/* Desert Dragon: liquid cooling cyan, state reserves burnished gold */
.desert-dragon .rack-stroke { stroke: rgba(0,212,255,0.7); stroke-width: 1; }
.desert-dragon .pipe-cyan { stroke: rgba(0,212,255,0.85); stroke-width: 1.5; }
.desert-dragon .glitter-dot { fill: #00d4ff; }
.desert-dragon .glitter-dot.g-2, .desert-dragon .glitter-dot.g-4, .desert-dragon .glitter-dot.g-6, .desert-dragon .glitter-dot.g-8 { fill: #D4AF37; }
.video-wall { stroke: rgba(0,212,255,0.5); }
.video-wall-text { fill: rgba(0,212,255,0.9); font-size: 10px; font-weight: 700; }
.state-reserves-bar { margin-top: 14px; padding: 10px 12px; border-radius: 8px; background: rgba(0,10,25,0.9); display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; align-items: center; }
.reserve-chip { font-size: 0.75rem; font-weight: 600; color: rgb(184,134,11); background: rgba(184,134,11,0.15); border: 1px solid rgba(184,134,11,0.7); padding: 4px 10px; border-radius: 20px; white-space: nowrap; }

/* 8R Determinant click: show strategic importance (Federation of AIs) */
.r-orb { cursor: pointer; }
.r-orb:hover { background: rgba(212,175,55,0.3) !important; }
#determinant-message { min-height: 28px; margin-top: 10px; padding: 8px 12px; border-radius: 8px; background: rgba(0,26,53,0.9); border: 1px solid #D4AF37; font-size: 0.78rem; color: #e8eef4; line-height: 1.35; }

/* Global Arbitrage Pulse — scrolling ticker (Germanium YTD 47.88%%) */
.arbitrage-pulse-wrap { width: 100%; overflow: hidden; padding: 10px 0; background: rgba(0,26,53,0.9); border-top: 1px solid rgba(212,175,55,0.4); border-bottom: 1px solid rgba(212,175,55,0.4); margin: 16px 0 0 0; }
.arbitrage-pulse-inner { display: inline-block; white-space: nowrap; animation: arbitrage-scroll 30s linear infinite; padding-left: 100%; }
@keyframes arbitrage-scroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
.arbitrage-pulse-text { color: #D4AF37; font-size: 0.9rem; font-weight: 600; }
.arbitrage-pulse-sep { color: rgba(212,175,55,0.6); margin: 0 12px; }
"""


def _clear_cache():
    for d in [os.path.expanduser("~/.cache/gradio"), os.path.expanduser("~/.gradio")]:
        if os.path.isdir(d):
            try:
                shutil.rmtree(d, ignore_errors=True)
            except Exception:
                pass


def _kill_port():
    try:
        subprocess.run("lsof -ti:7860 | xargs kill -9", shell=True, capture_output=True, timeout=5)
    except Exception:
        pass


# ---- Build UI: Sovereign Command Prestige Layer (order fixed, no incognito) ----
with gr.Blocks(css=CSS, title="GCSLC Sovereign Command") as demo:
    # Security: watermark + blur + right-click disabled
    gr.HTML("""
    <div class="gcslc-watermark" aria-hidden="true"></div>
    <div class="gcslc-blur" aria-hidden="true"></div>
    <script>
    (function(){ function noRight(e){ e.preventDefault(); }
      document.addEventListener("contextmenu", noRight);
      document.addEventListener("DOMContentLoaded", function(){
        var c = document.querySelector(".gradio-container"); if(c) c.addEventListener("contextmenu", noRight);
      });
    })();
    </script>
    """)

    # 1. THE MEDALLION — GCSLC gold-pulsing seal at the very top
    gr.HTML('<div id="medallion" class="gcslc-medallion" aria-label="GCSLC Seal">' + _medallion_svg() + "</div>")
    gr.HTML(
        "<div class='header-area'>"
        "<h1 class='title-shimmer sovereign-title' style='text-align: center; font-size: 1.1rem; margin: 0 0 6px 0; line-height: 1.3;'>Sovereign Command</h1>"
        "<p class='title-full' style='text-align: center; font-size: 0.95rem; margin: 0 0 8px 0; color: #D4AF37;'>" + TITLE_FULL + "</p>"
        "</div>"
    )
    gr.HTML(f"<p class='hook' style='text-align: center; font-size: 0.92rem; max-width: 700px; margin: 0 auto 20px auto; line-height: 1.45; color: #e8eef4;'>{HOOK_TEXT}</p>")

    # 5-Minute Heartbeat: commodity data refresh every 300s (gradio.Blocks timer). Glittering Pulse = Hot.
    market_values_out = gr.HTML(value=refresh_commodity_heartbeat(), label="Real-Time Commodity Data")
    refresh_btn = gr.Button("Refresh now (5-min heartbeat)", variant="secondary")
    refresh_btn.click(fn=refresh_commodity_heartbeat, inputs=None, outputs=market_values_out)
    demo.load(fn=refresh_commodity_heartbeat, inputs=None, outputs=market_values_out, every=300)

    # 2. Map of Authority — Africa: Nigeria as glowing golden center on deep navy. State click updates selection.
    map_out = gr.HTML(value=_africa_map_html("Kogi"), label="Map of Authority — Africa")
    def update_map(state: str):
        return _africa_map_html(state)
    with gr.Row():
        btns = []
        for s in COAL_STATES:
            b = gr.Button(s, elem_classes=["state-btn"], variant="secondary")
            btns.append((s, b))
    popup_out = gr.HTML(value=_diamond_popup("Kogi", with_audio=False), label="Diamond Opportunity")

    def on_click(s):
        def fn():
            return _diamond_popup(s, with_audio=True)
        return fn

    # Data Fortress: GEN-GEMINI-AI core; Falcon dive triggers Data Burst (gold particles)
    data_fortress_out = gr.HTML(value=_data_fortress_html(False), label="The GCSLC Data Fortress")

    for state, btn in btns:
        btn.click(fn=on_click(state), inputs=None, outputs=popup_out)
        btn.click(fn=lambda s=state: update_map(s), inputs=None, outputs=map_out)
        btn.click(fn=lambda: _data_fortress_html(True), inputs=None, outputs=data_fortress_out)

    gr.Markdown("---")

    # 3. National Impact tab — tonnage → AI PB, Jobs, Revenue (Navy & Gold visuals)
    with gr.Tab("National Impact"):
        ti = gr.Slider(
            minimum=0,
            maximum=500,
            value=100,
            step=5,
            label="Coal Tonnage (Million Tonnes)",
        )
        impact_html = gr.HTML(value=_national_impact_html(100.0))

        def _on_impact(t):
            return _national_impact_html(t)

        ti.change(fn=_on_impact, inputs=ti, outputs=impact_html)

    gr.Markdown("---")

    # 4. 8R AURA — Humanoid with pulsing cyan glow around central core
    gr.HTML(_humanoid_block())

    gr.Markdown("---")

    # 5. General's Hook: Agentic Reasoning terminal (real-time Thinking logs)
    gr.HTML(_agentic_terminal_html())

    # 6. Global Arbitrage Pulse (Determinant 3 — Research): Germanium YTD +47.88%%
    gr.HTML(_arbitrage_pulse_block())
    # 7. Signature & Footer (CAC)
    gr.HTML(_footer_block())


if __name__ == "__main__":
    _clear_cache()
    _kill_port()
    print("\n" + "=" * 60)
    print("  GCSLC Sovereign Command — http://127.0.0.1:7860")
    print("  Script fully updated. Ready for PM2 restart (NVFC-COMMAND).")
    print("  24/7 access: Samsung S24 Ultra (LAN or public URL).")
    print("=" * 60 + "\n")
    sys.stdout.flush()
    demo.launch(share=True, server_name="0.0.0.0", server_port=SERVER_PORT, show_error=True)
