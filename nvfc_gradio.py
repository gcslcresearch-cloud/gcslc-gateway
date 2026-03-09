"""
NVFC Dashboard — High-Velocity state. Navy & Gold theme, 13 coal states + Falcon.
S24 access: server_name="0.0.0.0", share=True. PM2 app name: NVFC-COMMAND.
"""
import gradio as gr
import os
import subprocess
import sys

SERVER_PORT = 7860
COAL_STATES = (
    "Enugu", "Kogi", "Benue", "Nasarawa", "Gombe", "Adamawa", "Delta",
    "Edo", "Ondo", "Bauchi", "Anambra", "Ebonyi", "Abia",
)

# Navy & Gold theme with shimmer
css = """
.gradio-container, .main, .container { background: #000B1E !important; }
.shimmer { color: #D4AF37; text-shadow: 0 0 15px #D4AF37; animation: pulse 2s infinite; }
.shimmer-sub { color: #B8860B; animation: pulse 2.5s infinite; }
@keyframes pulse { 0% { opacity: 0.75; } 50% { opacity: 1; } 100% { opacity: 0.75; } }
h1, h2, h3 { color: #D4AF37 !important; text-align: center; }
p, span, label { color: #e8eef4 !important; }
.gold-border { border: 2px solid #D4AF37; border-radius: 12px; background: linear-gradient(135deg, #001A35 0%, #000B1E 100%); }
"""


def _clear_gradio_cache():
    """Bypass system blocks: clear old Gradio cache."""
    for d in [os.path.expanduser("~/.cache/gradio"), os.path.expanduser("~/.gradio")]:
        if os.path.isdir(d):
            try:
                import shutil
                shutil.rmtree(d, ignore_errors=True)
            except Exception:
                pass


def _kill_port():
    try:
        subprocess.run("lsof -ti:7860 | xargs kill -9", shell=True, capture_output=True, timeout=5)
    except Exception:
        pass


# Shimmering Nigerian map: 13 coal-rich states + Falcon as strategic icon
def _map_html():
    states_list = "".join(f"<span class='shimmer-sub'>📍 {s}</span>" for s in COAL_STATES)
    return f"""
    <div class='gold-border' style='padding: 24px; text-align: center;'>
        <h3 class='shimmer'>🇳🇬 Sovereign Resource Map — 13 Coal-Rich States</h3>
        <p style='color: #b8c4ce; margin: 12px 0;'>National Velocity Falcon Cloud (NVFC) Ground-Base</p>
        <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; text-align: left; max-width: 400px; margin: 16px auto; font-size: 0.95rem;'>
            {states_list}
        </div>
        <div style='font-size: 72px; margin-top: 16px;' title='Strategic Falcon'>🦅</div>
        <p class='shimmer-sub' style='font-size: 0.9rem;'>Falcon — High-Velocity Sovereign Icon</p>
    </div>
    """


with gr.Blocks(css=css, title="GCSLC - NVFC High-Velocity") as demo:
    gr.HTML("<h1 class='shimmer' style='text-align:center;'>🦅 National Velocity Falcon Cloud</h1>")
    gr.Markdown("### *8R Paradigm — High-Velocity State*")

    with gr.Row():
        with gr.Column(scale=2):
            gr.HTML(_map_html())
        with gr.Column(scale=1):
            gr.Markdown("**Strategic Benchmark**")
            gr.Label(value="UAE ($15.2B AI Cloud) vs. Nigeria (2B MT Coal)")
            gr.Button("Ignite Determinant 5: Resuscitate", variant="primary")
            gr.Markdown("---")
            gr.Markdown("**8R:** Refine · Reset · Research · Restructure · Resuscitate · Revitalize · Re-engineer · Retain")

    gr.Markdown("---")
    gr.Markdown("*Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau) — GCSLC Strategic Command*")


if __name__ == "__main__":
    _clear_gradio_cache()
    _kill_port()
    print("\n" + "=" * 60)
    print("  NVFC High-Velocity — Local: http://127.0.0.1:7860")
    print("  Public URL appears below (share=True). Save it on your S24.")
    print("=" * 60 + "\n")
    sys.stdout.flush()
    demo.launch(share=True, server_name="0.0.0.0", server_port=SERVER_PORT, show_error=True)
