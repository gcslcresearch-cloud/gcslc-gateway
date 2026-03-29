"""
GCSLC Sovereign Gateway — Fusion Center.
Native Gradio components with server-driven pulse (.load every=1). No static HTML shell.
"""
# Fix Gradio ImportError: huggingface_hub no longer exposes HfFolder
try:
    import huggingface_hub
    if not hasattr(huggingface_hub, "HfFolder"):
        class HfFolder:
            @staticmethod
            def get_token():
                try:
                    from huggingface_hub import get_token as _get
                    return _get()
                except Exception:
                    return None
            @staticmethod
            def save_token(token):
                try:
                    from huggingface_hub import set_token
                    set_token(token)
                except Exception:
                    pass
        setattr(huggingface_hub, "HfFolder", HfFolder)
except Exception:
    pass

import gradio as gr
import time
import random
from datetime import datetime, timezone

# Baseline data — 640.04 Mt, 1,199 MW, 13 states
BASELINE_RESERVES = 640.04
BASELINE_POWER = 1199
BASELINE_STATES = 13
LEAK_BASE_B = 2.4
LEAK_STEP_B = 0.0001  # $0.0001 B = $100k per 60s — calibrated steady tick
LEAK_INTERVAL_S = 60
START_TIME = time.time()
RESERVES_TABLE = [
    ["Enugu", 167.72, 401, "active"],
    ["Kogi", 141.97, 320, "active"],
    ["Benue", 97.9, 180, "reserve"],
    ["Gombe", 61.99, 110, "reserve"],
    ["Nasarawa", 48.09, 85, "reserve"],
    ["Delta", 38.06, 65, "reserve"],
    ["Imo", 31.91, 55, "reserve"],
    ["Anambra", 27.97, 48, "active"],
    ["Edo", 18.0, 30, "reserve"],
    ["Kebbi", 15.05, 25, "reserve"],
    ["Bauchi", 12.1, 20, "reserve"],
    ["Kwara", 8.03, 12, "reserve"],
    ["Plateau", 5.96, 10, "reserve"],
]
TICKER_MESSAGES = [
    "▶ SOVEREIGN ACTIVE • 640.04 Mt LIVE • 8R PARADIGM ENGAGED",
    "▶ WEALTH LEAK $2.0 B • 13 STATES • 1,199 MW POWER POTENTIAL",
    "▶ NRRFC 2026 • GALADIMAN RUWA • GCSLC FUSION CENTER",
    "▶ NIGERIA COAL RESERVES • REAL-TIME HEARTBEAT • DETERMINANT 8R",
    "▶ SECTOR MORIBUND COST • $2.0 B CUMULATIVE • SOVEREIGN PULSE",
]

def get_utc_time():
    return "**Live UTC:** " + datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

def get_reserves_pulse():
    # Subtle pulse: 640.02–640.06 so the number "breathes"
    return round(BASELINE_RESERVES + random.uniform(-0.02, 0.02), 2)

def get_power_pulse():
    return BASELINE_POWER

def get_states_count():
    return BASELINE_STATES

def get_ticker():
    idx = int(time.time()) % len(TICKER_MESSAGES)
    return "`" + TICKER_MESSAGES[idx] + "`"

def get_reserves_table():
    return RESERVES_TABLE

# Debt-Swap (app.html): 10% Big Tech Capex $700B, Nigeria debt ₦50T, FX 1350
FX_2026 = 1350
DEBT_SWAP_DATA = [
    ["10% Big Tech Capex (A)", "$700.00 B", "₦945.0 T"],
    ["Nigeria domestic debt", "₦50.0 T", "$37.04 B"],
    ["Coverage (10% Capex ÷ debt)", "18.9×", "10% Capex could cover domestic debt"],
]
# Critical Mineral Yield (app.html): 10,000 MT coal baseline
YIELD_TABLE = [
    ["Raw Coal", "10,000 MT", "$110", "$1.1 M", "₦1.49 B"],
    ["Germanium (fly ash)", "800 KG", "$8,597", "$6.9 M", "₦9.28 B"],
    ["Ammonia", "6,000 MT", "$430", "$2.6 M", "₦3.48 B"],
    ["Total Revenue", "—", "—", "$10.6 M", "₦14.25 B"],
]

def get_debt_swap_html():
    return """<div style="background:#0a1225;border:1px solid #D4AF37;border-radius:8px;padding:1rem;margin:1rem 0;">
<h3 style="color:#D4AF37;margin:0 0 0.5rem 0;font-size:1rem;">National debt-swap: 10% Global Big Tech Capex vs Nigeria domestic debt</h3>
<p style="color:#8fa3bf;font-size:0.8rem;margin:0 0 0.75rem 0;">Live 2026 FX: ₦1,350 = $1 USD</p>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;">
<div style="padding:0.75rem;background:rgba(0,0,0,0.2);border-left:3px solid #D4AF37;border-radius:6px;"><div style="font-size:0.75rem;color:#8fa3bf;text-transform:uppercase;">10% Big Tech Capex (A)</div><div style="font-size:1.1rem;font-weight:700;color:#D4AF37;">$700.00 B</div><div style="font-size:0.8rem;color:#8fa3bf;">₦945.0 T</div></div>
<div style="padding:0.75rem;background:rgba(0,0,0,0.2);border-left:3px solid #D4AF37;border-radius:6px;"><div style="font-size:0.75rem;color:#8fa3bf;text-transform:uppercase;">Nigeria domestic debt</div><div style="font-size:1.1rem;font-weight:700;color:#D4AF37;">₦50.0 T</div><div style="font-size:0.8rem;color:#8fa3bf;">$37.04 B</div></div>
<div style="padding:0.75rem;background:rgba(0,0,0,0.2);border-left:3px solid #D4AF37;border-radius:6px;"><div style="font-size:0.75rem;color:#8fa3bf;text-transform:uppercase;">Coverage (10% Capex ÷ debt)</div><div style="font-size:1.1rem;font-weight:700;color:#D4AF37;">18.9×</div><div style="font-size:0.8rem;color:#8fa3bf;">10% Capex could cover domestic debt</div></div>
</div></div>"""

def get_leak_md():
    elapsed = max(0, time.time() - START_TIME)
    steps = int(elapsed // LEAK_INTERVAL_S)
    current_b = LEAK_BASE_B + LEAK_STEP_B * steps
    return f"**Sovereign Wealth Leakage: The Cost of Delay**  \\n# ${current_b:.2f} B  \\n*cumulative loss · sector moribund*"


def get_rhgi_sovereign_header_html() -> str:
    """Prompt 196 — RHGI / DG identity + cyan heart + mandate (Gradio HTML)."""
    return """
    <div class="rhgi-header-196">
      <h1 class="rhgi-brand-h1">Renewed Hope Grassroots Initiatives (RHGI)</h1>
      <p class="rhgi-brand-dg">OFFICE OF THE DG</p>
      <div class="rhgi-cyan-heart" aria-hidden="true"></div>
      <p class="rhgi-mandate-line">Securing the 20.7 Million Votes Mandate</p>
      <p class="rhgi-fusion-sub">GCSLC NRRFC — Nigeria Coal Reserves · 8R Stealth Paradigm</p>
    </div>
    """


# Prompt 196 — Metallic Deep Navy shell + RHGI shimmer + cyan heart + metallic gold mandate
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Goldman:wght@400;700&display=swap');
html, body, #root, [data-testid="gradio-app"], [data-testid="app"] {
    background: linear-gradient(165deg, #000033 0%, #00004d 42%, #000066 100%) !important;
    background-attachment: fixed !important;
    min-height: 100vh;
}
.gradio-container {
    background: linear-gradient(165deg, #000033 0%, #00004d 42%, #000066 100%) !important;
    background-attachment: fixed !important;
}
.main, .container, .wrap, .block { background: transparent !important; color: #f5f0e8 !important; }
.footer-native, .footer-native p { color: #8fa3bf !important; text-align: center; font-size: 0.9rem; margin-top: 1rem; }
label { color: #D4AF37 !important; }
.clock-pulse, .clock-pulse p { color: #D4AF37 !important; font-weight: 600; }
.ticker-box { color: #D4AF37; font-weight: 600; }
input, .number input { background: rgba(0, 10, 40, 0.55) !important; border: 1px solid #D4AF37 !important; color: #e8eef4 !important; }
table, .dataframe { background: rgba(0, 10, 40, 0.45) !important; color: #e8eef4 !important; border: 1px solid #D4AF37 !important; }

@keyframes rhgi-identity-breathe {
    0%, 100% { opacity: 0.88; }
    50% { opacity: 1; }
}
@keyframes rhgi-brand-dg-shimmer {
    0% { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
}
@keyframes rhgi-live-shimmer-gold-pulse {
    0%, 100% { filter: brightness(1.02) drop-shadow(0 0 0.12rem rgba(255, 248, 240, 0.75)) drop-shadow(0 0 0.45rem rgba(255, 215, 0, 0.4)); }
    50% { filter: brightness(1.16) drop-shadow(0 0 0.28rem rgba(255, 255, 255, 0.9)) drop-shadow(0 0 0.75rem rgba(255, 215, 0, 0.65)); }
}
.rhgi-brand-h1 {
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-weight: 700 !important;
    text-align: center !important;
    margin: 0 0 8px 0 !important;
    line-height: 1.25 !important;
    font-size: clamp(1rem, 2.8vw, 1.35rem) !important;
    letter-spacing: 0.04em !important;
    background: linear-gradient(90deg, #f5f0e8 0%, #ffd700 18%, #ffffff 32%, #ffe8b0 48%, #ffd700 62%, #f5f0e8 78%, #ffffff 92%, #f5f0e8 100%) !important;
    background-size: 300% 100% !important;
    -webkit-background-clip: text !important;
    background-clip: text !important;
    color: transparent !important;
    animation: rhgi-brand-dg-shimmer 4.2s linear infinite, rhgi-live-shimmer-gold-pulse 2.4s ease-in-out infinite, rhgi-identity-breathe 3.6s ease-in-out infinite !important;
}
.rhgi-brand-dg {
    font-family: 'Goldman', system-ui, sans-serif !important;
    font-weight: 700 !important;
    text-align: center !important;
    margin: 0 !important;
    font-size: clamp(0.82rem, 2.2vw, 1.05rem) !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    background: linear-gradient(90deg, #f5f0e8 0%, #ffd700 22%, #ffffff 40%, #ffd700 58%, #fdfaf5 76%, #ffd700 90%, #f5f0e8 100%) !important;
    background-size: 300% 100% !important;
    -webkit-background-clip: text !important;
    background-clip: text !important;
    color: transparent !important;
    animation: rhgi-brand-dg-shimmer 4.2s linear infinite, rhgi-live-shimmer-gold-pulse 2.4s ease-in-out infinite, rhgi-identity-breathe 3.6s ease-in-out infinite !important;
}
.rhgi-cyan-heart {
    width: min(100%, 28rem);
    height: 4px;
    margin: 10px auto 12px auto;
    border-radius: 3px;
    background: linear-gradient(90deg, transparent 0%, rgba(0, 206, 209, 0.25) 10%, #00CED1 35%, #7fffd4 50%, #00CED1 65%, rgba(0, 206, 209, 0.35) 90%, transparent 100%);
    background-size: 400% 100%;
    animation: rhgi-cyan-divider-travel 2s linear infinite, rhgi-cyan-divider-glow 1.35s ease-in-out infinite;
}
@keyframes rhgi-cyan-divider-travel {
    0% { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
}
@keyframes rhgi-cyan-divider-glow {
    0%, 100% { filter: brightness(1); box-shadow: 0 0 6px rgba(0, 206, 209, 0.5), 0 0 14px rgba(0, 180, 200, 0.22); }
    35% { filter: brightness(1.35); box-shadow: 0 0 18px rgba(0, 240, 255, 0.85), 0 0 32px rgba(0, 206, 209, 0.5); }
    55% { filter: brightness(0.82); box-shadow: 0 0 5px rgba(0, 206, 209, 0.28); }
    75% { filter: brightness(1.28); box-shadow: 0 0 22px rgba(0, 255, 252, 0.65), 0 0 36px rgba(0, 206, 209, 0.45); }
}
@keyframes rhgi-metallic-gold-pulse {
    0%, 100% { color: #ffd700 !important; text-shadow: 0 0 8px rgba(255, 215, 0, 0.45), 0 0 16px rgba(255, 215, 0, 0.25); filter: brightness(1); }
    50% { color: #fff8dc !important; text-shadow: 0 0 14px rgba(255, 215, 0, 0.85), 0 0 28px rgba(255, 215, 0, 0.45); filter: brightness(1.12); }
}
.rhgi-mandate-line {
    font-family: 'Goldman', system-ui, sans-serif !important;
    text-align: center !important;
    font-weight: 700 !important;
    font-size: clamp(0.88rem, 2.2vw, 1.05rem) !important;
    margin: 6px auto 10px auto !important;
    max-width: 720px !important;
    line-height: 1.4 !important;
    color: #ffd700 !important;
    animation: rhgi-metallic-gold-pulse 2.2s ease-in-out infinite !important;
}
.rhgi-fusion-sub {
    font-family: 'Goldman', system-ui, sans-serif !important;
    text-align: center !important;
    font-size: clamp(0.78rem, 1.8vw, 0.92rem) !important;
    color: rgba(212, 175, 55, 0.85) !important;
    margin: 0 0 4px 0 !important;
    letter-spacing: 0.04em !important;
}
.rhgi-header-196 { padding: 4px 0 12px 0; }
"""

with gr.Blocks(css=CSS, title="GCSLC NRRFC Fusion Center") as demo:
    gr.HTML(value=get_rhgi_sovereign_header_html())

    clock_md = gr.Markdown(value=get_utc_time(), elem_classes=["clock-pulse"])
    ticker_md = gr.Markdown(value=get_ticker(), elem_classes=["ticker-box"])

    with gr.Row():
        reserves_num = gr.Number(label="Total proven reserves (Mt)", value=BASELINE_RESERVES, precision=2)
        power_num = gr.Number(label="Power potential (MW)", value=BASELINE_POWER, precision=0)
        states_num = gr.Number(label="States with reserves", value=BASELINE_STATES, precision=0)

    reserves_df = gr.Dataframe(
        value=RESERVES_TABLE,
        headers=["State", "Reserves (Mt)", "Power (MW)", "Status"],
        label="Reserves by state",
        interactive=False,
    )
    debt_swap_html = gr.HTML(value=get_debt_swap_html())
    gr.Markdown("**Critical Mineral Yield**  \n*Total Revenue = (Raw Coal MT × $110) + (Germanium KG × $8,597) + (Ammonia MT × $430)*")
    yield_df = gr.Dataframe(
        value=YIELD_TABLE,
        headers=["Component", "Quantity", "Price", "Revenue (USD)", "Revenue (₦)"],
        label="Yield table (10,000 MT coal)",
        interactive=False,
    )
    leak_md = gr.Markdown(value=get_leak_md())
    gr.Markdown("*Galadiman Ruwa Center (GCSLC) · NRRFC 2026*", elem_classes=["footer-native"])

    # Heartbeat — .load(every=1) where needed; calibrated math for leakage & reserves
    demo.load(get_utc_time, None, clock_md, every=1)
    demo.load(get_ticker, None, ticker_md, every=1)
    demo.load(get_reserves_pulse, None, reserves_num, every=2)
    demo.load(get_power_pulse, None, power_num, every=2)
    demo.load(get_states_count, None, states_num, every=2)
    demo.load(get_reserves_table, None, reserves_df, every=1)
    demo.load(get_debt_swap_html, None, debt_swap_html, every=1)
    demo.load(get_leak_md, None, leak_md, every=60)

if __name__ == "__main__":
    demo.launch(server_port=8505, inline=False)
