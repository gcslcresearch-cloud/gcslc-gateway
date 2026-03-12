"""Local launcher on 8090 — uses monolithic SOVEREIGN_UI from app.py (no file loading)."""
from app import SOVEREIGN_UI
import gradio as gr

with gr.Blocks(
    css="body, .gradio-container { background: #050a15 !important; }",
    title="GCSLC NRRFC Fusion Center",
) as demo:
    gr.HTML(SOVEREIGN_UI)

if __name__ == "__main__":
    demo.launch(server_port=8090, server_name="0.0.0.0", show_api=False)
