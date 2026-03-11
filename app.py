"""
GCSLC Sovereign Command Center — VIDEO-CERTIFIED BASELINE (0:00–0:18)
Phase 1 Asset Hardening: Sovereign Radar (map_sovereign + diamonds), Guardian (guardian_final + breathing pulse).
"""
# Fix Gradio ImportError: huggingface_hub no longer exposes HfFolder
try:
    import huggingface_hub
    if not hasattr(huggingface_hub, "HfFolder"):
        class HfFolder:
            @staticmethod
            def get_token():
                try:
                    from huggingface_hub import get_token as _get
                    return _get()
                except Exception:
                    return None
            @staticmethod
            def save_token(token):
                try:
                    from huggingface_hub import set_token
                    set_token(token)
                except Exception:
                    pass
        setattr(huggingface_hub, "HfFolder", HfFolder)
except Exception:
    pass

import base64
import html
import os
from typing import Optional

import gradio as gr
import plotly.graph_objects as go

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")
CURSOR_ASSETS = os.path.join(os.path.expanduser("~"), ".cursor", "projects", "Users-user-Desktop-GCSLC-Sovereign-Gateway", "assets")

# --- Copy of constants from video-certified baseline ---
TITLE_FULL = "Galadiman Ruwa Center for Strategic Leadership and Communication (GCSLC - LTD/GTE)"
CHAIRMAN_SIGNATURE = "Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau), Chairman, GCSLC Strategic Command"
CAC_REGISTRATION = "176917792057"
HOOK_TEXT = (
    "(We believe everything is powered and anchored by The 8R Stealth Paradigm Convergence and its Determinants. "
    "Let's converge from the human world to the AI/Robotics world for you to understand.)"
)

COAL_STATES = ["Enugu", "Kogi", "Benue", "Nasarawa", "Gombe", "Delta", "Edo", "Anambra", "Plateau", "Oyo", "Ekiti", "Kwara", "Imo"]
STATE_RESERVES_MT = {"Enugu": 168.0, "Kogi": 223.0, "Benue": 85.0, "Nasarawa": 22.0, "Gombe": 62.0, "Delta": 45.0, "Edo": 38.0, "Anambra": 27.3, "Plateau": 22.0, "Oyo": 20.0, "Ekiti": 15.0, "Kwara": 18.0, "Imo": 18.0}

# Hard-coded (lat, lon) for Map of Authority — no GeoJSON
COORDS = [
    ("Enugu", 6.4, 7.5), ("Kogi", 7.8, 6.7), ("Benue", 7.3, 8.8), ("Gombe", 10.3, 11.2),
    ("Delta", 5.5, 5.9), ("Imo", 5.5, 7.1), ("Anambra", 6.2, 7.1), ("Edo", 6.5, 6.0),
    ("Plateau", 9.2, 9.5), ("Nasarawa", 8.5, 8.2), ("Oyo", 8.1, 3.6), ("Ekiti", 7.6, 5.3), ("Kwara", 8.8, 4.6),
]
BY_PRODUCT_GERMANIUM_USD = 8597
BY_PRODUCT_AMMONIA_MT = 430
BY_PRODUCT_SILICON_M = 6.50
DETERMINANTS_R = ["R1 Refine", "R2 Reset", "R3 Research", "R4 Restructure", "R5 Resuscitate", "R6 Revitalize", "R7 Re-engineer", "R8 Retain"]
DETERMINANT_STRATEGIC = {
    "R1 Refine": "Refine raw anthracite into high-value chemical feedstocks.",
    "R2 Reset": "Reset legacy energy dependencies. Sovereign data-center and AI infrastructure.",
    "R3 Research": "Research drives Germanium arbitrage. Core to Diamond Opportunity 2026.",
    "R4 Restructure": "Restructure asset deployment for Tier-III/IV hyperscale.",
    "R5 Resuscitate": "Resuscitate idle reserves into productive chemical nodes.",
    "R6 Revitalize": "Revitalize jobs and economic output.",
    "R7 Re-engineer": "Re-engineer logistics for Dubai Port and global arbitrage.",
    "R8 Retain": "Retain sovereign control over strategic reserves.",
}


def _b64(name):
    for p in (ROOT, ASSETS, CURSOR_ASSETS):
        path = os.path.join(p, name)
        if os.path.isfile(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
    return ""


B64_MEDALLION = _b64("medallion.png")
# Phase 1: Sovereign Radar map image; Guardian humanoid image
def _map_asset():
    for name, mime in [("map_sovereign.jpg", "jpeg"), ("map_sovereign.png", "png"), ("Screenshot_20260311_005856_CapCut-d2f96cb5-38be-4e56-8295-2f997503d052.png", "png")]:
        b = _b64(name)
        if b:
            return b, mime
    return "", ""

_B64_MAP, _MAP_MIME = _map_asset()
B64_MAP_SOVEREIGN = _B64_MAP
B64_GUARDIAN_HF = _b64("guardian_final.png") or _b64("Screenshot_20260311_181838_Gallery-ca931142-993a-40d4-a43b-a4c28e3e56e3.png") or _b64("guardian.png")


def _medallion_svg():
    return """<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="medG" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#5c4a00"/><stop offset="50%" style="stop-color:#D4AF37"/><stop offset="100%" style="stop-color:#FFD700"/></linearGradient></defs><circle cx="24" cy="24" r="22" fill="url(#medG)" stroke="#B8860B" stroke-width="2"/><text x="24" y="28" text-anchor="middle" fill="#0a1628" font-size="10" font-weight="700">GCSLC</text></svg>"""


# Nigeria bounds for overlay: lat 4–14, lon 2.5–15 (same as Plotly)
LAT_LO, LAT_HI = 4.0, 14.0
LON_LO, LON_HI = 2.5, 15.0

def _latlon_to_pct(lat: float, lon: float) -> tuple:
    """Map (lat, lon) to (left%, top%) for overlay on map image. North = low top."""
    left = (lon - LON_LO) / (LON_HI - LON_LO) * 100
    top = (LAT_HI - lat) / (LAT_HI - LAT_LO) * 100
    return (max(0, min(100, left)), max(0, min(100, top)))


def sovereign_radar_html() -> str:
    """Sovereign Radar: map_sovereign image with Golden Diamond markers. Hover: glow + Strategic Node text."""
    if not B64_MAP_SOVEREIGN:
        return ""
    markers_html = ""
    for name, lat, lon in COORDS:
        left, top = _latlon_to_pct(lat, lon)
        title = "Strategic Energy Potential: Equivalent to 4.2 Million GPU-Hours/Year (NVIDIA H100 Clusters)."
        markers_html += f'<div class="sovereign-diamond" style="left:{left}%;top:{top}%;" title="{html.escape(title)}" data-state="{html.escape(name)}"><span class="diamond-inner"></span><span class="diamond-tooltip">{html.escape(title)}</span></div>'
    return f"""
    <div class="sovereign-radar-wrap">
      <div class="sovereign-radar-bg" style="background-image:url('data:image/{_MAP_MIME};base64,{B64_MAP_SOVEREIGN}');"></div>
      <div class="sovereign-radar-markers">{markers_html}</div>
    </div>
    """


def build_map(highlight_state: Optional[str] = None):
    """Scatter-plot fallback: preserves visual authority (dark navy/teal) when map image not used."""
    lats = [c[1] for c in COORDS]
    lons = [c[2] for c in COORDS]
    names = [c[0] for c in COORDS]
    hover_line = "Strategic Energy Potential: Equivalent to 4.2 Million GPU-Hours/Year (NVIDIA H100 Clusters)."
    fig = go.Figure()
    fig.add_trace(
        go.Scattergeo(
            lon=lons, lat=lats,
            text=[hover_line.format(n) for n in names],
            hoverinfo="text", mode="markers",
            marker=dict(size=18, symbol="diamond", color="#D4AF37", line=dict(width=2, color="#FFD700")),
            name="Reserve",
        )
    )
    fig.update_geos(
        center=dict(lat=9.08, lon=8.0), scope="africa",
        showcountries=True, countrycolor="rgba(0,32,96,0.6)",
        showland=True, landcolor="rgba(0,31,63,0.4)",
        showocean=True, oceancolor="rgba(0,20,50,0.5)",
        lataxis=dict(range=[4, 14]), lonaxis=dict(range=[2.5, 15]),
    )
    fig.update_layout(
        margin=dict(r=0, t=0, l=0, b=0), height=380,
        paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e8eef4", size=12),
        hoverlabel=dict(bgcolor="#001f3f", bordercolor="#D4AF37"),
        showlegend=False,
    )
    return fig


def diamond_popup(state: str) -> str:
    reserves = STATE_RESERVES_MT.get(state, 0)
    return f"""
    <div class="diamond-popup diamond-opportunity-box gold-outline-block">
      <h4 class="shimmer">Diamond Opportunity — {state}</h4>
      <p class="reserves-line"><strong>Proven Reserves:</strong> {state}: <strong>{reserves:.0f}M Tonnes</strong></p>
      <div class="opportunity-card">
        <p class="byproduct-title">Market values</p>
        <div class="byproduct-grid byproduct-prominent">
          <span class="byproduct-item">Germanium: <strong class="val">${BY_PRODUCT_GERMANIUM_USD:,.0f}/kg</strong></span>
          <span class="byproduct-item">Ammonia: <strong class="val">${BY_PRODUCT_AMMONIA_MT:,.0f}/MT</strong></span>
          <span class="byproduct-item">Silicon: <strong class="val">${BY_PRODUCT_SILICON_M}M</strong> (monthly)</span>
        </div>
      </div>
    </div>
    """


def real_time_market_values_html() -> str:
    return f"""
    <div class="market-values heartbeat-wrap gold-outline-block">
      <h3 class="shimmer market-title">Real-Time Market Values — 5-Minute Heartbeat</h3>
      <p class="market-sub">Germanium, Silicon, Benzene, Rare Earths. March 2026. Glittering Pulse = Hot.</p>
      <div class="market-grid">
        <div class="mv-card mv-hot"><p class="mv-label">Germanium</p><p class="mv-price">$8,597/kg</p><p class="mv-caption">Optics, chips, sensors</p></div>
        <div class="mv-card mv-hot"><p class="mv-label">Silicon</p><p class="mv-price">$6,500/MT</p><p class="mv-caption">Solar, wafers, compute</p></div>
        <div class="mv-card"><p class="mv-label">Benzene</p><p class="mv-price">$950/MT</p><p class="mv-caption">Petrochem feedstock</p></div>
        <div class="mv-card"><p class="mv-label">Rare Earths</p><p class="mv-price">$120,000/kg</p><p class="mv-caption">Magnets, EV, defense</p></div>
      </div>
      <div class="opportunity-cost-box">
        <div class="opportunity-cost-inner">
          <span class="falcon-flap">&#9726;</span>
          <p class="opportunity-cost-label">Cumulative National Opportunity Cost</p>
          <p class="opportunity-cost-monthly">Monthly unrealized: $0.16 B</p>
          <p class="opportunity-cost-annual">Annual unrealized: $1.87 B</p>
          <p class="sovereign-warning">Sovereign Warning: Nigeria is losing $1.87 Billion annually in unrealized chemical wealth. ACT NOW.</p>
        </div>
      </div>
    </div>
    """


def convergence_metrics_html() -> str:
    return """
    <div class="convergence-metrics-wrap gold-outline-block">
      <h3 class="shimmer">Convergence Metrics — Monthly Projections</h3>
      <table class="metrics-table">
        <thead><tr><th>Commodity</th><th>Monthly Projection (USD M)</th></tr></thead>
        <tbody>
          <tr><td>Coal</td><td>$18.5M</td></tr>
          <tr><td>Germanium</td><td>$22.0M</td></tr>
          <tr><td>Silicon</td><td>$6.5M</td></tr>
          <tr><td><strong>Total</strong></td><td><strong>$47.0M</strong></td></tr>
        </tbody>
      </table>
    </div>
    """


def humanoid_svg():
    return """
    <svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="guardianNavy" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" style="stop-color:#0a1628"/><stop offset="50%" style="stop-color:#0d2137"/><stop offset="100%" style="stop-color:#001a33"/></linearGradient>
        <linearGradient id="burnishedGold" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" style="stop-color:#8B6914"/><stop offset="50%" style="stop-color:#D4AF37"/><stop offset="100%" style="stop-color:#B8860B"/></linearGradient>
        <filter id="depth"><feDropShadow dx="2" dy="2" stdDeviation="1" flood-color="#000"/></filter>
      </defs>
      <ellipse cx="50" cy="24" rx="20" ry="22" fill="url(#guardianNavy)" stroke="url(#burnishedGold)" stroke-width="2" filter="url(#depth)"/>
      <path fill="url(#guardianNavy)" stroke="url(#burnishedGold)" stroke-width="1.8" filter="url(#depth)" d="M32 48 L50 70 L68 48 L64 112 L36 112 Z"/>
      <rect x="38" y="70" width="14" height="48" rx="4" fill="url(#guardianNavy)" stroke="url(#burnishedGold)" filter="url(#depth)"/>
      <path fill="url(#guardianNavy)" stroke="url(#burnishedGold)" stroke-width="1.2" d="M68 48 L88 52 L92 58 L90 64 L70 60 Z"/>
      <g class="chemical-node"><ellipse cx="82" cy="58" rx="10" ry="8" fill="#1a2a2a" stroke="#00d4ff" stroke-width="1.5"/><ellipse cx="82" cy="58" rx="6" ry="5" fill="rgba(0,212,255,0.4)"/></g>
    </svg>
    """


def humanoid_block() -> str:
    """Phase 1: Guardian humanoid (guardian_final.png). No boxes/borders. Breathing pulse on coal glow. Institutional gold narrative."""
    if B64_GUARDIAN_HF:
        return f"""
        <div class="guardian-humanoid-wrap">
          <div class="guardian-humanoid-img guardian-breathing">
            <img src="data:image/png;base64,{B64_GUARDIAN_HF}" alt="8R Guardian" />
          </div>
          <p class="guardian-narrative">I NEED ENERGY TO THRIVE</p>
        </div>
        """
    orbs = "".join(
        f'<span class="r-orb" data-strategic="{html.escape(DETERMINANT_STRATEGIC.get(d, ""))}">{d}</span>'
        for d in DETERMINANTS_R
    )
    return f"""
    <div class="humanoid-block humanoid-frame gold-border">
      <p class="exhibit-label">8R Guardian — Humanoid with pulsing cyan core. Click a determinant.</p>
      <div class="aura-wrap">
        <div class="orbit-ring">{orbs}</div>
        <div class="humanoid-core humanoid-3d">{humanoid_svg()}</div>
        <div class="speech-wrap">
          <p class="speech-bubble">"I need energy to thrive; process the coal and its by-products—they're my power."</p>
        </div>
      </div>
      <div id="determinant-message" aria-live="polite">Click an 8R determinant to see strategic importance.</div>
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


def data_fortress_html() -> str:
    chips = "".join(f'<span class="reserve-chip">{s} {STATE_RESERVES_MT.get(s, 0):.0f}M</span>' for s in COAL_STATES[:8])
    chips += "".join(f'<span class="reserve-chip">{s} {STATE_RESERVES_MT.get(s, 0):.0f}M</span>' for s in COAL_STATES[8:])
    return f"""
    <div class="data-fortress-wrap desert-dragon prism-data-center gold-outline-block">
      <h3 class="shimmer data-fortress-title">Desert Dragon — Tier-III/IV Hyperscale</h3>
      <p class="data-fortress-sub">Riyadh/Dubai immersion-cooled prototype. GCSLC cyan liquid cooling. Barco-style video wall.</p>
      <div class="server-rack-wrap">
        <svg class="server-rack-svg" viewBox="0 0 260 140" xmlns="http://www.w3.org/2000/svg">
          <defs><linearGradient id="rackGrad" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" style="stop-color:rgb(10,22,40)"/><stop offset="100%" style="stop-color:rgb(0,26,53)"/></linearGradient></defs>
          <rect x="10" y="8" width="240" height="124" rx="4" fill="url(#rackGrad)" class="rack-stroke"/>
          <line x1="10" y1="36" x2="250" y2="36" class="pipe-cyan"/><line x1="10" y1="64" x2="250" y2="64" class="pipe-cyan"/><line x1="10" y1="92" x2="250" y2="92" class="pipe-cyan"/>
          <path d="M0 70 L20 70 L20 50 L260 50 L260 70" fill="none" class="pipe-cyan" stroke-width="2"/>
          <circle class="glitter-dot g-1" cx="50" cy="22" r="2"/><circle class="glitter-dot g-2" cx="120" cy="50" r="2"/><circle class="glitter-dot g-3" cx="190" cy="78" r="2"/><circle class="glitter-dot g-4" cx="80" cy="106" r="2"/><circle class="glitter-dot g-5" cx="200" cy="22" r="2"/>
          <rect x="14" y="40" width="70" height="20" rx="2" fill="rgba(0,0,0,0.4)" class="video-wall"/><text x="49" y="53" text-anchor="middle" class="video-wall-text">BARCO</text>
        </svg>
        <div class="gen-gemini-core"><span class="gen-gemini-label">GEN-GEMINI-AI</span></div>
      </div>
      <div class="state-reserves-bar">State reserves (M tonnes): {chips}</div>
    </div>
    """


def arbitrage_pulse_html() -> str:
    ticker_line = "NATIONAL ASSET RECOVERY DELAY COST: $1.87 BILLION/YEAR LOSS — RECOVERING VIA 8R STEALTH PARADIGM."
    return f"""
    <div class="arbitrage-pulse-wrap">
      <div class="arbitrage-pulse-inner">
        <span class="arbitrage-pulse-text">{ticker_line}</span>
        <span class="arbitrage-pulse-sep">&#9670;</span>
        <span class="arbitrage-pulse-text">{ticker_line}</span>
        <span class="arbitrage-pulse-sep">&#9670;</span>
      </div>
    </div>
    """


def footer_html() -> str:
    return f"""
    <div class="footer-block-wrap">
      <div class="blue-wave-overlay"><svg class="wave-svg" viewBox="0 0 1200 80" preserveAspectRatio="none"><path class="wave-path" d="M0,40 Q300,20 600,40 T1200,40 L1200,80 L0,80 Z" fill="rgba(0,212,255,0.12)"/></svg></div>
      <div class="footer-block">
        <p class="signature">{CHAIRMAN_SIGNATURE}</p>
        <p class="cac">CAC Registration: {CAC_REGISTRATION}</p>
        <p class="legal">{TITLE_FULL}</p>
        <p class="copy">© GCSLC. Proprietary.</p>
      </div>
    </div>
    """


# ---- CSS: Dark Navy/Carbon, gold-outline blocks, watermark, Sovereign Command header ----
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
.gradio-container, body, .main, .container, #root, .block, section {
  background: linear-gradient(135deg, #050508 0%, #0a0a18 50%, #050510 100%) !important;
  color: #e0e0e0 !important;
  font-family: Orbitron, sans-serif !important;
}
.gradio-container {
  border: 2px solid rgba(0, 212, 255, 0.5);
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.3), inset 0 0 60px rgba(0, 212, 255, 0.03);
}
.gradio-container .block { background: transparent !important; border: none !important; }

/* Gold-outlined data blocks */
.gold-outline-block {
  border: 2px solid #D4AF37 !important;
  border-radius: 12px;
  background: linear-gradient(135deg, #001A35 0%, #000B1E 100%);
  padding: 16px;
  margin: 14px 0;
  box-shadow: 0 0 14px rgba(212, 175, 55, 0.25);
}

/* Diagonal watermark */
.gradio-container::before {
  content: "GCSLC PROPRIETARY";
  position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-22deg);
  font-size: clamp(1.8rem, 4vw, 3.2rem); font-weight: 700; letter-spacing: 0.2em;
  color: rgba(212, 175, 55, 0.08); z-index: 9998; pointer-events: none;
}

/* Medallion + Sovereign Command header */
#medallion, .gcslc-medallion {
  text-align: center;
  background: radial-gradient(circle, #d4af37 0%, #1a1a0a 50%, #000 70%) !important;
  box-shadow: 0 0 25px #d4af37;
  display: flex; align-items: center; justify-content: center;
  color: black; font-weight: bold;
  animation: pulse 3s infinite;
}
@keyframes pulse { 0% { transform: scale(1); opacity: 0.8; } 50% { transform: scale(1.1); opacity: 1; } 100% { transform: scale(1); opacity: 0.8; } }
.gcslc-medallion { position: relative !important; width: 64px; height: 64px; margin: 0 auto 10px auto; border-radius: 50%; border: 3px solid #D4AF37; padding: 4px; }
.gcslc-medallion img { width: 100%; height: 100%; border-radius: 50%; }
@keyframes title-shimmer { 0%, 100% { color: #B8860B; text-shadow: 0 0 12px #D4AF37; } 50% { color: #FFD700; text-shadow: 0 0 20px #FFD700; } }
.title-shimmer, .shimmer { animation: title-shimmer 2.2s ease-in-out infinite; color: #D4AF37; }
.header-area { padding: 8px 0 12px 0; text-align: center; }
.gold-border { border: 2px solid #D4AF37; border-radius: 12px; background: linear-gradient(135deg, #001A35 0%, #000B1E 100%); }

/* Real-Time Market Values */
.market-values, .heartbeat-wrap { margin: 18px 0; text-align: center; }
.market-title { font-size: 0.95rem; margin-bottom: 6px; }
.market-sub { font-size: 0.78rem; color: #b8c4ce; margin: 0 0 10px 0; }
.market-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; max-width: 640px; margin: 0 auto; }
.mv-card { border: 1px solid rgba(0, 212, 255, 0.5); border-radius: 10px; padding: 10px 12px; background: radial-gradient(circle at top, rgba(0,212,255,0.12) 0%, #02030a 55%, #010107 100%); box-shadow: 0 0 10px rgba(0, 212, 255, 0.25); }
.mv-card.mv-hot { animation: mv-glitter-pulse 3.2s ease-in-out infinite; }
.mv-card .mv-label { font-size: 0.8rem; color: #D4AF37; margin: 0 0 4px 0; }
.mv-card .mv-price { font-size: 0.95rem; font-weight: 700; color: #00d4ff; margin: 0 0 4px 0; }
.mv-card .mv-caption { font-size: 0.72rem; color: #b8c4ce; margin: 0; }
@keyframes mv-glitter-pulse { 0%, 100% { box-shadow: 0 0 6px rgba(0,212,255,0.35); } 50% { box-shadow: 0 0 16px rgba(0,212,255,0.85); } }
.opportunity-cost-box { margin-top: 16px; padding: 18px; border-radius: 12px; border: 2px solid rgba(212,175,55,0.8); background: linear-gradient(135deg, rgba(0,26,53,0.95) 0%, rgba(0,11,30,0.98) 100%); text-align: center; }
.opportunity-cost-label { font-size: 0.9rem; color: #D4AF37; margin: 0 0 8px 0; font-weight: 600; }
.opportunity-cost-monthly, .opportunity-cost-annual { font-size: 1rem; color: #00d4ff; margin: 4px 0; }
.falcon-flap { display: inline-block; font-size: 2rem; margin: 8px 0; }
.sovereign-warning { font-size: 0.88rem; font-weight: 700; margin: 12px 0 0 0; color: rgba(255,80,80,1); }

/* Convergence Metrics */
.convergence-metrics-wrap { margin: 20px 0; }
.convergence-metrics-wrap h3 { margin: 0 0 12px 0; font-size: 1rem; }
.metrics-table { width: 100%; border-collapse: collapse; color: #e8eef4; font-size: 0.9rem; }
.metrics-table th, .metrics-table td { padding: 10px 16px; text-align: left; border-bottom: 1px solid rgba(212,175,55,0.3); }
.metrics-table th { color: #D4AF37; }
.metrics-table td:last-child { text-align: right; color: #D4AF37; }

/* Map of Authority */
.map-wrap { padding: 20px; text-align: center; }
.map-sub { color: #b8c4ce; font-size: 0.9rem; margin: 8px 0 12px 0; }

/* Sovereign Radar: map image + Golden Diamond markers, hover glow + tooltip */
.sovereign-radar-wrap { position: relative; width: 100%; max-width: 560px; margin: 0 auto; min-height: 380px; border-radius: 12px; overflow: hidden; border: 1px solid rgba(0,212,255,0.35); }
.sovereign-radar-bg { position: absolute; inset: 0; background-size: contain; background-position: center; background-repeat: no-repeat; background-color: #001f3f; }
.sovereign-radar-markers { position: absolute; inset: 0; pointer-events: none; }
.sovereign-diamond { position: absolute; width: 24px; height: 24px; margin: -12px 0 0 -12px; pointer-events: auto; cursor: pointer; transform: translate(-50%, -50%); transition: filter 0.25s, transform 0.2s; }
.sovereign-diamond:hover { filter: drop-shadow(0 0 12px #FFD700) drop-shadow(0 0 20px rgba(255,215,0,0.8)); transform: translate(-50%, -50%) scale(1.2); z-index: 5; }
.diamond-inner { display: block; width: 100%; height: 100%; background: #D4AF37; border: 2px solid #FFD700; transform: rotate(45deg); box-shadow: 0 0 8px rgba(212,175,55,0.6); }
.sovereign-diamond .diamond-tooltip { position: absolute; left: 50%; bottom: 100%; transform: translate(-50%, -8px); white-space: nowrap; background: #001f3f; color: #D4AF37; border: 1px solid #D4AF37; padding: 6px 10px; font-size: 0.75rem; border-radius: 6px; opacity: 0; pointer-events: none; transition: opacity 0.2s; box-shadow: 0 4px 12px rgba(0,0,0,0.6); }
.sovereign-diamond:hover .diamond-tooltip { opacity: 1; white-space: normal; max-width: 280px; }
/* When Sovereign Radar image is shown, hide the Plotly fallback */
body:has(.sovereign-radar-wrap) #sovereign-map-plot { display: none !important; }

/* Guardian Humanoid: no box/border; breathing pulse (coal glow); institutional gold narrative */
.guardian-humanoid-wrap { text-align: center; padding: 0; margin: 0; background: transparent; border: none; box-shadow: none; }
.guardian-humanoid-img { margin: 0 auto; max-width: 100%; line-height: 0; }
.guardian-humanoid-img img { max-width: 100%; height: auto; display: block; margin: 0 auto; }
@keyframes guardian-breathing { 0%, 100% { filter: brightness(1) drop-shadow(0 0 8px rgba(255,140,0,0.4)); } 50% { filter: brightness(1.08) drop-shadow(0 0 18px rgba(255,165,0,0.7)); } }
.guardian-breathing { animation: guardian-breathing 3s ease-in-out infinite; }
.guardian-narrative { color: #D4AF37; font-size: 1rem; font-weight: 700; letter-spacing: 0.08em; margin: 12px 0 0 0; text-shadow: 0 0 12px rgba(212,175,55,0.6); }

.diamond-popup { padding: 18px; margin: 12px 0; }
.diamond-opportunity-box .opportunity-card { background: #0d1117; border: 2px solid #00d4ff; border-radius: 10px; padding: 14px; margin: 10px 0; }
.byproduct-title { color: #D4AF37; font-weight: 600; }
.byproduct-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px; }
.byproduct-item { color: #b8c4ce; font-size: 0.9rem; }
.byproduct-prominent .val { color: #00d4ff !important; }
.reserves-line { margin: 8px 0; color: #e8eef4; }
.state-btn { min-width: 96px; border: 2px solid #D4AF37 !important; color: #D4AF37 !important; background: rgba(0,26,53,0.9) !important; font-weight: 600 !important; animation: gold-pulse 2s ease-in-out infinite !important; }
@keyframes gold-pulse { 0%, 100% { box-shadow: 0 0 10px rgba(212,175,55,0.5); } 50% { box-shadow: 0 0 18px #FFD700; } }

/* 8R Guardian */
.humanoid-frame { border: 2px solid rgba(0,255,204,0.6); border-radius: 15px; padding: 15px; background: rgba(0, 255, 204, 0.05); box-shadow: 0 0 15px rgba(0, 255, 204, 0.3); text-align: center; }
.humanoid-block { padding: 24px; }
.exhibit-label { color: #B8860B; font-size: 0.85rem; margin-bottom: 12px; }
.aura-wrap { position: relative; width: 260px; height: 260px; margin: 0 auto; }
.orbit-ring { position: absolute; left: 50%; top: 50%; width: 200px; height: 200px; animation: orbit 22s linear infinite; transform-origin: center center; }
.orbit-ring .r-orb { position: absolute; padding: 4px 8px; border-radius: 18px; font-size: 0.62rem; font-weight: 600; background: rgba(0,26,53,0.95); border: 1px solid #D4AF37; color: #D4AF37; white-space: nowrap; cursor: pointer; animation: gold-pulse 2.2s ease-in-out infinite; }
.orbit-ring .r-orb:nth-child(1) { left: 171px; top: 88px; }.orbit-ring .r-orb:nth-child(2) { left: 142px; top: 159px; }.orbit-ring .r-orb:nth-child(3) { left: 71px; top: 188px; }.orbit-ring .r-orb:nth-child(4) { left: 0; top: 159px; }
.orbit-ring .r-orb:nth-child(5) { left: 0; top: 88px; }.orbit-ring .r-orb:nth-child(6) { left: 71px; top: 0; }.orbit-ring .r-orb:nth-child(7) { left: 142px; top: 17px; }.orbit-ring .r-orb:nth-child(8) { left: 171px; top: 17px; }
@keyframes orbit { from { transform: translate(-50%, -50%) rotate(0deg); } to { transform: translate(-50%, -50%) rotate(360deg); } }
@keyframes cyan-core-pulse { 0%, 100% { box-shadow: 0 0 15px rgba(0, 212, 255, 0.4); } 50% { box-shadow: 0 0 25px rgba(0, 212, 255, 0.7); } }
.humanoid-core.humanoid-3d { position: absolute; left: 50%; top: 48%; width: 80px; height: 115px; transform: translate(-50%, -50%); z-index: 2; filter: drop-shadow(0 0 12px rgba(0,43,91,0.8)); border-radius: 50%; animation: cyan-core-pulse 2.5s ease-in-out infinite; border: 2px solid rgba(0, 212, 255, 0.5); }
.humanoid-3d svg { width: 100%; height: 100%; }
@keyframes coal-glow { 0% { opacity: 0.7; } 100% { opacity: 1; } }
.chemical-node { animation: coal-glow 2s infinite alternate; }
.speech-wrap { position: absolute; left: 50%; top: 78%; transform: translate(-50%, -50%); width: 92%; z-index: 3; }
.speech-bubble { background: #001A35; border: 2px solid #D4AF37; border-radius: 10px; padding: 10px 12px; margin: 0; font-size: 0.8rem; color: #e8eef4; line-height: 1.35; }
#determinant-message { min-height: 28px; margin-top: 10px; padding: 8px 12px; border-radius: 8px; background: rgba(0,26,53,0.9); border: 1px solid #D4AF37; font-size: 0.78rem; color: #e8eef4; }

/* Desert Dragon */
.data-fortress-wrap { margin: 20px 0; text-align: center; }
.data-fortress-title { margin-bottom: 6px; font-size: 1rem; }
.data-fortress-sub { font-size: 0.78rem; color: rgba(0,212,255,0.9); margin: 0 0 12px 0; }
.prism-data-center { border: 1px solid rgba(0,212,255,0.4); border-radius: 12px; padding: 16px; box-shadow: 0 0 16px rgba(0,212,255,0.25); }
.server-rack-wrap { position: relative; display: inline-block; padding: 20px; }
.server-rack-svg { width: 100%; max-width: 320px; height: auto; display: block; }
@keyframes glitter { 0%, 100% { opacity: 0.4; } 50% { opacity: 1; } }
.glitter-dot { animation: glitter 2s ease-in-out infinite; fill: #00d4ff; }
.glitter-dot.g-2, .glitter-dot.g-4 { fill: #D4AF37; }
.desert-dragon .rack-stroke { stroke: rgba(0,212,255,0.7); }
.desert-dragon .pipe-cyan { stroke: rgba(0,212,255,0.85); stroke-width: 1.5; }
.video-wall { stroke: rgba(0,212,255,0.5); }
.video-wall-text { fill: rgba(0,212,255,0.9); font-size: 10px; font-weight: 700; }
.gen-gemini-core { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%); width: 100px; height: 44px; display: flex; align-items: center; justify-content: center; background: radial-gradient(circle, rgba(0,212,255,0.25) 0%, rgba(0,26,53,0.9) 70%); border: 2px solid rgba(0,212,255,0.6); border-radius: 12px; animation: cyan-core-pulse 2.5s ease-in-out infinite; z-index: 2; }
.gen-gemini-label { font-size: 0.65rem; font-weight: 700; color: #00d4ff; letter-spacing: 0.08em; }
.state-reserves-bar { margin-top: 14px; padding: 10px 12px; border-radius: 8px; background: rgba(0,10,25,0.9); display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; }
.reserve-chip { font-size: 0.75rem; font-weight: 600; color: rgb(184,134,11); background: rgba(184,134,11,0.15); border: 1px solid rgba(184,134,11,0.7); padding: 4px 10px; border-radius: 20px; white-space: nowrap; }

/* Arbitrage pulse */
.arbitrage-pulse-wrap { width: 100%; overflow: hidden; padding: 10px 0; background: rgba(0,26,53,0.9); border-top: 1px solid rgba(212,175,55,0.4); border-bottom: 1px solid rgba(212,175,55,0.4); margin: 16px 0 0 0; }
.arbitrage-pulse-inner { display: inline-block; white-space: nowrap; animation: arbitrage-scroll 30s linear infinite; padding-left: 100%; }
@keyframes arbitrage-scroll { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
.arbitrage-pulse-text { color: #D4AF37; font-size: 0.9rem; font-weight: 600; }
.arbitrage-pulse-sep { color: rgba(212,175,55,0.6); margin: 0 12px; }

/* Footer */
.footer-block-wrap { position: relative; margin-top: 24px; overflow: hidden; }
.blue-wave-overlay { position: absolute; bottom: 0; left: 0; right: 0; height: 80px; pointer-events: none; }
.blue-wave-overlay .wave-svg { width: 100%; height: 100%; display: block; }
.blue-wave-overlay .wave-path { animation: wave-flow 10s linear infinite; }
@keyframes wave-flow { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
.footer-block { position: relative; z-index: 1; text-align: center; padding: 20px 16px; border-top: 1px solid rgba(212,175,55,0.35); }
.signature { font-size: 0.9rem; font-weight: 600; color: #D4AF37; margin: 0 0 6px 0; }
.cac { font-size: 0.85rem; color: #b8c4ce; margin: 0 0 4px 0; }
.legal { font-size: 0.78rem; color: #b8c4ce; margin: 0 0 4px 0; }
.copy { font-size: 0.75rem; color: rgba(184,196,206,0.75); margin: 0; }
"""


SHIELD_SCRIPT = """
<script>
document.addEventListener('contextmenu', function(e) { e.preventDefault(); }, true);
document.addEventListener('keydown', function(e) {
  var k = (e.key || '').toLowerCase();
  if ((e.metaKey && e.shiftKey && k === '4') || (e.metaKey && k === 's')) { e.preventDefault(); e.stopPropagation(); }
}, true);
</script>
"""


# ---- Build UI: order as in video 0:00–0:18 ----
demo = gr.Blocks(css=CSS, title="GCSLC Sovereign Command")
with demo:
    gr.HTML(
        '<div class="gcslc-watermark" aria-hidden="true"></div>'
        '<script>document.addEventListener("contextmenu", function(e){ e.preventDefault(); });</script>'
    )
    gr.HTML(SHIELD_SCRIPT)

    # 1. Medallion + Sovereign Command header (shimmering gold)
    medallion_content = f'<img src="data:image/png;base64,{B64_MEDALLION}" alt="GCSLC Seal" />' if B64_MEDALLION else _medallion_svg()
    gr.HTML(
        '<div id="medallion" class="gcslc-medallion" aria-label="GCSLC Seal">' + medallion_content + '</div>'
        + '<div class="header-area">'
        + "<h1 class='title-shimmer sovereign-title' style='text-align: center; font-size: 1.1rem; margin: 0 0 6px 0;'>Sovereign Command</h1>"
        + f"<p class='title-full' style='text-align: center; font-size: 0.95rem; margin: 0 0 8px 0; color: #D4AF37;'>{TITLE_FULL}</p>"
        + "<p class='strategic-header' style='text-align: center; font-size: 0.9rem; margin: 0 0 12px 0; color: #D4AF37; font-weight: 600;'>NVIDIA &amp; Microsoft: The 8R Stealth Paradigm is the bridge between Nigerian Energy Sovereignty and Global AI Dominance.</p>"
        + "</div>"
        + f"<p class='hook' style='text-align: center; font-size: 0.92rem; max-width: 700px; margin: 0 auto 20px auto; color: #e8eef4;'>{HOOK_TEXT}</p>"
    )

    # 2. Real-Time Market Values (gold-outlined block)
    gr.HTML(real_time_market_values_html())

    # 3. Convergence Metrics (gold-outlined block)
    gr.HTML(convergence_metrics_html())

    # 4. Map of Authority — Sovereign Radar (image + diamonds) or Scattergeo fallback
    gr.HTML(sovereign_radar_html())  # when map asset exists: image + Golden Diamond overlays; else empty
    map_plot = gr.Plot(value=build_map(), label="Map of Authority — Federal Republic of Nigeria (13 Coal States)", elem_id="sovereign-map-plot")
    with gr.Row():
        state_btns = [gr.Button(s, elem_classes=["state-btn"], variant="secondary") for s in COAL_STATES]
    popup_out = gr.HTML(value=diamond_popup("Kogi"), label="Diamond Opportunity")

    for i, state in enumerate(COAL_STATES):
        state_btns[i].click(
            fn=lambda s=state: (diamond_popup(s), build_map(s)),
            inputs=None,
            outputs=[popup_out, map_plot],
        )

    # 5. Desert Dragon wireframe
    gr.HTML(data_fortress_html())

    gr.Markdown("---")

    # 6. 8R Guardian schematic
    gr.HTML(humanoid_block())

    gr.Markdown("---")

    # 7. Arbitrage pulse ticker
    gr.HTML(arbitrage_pulse_html())

    # 8. Footer
    gr.HTML(footer_html())


if __name__ == "__main__":
    try:
        demo.launch(server_name="0.0.0.0", server_port=7865, share=True)
    except OSError:
        demo.launch(server_name="0.0.0.0", server_port=0, share=True)
