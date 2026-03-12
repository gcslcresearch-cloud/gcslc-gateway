"""Local launcher on 8091 — uses app.demo (FINAL_UI + Gradio UTC pulse)."""
from app import demo

if __name__ == "__main__":
    demo.launch(server_port=8091, server_name="0.0.0.0", show_api=False)
