"""
NVFC Sovereign Final — D7 Re-engineering consolidated (Gradio).
Bypasses WebSocket/Safari issues. Run: python nvfc_sovereign_final.py
"""
import gradio as gr

# Hard-coded signature (zero-error guard)
SIGNATURE_NAME = "Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau)"
SIGNATURE_TITLE = "Chairman, GCSLC Strategic Command"

# Primary widget: Global Strategic Context (UAE vs. Nigeria)
GLOBAL_STRATEGIC_CONTEXT = """
### 🌍 GLOBAL STRATEGIC CONTEXT

| | |
|---|---|
| **UAE (G42/Microsoft)** | **$15.2B Investment** in AI Cloud |
| **NIGERIA (NGECC)** | **2 Billion MT** Coal Ground-Base |

*Strategic Insight:* The NVFC provides the energy feedstock (D1–D8) that global AI clouds need to thrive.
"""

# 8R Stealth Paradigm Convergence — engine of the NGECC mission (D1–D8)
D1, D2, D3, D4, D5, D6, D7, D8 = (
    "Refinement", "Reset", "Research", "Restructure",
    "Resuscitate", "Revitalize", "Re-engineer", "Retain",
)
EIGHT_R_SIDEBAR = f"""
### 8R Stealth Paradigm Convergence

*Engine of the NGECC mission*

- **D1** {D1}
- **D2** {D2}
- **D3** {D3}
- **D4** {D4}
- **D5** {D5}
- **D6** {D6}
- **D7** {D7}
- **D8** {D8}
"""

# Soft Blue/Navy prestige theme + high-fidelity text
NAVY_CSS = """
.gradio-container { background: linear-gradient(180deg, #0a0a1a 0%, #000033 50%, #0a0a1a 100%) !important; }
.markdown { color: #e8eef4 !important; font-family: system-ui, -apple-system, sans-serif !important; }
.markdown h1, .markdown h2, .markdown h3 { color: #f9f295 !important; letter-spacing: 0.02em !important; }
.markdown strong { color: #f9f295 !important; }
.markdown em { color: #b8c4ce !important; }
footer { visibility: hidden !important; }
"""


demo = gr.Blocks(
    title="NVFC Sovereign Gateway",
    theme=gr.themes.Soft(primary_hue="blue"),
    css=NAVY_CSS,
)
with demo:
    gr.Markdown("# 🦅 National Velocity Falcon Cloud (NVFC)")
    gr.Markdown("---")

    # Primary widget at top: Global Strategic Context (UAE vs. Nigeria)
    gr.Markdown(GLOBAL_STRATEGIC_CONTEXT)
    gr.Markdown("---")

    with gr.Row():
        # Sidebar: 8R Stealth Paradigm (D1–D8) — engine of NGECC
        with gr.Column(scale=1):
            gr.Markdown(EIGHT_R_SIDEBAR)

        with gr.Column(scale=2):
            gr.Markdown("""
### NVFC Strategic Command

*National Velocity Falcon Cloud* — sovereign energy feedstock for global AI infrastructure.
            """)

    gr.Markdown("---")
    # Signature anchor (hard-coded)
    gr.Markdown(f"### 🖋️ {SIGNATURE_NAME}")
    gr.Markdown(f"*{SIGNATURE_TITLE}*")


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
