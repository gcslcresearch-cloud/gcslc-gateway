"""
THE GCSLC SOVEREIGN COMMAND GATEWAY — FINAL DIRECTIVE
Goldman Sachs-tier institutional dashboard for:
GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION - GCSLC LTD/GTE
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

# --- PATHS & ASSETS (root-first, then Cursor assets) ---
ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS_ROOT = os.path.join(ROOT, "assets")
CURSOR_ASSETS = os.path.join(
    os.path.expanduser("~"),
    ".cursor",
    "projects",
    "Users-user-Desktop-GCSLC-Sovereign-Gateway",
    "assets",
)


def _load_b64_from_candidates(names) -> str:
    for name in names:
        if not name:
            continue
        # 1) try root directory directly
        root_path = os.path.join(ROOT, name)
        if os.path.isfile(root_path):
            with open(root_path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        # 2) try assets/ under root
        assets_path = os.path.join(ASSETS_ROOT, name)
        if os.path.isfile(assets_path):
            with open(assets_path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        # 3) try Cursor-side assets mirror
        cursor_path = os.path.join(CURSOR_ASSETS, name)
        if os.path.isfile(cursor_path):
            with open(cursor_path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
    return ""


# Medallion and Falcon from project root; high-fidelity Guardian & Fortress from user images
B64_MEDALLION = _load_b64_from_candidates(["medallion.png"])
B64_FALCON = _load_b64_from_candidates(["falcon.png"])
B64_GUARDIAN_HF = _load_b64_from_candidates(
    [
        "guardian_hf.png",
        "Screenshot_20260311_181838_Gallery-ac54866c-be0b-40d0-b6b9-a8fdceee1b42.png",
        "guardian.png",
    ]
)
B64_FORTRESS_HF = _load_b64_from_candidates(
    [
        "fortress_hf.png",
        "Screenshot_20260311_181741_Gallery-30cf1785-4547-482a-8222-bb593a70cd40.png",
        "fortress.png",
    ]
)

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
HOVER_TEXT = (
    "Strategic Reserve Node | Energy Potential: "
    "4.2 Million GPU-Hours/Year (NVIDIA H100 Clusters)"
)


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


def _logic_terminal_lines():
    base = [
        "Analyzing_Revolution_Determinants...",
        "Sovereign_Wealth_Cloud_Syncing...",
        "8R_Paradigm_Lock_Engaged.",
    ]
    t = int(time.time())
    suffix = f"T{t % 100000:05d}"
    return [f"{line}  [{suffix}]" for line in base]


# --- GATEWAY CSS: watermark, fonts, medallion, guardian, falcon, fortress, ticker, logic terminal, signature ---
GATEWAY_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Roboto:wght@400;500;700&display=swap');
* { font-family: 'Inter', 'Roboto', sans-serif !important; }

/* Diagonal watermark across entire UI */
.gradio-container::before {
  content: 'GCSLC PROPRIETARY - SOVEREIGN INTEL - DR. SA’AD JAAFARU';
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) rotate(-35deg);
  font-size: clamp(2rem, 6vw, 4rem);
  font-weight: 700;
  letter-spacing: 0.25em;
  color: rgba(212, 175, 55, 0.05);
  white-space: nowrap;
  z-index: 9997;
  pointer-events: none;
}

body, .gradio-container, .contain, #root, .block, .wrap, section { background: #001f3f !important; }
.gradio-container {
  border: 4px solid #D4AF37 !important;
  border-radius: 16px !important;
  padding: 20px !important;
  box-shadow: 0 0 40px rgba(212,175,55,0.25), inset 0 0 60px rgba(0,80,160,0.08) !important;
}

/* Medallion: top center, rhythmic blue-ray pulse */
@keyframes medallion-blue-ray {
  0%, 100% { box-shadow: 0 0 20px rgba(0,120,255,0.5), 0 0 40px rgba(0,150,255,0.25); filter: drop-shadow(0 0 8px rgba(212,175,55,0.4)); }
  50% { box-shadow: 0 0 35px rgba(0,180,255,0.7), 0 0 55px rgba(0,200,255,0.4); filter: drop-shadow(0 0 14px rgba(212,175,55,0.6)); }
}
.medallion-wrap img {
  max-height: 120px;
  border-radius: 50%;
  animation: medallion-blue-ray 2.5s ease-in-out infinite;
}

/* Guardian narrative text: coal-fire orange glow */
@keyframes prism-text-coal {
  0% { filter: drop-shadow(0 0 8px rgba(255,140,0,0.8)); text-shadow: 0 0 12px rgba(255,140,0,0.6); }
  100% { filter: drop-shadow(0 0 14px rgba(255,165,0,0.95)); text-shadow: 0 0 18px rgba(255,165,0,0.8); }
}
.guardian-prism-text {
  color: #FF8C00;
  font-weight: 700;
  font-size: 1.05rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  animation: prism-text-coal 2s ease-in-out infinite alternate;
}

/* Falcon: floats over map, 1.2s shouting pulse, no white background */
@keyframes falcon-shouting {
  0%, 100% { transform: translate(-50%, -50%) scale(1); }
  50% { transform: translate(-50%, -50%) scale(1.15); }
}
.map-wrap-sovereign { position: relative; min-height: 440px; }
.falcon-overlay-map {
  position: absolute;
  left: 78%;
  top: 46%;
  z-index: 10;
  pointer-events: none;
}
.falcon-overlay-map img {
  height: 80px;
  animation: falcon-shouting 1.2s ease-in-out infinite;
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}

/* Fortress / Convergence Metrics wrap */
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
  opacity: 0.16;
  pointer-events: none;
}
.convergence-metrics-wrap .fortress-content { position: relative; z-index: 1; padding: 24px; }

/* Arbitrage ticker */
@keyframes ticker-scroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
@keyframes ticker-color {
  0%, 100% { color: #ff4444; }
  50% { color: #D4AF37; }
}
.arbitrage-ticker-shell {
  overflow: hidden;
  border-radius: 999px;
  border: 1px solid rgba(212,175,55,0.6);
  background: radial-gradient(circle at center, rgba(50,0,0,0.7), rgba(0,0,0,0.8));
}
.arbitrage-ticker-inner {
  display: inline-block;
  padding-left: 100%;
  animation: ticker-scroll 25s linear infinite;
  font-size: 0.9rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  animation-timing-function: linear;
  white-space: nowrap;
}
.arbitrage-ticker-inner span { animation: ticker-color 2.4s ease-in-out infinite; }

/* 8R Logic Terminal */
.logic-terminal {
  background: radial-gradient(circle at top left, rgba(0,120,60,0.35), rgba(0,0,0,0.9));
  border-radius: 12px;
  border: 2px solid rgba(0,255,128,0.6);
  padding: 14px 16px;
  font-family: "SF Mono", Menlo, Monaco, Consolas, monospace;
  color: #00ff9c;
  font-size: 0.8rem;
  position: relative;
  overflow: hidden;
}
.logic-terminal::before {
  content: 'GCSLC PROPRIETARY';
  position: absolute;
  top: 6px;
  right: 10px;
  font-size: 0.6rem;
  letter-spacing: 0.16em;
  color: rgba(0,255,128,0.6);
}
@keyframes terminal-scan {
  0% { opacity: 0; transform: translateY(8px); }
  50% { opacity: 1; transform: translateY(0); }
  100% { opacity: 0.4; transform: translateY(-6px); }
}
.logic-line {
  animation: terminal-scan 3s ease-in-out infinite;
}
.logic-line:nth-child(2) { animation-delay: 0.7s; }
.logic-line:nth-child(3) { animation-delay: 1.4s; }

/* Data blocks label */
.data-block-label {
  font-size: 0.7rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: rgba(212,175,55,0.78);
}

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
    """Institutional identity, shimmering gold official name, medallion top center."""
    medallion_img = (
        f'<img src="data:image/png;base64,{B64_MEDALLION}" alt="GCSLC Medallion" />'
        if B64_MEDALLION
        else '<div style="width:120px;height:120px;border:3px solid #D4AF37;border-radius:50%;margin:0 auto;"></div>'
    )
    return f"""
    <div style="text-align: center; padding: 12px 0 8px 0;">
        <h1 style="color: #D4AF37; font-size: 1.2rem; font-weight: 700; letter-spacing: 0.16em; margin: 0 0 6px 0; line-height: 1.4;">
            GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION - GCSLC LTD/GTE
        </h1>
        <div class="medallion-wrap" style="margin: 12px 0 4px 0;">
            {medallion_img}
        </div>
        <div class="data-block-label" style="margin-top: 6px;">GCSLC PROPRIETARY</div>
    </div>
    """


def build_guardian_html():
    """High-fidelity humanoid guardian with narrative."""
    img_html = (
        f'<img src="data:image/png;base64,{B64_GUARDIAN_HF}" alt="Guardian" '
        'style="max-width: 100%; max-height: 260px; display: block; margin: 0 auto;" />'
        if B64_GUARDIAN_HF
        else '<div style="font-size:48px; text-align:center;">🛡️</div>'
    )
    return f"""
    <div style="background: #001021; border: 3px solid #D4AF37; border-radius: 12px; padding: 14px; text-align: center; position: relative;">
        <div class="data-block-label" style="position:absolute; top:8px; left:14px;">GCSLC PROPRIETARY</div>
        {img_html}
        <p class="guardian-prism-text" style="margin: 12px 4px 4px 4px;">
            I NEED ENERGY TO THRIVE; process the coal and its by-products — they're my power
        </p>
    </div>
    """


def build_falcon_html():
    if not B64_FALCON:
        return '<span style="font-size:48px;">🦅</span>'
    return (
        f'<img src="data:image/png;base64,{B64_FALCON}" alt="Falcon" '
        'style="max-height: 100%; background: transparent !important;" />'
    )


def build_fortress_html():
    """Immersion-cooled data fortress: Desert Dragon label, cyan cooling feel."""
    fortress_bg = ""
    img_html = ""
    if B64_FORTRESS_HF:
        img_html = (
            f'<img src="data:image/png;base64,{B64_FORTRESS_HF}" '
            'alt="DESERT DRAGON – TIER-III/IV HYPERSCALE" '
            'style="width:100%; max-height:260px; object-fit:cover; border-radius:10px;" />'
        )
        fortress_bg = (
            f'background-image: url("data:image/png;base64,{B64_FORTRESS_HF}");'
        )
    return f"""
    <div class="convergence-metrics-wrap" style="margin-top: 18px;">
        <div class="fortress-bg" style="{fortress_bg}"></div>
        <div class="fortress-content">
            <div class="data-block-label">GCSLC PROPRIETARY</div>
            <h3 style="color:#7de3ff; margin: 8px 0 12px 0; letter-spacing:0.12em; font-size:0.95rem;">
                DESERT DRAGON – TIER-III/IV HYPERSCALE (Riyadh/Dubai Prototype)
            </h3>
            {img_html}
        </div>
    </div>
    """


def build_convergence_metrics_html():
    """Convergence Metrics table for Coal, Germanium, Silicon."""
    # Static illustrative values (USD M / month)
    rows = [
        {"commodity": "Coal", "monthly_proj_usd_m": 18.5},
        {"commodity": "Germanium", "monthly_proj_usd_m": 22.0},
        {"commodity": "Silicon", "monthly_proj_usd_m": 6.5},
    ]
    total = sum(r["monthly_proj_usd_m"] for r in rows)
    table_rows = "".join(
        f"<tr><td style='padding:10px 16px; color:#e8eef4;'>{r['commodity']}</td>"
        f"<td style='padding:10px 16px; color:#D4AF37; font-weight:600; text-align:right;'>"
        f"${r['monthly_proj_usd_m']}M</td></tr>"
        for r in rows
    )
    return f"""
    <div class="convergence-metrics-wrap" style="margin-top: 20px;">
        <div class="fortress-bg"></div>
        <div class="fortress-content">
            <div class="data-block-label">GCSLC PROPRIETARY</div>
            <h3 style="color: #D4AF37; margin: 6px 0 14px 0; letter-spacing: 0.1em; font-size:0.95rem;">
                CONVERGENCE METRICS — MONTHLY PROJECTIONS
            </h3>
            <table style="width: 100%; border-collapse: collapse; color: #e8eef4; font-size:0.9rem;">
                <thead>
                    <tr>
                        <th style="text-align:left; padding:8px 16px; color:#D4AF37;">Commodity</th>
                        <th style="text-align:right; padding:8px 16px; color:#D4AF37;">Total Monthly Projection</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                    <tr>
                        <td style="padding:12px 16px; font-weight:700; color:#e8eef4;">Total</td>
                        <td style="padding:12px 16px; color:#D4AF37; font-weight:700; text-align:right;">
                            ${total:.1f}M
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    """


def build_logic_terminal_html():
    lines = _logic_terminal_lines()
    inner = "".join(f"<div class='logic-line'>{line}</div>" for line in lines)
    return f"<div class='logic-terminal'>{inner}</div>"


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
    # Shield script: disable right-click and key combos (Cmd+Shift+4, Cmd+S)
    gr.HTML(
        """
        <script>
        document.addEventListener('contextmenu', function(e) { e.preventDefault(); }, { capture: true });
        document.addEventListener('keydown', function(e) {
            const key = e.key ? e.key.toLowerCase() : '';
            if ((e.metaKey && e.shiftKey && key === '4') || (e.metaKey && key === 's')) {
                e.preventDefault();
                e.stopPropagation();
            }
        }, { capture: true });
        </script>
        """
    )

    gr.HTML(build_header_html())

    # Arbitrage ticker above the map
    gr.HTML(
        """
        <div class="arbitrage-ticker-shell" style="margin: 10px 0 16px 0; padding: 6px 0;">
            <div class="arbitrage-ticker-inner">
                <span>
                NATIONAL ASSET RECOVERY DELAY COST: $1.87 BILLION/YEAR LOSS – RECOVERING VIA 8R STEALTH PARADIGM.
                NATIONAL ASSET RECOVERY DELAY COST: $1.87 BILLION/YEAR LOSS – RECOVERING VIA 8R STEALTH PARADIGM.
                </span>
            </div>
        </div>
        """
    )

    with gr.Row():
        with gr.Column(scale=3):
            gr.HTML(
                "<p style='color:#D4AF37; margin:0 0 8px 0; font-weight:600; "
                "font-size:0.95rem;'>Sovereign Map — 13 Coal States "
                "(Strategic Reserve Nodes)</p>"
            )
            gr.HTML('<div class="map-wrap-sovereign">')
            gr.Plot(create_sovereign_map(), label="")
            falcon_overlay = (
                f'<div class="falcon-overlay-map" '
                f'style="margin-top:-440px;height:0;overflow:visible;">'
                f"{build_falcon_html()}</div></div>"
                if B64_FALCON
                else '<div class="falcon-overlay-map" '
                'style="margin-top:-440px;height:0;overflow:visible;">'
                '<span style="font-size:48px;">🦅</span></div></div>'
            )
            gr.HTML(falcon_overlay)

        with gr.Column(scale=1):
            gr.HTML(build_guardian_html())
            gr.HTML("<div style='height:10px;'></div>")
            gr.HTML(build_logic_terminal_html())

    gr.HTML(build_fortress_html())
    gr.HTML(build_convergence_metrics_html())

    _footer = (
        '<div style="position: relative; min-height: 80px; padding: 20px 0 70px 0; '
        'border-top: 1px solid rgba(212,175,55,0.4); margin-top: 24px;">'
        '<p class="signature-calligraphy">Dr. Sa’ad Jaafaru, Chairman &amp; Founder</p>'
        '<p style="color: #b8c4ce; font-size: 0.85rem; margin: 4px 0 0 0; '
        'position: absolute; bottom: 10px; right: 24px;">'
        "GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION — GCSLC LTD/GTE"
        "</p>"
        "</div>"
    )
    gr.HTML(_footer)

if __name__ == "__main__":
    demo.launch(share=True)
