import gradio as gr

# GCSLC Strategic Branding
NAVY_BLUE = "#001B3A"
SHIMMERING_GOLD = "#D4AF37"
TEXT_WHITE = "#FFFFFF"

custom_css = f"""
.gradio-container {{ background-color: {NAVY_BLUE} !important; border: 2px solid {SHIMMERING_GOLD}; }}
h1, h2, h3, p, span, label {{ color: {SHIMMERING_GOLD} !important; text-align: center; }}
.stat-box {{ border: 1px solid {SHIMMERING_GOLD}; padding: 15px; border-radius: 10px; margin: 10px; }}
footer {{ visibility: hidden; }}
/* Professional input styling */
input, textarea, select {{
    background-color: #002b5c !important;
    color: white !important;
    border: 1px solid {SHIMMERING_GOLD} !important;
}}
"""


def investor_briefing(pillar):
    briefs = {
        "Executive Summary": "GCSLC LTD/GTE is spearheading the NVFC to pivot Nigeria's 2B Metric Tonnes of coal into a Green Energy/AI infrastructure.",
        "Market Opportunity": "Benchmark: UAE G42/Microsoft $15.2B Investment. Target: African Sovereign Wealth Cloud 2050.",
        "8R Framework": "Proprietary 8R Stealth Paradigm: Refine, Reset, Research, Restructure, Resuscitate, Revitalize, Re-engineer, Retain.",
        "Legal & Compliance": "Entity: GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION LTD/GTE. CAC Code: 176917792057."
    }
    return briefs.get(pillar)


with gr.Blocks(css=custom_css, title="GCSLC Sovereign Gateway") as demo:
    gr.Markdown("# 🦅 NATIONAL VELOCITY FALCON CLOUD (NVFC)")
    gr.Markdown("### GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION (GCSLC) LTD/GTE")

    with gr.Row():
        with gr.Column(elem_classes="stat-box"):
            gr.Markdown("#### STRATEGIC ASSET")
            gr.Markdown("2 Billion Metric Tonnes Coal Base")
        with gr.Column(elem_classes="stat-box"):
            gr.Markdown("#### CAC STATUS")
            gr.Markdown("Name Reserved: 176917792057")

    pillar_input = gr.Dropdown(
        choices=["Executive Summary", "Market Opportunity", "8R Framework", "Legal & Compliance"],
        label="Select Investor Intelligence Module",
        value="Executive Summary"
    )

    output_text = gr.Textbox(label="Strategic Briefing Output", lines=3)
    pillar_input.change(fn=investor_briefing, inputs=pillar_input, outputs=output_text)

    gr.Markdown("---")
    gr.Markdown("**CHAIRMAN & FOUNDER:** Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau)")
    gr.Markdown("**CONTACT:** info@gcslc.center | **ENQUIRIES:** Strategic Leadership Command")

if __name__ == "__main__":
    demo.launch(share=True)
