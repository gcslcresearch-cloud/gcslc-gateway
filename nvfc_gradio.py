"""
GCSLC Strategic Command Center — Mission Directive: No Placeholders.
Map of Authority: Real Nigeria state borders (GeoJSON choropleth). Gold #FFD700 coal states, Navy #000080 else.
Sovereign Guardian: Navy + Gold SVG, coal with coal-glow 2s infinite alternate.
Falcon: Python updates (x,y) to state coordinates on map (tactical dive).
Agentic Reasoning: gr.HTML scrolling Thinking logs at bottom.
"""
import base64
import io
import json
import math
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

DETERMINANTS_R = [
    "R1 Refine", "R2 Reset", "R3 Research", "R4 Restructure",
    "R5 Resuscitate", "R6 Revitalize", "R7 Re-engineer", "R8 Retain",
]

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


def _map_html(selected_state: Optional[str]) -> str:
    ng = _nigeria_svg()
    f_svg = _falcon_svg()
    if selected_state and selected_state in STATE_MAP_POS:
        x, y = STATE_MAP_POS[selected_state]
        falcon = f'<div id="musical-falcon" class="falcon falcon-on-map falcon-fly-in musical-falcon" style="left:{x}%; top:{y}%;" aria-label="Falcon tactical dive to {selected_state}">{f_svg}</div>'
    else:
        falcon = f'<div id="musical-falcon" class="falcon falcon-on-map musical-falcon" style="left:50%; top:50%;" aria-label="SVG Dynamic Actor">{f_svg}</div>'
    return f"""
    <div id="falcon-map" class="map-wrap gold-border true-map-wrap map-of-authority">
      <h3 class="shimmer">Map of Authority — Federal Republic of Nigeria</h3>
      <p class="map-sub">13 coal-rich states: Gold (#FFD700). Others: Navy (#000080). Click a state: Falcon tactical dive to coordinates; Sovereign Pulse plays.</p>
      <div class="nigeria-container">
        {ng}
        {falcon}
      </div>
    </div>
    """


def _humanoid_block() -> str:
    orbs = "".join(f'<span class="r-orb">{d}</span>' for d in DETERMINANTS_R)
    return f"""
    <div class="humanoid-block humanoid-frame gold-border">
      <p class="exhibit-label">8R Aura — Humanoid with pulsing cyan core</p>
      <div class="aura-wrap">
        <div class="orbit-ring">{orbs}</div>
        <div class="humanoid-core humanoid-3d">{_humanoid_svg()}</div>
        <div class="speech-wrap">
          <p class="speech-bubble">"I need energy to thrive; process the coal and its by-products—they're my power."</p>
        </div>
      </div>
    </div>
    """


def _data_fortress_html(burst: bool = False) -> str:
    """The GCSLC Data Fortress: server rack SVG, glitter lights, GEN-GEMINI-AI pulsing core. burst=True triggers Data Burst (gold particles) on Falcon dive."""
    burst_class = " data-burst-trigger" if burst else ""
    return f"""
    <div class="data-fortress-wrap">
      <h3 class="shimmer data-fortress-title">The GCSLC Data Fortress</h3>
      <div class="server-rack-wrap{burst_class}">
        <svg class="server-rack-svg" viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="rackGrad" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" style="stop-color:#0a1628"/>
              <stop offset="50%" style="stop-color:#0d2137"/>
              <stop offset="100%" style="stop-color:#001a33"/>
            </linearGradient>
          </defs>
          <rect x="10" y="8" width="180" height="104" rx="4" fill="url(#rackGrad)" stroke="#00d4ff" stroke-width="1"/>
          <line x1="10" y1="28" x2="190" y2="28" stroke="#00d4ff" stroke-width="0.8" opacity="0.7"/>
          <line x1="10" y1="48" x2="190" y2="48" stroke="#00d4ff" stroke-width="0.8" opacity="0.7"/>
          <line x1="10" y1="68" x2="190" y2="68" stroke="#00d4ff" stroke-width="0.8" opacity="0.7"/>
          <line x1="10" y1="88" x2="190" y2="88" stroke="#00d4ff" stroke-width="0.8" opacity="0.7"/>
          <circle class="glitter-dot g-1" cx="40" cy="18" r="2" fill="#00d4ff"/>
          <circle class="glitter-dot g-2" cx="90" cy="38" r="2" fill="#FFD700"/>
          <circle class="glitter-dot g-3" cx="150" cy="58" r="2" fill="#00d4ff"/>
          <circle class="glitter-dot g-4" cx="60" cy="78" r="2" fill="#FFD700"/>
          <circle class="glitter-dot g-5" cx="120" cy="98" r="2" fill="#00d4ff"/>
          <circle class="glitter-dot g-6" cx="170" cy="18" r="2" fill="#FFD700"/>
          <circle class="glitter-dot g-7" cx="30" cy="58" r="2" fill="#00d4ff"/>
          <circle class="glitter-dot g-8" cx="140" cy="38" r="2" fill="#FFD700"/>
        </svg>
        <div class="gen-gemini-core" id="gen-gemini-core">
          <span class="gen-gemini-label">GEN-GEMINI-AI</span>
          <div class="data-burst-particles" aria-hidden="true">
            <span class="particle p1"></span><span class="particle p2"></span><span class="particle p3"></span>
            <span class="particle p4"></span><span class="particle p5"></span><span class="particle p6"></span>
          </div>
        </div>
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
.data-fortress-title { margin-bottom: 12px; font-size: 1rem; }
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

    # 2. Map of Authority: Real Nigeria state borders (gr.Plot choropleth) or fallback SVG. Falcon position updated by Python on state click.
    _initial_fig = _nigeria_choropleth_figure("Kogi")
    use_plotly_map = _initial_fig is not None
    if use_plotly_map:
        map_out = gr.Plot(value=_initial_fig, label="Map of Authority — Nigeria (real state borders)")
        def update_map(state: str):
            return _nigeria_choropleth_figure(state)
    else:
        map_out = gr.HTML(value=_map_html("Kogi"), label="Map of Authority — Nigeria")
        def update_map(state: str):
            return _map_html(state)
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

    # 3. 8R AURA — Humanoid with pulsing cyan glow around central core
    gr.HTML(_humanoid_block())

    gr.Markdown("---")

    # 4. General's Hook: Agentic Reasoning terminal (real-time Thinking logs)
    gr.HTML(_agentic_terminal_html())

    # 5. Signature & Footer (CAC)
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
