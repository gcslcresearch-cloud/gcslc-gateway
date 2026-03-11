"""
GCSLC SOVEREIGN COMMAND GATEWAY
Sovereign Systems Architecture — Goldman Sachs-tier institutional aesthetic.
Deep Navy (#001f3f), Shimmering Gold (#D4AF37). Medallion, Guardian Humanoid, NVFC Falcon,
Interactive Grok-style map, Fortress Data Hub, live-nodal streams, watermark & authority.
"""
import base64
import gradio as gr
import plotly.express as px
import pandas as pd
import json
import os
import time
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


# Embed assets as data URLs for HTML
B64_GUARDIAN = _load_b64("guardian.png")
B64_FALCON = _load_b64("falcon.png")
B64_MEDALLION = _load_b64("medallion.png")
B64_FORTRESS = _load_b64("fortress.png")

# --- SOVEREIGN DATA ---
COAL_STATES = [
    "Kogi", "Enugu", "Benue", "Gombe", "Delta", "Imo", "Anambra", "Abia",
    "Edo", "Nasarawa", "Plateau", "Cross River", "Bauchi"
]
LOSS_VAL = "$1.87 Billion/Year"
STATE_RESERVES_MT = {
    "Kogi": 142.0, "Enugu": 168.0, "Benue": 85.0, "Gombe": 62.0, "Delta": 45.0,
    "Imo": 20.0, "Anambra": 27.3, "Abia": 18.0, "Edo": 38.0, "Nasarawa": 22.0,
    "Plateau": 28.0, "Cross River": 13.0, "Bauchi": 25.0,
}
BYPRODUCT_GERMANIUM_USD_KG = 8597
BYPRODUCT_AMMONIA_USD_MT = 430
BYPRODUCT_SILICON_USD_MT = 6500
STATES_36_FCT = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno",
    "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "FCT", "Gombe", "Imo",
    "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos", "Nasarawa",
    "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers", "Sokoto", "Taraba",
    "Yobe", "Zamfara"
]

DETERMINANTS_8R = [
    ("Refine", "Feedstock yield", "$18.2M/mo"),
    ("Reset", "Legacy MW freed", "1,205 MW"),
    ("Research", "Germanium arb", "47.9% YTD"),
    ("Restructure", "Tier-III/IV", "12 nodes"),
    ("Resuscitate", "Idle → active", "639.3 Mt"),
    ("Revitalize", "Jobs 10yr", "1,654/MW"),
    ("Re-engineer", "Dubai port", "Blue Wave"),
    ("Retain", "Sovereign control", "Vision 2050"),
]

FALCON_ALERTS = "  ★  ".join([
    "Kogi: 142 Mt — Germanium arbitrage", "Enugu: 168 Mt — High-grade feedstock",
    "Benue: 85 Mt — Ammonia & Silicon", "Gombe: 62 Mt — Data hub link",
    "Delta: 45 Mt — Port corridor", "Imo: 20 Mt — Byproduct recovery",
    "Anambra: 27.3 Mt — Coal-to-compute", "Abia: 18 Mt — Semiconductor",
    "Edo: 38 Mt — Regional integration", "Nasarawa: 22 Mt — Abuja nexus",
    "Plateau: 28 Mt — Germanium yield", "Cross River: 13 Mt — Export",
    "Bauchi: 25 Mt — North-East hub",
]) * 2


def _geojson_path():
    for p in [os.path.join(ROOT, "ng_state.geojson"), os.path.join(ROOT, "data", "ng_state.geojson")]:
        if os.path.isfile(p):
            return p
    return None


def _hover_text(state: str) -> str:
    if state in COAL_STATES:
        r = STATE_RESERVES_MT.get(state, 0)
        return f"<b>{state}</b><br>Proven reserves: <b>{r:.1f} M tonnes</b><br>Germanium ${BYPRODUCT_GERMANIUM_USD_KG:,.0f}/kg · Ammonia ${BYPRODUCT_AMMONIA_USD_MT:,.0f}/MT · Silicon ${BYPRODUCT_SILICON_USD_MT:,.0f}/MT"
    return f"<b>{state}</b><br>Sovereign Navy"


def create_sovereign_map():
    path = _geojson_path()
    geojson_data = None
    if path:
        try:
            with open(path, encoding="utf-8") as f:
                geojson_data = json.load(f)
        except Exception:
            pass
    if not geojson_data:
        fig = go.Figure()
        fig.update_layout(
            title="Add ng_state.geojson to repo root or data/",
            paper_bgcolor="rgba(0,31,63,0.3)", margin={"r": 0, "t": 40, "l": 0, "b": 0},
            height=440, font=dict(color="#e8eef4"),
            annotations=[dict(text="Upload ng_state.geojson", x=0.5, y=0.5, showarrow=False, xref="paper", yref="paper")]
        )
        return fig
    featureidkey = "properties.name"
    name_to_status = {}
    name_to_hover = {}
    _norm = {"Federal Capital Territory": "FCT", "Abuja": "FCT", "Nassarawa": "Nasarawa"}
    for f in geojson_data.get("features") or []:
        p = f.get("properties") or {}
        name = (p.get("name") or p.get("adm1_name") or p.get("shapeName") or p.get("NAME_1") or "").strip()
        if name:
            can = _norm.get(name, name)
            is_coal = can in COAL_STATES
            name_to_status[name] = "Coal-Rich" if is_coal else "Sovereign Navy"
            name_to_hover[name] = _hover_text(can if is_coal else name)
    if not name_to_status:
        name_to_status = {s: ("Coal-Rich" if s in COAL_STATES else "Sovereign Navy") for s in STATES_36_FCT}
        name_to_hover = {s: _hover_text(s) for s in STATES_36_FCT}
    df = pd.DataFrame({"State": list(name_to_status.keys()), "Status": list(name_to_status.values()),
                       "Hover": [name_to_hover.get(s, _hover_text(s)) for s in name_to_status]})
    fig = px.choropleth(df, geojson=geojson_data, locations="State", featureidkey=featureidkey, color="Status",
                        color_discrete_map={"Coal-Rich": "rgb(212, 175, 55)", "Sovereign Navy": "rgb(0, 32, 96)"},
                        scope="africa", center={"lat": 9.08, "lon": 7.53})
    fig.update_traces(hovertemplate="%{customdata}<extra></extra>", customdata=df["Hover"].tolist())
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,31,63,0.25)", dragmode=False, height=440,
                      font=dict(color="#e8eef4", size=12),
                      hoverlabel=dict(bgcolor="#001f3f", font_size=12, bordercolor="#D4AF37"))
    return fig


def get_market_velocity_nodes():
    t = time.time()
    seed = int(t) % 86400
    def _v(lo, hi, off=0):
        x = abs(hash(str(seed + off))) % 100
        return lo + (x / 100.0) * (hi - lo)
    return [
        {"commodity": "Coal", "unit_price": "$98/t", "volume_kt": round(1200 * _v(0.9, 1.1, 0)), "unit": "kt", "monthly_proj_usd_m": round(18.5 * _v(0.95, 1.05, 1), 1)},
        {"commodity": "Germanium", "unit_price": "$8,597/kg", "volume_kt": round(2.4 * _v(0.9, 1.1, 2), 2), "unit": "t", "monthly_proj_usd_m": round(22.0 * _v(0.95, 1.05, 3), 1)},
        {"commodity": "Silicon", "unit_price": "$6,500/MT", "volume_kt": round(85 * _v(0.9, 1.1, 4)), "unit": "kt", "monthly_proj_usd_m": round(6.5 * _v(0.95, 1.05, 5), 1)},
        {"commodity": "Ammonia", "unit_price": "$430/MT", "volume_kt": round(45 * _v(0.9, 1.1, 6)), "unit": "kt", "monthly_proj_usd_m": round(19.4 * _v(0.95, 1.05, 7), 1)},
        {"commodity": "Semiconductors", "unit_price": "Index 1.24", "volume_kt": "—", "unit": "index", "monthly_proj_usd_m": round(12.0 * _v(0.95, 1.05, 8), 1)},
    ]


def state_popup_html(state: str) -> str:
    if not state or state not in COAL_STATES:
        return "<div class='state-popup' style='border:2px solid #D4AF37; border-radius:12px; padding:16px; background:rgba(0,31,63,0.98); color:#e8eef4;'><p>Select a coal state above.</p></div>"
    r = STATE_RESERVES_MT.get(state, 0)
    return f"""
    <div class="state-popup" style="border:3px solid #D4AF37; border-radius:12px; padding:20px; background:rgba(0,31,63,0.98); color:#e8eef4; box-shadow:0 0 20px rgba(212,175,55,0.3);">
        <div style="color:#D4AF37; font-weight:700; font-size:1.2rem; margin-bottom:10px;">▶ {state}</div>
        <p style="margin:6px 0;"><b>Proven Reserves:</b> {r:.1f} M tonnes</p>
        <p style="margin:6px 0;"><b>Byproduct Market Value:</b></p>
        <p style="margin:4px 0 0 16px;">Germanium: ${BYPRODUCT_GERMANIUM_USD_KG:,.0f}/kg</p>
        <p style="margin:2px 0 0 16px;">Silicon: ${BYPRODUCT_SILICON_USD_MT:,.0f}/MT</p>
        <p style="margin:2px 0 0 16px;">Ammonia: ${BYPRODUCT_AMMONIA_USD_MT:,.0f}/MT</p>
    </div>
    """


# --- GATEWAY CSS ---
GATEWAY_CSS = """
body, .gradio-container, .contain, #root, .block, .wrap, section { background: #001f3f !important; }
.gradio-container {
  border: 4px solid #D4AF37 !important; border-radius: 16px !important; padding: 20px !important;
  animation: prism-shimmer 4s ease-in-out infinite !important;
  box-shadow: 0 0 40px rgba(212,175,55,0.25), inset 0 0 60px rgba(0,80,160,0.08) !important;
}
@keyframes prism-shimmer {
  0%, 100% { border-color: #D4AF37; box-shadow: 0 0 25px rgba(212,175,55,0.35), inset 0 0 40px rgba(0,100,255,0.06); }
  50% { border-color: #7eb8da; box-shadow: 0 0 35px rgba(126,184,218,0.4), inset 0 0 50px rgba(0,120,200,0.08); }
}
@keyframes title-glow { 0%, 100% { text-shadow: 0 0 20px rgba(212,175,55,0.6); opacity: 1; } 50% { text-shadow: 0 0 35px rgba(212,175,55,0.9); opacity: 0.95; } }
@keyframes medallion-pulse { 0%, 100% { transform: scale(1); filter: drop-shadow(0 0 12px rgba(212,175,55,0.5)); } 50% { transform: scale(1.06); filter: drop-shadow(0 0 20px rgba(212,175,55,0.7)); } }
@keyframes letter-pulse { 0%, 100% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.15); opacity: 0.9; } }
@keyframes prism-text { 0% { background-position: 0% 50%; } 100% { background-position: 200% 50%; } }
@keyframes falcon-shout { 0%, 100% { transform: scale(1) rotate(-3deg); filter: drop-shadow(0 0 10px rgba(212,175,55,0.6)); } 50% { transform: scale(1.1) rotate(2deg); filter: drop-shadow(0 0 18px rgba(212,175,55,0.9)); } }
@keyframes blue-ray { 0%, 100% { opacity: 0.6; box-shadow: 0 0 30px rgba(0,150,255,0.4); } 50% { opacity: 1; box-shadow: 0 0 50px rgba(0,200,255,0.6); } }
@keyframes live-node { 0%, 100% { box-shadow: 0 0 12px rgba(212,175,55,0.4); } 50% { box-shadow: 0 0 22px rgba(212,175,55,0.65); } }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.35; } }
@keyframes ticker-scroll { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
.sovereign-title { color: #D4AF37; font-size: 1.1rem; letter-spacing: 0.12em; text-align: center; animation: title-glow 2.5s ease-in-out infinite; font-weight: 700; margin: 0 0 8px 0; }
.medallion-wrap { text-align: center; margin: 16px 0; }
.medallion-wrap img { animation: medallion-pulse 2.2s ease-in-out infinite; max-height: 120px; }
.gcslc-letters { display: inline-flex; gap: 4px; margin-top: 8px; }
.gcslc-letters span { color: #D4AF37; font-weight: 800; font-size: 1.4rem; letter-spacing: 0.2em; animation: letter-pulse 2.2s ease-in-out infinite; }
.gcslc-letters span:nth-child(1) { animation-delay: 0s; } .gcslc-letters span:nth-child(2) { animation-delay: 0.1s; }
.gcslc-letters span:nth-child(3) { animation-delay: 0.2s; } .gcslc-letters span:nth-child(4) { animation-delay: 0.3s; }
.gcslc-letters span:nth-child(5) { animation-delay: 0.4s; }
.prism-text { background: linear-gradient(90deg, #D4AF37, #7eb8da, #D4AF37, #5c9ead, #D4AF37); background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; animation: prism-text 3s linear infinite; font-weight: 700; font-size: 1.1rem; }
.falcon-hover { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); z-index: 10; pointer-events: none; }
.falcon-hover img { height: 80px; animation: falcon-shout 1.8s ease-in-out infinite; }
.fortress-prism { position: relative; border: 3px solid #D4AF37; border-radius: 12px; overflow: hidden; animation: prism-shimmer 4s ease-in-out infinite; }
.fortress-prism::after { content: ''; position: absolute; inset: 0; background: radial-gradient(ellipse at center, transparent 40%, rgba(0,150,255,0.15) 100%); pointer-events: none; animation: blue-ray 2.5s ease-in-out infinite; }
.live-node { animation: live-node 2.5s ease-in-out infinite; border: 2px solid #D4AF37 !important; border-radius: 10px; padding: 12px; background: rgba(0,30,60,0.95) !important; color: #e8eef4; }
.gcslc-watermark { position: fixed; bottom: 8px; right: 12px; font-size: 0.7rem; color: rgba(212,175,55,0.4); letter-spacing: 0.15em; z-index: 9999; pointer-events: none; }
.shield-overlay { position: fixed; inset: 0; background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60'%3E%3Cpath fill='%23D4AF37' fill-opacity='0.03' d='M30 2 L58 14 L58 30 L30 42 L2 30 L2 14 Z'/%3E%3C/svg%3E"); pointer-events: none; z-index: 9998; }
.signature-calligraphy { color: #D4AF37; font-size: 1.15rem; font-weight: 600; font-style: italic; text-shadow: 0 0 12px rgba(212,175,55,0.5); }
"""


def build_header_html():
    medallion_img = f'<img src="data:image/png;base64,{B64_MEDALLION}" alt="GCSLC Medallion" />' if B64_MEDALLION else '<div style="width:120px;height:120px;border:3px solid #D4AF37;border-radius:50%;margin:0 auto;"></div>'
    return f"""
    <div style="text-align: center; padding: 12px 0 8px 0;">
        <h1 class="sovereign-title" style="font-size: 1.35rem; line-height: 1.4;">GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION - GCSLC LTD/GTE</h1>
        <p style="color: #b8c4ce; font-size: 0.9rem; margin: 4px 0;">(Powered by 8R Stealth Paradigm Convergence and its Determinants)</p>
        <p style="color: #7eb8da; font-size: 0.95rem; margin: 8px 0;">Let's Converge for you to understand.</p>
        <div class="medallion-wrap">
            {medallion_img}
            <div class="gcslc-letters"><span>G</span><span>-</span><span>C</span><span>-</span><span>S</span><span>-</span><span>L</span><span>-</span><span>C</span></div>
        </div>
    </div>
    """


def build_guardian_html():
    if not B64_GUARDIAN:
        return """
        <div class="live-node" style="text-align: center; padding: 24px;">
            <div style="font-size: 48px;">🛡️</div>
            <h3 style="color:#D4AF37;">8R Humanoid Guardian</h3>
            <p class="prism-text">I need energy to thrive</p>
        </div>
        """
    return f"""
    <div class="live-node" style="text-align: center; padding: 12px;">
        <img src="data:image/png;base64,{B64_GUARDIAN}" alt="Guardian Humanoid" style="max-width: 100%; max-height: 200px; display: block; margin: 0 auto;" />
        <p class="prism-text" style="margin: 10px 0 0 0;">I need energy to thrive</p>
    </div>
    """


def build_falcon_html():
    if not B64_FALCON:
        return '<span style="font-size:48px;">🦅</span>'
    return f'<img src="data:image/png;base64,{B64_FALCON}" alt="NVFC Falcon" style="max-height: 100%;" />'


def build_fortress_html():
    if not B64_FORTRESS:
        return """
        <div class="fortress-prism" style="padding: 24px; background: rgba(0,40,80,0.9);">
            <h3 style="color:#7eb8da; text-align:center;">DUBAI PROTOTYPE: STRATEGIC DATA HUB</h3>
            <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 12px;">
                <div style="background: rgba(0,60,120,0.5); border: 1px solid #5c9ead; border-radius: 8px; padding: 12px; text-align: center; color: #b8d4e8;">Core-1</div>
                <div style="background: rgba(0,60,120,0.5); border: 1px solid #5c9ead; border-radius: 8px; padding: 12px; text-align: center; color: #b8d4e8;">Core-2</div>
                <div style="background: rgba(0,60,120,0.5); border: 1px solid #5c9ead; border-radius: 8px; padding: 12px; text-align: center; color: #b8d4e8;">AI-Cluster</div>
                <div style="background: rgba(0,60,120,0.5); border: 1px solid #5c9ead; border-radius: 8px; padding: 12px; text-align: center; color: #b8d4e8;">Secure-Vault</div>
            </div>
        </div>
        """
    return f"""
    <div class="fortress-prism" style="padding: 16px; background: rgba(0,31,63,0.95);">
        <h3 style="color: #7eb8da; text-align: center; letter-spacing: 0.12em; margin: 0 0 12px 0;">DUBAI PROTOTYPE: STRATEGIC DATA HUB</h3>
        <img src="data:image/png;base64,{B64_FORTRESS}" alt="Strategic Data Hub" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px;" />
    </div>
    """


def build_8r_nodes_html():
    parts = []
    for i, (label, sub, proj) in enumerate(DETERMINANTS_8R, 1):
        parts.append(f'<div class="live-node" style="text-align:center;"><div style="color:#D4AF37;font-weight:700;">R{i} {label}</div><div style="font-size:0.8rem;color:#7eb8da;">{sub}</div><div style="font-size:0.85rem;margin-top:4px;">{proj}</div></div>')
    return "<div style='display: grid; grid-template-columns: repeat(8, 1fr); gap: 10px;'>" + "".join(parts) + "</div>"


def build_market_intel_html():
    nodes = get_market_velocity_nodes()
    parts = []
    for n in nodes:
        vol = n["volume_kt"] if isinstance(n["volume_kt"], str) else f"{n['volume_kt']} {n['unit']}"
        parts.append(f"""
        <div class="live-node">
            <div style="color:#D4AF37; font-weight:700;">{n['commodity']}</div>
            <div style="font-size:0.8rem;">Unit: {n['unit_price']}</div>
            <div style="font-size:0.85rem;">Vol: {vol}</div>
            <div style="color:#7eb8da; font-weight:600;">${n['monthly_proj_usd_m']}M/mo</div>
        </div>
        """)
    return "<div style='display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px;'>" + "".join(parts) + "</div>"


def build_total_projections_html():
    nodes = get_market_velocity_nodes()
    total = sum(n["monthly_proj_usd_m"] for n in nodes)
    rows = "".join(f"<tr><td>{n['commodity']}</td><td style='color:#D4AF37;'>${n['monthly_proj_usd_m']}M</td></tr>" for n in nodes)
    falcon_img = f'<img src="data:image/png;base64,{B64_FALCON}" alt="NVFC" style="height: 64px; animation: falcon-shout 1.8s ease-in-out infinite;" />' if B64_FALCON else '<span style="font-size:48px;">🦅</span>'
    return f"""
    <div class="live-node" style="display: flex; align-items: center; justify-content: space-between; gap: 24px; padding: 20px;">
        <div style="flex: 1;">
            <div style="color: #D4AF37; font-weight: 700; margin-bottom: 10px;">Total Monthly Projections</div>
            <table style="width: 100%; color: #e8eef4; font-size: 0.9rem;">
                {rows}
                <tr><td><b>Total</b></td><td style="color: #D4AF37; font-weight: 700;">${total:.1f}M</td></tr>
            </table>
        </div>
        <div class="falcon-hover" style="position: relative; right: auto; top: auto;">{falcon_img}</div>
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
    gr.HTML('<div class="shield-overlay"></div><div class="gcslc-watermark">GCSLC SOVEREIGN COMMAND GATEWAY</div>')

    gr.HTML(build_header_html())

    gr.HTML("""
    <div style="text-align: center; padding: 10px 0; margin: 12px 0; border-top: 1px solid rgba(212,175,55,0.3); border-bottom: 1px solid rgba(212,175,55,0.3);">
        <p style="color: #7eb8da; font-size: 0.95rem; margin: 0;">NVIDIA &amp; Microsoft: The 8R Stealth Paradigm is the bridge between Nigerian Energy Sovereignty and Global AI Dominance.</p>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=3):
            gr.HTML("<p style='color:#D4AF37; margin:0 0 6px 0; font-weight:600;'>Interactive Map of Nigeria — 13 coal states: hover for reserves &amp; byproduct value</p>")
            gr.Plot(create_sovereign_map(), label="")
            gr.HTML("<p style='color:#b8c4ce; font-size:0.85rem; margin: 8px 0 0 0;'>Select a coal state for a gold-framed pop-up:</p>")
            state_dropdown = gr.Dropdown(choices=[""] + COAL_STATES, value="", label="State", elem_classes=[])
            state_popup = gr.HTML(state_popup_html(""))

        with gr.Column(scale=1):
            gr.HTML(build_guardian_html())
            gr.HTML(f"""
            <div style="margin-top: 12px;">
                <div style="color: #D4AF37; font-weight: 700; margin-bottom: 6px;">National Velocity Falcon (NVFC)</div>
                <div class="falcon-hover" style="position: relative; right: auto; top: auto; margin: 8px 0;">{build_falcon_html()}</div>
                <p style="color: #b8c4ce; font-size: 0.8rem;">Market urgency — 13 states</p>
                <div style="overflow: hidden; border: 1px solid rgba(212,175,55,0.4); border-radius: 8px; padding: 8px; margin-top: 8px; background: rgba(0,0,0,0.3);">
                    <div class="ticker" style="display: inline-block; padding-left: 100%; animation: ticker-scroll 25s linear infinite; color: #D4AF37; font-size: 0.85rem;">{FALCON_ALERTS}</div>
                </div>
            </div>
            """)

    state_dropdown.change(fn=state_popup_html, inputs=[state_dropdown], outputs=[state_popup])

    gr.HTML(build_fortress_html())

    gr.HTML("<p style='color:#D4AF37; margin: 14px 0 6px 0; font-weight: 600;'>8R Determinants — Live-nodal streams</p>")
    gr.HTML(build_8r_nodes_html())

    gr.HTML("<p style='color:#D4AF37; margin: 18px 0 6px 0; font-weight: 600;'>Market Intel — Unit prices &amp; monthly projections</p>")
    gr.HTML(build_market_intel_html())

    gr.HTML("""
    <div style="background: rgba(0,31,63,0.95); border: 4px solid #D4AF37; padding: 20px; border-radius: 12px; margin: 20px 0; text-align: center;">
        <h2 style="color: #D4AF37; margin: 0 0 10px 0; letter-spacing: 2px;">8R STEALTH PARADIGM CONVERGENCE</h2>
        <h1 style="color: #ff0000; font-size: 40px; animation: blink 1s infinite; margin: 10px 0;">$1.87 Billion/Year LOSS</h1>
        <p style="color: #e8eef4; font-size: 0.9rem; margin: 6px 0;">Cumulative national opportunity cost</p>
    </div>
    """)

    gr.HTML("<p style='color:#D4AF37; margin: 16px 0 6px 0; font-weight: 600;'>Total Monthly Projections</p>")
    gr.HTML(build_total_projections_html())

    gr.HTML("""
    <div style="text-align: center; padding: 14px; color: #D4AF37; font-size: 0.95rem; border-top: 1px solid rgba(212,175,55,0.4); margin-top: 20px;">
        For Strategic Inquiries: <a href="mailto:info@galadimanruwacenter.org" style="color: #D4AF37;">info@galadimanruwacenter.org</a>
    </div>
    <div style="text-align: center; padding: 12px 0 24px 0;">
        <p class="signature-calligraphy">Dr. Sa\u2019ad Jaafaru, Chairman &amp; Founder</p>
        <p style="color: #b8c4ce; font-size: 0.85rem; margin: 4px 0 0 0;">Authorized Signature · Galadiman Ruwa Center for Strategic Leadership and Communication - GCSLC LTD/GTE</p>
    </div>
    """)

if __name__ == "__main__":
    demo.launch()
