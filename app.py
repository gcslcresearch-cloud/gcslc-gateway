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
    return round(BASELINE_RESERVES + (random.random() * 0.04 - 0.02), 2)

def get_power_pulse():
    return BASELINE_POWER

def get_states_count():
    return BASELINE_STATES

def get_ticker():
    idx = int(time.time()) % len(TICKER_MESSAGES)
    return "`" + TICKER_MESSAGES[idx] + "`"

def get_reserves_table():
    return RESERVES_TABLE

def get_leak_md():
    return "**Sovereign Wealth Leakage: The Cost of Delay**  \n# $2.0 B  \n*cumulative loss · sector moribund*"

CSS = (
    ":root, body, .gradio-container { background: #050a15 !important; } "
    ".block, .wrap { background: transparent !important; } "
    ".header-native, .header-native p { color: #D4AF37 !important; text-align: center; } "
    ".footer-native, .footer-native p { color: #8fa3bf !important; text-align: center; font-size: 0.9rem; margin-top: 1rem; } "
    "label { color: #D4AF37 !important; } "
    ".clock-pulse, .clock-pulse p { color: #D4AF37 !important; font-weight: 600; } "
    ".ticker-box { color: #D4AF37; font-weight: 600; } "
    "input, .number input { background: #0a1225 !important; border: 1px solid #D4AF37 !important; color: #e8eef4 !important; } "
    "table, .dataframe { background: #0a1225 !important; color: #e8eef4 !important; border: 1px solid #D4AF37 !important; } "
)

with gr.Blocks(css=CSS, title="GCSLC NRRFC Fusion Center") as demo:
    gr.Markdown("## GCSLC NRRFC — Nigeria Coal Reserves  \n*National Resources Revitalization Fusion Center · 8R Stealth Paradigm*", elem_classes=["header-native"])

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
    leak_md = gr.Markdown(value=get_leak_md())
    gr.Markdown("*Galadiman Ruwa Center (GCSLC) · NRRFC 2026*", elem_classes=["footer-native"])

    # Server heartbeat — every 1 second, bypasses browser
    demo.load(get_utc_time, None, clock_md, every=1)
    demo.load(get_ticker, None, ticker_md, every=1)
    demo.load(get_reserves_pulse, None, reserves_num, every=1)
    demo.load(get_power_pulse, None, power_num, every=1)
    demo.load(get_states_count, None, states_num, every=1)
    demo.load(get_reserves_table, None, reserves_df, every=1)
    demo.load(get_leak_md, None, leak_md, every=1)

if __name__ == "__main__":
    try:
        demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
    except OSError:
        demo.launch(server_name="0.0.0.0", server_port=0, share=False)
