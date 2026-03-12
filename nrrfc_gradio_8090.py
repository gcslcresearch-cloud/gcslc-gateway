"""Fusion Center launcher — Port 8091. Native Gradio only, no HTML dependency."""
from app import demo

if __name__ == "__main__":
    demo.launch(server_port=8091, server_name="0.0.0.0", show_api=False)
