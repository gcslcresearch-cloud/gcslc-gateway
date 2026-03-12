"""
GCSLC Sovereign Command Center — SOVEREIGN COMMAND CENTER BASELINE
Restored to match institutional density and layout of the original GCSLC dashboard video.
Layout: Header → Real-Time Market Values (4 boxes) → Map of Authority (map + 13 diamond buttons) → Data Fortress (3x3 grid) → National Impact → 8R Guardian → Footer.
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
REVENUE_POTENTIAL_B = 125.8
AI_PROCESSING_POWER = "4.2M GPU-Hours"
JOBS_CREATED = "1,203 MW Corridor"

BY_PRODUCT_GERMANIUM_USD = 8597
NODE_TOOLTIP = "Potential: 4.2M GPU-Hours (NVIDIA H100 Equivalent)."
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
B64_FALCON = _b64("falcon_final.png") or _b64("falcon.png")
B64_GUARDIAN_HF = _b64("guardian_final.png") or _b64("Screenshot_20260311_181838_Gallery-ca931142-993a-40d4-a43b-a4c28e3e56e3.png") or _b64("guardian.png")
B64_FORTRESS = _b64("fortress_final.png") or _b64("fortress.png")


def _medallion_svg():
    return """<svg viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="medG" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#5c4a00"/><stop offset="50%" style="stop-color:#D4AF37"/><stop offset="100%" style="stop-color:#FFD700"/></linearGradient></defs><circle cx="24" cy="24" r="22" fill="url(#medG)" stroke="#B8860B" stroke-width="2"/><text x="24" y="28" text-anchor="middle" fill="#0a1628" font-size="10" font-weight="700">GCSLC</text></svg>"""


def map_of_authority_html() -> str:
    """Map of Authority: clean dark navy center map with falcon_final.png tactical dive overlay."""
    falcon = ""
    if B64_FALCON:
        falcon = f"""
    <div class="falcon-tactical-overlay falcon-glide" aria-hidden="true">
      <img src="data:image/png;base64,{B64_FALCON}" alt="Falcon" />
    </div>"""
    return f"""
    <div class="map-of-authority-wrap">
      <div class="map-of-authority-center"></div>
      {falcon}
    </div>
    """


def falcon_overlay_html() -> str:
    """Falcon tactical dive animation over the map."""
    if not B64_FALCON:
        return ""
    return f"""
    <div class="falcon-tactical-overlay falcon-glide" aria-hidden="true">
      <img src="data:image/png;base64,{B64_FALCON}" alt="Falcon" />
    </div>
    """


def diamond_popup(state: str) -> str:
    reserves = STATE_RESERVES_MT.get(state, 0)
    return f"""
    <div class="diamond-popup diamond-opportunity-box gold-outline-block">
      <h4 class="shimmer">Diamond Opportunity — {state}</h4>
      <p class="reserves-line"><strong>{NODE_TOOLTIP}</strong></p>
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
    """Real-Time Market Values — 4 distinct gold-outlined glass boxes."""
    return """
    <div class="market-values gold-glass-block">
      <h3 class="shimmer market-title">Real-Time Market Values</h3>
      <p class="market-sub">Germanium, Silicon, Benzene, Rare Earths. March 2026.</p>
      <div class="market-grid four-boxes">
        <div class="mv-card gold-glass"><p class="mv-label">Germanium</p><p class="mv-price">$8,597/kg</p><p class="mv-caption">Optics, chips, sensors</p></div>
        <div class="mv-card gold-glass"><p class="mv-label">Silicon</p><p class="mv-price">$6,500/MT</p><p class="mv-caption">Solar, wafers, compute</p></div>
        <div class="mv-card gold-glass"><p class="mv-label">Benzene</p><p class="mv-price">$950/MT</p><p class="mv-caption">Petrochem feedstock</p></div>
        <div class="mv-card gold-glass"><p class="mv-label">Rare Earths</p><p class="mv-price">$120,000/kg</p><p class="mv-caption">Magnets, EV, defense</p></div>
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
    """8R Humanoid Guardian: guardian_final.png, pulsing core, I NEED ENERGY TO THRIVE narrative."""
    if B64_GUARDIAN_HF:
        return f"""
        <div class="guardian-baseline gold-glass-block">
          <h3 class="shimmer">8R Humanoid Guardian</h3>
          <div class="guardian-pulse-wrap">
            <div class="guardian-humanoid-img guardian-breathing">
              <img src="data:image/png;base64,{B64_GUARDIAN_HF}" alt="8R Guardian" />
            </div>
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


def data_fortress_3x3_html() -> str:
    """The GCSLC Data Fortress — 3x3 grid: AI Processing Power, Jobs Created, Revenue Potential. fortress_final.png."""
    img_block = ""
    if B64_FORTRESS:
        img_block = f'<div class="fortress-img-wrap"><img src="data:image/png;base64,{B64_FORTRESS}" alt="GCSLC Data Fortress" /></div>'
    return f"""
    <div class="data-fortress-section gold-glass-block">
      <h3 class="shimmer">The GCSLC Data Fortress</h3>
      {img_block}
      <div class="fortress-grid-3x3">
        <div class="fortress-cell gold-glass"><p class="fortress-cell-label">AI Processing Power</p><p class="fortress-cell-value">{AI_PROCESSING_POWER}</p></div>
        <div class="fortress-cell gold-glass"><p class="fortress-cell-label">Jobs Created</p><p class="fortress-cell-value">{JOBS_CREATED}</p></div>
        <div class="fortress-cell gold-glass"><p class="fortress-cell-label">Revenue Potential</p><p class="fortress-cell-value">${REVENUE_POTENTIAL_B}B</p></div>
        <div class="fortress-cell gold-glass"><p class="fortress-cell-label">Coal Reserves</p><p class="fortress-cell-value">639.3 M MT</p></div>
        <div class="fortress-cell gold-glass"><p class="fortress-cell-label">Power Corridor</p><p class="fortress-cell-value">1,203 MW</p></div>
        <div class="fortress-cell gold-glass"><p class="fortress-cell-label">8R Paradigm</p><p class="fortress-cell-value">Active</p></div>
        <div class="fortress-cell gold-glass"><p class="fortress-cell-label">Germanium</p><p class="fortress-cell-value">${BY_PRODUCT_GERMANIUM_USD:,}/kg</p></div>
        <div class="fortress-cell gold-glass"><p class="fortress-cell-label">Liquid Cooling</p><p class="fortress-cell-value">Cyan Active</p></div>
        <div class="fortress-cell gold-glass"><p class="fortress-cell-label">Sovereign Lock</p><p class="fortress-cell-value">95%</p></div>
      </div>
    </div>
    """


def arbitrage_pulse_html() -> str:
    """Bloomberg-style scrolling red/gold bar."""
    ticker_line = "NATIONAL ASSET RECOVERY DELAY COST: $1.87 BILLION/YEAR LOSS"
    return f"""
    <div class="bloomberg-ticker-wrap">
      <div class="bloomberg-ticker-inner">
        <span class="bloomberg-ticker-text">{ticker_line}</span>
        <span class="bloomberg-ticker-sep">&#9670;</span>
        <span class="bloomberg-ticker-text">{ticker_line}</span>
        <span class="bloomberg-ticker-sep">&#9670;</span>
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


# ---- CSS: BASELINE — Dark Navy-to-Charcoal #050a15, ghost-white watermark, 1px gold glassmorphism ----
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
.gradio-container, body, .main, .container, #root, .block, section {
  background: linear-gradient(180deg, #050a15 0%, #0a1225 50%, #050a15 100%) !important;
  color: #e0e0e0 !important;
  font-family: Orbitron, sans-serif !important;
}
.gradio-container {
  border: 1px solid #D4AF37;
  box-shadow: 0 0 20px rgba(212, 175, 55, 0.2);
}
.gradio-container .block { background: transparent !important; border: none !important; }

/* GCSLC PROPRIETARY — large diagonal ghost-white watermark */
.gradio-container::before {
  content: "GCSLC PROPRIETARY";
  position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-22deg);
  font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 700; letter-spacing: 0.25em;
  color: rgba(255, 255, 255, 0.08); z-index: 9998; pointer-events: none;
}

/* Gold Glassmorphism: all containers 1px solid #D4AF37 */
.gold-glass-block, .gold-outline-block {
  border: 1px solid #D4AF37 !important;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(10, 22, 45, 0.7) 0%, rgba(5, 10, 21, 0.9) 100%);
  padding: 16px;
  margin: 14px 0;
  backdrop-filter: blur(8px);
}
.gold-glass { border: 1px solid #D4AF37 !important; border-radius: 10px; background: rgba(5, 10, 21, 0.6); }

/* Medallion + Sovereign Command header */
/* Gold Medallion top-center + Institutional title Bold Shimmering Gold */
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
.sovereign-title { font-weight: 800 !important; animation: title-shimmer 2.2s ease-in-out infinite; color: #FFD700 !important; }
.header-area { padding: 8px 0 12px 0; text-align: center; }
.gold-border { border: 2px solid #D4AF37; border-radius: 12px; background: linear-gradient(135deg, #0a1225 0%, #050a15 100%); }

/* Real-Time Market Values — 4 distinct gold-outlined glass boxes */
.market-values { margin: 18px 0; text-align: center; }
.market-title { font-size: 0.95rem; margin-bottom: 6px; }
.market-sub { font-size: 0.78rem; color: #b8c4ce; margin: 0 0 10px 0; }
.market-grid.four-boxes { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; max-width: 720px; margin: 0 auto; }
@media (max-width: 640px) { .market-grid.four-boxes { grid-template-columns: repeat(2, 1fr); } }
.mv-card.gold-glass { border: 1px solid #D4AF37 !important; border-radius: 10px; padding: 14px 12px; background: rgba(5, 10, 21, 0.7); }
.mv-card .mv-label { font-size: 0.8rem; color: #D4AF37; margin: 0 0 4px 0; font-weight: 600; }
.mv-card .mv-price { font-size: 0.95rem; font-weight: 700; color: #00d4ff; margin: 0 0 4px 0; }
.mv-card .mv-caption { font-size: 0.72rem; color: #b8c4ce; margin: 0; }

/* Map of Authority — clean dark navy center map + falcon overlay */
.map-section-title { text-align: center; margin: 16px 0 8px 0; }
.map-of-authority-wrap { position: relative; min-height: 320px; margin: 12px 0; border: 1px solid #D4AF37; border-radius: 12px; overflow: hidden; }
.map-of-authority-center { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(135deg, #0a1628 0%, #050a15 100%); }
.falcon-tactical-overlay { position: absolute !important; top: 0; left: 0; right: 0; bottom: 0; pointer-events: none; z-index: 10; display: flex; align-items: center; justify-content: center; }
.falcon-tactical-overlay img { width: 52px; height: 52px; object-fit: contain; }
.falcon-glide img { animation: falcon-tactical-glide 3.5s ease-in-out infinite; }
@keyframes falcon-tactical-glide { 0% { transform: translate(-80%, -60%) scale(1); opacity: 0.85; } 35% { transform: translate(0, 0) scale(1.1); opacity: 1; } 70% { transform: translate(40%, 30%) scale(1); opacity: 0.9; } 100% { transform: translate(-80%, -60%) scale(1); opacity: 0.85; } }

/* Convergence Metrics */
.convergence-metrics-wrap { margin: 20px 0; }
.convergence-metrics-wrap h3 { margin: 0 0 12px 0; font-size: 1rem; }
.metrics-table { width: 100%; border-collapse: collapse; color: #e8eef4; font-size: 0.9rem; }
.metrics-table th, .metrics-table td { padding: 10px 16px; text-align: left; border-bottom: 1px solid rgba(212,175,55,0.3); }
.metrics-table th { color: #D4AF37; }
.metrics-table td:last-child { text-align: right; color: #D4AF37; }

/* D2 Sovereign Radar Grid: 4x4 dark-navy container, Golden Diamond buttons */
.radar-grid-label { color: #D4AF37; font-weight: 600; font-size: 0.95rem; margin: 0 0 8px 0; }
.radar-grid-wrap { position: relative; background: #001f3f; border: 2px solid #D4AF37; border-radius: 12px; padding: 16px; min-height: 320px; display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(4, 1fr); gap: 10px; }
.radar-diamond-btn { min-width: 72px !important; border: 1px solid #D4AF37 !important; color: #D4AF37 !important; background: rgba(5, 10, 21, 0.9) !important; font-weight: 600 !important; border-radius: 8px !important; animation: gold-pulse 2s ease-in-out infinite !important; }
.radar-diamond-btn:hover { box-shadow: 0 0 16px rgba(255, 215, 0, 0.7) !important; }
#radar-column { position: relative !important; }
/* Falcon: diagonal shuttle across grid with rhythmic pulse */
.falcon-shuttle-overlay { position: absolute !important; top: 0; left: 0; right: 0; bottom: 0; pointer-events: none; z-index: 5; }
.falcon-shuttle-overlay img { position: absolute; width: 48px; height: 48px; object-fit: contain; animation: falcon-diagonal 2.4s ease-in-out infinite; }
@keyframes falcon-diagonal { 0% { left: 5%; top: 5%; transform: scale(1); opacity: 0.9; } 25% { left: 45%; top: 25%; transform: scale(1.1); opacity: 1; } 50% { left: 85%; top: 55%; transform: scale(1); opacity: 0.95; } 75% { left: 45%; top: 85%; transform: scale(1.08); opacity: 1; } 100% { left: 5%; top: 5%; transform: scale(1); opacity: 0.9; } }

/* The GCSLC Data Fortress — 3x3 grid + fortress_final.png */
.data-fortress-section { text-align: center; }
.data-fortress-section h3 { margin-bottom: 12px; }
.data-fortress-section .fortress-img-wrap { margin-bottom: 14px; }
.data-fortress-section .fortress-img-wrap img { max-width: 100%; max-height: 160px; object-fit: contain; }
.fortress-grid-3x3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; max-width: 560px; margin: 0 auto; }
.fortress-cell { padding: 12px; text-align: center; }
.fortress-cell-label { font-size: 0.75rem; color: #D4AF37; margin: 0 0 4px 0; font-weight: 600; }
.fortress-cell-value { font-size: 0.9rem; font-weight: 700; color: #00d4ff; margin: 0; }

/* 8R Humanoid Guardian — pulsing core, I NEED ENERGY TO THRIVE */
.guardian-baseline { text-align: center; }
.guardian-baseline h3 { margin-bottom: 12px; }
.guardian-pulse-wrap { position: relative; display: inline-block; }
.guardian-humanoid-img { margin: 0 auto; max-width: 100%; line-height: 0; position: relative; z-index: 1; }
.guardian-humanoid-img img { max-width: 100%; height: auto; display: block; margin: 0 auto; }
@keyframes guardian-breathing { 0%, 100% { filter: brightness(1) drop-shadow(0 0 8px rgba(0,212,255,0.4)); } 50% { filter: brightness(1.08) drop-shadow(0 0 18px rgba(0,212,255,0.6)); } }
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

@keyframes ticker-red-gold { 0%, 100% { color: #cc3333; } 50% { color: #D4AF37; } }

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


# ---- Build UI: Sovereign Command Center BASELINE (video order) ----
demo = gr.Blocks(css=CSS, title="GCSLC Sovereign Command")
with demo:
    gr.HTML('<script>document.addEventListener("contextmenu", function(e){ e.preventDefault(); });</script>')
    gr.HTML(SHIELD_SCRIPT)

    # 1. Header: Shimmering Gold Medallion + institutional name in gold bold text
    medallion_content = f'<img src="data:image/png;base64,{B64_MEDALLION}" alt="GCSLC Seal" />' if B64_MEDALLION else _medallion_svg()
    gr.HTML(
        '<div id="medallion" class="gcslc-medallion" aria-label="GCSLC Seal">' + medallion_content + '</div>'
        + '<div class="header-area">'
        + "<h1 class='sovereign-title' style='text-align: center; font-size: 1.2rem; margin: 0 0 6px 0;'>Sovereign Command</h1>"
        + f"<p class='title-full' style='text-align: center; font-size: 0.95rem; margin: 0 0 8px 0; color: #D4AF37; font-weight: 700;'>{TITLE_FULL}</p>"
        + "</div>"
        + f"<p class='hook' style='text-align: center; font-size: 0.92rem; max-width: 700px; margin: 0 auto 20px auto; color: #e8eef4;'>{HOOK_TEXT}</p>"
    )

    # 2. Top Section: Real-Time Market Values — 4 distinct gold-outlined glass boxes
    gr.HTML(real_time_market_values_html())

    # 3. Map Section: Map of Authority — dark navy center map + falcon overlay + 13 gold diamond buttons underneath
    gr.HTML('<h3 class="shimmer map-section-title">Map of Authority</h3>')
    gr.HTML(map_of_authority_html())
    gr.HTML('<p class="radar-grid-label">13 State Nodes — Enugu to Imo</p>')
    with gr.Row():
        b1 = gr.Button(COAL_STATES[0], elem_classes=["radar-diamond-btn"], variant="secondary")
        b2 = gr.Button(COAL_STATES[1], elem_classes=["radar-diamond-btn"], variant="secondary")
        b3 = gr.Button(COAL_STATES[2], elem_classes=["radar-diamond-btn"], variant="secondary")
        b4 = gr.Button(COAL_STATES[3], elem_classes=["radar-diamond-btn"], variant="secondary")
    with gr.Row():
        b5 = gr.Button(COAL_STATES[4], elem_classes=["radar-diamond-btn"], variant="secondary")
        b6 = gr.Button(COAL_STATES[5], elem_classes=["radar-diamond-btn"], variant="secondary")
        b7 = gr.Button(COAL_STATES[6], elem_classes=["radar-diamond-btn"], variant="secondary")
        b8 = gr.Button(COAL_STATES[7], elem_classes=["radar-diamond-btn"], variant="secondary")
    with gr.Row():
        b9 = gr.Button(COAL_STATES[8], elem_classes=["radar-diamond-btn"], variant="secondary")
        b10 = gr.Button(COAL_STATES[9], elem_classes=["radar-diamond-btn"], variant="secondary")
        b11 = gr.Button(COAL_STATES[10], elem_classes=["radar-diamond-btn"], variant="secondary")
        b12 = gr.Button(COAL_STATES[11], elem_classes=["radar-diamond-btn"], variant="secondary")
    b13 = gr.Button(COAL_STATES[12], elem_classes=["radar-diamond-btn"], variant="secondary")
    popup_out = gr.HTML(value=diamond_popup("Kogi"), label="Diamond Opportunity")
    state_btns = [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13]
    for i, state in enumerate(COAL_STATES):
        state_btns[i].click(fn=lambda s=state: diamond_popup(s), inputs=None, outputs=[popup_out])

    # 4. Metric Center: The GCSLC Data Fortress — 3x3 grid + fortress_final.png
    gr.HTML(data_fortress_3x3_html())

    # 5. Footer Section: National Impact (Coal Tonnage slider) → 8R Humanoid Guardian → Footer
    gr.HTML('<h3 class="shimmer">National Impact</h3>')
    coal_slider = gr.Slider(0, 500, value=100, step=10, label="Coal Tonnage (Million Tonnes)")
    national_impact_out = gr.HTML(
        value=f'<div class="gold-glass-block"><p class="reserves-line">At <strong>100</strong> M tonnes: {AI_PROCESSING_POWER} equivalent · Revenue potential scale: ${REVENUE_POTENTIAL_B}B.</p></div>'
    )

    def on_tonnage(t):
        return f'<div class="gold-glass-block"><p class="reserves-line">At <strong>{int(t)}</strong> M tonnes: {AI_PROCESSING_POWER} equivalent · Revenue potential scale: ${REVENUE_POTENTIAL_B}B.</p></div>'

    coal_slider.change(fn=on_tonnage, inputs=[coal_slider], outputs=[national_impact_out])

    gr.HTML(humanoid_block())
    gr.HTML(footer_html())


if __name__ == "__main__":
    try:
        demo.launch(server_name="0.0.0.0", server_port=7865, share=True)
    except OSError:
        demo.launch(server_name="0.0.0.0", server_port=0, share=True)
