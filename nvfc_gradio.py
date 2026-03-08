import gradio as gr


def get_sovereign_context():
    return """
    ### 🌍 GLOBAL STRATEGIC CONTEXT
    **UAE (G42/Microsoft):** $15.2B Investment in AI Cloud.
    **NIGERIA (NGECC):** 2 Billion MT Coal Ground-Base.
    
    *Strategic Insight:* The NVFC provides the energy feedstock (D1-D8) 
    that global AI clouds need to thrive.
    """


with gr.Blocks(title="NVFC Sovereign Gateway", theme=gr.themes.Soft(primary_hue="blue")) as demo:
    gr.Markdown("# 🦅 National Velocity Falcon Cloud (NVFC)")
    gr.Markdown("---")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 8R Stealth Paradigm")
            gr.Markdown("- Refine & Reset\n- Research & Restructure\n- Resuscitate & Revitalize\n- Re-engineer & Retain")

        with gr.Column(scale=2):
            gr.Markdown(get_sovereign_context())

    gr.Markdown("---")
    gr.Markdown("### 🖋️ Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau)")
    gr.Markdown("*Chairman, GCSLC Strategic Command*")


if __name__ == "__main__":
    demo.launch(server_port=7860, share=True)
