"""
GCSLC Sovereign Gateway — NVFC Dashboard (Final).
Galadiman Ruwa Center for Strategic Leadership and Communication.
Navy & Gold theme, interactive Nigeria map (13 coal states), Falcon, Navy Humanoid,
Diamond Opportunity popups, GCSLC watermark, CAC footer. S24: server_name='0.0.0.0', share=True.
"""
import gradio as gr
import os
import subprocess
import sys

SERVER_PORT = 7860

# 13 coal-rich states (user-specified)
COAL_STATES = [
    "Enugu", "Kogi", "Benue", "Nasarawa", "Gombe", "Adamawa", "Delta",
    "Edo", "Ondo", "Bauchi", "Anambra", "Ebonyi", "Abia",
]

# Proven reserves (M Tonnes) — GEC/coastal corridor blend; Kogi district example ~223 in some reports, using 142 from GEC
STATE_RESERVES_MT = {
    "Enugu": 168.0, "Kogi": 223.0, "Benue": 85.0, "Nasarawa": 22.0, "Gombe": 62.0,
    "Adamawa": 12.0, "Delta": 45.0, "Edo": 38.0, "Ondo": 20.0, "Bauchi": 25.0,
    "Anambra": 27.3, "Ebonyi": 15.0, "Abia": 18.0,
}

# By-product market values (D3 / d8_logic)
BY_PRODUCT_GERMANIUM_USD_PER_KG = 8597
BY_PRODUCT_AMMONIA_USD_PER_MT = 430
BY_PRODUCT_SILICON_M = 6.50   # $M monthly yield
BY_PRODUCT_AMMONIUM_SULFATE_USD_PER_MT = 180

# 8R Determinants (R1–R8)
DETERMINANTS_R = ["R1 Refine", "R2 Reset", "R3 Research", "R4 Restructure", "R5 Resuscitate", "R6 Revitalize", "R7 Re-engineer", "R8 Retain"]

CAC_REGISTRATION = "176917792057"

# 8R Stealth Paradigm mission statement
MISSION_8R = (
    "The 8R Stealth Paradigm converges Refine, Reset, Research, Restructure, "
    "Resuscitate, Revitalize, Re-engineer, and Retain to secure sovereign energy and "
    "mineral corridors—ensuring 95% national equity and high-velocity strategic command."
)


def _by_product_html():
    return (
        f"<div class='byproduct-grid'>"
        f"<span class='byproduct-item'>Germanium: <strong>${BY_PRODUCT_GERMANIUM_USD_PER_KG:,.0f}/kg</strong></span>"
        f"<span class='byproduct-item'>Ammonia: <strong>${BY_PRODUCT_AMMONIA_USD_PER_MT:,.0f}/MT</strong></span>"
        f"<span class='byproduct-item'>Silicon: <strong>${BY_PRODUCT_SILICON_M}M</strong> (monthly yield)</span>"
        f"<span class='byproduct-item'>Ammonium Sulfate: <strong>${BY_PRODUCT_AMMONIUM_SULFATE_USD_PER_MT}/MT</strong></span>"
        f"</div>"
    )


def _diamond_popup_html(state: str) -> str:
    reserves = STATE_RESERVES_MT.get(state, 0)
    return f"""
    <div class='diamond-popup gold-border'>
        <h4 class='shimmer'>Diamond Opportunity — {state}</h4>
        <p class='reserves-line'><strong>Proven Reserves:</strong> {state} District: <strong>{reserves:.0f}M Tonnes</strong></p>
        <p class='byproduct-title'>By-Product Market Values</p>
        {_by_product_html()}
    </div>
    """


# Navy & Gold theme, watermark, no right-click, falcon hover, humanoid aura
css = """
.gradio-container, .main, .container { background: #000B1E !important; }
@keyframes gold-shimmer {
  0%, 100% { color: #B8860B; text-shadow: 0 0 12px #D4AF37, 0 0 24px rgba(212,175,55,0.5); opacity: 0.9; }
  50% { color: #FFD700; text-shadow: 0 0 20px #FFD700, 0 0 40px rgba(255,215,0,0.6); opacity: 1; }
}
@keyframes pulse { 0% { opacity: 0.75; } 50% { opacity: 1; } 100% { opacity: 0.75; } }
@keyframes falcon-hover {
  0%, 100% { transform: translateY(0) scale(1); filter: drop-shadow(0 0 12px #D4AF37); }
  50% { transform: translateY(-8px) scale(1.02); filter: drop-shadow(0 0 20px #FFD700); }
}
@keyframes aura-pulse {
  0%, 100% { opacity: 0.4; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.05); }
}
.shimmer { color: #D4AF37; text-shadow: 0 0 15px #D4AF37; animation: gold-shimmer 2.2s ease-in-out infinite; }
.shimmer-sub { color: #B8860B; animation: pulse 2.5s infinite; }
.shimmer-8r { color: #D4AF37; animation: gold-shimmer 2.5s ease-in-out infinite; font-weight: 600; }
h1, h2, h3, h4 { color: #D4AF37 !important; }
p, span, label { color: #e8eef4 !important; }
.gold-border { border: 2px solid #D4AF37; border-radius: 12px; background: linear-gradient(135deg, #001A35 0%, #000B1E 100%); }
/* GCSLC Watermark & IP protection */
.gcslc-watermark {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  pointer-events: none; z-index: 9999;
  background: repeating-linear-gradient(-30deg, transparent, transparent 80px, rgba(212,175,55,0.03) 80px, rgba(212,175,55,0.03) 160px);
}
.gcslc-watermark::after {
  content: "GCSLC PROPRIETARY"; position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%) rotate(-25deg); font-size: 3rem; font-weight: 700;
  color: rgba(212,175,55,0.06); letter-spacing: 0.2em; white-space: nowrap;
}
.gradio-container { user-select: none; -webkit-user-select: none; -moz-user-select: none; -ms-user-select: none; }
.gradio-container * { user-select: none; -webkit-user-select: none; }
/* Disable right-click / screenshot discouragement via overlay (context menu still browser-controlled; we discourage copy) */
.diamond-popup { padding: 20px; margin: 12px 0; }
.reserves-line, .byproduct-title { margin: 8px 0; color: #e8eef4; }
.byproduct-title { color: #D4AF37; font-weight: 600; margin-top: 12px; }
.byproduct-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px; }
.byproduct-item { color: #b8c4ce; font-size: 0.9rem; }
.falcon-hover { animation: falcon-hover 2s ease-in-out infinite; display: inline-block; }
.btn-glow { background: linear-gradient(135deg, #D4AF37, #B8860B) !important; color: #000B1E !important; font-weight: 700 !important; border: none !important; box-shadow: 0 0 20px rgba(212,175,55,0.6); animation: pulse 2s infinite; }
.humanoid-aura { position: relative; display: inline-flex; flex-wrap: wrap; justify-content: center; gap: 6px; padding: 16px; }
.humanoid-aura .r-badge { padding: 4px 10px; border-radius: 8px; background: rgba(0,26,53,0.9); border: 1px solid #D4AF37; color: #D4AF37; font-size: 0.75rem; animation: aura-pulse 2s ease-in-out infinite; }
.humanoid-aura .r-badge:nth-child(1) { animation-delay: 0s; }
.humanoid-aura .r-badge:nth-child(2) { animation-delay: 0.2s; }
.humanoid-aura .r-badge:nth-child(3) { animation-delay: 0.4s; }
.humanoid-aura .r-badge:nth-child(4) { animation-delay: 0.6s; }
.humanoid-aura .r-badge:nth-child(5) { animation-delay: 0.8s; }
.humanoid-aura .r-badge:nth-child(6) { animation-delay: 1s; }
.humanoid-aura .r-badge:nth-child(7) { animation-delay: 1.2s; }
.humanoid-aura .r-badge:nth-child(8) { animation-delay: 1.4s; }
.state-node { min-width: 100px; }
"""


def _nigeria_map_svg():
    """Simplified Nigeria outline SVG (approximate shape) for sovereign map."""
    return """
    <svg class="nigeria-outline" viewBox="0 0 200 280" xmlns="http://www.w3.org/2000/svg" style="max-width: 100%; height: auto;">
      <path fill="none" stroke="#D4AF37" stroke-width="2" opacity="0.8"
        d="M100 20 L140 40 L160 80 L155 140 L165 200 L140 250 L100 265 L60 250 L40 200 L30 120 L50 60 Z"/>
      <text x="100" y="150" text-anchor="middle" fill="rgba(212,175,55,0.4)" font-size="14">NIGERIA</text>
    </svg>
    """


def _map_section_html():
    return f"""
    <div class='gold-border' style='padding: 20px; text-align: center;'>
        <h3 class='shimmer'>Sovereign Resource Map — Nigeria</h3>
        <p style='color: #b8c4ce; font-size: 0.9rem; margin: 8px 0;'>13 Coal-Rich States — Click a node below</p>
        {_nigeria_map_svg()}
    </div>
    """


def _falcon_html():
    return """
    <div class='gold-border falcon-hover' style='padding: 24px; text-align: center;'>
        <div style='font-size: 64px; line-height: 1;' title='High-Velocity Falcon'>🦅</div>
        <p class='shimmer-sub' style='margin-top: 8px; font-size: 0.9rem;'>Falcon — Hovering over the 13 States</p>
    </div>
    """


def _humanoid_html():
    r_badges = "".join(f"<span class='r-badge'>{d}</span>" for d in DETERMINANTS_R)
    return f"""
    <div class='gold-border' style='padding: 24px; text-align: center;'>
        <div class='humanoid-aura'>
            <div style='width: 100%; margin-bottom: 12px;'>
                <div style='width: 60px; height: 100px; margin: 0 auto; background: linear-gradient(180deg, #0a1628 0%, #0d2137 40%, #001a33 100%); border: 2px solid #D4AF37; border-radius: 12px; position: relative; box-shadow: 0 0 20px rgba(0,43,91,0.8);'>
                    <div style='width: 24px; height: 24px; background: #001a33; border: 2px solid #D4AF37; border-radius: 50%; position: absolute; top: 8px; left: 50%; transform: translateX(-50%);'></div>
                </div>
            </div>
            <div style='width: 100%; position: relative; margin: 8px 0 12px 0;'>
                <p class='bubble-text' style='background: #001A35; border: 2px solid #D4AF37; border-radius: 12px; padding: 12px 16px; color: #e8eef4; font-size: 0.9rem; margin: 0;'>
                    &ldquo;I need energy to thrive; process the coal and its by-products—they're my power.&rdquo;
                </p>
            </div>
            <div style='width: 100%;'>{r_badges}</div>
        </div>
        <p class='shimmer-sub' style='margin-top: 12px; font-size: 0.8rem;'>Navy Humanoid — Determinants R1–R8</p>
    </div>
    """


def _footer_html():
    return f"""
    <div style='text-align: center; padding: 16px; margin-top: 24px; border-top: 1px solid rgba(212,175,55,0.3);'>
        <p class='shimmer-sub' style='font-size: 0.85rem; margin: 0;'>CAC Registration: {CAC_REGISTRATION}</p>
        <p style='color: #b8c4ce; font-size: 0.8rem; margin: 4px 0 0 0;'>Galadiman Ruwa Center for Strategic Leadership and Communication (GCSLC) LTD/GTE</p>
        <p style='color: rgba(184,196,206,0.7); font-size: 0.75rem; margin: 4px 0 0 0;'>© GCSLC. Proprietary. 8R Stealth Paradigm.</p>
    </div>
    """


def _clear_gradio_cache():
    for d in [os.path.expanduser("~/.cache/gradio"), os.path.expanduser("~/.gradio")]:
        if os.path.isdir(d):
            try:
                import shutil
                shutil.rmtree(d, ignore_errors=True)
            except Exception:
                pass


def _kill_port():
    try:
        subprocess.run("lsof -ti:7860 | xargs kill -9", shell=True, capture_output=True, timeout=5)
    except Exception:
        pass


with gr.Blocks(css=css, title="GCSLC Sovereign Gateway — NVFC") as demo:
    # Watermark overlay + disable right-click (IP / screenshot protection)
    gr.HTML("""
    <div class='gcslc-watermark' aria-hidden='true'></div>
    <script>
    (function(){
      document.addEventListener('contextmenu', function(e) { e.preventDefault(); });
      document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.gradio-container').forEach(function(el) { el.addEventListener('contextmenu', function(e) { e.preventDefault(); }); });
      });
    })();
    </script>
    """)

    # Header & Prestige Branding
    gr.HTML(
        "<h1 class='shimmer' style='text-align: center; font-size: 1.4rem; margin-bottom: 8px;'>"
        "Galadiman Ruwa Center for Strategic Leadership and Communication"
        "</h1>"
    )
    gr.HTML(
        f"<p class='shimmer-8r' style='text-align: center; font-size: 1rem; max-width: 720px; margin: 0 auto 24px auto; line-height: 1.4;'>"
        f"{MISSION_8R}"
        "</p>"
    )

    # Interactive Sovereign Map: Nigeria SVG + clickable state nodes
    gr.HTML(_map_section_html())
    with gr.Row():
        state_buttons = []
        for s in COAL_STATES:
            btn = gr.Button(s, elem_classes=["state-node"], variant="secondary")
            state_buttons.append((s, btn))
    popup_out = gr.HTML(value=_diamond_popup_html("Kogi"), label="Diamond Opportunity")

    def make_click_fn(s):
        def _fn():
            return _diamond_popup_html(s)
        return _fn
    for state, btn in state_buttons:
        btn.click(fn=make_click_fn(state), inputs=None, outputs=popup_out)

    gr.Markdown("---")

    # Falcon + GO TAP INTO IT
    with gr.Row():
        with gr.Column(scale=1):
            gr.HTML(_falcon_html())
            go_btn = gr.Button("GO TAP INTO IT", elem_classes=["btn-glow"], variant="primary")
        with gr.Column(scale=2):
            gr.HTML(_humanoid_html())

    gr.Markdown("---")
    gr.HTML(_footer_html())

    def _go_tap(_):
        return None  # Optional: trigger a message or reload
    go_btn.click(fn=_go_tap, inputs=None, outputs=None)


if __name__ == "__main__":
    _clear_gradio_cache()
    _kill_port()
    print("\n" + "=" * 60)
    print("  GCSLC Sovereign Gateway — Local: http://127.0.0.1:7860")
    print("  Public URL below (share=True). Save on Samsung S24 Ultra.")
    print("=" * 60 + "\n")
    sys.stdout.flush()
    demo.launch(share=True, server_name="0.0.0.0", server_port=SERVER_PORT, show_error=True)
