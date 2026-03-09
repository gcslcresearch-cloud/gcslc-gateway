import gradio as gr
import pandas as pd
import subprocess
import sys

SERVER_PORT = 7860

# GCSLC Sovereign Prestige CSS
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


with gr.Blocks(css=css, title="GCSLC - National Velocity Falcon Cloud") as demo:
    gr.HTML("<h1 class='shimmer' style='text-align:center;'>🦅 National Velocity Falcon Cloud</h1>")

    with gr.Row():
        with gr.Column(scale=2):
            # THE SHIMMERING MAP OF NIGERIA
            gr.HTML("""
                <div style='border: 2px solid #D4AF37; padding: 20px; border-radius: 15px; background: #001A35; text-align: center;'>
                    <h3 style='color: #D4AF37;'>🇳🇬 Sovereign Resource Map</h3>
                    <p style='color: white;'>Visualizing the 13 Coal-Rich Sovereign States...</p>
                    <img src='https://upload.wikimedia.org/wikipedia/commons/7/79/Flag_of_Nigeria.svg' style='width: 50px; opacity: 0.8;'>
                    <div style='font-size: 80px;'>🦅</div>
                </div>
            """)
        with gr.Column(scale=1):
            gr.Label("Strategic Benchmark", value="UAE ($15.2B) vs. Nigeria (2B Tonnes Coal)")
            gr.Button("Ignite Determinant 5: Resuscitate", variant="primary")


# FIX: server_name="0.0.0.0" allows your S24 to connect via the local network immediately.
if __name__ == "__main__":
    _kill_port()
    demo.launch(share=True, server_name="0.0.0.0", server_port=SERVER_PORT, show_error=True)
