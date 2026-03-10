import gradio as gr
import plotly.express as px
import pandas as pd
import json
import os
import plotly.graph_objects as go

# --- SOVEREIGN DATA CONFIGURATION ---
COAL_STATES = ['Kogi', 'Enugu', 'Benue', 'Gombe', 'Delta', 'Imo', 'Anambra', 'Abia', 'Edo', 'Nasarawa', 'Plateau', 'Cross River', 'Bauchi']
LOSS_VAL = "$1.87 Billion/Year"

# 36 states + FCT (Zamfara spelling corrected)
STATES_36_FCT = [
    "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno",
    "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "FCT", "Gombe", "Imo",
    "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos", "Nasarawa",
    "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers", "Sokoto", "Taraba",
    "Yobe", "Zamfara"
]


def _geojson_path():
    """Resolve ng_state.geojson: HF Spaces often have it in repo root; else data/ next to app."""
    root = os.path.dirname(os.path.abspath(__file__))
    for path in [
        os.path.join(root, "ng_state.geojson"),   # repo root (where HF uploads often go)
        os.path.join(root, "data", "ng_state.geojson"),
    ]:
        if os.path.isfile(path):
            return path
    return None


def create_sovereign_map():
    """True Map of Nigeria: Plotly choropleth. Coal-Rich = Burnished Gold, others = Sovereign Navy. Optimized for S24 Ultra."""
    path = _geojson_path()
    geojson_data = None
    if path:
        try:
            with open(path, encoding="utf-8") as f:
                geojson_data = json.load(f)
        except Exception:
            geojson_data = None

    df = pd.DataFrame({"State": STATES_36_FCT})
    df['Status'] = df['State'].apply(lambda x: 'Coal-Rich' if x in COAL_STATES else 'Sovereign Navy')

    if geojson_data is None:
        # Fallback: minimal figure so app does not crash (add ng_state.geojson to repo root or data/ for full map)
        fig = go.Figure()
        fig.update_layout(
            title="True Map of Nigeria — Add ng_state.geojson to this Space (root or data/)",
            paper_bgcolor='rgba(0,0,0,0)',
            margin={"r": 0, "t": 40, "l": 0, "b": 0},
            height=400,
            annotations=[dict(text="Upload ng_state.geojson to repo root or data/ folder", x=0.5, y=0.5, showarrow=False, font=dict(size=14))]
        )
        return fig

    # Detect property key used for state name in GeoJSON
    featureidkey = "properties.name"
    name_to_status = {}
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
        # Build locations from actual GeoJSON names so choropleth matches (avoids blank grid)
        for f in geojson_data["features"]:
            p = f.get("properties") or {}
            name = p.get("name") or p.get("adm1_name") or p.get("shapeName") or p.get("NAME_1") or p.get("name_1") or ""
            if isinstance(name, str):
                name = name.strip()
            if name:
                name_to_status[name] = "Coal-Rich" if name in COAL_STATES else "Sovereign Navy"
        # Normalize common variants for coal coloring
        _norm = {"Federal Capital Territory": "FCT", "Abuja": "FCT", "Nassarawa": "Nasarawa"}
        for geo_name, status in list(name_to_status.items()):
            canonical = _norm.get(geo_name, geo_name)
            if canonical in COAL_STATES:
                name_to_status[geo_name] = "Coal-Rich"
            else:
                name_to_status[geo_name] = "Sovereign Navy"
    if not name_to_status:
        name_to_status = {s: ("Coal-Rich" if s in COAL_STATES else "Sovereign Navy") for s in STATES_36_FCT}
    df = pd.DataFrame({"State": list(name_to_status.keys()), "Status": list(name_to_status.values())})

    fig = px.choropleth(
        df,
        geojson=geojson_data,
        locations='State',
        featureidkey=featureidkey,
        color='Status',
        color_discrete_map={'Coal-Rich': 'rgb(184, 134, 11)', 'Sovereign Navy': 'rgb(0, 32, 96)'},
        scope="africa",
        center={"lat": 9.08, "lon": 7.53}
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor='rgba(0,0,0,0)',
        dragmode=False,
        height=400,
    )
    return fig


# --- UI ARCHITECTURE ---
with gr.Blocks(theme=gr.themes.Default(primary_hue="yellow", secondary_hue="blue")) as demo:
    gr.HTML("<h1 style='text-align:center; color:#b8860b;'>AFRICAN WEALTH CLOUD: SOVEREIGN COMMAND</h1>")

    with gr.Row():
        # THE MAP OF AUTHORITY
        with gr.Column(scale=3):
            gr.Plot(create_sovereign_map(), label="True Map of Nigeria")

        # THE 8R HUMANOID GUARDIAN
        with gr.Column(scale=1):
            gr.HTML("""
            <div style='border: 2px solid #b8860b; border-radius: 20px; padding: 15px; background: #002060; text-align: center;'>
                <div style='font-size: 60px; animation: pulse 1.5s infinite;'>🛡️</div>
                <h3 style='color: #b8860b;'>8R Humanoid Guardian</h3>
                <p style='color: white; font-size: 12px;'>Navy & Gold Protocol Active</p>
            </div>
            <style>
                @keyframes pulse { 0% { transform: scale(1); opacity: 0.8; } 50% { transform: scale(1.1); opacity: 1; } 100% { transform: scale(1); opacity: 0.8; } }
            </style>
            """)
            with gr.Accordion("Manifest Determinants", open=False):
                gr.Markdown("1. Resource Sovereignty\n2. Regulatory Realignment\n3. Revenue Revitalization...")

    # THE 5TH BOX: FINANCIAL KILL-SHOT
    gr.HTML("""
    <div style="background-color: #001f3f; border: 6px solid #D4AF37; padding: 25px; border-radius: 15px; color: white; font-family: sans-serif; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
        <h2 style="color: #D4AF37; margin-top: 0; letter-spacing: 2px;">COMMAND PROTOCOL: 8R STEALTH PARADIGM CONVERGENCE</h2>
        <div style="display: grid; grid-template-columns: 1fr 1fr; text-align: left; gap: 10px; margin: 15px 0; font-size: 14px;">
            <div>1. REFINE | 2. RESET | 3. RESEARCH | 4. RESTRUCTURE</div>
            <div>5. RESUSCITATE | 6. REVITALIZE | 7. RE-ENGINEER | 8. RETAIN</div>
        </div>
        <h1 style="color: #ff0000; font-size: 40px; animation: blink 1s infinite; margin: 10px 0;">$1.87 Billion/Year LOSS</h1>
        <p style="font-weight: bold; font-size: 1.1em; margin-bottom: 5px;">Galadiman Ruwa Center for Strategic Leadership and Communication - GCSLC LTD/GTE</p>
        <div style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #D4AF37;">
            <p style="color: #D4AF37; font-size: 1.2em; font-weight: 600; margin: 0;">Dr. Sa’ad Jaafaru, Chairman &amp; Founder</p>
        </div>
    </div>
    <style>
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    </style>
    """)

if __name__ == "__main__":
    demo.launch()
