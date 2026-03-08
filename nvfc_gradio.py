import gradio as gr

# GCSLC Strategic Branding Constants
NAVY_BLUE = "#001B3A"  # Deeper, more prestigious Navy
SHIMMERING_GOLD = "#D4AF37"
TEXT_WHITE = "#FFFFFF"

custom_css = f"""
/* Targets the entire background of the page */
.gradio-container {{
    background-color: {NAVY_BLUE} !important;
    color: {TEXT_WHITE} !important;
}}

/* Ensures all markdown and headings are Gold */
h1, h2, h3, p, span {{
    color: {SHIMMERING_GOLD} !important;
    text-align: center;
}}

/* Styles the input dropdown and textboxes to fit the theme */
.gradio-container input, .gradio-container textarea, .gradio-container select {{
    background-color: #002b5c !important; /* Slightly lighter navy for contrast */
    color: {TEXT_WHITE} !important;
    border: 1px solid {SHIMMERING_GOLD} !important;
}}

/* Removes the default Gradio footer for a cleaner 'Sovereign' look */
footer {{ visibility: hidden; }}
"""


def nvfc_briefing(sector):
    # Strategic Intelligence mapping
    data = {
        "Global Context": "UAE (G42/Microsoft) $15.2 Billion AI Cloud vs. Nigeria's 2 Billion Metric Tonnes Coal Base.",
        "8R Framework": "1. Refine 2. Reset 3. Research 4. Restructure 5. Resuscitate 6. Revitalize 7. Re-engineer 8. Retain.",
        "Ground-Base": "13 States in Nigeria hold the catalyst for the National Velocity Falcon Cloud.",
        "Command": "Strategist: Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau)"
    }
    return data.get(sector, "Select a Strategic Pillar to view the Brief.")


with gr.Blocks(css=custom_css, title="GCSLC: NVFC Sovereign Dashboard") as demo:
    gr.Markdown("# 🦅 National Velocity Falcon Cloud (NVFC)")
    gr.Markdown("### GCSLC Strategic Command & Leadership Center")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Image("https://img.icons8.com/ios-filled/100/D4AF37/falcon.png", show_label=False, container=False)
        with gr.Column(scale=4):
            gr.Markdown("**The Nigeria Ground-Base:** 2 Billion Metric Tonnes of Coal.")
            gr.Markdown("**The Engine:** 8R Stealth Paradigm Convergence.")

    with gr.Row():
        pillar = gr.Dropdown(
            choices=["Global Context", "8R Framework", "Ground-Base", "Command"],
            label="Select Strategic Intelligence Pillar",
            value="Global Context"
        )

    output = gr.Textbox(label="Strategic Intelligence Output", lines=4)

    pillar.change(fn=nvfc_briefing, inputs=pillar, outputs=output)

    gr.Markdown("---")
    gr.Markdown("**Anchor:** Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau) | © 2026 GCSLC")

# CRITICAL: This generates your 72-hour public link
if __name__ == "__main__":
    demo.launch(share=True)
