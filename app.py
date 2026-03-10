import gradio as gr
import plotly.express as px
import pandas as pd
import json
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


def create_sovereign_map():
    """True Map of Nigeria: Plotly choropleth. Coal-Rich = Burnished Gold, others = Sovereign Navy. Optimized for S24 Ultra."""
    try:
        with open('data/ng_state.geojson') as f:
            geojson_data = json.load(f)
    except Exception:
        geojson_data = None

    df = pd.DataFrame({"State": STATES_36_FCT})
    df['Status'] = df['State'].apply(lambda x: 'Coal-Rich' if x in COAL_STATES else 'Sovereign Navy')

    if geojson_data is None:
        # Fallback: minimal figure so app does not crash (add data/ng_state.geojson for full map)
        fig = go.Figure()
        fig.update_layout(
            title="True Map of Nigeria — Add data/ng_state.geojson for 36 state borders",
            paper_bgcolor='rgba(0,0,0,0)',
            margin={"r": 0, "t": 40, "l": 0, "b": 0},
            height=400,
            annotations=[dict(text="Upload data/ng_state.geojson to this Space", x=0.5, y=0.5, showarrow=False, font=dict(size=14))]
        )
        return fig

    # Try common GeoJSON property keys for state name
    featureidkey = "properties.name"
    if geojson_data.get("features") and geojson_data["features"][0].get("properties"):
        props = geojson_data["features"][0]["properties"]
        if "name" in props:
            featureidkey = "properties.name"
        elif "adm1_name" in props:
            featureidkey = "properties.adm1_name"
        elif "shapeName" in props:
            featureidkey = "properties.shapeName"
        elif "NAME_1" in props:
            featureidkey = "properties.NAME_1"

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
    gr.HTML(f"""
    <div style='background: #721c24; border: 4px solid #b8860b; padding: 20px; border-radius: 15px; text-align: center;'>
        <h2 style='color: white; margin: 0;'>CUMULATIVE NATIONAL OPPORTUNITY COST</h2>
        <h1 style='color: #ff0000; font-size: 45px; animation: blink 1s infinite;'>{LOSS_VAL} LOSS</h1>
        <p style='color: white; font-size: 18px;'>Sovereign Warning: Nigeria is losing $1.9 Billion annually in unrealized wealth.</p>
    </div>
    <style>
        @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} 100% {{ opacity: 1; }} }}
    </style>
    """)

if __name__ == "__main__":
    demo.launch()
