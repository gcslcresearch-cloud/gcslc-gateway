"""
GCSLC Sovereign Gateway — Prestige Lock (High-Velocity Final).
Galadiman Ruwa Center for Strategic Leadership and Communication (GCSLC - LTD/GTE).
Detailed Nigeria SVG map, Gold+White pulsing corridors, Diamond expand, Musical Falcon (Talon Lock),
3D Navy Humanoid with orbiting R1–R8, branding, signature, watermark, anti-screenshot. server_name='0.0.0.0'.
"""
import base64
import math
import gradio as gr
import os
import subprocess
import struct
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

# Approximate (x%, y%) on map for falcon landing — viewBox 280 360
STATE_MAP_POS = {
    "Enugu": (52, 72), "Kogi": (48, 58), "Benue": (58, 62), "Nasarawa": (50, 48),
    "Gombe": (62, 42), "Adamawa": (68, 48), "Delta": (38, 78), "Edo": (42, 68),
    "Ondo": (36, 62), "Bauchi": (58, 38), "Anambra": (50, 75), "Ebonyi": (54, 72), "Abia": (52, 78),
}

BY_PRODUCT_GERMANIUM_USD_PER_KG = 8597
BY_PRODUCT_AMMONIA_USD_PER_MT = 430
BY_PRODUCT_SILICON_M = 6.50
BY_PRODUCT_AMMONIUM_SULFATE_USD_PER_MT = 180

DETERMINANTS_R = ["R1 Refine", "R2 Reset", "R3 Research", "R4 Restructure", "R5 Resuscitate", "R6 Revitalize", "R7 Re-engineer", "R8 Retain"]

CAC_REGISTRATION = "176917792057"
CHAIRMAN_SIGNATURE = "Dr. Sa'ad Jaafaru (Galadiman Ruwan Zazzau), Chairman, GCSLC Strategic Command"

HOOK_TEXT = (
    "(We believe everything is powered and anchored by The 8R Stealth Paradigm Convergence and its Determinants. "
    "Let's converge from the human world to the AI/Robotics world for you to understand.)"
)

TITLE_FULL = "Galadiman Ruwa Center for Strategic Leadership and Communication (GCSLC - LTD/GTE)"


def _falcon_cry_data_url() -> str:
    """Generate a minimal WAV (0.25s high-velocity tone) as data URL for Falcon Cry on Diamond reveal."""
    sample_rate = 8000
    duration_sec = 0.25
    freq = 880
    n_samples = int(sample_rate * duration_sec)
    max_val = 32767 * 0.3
    frames = []
    for i in range(n_samples):
        t = i / sample_rate
        val = int(max_val * math.sin(2 * math.pi * freq * t) * (1 - i / n_samples))
        frames.append(struct.pack("<h", max(-32768, min(32767, val))))
    wav_data = b"".join(frames)
    # WAV header (44 bytes)
    channels, bits = 1, 16
    block_align = channels * (bits // 8)
    byte_rate = sample_rate * block_align
    data_size = len(wav_data)
    header = (
        b"RIFF" + struct.pack("<I", 36 + data_size) + b"WAVE"
        + b"fmt " + struct.pack("<IHHIIHH", 16, 1, channels, sample_rate, byte_rate, block_align, bits)
        + b"data" + struct.pack("<I", data_size)
    )
    b64 = base64.b64encode(header + wav_data).decode("ascii")
    return f"data:audio/wav;base64,{b64}"


def _diamond_popup_html(state: str, with_audio: bool = True) -> str:
    reserves = STATE_RESERVES_MT.get(state, 0)
    audio_tag = ""
    if with_audio:
        audio_tag = f'<audio id="falcon-cry" autoplay><source src="{_falcon_cry_data_url()}" type="audio/wav"></audio>'
    return f"""
    <div class="diamond-popup diamond-popup-expand gold-border">
        {audio_tag}
        <h4 class="shimmer">Diamond Opportunity — {state}</h4>
        <p class="reserves-line"><strong>Proven Reserves:</strong> {state} District: <strong>{reserves:.0f}M Tonnes</strong></p>
        <p class="byproduct-title">By-Products (Market Values)</p>
        <div class="byproduct-grid">
            <span class="byproduct-item">Germanium: <strong>${BY_PRODUCT_GERMANIUM_USD_PER_KG:,.0f}/kg</strong></span>
            <span class="byproduct-item">Ammonia: <strong>${BY_PRODUCT_AMMONIA_USD_PER_MT:,.0f}/MT</strong></span>
            <span class="byproduct-item">Silicon: <strong>${BY_PRODUCT_SILICON_M}M</strong> (monthly yield)</span>
            <span class="byproduct-item">Ammonium Sulfate: <strong>${BY_PRODUCT_AMMONIUM_SULFATE_USD_PER_MT}/MT</strong></span>
        </div>
    </div>
    """


# Detailed high-resolution Nigeria SVG (multi-segment path, no simple polygon)
def _nigeria_detailed_svg():
    return """
    <svg class="nigeria-hv-map" viewBox="0 0 280 360" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="goldStroke" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#B8860B"/>
          <stop offset="50%" style="stop-color:#FFD700"/>
          <stop offset="100%" style="stop-color:#D4AF37"/>
        </linearGradient>
        <linearGradient id="fillNg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:rgba(0,26,53,0.5)"/>
          <stop offset="100%" style="stop-color:rgba(0,11,30,0.6)"/>
        </linearGradient>
      </defs>
      <path class="nigeria-path" fill="url(#fillNg)" stroke="url(#goldStroke)" stroke-width="2"
        d="M140 22 L175 38 L198 68 L202 105 L210 145 L218 185 L212 235 L188 278 L148 338 L118 338 L85 300 L62 255 L48 205 L42 155 L52 105 L72 65 L95 38 L120 22 Z"/>
      <path class="nigeria-path" fill="none" stroke="url(#goldStroke)" stroke-width="1.2" opacity="0.7"
        d="M140 22 L175 38 L198 68 L202 105 L210 145 L218 185 L212 235 L188 278 L148 338 L118 338 L85 300 L62 255 L48 205 L42 155 L52 105 L72 65 L95 38 L120 22 Z"/>
      <text x="140" y="185" text-anchor="middle" fill="rgba(212,175,55,0.25)" font-size="18" font-weight="700">NIGERIA</text>
    </svg>
    """


def _falcon_prestige_svg():
    """High-Prestige Falcon SVG (Talon Lock)."""
    return """
    <svg class="falcon-prestige" viewBox="0 0 96 64" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="fg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:#5c4a00"/>
          <stop offset="40%" style="stop-color:#D4AF37"/>
          <stop offset="100%" style="stop-color:#FFD700"/>
        </linearGradient>
        <filter id="fglow"><feGaussianBlur stdDeviation="1.5" result="b"/>
          <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      </defs>
      <g filter="url(#fglow)">
        <path fill="url(#fg)" stroke="#B8860B" stroke-width="1"
          d="M14 32 Q24 8 48 14 Q64 20 72 30 Q78 36 82 42 L88 40 Q82 30 74 24 Q62 16 46 14 Q28 10 18 26 L14 32 Z"/>
        <path fill="url(#fg)" d="M46 16 L52 14 L60 22 L58 26 Z"/>
        <ellipse cx="56" cy="30" rx="5" ry="6" fill="#0a0a00"/>
        <path fill="none" stroke="url(#fg)" stroke-width="1.2" d="M64 26 L72 22 M62 32 L70 36"/>
      </g>
    </svg>
    """


def _map_with_falcon_html(selected_state: str | None) -> str:
    """Map + Falcon that flies from header to selected state (Talon Lock)."""
    svg = _nigeria_detailed_svg()
    falcon_svg = _falcon_prestige_svg()
    if selected_state and selected_state in STATE_MAP_POS:
        x, y = STATE_MAP_POS[selected_state]
        # Falcon lands at (x%, y%) with fly-in animation
        falcon_div = (
            f'<div class="falcon-landed falcon-fly-in" style="left:{x}%; top:{y}%;" data-state="{selected_state}">'
            f'{falcon_svg}</div>'
        )
    else:
        falcon_div = f'<div class="falcon-landed" style="left:50%; top:50%;">{falcon_svg}</div>'
    return f"""
    <div class="map-falcon-wrap gold-border">
        <h3 class="shimmer">Sovereign Resource Map — Nigeria</h3>
        <p class="map-sub">13 Coal-Rich States — Live Pulsing Corridors (click a node)</p>
        <div class="nigeria-map-container">
            {svg}
            {falcon_div}
        </div>
    </div>
    """


# Navy Humanoid: 3D-style avatar + R1–R8 orbiting chest
def _humanoid_html():
    r_orbs = "".join(f'<span class="r-orb">{d}</span>' for d in DETERMINANTS_R)
    return f"""
    <div class="gold-border humanoid-exhibit">
        <p class="shimmer-sub exhibit-label">The Navy Humanoid — Determinant Exhibit</p>
        <div class="determinant-aura-orbit">
            <div class="orbit-ring">
                {r_orbs}
            </div>
            <div class="navy-humanoid-3d">
                <svg viewBox="0 0 80 120" class="humanoid-3d-svg">
                    <defs>
                        <linearGradient id="navy3d" x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" style="stop-color:#0a1628"/>
                            <stop offset="40%" style="stop-color:#0d2137"/>
                            <stop offset="100%" style="stop-color:#001a33"/>
                        </linearGradient>
                        <filter id="depth"><feDropShadow dx="2" dy="2" stdDeviation="1" flood-color="#000"/></filter>
                    </defs>
                    <ellipse cx="40" cy="22" rx="18" ry="20" fill="url(#navy3d)" stroke="#D4AF37" stroke-width="2" filter="url(#depth)"/>
                    <path fill="url(#navy3d)" stroke="#D4AF37" stroke-width="1.5" filter="url(#depth)"
                        d="M28 44 L40 62 L52 44 L48 108 L32 108 Z"/>
                    <rect x="34" y="62" width="12" height="50" rx="3" fill="url(#navy3d)" stroke="#D4AF37" filter="url(#depth)"/>
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
        <p class="legal-line">{TITLE_FULL}</p>
        <p class="copyright-line">© GCSLC. Proprietary. GCSLC Strategic Command.</p>
    </div>
    """


# CSS: Prestige Lock — gold+white shimmer, expandable diamond, falcon fly-in, orbit, watermark, blur
css = """
.gradio-container, .main, .container { background: #000B1E !important; }
@keyframes gold-shimmer {
  0%, 100% { color: #B8860B; text-shadow: 0 0 12px #D4AF37, 0 0 24px rgba(212,175,55,0.5); }
  50% { color: #FFD700; text-shadow: 0 0 20px #FFD700, 0 0 40px rgba(255,255,255,0.4); }
}
@keyframes gold-white-pulse {
  0%, 100% { box-shadow: 0 0 10px rgba(212,175,55,0.6), 0 0 20px rgba(255,255,255,0.2); border-color: #D4AF37; color: #D4AF37; }
  50% { box-shadow: 0 0 18px #FFD700, 0 0 28px rgba(255,255,255,0.5); border-color: #FFE4B5; color: #FFE4B5; }
}
@keyframes diamond-expand {
  from { max-height: 0; opacity: 0; transform: scale(0.95); }
  to { max-height: 420px; opacity: 1; transform: scale(1); }
}
@keyframes falcon-fly-in {
  0% { transform: translate(-50%, -50%) translateY(-200px) scale(0.5); opacity: 0; }
  70% { transform: translate(-50%, -50%) translateY(5px) scale(1.05); opacity: 1; }
  100% { transform: translate(-50%, -50%) translateY(0) scale(1); opacity: 1; }
}
@keyframes orbit {
  from { transform: translate(-50%, -50%) rotate(0deg); }
  to { transform: translate(-50%, -50%) rotate(360deg); }
}
.shimmer { color: #D4AF37; animation: gold-shimmer 2.2s ease-in-out infinite; }
.shimmer-sub { color: #B8860B; }
.gold-border { border: 2px solid #D4AF37; border-radius: 12px; background: linear-gradient(135deg, #001A35 0%, #000B1E 100%); }
h1, h2, h3, h4 { color: #D4AF37 !important; }
p, span, label { color: #e8eef4 !important; }

/* GCSLC PROPRIETARY diagonal watermark + anti-screenshot blur overlay */
.gcslc-watermark {
  position: fixed !important; top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
  pointer-events: none !important; z-index: 99998 !important;
  background: repeating-linear-gradient(-28deg, transparent 0, transparent 68px, rgba(212,175,55,0.045) 68px, rgba(212,175,55,0.045) 136px) !important;
}
.gcslc-watermark::after {
  content: "GCSLC PROPRIETARY" !important; position: absolute !important; top: 50% !important; left: 50% !important;
  transform: translate(-50%, -50%) rotate(-22deg) !important; font-size: clamp(2rem, 4.5vw, 3.8rem) !important;
  font-weight: 700 !important; color: rgba(212,175,55,0.1) !important; letter-spacing: 0.28em !important;
  white-space: nowrap !important;
}
.gcslc-blur-overlay {
  position: fixed !important; top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important;
  pointer-events: none !important; z-index: 99997 !important;
  backdrop-filter: blur(0.8px); -webkit-backdrop-filter: blur(0.8px);
  opacity: 0.15;
}
.gradio-container { user-select: none !important; -webkit-user-select: none !important; }
.gradio-container * { user-select: none !important; -webkit-user-select: none !important; }

.diamond-popup { padding: 16px; margin: 12px 0; overflow: hidden; }
.diamond-popup-expand { animation: diamond-expand 0.5s ease-out forwards; }
.reserves-line, .byproduct-title { margin: 8px 0; color: #e8eef4; }
.byproduct-title { color: #D4AF37; font-weight: 600; margin-top: 12px; }
.byproduct-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 8px; }
.byproduct-item { color: #b8c4ce; font-size: 0.9rem; }

.map-falcon-wrap { padding: 20px; text-align: center; position: relative; }
.map-sub { color: #b8c4ce; font-size: 0.9rem; margin: 8px 0 12px 0; }
.nigeria-map-container { position: relative; display: inline-block; max-width: 320px; margin: 0 auto; }
.nigeria-hv-map { width: 100%; height: auto; display: block; }
.falcon-landed {
  position: absolute; width: 56px; height: 38px; margin-left: -28px; margin-top: -19px;
  transform: translate(-50%, -50%); z-index: 10; pointer-events: none;
}
.falcon-fly-in { animation: falcon-fly-in 0.7s ease-out forwards; }
.falcon-prestige { width: 100%; height: 100%; filter: drop-shadow(0 0 14px rgba(212,175,55,0.8)); }

/* Live Pulsing Corridors: Gold and White shimmer */
.state-node {
  min-width: 100px; animation: gold-white-pulse 2s ease-in-out infinite !important;
  border: 2px solid #D4AF37 !important; color: #D4AF37 !important;
  background: rgba(0,26,53,0.92) !important; font-weight: 600 !important;
}
.state-node:hover { box-shadow: 0 0 22px #FFD700, 0 0 40px rgba(255,255,255,0.35) !important; }

/* 3D Navy Humanoid + orbiting R1–R8 */
.humanoid-exhibit { padding: 24px; text-align: center; }
.exhibit-label { font-size: 0.85rem; margin-bottom: 12px; }
.determinant-aura-orbit { position: relative; width: 280px; height: 280px; margin: 0 auto; }
.orbit-ring {
  position: absolute; left: 50%; top: 50%; width: 200px; height: 200px;
  animation: orbit 24s linear infinite;
  transform-origin: center center;
}
.orbit-ring .r-orb {
  position: absolute; width: 58px; margin-left: -29px; margin-top: -12px;
  padding: 4px 8px; border-radius: 20px; font-size: 0.65rem; font-weight: 600;
  background: rgba(0,26,53,0.95); border: 1px solid #D4AF37; color: #D4AF37; white-space: nowrap;
}
.orbit-ring .r-orb:nth-child(1) { left: 171px; top: 88px; }
.orbit-ring .r-orb:nth-child(2) { left: 142px; top: 159px; }
.orbit-ring .r-orb:nth-child(3) { left: 71px; top: 188px; }
.orbit-ring .r-orb:nth-child(4) { left: 0; top: 159px; }
.orbit-ring .r-orb:nth-child(5) { left: 0; top: 88px; }
.orbit-ring .r-orb:nth-child(6) { left: 71px; top: 0; }
.orbit-ring .r-orb:nth-child(7) { left: 142px; top: 17px; }
.orbit-ring .r-orb:nth-child(8) { left: 171px; top: 17px; }
.navy-humanoid-3d {
  position: absolute; left: 50%; top: 48%; width: 70px; height: 105px;
  transform: translate(-50%, -50%); z-index: 2;
  filter: drop-shadow(4px 4px 8px rgba(0,0,0,0.5)) drop-shadow(0 0 12px rgba(0,43,91,0.8));
}
.humanoid-3d-svg { width: 100%; height: 100%; }
.speech-bubble-wrap { position: absolute; left: 50%; top: 78%; transform: translate(-50%, -50%); width: 90%; z-index: 3; }
.speech-bubble { background: #001A35; border: 2px solid #D4AF37; border-radius: 12px; padding: 10px 14px; margin: 0; font-size: 0.82rem; color: #e8eef4; line-height: 1.35; }

.footer-signature { text-align: center; padding: 20px 16px; margin-top: 24px; border-top: 1px solid rgba(212,175,55,0.35); }
.signature-line { font-size: 0.9rem; margin: 0 0 8px 0; font-weight: 600; }
.cac-line { font-size: 0.85rem; color: #D4AF37; margin: 0 0 4px 0; }
.legal-line { font-size: 0.78rem; color: #b8c4ce; margin: 0 0 4px 0; }
.header-sovereign { position: relative; padding-bottom: 8px; }
.falcon-header-icon { display: block; width: 48px; height: 32px; margin: 4px auto 0; }
.falcon-header-icon svg { width: 100%; height: 100%; filter: drop-shadow(0 0 8px rgba(212,175,55,0.6)); }
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


def _on_state_click(state: str):
    return _diamond_popup_html(state, with_audio=True)


def _on_state_click_map(state: str):
    return _map_with_falcon_html(state)


with gr.Blocks(css=css, title="GCSLC Sovereign Gateway — Prestige Lock") as demo:
    gr.HTML("""
    <div class='gcslc-watermark' aria-hidden='true'></div>
    <div class='gcslc-blur-overlay' aria-hidden='true'></div>
    <script>
    (function(){ function noRightClick(e) { e.preventDefault(); return false; }
      document.addEventListener('contextmenu', noRightClick);
      document.addEventListener('DOMContentLoaded', function() {
        var r = document.querySelector('.gradio-container'); if (r) r.addEventListener('contextmenu', noRightClick);
      });
    })();
    </script>
    """)

    # Sovereign Command header: title (GCSLC - LTD/GTE) + Falcon in header
    gr.HTML(
        "<div class='header-sovereign'>"
        "<h1 class='shimmer' style='text-align: center; font-size: 1.2rem; margin-bottom: 4px;'>"
        "Sovereign Command</h1>"
        "<p class='title-full shimmer-sub' style='text-align: center; font-size: 1rem; margin: 0 0 8px 0;'>"
        + TITLE_FULL +
        "</p>"
        "<div class='falcon-header-icon'>" + _falcon_prestige_svg() + "</div>"
        "</div>"
    )
    gr.HTML(
        f"<p style='text-align: center; font-size: 0.95rem; max-width: 720px; margin: 0 auto 20px auto; line-height: 1.45; color: #e8eef4;'>"
        f"{HOOK_TEXT}</p>"
    )

    # Map: Falcon flies to clicked state (Talon Lock)
    map_out = gr.HTML(value=_map_with_falcon_html("Kogi"), label="Map")
    # Live Pulsing Corridors: 13 state nodes (Gold and White shimmer)
    with gr.Row():
        state_buttons = []
        for s in COAL_STATES:
            btn = gr.Button(s, elem_classes=["state-node"], variant="secondary")
            state_buttons.append((s, btn))
    popup_out = gr.HTML(value=_diamond_popup_html("Kogi", with_audio=False), label="Diamond Opportunity")

    def make_click(state):
        def fn():
            return _diamond_popup_html(state, with_audio=True)
        return fn

    def make_click_map(state):
        def fn():
            return _map_with_falcon_html(state)
        return fn

    for state, btn in state_buttons:
        btn.click(fn=make_click(state), inputs=None, outputs=popup_out)
        btn.click(fn=make_click_map(state), inputs=None, outputs=map_out)

    gr.Markdown("---")
    gr.HTML(_humanoid_html())
    gr.Markdown("---")
    gr.HTML(_footer_html())


if __name__ == "__main__":
    _clear_gradio_cache()
    _kill_port()
    print("\n" + "=" * 60)
    print("  GCSLC Sovereign Gateway — Prestige Lock | http://127.0.0.1:7860")
    print("  Samsung S24 Ultra: use LAN IP or public URL (share=True).")
    print("=" * 60 + "\n")
    sys.stdout.flush()
    demo.launch(share=True, server_name="0.0.0.0", server_port=SERVER_PORT, show_error=True)
