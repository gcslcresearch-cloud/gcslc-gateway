import gradio as gr

# GCSLC Sovereign Branding
NAVY_BG = "#000B1E"
GOLD_SHIMMER = "#D4AF37"

custom_css = """
.gradio-container { background-color: #000B1E !important; border: 2px solid #D4AF37; }
@keyframes shimmer {
    0% { color: #D4AF37; text-shadow: 0 0 5px #D4AF37; }
    50% { color: #FFDF00; text-shadow: 0 0 20px #FFD700; }
    100% { color: #D4AF37; text-shadow: 0 0 5px #D4AF37; }
}
h1, h2, h3 { animation: shimmer 3s infinite; text-align: center; font-family: serif; }
p, span, label { color: #D4AF37 !important; font-weight: bold; }
input, textarea, select { background-color: #001B3A !important; color: white !important; border: 1px solid #D4AF37 !important; }
footer { visibility: hidden; }
"""


def nodal_brief(node):
    data = {
        "NVFC": "The Engine: High-Velocity Cloud for 2B Tonnes Coal.",
        "NRRFC": "The Brain: Asset Fusion (NARICT/NILEST).",
        "NWC": "The Vault: $170.85B Coal & Diamond Valuation.",
        "AWC": "The Vision: Pan-African Sovereign Cloud 2050."
    }
    return data.get(node)


with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("# 🦅 NATIONAL VELOCITY FALCON CLOUD")
    gr.Markdown("### GCSLC LTD/GTE | CAC: 176917792057")

    node_sel = gr.Dropdown(["NVFC", "NRRFC", "NWC", "AWC"], label="Sovereign Node", value="NVFC")
    output = gr.Textbox(label="Strategic Intelligence", lines=2)
    node_sel.change(nodal_brief, node_sel, output)

    gr.Markdown("---")
    gr.Markdown("CHAIRMAN: Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau)")


if __name__ == "__main__":
    demo.launch(share=True)
