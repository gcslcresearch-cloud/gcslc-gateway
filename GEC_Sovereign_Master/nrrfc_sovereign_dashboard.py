"""
GCSLC Sovereign Gateway — NRRFC Dashboard (Port 8051).
Zero local file dependencies: web-hosted placeholders for medallion and video.
Deep Navy background, Gold/White shimmer, 8R Determinant cards. CAC & Chairman Lock.
© 2026 GCSLC LTD/GTE.
"""
import streamlit as st
import streamlit.components.v1 as components
import base64
import math
import pandas as pd
import random
import time
from pathlib import Path

# SOVEREIGN CONFIGURATION — Isolated UI via html(); no Streamlit sidebar
st.set_page_config(page_title="GCSLC Sovereign Gateway", layout="wide", initial_sidebar_state="collapsed")

# WEB-HOSTED / EMBEDDED ASSETS (no local files)
# Medallion: inline SVG (gold circle, GCSLC) — zero file dependency
MEDALLION_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 150 150">
  <defs><linearGradient id="gold" x1="0%%" y1="0%%" x2="100%%" y2="100%%"><stop offset="0%%" style="stop-color:#FFD700"/><stop offset="100%%" style="stop-color:#B8860B"/></linearGradient></defs>
  <circle cx="75" cy="75" r="72" fill="none" stroke="url(#gold)" stroke-width="4"/>
  <circle cx="75" cy="75" r="58" fill="#001d3d"/>
  <text x="75" y="78" text-anchor="middle" fill="#FFD700" font-size="20" font-weight="bold" font-family="system-ui,sans-serif">GCSLC</text>
</svg>"""
MEDALLION_DATA_URI = "data:image/svg+xml;base64," + base64.b64encode(MEDALLION_SVG.encode()).decode()

# Eagle video: local file (same folder as this script); Path.exists() avoids FileNotFoundError
_EAGLE_VIDEO_PATH = Path(__file__).resolve().parent / "eagle_anim.mp4"

# 8R Sovereign Cycle — D-Determinant labels for circular layout (high-contrast gold on navy)
R8_NODES = [
    ("D1", "RESET"),
    ("D2", "REGENERATE"),
    ("D3", "RESEARCH"),
    ("D4", "RESTRUCTURE"),
    ("D5", "REVITALIZE"),
    ("D6", "REPLICATE"),
    ("D7", "REVENUE"),
    ("D8", "RETAIN"),
]

# Sovereign Data Nodes — 13-state coal reserves (for Coal Reserves table in HTML)
SOVEREIGN_DATA_NODES = {
    "State": ["Enugu", "Kogi", "Gombe", "Benue", "Delta", "Nasarawa", "Anambra", "Plateau", "Adamawa", "Edo", "Bauchi", "Kwara", "Zamfara"],
    "Coal Reserves (MT)": [150.0, 120.0, 80.0, 70.0, 55.0, 45.0, 35.0, 25.0, 20.0, 15.0, 10.0, 10.0, 5.2],
    "Nodal Status": "PROTECTED",
}


def build_sovereign_dashboard_html(current_time, reset_phase_active):
    """Build ENTIRE dashboard as single HTML for st.components.v1.html. Sovereign standards: #000814, #D4AF37, no white. Sections: Derivative Strike, Mineral Yield, 8R Circle, Glossary."""
    # 8R SVG: perfect circle — each node is <g> with hollow gold circle + text (click-to-shimmer)
    cx, cy, r_node = 175, 175, 100
    r_circle = 28
    svg_nodes = ""
    for i, (code, name) in enumerate(R8_NODES):
        rad = math.radians(i * 45)
        x = cx + r_node * math.cos(rad)
        y = cy - r_node * math.sin(rad)
        pulse_class = " r8-svg-pulse" if i == 2 else (" r8-svg-pulse-all" if reset_phase_active else "")
        svg_nodes += f'<g class="r8-node-g" style="cursor:pointer"><circle class="r8-svg-node{pulse_class}" cx="{x:.1f}" cy="{y:.1f}" r="{r_circle}" fill="none" stroke="#D4AF37" stroke-width="2"/>'
        svg_nodes += f'<text x="{x:.1f}" y="{y - 4:.1f}" text-anchor="middle" fill="#D4AF37" font-size="9" font-weight="bold">{code}</text>'
        svg_nodes += f'<text x="{x:.1f}" y="{y + 8:.1f}" text-anchor="middle" fill="#D4AF37" font-size="8">{name}</text></g>'
    # Coal table rows
    states = SOVEREIGN_DATA_NODES["State"]
    reserves = SOVEREIGN_DATA_NODES["Coal Reserves (MT)"]
    table_rows = "".join(
        f'<tr><td style="color:#D4AF37;padding:8px;border-bottom:1px solid #D4AF37">{s}</td>'
        f'<td style="color:#D4AF37;padding:8px;border-bottom:1px solid #D4AF37">{m:.1f}</td>'
        f'<td style="color:#D4AF37;padding:8px;border-bottom:1px solid #D4AF37">PROTECTED</td></tr>'
        for s, m in zip(states, reserves)
    )
    active_banner = '<div class="active-scan-banner">● ACTIVE SCAN MODE — DASHBOARD LOCKED</div>' if reset_phase_active else ""
    system_class = " system-online" if reset_phase_active else ""
    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    * {{ box-sizing: border-box; }}
    body, html {{ margin:0; padding:0; background:#000814; color:#D4AF37; font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif; }}
    .wrap {{ background:#000814; min-height:100vh; padding-bottom: 60px; }}
    .watermark {{ position:fixed; top:50%; left:50%; transform:translate(-50%,-50%) rotate(-25deg); font-size:clamp(2rem,6vw,4rem); color:rgba(212,175,55,0.10); z-index:1; pointer-events:none; white-space:nowrap; font-weight:bold; text-transform:uppercase; }}
    .glossary {{ position:fixed; right:0; top:0; height:100vh; width:20%; min-width:200px; background:rgba(0,8,20,0.98); border-left:1px solid #D4AF37; padding:16px; z-index:9999; overflow-y:auto; }}
    .glossary h3 {{ color:#D4AF37; font-size:0.9rem; text-transform:uppercase; margin-top:0; }}
    .glossary p {{ color:#b5a48b; font-size:0.75rem; line-height:1.5; }}
    .main {{ margin-right:22%; padding:16px; position:relative; z-index:2; }}
    .medallion-header {{ text-align:center; padding:24px 16px; border-bottom:1px solid #D4AF37; background:rgba(0,8,20,0.6); }}
    .medallion-header h1, .medallion-header h2 {{ font-size:1rem; color:#D4AF37; text-transform:uppercase; }}
    .medallion-header p {{ color:#b5a48b; font-size:0.8rem; }}
    .welcome {{ text-align:center; color:#D4AF37; font-weight:700; margin:12px 0; text-transform:uppercase; font-size:0.9rem; }}
    .ticker {{ background:rgba(0,8,20,0.6); border:1px solid #D4AF37; padding:8px 16px; text-align:center; color:#D4AF37; font-size:0.85rem; margin:12px 0; }}
    .activation-alert {{ background:rgba(0,8,20,0.6); border:1px solid #D4AF37; padding:8px; text-align:center; margin:12px 0; font-size:0.75rem; color:#D4AF37; text-transform:uppercase; }}
    .active-scan-banner {{ background:rgba(0,8,20,0.98); border-bottom:1px solid #D4AF37; padding:8px; text-align:center; color:#D4AF37; font-weight:700; margin-bottom:12px; text-transform:uppercase; }}
    .section-title {{ color:#D4AF37; font-size:0.85rem; text-transform:uppercase; margin:16px 0 8px 0; letter-spacing:0.05em; }}
    .sovereign-box {{ background:rgba(0,8,20,0.6); border:1px solid #D4AF37; padding:12px 16px; color:#D4AF37; }}
    .metric-grid {{ display:flex; flex-wrap:wrap; gap:12px; align-items:stretch; margin:12px 0; }}
    .metric-grid .metric-cell {{ flex:1; min-width:140px; background:rgba(0,8,20,0.6); border:1px solid #D4AF37; padding:14px; color:#D4AF37; font-size:0.8rem; }}
    .metric-grid .metric-cell .label {{ text-transform:uppercase; font-size:0.7rem; margin-bottom:4px; color:#D4AF37; }}
    .metric-grid .metric-cell .value {{ font-weight:700; color:#D4AF37; }}
    .multiplier-box {{ background:rgba(0,8,20,0.6); border:1px solid #D4AF37; padding:14px 20px; text-align:center; color:#D4AF37; }}
    .multiplier-box .value {{ font-size:1.5rem; font-weight:700; color:#D4AF37; }}
    .mineral-table {{ width:100%; border-collapse:collapse; background:#000814; border:1px solid #D4AF37; margin:12px 0; }}
    .mineral-table th {{ color:#D4AF37; padding:10px; text-align:left; border-bottom:1px solid #D4AF37; background:#000814; font-size:0.8rem; text-transform:uppercase; }}
    .mineral-table td {{ color:#D4AF37; padding:8px; border-bottom:1px solid rgba(212,175,55,0.4); background:#000814; }}
    .mineral-table tfoot td {{ border-top:2px solid #D4AF37; font-weight:700; color:#D4AF37; padding:10px; background:#000814; }}
    .total-underscore {{ border-bottom:2px solid #D4AF37; padding:10px 0; margin-top:8px; font-weight:700; color:#D4AF37; }}
    .r8-wrap {{ margin:24px auto; width:350px; }}
    .r8-wrap svg {{ display:block; margin:0 auto; }}
    .r8-svg-path {{ fill:none; stroke:#D4AF37; stroke-width:1; stroke-dasharray:6 4; }}
    .r8-svg-node {{ fill:none; stroke:#D4AF37; }}
    .r8-node-g {{ cursor:pointer; }}
    .r8-svg-node.r8-node-clicked {{ animation: node-shimmer 1s ease; }}
    @keyframes node-shimmer {{ 0% {{ stroke:#fff; }} 100% {{ stroke:#D4AF37; }} }}
    .r8-svg-pulse {{ animation: pulse 2s ease-in-out infinite; }}
    .r8-svg-pulse-all {{ animation: pulse 1.5s ease-in-out infinite; }}
    @keyframes pulse {{ 0%,100% {{ stroke-opacity:0.9; }} 50% {{ stroke-opacity:1; filter:drop-shadow(0 0 8px #D4AF37); }} }}
    .coal-table {{ width:100%; border-collapse:collapse; background:#000814; border:1px solid #D4AF37; margin:12px 0; }}
    .coal-table th {{ color:#D4AF37; padding:10px; text-align:left; border-bottom:1px solid #D4AF37; background:#000814; font-size:0.8rem; text-transform:uppercase; }}
    .coal-table td {{ color:#D4AF37; padding:8px; border-bottom:1px solid rgba(212,175,55,0.4); background:#000814; }}
    .status-bar {{ position:fixed; bottom:0; left:0; right:0; padding:10px 20px; background:#000814; border-top:1px solid #D4AF37; text-align:center; color:#D4AF37; font-weight:700; z-index:9998; text-transform:uppercase; }}
    .footer {{ text-align:center; padding:16px; color:#b5a48b; font-size:0.8rem; border-top:1px solid #D4AF37; margin-top:24px; }}
    .debt-swap-statement {{ text-align:center; color:#D4AF37; font-size:0.9rem; margin:20px 0; padding:12px; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="watermark">GCSLC PROPRIETARY | SOVEREIGN</div>

  <div class="glossary">
    <h3>TECHNICAL GLOSSARY</h3>
    <p><strong>LLMS</strong> — AI systems for yield prediction.</p>
    <p><strong>KPIS</strong> — Revenue ($50.1M), Multiplier (9.6x).</p>
    <p>Python-to-Sovereign Feedstock — Pipeline from stack to Syngas conversion.</p>
    <hr style="border-color:rgba(212,175,55,0.3);">
    <p style="font-size:0.7rem; color:#b5a48b;">2026 FX: ₦1,350 = $1</p>
  </div>

  <div class="main">
    <div class="medallion-header">
      <h1>Galadiman Ruwa Center for Strategic Leadership and Communication</h1>
      <h2>GCSLC LTD/GTE</h2>
      <p>Proponent of the 8R Stealth Paradigm Convergence</p>
    </div>
    <p class="welcome">Welcome, Chairman. The Eagle is Scanning. Nigeria's 638.3 MT Reserves are Live.</p>
    <div class="ticker">+12.2% Price Spike Detected. Revaluing Strategic Reserves...</div>
    <div class="activation-alert">Sovereign Activation Alert</div>
    {active_banner}
    <p class="section-title">Last updated: {current_time}</p>

    <h2 class="section-title">NRRFC VALUE-ADDED DERIVATIVE STRIKE — GCSLC SOVEREIGN</h2>
    <div class="metric-grid">
      <div class="metric-cell">
        <div class="label">RAW COAL VALUE (USD)</div>
        <div class="value">$1.1 M</div>
        <div class="label" style="font-size:0.65rem;">₦1.49 B</div>
      </div>
      <div class="metric-cell">
        <div class="label">DERIVATIVE UPSIDE (USD)</div>
        <div class="value">$9.5 M</div>
        <div class="label" style="font-size:0.65rem;">₦12.77 B</div>
      </div>
      <div class="metric-cell">
        <div class="label">TOTAL SOVEREIGN EQUITY (USD)</div>
        <div class="value">$10.6 M</div>
        <div class="label" style="font-size:0.65rem;">₦14.25 B</div>
      </div>
      <div class="multiplier-box">
        <div class="label" style="text-transform:uppercase; font-size:0.7rem;">VALUE MULTIPLIER</div>
        <div class="value">9.6x</div>
      </div>
    </div>

    <h2 class="section-title">CRITICAL MINERAL YIELD (THE MATHEMATICAL STRIKE)</h2>
    <table class="mineral-table">
      <thead><tr><th>Product</th><th>Volume</th><th>Price</th><th>Revenue (USD)</th><th>Revenue (₦)</th></tr></thead>
      <tbody>
        <tr><td>Raw Coal</td><td>10,000 MT</td><td>$110</td><td>$1.1 M</td><td>₦1.49 B</td></tr>
        <tr><td>Germanium (fly ash)</td><td>800 KG</td><td>$8,597</td><td>$6.9 M</td><td>₦9.28 B</td></tr>
        <tr><td>Ammonia</td><td>6,000 MT</td><td>$430</td><td>$2.6 M</td><td>₦3.48 B</td></tr>
      </tbody>
      <tfoot><tr><td colspan="3">Total Revenue</td><td>$10.6 M</td><td>₦14.25 B</td></tr></tfoot>
    </table>
    <p class="total-underscore" style="border-bottom:2px solid #D4AF37;">Total Revenue: $10.6 M (₦14.25 B)</p>

    <h2 class="section-title">THE 8R STEALTH PARADIGM CIRCLE</h2>
    <p style="font-size:0.75rem; color:#D4AF37;">D1–D8 Determinants — click a node for shimmer</p>
    <div class="r8-wrap{system_class}">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 350 350" width="350" height="350">
        <circle class="r8-svg-path" cx="175" cy="175" r="130"/>
        {svg_nodes}
      </svg>
    </div>

    <p class="section-title">D3: RESEARCH — 13-STATE ASSET MAPPING</p>
    <p style="font-size:0.75rem; color:#D4AF37;">ACTIVE SCAN — 13-State strike zone</p>
    <p class="section-title">MEASURABLE SUBSOIL NODAL MAPPING</p>
    <table class="coal-table">
      <thead><tr><th>State</th><th>Coal Reserves (MT)</th><th>Nodal Status</th></tr></thead>
      <tbody>{table_rows}</tbody>
    </table>
    <p style="color:#b5a48b; font-size:0.8rem;">Strike Revenue Target: $50.1M Monthly per Node.</p>

    <p class="debt-swap-statement">By capturing 10% of Global Big Tech CAPEX, we achieve 189% coverage of Nigeria's domestic debt.</p>

    <div class="footer">
      <p style="color:#D4AF37;"><strong>INCONTROVERTIBLE NODAL AUTHORITY:</strong> DR. JAAFARU SA'AD (GALADIMAN RUWA) | CAC: 176917792057</p>
      <p>© 2026 GCSLC LTD/GTE. Proprietary 8R Stealth Paradigm Convergence.</p>
    </div>
  </div>

  <div class="status-bar">SOVEREIGN STRIKE &nbsp; $50.1M &nbsp; MONTHLY REVENUE</div>
</div>
<script>
document.querySelectorAll('.r8-node-g').forEach(function(g) {{
  g.addEventListener('click', function() {{
    var circle = this.querySelector('circle');
    circle.classList.add('r8-node-clicked');
    setTimeout(function() {{ circle.classList.remove('r8-node-clicked'); }}, 1000);
  }});
}});
</script>
</body>
</html>
"""
    return html


# ---- ISOLATED UI: dashboard rendered via st.components.v1.html (replaces Streamlit container) ----
# CUSTOM CSS: DEEP NAVY BASE, GOLD/WHITE SHIMMER, HIGHLY VISIBLE 8R CARDS
st.markdown("""
    <style>
    /* PERMANENT NAVY & GOLD — purge white (reference override) */
    .stApp { background-color: #000814 !important; color: #D4AF37 !important; }
    div[data-testid="stMetricValue"], .stMarkdown, div[role="button"] {
        background-color: transparent !important;
        color: #D4AF37 !important;
    }
    /* REMOVE ALL WHITE from node and glossary */
    .node, .circle-container .node { background: transparent !important; background-color: transparent !important; color: #D4AF37 !important; }
    .node *, .circle-container .node span { color: #D4AF37 !important; }
    .glossary-sidebar { background: #000814 !important; background-color: #000814 !important; }
    /* Nodal text — gold on navy */
    .node-text {
        color: #D4AF37 !important;
        font-weight: bold;
        text-shadow: 0 0 5px #000;
        text-transform: uppercase;
        font-size: 10px;
    }
    /* Sovereign Branding Standards - GCSLC */
    :root {
        --deep-navy: #000814;
        --gold-shimmer: #FFD700;
        --gold-grey: #b5a48b;
    }
    .sovereign-header {
        font-size: 1.1rem !important;
        letter-spacing: 0.1rem;
        text-transform: uppercase;
    }
    .glossary-sidebar {
        width: 220px;
        font-size: 0.75rem;
        color: var(--gold-grey);
        border-left: 1px solid rgba(255, 215, 0, 0.3);
        padding: 10px;
    }
    /* Technical Glossary — FIXED RIGHT SIDEBAR (250px), gold-grey text */
    [data-testid="stSidebar"] {
        position: fixed !important;
        right: 0 !important;
        left: auto !important;
        width: 250px !important;
        min-width: 250px !important;
        background: rgba(0, 8, 20, 0.95) !important;
        background-color: rgba(0, 8, 20, 0.95) !important;
        border-left: 2px solid #D4AF37 !important;
        padding: 12px !important;
        color: #b5a48b !important;
    }
    [data-testid="stSidebar"] .stMarkdown { font-size: 0.7rem; color: #b5a48b !important; }
    [data-testid="stSidebar"] .stMarkdown h3 { font-size: 0.8rem; color: #D4AF37 !important; text-transform: uppercase; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label { color: #b5a48b !important; }
    [data-testid="stAppViewContainer"] > section:first-child { margin-right: 268px !important; }
    .shimmer-text {
        background: linear-gradient(90deg, #FFD700, #FFF, #FFD700);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 3s linear infinite;
    }
    @keyframes shimmer {
        to { background-position: 200% center; }
    }
    /* NRRFC Sovereign Gateway — Deep Navy, Gold, PURGE WHITE */
    .stApp, .main, [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > section,
    .block-container, [data-testid="block-container"] {
        background-color: var(--deep-navy) !important;
        color: #D4AF37;
        font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
        padding-bottom: 56px !important;
    }
    p, span, label, div[data-testid="stMarkdown"] { color: #e0e0e0 !important; }
    div[data-testid="stMarkdown"] p { color: #e0e0e0 !important; }
    .stCaption { color: var(--gold-grey) !important; }
    .medallion-header {
        text-align: center;
        padding: 36px 24px;
        border-bottom: 3px solid #FFD700;
        background: linear-gradient(180deg, #001d3d 0%, #000814 100%);
    }
    /* 8R Stealth Paradigm Convergence Cycle — clockwise generative energy pulse */
    .r8-nodal-grid {
        display: grid;
        gap: 12px;
        margin-bottom: 16px;
    }
    .r8-node {
        background: linear-gradient(145deg, rgba(0, 45, 90, 0.95) 0%, rgba(0, 29, 61, 0.98) 100%);
        border: 2px solid rgba(255, 215, 0, 0.5);
        padding: 16px 12px;
        border-radius: 12px;
        text-align: center;
        transition: transform 0.2s ease;
        animation: r8-pulse 3.2s linear infinite;
    }
    .r8-node:hover { transform: translateY(-2px); }
    .r8-node-1 { animation-delay: 0s; }
    .r8-node-2 { animation-delay: -0.4s; }
    .r8-node-3 { animation-delay: -0.8s; }
    .r8-node-4 { animation-delay: -1.2s; }
    .r8-node-5 { animation-delay: -1.6s; }
    .r8-node-6 { animation-delay: -2s; }
    .r8-node-7 { animation-delay: -2.4s; }
    .r8-node-8 { animation-delay: -2.8s; }
    @keyframes r8-pulse {
        0% {
            border-color: #cb9b51;
            box-shadow: 0 0 24px rgba(203, 155, 81, 0.6), inset 0 0 16px rgba(246, 226, 122, 0.2);
            background: linear-gradient(90deg, #462523 0%, #cb9b51 22%, #f6e27a 45%, #f6f2c0 50%, #f6e27a 55%) !important;
        }
        12.5%, 100% {
            border-color: rgba(255, 215, 0, 0.5);
            box-shadow: 0 4px 20px rgba(255, 215, 0, 0.2);
            background: linear-gradient(145deg, rgba(0, 45, 90, 0.95) 0%, rgba(0, 29, 61, 0.98) 100%) !important;
        }
    }
    .r8-node-active {
        background: linear-gradient(90deg, #462523 0%, #cb9b51 22%, #f6e27a 45%, #f6f2c0 50%, #f6e27a 55%) !important;
        color: #f6f2c0;
        border-color: #cb9b51 !important;
        box-shadow: 0 0 24px rgba(203, 155, 81, 0.5);
    }
    .r8-node-active .r8-node-title { color: #f6e27a; }
    .r8-node .r8-node-title {
        color: #FFD700;
        font-size: 0.95rem;
        font-weight: 800;
        margin-bottom: 6px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }
    .r8-node .r8-node-desc {
        color: #e0e0e0;
        font-size: 0.8rem;
    }
    /* 8R Nodal Logic — node-card & shimmer-gold (interactive buttons) */
    .node-card {
        background-color: #000814;
        border: 1px solid #D4AF37;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        transition: 0.3s;
    }
    .node-card:hover {
        background: linear-gradient(45deg, #000814, #1a2a44);
        border: 1px solid #FFF;
        cursor: pointer;
    }
    .shimmer-gold {
        color: #D4AF37;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
        animation: node-pulse 2s infinite;
    }
    @keyframes node-pulse {
        0% { opacity: 0.8; }
        50% { opacity: 1; text-shadow: 0 0 20px #D4AF37; }
        100% { opacity: 0.8; }
    }
    .determinant-card {
        background: linear-gradient(145deg, rgba(0, 45, 90, 0.95) 0%, rgba(0, 29, 61, 0.98) 100%);
        border: 2px solid #FFD700;
        padding: 20px 16px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(255, 215, 0, 0.2), inset 0 1px 0 rgba(255,255,255,0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .determinant-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 28px rgba(255, 215, 0, 0.35);
    }
    .determinant-title {
        color: #FFD700;
        font-size: 1.15rem;
        font-weight: 800;
        margin-bottom: 8px;
        letter-spacing: 1px;
    }
    .determinant-desc {
        color: #e0e0e0;
        font-size: 0.95rem;
    }
    @keyframes navy-shimmer {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    div[data-testid="stVideo"] {
        width: 100% !important;
        max-width: 100%;
        background: linear-gradient(135deg, #001d3d 0%, #000814 50%, #001d3d 100%);
        background-size: 200% 200%;
        animation: navy-shimmer 4s ease infinite;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid rgba(255, 215, 0, 0.35);
    }
    div[data-testid="stVideo"] video { width: 100% !important; }
    .shimmer-headline {
        font-family: 'Inter', sans-serif;
        font-weight: bold;
        color: #FFD700;
        background: linear-gradient(90deg, #FFD700 25%, #FFFACD 50%, #FFD700 75%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 3s linear infinite;
    }
    /* Tables: navy background, gold border (no white) */
    .stDataFrame, div[data-testid="stDataFrame"], div[data-testid="stTable"] {
        background-color: #001F3F !important;
        border: 1px solid #FFD700;
    }
    /* Shimmer strike cycles — gold-pulse for D3 nodal headline */
    @keyframes gold-pulse {
        0% { text-shadow: 0 0 5px #FFD700; opacity: 0.8; }
        50% { text-shadow: 0 0 20px #FFFACD; opacity: 1; }
        100% { text-shadow: 0 0 5px #FFD700; opacity: 0.8; }
    }
    .shimmer-nodal {
        color: #FFD700 !important;
        font-weight: bold;
        animation: gold-pulse 2s infinite;
        text-align: center;
    }
    /* Meticulous table styling (Golden-Navy) — transparent bg, gold border */
    .stTable {
        background-color: transparent !important;
        border: 2px solid #FFD700 !important;
        border-radius: 15px;
    }
    .stTable th { color: #FFD700 !important; font-family: 'Inter', sans-serif; border-bottom: 2px solid #FFD700; }
    .stTable td { color: #ffffff !important; font-family: monospace; }
    /* Diamond shimmer — strike cycles for D3 nodal headline */
    @keyframes diamond-shimmer {
        0% { color: #FFD700; text-shadow: 0 0 5px #FFD700; }
        50% { color: #FFFFFF; text-shadow: 0 0 20px #FFFFFF; }
        100% { color: #FFD700; text-shadow: 0 0 5px #FFD700; }
    }
    .shimmer-node {
        animation: diamond-shimmer 2s infinite;
        font-weight: bold;
        text-align: center;
    }
    /* Gold & Navy lock — clinical table + gold-shimmer headline */
    @keyframes shimmer-opacity {
        0% { opacity: 0.7; } 50% { opacity: 1; } 100% { opacity: 0.7; }
    }
    .gold-shimmer {
        color: #FFD700 !important;
        font-weight: bold;
        text-shadow: 0 0 10px #FFD700;
        animation: shimmer-opacity 2s infinite;
    }
    table { background-color: #001F3F !important; border: 1px solid #FFD700 !important; width: 100%; color: white; }
    th { color: #FFD700 !important; text-align: left; border-bottom: 2px solid #FFD700; }
    td { border-bottom: 1px solid #334b63; padding: 8px; }
    /* GEC Sovereign Shimmer Engine (white & gold) */
    @keyframes gec-diamond-shimmer {
        0% { color: #FFD700; text-shadow: 0 0 10px #FFD700; }
        50% { color: #FFFFFF; text-shadow: 0 0 25px #FFFFFF; }
        100% { color: #FFD700; text-shadow: 0 0 10px #FFD700; }
    }
    .gec-shimmer {
        animation: gec-diamond-shimmer 2.5s infinite;
        font-weight: bold;
    }
    .brief-box {
        background-color: #001F3F;
        border: 2px solid #FFD700;
        border-radius: 10px;
        padding: 20px;
        margin-top: 25px;
    }
    /* Lean strategic styling (brainbox aesthetic) */
    h2, h3 {
        text-transform: none !important;
        font-size: 1.2rem !important;
        letter-spacing: 0.05rem;
    }
    .lean-brief {
        font-size: 0.95rem;
        line-height: 1.4;
        color: #e0e0e0;
    }
    .debt-card {
        background: rgba(0, 31, 63, 0.8);
        border: 1px solid #FFD700;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
    }
    /* Lean SFP Analytics */
    .sfp-header {
        color: #FFD700;
        font-size: 1.1rem !important;
        text-transform: none;
        margin-bottom: 5px;
    }
    .sfp-subtext {
        color: #e0e0e0;
        font-size: 0.85rem;
        margin-bottom: 20px;
    }
    .revenue-shimmer {
        color: #FFD700;
        font-weight: bold;
        animation: gec-diamond-shimmer 2s infinite;
    }
    /* Lean clinical styling (CC & Roadmap) */
    .cc-header {
        color: #FFD700;
        font-size: 1.05rem !important;
        text-transform: none;
        letter-spacing: 0.04rem;
        margin-top: 30px;
    }
    .road-step {
        border-left: 2px solid #FFD700;
        padding-left: 15px;
        margin-bottom: 15px;
    }
    .step-title {
        color: #FFD700;
        font-size: 0.9rem;
        font-weight: bold;
        text-transform: uppercase;
    }
    .step-detail {
        color: #e0e0e0;
        font-size: 0.8rem;
    }
    .sovereign-tax {
        background: rgba(255, 215, 0, 0.1);
        border: 1px dashed #FFD700;
        padding: 10px;
        text-align: center;
        border-radius: 5px;
    }
    /* S24 Ultra mobile engine (responsive strike) */
    @media (max-width: 480px) {
        .gec-card { padding: 10px; margin-bottom: 8px; border-radius: 6px; }
        .stMetric { font-size: 0.75rem !important; }
        .gec-shimmer { font-size: 0.85rem !important; }
        [data-testid="column"] { width: 100% !important; flex: 1 1 100% !important; }
    }
    .lean-header {
        color: #FFD700;
        font-size: 0.9rem;
        text-transform: none;
        letter-spacing: 0.03rem;
        margin-top: 25px;
    }
    .footer-sovereign {
        text-align: center;
        color: #a3a3a3;
        font-size: 0.85rem;
        padding: 20px 16px;
        border-top: 2px solid rgba(255, 215, 0, 0.4);
        background: rgba(0, 29, 61, 0.5);
    }
    .footer-sovereign strong { color: #FFD700; }
    /* THE $50.1M STRIKE — Sovereign Status Bar (fixed bottom, high-fidelity) */
    .sovereign-status-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        padding: 10px 20px;
        background: rgba(0, 8, 20, 0.95);
        border-top: 2px solid #D4AF37;
        color: #D4AF37;
        font-weight: 700;
        z-index: 1000;
    }
    .sovereign-status-bar .status-bar-label { font-size: 0.7rem; letter-spacing: 0.15em; text-transform: uppercase; }
    .sovereign-status-bar .status-bar-value { font-size: 1.4rem; text-shadow: 0 0 12px rgba(212, 175, 55, 0.6); }
    .sovereign-status-bar .status-bar-sublabel { font-size: 0.7rem; color: #b5a48b; text-transform: uppercase; }
    /* PURGE WHITE BOXES — translucent navy for all widget surfaces */
    [data-testid="stExpander"], .stExpander { background: rgba(0, 8, 20, 0.9) !important; border: 1px solid #D4AF37 !important; }
    .stSuccess, [data-testid="stAlert"] div { background: rgba(0, 8, 20, 0.95) !important; border-color: #D4AF37 !important; color: #b5a48b !important; }
    /* Security & watermark — GCSLC PROPRIETARY | SOVEREIGN diagonal 8% opacity (Kwas-Kwas) */
    .watermark {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-25deg);
        font-size: clamp(3rem, 8vw, 5rem);
        color: rgba(212, 175, 55, 0.08);
        z-index: 9999;
        pointer-events: none;
        user-select: none;
        white-space: nowrap;
        font-weight: bold;
        font-family: 'Inter', sans-serif;
    }
    /* PURGE ALL WHITE BACKGROUNDS — Sovereign data visibility */
    [data-testid="stMetric"], .stMetric, [data-testid="metric-container"] {
        background-color: #000814 !important;
        border: 1px solid #D4AF37 !important;
        color: #D4AF37 !important;
        padding: 10px !important;
        border-radius: 8px !important;
    }
    [data-testid="stMetric"] label, .stMetric label { color: var(--gold-grey) !important; }
    [data-testid="stMetric"] [data-testid="stMetricValue"] { color: #D4AF37 !important; }
    .stAlert, [data-testid="stAlert"] {
        background-color: rgba(0, 8, 20, 0.98) !important;
        border: 1px solid #D4AF37 !important;
        color: var(--gold-grey) !important;
    }
    .stButton > button {
        background-color: rgba(0, 29, 61, 0.9) !important;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important;
    }
    .stButton > button:hover {
        background-color: rgba(212, 175, 55, 0.2) !important;
        border-color: #D4AF37 !important;
        color: #fff !important;
    }
    /* System Online pulse (Sovereign Activation) */
    @keyframes system-online-pulse {
        0%, 100% { opacity: 0.9; box-shadow: 0 0 12px #D4AF37; }
        50% { opacity: 1; box-shadow: 0 0 28px #D4AF37, 0 0 40px rgba(212, 175, 55, 0.4); }
    }
    .system-online-pulse {
        display: inline-block;
        padding: 8px 20px;
        background: rgba(0, 8, 20, 0.95);
        border: 1px solid #D4AF37;
        border-radius: 8px;
        color: #D4AF37;
        font-weight: 700;
        animation: system-online-pulse 1.5s ease-in-out infinite;
    }
    /* D3 Research Strike — Active Scan overlay (shimmering) */
    .d3-active-scan {
        position: relative;
    }
    .d3-active-scan::after {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(105deg, transparent 0%, rgba(255, 215, 0, 0.06) 45%, rgba(255, 215, 0, 0.12) 50%, rgba(255, 215, 0, 0.06) 55%, transparent 100%);
        background-size: 200% 100%;
        animation: active-scan-shimmer 2.5s ease-in-out infinite;
        pointer-events: none;
        border-radius: 8px;
    }
    @keyframes active-scan-shimmer {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    .active-scan-label {
        position: absolute;
        top: 8px;
        right: 12px;
        font-size: 0.7rem;
        color: #FFD700;
        letter-spacing: 0.1em;
        animation: gec-diamond-shimmer 2s infinite;
        z-index: 2;
    }
    /* Welcome message — shimmering CSS text */
    @keyframes welcome-shimmer {
        0%, 100% { color: #FFF; text-shadow: 0 0 10px #FFF, 0 0 20px rgba(212, 175, 55, 0.4); }
        50% { color: #D4AF37; text-shadow: 0 0 16px #D4AF37, 0 0 32px rgba(212, 175, 55, 0.7); }
    }
    .welcome-shimmer {
        animation: welcome-shimmer 2.5s ease-in-out infinite;
        font-weight: 700;
        font-size: clamp(0.95rem, 2.2vw, 1.15rem);
        text-align: center;
        margin-bottom: 16px;
    }
    /* Sovereign Activation Alert — status-bar feel */
    .activation-alert {
        background: linear-gradient(90deg, rgba(0, 8, 20, 0.98) 0%, rgba(0, 29, 61, 0.6) 100%);
        border: 1px solid rgba(255, 215, 0, 0.4);
        border-radius: 6px;
        padding: 8px 16px;
        margin: 8px 0;
        text-align: center;
        font-size: 0.8rem;
    }
    .activation-alert .alert-heading {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #D4AF37;
        font-weight: 700;
        margin: 0;
    }
    /* INITIATE RESET button — Red background + Gold Shimmer border */
    .stButton > button {
        background-color: #c0392b !important;
        background: #c0392b !important;
        color: #fff !important;
        border: 2px solid #D4AF37 !important;
        box-shadow: 0 0 12px rgba(212, 175, 55, 0.5) !important;
    }
    .stButton > button:hover {
        border-color: #f6e27a !important;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.7) !important;
    }
    /* ACTIVE SCAN mode — when INITIATE RESET clicked, dashboard transitions */
    .active-scan-mode-banner {
        position: sticky;
        top: 0;
        left: 0;
        right: 0;
        padding: 8px 16px;
        background: rgba(0, 8, 20, 0.98);
        border-bottom: 2px solid #D4AF37;
        color: #D4AF37;
        font-weight: 700;
        text-align: center;
        z-index: 100;
        animation: active-scan-pulse 2s ease-in-out infinite;
    }
    @keyframes active-scan-pulse {
        0%, 100% { box-shadow: 0 4px 20px rgba(212, 175, 55, 0.2); }
        50% { box-shadow: 0 4px 28px rgba(212, 175, 55, 0.5); }
    }
    /* All widget headings UPPERCASE, 25% reduced font (Kwas-Kwas) */
    .widget-heading {
        text-transform: uppercase !important;
        letter-spacing: 0.04em;
        color: #D4AF37;
        font-weight: 700;
        font-size: 0.75em !important;
    }
    .sovereign-header { font-size: 0.825rem !important; }
    /* NGECC flow: Raw Coal = Blue Oval, Gasifier = Gold Box, Syngas = Pulsing Gold Box */
    .flow-raw-coal {
        background: linear-gradient(145deg, #1e3a5f 0%, #0d2137 100%);
        border: 2px solid #4a90d9;
        border-radius: 50%;
        padding: 16px 24px;
        text-align: center;
        color: #fff;
        min-width: 100px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }
    .flow-raw-coal .label { color: #a8d0ff; font-weight: bold; font-size: 0.85rem; }
    .flow-gasifier {
        background: rgba(0, 0, 80, 0.95);
        border: 2px solid #D4AF37;
        border-radius: 10px;
        padding: 16px 24px;
        text-align: center;
        color: #D4AF37;
        font-weight: bold;
        min-width: 100px;
    }
    .flow-syngas {
        background: rgba(0, 0, 80, 0.95);
        border: 2px solid #D4AF37;
        border-radius: 10px;
        padding: 16px 24px;
        text-align: center;
        color: #fff;
        min-width: 100px;
        animation: diamond-pulse 2s ease-in-out infinite;
    }
    .flow-syngas .label { color: #D4AF37; font-weight: bold; }
    /* Global Silicon Scarcity ticker (KWAS-KWAS D3 RESEARCH) */
    @keyframes ticker-pulse {
        0%, 100% { opacity: 0.85; border-color: rgba(212, 175, 55, 0.6); }
        50% { opacity: 1; border-color: #D4AF37; box-shadow: 0 0 20px rgba(212, 175, 55, 0.3); }
    }
    .silicon-ticker {
        background: linear-gradient(90deg, rgba(0,0,80,0.9) 0%, rgba(212,175,55,0.08) 50%, rgba(0,0,80,0.9) 100%);
        border: 1px solid #D4AF37;
        border-radius: 8px;
        padding: 10px 16px;
        text-align: center;
        color: #D4AF37;
        font-weight: 700;
        font-size: 0.9rem;
        animation: ticker-pulse 2s ease-in-out infinite;
    }
    .sovereign-signature {
        border-top: 1px solid #FFD700;
        margin-top: 50px;
        padding: 20px;
        text-align: center;
        background: linear-gradient(to right, transparent, rgba(255, 215, 0, 0.05), transparent);
    }
    /* NRRFC Value-Extraction Engine — Deep Navy #000080, Metallic Gold #D4AF37, S24-friendly */
    .nrrfc-module {
        background: linear-gradient(180deg, #000080 0%, #000050 100%);
        border: 2px solid #D4AF37;
        border-radius: 12px;
        padding: 24px;
        margin: 20px 0;
        max-width: 100%;
    }
    .nrrfc-title {
        color: #D4AF37;
        font-weight: 800;
        text-align: center;
        margin-bottom: 20px;
        font-size: clamp(1rem, 2.5vw, 1.4rem);
    }
    @keyframes diamond-pulse {
        0%, 100% { opacity: 0.9; transform: scale(1); box-shadow: 0 0 12px #D4AF37; }
        50% { opacity: 1; transform: scale(1.05); box-shadow: 0 0 24px #FFF, 0 0 36px rgba(212, 175, 55, 0.6); }
    }
    .diamond-bridge {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
        gap: 8px;
        margin: 12px 0;
    }
    .diamond-node {
        width: 14px;
        height: 14px;
        background: linear-gradient(135deg, #FFF 0%, #D4AF37 100%);
        transform: rotate(45deg);
        animation: diamond-pulse 2s ease-in-out infinite;
    }
    .diamond-node:nth-child(2) { animation-delay: 0.2s; }
    .diamond-node:nth-child(3) { animation-delay: 0.4s; }
    .diamond-node:nth-child(4) { animation-delay: 0.6s; }
    .flow-step {
        background: rgba(0, 0, 80, 0.9);
        border: 1px solid #D4AF37;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        color: #fff;
        min-width: 100px;
    }
    .flow-step .label { color: #D4AF37; font-weight: bold; font-size: 0.85rem; }
    .flow-arrow { color: #D4AF37; font-size: 1.5rem; margin: 0 4px; }
    .sovereign-feedstock { color: #D4AF37 !important; font-weight: bold; animation: diamond-pulse 2.5s infinite; }
    .nrrfc-footer {
        border-top: 1px solid #D4AF37;
        margin-top: 24px;
        padding-top: 16px;
        text-align: center;
        color: #e0e0e0;
        font-size: 0.95rem;
    }
    /* 8R CIRCULAR CYCLE — 350px, dashed gold path, hollow nodes (purge white) */
    .circle-container {
        position: relative;
        width: 350px;
        height: 350px;
        margin: 24px auto;
        border: 1px dashed #D4AF37;
        border-radius: 50%;
        background: transparent !important;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.25);
    }
    .circle-container .node {
        position: absolute;
        left: 50%;
        top: 50%;
        width: 80px;
        height: 80px;
        margin-left: -40px;
        margin-top: -40px;
        background: transparent !important;
        background-color: transparent !important;
        border: 2px solid #D4AF37 !important;
        color: #D4AF37 !important;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 10px;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 0 12px rgba(212, 175, 55, 0.35);
        line-height: 1.2;
    }
    .circle-container .node span { display: block; color: #D4AF37 !important; }
    .circle-container .node:hover {
        border-color: #D4AF37 !important;
        box-shadow: 0 0 25px #D4AF37 !important;
    }
    /* D3: RESEARCH node — permanent shimmer pulse (active node) */
    .circle-container .node-d3-active {
        animation: d3-node-shimmer 2s ease-in-out infinite !important;
    }
    @keyframes d3-node-shimmer {
        0%, 100% { box-shadow: 0 0 15px rgba(212, 175, 55, 0.4); border-color: #D4AF37; }
        50% { box-shadow: 0 0 28px #D4AF37, 0 0 40px rgba(212, 175, 55, 0.6); border-color: #f6e27a; }
    }
    /* System Online — gold glow on ALL 8R nodes when INITIATE RESET triggered */
    .circle-container.system-online .node {
        animation: system-online-glow 1.5s ease-in-out infinite !important;
    }
    @keyframes system-online-glow {
        0%, 100% { box-shadow: 0 0 18px rgba(212, 175, 55, 0.5); border-color: #D4AF37; }
        50% { box-shadow: 0 0 32px #D4AF37, 0 0 48px rgba(212, 175, 55, 0.7); border-color: #f6e27a; }
    }
    .r8-circle-wrap { position: relative; width: 400px; height: 400px; margin: 24px auto; }
    .r8-circle-ring { position: absolute; inset: 20px; border: 1px solid rgba(212, 175, 55, 0.4); border-radius: 50%; }
    .r8-circle-node {
        position: absolute; left: 50%; top: 50%; width: 70px; margin-left: -35px; margin-top: -35px;
        text-align: center; background: #000814 !important; border: 1px solid #D4AF37 !important;
        border-radius: 8px; padding: 6px 4px; color: #D4AF37 !important; font-weight: 700; font-size: 0.65rem;
    }
    @keyframes r8-node-shimmer {
        0%, 100% { opacity: 0.9; box-shadow: 0 0 8px rgba(212, 175, 55, 0.3); }
        50% { opacity: 1; box-shadow: 0 0 16px rgba(212, 175, 55, 0.6); }
    }
    </style>
    """, unsafe_allow_html=True)
# ISOLATED UI: entire dashboard in one HTML iframe (no Streamlit sidebar; glossary + 8R SVG + coal table inside)
current_time = time.strftime("%Y-%m-%d %H:%M:%S UTC")
if st.button("🔴 INITIATE RESET - SOVEREIGN ACTIVATION", key="sovereign_activation", use_container_width=True):
    st.session_state["reset_phase_active"] = True
    st.session_state["balloons_shown"] = False
if st.session_state.get("reset_phase_active"):
    st.success("SYSTEM ONLINE: 8R STEALTH CYCLE ACTIVE.")
    if not st.session_state.get("balloons_shown"):
        st.balloons()
        st.session_state["balloons_shown"] = True

dashboard_html = build_sovereign_dashboard_html(current_time, st.session_state.get("reset_phase_active", False))
components.html(dashboard_html, height=1600, scrolling=True)

# SOVEREIGN PULSE HEARTBEAT — full rerun every 1 second
time.sleep(1)
st.rerun()
