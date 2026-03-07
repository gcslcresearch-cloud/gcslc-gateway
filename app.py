"""
GCSLC Sovereign Gateway — Streamlit Cloud entry point.
Uses absolute, Linux-compatible paths for index.html. Passes HTML string to components.html (never a path).
© 2026 GCSLC LTD/GTE.
"""
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

# Linux/Streamlit Cloud: resolve script dir once (absolute path, no reliance on cwd)
_BASE_DIR = Path(__file__).resolve().parent
_INDEX_HTML = _BASE_DIR / "index.html"

st.set_page_config(page_title="GCSLC Sovereign Gateway", layout="wide")

# Load HTML content: use file if present, else inline fallback (avoids white screen / raw JS)
def _get_html():
    if _INDEX_HTML.is_file():
        with open(_INDEX_HTML, "r", encoding="utf-8") as f:
            return f.read()
    # Fallback when index.html is missing (e.g. first deploy): full inline HTML so iframe renders
    return """
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"/><style>body{background:#000814;color:#D4AF37;font-family:system-ui,sans-serif;margin:2rem;}</style></head>
<body>
<h1>GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION</h1>
<p>GCSLC Sovereign Gateway — Dashboard.</p>
<p>Place <code>index.html</code> in the same folder as <code>app.py</code> to load your custom UI.</p>
</body>
</html>
"""

html_content = _get_html()
components.html(html_content, height=800, scrolling=True)
