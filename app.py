"""
GCSLC SOVEREIGN COMMAND GATEWAY
Sovereign Systems Architecture — Goldman Sachs-tier institutional aesthetic.
Deep Navy (#001f3f), Shimmering Gold (#D4AF37). Medallion, Guardian, Falcon, Fortress.
Interactive Sovereign Map with Golden Arrow markers, Prism Hub, Shield overlay, authority banner.
"""
import base64
import json
import os
import time
from typing import Optional

# --- Compatibility shim for latest huggingface_hub + Gradio oauth ---
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
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PATHS & ASSETS (medallion.png, guardian.png, fortress.png, falcon.png) ---
ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, "assets")


def _load_b64(name: str) -> str:
    path = os.path.join(ASSETS, name)
    if os.path.isfile(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""


# Embed assets as data URLs for HTML — internal refs: medallion.png, guardian.png, fortress.png, falcon.png
B64_MEDALLION = _load_b64("medallion.png")
B64_GUARDIAN = _load_b64("guardian.png")
B64_FORTRESS = _load_b64("fortress.png")
B64_FALCON = _load_b64("falcon.png")

# --- SOVEREIGN DATA ---
COAL_STATES = [
    "Kogi", "Enugu", "Benue", "Gombe", "Delta", "Imo", "Anambra", "Abia",
    "Edo", "Nasarawa", "Plateau", "Cross River", "Bauchi"
]
# Golden Arrow marker positions (lon, lat) for Plotly — 13 coal states
STATE_CENTROIDS_LNGLAT = {
    "Kogi": (6.7, 7.8), "Enugu": (7.5, 6.4), "Benue": (8.2, 7.2), "Gombe": (11.2, 10.3),
    "Delta": (6.2, 5.9), "Imo": (7.0, 5.5), "Anambra": (7.0, 6.2), "Abia": (7.5, 5.5),
    "Edo": (6.3, 6.5), "Nasarawa": (8.5, 8.5), "Plateau": (8.9, 9.9), "Cross River": (8.3, 5.9), "Bauchi": (9.8, 10.3),
}
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
    # Golden Arrow markers (shimmering gold from falcon.png) for 13 coal states
    lons = [STATE_CENTROIDS_LNGLAT[s][0] for s in COAL_STATES if s in STATE_CENTROIDS_LNGLAT]
    lats = [STATE_CENTROIDS_LNGLAT[s][1] for s in COAL_STATES if s in STATE_CENTROIDS_LNGLAT]
    if lons and lats:
        fig.add_trace(
            go.Scattergeo(
                lon=lons,
                lat=lats,
                mode="markers",
                marker=dict(
                    size=14,
                    symbol="diamond",
                    color="#D4AF37",
                    line=dict(width=2, color="#FFD700"),
                ),
                name="Golden Arrow",
                hoverinfo="skip",
            )
        )
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


# --- GATEWAY CSS (Vision-Enhanced: medallion blue-ray, G-C-S-L-C sync, prism coal glow, fortress frame, falcon overlay) ---
# Coal glow from guardian.png (internal orange/yellow): #FFB200. Deep Navy: #001f3f. Shimmering Gold: #D4AF37.
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
/* Medallion: blue "ray" light — box-shadow mimics blue glow; sync G-C-S-L-C pulse to same 2.5s frequency */
@keyframes medallion-blue-ray {
  0%, 100% { box-shadow: 0 0 20px rgba(0,120,255,0.5), 0 0 40px rgba(0,150,255,0.25), 0 0 60px rgba(0,200,255,0.15); filter: drop-shadow(0 0 8px rgba(212,175,55,0.4)); }
  50% { box-shadow: 0 0 35px rgba(0,180,255,0.7), 0 0 55px rgba(0,200,255,0.4), 0 0 80px rgba(0,220,255,0.2); filter: drop-shadow(0 0 14px rgba(212,175,55,0.6)); }
}
@keyframes gcslc-letter-pulse {
  0%, 100% { transform: scale(1); opacity: 1; text-shadow: 0 0 12px rgba(0,180,255,0.4); }
  50% { transform: scale(1.12); opacity: 0.95; text-shadow: 0 0 20px rgba(0,200,255,0.7); }
}
.medallion-wrap { text-align: center; margin: 16px 0; }
.medallion-wrap img { max-height: 120px; border-radius: 50%; animation: medallion-blue-ray 2.5s ease-in-out infinite; }
.gcslc-letters { display: inline-flex; gap: 4px; margin-top: 8px; }
.gcslc-letters span { color: #D4AF37; font-weight: 800; font-size: 1.4rem; letter-spacing: 0.2em; animation: gcslc-letter-pulse 2.5s ease-in-out infinite; }
.gcslc-letters span:nth-child(1) { animation-delay: 0s; } .gcslc-letters span:nth-child(2) { animation-delay: 0.08s; }
.gcslc-letters span:nth-child(3) { animation-delay: 0.16s; } .gcslc-letters span:nth-child(4) { animation-delay: 0.24s; }
.gcslc-letters span:nth-child(5) { animation-delay: 0.32s; } .gcslc-letters span:nth-child(6) { animation-delay: 0.4s; }
.gcslc-letters span:nth-child(7) { animation-delay: 0.48s; } .gcslc-letters span:nth-child(8) { animation-delay: 0.56s; }
.gcslc-letters span:nth-child(9) { animation-delay: 0.64s; }
/* Guardian coal glow (#FFB200) for "I NEED ENERGY TO THRIVE" prism-text */
@keyframes prism-text-coal { 0% { background-position: 0% 50%; filter: drop-shadow(0 0 8px rgba(255,178,0,0.6)); } 100% { background-position: 200% 50%; filter: drop-shadow(0 0 14px rgba(255,178,0,0.9)); } }
.prism-text {
  background: linear-gradient(90deg, #FFB200, #FF9900, #FFB200, #FFD700, #FFB200);
  background-size: 200% auto; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; animation: prism-text-coal 3s linear infinite; font-weight: 700; font-size: 1.1rem; text-transform: uppercase;
}
/* Falcon overlay: position absolute, hover and pulse over map — market urgency */
@keyframes falcon-urgency { 0%, 100% { transform: translate(-50%,-50%) scale(1) rotate(-2deg); filter: drop-shadow(0 0 12px rgba(212,175,55,0.7)); } 50% { transform: translate(-50%,-50%) scale(1.08) rotate(2deg); filter: drop-shadow(0 0 22px rgba(212,175,55,0.95)); } }
.falcon-overlay-map { position: absolute; left: 82%; top: 50%; z-index: 10; pointer-events: none; }
.falcon-overlay-map img { height: 72px; animation: falcon-urgency 1.8s ease-in-out infinite; }
.map-wrap-sovereign { position: relative; min-height: 440px; }
/* Fortress frame: deep navy #001f3f from guardian.png background — houses Guardian */
.guardian-fortress-frame { background: #001f3f !important; border: 3px solid #D4AF37; border-radius: 12px; padding: 20px; box-shadow: 0 0 30px rgba(0,31,63,0.9), inset 0 0 40px rgba(0,20,50,0.5); }
/* Prism Hub: crystalline hexagonal structure (fortress.png inspiration) */
.prism-hub-hex { clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%); border: 2px solid rgba(212,175,55,0.8); background: rgba(0,31,63,0.95); padding: 14px; text-align: center; }
.prism-hub-widget { animation: live-node 2.5s ease-in-out infinite; border: 2px solid #D4AF37 !important; border-radius: 10px; padding: 12px; background: rgba(0,31,63,0.95) !important; color: #e8eef4; }
@keyframes live-node { 0%, 100% { box-shadow: 0 0 12px rgba(212,175,55,0.4); } 50% { box-shadow: 0 0 22px rgba(212,175,55,0.65); } }
@keyframes blue-ray { 0%, 100% { opacity: 0.6; box-shadow: 0 0 30px rgba(0,150,255,0.4); } 50% { opacity: 1; box-shadow: 0 0 50px rgba(0,200,255,0.6); } }
.fortress-prism { position: relative; border: 3px solid #D4AF37; border-radius: 12px; overflow: hidden; animation: prism-shimmer 4s ease-in-out infinite; background: #001f3f !important; }
.fortress-prism::after { content: ''; position: absolute; inset: 0; background: radial-gradient(ellipse at center, transparent 40%, rgba(0,150,255,0.12) 100%); pointer-events: none; animation: blue-ray 2.5s ease-in-out infinite; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.35; } }
@keyframes ticker-scroll { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }
.sovereign-title { color: #D4AF37; font-size: 1.1rem; letter-spacing: 0.12em; text-align: center; animation: title-glow 2.5s ease-in-out infinite; font-weight: 700; margin: 0 0 8px 0; }
.falcon-hover { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); z-index: 10; pointer-events: none; }
.falcon-hover img { height: 80px; animation: falcon-urgency 1.8s ease-in-out infinite; }
.gcslc-watermark { position: fixed; bottom: 8px; right: 12px; font-size: 0.7rem; color: rgba(212,175,55,0.4); letter-spacing: 0.15em; z-index: 9999; pointer-events: none; }
.shield-overlay { position: fixed; inset: 0; background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60'%3E%3Cpath fill='%23D4AF37' fill-opacity='0.03' d='M30 2 L58 14 L58 30 L30 42 L2 30 L2 14 Z'/%3E%3C/svg%3E"); pointer-events: none; z-index: 9998; }
.signature-calligraphy { color: #D4AF37; font-size: 1.15rem; font-weight: 600; font-style: italic; text-shadow: 0 0 12px rgba(212,175,55,0.5); position: absolute; bottom: 24px; right: 24px; }
"""


def build_header_html():
    medallion_img = f'<img src="data:image/png;base64,{B64_MEDALLION}" alt="GCSLC Medallion (medallion.png)" />' if B64_MEDALLION else '<div style="width:120px;height:120px;border:3px solid #D4AF37;border-radius:50%;margin:0 auto;"></div>'
    return f"""
    <div style="text-align: center; padding: 12px 0 8px 0;">
        <h1 class="sovereign-title" style="font-size: 1.35rem; line-height: 1.4;">GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION</h1>
        <p style="color: #D4AF37; font-size: 0.95rem; margin: 6px 0; letter-spacing: 0.08em;">8R Stealth Paradigm</p>
        <p style="color: #b8c4ce; font-size: 0.9rem; margin: 4px 0;">(Powered by 8R Stealth Paradigm Convergence and its Determinants)</p>
        <p style="color: #7eb8da; font-size: 0.95rem; margin: 8px 0;">Let's Converge for you to understand.</p>
        <div class="medallion-wrap">
            {medallion_img}
            <div class="gcslc-letters"><span>G</span><span>-</span><span>C</span><span>-</span><span>S</span><span>-</span><span>L</span><span>-</span><span>C</span></div>
        </div>
    </div>
    """


def build_guardian_html():
    """Guardian (guardian.png) in Fortress frame — deep navy #001f3f; prism-text uses coal glow #FFB200."""
    if not B64_GUARDIAN:
        return """
        <div class="guardian-fortress-frame" style="text-align: center; padding: 24px;">
            <div style="font-size: 48px;">🛡️</div>
            <h3 style="color:#D4AF37;">8R Humanoid Guardian</h3>
            <p class="prism-text">I NEED ENERGY TO THRIVE</p>
        </div>
        """
    return f"""
    <div class="guardian-fortress-frame" style="text-align: center; padding: 12px;">
        <img src="data:image/png;base64,{B64_GUARDIAN}" alt="Guardian (guardian.png)" style="max-width: 100%; max-height: 200px; display: block; margin: 0 auto;" />
        <p class="prism-text" style="margin: 10px 0 0 0;">I NEED ENERGY TO THRIVE</p>
    </div>
    """


def build_falcon_html():
    if not B64_FALCON:
        return '<span style="font-size:48px;">🦅</span>'
    return f'<img src="data:image/png;base64,{B64_FALCON}" alt="Falcon (falcon.png)" style="max-height: 100%;" />'


def build_fortress_html():
    """Fortress (fortress.png): crystalline hexagonal Prism Hub data widgets inspiration."""
    if not B64_FORTRESS:
        return """
        <div class="fortress-prism" style="padding: 24px;">
            <h3 style="color:#7eb8da; text-align:center; letter-spacing: 0.12em;">PRISM HUB — STRATEGIC DATA HUB</h3>
            <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 16px;">
                <div class="prism-hub-hex" style="color: #b8d4e8;"><div style="color:#D4AF37;font-weight:700;">Core-1</div><div style="font-size:0.8rem;">Tier-III</div></div>
                <div class="prism-hub-hex" style="color: #b8d4e8;"><div style="color:#D4AF37;font-weight:700;">Core-2</div><div style="font-size:0.8rem;">Tier-IV</div></div>
                <div class="prism-hub-hex" style="color: #b8d4e8;"><div style="color:#D4AF37;font-weight:700;">AI-Cluster</div><div style="font-size:0.8rem;">GEN-GEMINI</div></div>
                <div class="prism-hub-hex" style="color: #b8d4e8;"><div style="color:#D4AF37;font-weight:700;">Secure-Vault</div><div style="font-size:0.8rem;">Sovereign</div></div>
            </div>
        </div>
        """
    return f"""
    <div class="fortress-prism" style="padding: 16px;">
        <h3 style="color: #7eb8da; text-align: center; letter-spacing: 0.12em; margin: 0 0 12px 0;">PRISM HUB — STRATEGIC DATA HUB</h3>
        <img src="data:image/png;base64,{B64_FORTRESS}" alt="Fortress (fortress.png)" style="width: 100%; max-height: 280px; object-fit: contain; border-radius: 8px;" />
    </div>
    """


def build_8r_nodes_html():
    parts = []
    for i, (label, sub, proj) in enumerate(DETERMINANTS_8R, 1):
        parts.append(f'<div class="prism-hub-widget" style="text-align:center;"><div style="color:#D4AF37;font-weight:700;">R{i} {label}</div><div style="font-size:0.8rem;color:#7eb8da;">{sub}</div><div style="font-size:0.85rem;margin-top:4px;">{proj}</div></div>')
    return "<div style='display: grid; grid-template-columns: repeat(8, 1fr); gap: 10px;'>" + "".join(parts) + "</div>"


def build_market_intel_html():
    nodes = get_market_velocity_nodes()
    parts = []
    for n in nodes:
        vol = n["volume_kt"] if isinstance(n["volume_kt"], str) else f"{n['volume_kt']} {n['unit']}"
        parts.append(f"""
        <div class="prism-hub-widget">
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
    falcon_img = build_falcon_html()
    return f"""
    <div class="prism-hub-widget" style="display: flex; align-items: center; justify-content: space-between; gap: 24px; padding: 20px;">
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
    <div style="text-align: center; padding: 12px 16px; margin: 12px 0; border-top: 1px solid rgba(212,175,55,0.3); border-bottom: 1px solid rgba(212,175,55,0.3); background: rgba(0,31,63,0.6);">
        <p style="color: #D4AF37; font-size: 0.95rem; margin: 0; font-weight: 600;">NVIDIA · Microsoft · 8R Bridge — The 8R Stealth Paradigm is the bridge between Nigerian Energy Sovereignty and Global AI Dominance.</p>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=3):
            gr.HTML("<p style='color:#D4AF37; margin:0 0 6px 0; font-weight:600;'>Interactive Sovereign Map — 13 coal states (Golden Arrow markers): click state for reserves &amp; byproduct value</p>")
            gr.HTML('<div class="map-wrap-sovereign" style="position:relative;">')
            gr.Plot(create_sovereign_map(), label="")
            falcon_overlay = f'<div class="falcon-overlay-map" style="margin-top:-440px;height:0;overflow:visible;pointer-events:none;">{build_falcon_html()}</div></div>' if B64_FALCON else '<div class="falcon-overlay-map" style="margin-top:-440px;height:0;overflow:visible;"><span style="font-size:48px;">🦅</span></div></div>'
            gr.HTML(falcon_overlay)
            gr.HTML("<p style='color:#b8c4ce; font-size:0.85rem; margin: 8px 0 0 0;'>Select a coal state for gold-bordered pop-up:</p>")
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

    _footer = (
        '<div style="position: relative; min-height: 80px; padding: 14px 0 60px 0; border-top: 1px solid rgba(212,175,55,0.4); margin-top: 20px;">'
        '<p style="text-align: center; color: #D4AF37; font-size: 0.95rem;">For Strategic Inquiries: <a href="mailto:info@galadimanruwacenter.org" style="color: #D4AF37;">info@galadimanruwacenter.org</a></p>'
        '<p class="signature-calligraphy">Dr. Sa\u2019ad Jaafaru, Chairman &amp; Founder</p>'
        '<p style="color: #b8c4ce; font-size: 0.85rem; margin: 4px 0 0 0; position: absolute; bottom: 8px; right: 24px;">Galadiman Ruwa Center for Strategic Leadership and Communication — GCSLC LTD/GTE</p>'
        '</div>'
    )
    gr.HTML(_footer)

if __name__ == "__main__":
    demo.launch()
