"""
GCSLC Sovereign Command Center — High-Fidelity Restoration
Deep Navy (#001f3f) + Shimmering Gold (#D4AF37). No GeoJSON. No generic Gradio boxes.
"""
import base64
import os

import gradio as gr
import plotly.graph_objects as go

ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")
CURSOR_ASSETS = os.path.join(
    os.path.expanduser("~"),
    ".cursor", "projects", "Users-user-Desktop-GCSLC-Sovereign-Gateway", "assets",
)


def _b64(name):
    for p in (ROOT, ASSETS, CURSOR_ASSETS):
        path = os.path.join(p, name)
        if os.path.isfile(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
    return ""


B64_MEDALLION = _b64("medallion.png")
B64_GUARDIAN = _b64("guardian_final.png") or _b64("guardian.png")
B64_FORTRESS = _b64("fortress_final.png") or _b64("fortress.png")
B64_FALCON = _b64("falcon_final.png") or _b64("falcon.png")

# Hard-coded 13 state coordinates (lat, lon). No GeoJSON.
COORDS = [
    ("Enugu", 6.4, 7.5), ("Kogi", 7.8, 6.7), ("Benue", 7.3, 8.8), ("Gombe", 10.3, 11.2),
    ("Delta", 5.5, 5.9), ("Imo", 5.5, 7.1), ("Anambra", 6.2, 7.1), ("Edo", 6.5, 6.0),
    ("Plateau", 9.2, 9.5), ("Nasarawa", 8.5, 8.2), ("Oyo", 8.1, 3.6), ("Ekiti", 7.6, 5.3),
    ("Kwara", 8.8, 4.6),
]
HOVER = "Strategic Reserve Node | Potential: 4.2 Million GPU-Hours/Year."


def build_map():
    lats = [c[1] for c in COORDS]
    lons = [c[2] for c in COORDS]
    names = [c[0] for c in COORDS]
    fig = go.Figure()
    fig.add_trace(
        go.Scattergeo(
            lon=lons, lat=lats,
            text=[f"{n}<br>{HOVER}" for n in names],
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
        margin=dict(r=0, t=0, l=0, b=0), height=420,
        paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e8eef4", size=12),
        hoverlabel=dict(bgcolor="#001f3f", bordercolor="#D4AF37"),
        showlegend=False,
    )
    return fig


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
* { font-family: Inter, sans-serif !important; }
body, .gradio-container, #root, .block, section { background: #001f3f !important; }
.gradio-container {
  background: #001f3f !important;
  border: 1px solid rgba(212,175,55,0.4) !important;
  border-radius: 8px !important;
  padding: 20px !important;
  box-shadow: inset 0 0 60px rgba(0,40,80,0.12) !important;
}
.gradio-container .block { background: transparent !important; border: none !important; }
.gradio-container label { color: #D4AF37 !important; border: none !important; }

@keyframes blue-ray {
  0%, 100% { box-shadow: 0 0 20px rgba(0,120,255,0.5); filter: drop-shadow(0 0 8px rgba(212,175,55,0.4)); }
  50% { box-shadow: 0 0 35px rgba(0,180,255,0.7); filter: drop-shadow(0 0 14px rgba(212,175,55,0.6)); }
}
.medallion-wrap img { max-height: 110px; border-radius: 50%; animation: blue-ray 2.5s ease-in-out infinite; }

@keyframes gold-shimmer { 0%, 100% { color: #B8860B; } 50% { color: #FFD700; } }
.title-gold { color: #D4AF37; animation: gold-shimmer 2.2s ease-in-out infinite; }

@keyframes ticker-scroll { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
@keyframes ticker-pulse { 0%, 100% { color: #cc3333; } 50% { color: #D4AF37; } }
.ticker-wrap { overflow: hidden; padding: 8px 0; border-top: 1px solid rgba(212,175,55,0.3); border-bottom: 1px solid rgba(212,175,55,0.3); }
.ticker-inner { display: inline-block; padding-left: 100%; animation: ticker-scroll 14s linear infinite; white-space: nowrap; font-weight: 700; letter-spacing: 0.1em; }
.ticker-inner span { animation: ticker-pulse 2s ease-in-out infinite; }

.map-wrap { position: relative; min-height: 420px; }
@keyframes falcon-shuttle {
  0% { left: 15%; top: 60px; }
  14% { left: 28%; top: 120px; }
  28% { left: 42%; top: 80px; }
  42% { left: 55%; top: 180px; }
  57% { left: 48%; top: 260px; }
  71% { left: 35%; top: 200px; }
  85% { left: 22%; top: 140px; }
  100% { left: 15%; top: 60px; }
}
.falcon-abs { position: relative; margin-top: -420px; height: 0; overflow: visible; z-index: 10; pointer-events: none; animation: falcon-shuttle 1.2s ease-in-out infinite; left: 15%; top: 60px; }
.falcon-abs img { position: absolute; width: 48px; height: 48px; margin: -24px 0 0 -24px; background: transparent !important; }

.guardian-box { background: #001021; border: 1px solid rgba(212,175,55,0.5); border-radius: 8px; padding: 12px; text-align: center; }
.fortress-box { background: #001021; border: 1px solid rgba(212,175,55,0.5); border-radius: 8px; padding: 14px; margin-top: 16px; }
.signature { color: #D4AF37; font-weight: 600; font-style: italic; position: absolute; bottom: 16px; right: 20px; }

.gradio-container::before {
  content: "GCSLC PROPRIETARY";
  position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-32deg);
  font-size: clamp(1.8rem, 5vw, 3.5rem); font-weight: 700; letter-spacing: 0.2em;
  color: rgba(212, 175, 55, 0.05); z-index: 9998; pointer-events: none;
}
"""

SHIELD_SCRIPT = """
<script>
document.addEventListener('contextmenu', e => e.preventDefault(), true);
document.addEventListener('keydown', function(e) {
  var k = (e.key || '').toLowerCase();
  if ((e.metaKey && e.shiftKey && k === '4') || (e.metaKey && k === 's')) { e.preventDefault(); e.stopPropagation(); }
}, true);
</script>
"""


def header_html():
    img = f'<img src="data:image/png;base64,{B64_MEDALLION}" alt="Medallion" />' if B64_MEDALLION else '<div style="width:100px;height:100px;border:2px solid #D4AF37;border-radius:50%;"></div>'
    return f"""
    <div style="text-align:center; padding: 16px 0 12px 0; background: #001f3f;">
      <div class="medallion-wrap" style="margin-bottom: 10px;">{img}</div>
      <h1 class="title-gold" style="font-size: 1.05rem; font-weight: 700; letter-spacing: 0.14em; margin: 0; line-height: 1.35;">
        GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION - GCSLC LTD/GTE
      </h1>
    </div>
    """


def ticker_html():
    return """
    <div class="ticker-wrap">
      <div class="ticker-inner"><span>NATIONAL ASSET RECOVERY DELAY COST: $1.87 BILLION/YEAR LOSS — RECOVERING VIA 8R STEALTH PARADIGM. </span><span>NATIONAL ASSET RECOVERY DELAY COST: $1.87 BILLION/YEAR LOSS — RECOVERING VIA 8R STEALTH PARADIGM. </span></div>
    </div>
    """


def guardian_html():
    if not B64_GUARDIAN:
        return '<div class="guardian-box"><p style="color:#D4AF37;">Guardian</p></div>'
    return f'''
    <div class="guardian-box">
      <img src="data:image/png;base64,{B64_GUARDIAN}" alt="Guardian" style="max-width:100%; max-height:220px; display:block; margin:0 auto;" />
      <p style="color:#FF8C00; font-weight:700; font-size:0.9rem; margin:10px 0 0 0;">I NEED ENERGY TO THRIVE</p>
    </div>
    '''


def fortress_html():
    if not B64_FORTRESS:
        return '<div class="fortress-box"><p style="color:#D4AF37;">Desert Dragon — TIER-III/IV HYPERSCALE</p></div>'
    return f'''
    <div class="fortress-box">
      <p style="color:#D4AF37; font-size:0.85rem; margin:0 0 8px 0;">DESERT DRAGON — TIER-III/IV HYPERSCALE</p>
      <img src="data:image/png;base64,{B64_FORTRESS}" alt="Fortress" style="width:100%; max-height:200px; object-fit:cover; border-radius:6px;" />
    </div>
    '''


def falcon_overlay_html():
    if not B64_FALCON:
        return '<div class="falcon-abs"><span style="font-size:32px;">&#9726;</span></div>'
    return f'<div class="falcon-abs"><img src="data:image/png;base64,{B64_FALCON}" alt="Falcon" /></div>'


with gr.Blocks(theme=gr.themes.Base(primary_hue="amber").set(body_background_fill="#001f3f", block_background_fill="#001f3f"), css=CSS) as demo:
    gr.HTML(SHIELD_SCRIPT)
    gr.HTML(header_html())
    gr.HTML(ticker_html())
    with gr.Row():
        with gr.Column(scale=3):
            gr.HTML('<p style="color:#D4AF37; font-weight:600; font-size:0.9rem; margin:0 0 6px 0;">Sovereign Radar — 13 Coal States</p>')
            gr.HTML('<div class="map-wrap">')
            gr.Plot(build_map(), label="")
            gr.HTML(falcon_overlay_html() + "</div>")
        with gr.Column(scale=1):
            gr.HTML(guardian_html())
    gr.HTML(fortress_html())
    gr.HTML(
        '<div style="position:relative; min-height:60px; padding: 16px 0 50px 0; border-top: 1px solid rgba(212,175,55,0.35);">'
        '<p class="signature">Dr. Sa\'ad Jaafaru, Chairman & Founder</p>'
        '<p style="color:#8899aa; font-size:0.8rem; position:absolute; bottom:8px; right:20px;">GCSLC LTD/GTE</p>'
        '</div>'
    )

if __name__ == "__main__":
    demo.launch(share=True)
