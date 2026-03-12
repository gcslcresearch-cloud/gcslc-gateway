"""
GCSLC Sovereign Gateway — Hugging Face / GitHub entry point.
Serves the Navy NRRFC dashboard (app.html): Deep Navy #050a15, Gold #D4AF37,
live UTC clock, 640.04 Mt reserves, $2.0B Sovereign Wealth Leakage.
"""
import os
import gradio as gr

ROOT = os.path.dirname(os.path.abspath(__file__))
DASHBOARD_HTML = os.path.join(ROOT, "app.html")


def load_dashboard():
    if not os.path.exists(DASHBOARD_HTML):
        return f"<p style='color:#D4AF37;'>Dashboard not found: {DASHBOARD_HTML}</p>"
    with open(DASHBOARD_HTML, "r", encoding="utf-8") as f:
        return f.read()


with gr.Blocks(
    css="body, .gradio-container { background: #050a15 !important; }",
    title="GCSLC NRRFC Fusion Center",
) as demo:
    gr.HTML(load_dashboard())

if __name__ == "__main__":
    try:
        demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
    except OSError:
        demo.launch(server_name="0.0.0.0", server_port=0, share=False)
