#!/usr/bin/env python3
"""
GCSLC Mock Termii — local handshake receiver for SOVEREIGN_ASSET_LOCK simulation.
Run: python3 termii_mock_server.py
Then open index.html and click: TEST_HANDSHAKE: GCSLC -> TERMII (SIMULATED)
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("[mock-termii]", self.address_string(), fmt % args)

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        n = int(self.headers.get("Content-Length", "0") or 0)
        raw = self.rfile.read(n).decode("utf-8", "replace")
        try:
            body = json.loads(raw) if raw.strip() else {}
        except json.JSONDecodeError:
            body = {"_raw": raw}
        print("INBOUND PAYLOAD:", json.dumps(body, indent=2)[:4000])
        out = {
            "code": "ok",
            "message": "Mock Termii accepted — Eagle handshake ready",
            "mock": True,
            "echo": body,
        }
        payload = json.dumps(out).encode("utf-8")
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    host, port = "127.0.0.1", 8787
    print(f"Mock Termii listening on http://{host}:{port}/api/sms/send")
    HTTPServer((host, port), Handler).serve_forever()
