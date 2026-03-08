"""
NVFC Dashboard (Gradio) — Deploy-ready with 8R Engine, Sovereign Widget, Prestige UI.
Run: python nvfc_gradio.py  OR  ./deploy/run_nvfc_clean_restart.sh
"""
import gradio as gr
import subprocess
import sys

SERVER_PORT = 7860
LOCAL_URL = f"http://127.0.0.1:{SERVER_PORT}"
PUBLIC_URL_MSG = "Public URL will appear in the lines below (Gradio prints it when share=True)."


def _kill_port_7860():
    """Free port 7860 so launch does not get OSError 48 (Address already in use)."""
    try:
        if sys.platform == "darwin":
            subprocess.run(
                "lsof -ti:7860 | xargs kill -9",
                shell=True,
                capture_output=True,
                timeout=5,
            )
        else:
            subprocess.run(
                "fuser -k 7860/tcp 2>/dev/null || true",
                shell=True,
                capture_output=True,
                timeout=5,
            )
    except Exception:
        pass

# GCSLC Sovereign Branding
NAVY_BG = "#000B1E"
GOLD_SHIMMER = "#D4AF37"
SIGNATURE_ANCHOR = "Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau), Chairman, GCSLC Strategic Command"

# 8R Stealth Paradigm Convergence
EIGHT_R = ("Refine", "Reset", "Research", "Restructure", "Resuscitate", "Revitalize", "Re-engineer", "Retain")

# Prestige UI: Navy Blue + Shimmering Gold
custom_css = f"""
.gradio-container, .main, .container {{
    background-color: {NAVY_BG} !important;
    border: 2px solid {GOLD_SHIMMER};
}}
@keyframes shimmer {{
    0% {{ color: {GOLD_SHIMMER}; text-shadow: 0 0 5px {GOLD_SHIMMER}; }}
    50% {{ color: #FFDF00; text-shadow: 0 0 20px #FFD700; }}
    100% {{ color: {GOLD_SHIMMER}; text-shadow: 0 0 5px {GOLD_SHIMMER}; }}
}}
h1, h2, h3 {{ animation: shimmer 3s infinite; text-align: center; font-family: serif; }}
p, span, label {{ color: {GOLD_SHIMMER} !important; font-weight: bold; }}
input, textarea, select {{
    background-color: #001B3A !important;
    color: white !important;
    border: 1px solid {GOLD_SHIMMER} !important;
}}
.stat-box {{ border: 1px solid {GOLD_SHIMMER}; padding: 12px; border-radius: 8px; background: rgba(212, 175, 55, 0.08); }}
footer {{ visibility: hidden; }}
"""

# Sovereign Widget: UAE vs Nigeria comparison (markdown table)
SOVEREIGN_COMPARISON = """
| | **UAE** | **Nigeria** |
|---|---|---|
| **Asset / Investment** | $15.2B AI Cloud (G42/Microsoft) | 2 Billion Metric Tonnes Coal (Ground-Base) |
| **Strategic Role** | Global AI infrastructure | Sovereign energy feedstock (D1–D8) for NVFC |
"""


def nodal_brief(node):
    data = {
        "NVFC": "The Engine: High-Velocity Cloud for 2B Tonnes Coal.",
        "NRRFC": "The Brain: Asset Fusion (NARICT/NILEST).",
        "NWC": "The Vault: $170.85B Coal & Diamond Valuation.",
        "AWC": "The Vision: Pan-African Sovereign Cloud 2050."
    }
    return data.get(node)


with gr.Blocks(css=custom_css, title="NVFC Sovereign Dashboard") as demo:
    gr.Markdown("# 🦅 NATIONAL VELOCITY FALCON CLOUD (NVFC)")
    gr.Markdown("### GCSLC LTD/GTE | CAC: 176917792057")

    # Sovereign Widget: UAE vs Nigeria comparison
    gr.Markdown("### 🌍 Sovereign Comparison")
    gr.Markdown(SOVEREIGN_COMPARISON)

    # 8R Stealth Paradigm Convergence (UI logic)
    gr.Markdown("### 8R Stealth Paradigm Convergence")
    eight_r_text = " · ".join(EIGHT_R)
    gr.Markdown(f"**{eight_r_text}**")

    with gr.Row():
        node_sel = gr.Dropdown(["NVFC", "NRRFC", "NWC", "AWC"], label="Sovereign Node", value="NVFC")
    output = gr.Textbox(label="Strategic Intelligence", lines=2)
    node_sel.change(nodal_brief, node_sel, output)

    gr.Markdown("---")
    # Hardcoded footer anchor
    gr.Markdown(f"**{SIGNATURE_ANCHOR}**")


if __name__ == "__main__":
    _kill_port_7860()
    print("\n" + "=" * 60)
    print("NVFC SOVEREIGN DASHBOARD")
    print("=" * 60)
    print(f"  Local URL:  {LOCAL_URL}")
    print(f"  {PUBLIC_URL_MSG}")
    print("=" * 60 + "\n")
    sys.stdout.flush()
    sys.stderr.flush()
    demo.launch(share=True, server_port=SERVER_PORT, show_error=True)
