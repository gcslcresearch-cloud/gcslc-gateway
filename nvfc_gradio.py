"""
GCSLC Strategic Command Center — NVFC High-Velocity (Zero-Error Final).
Galadiman Ruwa Center for Strategic Leadership and Communication.
Strict: Shimmer title + Hook, SVG Nigeria map + pulsing nodes, Falcon over map,
Navy Humanoid + circular R1–R8 aura, signature, watermark, CAC. server_name='0.0.0.0'.
"""
import gradio as gr
import os
import subprocess
import sys

SERVER_PORT = 7860

COAL_STATES = [
    "Enugu", "Kogi", "Benue", "Nasarawa", "Gombe", "Adamawa", "Delta",
    "Edo", "Ondo", "Bauchi", "Anambra", "Ebonyi", "Abia",
]

STATE_RESERVES_MT = {
    "Enugu": 168.0, "Kogi": 223.0, "Benue": 85.0, "Nasarawa": 22.0, "Gombe": 62.0,
    "Adamawa": 12.0, "Delta": 45.0, "Edo": 38.0, "Ondo": 20.0, "Bauchi": 25.0,
    "Anambra": 27.3, "Ebonyi": 15.0, "Abia": 18.0,
}

BY_PRODUCT_GERMANIUM_USD_PER_KG = 8597
BY_PRODUCT_AMMONIA_USD_PER_MT = 430
BY_PRODUCT_SILICON_M = 6.50

DETERMINANTS_R = ["R1 Refine", "R2 Reset", "R3 Research", "R4 Restructure", "R5 Resuscitate", "R6 Revitalize", "R7 Re-engineer", "R8 Retain"]

CAC_REGISTRATION = "176917792057"
CHAIRMAN_SIGNATURE = "Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau), Chairman, GCSLC Strategic Command"

HOOK_TEXT = (
    "(We believe everything is powered and anchored by The 8R Stealth Paradigm Convergence and its Determinants. "
    "Let's converge from the human world to the AI/Robotics world for you to understand.)"
)


def _diamond_popup_html(state: str) -> str:
    reserves = STATE_RESERVES_MT.get(state, 0)
    return f"""
    <div class='diamond-popup gold-border'>
        <h4 class='shimmer'>Diamond Opportunity — {state}</h4>
        <p class='reserves-line'><strong>Proven Reserves:</strong> {state} District: <strong>{reserves:.0f}M Tonnes</strong></p>
        <p class='byproduct-title'>Market Values (By-Products)</p>
        <div class='byproduct-grid'>
            <span class='byproduct-item'>Germanium: <strong>${BY_PRODUCT_GERMANIUM_USD_PER_KG:,.0f}/kg</strong></span>
            <span class='byproduct-item'>Ammonia: <strong>${BY_PRODUCT_AMMONIA_USD_PER_MT:,.0f}/MT</strong></span>
            <span class='byproduct-item'>Silicon: <strong>${BY_PRODUCT_SILICON_M}M</strong> (monthly yield)</span>
        </div>
    </div>
    """


# High-velocity SVG: Nigeria outline with animated stroke
def _nigeria_map_svg():
    return """
    <svg class="nigeria-hv-map" viewBox="0 0 240 320" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="goldStroke" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#B8860B"/>
          <stop offset="50%" style="stop-color:#FFD700"/>
          <stop offset="100%" style="stop-color:#D4AF37"/>
        </linearGradient>
        <filter id="glow">
          <feGaussianBlur stdDeviation="2" result="blur"/>
          <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
      </defs>
      <path class="nigeria-path" fill="rgba(0,26,53,0.4)" stroke="url(#goldStroke)" stroke-width="2.5"
        d="M120 25 L165 50 L185 95 L178 160 L188 220 L162 275 L120 295 L78 275 L55 220 L45 140 L65 75 Z"/>
      <text x="120" y="165" text-anchor="middle" fill="rgba(212,175,55,0.35)" font-size="16" font-weight="700">NIGERIA</text>
    </svg>
    """


# Falcon SVG — high-resolution bird icon (streamlined falcon, not eagle)
def _falcon_svg():
    return """
    <svg class="falcon-over-map" viewBox="0 0 80 56" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="falconGold" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#B8860B"/>
          <stop offset="100%" style="stop-color:#FFD700"/>
        </linearGradient>
      </defs>
      <path fill="url(#falconGold)" stroke="#D4AF37" stroke-width="0.8" opacity="0.95"
        d="M12 28 Q20 8 40 14 Q52 18 58 26 Q64 32 68 38 L72 36 Q66 28 58 22 Q48 16 38 14 Q24 12 16 24 L12 28 Z"/>
      <path fill="url(#falconGold)" d="M38 16 L42 14 L48 20 L46 24 Z"/>
      <ellipse cx="44" cy="26" rx="4" ry="5" fill="#1a0a00"/>
      <path fill="none" stroke="url(#falconGold)" stroke-width="1" d="M50 22 L56 18 M48 28 L54 32"/>
    </svg>
    """


def _map_with_falcon_html():
    return f"""
    <div class="map-falcon-wrap gold-border">
        <h3 class="shimmer">Sovereign Resource Map — Nigeria</h3>
        <p class="map-sub">13 Coal-Rich States — Live Pulsing Nodes (click below)</p>
        <div class="nigeria-map-container">
            {_nigeria_map_svg()}
            <div class="falcon-hover-over-map" aria-hidden="true">{_falcon_svg()}</div>
        </div>
    </div>
    """


# Navy Humanoid: professional avatar + speech bubble + circular R1–R8 aura
def _humanoid_html():
    # R badges positioned on a circle (8 points)
    r_positions = [
        (50, 0), (85, 15), (100, 50), (85, 85), (50, 100), (15, 85), (0, 50), (15, 15)
    ]
    r_badges = []
    for i, (x, y) in enumerate(r_positions):
        r_badges.append(
            f'<span class="r-orb r-orb-{i+1}" style="left:{x}%; top:{y}%;">{DETERMINANTS_R[i]}</span>'
        )
    r_ring = "".join(r_badges)
    return f"""
    <div class="gold-border humanoid-exhibit">
        <p class="shimmer-sub exhibit-label">The Navy Humanoid — Determinant Exhibit</p>
        <div class="determinant-aura">
            {r_ring}
            <div class="navy-humanoid-avatar">
                <svg viewBox="0 0 64 100" class="humanoid-svg">
                    <defs><linearGradient id="navyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" style="stop-color:#0a1628"/>
                        <stop offset="50%" style="stop-color:#0d2137"/>
                        <stop offset="100%" style="stop-color:#001a33"/>
                    </linearGradient></defs>
                    <ellipse cx="32" cy="18" rx="14" ry="16" fill="url(#navyGrad)" stroke="#D4AF37" stroke-width="1.5"/>
                    <path fill="url(#navyGrad)" stroke="#D4AF37" stroke-width="1.2" d="M22 36 L32 50 L42 36 L38 90 L26 90 Z"/>
                    <rect x="28" y="50" width="8" height="42" rx="2" fill="url(#navyGrad)" stroke="#D4AF37"/>
                </svg>
            </div>
            <div class="speech-bubble-wrap">
                <p class="speech-bubble">"I need energy to thrive; process the coal and its by-products—they're my power."</p>
            </div>
        </div>
    </div>
    """


def _footer_html():
    return f"""
    <div class="footer-signature">
        <p class="signature-line shimmer-sub">{CHAIRMAN_SIGNATURE}</p>
        <p class="cac-line">CAC Registration: {CAC_REGISTRATION}</p>
        <p class="legal-line">Galadiman Ruwa Center for Strategic Leadership and Communication (GCSLC) LTD/GTE</p>
        <p class="copyright-line">© GCSLC. Proprietary. GCSLC Strategic Command.</p>
    </div>
    """


# CSS: shimmer, pulsing nodes, falcon over map, circular aura, watermark, protection
css = """
.gradio-container, .main, .container { background: #000B1E !important; }
@keyframes gold-shimmer {
  0%, 100% { color: #B8860B; text-shadow: 0 0 12px #D4AF37, 0 0 24px rgba(212,175,55,0.5); opacity: 0.95; }
  50% { color: #FFD700; text-shadow: 0 0 20px #FFD700, 0 0 40px rgba(255,215,0,0.6); opacity: 1; }
}
@keyframes node-pulse {
  0%, 100% { box-shadow: 0 0 8px rgba(212,175,55,0.5), 0 0 16px rgba(212,175,55,0.3); border-color: #B8860B; }
  50% { box-shadow: 0 0 16px #D4AF37, 0 0 28px rgba(255,215,0,0.5); border-color: #FFD700; }
}
@keyframes falcon-float {
  0%, 100% { transform: translate(-50%, -50%) translateY(0) scale(1); filter: drop-shadow(0 0 10px #D4AF37); }
  50% { transform: translate(-50%, -50%) translateY(-12px) scale(1.05); filter: drop-shadow(0 0 18px #FFD700); }
}
@keyframes path-dash {
  to { stroke-dashoffset: 0; }
}
.shimmer { color: #D4AF37; animation: gold-shimmer 2.2s ease-in-out infinite; }
.shimmer-sub { color: #B8860B; }
.gold-border { border: 2px solid #D4AF37; border-radius: 12px; background: linear-gradient(135deg, #001A35 0%, #000B1E 100%); }
h1, h2, h3, h4 { color: #D4AF37 !important; }
p, span, label { color: #e8eef4 !important; }

/* GCSLC PROPRIETARY watermark — fully active */
.gcslc-watermark {
  position: fixed !important; top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
  pointer-events: none !important; z-index: 99999 !important;
  background: repeating-linear-gradient(-28deg, transparent 0, transparent 70px, rgba(212,175,55,0.04) 70px, rgba(212,175,55,0.04) 140px) !important;
}
.gcslc-watermark::after {
  content: "GCSLC PROPRIETARY" !important; position: absolute !important; top: 50% !important; left: 50% !important;
  transform: translate(-50%, -50%) rotate(-22deg) !important; font-size: clamp(2rem, 4vw, 3.5rem) !important;
  font-weight: 700 !important; color: rgba(212,175,55,0.08) !important; letter-spacing: 0.25em !important;
  white-space: nowrap !important;
}
/* Screenshot / copy prevention */
.gradio-container { user-select: none !important; -webkit-user-select: none !important; -moz-user-select: none !important; -ms-user-select: none !important; }
.gradio-container * { user-select: none !important; -webkit-user-select: none !important; }

.diamond-popup { padding: 20px; margin: 12px 0; }
.reserves-line, .byproduct-title { margin: 8px 0; color: #e8eef4; }
.byproduct-title { color: #D4AF37; font-weight: 600; margin-top: 12px; }
.byproduct-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 8px; }
.byproduct-item { color: #b8c4ce; font-size: 0.9rem; }

/* High-velocity map container + Falcon hovering over it */
.map-falcon-wrap { padding: 20px; text-align: center; position: relative; }
.map-sub { color: #b8c4ce; font-size: 0.9rem; margin: 8px 0 12px 0; }
.nigeria-map-container { position: relative; display: inline-block; max-width: 280px; margin: 0 auto; }
.nigeria-hv-map { width: 100%; height: auto; display: block; }
.nigeria-path { stroke-dasharray: 1200; stroke-dashoffset: 1200; animation: path-dash 3s ease-out 1 forwards; }
.falcon-hover-over-map {
  position: absolute !important; left: 50% !important; top: 45% !important;
  width: 72px; height: 52px; margin-left: -36px; margin-top: -26px;
  animation: falcon-float 2.4s ease-in-out infinite;
  pointer-events: none; z-index: 5;
}
.falcon-over-map { width: 100%; height: 100%; filter: drop-shadow(0 0 12px rgba(212,175,55,0.7)); }

/* Live pulsing state nodes (golden glow) */
.state-node { min-width: 100px; animation: node-pulse 2s ease-in-out infinite !important;
  border: 2px solid #D4AF37 !important; color: #D4AF37 !important;
  background: rgba(0,26,53,0.9) !important; font-weight: 600 !important;
}
.state-node:hover { box-shadow: 0 0 20px #FFD700, 0 0 36px rgba(255,215,0,0.4) !important; }

/* Navy Humanoid: circular Determinant Aura (R1–R8) */
.humanoid-exhibit { padding: 24px; text-align: center; }
.exhibit-label { font-size: 0.85rem; margin-bottom: 12px; }
.determinant-aura { position: relative; width: 260px; height: 260px; margin: 0 auto; }
.navy-humanoid-avatar { position: absolute; left: 50%; top: 42%; transform: translate(-50%, -50%); width: 70px; height: 110px; z-index: 2; }
.humanoid-svg { width: 100%; height: 100%; filter: drop-shadow(0 0 10px rgba(0,43,91,0.9)); }
.speech-bubble-wrap { position: absolute; left: 50%; top: 78%; transform: translate(-50%, -50%); width: 92%; z-index: 3; }
.speech-bubble { background: #001A35; border: 2px solid #D4AF37; border-radius: 12px; padding: 10px 14px; margin: 0; font-size: 0.82rem; color: #e8eef4; line-height: 1.35; }
.r-orb { position: absolute; transform: translate(-50%, -50%); padding: 4px 8px; border-radius: 20px;
  background: rgba(0,26,53,0.95); border: 1px solid #D4AF37; color: #D4AF37; font-size: 0.65rem; font-weight: 600;
  animation: aura-pulse 2.2s ease-in-out infinite; white-space: nowrap;
}
@keyframes aura-pulse { 0%, 100% { opacity: 0.7; transform: translate(-50%, -50%) scale(1); } 50% { opacity: 1; transform: translate(-50%, -50%) scale(1.08); } }
.r-orb-1 { left: 50%; top: 0%; }
.r-orb-2 { left: 92%; top: 15%; }
.r-orb-3 { left: 100%; top: 50%; }
.r-orb-4 { left: 92%; top: 85%; }
.r-orb-5 { left: 50%; top: 100%; }
.r-orb-6 { left: 8%; top: 85%; }
.r-orb-7 { left: 0%; top: 50%; }
.r-orb-8 { left: 8%; top: 15%; }

.footer-signature { text-align: center; padding: 20px 16px; margin-top: 24px; border-top: 1px solid rgba(212,175,55,0.35); }
.signature-line { font-size: 0.9rem; margin: 0 0 8px 0; font-weight: 600; }
.cac-line { font-size: 0.85rem; color: #D4AF37; margin: 0 0 4px 0; }
.legal-line { font-size: 0.8rem; color: #b8c4ce; margin: 0 0 4px 0; }
.copyright-line { font-size: 0.75rem; color: rgba(184,196,206,0.75); margin: 0; }
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


with gr.Blocks(css=css, title="GCSLC Strategic Command Center — NVFC") as demo:
    # GCSLC PROPRIETARY watermark + screenshot/right-click prevention (fully active)
    gr.HTML("""
    <div class='gcslc-watermark' aria-hidden='true'></div>
    <script>
    (function(){
      function noRightClick(e) { e.preventDefault(); return false; }
      document.addEventListener('contextmenu', noRightClick);
      document.addEventListener('DOMContentLoaded', function() {
        var r = document.querySelector('.gradio-container');
        if (r) r.addEventListener('contextmenu', noRightClick);
      });
    })();
    </script>
    """)

    # Correct Branding: title at absolute top, then Hook
    gr.HTML(
        "<h1 class='shimmer' style='text-align: center; font-size: 1.35rem; margin-bottom: 6px;'>"
        "Galadiman Ruwa Center for Strategic Leadership and Communication"
        "</h1>"
    )
    gr.HTML(
        f"<p style='text-align: center; font-size: 0.95rem; max-width: 720px; margin: 0 auto 20px auto; line-height: 1.45; color: #e8eef4;'>"
        f"{HOOK_TEXT}"
        "</p>"
    )

    # Interactive Map of Nigeria (high-velocity SVG) + Falcon hovering over the 13 states
    gr.HTML(_map_with_falcon_html())
    # Live pulsing nodes: 13 coal-rich states with golden glow
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

    # Navy Humanoid (Determinant Exhibit): professional avatar + speech bubble + circular R1–R8 aura
    gr.HTML(_humanoid_html())

    gr.Markdown("---")
    gr.HTML(_footer_html())


if __name__ == "__main__":
    _clear_gradio_cache()
    _kill_port()
    print("\n" + "=" * 60)
    print("  GCSLC Strategic Command Center — Local: http://127.0.0.1:7860")
    print("  Samsung S24 Ultra: use LAN IP or public URL (share=True).")
    print("=" * 60 + "\n")
    sys.stdout.flush()
    demo.launch(share=True, server_name="0.0.0.0", server_port=SERVER_PORT, show_error=True)
