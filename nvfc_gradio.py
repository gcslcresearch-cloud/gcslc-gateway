import gradio as gr

# GCSLC Strategic Branding Constants
NAVY_BG = "#000B1E"  # Deepest Navy for maximum contrast
GOLD_SHIMMER = "#D4AF37"

custom_css = """
/* Force Navy Background on all layers */
.gradio-container, .main, .container {
    background-color: #000B1E !important;
}

/* Shimmering Gold Animation */
@keyframes gold-glow {
    0% { color: #B8860B; text-shadow: 0 0 5px #D4AF37; }
    50% { color: #FFDF00; text-shadow: 0 0 20px #FFD700; }
    100% { color: #B8860B; text-shadow: 0 0 5px #D4AF37; }
}

h1, h2, h3 {
    animation: gold-glow 3s infinite;
    font-weight: bold !important;
    text-align: center;
}

/* Visibility Fix for Mac/S24 - Forced Gold Text */
p, span, label, .markdown-text {
    color: #D4AF37 !important;
    font-size: 1.1rem;
}

/* Investor-Grade Input Boxes */
input, textarea, select {
    background-color: #001B3A !important;
    color: white !important;
    border: 2px solid #D4AF37 !important;
}

.stat-box { border: 1px solid #D4AF37; padding: 15px; border-radius: 10px; background: rgba(212, 175, 55, 0.1); }
footer { visibility: hidden; }
.watermark { position: fixed; bottom: 10px; right: 10px; opacity: 0.3; color: #D4AF37; font-size: 10px; }
"""


def nodal_intelligence(module):
    data = {
        "NVFC (The Engine)": "National Velocity Falcon Cloud: High-speed Sovereign AI interface for Nigeria's 2B Tonnes Coal Base.",
        "NRRFC (The Brain)": "National Resources Revitalization Fusion Center: Data synthesis for NARICT, NILEST, and NITT assets.",
        "NWC/C&D (The Vault)": "National Wealth Cloud: Strategic valuation of Coal & Diamond reserves (The $170.85B Portfolio).",
        "AWC/GEC (The Vision)": "African Wealth Cloud / Generative Eagle Cloud: The 2050 Pan-African Sovereign Digital Framework.",
        "Legal Status": "GCSLC LTD/GTE | CAC NAME RESERVATION: 176917792057 | Chairman: Dr. Sa'ad Jaafaru."
    }
    return data.get(module)


with gr.Blocks(css=custom_css, title="GCSLC Sovereign Gateway") as demo:
    gr.HTML("<div class='watermark'>GCSLC CONFIDENTIAL - STRATEGIC LEADERSHIP COMMAND</div>")
    gr.Markdown("# 🦅 NATIONAL VELOCITY FALCON CLOUD (NVFC)")
    gr.Markdown("### GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION (GCSLC) LTD/GTE")

    with gr.Row():
        with gr.Column(elem_classes="stat-box"):
            gr.Markdown("#### STRATEGIC NODE")
            gr.Markdown("2 Billion Metric Tonnes Coal Base")
        with gr.Column(elem_classes="stat-box"):
            gr.Markdown("#### CAC IDENTIFIER")
            gr.Markdown("AVAILABILITY: 176917792057")

    selector = gr.Radio(
        choices=["NVFC (The Engine)", "NRRFC (The Brain)", "NWC/C&D (The Vault)", "AWC/GEC (The Vision)", "Legal Status"],
        label="Sovereign Cloud Nodal Selection",
        value="NVFC (The Engine)"
    )

    display = gr.Textbox(label="Nodal Intelligence Brief", lines=3)
    selector.change(fn=nodal_intelligence, inputs=selector, outputs=display)

    gr.Markdown("---")
    gr.Markdown("**CHAIRMAN & FOUNDER:** Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau)")
    gr.Markdown("**CONTACT:** info@gcslc.center | **ENQUIRIES:** Strategic Leadership Command")

if __name__ == "__main__":
    demo.launch(share=True)
