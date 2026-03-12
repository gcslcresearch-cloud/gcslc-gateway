import gradio as gr
import os

# Path to your high-fidelity asset
FILE_PATH = os.path.expanduser("~/Desktop/8RStealthBfiles/app.html")


def load_dashboard():
    if not os.path.exists(FILE_PATH):
        return f"CRITICAL ERROR: {FILE_PATH} not found."
    with open(FILE_PATH, "r") as f:
        return f.read()


# Gradio Wrapper with corrected Color Logic
# Using 'amber' as the shortcut for Gold to avoid the ValueError
with gr.Blocks(
    theme=gr.themes.Default(primary_hue="blue", secondary_hue="amber"),
    title="GCSLC NRRFC Fusion Center",
) as demo:
    gr.HTML(load_dashboard())

if __name__ == "__main__":
    # Launching on 8090 with verified color mapping
    demo.launch(server_port=8090, show_api=False)
