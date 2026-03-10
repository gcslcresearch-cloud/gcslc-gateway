"""
Sovereign Command Center — Goldman-style high-finance aesthetic.
Deep Navy (#001f3f), Blue-Ray prism frame, Dubai Data Hub, Velocity Falcon, Market Velocity nodes.
Interactive map: 13 coal states show proven reserves + byproduct market value on hover.
"""
import gradio as gr
import plotly.express as px
import pandas as pd
import json
import os
import time
import plotly.graph_objects as go

# --- SOVEREIGN DATA CONFIGURATION ---
COAL_STATES = [
    "Kogi", "Enugu", "Benue", "Gombe", "Delta", "Imo", "Anambra", "Abia",
    "Edo", "Nasarawa", "Plateau", "Cross River", "Bauchi"
]
LOSS_VAL = "$1.87 Billion/Year"

# Proven reserves (million tonnes) and byproduct market value placeholder per state
STATE_RESERVES_MT = {
    "Kogi": 142.0, "Enugu": 168.0, "Benue": 85.0, "Gombe": 62.0, "Delta": 45.0,
    "Imo": 20.0, "Anambra": 27.3, "Abia": 18.0, "Edo": 38.0, "Nasarawa": 22.0,
    "Plateau": 28.0, "Cross River": 13.0, "Bauchi": 25.0,
}
# Byproduct market value (USD) — used in map hover and velocity nodes
BYPRODUCT_GERMANIUM_USD_KG = 8597
BYPRODUCT_AMMONIA_USD_MT = 430
BYPRODUCT_SILICON_USD_MT = 6500
BYPRODUCT_SEMICONDUCTOR_INDEX = 1.24  # notional

STATES_36_FCT = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno",
    "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "FCT", "Gombe", "Imo",
    "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos", "Nasarawa",
    "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers", "Sokoto", "Taraba",
    "Yobe", "Zamfara"
]


def _geojson_path():
    root = os.path.dirname(os.path.abspath(__file__))
    for path in [
        os.path.join(root, "ng_state.geojson"),
        os.path.join(root, "data", "ng_state.geojson"),
    ]:
        if os.path.isfile(path):
            return path
    return None


def _hover_text(state: str) -> str:
    if state in COAL_STATES:
        reserves = STATE_RESERVES_MT.get(state, 0)
        byproduct_val = (
            f"Germanium ${BYPRODUCT_GERMANIUM_USD_KG:,.0f}/kg | "
            f"Ammonia ${BYPRODUCT_AMMONIA_USD_MT:,.0f}/MT | "
            f"Silicon ${BYPRODUCT_SILICON_USD_MT:,.0f}/MT"
        )
        return f"<b>{state}</b><br>Proven reserves: <b>{reserves:.1f} M tonnes</b><br>Byproduct market: {byproduct_val}"
    return f"<b>{state}</b><br>Sovereign Navy"


def create_sovereign_map():
    """Interactive choropleth: hover over 13 coal states shows proven reserves and byproduct market value."""
    path = _geojson_path()
    geojson_data = None
    if path:
        try:
            with open(path, encoding="utf-8") as f:
                geojson_data = json.load(f)
        except Exception:
            geojson_data = None

    if geojson_data is None:
        fig = go.Figure()
        fig.update_layout(
            title="True Map of Nigeria — Add ng_state.geojson (root or data/)",
            paper_bgcolor="rgba(0,31,63,0.3)",
            margin={"r": 0, "t": 40, "l": 0, "b": 0},
            height=420,
            font=dict(color="#e8eef4"),
            annotations=[
                dict(
                    text="Upload ng_state.geojson to repo root or data/ folder",
                    x=0.5, y=0.5, showarrow=False, font=dict(size=14), xref="paper", yref="paper"
                )
            ],
        )
        return fig

    featureidkey = "properties.name"
    name_to_status = {}
    name_to_hover = {}
    if geojson_data.get("features"):
        props = geojson_data["features"][0].get("properties") or {}
        if "name" in props:
            featureidkey = "properties.name"
        elif "adm1_name" in props:
            featureidkey = "properties.adm1_name"
        elif "shapeName" in props:
            featureidkey = "properties.shapeName"
        elif "NAME_1" in props:
            featureidkey = "properties.NAME_1"
        _norm = {"Federal Capital Territory": "FCT", "Abuja": "FCT", "Nassarawa": "Nasarawa"}
        for f in geojson_data["features"]:
            p = f.get("properties") or {}
            name = p.get("name") or p.get("adm1_name") or p.get("shapeName") or p.get("NAME_1") or p.get("name_1") or ""
            if isinstance(name, str):
                name = name.strip()
            if name:
                canonical = _norm.get(name, name)
                is_coal = canonical in COAL_STATES
                name_to_status[name] = "Coal-Rich" if is_coal else "Sovereign Navy"
                name_to_hover[name] = _hover_text(canonical if canonical in COAL_STATES else name)

    if not name_to_status:
        name_to_status = {s: ("Coal-Rich" if s in COAL_STATES else "Sovereign Navy") for s in STATES_36_FCT}
        name_to_hover = {s: _hover_text(s) for s in STATES_36_FCT}

    df = pd.DataFrame({
        "State": list(name_to_status.keys()),
        "Status": list(name_to_status.values()),
        "Hover": [name_to_hover.get(s, _hover_text(s)) for s in name_to_status.keys()],
    })

    fig = px.choropleth(
        df,
        geojson=geojson_data,
        locations="State",
        featureidkey=featureidkey,
        color="Status",
        color_discrete_map={"Coal-Rich": "rgb(212, 175, 55)", "Sovereign Navy": "rgb(0, 32, 96)"},
        scope="africa",
        center={"lat": 9.08, "lon": 7.53},
    )
    fig.update_traces(
        hovertemplate="%{customdata}<extra></extra>",
        customdata=df["Hover"].tolist(),
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,31,63,0.2)",
        dragmode=False,
        height=420,
        font=dict(color="#e8eef4", size=12),
        hoverlabel=dict(bgcolor="#001f3f", font_size=12, font_family="sans-serif"),
    )
    return fig


def get_market_velocity_nodes():
    """High-velocity nodes: real-time volume and monthly projections (Coal, Germanium, Silicon, Ammonia, Semiconductors)."""
    t = time.time()
    # Deterministic but time-varying for "live" feel
    seed = int(t) % 86400
    def _v(lo, hi, seed_off=0):
        x = abs(hash(str(seed + seed_off))) % 100
        return lo + (x / 100.0) * (hi - lo)

    return [
        {
            "commodity": "Coal",
            "volume_kt": round(1200 * _v(0.9, 1.1, 0)),
            "monthly_proj_usd_m": round(18.5 * _v(0.95, 1.05, 1), 1),
            "unit": "kt",
        },
        {
            "commodity": "Germanium",
            "volume_kt": round(2.4 * _v(0.9, 1.1, 2), 2),
            "monthly_proj_usd_m": round(22.0 * _v(0.95, 1.05, 3), 1),
            "unit": "t",
        },
        {
            "commodity": "Silicon",
            "volume_kt": round(85 * _v(0.9, 1.1, 4)),
            "monthly_proj_usd_m": round(6.5 * _v(0.95, 1.05, 5), 1),
            "unit": "kt",
        },
        {
            "commodity": "Ammonia",
            "volume_kt": round(45 * _v(0.9, 1.1, 6)),
            "monthly_proj_usd_m": round(19.4 * _v(0.95, 1.05, 7), 1),
            "unit": "kt",
        },
        {
            "commodity": "Semiconductors",
            "volume_kt": "—",
            "monthly_proj_usd_m": round(12.0 * _v(0.95, 1.05, 8), 1),
            "unit": "index",
        },
    ]


# --- UI: Sovereign Command Center ---
PRISM_CSS = """
@keyframes prism-shimmer {
  0%, 100% { border-color: #D4AF37; box-shadow: 0 0 20px rgba(212,175,55,0.3), inset 0 0 30px rgba(0,100,255,0.05); }
  25% { border-color: #5c9ead; box-shadow: 0 0 25px rgba(92,158,173,0.4), inset 0 0 35px rgba(0,100,255,0.08); }
  50% { border-color: #D4AF37; box-shadow: 0 0 30px rgba(212,175,55,0.5), inset 0 0 40px rgba(0,150,255,0.1); }
  75% { border-color: #7eb8da; box-shadow: 0 0 25px rgba(126,184,218,0.4), inset 0 0 35px rgba(0,100,255,0.08); }
}
@keyframes falcon-pulse {
  0%, 100% { transform: scale(1) rotate(-5deg); opacity: 1; }
  50% { transform: scale(1.08) rotate(2deg); opacity: 0.95; }
}
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.35; } }
@keyframes ticker-scroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
@keyframes gold-glow {
  0%, 100% { box-shadow: 0 0 12px rgba(212,175,55,0.4); }
  50% { box-shadow: 0 0 20px rgba(212,175,55,0.6); }
}
.sovereign-wrap { background: #001f3f; min-height: 100vh; padding: 20px; font-family: 'Segoe UI', system-ui, sans-serif; }
.prism-frame { border: 3px solid #D4AF37; border-radius: 12px; padding: 24px; animation: prism-shimmer 4s ease-in-out infinite; background: linear-gradient(145deg, #001f3f 0%, #002244 50%, #001a35 100%); }
.prism-frame .header { text-align: center; color: #D4AF37; font-size: 1.6rem; letter-spacing: 0.2em; margin-bottom: 20px; font-weight: 600; text-shadow: 0 0 20px rgba(212,175,55,0.4); }
.main-wrap { background: #001f3f; }
.gradio-container { background: #001f3f !important; border: 3px solid #D4AF37; border-radius: 12px; animation: prism-shimmer 4s ease-in-out infinite; padding: 16px !important; }
.velocity-falcon { display: flex; align-items: center; gap: 12px; padding: 12px; background: rgba(0,40,80,0.8); border: 2px solid #D4AF37; border-radius: 10px; margin-bottom: 12px; }
.velocity-falcon .falcon-icon { font-size: 48px; animation: falcon-pulse 2s ease-in-out infinite; }
.ticker-wrap { overflow: hidden; white-space: nowrap; width: 100%; border: 1px solid rgba(212,175,55,0.4); border-radius: 6px; padding: 8px; background: rgba(0,0,0,0.3); }
.ticker { display: inline-block; padding-left: 100%; animation: ticker-scroll 25s linear infinite; color: #D4AF37; font-size: 0.9rem; }
.dubai-hub { background: linear-gradient(180deg, rgba(0,40,80,0.9) 0%, rgba(0,20,50,0.95) 100%); border: 2px solid #5c9ead; border-radius: 12px; padding: 20px; margin: 16px 0; }
.dubai-hub h3 { color: #7eb8da; text-align: center; letter-spacing: 0.15em; margin-bottom: 16px; font-size: 1.1rem; }
.dubai-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
.dubai-node { background: rgba(0,60,120,0.5); border: 1px solid rgba(126,184,218,0.5); border-radius: 8px; padding: 12px; text-align: center; color: #b8d4e8; font-size: 0.8rem; }
.velocity-box { background: rgba(0,30,60,0.9); border: 2px solid #D4AF37; border-radius: 10px; padding: 14px; color: #e8eef4; animation: gold-glow 3s ease-in-out infinite; }
.velocity-box .commodity { color: #D4AF37; font-weight: 700; font-size: 1rem; margin-bottom: 6px; }
.velocity-box .volume { font-size: 0.85rem; color: #b8c4ce; }
.velocity-box .projection { font-size: 1rem; color: #7eb8da; font-weight: 600; }
.contact-footer { text-align: center; padding: 16px; color: #D4AF37; font-size: 0.95rem; letter-spacing: 0.1em; border-top: 1px solid rgba(212,175,55,0.3); margin-top: 20px; }
.signature-block { margin-top: 20px; padding-top: 16px; border-top: 2px solid #D4AF37; text-align: center; }
.signature-block .entity { color: #e8eef4; font-weight: 600; font-size: 1rem; margin-bottom: 6px; }
.signature-block .officer { color: #D4AF37; font-size: 1.1rem; font-weight: 600; }
"""

# Scrolling alerts: market opportunities in 13 coal states
FALCON_ALERTS = "  ★  ".join([
    "Kogi: 142 Mt reserves — Germanium arbitrage open",
    "Enugu: 168 Mt — High-grade feedstock ready",
    "Benue: 85 Mt — Ammonia & Silicon pipeline",
    "Gombe: 62 Mt — Strategic data hub link",
    "Delta: 45 Mt — Port logistics corridor",
    "Imo: 20 Mt — Byproduct recovery opportunity",
    "Anambra: 27.3 Mt — Coal-to-compute node",
    "Abia: 18 Mt — Semiconductor feedstock",
    "Edo: 38 Mt — Regional integration",
    "Nasarawa: 22 Mt — Abuja nexus",
    "Plateau: 28 Mt — Germanium yield",
    "Cross River: 13 Mt — Export corridor",
    "Bauchi: 25 Mt — North-East hub",
]) * 2


def build_dubai_html():
    nodes = ["Core-1", "Core-2", "Storage-A", "Storage-B", "AI-Cluster", "Analytics", "Secure-Vault", "API-Gateway"]
    cells = "".join(f'<div class="dubai-node">{n}</div>' for n in nodes)
    return f"""
    <div class="dubai-hub">
        <h3>DUBAI PROTOTYPE: STRATEGIC DATA HUB</h3>
        <div class="dubai-grid">{cells}</div>
    </div>
    """


def build_velocity_html():
    nodes = get_market_velocity_nodes()
    boxes = []
    for n in nodes:
        vol = n["volume_kt"] if isinstance(n["volume_kt"], str) else f"{n['volume_kt']} {n['unit']}"
        boxes.append(f"""
        <div class="velocity-box">
            <div class="commodity">{n['commodity']}</div>
            <div class="volume">Volume: {vol}</div>
            <div class="projection">Monthly proj: ${n['monthly_proj_usd_m']}M</div>
        </div>
        """)
    return "<div style='display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px;'>" + "".join(boxes) + "</div>"


with gr.Blocks(
    theme=gr.themes.Base(
        primary_hue="amber",
        secondary_hue="blue",
    ).set(
        body_background_fill="#001f3f",
        block_background_fill="#001f3f",
        block_border_color="#D4AF37",
        block_label_text_color="#D4AF37",
        block_title_text_color="#D4AF37",
        button_primary_text_color="#001f3f",
        button_primary_background_fill="#D4AF37",
    ),
    css=PRISM_CSS,
) as demo:
    gr.HTML("""
    <div class="prism-frame main-wrap">
        <div class="header">SOVEREIGN COMMAND CENTER</div>
    """)

    with gr.Row():
        with gr.Column(scale=3):
            gr.HTML("<p style='color:#D4AF37; margin:0 0 8px 0; font-weight:600;'>Map of Authority — Hover 13 coal states for reserves & byproduct value</p>")
            gr.Plot(create_sovereign_map(), label="")

        with gr.Column(scale=1):
            gr.HTML(f"""
            <div class="velocity-falcon">
                <span class="falcon-icon">🦅</span>
                <div>
                    <strong style="color:#D4AF37;">Velocity Falcon (NVFC)</strong>
                    <p style="color:#b8c4ce; font-size:0.8rem; margin:4px 0 0 0;">Market signals: 13 coal-bearing states</p>
                </div>
            </div>
            <div class="ticker-wrap">
                <div class="ticker">{FALCON_ALERTS}</div>
            </div>
            """)

    gr.HTML(build_dubai_html())

    gr.HTML("<p style='color:#D4AF37; margin:16px 0 8px 0; font-weight:600;'>Market Velocity Logic — Real-time volume & monthly projections</p>")
    gr.HTML(build_velocity_html())

    gr.HTML("""
        <div style="background: rgba(0,31,63,0.95); border: 4px solid #D4AF37; padding: 24px; border-radius: 12px; margin: 20px 0; text-align: center;">
            <h2 style="color: #D4AF37; margin-top: 0; letter-spacing: 2px;">COMMAND PROTOCOL: 8R STEALTH PARADIGM CONVERGENCE</h2>
            <div style="display: grid; grid-template-columns: 1fr 1fr; text-align: center; gap: 10px; margin: 15px 0; font-size: 14px; color: #b8c4ce;">
                <div>1. REFINE | 2. RESET | 3. RESEARCH | 4. RESTRUCTURE</div>
                <div>5. RESUSCITATE | 6. REVITALIZE | 7. RE-ENGINEER | 8. RETAIN</div>
            </div>
            <h1 style="color: #ff0000; font-size: 42px; animation: blink 1s infinite; margin: 14px 0;">$1.87 Billion/Year LOSS</h1>
            <p style="color: #e8eef4; font-size: 0.95rem; margin: 8px 0;">Cumulative national opportunity cost — institutional urgency</p>
        </div>
    """)

    gr.HTML("""
        <div class="contact-footer">
            For Strategic Inquiries: <a href="mailto:info@galadimanruwacenter.org" style="color:#D4AF37;">info@galadimanruwacenter.org</a>
        </div>
        <div class="signature-block">
            <p class="entity">Galadiman Ruwa Center for Strategic Leadership and Communication - GCSLC LTD/GTE</p>
            <p class="officer">AUTHORIZING OFFICER: Dr. Sa\u2019ad Jaafaru, Chairman &amp; Founder</p>
        </div>
    """)

if __name__ == "__main__":
    demo.launch()
