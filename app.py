"""
GCSLC SOVEREIGN COMMAND GATEWAY — Vision-Enhanced
THE SOVEREIGN RESET DIRECTIVE
Goldman Sachs-tier Institutional Dashboard.
Official: GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION - GCSLC LTD/GTE
"""
import base64
import os
import time
from typing import Optional

try:
    import huggingface_hub
    if not hasattr(huggingface_hub, "HfFolder"):
        class HfFolder:
            @staticmethod
            def get_token() -> Optional[str]:
                try:
                    from huggingface_hub import get_token
                    return get_token()
                except Exception:
                    return None
            @staticmethod
            def save_token(token: str) -> None:
                try:
                    from huggingface_hub import set_token
                    set_token(token)
                except Exception:
                    pass
        setattr(huggingface_hub, "HfFolder", HfFolder)
except Exception:
    pass

import gradio as gr
import plotly.graph_objects as go

# --- PATHS & ASSETS ---
ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")


def _load_b64(name: str) -> str:
    path = os.path.join(ASSETS, name)
    if os.path.isfile(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""


B64_MEDALLION = _load_b64("medallion.png")
B64_GUARDIAN = _load_b64("guardian.png")
B64_FORTRESS = _load_b64("fortress.png")
B64_FALCON = _load_b64("falcon.png")

# --- HARD-CODED SOVEREIGN MAP: 13 Coal States (lat, lon) ---
COAL_STATES_COORDS = [
    ("Enugu", 6.4, 7.5),
    ("Kogi", 7.8, 6.7),
    ("Benue", 7.3, 8.8),
    ("Gombe", 10.3, 11.2),
    ("Delta", 5.5, 5.9),
    ("Imo", 5.5, 7.1),
    ("Anambra", 6.2, 7.1),
    ("Edo", 6.5, 6.0),
    ("Plateau", 9.2, 9.5),
    ("Nasarawa", 8.5, 8.2),
    ("Oyo", 8.1, 3.6),
    ("Ekiti", 7.6, 5.3),
    ("Kwara", 8.8, 4.6),
]
HOVER_TEXT = "Strategic Reserve Node | Byproducts: Germanium, Silicon, Ammonia"


def create_sovereign_map():
    """Plotly scatter map of Nigeria — 13 coal states, golden diamond markers. No GeoJSON."""
    lats = [c[1] for c in COAL_STATES_COORDS]
    lons = [c[2] for c in COAL_STATES_COORDS]
    names = [c[0] for c in COAL_STATES_COORDS]

    fig = go.Figure()
    fig.add_trace(
        go.Scattergeo(
            lon=lons,
            lat=lats,
            text=[f"{n}<br>{HOVER_TEXT}" for n in names],
            hoverinfo="text",
            mode="markers",
            marker=dict(
                size=18,
                symbol="diamond",
                color="#D4AF37",
                line=dict(width=2, color="#FFD700"),
            ),
            name="Strategic Reserve",
        )
    )
    fig.update_geos(
        center=dict(lat=9.08, lon=8.0),
        scope="africa",
        visible=True,
        showcountries=True,
        countrycolor="rgba(0,32,96,0.6)",
        showland=True,
        landcolor="rgba(0,31,63,0.4)",
        showocean=True,
        oceancolor="rgba(0,20,50,0.5)",
        lataxis=dict(range=[4, 14]),
        lonaxis=dict(range=[2.5, 15]),
    )
    fig.update_layout(
        title="",
        margin=dict(r=0, t=0, l=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        geo=dict(bgcolor="rgba(0,0,0,0)"),
        height=440,
        font=dict(family="Inter, Roboto, sans-serif", color="#e8eef4", size=12),
        hoverlabel=dict(
            bgcolor="#001f3f",
            font_size=12,
            bordercolor="#D4AF37",
            font_family="Inter, Roboto, sans-serif",
        ),
        showlegend=False,
    )
    return fig


def get_monthly_projections():
    """Total Monthly Projections for Coal, Germanium, Silicon."""
    t = time.time()
    seed = int(t) % 86400

    def _v(lo, hi, off=0):
        x = abs(hash(str(seed + off))) % 100
        return lo + (x / 100.0) * (hi - lo)

    return [
        {"commodity": "Coal", "monthly_proj_usd_m": round(18.5 * _v(0.95, 1.05, 0), 1)},
        {"commodity": "Germanium", "monthly_proj_usd_m": round(22.0 * _v(0.95, 1.05, 1), 1)},
        {"commodity": "Silicon", "monthly_proj_usd_m": round(6.5 * _v(0.95, 1.05, 2), 1)},
    ]


# --- GATEWAY CSS: Diagonal watermark, Inter/Roboto, medallion blue-ray, guardian coal glow, falcon 1.2s pulse, fortress, signature ---
GATEWAY_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Roboto:wght@400;500;700&display=swap');
* { font-family: 'Inter', 'Roboto', sans-serif !important; }

/* Diagonal watermark across entire UI */
.gradio-container::before {
  content: 'GCSLC PROPRIETARY - SOVEREIGN INTEL';
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(-35deg);
  font-size: clamp(2rem, 6vw, 4rem);
  font-weight: 700;
  letter-spacing: 0.25em;
  color: rgba(212, 175, 55, 0.06);
  white-space: nowrap;
  z-index: 9997;
  pointer-events: none;
  font-family: 'Inter', 'Roboto', sans-serif;
}

body, .gradio-container, .contain, #root, .block, .wrap, section { background: #001f3f !important; }
.gradio-container {
  border: 4px solid #D4AF37 !important;
  border-radius: 16px !important;
  padding: 20px !important;
  box-shadow: 0 0 40px rgba(212,175,55,0.25), inset 0 0 60px rgba(0,80,160,0.08) !important;
}

/* Medallion: top center, blue-ray aura */
@keyframes medallion-blue-ray {
  0%, 100% { box-shadow: 0 0 20px rgba(0,120,255,0.5), 0 0 40px rgba(0,150,255,0.25); filter: drop-shadow(0 0 8px rgba(212,175,55,0.4)); }
  50% { box-shadow: 0 0 35px rgba(0,180,255,0.7), 0 0 55px rgba(0,200,255,0.4); filter: drop-shadow(0 0 14px rgba(212,175,55,0.6)); }
}
.medallion-wrap img {
  max-height: 120px;
  border-radius: 50%;
  animation: medallion-blue-ray 2.5s ease-in-out infinite;
}

/* Guardian: "I NEED ENERGY TO THRIVE" — coal-fire orange glow */
@keyframes prism-text-coal {
  0% { filter: drop-shadow(0 0 8px rgba(255,140,0,0.8)); text-shadow: 0 0 12px rgba(255,140,0,0.6); }
  100% { filter: drop-shadow(0 0 14px rgba(255,165,0,0.95)); text-shadow: 0 0 18px rgba(255,165,0,0.8); }
}
.guardian-prism-text {
  color: #FF8C00;
  font-weight: 700;
  font-size: 1.1rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  animation: prism-text-coal 2s ease-in-out infinite alternate;
}

/* Falcon: floats over map, 1.2s shouting pulse, no white background */
@keyframes falcon-shouting {
  0%, 100% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.15); }
}
.falcon-overlay-map {
  position: absolute;
  left: 78%;
  top: 48%;
  z-index: 10;
  pointer-events: none;
}
.falcon-overlay-map img {
  height: 72px;
  animation: falcon-shouting 1.2s ease-in-out infinite;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}
.map-wrap-sovereign { position: relative; min-height: 440px; }

/* Fortress as background for Convergence Metrics */
.convergence-metrics-wrap {
  position: relative;
  border: 3px solid #D4AF37;
  border-radius: 12px;
  overflow: hidden;
  background: #001f3f !important;
}
.convergence-metrics-wrap .fortress-bg {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  opacity: 0.15;
  pointer-events: none;
}
.convergence-metrics-wrap .fortress-content { position: relative; z-index: 1; padding: 24px; }

/* Signature: gold-shimmer calligraphy */
@keyframes gold-shimmer {
  0%, 100% { text-shadow: 0 0 12px rgba(212,175,55,0.6); }
  50% { text-shadow: 0 0 20px rgba(212,175,55,0.9); }
}
.signature-calligraphy {
  color: #D4AF37;
  font-size: 1.15rem;
  font-weight: 600;
  font-style: italic;
  animation: gold-shimmer 2.5s ease-in-out infinite;
  position: absolute;
  bottom: 24px;
  right: 24px;
  font-family: 'Inter', 'Roboto', serif;
}
"""


def build_header_html():
    """Official name + medallion top center with blue-ray aura."""
    medallion_img = (
        f'<img src="data:image/png;base64,{B64_MEDALLION}" alt="GCSLC Medallion" />'
        if B64_MEDALLION
        else '<div style="width:120px;height:120px;border:3px solid #D4AF37;border-radius:50%;margin:0 auto;"></div>'
    )
    return f"""
    <div style="text-align: center; padding: 16px 0 12px 0;">
        <h1 style="color: #D4AF37; font-size: 1.25rem; font-weight: 700; letter-spacing: 0.1em; margin: 0 0 8px 0; line-height: 1.35;">
            GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION
        </h1>
        <p style="color: #b8c4ce; font-size: 0.95rem; margin: 4px 0; letter-spacing: 0.06em;">
            GCSLC LTD/GTE
        </p>
        <div class="medallion-wrap" style="margin: 16px 0;">
            {medallion_img}
        </div>
    </div>
    """


def build_guardian_html():
    """Guardian on right flank + 'I NEED ENERGY TO THRIVE' in coal-fire orange glow."""
    if not B64_GUARDIAN:
        return """
        <div style="background: #001f3f; border: 3px solid #D4AF37; border-radius: 12px; padding: 20px; text-align: center;">
            <div style="font-size: 48px;">🛡️</div>
            <p class="guardian-prism-text">I NEED ENERGY TO THRIVE</p>
        </div>
        """
    return f"""
    <div style="background: #001f3f; border: 3px solid #D4AF37; border-radius: 12px; padding: 16px; text-align: center;">
        <img src="data:image/png;base64,{B64_GUARDIAN}" alt="Guardian" style="max-width: 100%; max-height: 180px; display: block; margin: 0 auto;" />
        <p class="guardian-prism-text" style="margin: 12px 0 0 0;">I NEED ENERGY TO THRIVE</p>
    </div>
    """


def build_falcon_html():
    if not B64_FALCON:
        return '<span style="font-size:48px;">🦅</span>'
    return f'<img src="data:image/png;base64,{B64_FALCON}" alt="Falcon" style="max-height: 100%; background: transparent !important;" />'


def build_convergence_metrics_html():
    """Convergence Metrics: fortress background + clean table (Coal, Germanium, Silicon)."""
    rows = get_monthly_projections()
    total = sum(r["monthly_proj_usd_m"] for r in rows)
    fortress_bg = ""
    if B64_FORTRESS:
        fortress_bg = f'<div class="fortress-bg" style="background-image: url(\'data:image/png;base64,{B64_FORTRESS}\');"></div>'
    table_rows = "".join(
        f"<tr><td style='padding:10px 16px; color:#e8eef4;'>{r['commodity']}</td><td style='padding:10px 16px; color:#D4AF37; font-weight:600;'>${r['monthly_proj_usd_m']}M</td></tr>"
        for r in rows
    )
    return f"""
    <div class="convergence-metrics-wrap">
        {fortress_bg}
        <div class="fortress-content">
            <h3 style="color: #D4AF37; margin: 0 0 16px 0; letter-spacing: 0.1em;">Convergence Metrics</h3>
            <table style="width: 100%; border-collapse: collapse; color: #e8eef4;">
                <thead>
                    <tr><th style="text-align:left; padding:10px 16px; color:#D4AF37;">Commodity</th><th style="text-align:right; padding:10px 16px; color:#D4AF37;">Total Monthly Projection</th></tr>
                </thead>
                <tbody>
                    {table_rows}
                    <tr><td style="padding:12px 16px; font-weight:700; color:#e8eef4;">Total</td><td style="padding:12px 16px; color:#D4AF37; font-weight:700;">${total:.1f}M</td></tr>
                </tbody>
            </table>
        </div>
    </div>
    """


with gr.Blocks(
    theme=gr.themes.Base(primary_hue="amber", secondary_hue="blue").set(
        body_background_fill="#001f3f",
        block_background_fill="#001f3f",
        block_border_color="#D4AF37",
        block_label_text_color="#D4AF37",
        block_title_text_color="#D4AF37",
    ),
    css=GATEWAY_CSS,
) as demo:
    gr.HTML(
        '<div style="position:fixed; bottom:10px; right:14px; font-size:0.7rem; color:rgba(212,175,55,0.35); letter-spacing:0.12em; z-index:9998; pointer-events:none;">GCSLC PROPRIETARY - SOVEREIGN INTEL</div>'
    )

    gr.HTML(build_header_html())

    with gr.Row():
        with gr.Column(scale=3):
            gr.HTML(
                "<p style='color:#D4AF37; margin:0 0 8px 0; font-weight:600; font-size:0.95rem;'>Sovereign Map — 13 Coal States (Strategic Reserve Nodes)</p>"
            )
            gr.HTML('<div class="map-wrap-sovereign">')
            gr.Plot(create_sovereign_map(), label="")
            falcon_overlay = (
                f'<div class="falcon-overlay-map" style="margin-top:-440px;height:0;overflow:visible;">{build_falcon_html()}</div></div>'
                if B64_FALCON
                else '<div class="falcon-overlay-map" style="margin-top:-440px;height:0;overflow:visible;"><span style="font-size:48px;">🦅</span></div></div>'
            )
            gr.HTML(falcon_overlay)

        with gr.Column(scale=1):
            gr.HTML(build_guardian_html())

    gr.HTML(build_convergence_metrics_html())

    _footer = (
        '<div style="position: relative; min-height: 80px; padding: 20px 0 70px 0; border-top: 1px solid rgba(212,175,55,0.4); margin-top: 24px;">'
        '<p class="signature-calligraphy">Dr. Sa\'ad Jaafaru, Chairman & Founder</p>'
        '<p style="color: #b8c4ce; font-size: 0.85rem; margin: 4px 0 0 0; position: absolute; bottom: 10px; right: 24px;">GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION — GCSLC LTD/GTE</p>'
        '</div>'
    )
    gr.HTML(_footer)


if __name__ == "__main__":
    demo.launch()
