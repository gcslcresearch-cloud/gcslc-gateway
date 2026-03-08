import gradio as gr

# GCSLC Strategic Branding
NAVY_BLUE = "#001B3A"
SHIMMERING_GOLD = "#D4AF37"
TEXT_WHITE = "#FFFFFF"

custom_css = f"""
.gradio-container {{
    background-color: {NAVY_BLUE} !important;
    border: 3px solid {SHIMMERING_GOLD};
    background-image: linear-gradient(rgba(0, 27, 58, 0.95), rgba(0, 27, 58, 0.95)), url('https://www.transparenttextures.com/patterns/carbon-fibre.png');
}}
h1, h2, h3, p, span, label {{ color: {SHIMMERING_GOLD} !important; text-align: center; font-family: 'Garamond', serif; }}
.stat-box {{ border: 1px solid {SHIMMERING_GOLD}; padding: 15px; border-radius: 10px; background: rgba(212, 175, 55, 0.1); }}
footer {{ visibility: hidden; }}
input, textarea, select {{
    background-color: #002b5c !important;
    color: white !important;
    border: 1px solid {SHIMMERING_GOLD} !important;
}}
/* Watermark Style */
.watermark {{
    position: fixed; bottom: 10px; right: 10px; opacity: 0.3; color: {SHIMMERING_GOLD}; font-size: 10px;
}}
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
