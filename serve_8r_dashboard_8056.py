#!/usr/bin/env python3
"""
Serve the NRRFC pulsing dashboard from 8RStealthBfiles on localhost:8056.
Opens app.html by default so the real-time pulsing effect is active.
Strategy: 37-Node Grid Status. GCSLC Sovereign Gateway — © 2026 GCSLC LTD/GTE.
"""
import os
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

# ROOT: ~/Desktop/8RStealthBfiles/ — serves app.html on port 8056
ROOT = Path.home() / "Desktop" / "8RStealthBfiles"
APP_HTML = "app.html"
PORT = 8056


class DashboardHandler(SimpleHTTPRequestHandler):
    """Serve from 8RStealthBfiles and redirect / to app.html."""

    def do_GET(self):
        # Redirect root to app.html so pulsing dashboard loads directly
        if self.path in ("/", ""):
            self.send_response(302)
            self.send_header("Location", f"/{APP_HTML}")
            self.end_headers()
            return
        return SimpleHTTPRequestHandler.do_GET(self)

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")


def main():
    if not ROOT.is_dir():
        print(f"Error: Directory not found: {ROOT}")
        print("Create the folder and add app.html, then run this script again.")
        sys.exit(1)
    if not (ROOT / APP_HTML).is_file():
        print(f"Warning: {APP_HTML} not found in {ROOT}")

    os.chdir(ROOT)
    server = HTTPServer(("", PORT), DashboardHandler)
    url = f"http://localhost:{PORT}/"
    print(f"NRRFC Pulsing Dashboard — serving {ROOT}")
    print(f"Open: {url}  (redirects to {url}{APP_HTML})")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutdown.")
        server.shutdown()


if __name__ == "__main__":
    main()
