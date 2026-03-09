"""
GCSLC Strategic Command Center — Strategic Command Override.
Prestige Humanoid (Guardian + Anthracite Chemical Node) | Falcon SVG Dynamic Actor + Sovereign Pulse |
Map of Authority (GeoJSON state borders, gold-cyan Value Realization) | Agentic Reasoning terminal. March Automations.
"""
import base64
import json
import math
import gradio as gr
import os
import shutil
import subprocess
import struct
import sys
import time
from typing import Optional

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

# Falcon landing position (x%, y%) on map for each state
STATE_MAP_POS = {
    "Enugu": (52, 72), "Kogi": (48, 58), "Benue": (58, 62), "Nasarawa": (50, 48),
    "Gombe": (62, 42), "Adamawa": (68, 48), "Delta": (38, 78), "Edo": (42, 68),
    "Ondo": (36, 62), "Bauchi": (58, 38), "Anambra": (50, 75), "Ebonyi": (54, 72), "Abia": (52, 78),
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


# ---- Map of Authority: Gold-to-Cyan gradient (Value Realization) ----
def _nigeria_svg() -> str:
    return """
    <svg class="nigeria-svg true-map map-of-authority" viewBox="0 0 280 360" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="ngStroke" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#B8860B"/>
          <stop offset="50%" style="stop-color:#FFD700"/>
          <stop offset="100%" style="stop-color:#D4AF37"/>
        </linearGradient>
        <linearGradient id="valueRealization" x1="0%" y1="100%" x2="100%" y2="0%">
          <stop offset="0%" style="stop-color:#FFD700"/>
          <stop offset="50%" style="stop-color:#D4AF37"/>
          <stop offset="100%" style="stop-color:#00d4ff"/>
        </linearGradient>
        <linearGradient id="ngFill" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:rgba(0,26,53,0.5)"/>
          <stop offset="100%" style="stop-color:rgba(0,11,30,0.6)"/>
        </linearGradient>
      </defs>
      <!-- National outline: Federal Republic of Nigeria — Value Realization (gold-to-cyan) -->
      <path fill="url(#valueRealization)" fill-opacity="0.35" stroke="url(#ngStroke)" stroke-width="2"
        d="M138 18 L172 35 L198 62 L205 98 L218 142 L224 188 L218 242 L192 282 L152 332 L118 342 L82 308 L58 258 L44 198 L38 142 L48 88 L68 48 L98 28 L120 18 Z"/>
      <!-- State borders (internal boundaries) -->
      <path fill="none" stroke="url(#ngStroke)" stroke-width="0.9" opacity="0.7" d="M138 95 L138 198 L95 258 L58 258"/>
      <path fill="none" stroke="url(#ngStroke)" stroke-width="0.9" opacity="0.7" d="M138 95 L178 118 L198 62"/>
      <path fill="none" stroke="url(#ngStroke)" stroke-width="0.9" opacity="0.7" d="M138 198 L192 242 L218 242"/>
      <path fill="none" stroke="url(#ngStroke)" stroke-width="0.9" opacity="0.7" d="M82 308 L118 342 L152 332"/>
      <path fill="none" stroke="url(#ngStroke)" stroke-width="0.9" opacity="0.7" d="M44 198 L38 142 L48 88"/>
      <path fill="none" stroke="url(#ngStroke)" stroke-width="0.9" opacity="0.7" d="M68 48 L98 28 L120 18 L138 18"/>
      <path fill="none" stroke="url(#ngStroke)" stroke-width="0.9" opacity="0.7" d="M172 35 L198 62 L205 98"/>
      <path fill="none" stroke="url(#ngStroke)" stroke-width="0.9" opacity="0.7" d="M218 142 L224 188 L218 242 L192 282"/>
      <text x="140" y="178" text-anchor="middle" fill="rgba(212,175,55,0.35)" font-size="13" font-weight="700">FEDERAL REPUBLIC OF NIGERIA</text>
      <text x="140" y="198" text-anchor="middle" fill="rgba(0,212,255,0.3)" font-size="10">13 coal-rich states — Value Realization (Gold → Cyan)</text>
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
      <h3 class="shimmer">Map of Authority — Federal Republic of Nigeria (state borders, Value Realization)</h3>
      <p class="map-sub">13 coal-rich states (Gold → Cyan). Click a state: Falcon performs tactical dive to coordinate; Sovereign Pulse sound plays.</p>
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


def _footer_block() -> str:
    return f"""
    <div class="footer-block">
      <p class="signature">{CHAIRMAN_SIGNATURE}</p>
      <p class="cac">CAC Registration: {CAC_REGISTRATION}</p>
      <p class="legal">{TITLE_FULL}</p>
      <p class="copy">© GCSLC. Proprietary.</p>
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

.gradio-container, .main, .container {
    background-color: #050505 !important;
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
/* Chemical Node: Nigerian Anthracite in Guardian hand — cyan inner-glow (raw asset → green chemicals) */
@keyframes chemical-node-pulse {
  0%, 100% { opacity: 0.7; filter: drop-shadow(0 0 6px rgba(0,212,255,0.6)); }
  50% { opacity: 1; filter: drop-shadow(0 0 14px rgba(0,212,255,0.9)); }
}
.chemical-node { animation: chemical-node-pulse 2s ease-in-out infinite; }
.chemical-node ellipse { transform-origin: center; }
.speech-wrap { position: absolute; left: 50%; top: 78%; transform: translate(-50%, -50%); width: 92%; z-index: 3; }
.speech-bubble { background: #001A35; border: 2px solid #D4AF37; border-radius: 10px; padding: 10px 12px; margin: 0; font-size: 0.8rem; color: #e8eef4; line-height: 1.35; }

.footer-block { text-align: center; padding: 20px 16px; margin-top: 24px; border-top: 1px solid rgba(212,175,55,0.35); }
.signature { font-size: 0.9rem; font-weight: 600; color: #D4AF37; margin: 0 0 6px 0; }
.cac { font-size: 0.85rem; color: #b8c4ce; margin: 0 0 4px 0; }
.legal { font-size: 0.78rem; color: #b8c4ce; margin: 0 0 4px 0; }
.copy { font-size: 0.75rem; color: rgba(184,196,206,0.75); margin: 0; }

/* General's Hook: Agentic Reasoning terminal (hidden by default, expandable) */
.agentic-terminal-wrap { margin-top: 16px; }
.agentic-terminal { background: #0a0a0f; border: 1px solid #00d4ff; border-radius: 8px; padding: 10px 12px; max-height: 140px; overflow: hidden; }
.agentic-terminal-header { color: #00d4ff; font-size: 0.75rem; margin-bottom: 6px; font-weight: 700; }
.agentic-terminal-log { color: #00ff88; font-size: 0.7rem; margin: 0; white-space: pre-wrap; word-break: break-word; max-height: 100px; overflow-y: auto; }
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

    # 2. TRUE MAP + MUSICAL FALCON (state-bordered Nigeria SVG; Falcon dives into 13 coal states)
    map_out = gr.HTML(value=_map_html("Kogi"), label="Nigeria Map")
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

    def on_map(s):
        def fn():
            return _map_html(s)
        return fn

    for state, btn in btns:
        btn.click(fn=on_click(state), inputs=None, outputs=popup_out)
        btn.click(fn=on_map(state), inputs=None, outputs=map_out)

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
