"""
NVFC Dashboard (Gradio) — GCSLC Shimmering Gold UI. S24 access: server_name="0.0.0.0".
Run: python nvfc_gradio.py  OR  ./deploy/run_nvfc_clean_restart.sh
"""
import gradio as gr
import pandas as pd
import subprocess
import sys

SERVER_PORT = 7860

# Custom CSS for the "GCSLC Shimmering Gold" effect
css = """
.shimmer-text {
    color: #D4AF37;
    font-weight: bold;
    text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
    animation: shimmer 2s infinite linear;
}
@keyframes shimmer { 0% { opacity: 0.8; } 50% { opacity: 1; } 100% { opacity: 0.8; } }
.gradio-container { background-color: #000B1E !important; color: white !important; }
"""


def _kill_port_7860():
    """Free port 7860 to avoid OSError 48 (Address already in use)."""
    try:
        if sys.platform == "darwin":
            subprocess.run("lsof -ti:7860 | xargs kill -9", shell=True, capture_output=True, timeout=5)
        else:
            subprocess.run("fuser -k 7860/tcp 2>/dev/null || true", shell=True, capture_output=True, timeout=5)
    except Exception:
        pass


with gr.Blocks(css=css, title="GCSLC - National Velocity Falcon Cloud") as demo:
    gr.Markdown("# 🦅 GCSLC: National Velocity Falcon Cloud (NVFC)")
    gr.Markdown("### *Strategizing 2 Billion Metric Tonnes of Coal into High-Velocity Digital Wealth*")

    with gr.Row():
        with gr.Column(scale=2):
            gr.HTML("""
                <div style='background: #001529; padding: 20px; border: 2px solid #D4AF37; border-radius: 15px; text-align: center;'>
                    <h2 class='shimmer-text'>🇳🇬 Sovereign Map of Nigeria</h2>
                    <p>Highlighting the 13 Coal-Rich Sovereign States</p>
                    <div style='font-size: 50px;'>🦅</div>
                </div>
            """)
        with gr.Column(scale=1):
            gr.Label(label="Sovereign Benchmark", value="UAE AI Cloud ($15.2B) vs. Nigeria Coal (2B Tonnes)")
            gr.Button("Execute 8R Paradigm", variant="primary")

    gr.Markdown("---")
    gr.Markdown("#### Status: Determinant 4 (Reset) Complete. Ready for D5 (Resuscitate).")


if __name__ == "__main__":
    _kill_port_7860()
    print("\n" + "=" * 60)
    print("  Local:  http://127.0.0.1:7860")
    print("  Public: (see below after Gradio starts)")
    print("=" * 60 + "\n")
    sys.stdout.flush()
    # CRITICAL: server_name="0.0.0.0" allows S24 / LAN devices to reach the app
    demo.launch(share=True, server_name="0.0.0.0", server_port=SERVER_PORT, show_error=True)
