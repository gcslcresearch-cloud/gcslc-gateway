import gradio as gr
import os

# Path to your high-fidelity asset
FILE_PATH = os.path.expanduser("~/Desktop/8RStealthBfiles/app.html")


def load_dashboard():
    with open(FILE_PATH, "r") as f:
        html_content = f.read()
    return html_content


# The Gradio Wrapper for NRRFC
with gr.Blocks(
    theme=gr.themes.Default(primary_hue="blue", secondary_hue="gold"),
    title="GCSLC NRRFC Fusion Center",
) as demo:
    gr.HTML(load_dashboard())

if __name__ == "__main__":
    # Launching for local verification before Hugging Face Push
    demo.launch(server_port=8090, show_api=False)
