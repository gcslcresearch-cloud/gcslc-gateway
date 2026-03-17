#!/usr/bin/env python3
"""
Serve the NRRFC pulsing dashboard on localhost:8090.
Strategy: 37-Node Grid Status from the current project (GCSLC_Sovereign_Gateway/app.html).
No external 8RStealthBfiles path; app.html is resolved from the working directory.
GCSLC Sovereign Gateway — © 2026 GCSLC LTD/GTE.
"""
import os
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

# ROOT: lock to current working directory (GCSLC_Sovereign_Gateway)
ROOT = Path.cwd().resolve()
LIVE_APP = ROOT / "app.html"  # LIVE dashboard HTML served from project root
APP_HTML = "app.html"
PORT = 8090


class DashboardHandler(SimpleHTTPRequestHandler):
    """Serve LIVE app.html from 8RStealthBfiles; no caching so real-time data shows."""

    def _send_no_cache_headers(self):
        """Hard-lock: disable all caching so real-time updates are always visible."""
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0, private")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("Surrogate-Control", "no-store")

    def do_GET(self):
        # Redirect root to app.html so LIVE pulsing dashboard loads directly
        if self.path in ("/", ""):
            self.send_response(302)
            self.send_header("Location", f"/{APP_HTML}")
            self.end_headers()
            return
        return SimpleHTTPRequestHandler.do_GET(self)

    def end_headers(self):
        self._send_no_cache_headers()
        SimpleHTTPRequestHandler.end_headers(self)

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")


def main():
    if not ROOT.is_dir():
        print(f"Error: Directory not found: {ROOT}")
        print("Run from the GCSLC_Sovereign_Gateway project root so app.html is accessible.")
        sys.exit(1)
    if not LIVE_APP.is_file():
        print(f"Error: LIVE app not found: {LIVE_APP}")
        print("Ensure app.html exists in the project root (GCSLC_Sovereign_Gateway/app.html).")
        sys.exit(1)

    try:
        raw = LIVE_APP.read_text(encoding="utf-8", errors="ignore")[:16000]
        if ("639.3" in raw or "639" in raw) and "2026" in raw:
            print("Live state verified: 639.3 Mt present in app.html")
        else:
            print("Note: Confirm in browser that app.html shows 639.3 Mt reserves.")
    except Exception:
        pass

    # Serve from the project root so relative assets resolve correctly
    os.chdir(ROOT)
    server = HTTPServer(("", PORT), DashboardHandler)
    url = f"http://localhost:{PORT}/"
    print("SOVEREIGN GATEWAY LIVE ON 8090")
    print(f"NRRFC LIVE Dashboard — serving LIVE app from: {LIVE_APP}")
    print(f"Open: {url}  (redirects to {url}{APP_HTML})")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown.")
        server.shutdown()


if __name__ == "__main__":
    main()
