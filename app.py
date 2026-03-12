"""
GCSLC Sovereign Gateway — March 12 Monolithic Deployment.
Self-contained Gradio app. FINAL_UI only. No external assets.
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

FINAL_UI = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>GCSLC NRRFC — Sovereign Dashboard</title>
  <style>
    :root, body, .gradio-container { background: #050a15 !important; }
    * { box-sizing: border-box; }
    body { margin: 0; padding: 0; color: #e8eef4; font-family: system-ui, sans-serif; min-height: 100vh; }
    .wrap { max-width: 900px; margin: 0 auto; padding: 2rem; }
    h1 { color: #D4AF37; font-size: 1.5rem; margin-bottom: 0.5rem; }
    .sub { color: #8fa3bf; font-size: 0.9rem; margin-bottom: 1.5rem; }
    .clock { color: #D4AF37; font-size: 1.1rem; font-weight: 600; margin-bottom: 1.5rem; }
    .kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }
    .kpi { background: #0a1225; border: 1px solid #D4AF37; border-radius: 8px; padding: 1rem; }
    .kpi .label { color: #8fa3bf; font-size: 0.75rem; text-transform: uppercase; }
    .kpi .value { color: #D4AF37; font-size: 1.25rem; font-weight: 700; margin-top: 0.25rem; }
    .leak { background: rgba(229,62,62,0.15); border-left: 4px solid #e53e3e; padding: 1rem; border-radius: 8px; margin-top: 1rem; }
    .leak .val { font-size: 1.5rem; font-weight: 800; color: #e53e3e; }
    .footer { margin-top: 2rem; padding-top: 1rem; border-top: 1px solid rgba(212,175,55,0.3); color: #8fa3bf; font-size: 0.8rem; }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>GCSLC NRRFC — Nigeria Coal Reserves Dashboard</h1>
    <p class="sub">National Resources Revitalization Fusion Center · 8R Stealth Paradigm</p>
    <p class="clock">UTC: <span id="clock">—</span></p>
    <div class="kpis">
      <div class="kpi"><div class="label">Total proven reserves</div><div class="value">640.04</div><span class="unit">Mt</span></div>
      <div class="kpi"><div class="label">Power potential</div><div class="value">1,199</div><span class="unit">MW</span></div>
      <div class="kpi"><div class="label">States with reserves</div><div class="value">13</div><span class="unit">regions</span></div>
    </div>
    <div class="leak">
      <div class="label">Sovereign Wealth Leakage: The Cost of Delay</div>
      <div class="val">$2.0 B</div>
      <div class="sub">cumulative loss · sector moribund</div>
    </div>
    <p class="footer">Galadiman Ruwa Center (GCSLC) · NRRFC 2026</p>
  </div>
  <script>
    (function() {
      var el = document.getElementById('clock');
      if (el) {
        function tick() { el.innerText = new Date().toLocaleString(); }
        tick();
        setInterval(tick, 1000);
      }
    })();
  </script>
</body>
</html>
"""

with gr.Blocks(
    css=":root, body, .gradio-container { background: #050a15 !important; }",
    title="GCSLC NRRFC Fusion Center",
) as demo:
    gr.HTML(FINAL_UI)

if __name__ == "__main__":
    try:
        demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
    except OSError:
        demo.launch(server_name="0.0.0.0", server_port=0, share=False)
