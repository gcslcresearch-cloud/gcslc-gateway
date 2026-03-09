import gradio as gr
import pandas as pd
import subprocess
import sys

SERVER_PORT = 7860

# GCSLC Sovereign CSS - Shimmering Gold & Navy
css = """
.shimmer { color: #D4AF37; text-shadow: 0 0 15px #D4AF37; animation: pulse 2s infinite; }
@keyframes pulse { 0% { opacity: 0.7; } 50% { opacity: 1; } 100% { opacity: 0.7; } }
.gradio-container { background: #000B1E !important; }
"""


def _kill_port():
    try:
        subprocess.run("lsof -ti:7860 | xargs kill -9", shell=True, capture_output=True, timeout=5)
    except Exception:
        pass


with gr.Blocks(css=css, title="NVFC Sovereign Gateway") as demo:
    gr.HTML("<h1 class='shimmer' style='text-align:center;'>🦅 National Velocity Falcon Cloud</h1>")

    with gr.Row():
        with gr.Column(scale=2):
            gr.HTML("""
                <div style='border: 2px solid #D4AF37; padding: 20px; border-radius: 15px; background: #001A35;'>
                    <h3 style='color: #D4AF37;'>🇳🇬 Sovereign Resource Map</h3>
                    <p style='color: white;'>Visualizing the 13 Coal-Rich Sovereign States...</p>
                    <div style='font-size: 60px; text-align:center;'>🦅</div>
                </div>
            """)
        with gr.Column(scale=1):
            gr.Label("Strategic Benchmark", value="UAE ($15.2B) vs. Nigeria (2B Tonnes Coal)")
            gr.Button("Ignite Determinant 5: Resuscitate", variant="primary")


# S24 24/7/365 fix: server_name="0.0.0.0" allows phone access on same Wi-Fi
if __name__ == "__main__":
    _kill_port()
    demo.launch(share=True, server_name="0.0.0.0", server_port=SERVER_PORT, show_error=True)
