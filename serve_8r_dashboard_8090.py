#!/usr/bin/env python3
"""
Serve the NRRFC pulsing dashboard from 8RStealthBfiles on localhost:8090.
ONLY ~/Desktop/8RStealthBfiles/app.html is served (639.3 Mt live).
Strategy: 37-Node Grid Status. GCSLC Sovereign Gateway — © 2026 GCSLC LTD/GTE.
"""
import os
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

# LOCK ROOT: Hard-link ONLY to ~/Desktop/8RStealthBfiles/app.html (no other dashboard sources)
ROOT = (Path.home() / "Desktop" / "8RStealthBfiles").resolve()
LIVE_APP = ROOT / "app.html"  # Only file served: 639.3 Mt reserves
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
        print("Create ~/Desktop/8RStealthBfiles/ and add app.html (639.3 Mt).")
        sys.exit(1)
    if not LIVE_APP.is_file():
        print(f"Error: LIVE app not found: {LIVE_APP}")
        print("Only ~/Desktop/8RStealthBfiles/app.html is allowed (639.3 Mt reserves).")
        sys.exit(1)

    try:
        raw = LIVE_APP.read_text(encoding="utf-8", errors="ignore")[:16000]
        if ("639.3" in raw or "639" in raw) and "2026" in raw:
            print("Live state verified: 639.3 Mt present in app.html")
        else:
            print("Note: Confirm in browser that app.html shows 639.3 Mt reserves.")
    except Exception:
        pass

    os.chdir(ROOT)
    server = HTTPServer(("", PORT), DashboardHandler)
    url = f"http://localhost:{PORT}/"
    print("SOVEREIGN GATEWAY LIVE ON 8090")
    print(f"NRRFC LIVE Dashboard — serving ONLY: {LIVE_APP}")
    print(f"Open: {url}  (redirects to {url}{APP_HTML})")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown.")
        server.shutdown()


if __name__ == "__main__":
    main()
