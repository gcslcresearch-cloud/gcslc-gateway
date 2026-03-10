"""
African Wealth Cloud Gateway — Master production file for Hugging Face Spaces.
GCSLC Sovereign Command: True Map of Nigeria (36 state borders), Kill-Shot $1.87B, 8R Humanoid Guardian.
"""
import html
import json
import os
from typing import Optional, Dict, Any, Tuple, List

import gradio as gr
import plotly.graph_objects as go

# ----- Constants -----
TITLE_FULL = "Galadiman Ruwa Center for Strategic Leadership and Communication (GCSLC - LTD/GTE)"
CHAIRMAN_SIGNATURE = "Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau), Chairman, GCSLC Strategic Command"
CAC_REGISTRATION = "176917792057"

# 13 coal-rich states (Burnished Gold); others Deep Navy
COAL_STATES = [
    "Enugu", "Kogi", "Benue", "Nasarawa", "Gombe", "Adamawa", "Delta",
    "Edo", "Ondo", "Bauchi", "Anambra", "Ebonyi", "Abia",
]

# Kill-Shot: Cumulative National Opportunity Cost ($1.87 Billion/year)
ANNUAL_OPPORTUNITY_COST_BILLIONS = 1.87
MONTHLY_OPPORTUNITY_COST_BILLIONS = round(ANNUAL_OPPORTUNITY_COST_BILLIONS / 12, 2)

# Falcon centroids (lon, lat) for Plotly map
STATE_CENTROIDS_LNGLAT: Dict[str, Tuple[float, float]] = {
    "Enugu": (7.5, 6.4), "Kogi": (6.7, 7.8), "Benue": (8.2, 7.2), "Nasarawa": (8.5, 8.5),
    "Gombe": (11.2, 10.3), "Adamawa": (12.5, 9.3), "Delta": (6.2, 5.9), "Edo": (6.3, 6.5),
    "Ondo": (5.7, 7.2), "Bauchi": (9.8, 10.3), "Anambra": (7.0, 6.2), "Ebonyi": (8.1, 6.3), "Abia": (7.5, 5.5),
    "FCT": (7.5, 9.1), "Lagos": (3.4, 6.5), "Kano": (8.5, 12.0), "Kaduna": (7.4, 10.5),
    "Rivers": (6.9, 4.8), "Oyo": (3.9, 7.8), "Borno": (12.2, 11.8), "Jigawa": (9.4, 11.7),
    "Imo": (7.0, 5.5), "Akwa Ibom": (7.9, 4.9), "Ogun": (3.5, 7.2), "Osun": (4.5, 7.6),
    "Plateau": (8.9, 9.9), "Sokoto": (5.2, 13.0), "Katsina": (7.6, 12.9), "Niger": (6.0, 10.0),
    "Kwara": (4.5, 8.5), "Cross River": (8.3, 5.9), "Bayelsa": (6.3, 4.8), "Ekiti": (5.2, 7.6),
    "Taraba": (10.8, 7.9), "Yobe": (11.7, 11.9), "Kebbi": (4.2, 11.2), "Zamfara": (6.2, 12.2),
}

_GEOJSON_STATE_NORMALIZE = {"Nassarawa": "Nasarawa", "Federal Capital Territory": "FCT", "Abuja": "FCT"}
COLOR_DEEP_NAVY = "rgb(0, 32, 96)"
COLOR_BURNISHED_GOLD = "rgb(184, 134, 11)"

# 8R Determinants
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


def _state_name_from_props(props: Dict[str, Any]) -> Optional[str]:
    name = (
        (props.get("shapeName") or props.get("adm1_name") or props.get("name_1")
         or props.get("NAME_1") or props.get("name") or props.get("ADM1_NAME") or "")
    )
    if isinstance(name, str):
        name = name.strip()
    else:
        name = ""
    if not name:
        return None
    return _GEOJSON_STATE_NORMALIZE.get(name, name)


def _load_nigeria_geojson() -> Optional[Dict[str, Any]]:
    """Load Nigeria 36 state borders from data/ng_state.geojson (for HF Spaces, add this file to the repo)."""
    repo = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(repo, "data", "ng_state.geojson")
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return None
    if data.get("type") != "FeatureCollection" or not data.get("features"):
        return None
    features = []
    for f in data["features"]:
        props = f.get("properties") or {}
        name = _state_name_from_props(props)
        if not name:
            continue
        geom = f.get("geometry")
        if not geom:
            continue
        features.append({"type": "Feature", "properties": {"adm1_name": name}, "geometry": geom})
    if not features:
        return None
    return {"type": "FeatureCollection", "features": features}


def _nigeria_choropleth(selected_state: Optional[str]) -> Optional[go.Figure]:
    """True Map of Nigeria: high-prestige Plotly choropleth. 36 state borders. Coal = Burnished Gold, others = Deep Navy. Responsive."""
    geojson_data = _load_nigeria_geojson()
    if not geojson_data or not geojson_data.get("features"):
        return None
    locations = []
    z_vals = []
    for f in geojson_data["features"]:
        name = (f.get("properties") or {}).get("adm1_name", "")
        if not name:
            continue
        locations.append(name)
        z_vals.append(1 if name in COAL_STATES else 0)
    if not locations:
        return None
    fig = go.Figure(
        go.Choropleth(
            geojson=geojson_data,
            locations=locations,
            z=z_vals,
            featureidkey="properties.adm1_name",
            colorscale=[[0, COLOR_DEEP_NAVY], [1, COLOR_BURNISHED_GOLD]],
            showscale=False,
        )
    )
    fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator",
        center={"lon": 8.7, "lat": 9.1},
    )
    # Responsive for Samsung S24 Ultra and mobile
    fig.update_layout(
        margin={"l": 0, "r": 0, "t": 24, "b": 0},
        paper_bgcolor="rgba(5,5,5,0.95)",
        plot_bgcolor="rgba(5,5,5,0.95)",
        height=400,
        autosize=True,
        title=dict(
            text="Map of Authority — Federal Republic of Nigeria (36 State Borders)",
            font=dict(size=14, color="rgb(212, 175, 55)"),
        ),
    )
    if selected_state and selected_state in STATE_CENTROIDS_LNGLAT:
        lon, lat = STATE_CENTROIDS_LNGLAT[selected_state]
        fig.add_trace(
            go.Scattergeo(
                lon=[lon], lat=[lat],
                mode="markers+text",
                text=["🦅"],
                textfont=dict(size=20, color=COLOR_BURNISHED_GOLD),
                marker=dict(size=16, symbol="diamond", color=COLOR_BURNISHED_GOLD, line=dict(width=2, color=COLOR_BURNISHED_GOLD)),
                name="Falcon",
            )
        )
    return fig


def _kill_shot_html() -> str:
    """5th Box (Kill-Shot): Cumulative National Opportunity Cost — front and center. $1.87 B/year, pulsing red warning."""
    return f"""
    <div class="kill-shot-box">
      <div class="kill-shot-inner">
        <span class="falcon-flap" aria-hidden="true">🦅</span>
        <p class="kill-shot-label">Cumulative National Opportunity Cost</p>
        <p class="kill-shot-monthly">Monthly unrealized: ${MONTHLY_OPPORTUNITY_COST_BILLIONS} B</p>
        <p class="kill-shot-annual">Annual unrealized: ${ANNUAL_OPPORTUNITY_COST_BILLIONS} B</p>
        <p class="sovereign-warning">Sovereign Warning: Nigeria is losing $1.87 Billion annually in unrealized chemical wealth. ACT NOW.</p>
      </div>
    </div>
    """


def _humanoid_svg() -> str:
    """8R Humanoid Guardian — Navy & Gold, holding anthracite."""
    return """
    <svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="gNavy" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" style="stop-color:#0a1628"/><stop offset="50%" style="stop-color:#0d2137"/><stop offset="100%" style="stop-color:#001a33"/>
        </linearGradient>
        <linearGradient id="gGold" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" style="stop-color:#8B6914"/><stop offset="50%" style="stop-color:#D4AF37"/><stop offset="100%" style="stop-color:#B8860B"/>
        </linearGradient>
        <filter id="depth"><feDropShadow dx="2" dy="2" stdDeviation="1" flood-color="#000"/></filter>
      </defs>
      <ellipse cx="50" cy="24" rx="20" ry="22" fill="url(#gNavy)" stroke="url(#gGold)" stroke-width="2" filter="url(#depth)"/>
      <path fill="url(#gNavy)" stroke="url(#gGold)" stroke-width="1.8" filter="url(#depth)" d="M32 48 L50 70 L68 48 L64 112 L36 112 Z"/>
      <rect x="38" y="70" width="14" height="48" rx="4" fill="url(#gNavy)" stroke="url(#gGold)" filter="url(#depth)"/>
      <path fill="url(#gNavy)" stroke="url(#gGold)" stroke-width="1.2" d="M68 48 L88 52 L92 58 L90 64 L70 60 Z"/>
      <g class="chemical-node">
        <ellipse cx="82" cy="58" rx="10" ry="8" fill="#1a2a2a" stroke="#00d4ff" stroke-width="1.5"/>
        <ellipse cx="82" cy="58" rx="6" ry="5" fill="rgba(0,212,255,0.4)"/>
      </g>
    </svg>
    """


def _humanoid_block() -> str:
    """8R Humanoid Guardian with pulsing determinants around it."""
    orbs = "".join(
        f'<span class="r-orb" data-strategic="{html.escape(DETERMINANT_STRATEGIC.get(d, ""))}" title="Click">{d}</span>'
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
      <div id="determinant-message" aria-live="polite">Click an 8R determinant for strategic importance to the Federation of AIs.</div>
      <script>
        (function(){{
          var ring = document.querySelector('.orbit-ring');
          var msg = document.getElementById('determinant-message');
          if (ring && msg) ring.addEventListener('click', function(e) {{
            var orb = e.target.closest('.r-orb');
            if (orb && orb.dataset.strategic) msg.textContent = orb.dataset.strategic;
          }});
        }})();
      </script>
    </div>
    """


def _map_fallback_html() -> str:
    """Fallback when GeoJSON not in repo."""
    return """
    <div class="map-fallback">
      <h3 class="shimmer">Map of Authority — Federal Republic of Nigeria (36 State Borders)</h3>
      <p class="map-sub">Coal-rich states: Burnished Gold. Others: Deep Navy.</p>
      <p class="map-note">Add <code>data/ng_state.geojson</code> to this Space for the True Map. High-prestige Plotly choropleth.</p>
    </div>
    """


# ----- Responsive CSS: Samsung S24 Ultra + prestige -----
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
.gradio-container { background: linear-gradient(135deg, #050508 0%, #0a0a18 50%, #050510 100%) !important; }
.main, .container { background: transparent !important; color: #e0e0e0; font-family: 'Orbitron', sans-serif; }

/* Kill-Shot: front and center, pulsing red */
.kill-shot-box {
  margin: 0 auto 24px auto; padding: 20px; max-width: 560px; text-align: center;
  border-radius: 16px; border: 2px solid rgba(212,175,55,0.85);
  background: linear-gradient(135deg, rgba(0,26,53,0.98) 0%, rgba(0,11,30,0.99) 100%);
  box-shadow: 0 0 24px rgba(212,175,55,0.3);
}
.kill-shot-inner { position: relative; }
.kill-shot-label { font-size: clamp(0.9rem, 2.5vw, 1rem); color: rgb(212,175,55); margin: 0 0 8px 0; font-weight: 600; }
.kill-shot-monthly, .kill-shot-annual { font-size: clamp(1rem, 3vw, 1.1rem); color: #00d4ff; margin: 6px 0; }
.falcon-flap { display: inline-block; font-size: clamp(1.8rem, 5vw, 2.2rem); margin: 8px 0; animation: falcon-flap 1.2s ease-in-out infinite; }
@keyframes falcon-flap { 0%, 100% { transform: scaleY(1) rotate(-3deg); } 50% { transform: scaleY(1.08) rotate(3deg); } }
.sovereign-warning {
  font-size: clamp(0.85rem, 2.2vw, 0.95rem); font-weight: 700; margin: 14px 0 0 0;
  animation: sovereign-pulse 1.5s ease-in-out infinite;
}
@keyframes sovereign-pulse {
  0%, 100% { color: rgba(220,50,50,0.95); text-shadow: 0 0 10px rgba(220,50,50,0.7); }
  50% { color: rgba(255,80,80,1); text-shadow: 0 0 18px rgba(255,80,80,0.9); }
}

/* Map: responsive */
.map-fallback { padding: 20px; text-align: center; }
.map-sub { color: #b8c4ce; font-size: 0.9rem; margin: 8px 0; }
.map-note { font-size: 0.8rem; color: rgba(184,196,206,0.8); margin-top: 12px; }
.js-plotly-plot, .plotly { width: 100% !important; max-width: 100% !important; }
.js-plotly-plot .svg-container { width: 100% !important; }

/* 8R Humanoid */
.humanoid-frame { border: 2px solid rgba(0,212,255,0.6); border-radius: 16px; padding: 20px; background: rgba(0,255,204,0.05); text-align: center; }
.exhibit-label { color: rgb(184,134,11); font-size: clamp(0.8rem, 2vw, 0.9rem); margin-bottom: 12px; }
.aura-wrap { position: relative; width: min(280px, 90vw); height: min(280px, 90vw); margin: 0 auto; }
.orbit-ring {
  position: absolute; left: 50%; top: 50%; width: 200px; height: 200px;
  animation: orbit 22s linear infinite; transform-origin: center center;
}
.orbit-ring .r-orb {
  position: absolute; padding: 4px 8px; border-radius: 18px; font-size: clamp(0.55rem, 1.5vw, 0.65rem); font-weight: 600;
  background: rgba(0,26,53,0.95); border: 1px solid rgb(212,175,55); color: rgb(212,175,55); white-space: nowrap;
  animation: gold-pulse 2.2s ease-in-out infinite; cursor: pointer;
}
.orbit-ring .r-orb:nth-child(1) { left: 171px; top: 88px; } .orbit-ring .r-orb:nth-child(2) { left: 142px; top: 159px; }
.orbit-ring .r-orb:nth-child(3) { left: 71px; top: 188px; } .orbit-ring .r-orb:nth-child(4) { left: 0; top: 159px; }
.orbit-ring .r-orb:nth-child(5) { left: 0; top: 88px; } .orbit-ring .r-orb:nth-child(6) { left: 71px; top: 0; }
.orbit-ring .r-orb:nth-child(7) { left: 142px; top: 17px; } .orbit-ring .r-orb:nth-child(8) { left: 171px; top: 17px; }
@keyframes orbit { from { transform: translate(-50%, -50%) rotate(0deg); } to { transform: translate(-50%, -50%) rotate(360deg); } }
@keyframes gold-pulse { 0%, 100% { box-shadow: 0 0 10px rgba(212,175,55,0.5); } 50% { box-shadow: 0 0 18px rgba(255,215,0,0.7); } }
.humanoid-core.humanoid-3d {
  position: absolute; left: 50%; top: 48%; width: 80px; height: 115px;
  transform: translate(-50%, -50%); z-index: 2;
  filter: drop-shadow(0 0 12px rgba(0,212,255,0.5)); border: 2px solid rgba(0,212,255,0.5); border-radius: 50%;
  animation: cyan-pulse 2.5s ease-in-out infinite;
}
@keyframes cyan-pulse { 0%, 100% { box-shadow: 0 0 15px rgba(0,212,255,0.4); } 50% { box-shadow: 0 0 25px rgba(0,212,255,0.7); } }
.humanoid-3d svg { width: 100%; height: 100%; }
.speech-wrap { position: absolute; left: 50%; top: 78%; transform: translate(-50%, -50%); width: 92%; z-index: 3; }
.speech-bubble { background: rgb(0,26,53); border: 2px solid rgb(212,175,55); border-radius: 10px; padding: 10px 12px; margin: 0; font-size: clamp(0.7rem, 2vw, 0.8rem); color: #e8eef4; }
#determinant-message { min-height: 28px; margin-top: 10px; padding: 8px 12px; border-radius: 8px; background: rgba(0,26,53,0.9); border: 1px solid rgb(212,175,55); font-size: 0.78rem; color: #e8eef4; }
.shimmer { color: rgb(212,175,55); animation: title-shimmer 2.2s ease-in-out infinite; }
@keyframes title-shimmer { 0%, 100% { color: rgb(184,134,11); } 50% { color: rgb(255,215,0); } }
.gold-border { border: 2px solid rgb(212,175,55); border-radius: 12px; background: linear-gradient(135deg, #001A35 0%, #000B1E 100%); }
"""


# ----- Build UI -----
demo = gr.Blocks(css=CSS, title="GCSLC Sovereign Command — African Wealth Cloud Gateway")
with demo:
    gr.HTML(
        "<div style='text-align:center; padding:12px 0;'>"
        "<h1 class='shimmer' style='font-size: clamp(1rem, 4vw, 1.3rem); margin:0 0 4px 0;'>Sovereign Command</h1>"
        f"<p style='font-size: clamp(0.85rem, 2.5vw, 0.95rem); color: rgb(212,175,55); margin:0;'>{TITLE_FULL}</p>"
        "</div>"
    )

    # 1. Kill-Shot: 5th Box front and center — $1.87 B/year, pulsing red
    gr.HTML(_kill_shot_html())

    gr.Markdown("---")

    # 2. Map of Authority — True Nigeria (36 state borders, Plotly choropleth) or fallback
    _fig = _nigeria_choropleth("Kogi")
    if _fig is not None:
        map_plot = gr.Plot(value=_fig, label="Map of Authority — Federal Republic of Nigeria (36 State Borders)")
        def update_map(s: str):
            return _nigeria_choropleth(s)
    else:
        map_plot = gr.HTML(value=_map_fallback_html(), label="Map of Authority — Federal Republic of Nigeria (36 State Borders)")
        def update_map(s: str):
            return _map_fallback_html()

    with gr.Row():
        for state in COAL_STATES:
            btn = gr.Button(state, variant="secondary", size="sm")
            btn.click(fn=lambda s=state: update_map(s), inputs=None, outputs=map_plot)

    gr.Markdown("---")

    # 3. 8R Humanoid Guardian (Navy & Gold, pulsing determinants)
    gr.HTML(_humanoid_block())

    gr.Markdown("---")

    # 4. Footer
    gr.HTML(f"""
    <div style='text-align:center; padding:20px 16px; border-top: 1px solid rgba(212,175,55,0.35);'>
      <p style='font-size: 0.9rem; font-weight: 600; color: rgb(212,175,55); margin:0 0 6px 0;'>{CHAIRMAN_SIGNATURE}</p>
      <p style='font-size: 0.85rem; color: #b8c4ce; margin:0 0 4px 0;'>CAC Registration: {CAC_REGISTRATION}</p>
      <p style='font-size: 0.78rem; color: #b8c4ce; margin:0;'>{TITLE_FULL}</p>
      <p style='font-size: 0.75rem; color: rgba(184,196,206,0.75); margin:8px 0 0 0;'>© GCSLC. African Wealth Cloud Gateway.</p>
    </div>
    """)


if __name__ == "__main__":
    demo.launch()
