"""
NVFC Sovereign Pulse — Gradio version (stable render test).
Run: pip install gradio && python nvfc_sovereign_pulse_gradio.py
Opens at http://127.0.0.1:7860 (or http://0.0.0.0:7860).
"""
import gradio as gr

SOVEREIGN = "Sovereign"
PARADIGM = "Paradigm"
SIGNATURE_TITLE = "Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau)"
DETERMINANTS = ("Refinement", "Reset", "Research", "Restructure", "Resuscitate", "Revitalize", "Re-engineer", "Retain")
COAL_STATES = ("Enugu", "Kogi", "Benue", "Nasarawa", "Gombe", "Adamawa", "Delta", "Edo", "Ondo", "Bauchi", "Anambra", "Ebonyi", "Abia")

COMPARISON_WIDGET_MD = """
## 🌍 GLOBAL STRATEGIC CONTEXT

**UAE (G42/Microsoft):** $15.2B Investment in AI Cloud.

**NIGERIA (NGECC):** 2 Billion MT Coal Ground-Base.

*Strategic Gap:* The NVFC provides the energy feedstock (D1–D8) that global clouds need to thrive.
"""


def build_blocks():
    with gr.Blocks(
        title="NVFC Sovereign Pulse",
        css="""
        .gradio-container { background-color: #000033 !important; }
        .markdown { color: #e8eef4 !important; }
        """,
    ) as app:
        gr.Markdown("# GCSLC STRATEGIC COMMAND")

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("**8R Stealth Paradigm Convergence**")
                gr.Markdown("---")
                # Sovereign Comparison Widget (UAE vs. Nigeria) — primary test for stable render
                gr.Markdown(COMPARISON_WIDGET_MD, elem_classes="comparison-widget")
                gr.Markdown("---")
                gr.Markdown("**8R BRAINBOX DETERMINANTS**")
                det_list = "\n".join(f"• D{i+1} {d}" for i, d in enumerate(DETERMINANTS))
                gr.Markdown(det_list)
                gr.Markdown("---")
                gr.Markdown("**STATUS ARCHIVE**\n\n● ACTIVE\n\n● RESERVE")
                gr.Markdown("---")
                gr.Markdown("👤 **Humanoid**\n\n*I need energy to thrive.*")

            with gr.Column(scale=2):
                gr.Markdown("### 🦅 NATIONAL VELOCITY FALCON CLOUD (NVFC)")
                states_line = " · ".join(f"📍 {s}" for s in COAL_STATES)
                gr.Markdown(f"**13 Coal States:**  \n{states_line}\n\n🏛️ Data Centers: Nasarawa · Kogi")
                gr.Markdown("---")
                gr.Markdown("**Industrial Gallery**")
                gr.Markdown(f"""
| | |
|---|---|
| **NGECC Urea Fertilizer** | {SOVEREIGN} feedstock |
| **Activated Carbon** | 8R Stealth {PARADIGM} |
| **AI Hardware Feedstock** | Germanium · high-value |
""")

        gr.Markdown("---")
        # Signature: hard-coded for stable render
        gr.Markdown(f"## {SIGNATURE_TITLE}")
        gr.Markdown("*NVFC STRATEGIC COMMAND | GCSLC LTD/GTE*")

    return app


if __name__ == "__main__":
    app = build_blocks()
    app.launch(server_name="0.0.0.0", server_port=7860)
