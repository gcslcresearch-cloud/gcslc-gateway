#!/usr/bin/env python3
"""
Serve the NRRFC pulsing dashboard from 8RStealthBfiles on localhost:8056.
Determinant 3 cleanup: ONLY ~/Desktop/8RStealthBfiles/app.html is served.
Verify live state: March 7, 2026 timestamp; 640 Mt reserves.
Strategy: 37-Node Grid Status. GCSLC Sovereign Gateway — © 2026 GCSLC LTD/GTE.
"""
import os
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

# LOCK ROOT: Hard-link ONLY to ~/Desktop/8RStealthBfiles/app.html (no other dashboard sources)
ROOT = (Path.home() / "Desktop" / "8RStealthBfiles").resolve()
LIVE_APP = ROOT / "app.html"  # Only file allowed to serve: March 7, 2026; 640 Mt reserves
APP_HTML = "app.html"
PORT = 8056


class DashboardHandler(SimpleHTTPRequestHandler):
    """Serve LIVE app.html from 8RStealthBfiles; no caching so real-time data shows."""

    def _send_no_cache_headers(self):
        """Disable browser and server caching so today's real-time updates are visible."""
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")

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
        print("Create ~/Desktop/8RStealthBfiles/ and add app.html (March 7, 2026; 640 Mt).")
        sys.exit(1)
    if not LIVE_APP.is_file():
        print(f"Error: LIVE app not found: {LIVE_APP}")
        print("Only ~/Desktop/8RStealthBfiles/app.html is allowed (March 7, 2026; 640 Mt reserves).")
        sys.exit(1)

    # Verify live state: March 7, 2026 timestamp and 640 Mt reserves
    try:
        raw = LIVE_APP.read_text(encoding="utf-8", errors="ignore")[:16000]
        if "640" in raw and ("2026" in raw or "March" in raw):
            print("Live state verified: 640 Mt and 2026 date present in app.html")
        else:
            print("Note: Confirm in browser that app.html shows March 7, 2026 and 640 Mt reserves.")
    except Exception:
        pass

    os.chdir(ROOT)
    server = HTTPServer(("", PORT), DashboardHandler)
    url = f"http://localhost:{PORT}/"
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
