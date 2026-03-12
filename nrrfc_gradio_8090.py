"""Local launcher on 8090 — uses FINAL_UI from app.py."""
from app import FINAL_UI
import gradio as gr

with gr.Blocks(
    css=":root, body, .gradio-container { background: #050a15 !important; }",
    title="GCSLC NRRFC Fusion Center",
) as demo:
    gr.HTML(FINAL_UI)

if __name__ == "__main__":
    demo.launch(server_port=8090, server_name="0.0.0.0", show_api=False)
