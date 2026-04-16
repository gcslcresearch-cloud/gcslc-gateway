#!/usr/bin/env python3
"""GCSLC Command Central — serves index.html + GeoJSON from this script's directory (port 5050)."""

from __future__ import annotations

import json
import threading
import time
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Final

_BASE: Final[Path] = Path(__file__).resolve().parent
INDEX_HTML: Final[Path] = _BASE / "index.html"
GEOJSON: Final[Path] = _BASE / "nigeria-states.geojson"
INTERFACE_HTML: Final[Path] = _BASE / "interface.html"
FORENSIC_JSON: Final[Path] = _BASE / "forensic_intel.json"
PORT: Final[int] = 5050


def _read_bytes(path: Path) -> bytes:
    return path.read_bytes()


class CommandHandler(BaseHTTPRequestHandler):
    server_version = "GCSLCCommandNode/5050"

    def do_GET(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0].rstrip("/") or "/"

        if path in ("/", "/index.html"):
            if not INDEX_HTML.is_file():
                self.send_error(HTTPStatus.NOT_FOUND, f"Missing: {INDEX_HTML}")
                return
            self._send(INDEX_HTML, "text/html; charset=utf-8")
            return

        if path == "/interface.html":
            if INTERFACE_HTML.is_file():
                self._send(INTERFACE_HTML, "text/html; charset=utf-8")
            else:
                self._send(INDEX_HTML, "text/html; charset=utf-8")
            return

        if path == "/nigeria-states.geojson":
            if not GEOJSON.is_file():
                self.send_error(HTTPStatus.NOT_FOUND, f"Missing: {GEOJSON}")
                return
            self._send(GEOJSON, "application/geo+json; charset=utf-8")
            return

        if path == "/forensic_intel.json":
            if not FORENSIC_JSON.is_file():
                self.send_error(HTTPStatus.NOT_FOUND, f"Missing: {FORENSIC_JSON}")
                return
            self._send(FORENSIC_JSON, "application/json; charset=utf-8")
            return

        if path == "/health":
            body = json.dumps(
                {
                    "status": "ok",
                    "port": PORT,
                    "index_served": str(INDEX_HTML),
                    "deployment": "SOVEREIGN_DATA_INTEGRATION_V9",
                }
            ).encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def log_message(self, fmt: str, *args: object) -> None:
        print("[5050]", fmt % args)

    def _send(self, file_path: Path, content_type: str) -> None:
        data = _read_bytes(file_path)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.end_headers()
        self.wfile.write(data)


def _open_browser() -> None:
    time.sleep(0.35)
    webbrowser.open(f"http://localhost:5050/?v9data={int(time.time())}")


def main() -> None:
    if not INDEX_HTML.is_file():
        raise FileNotFoundError(str(INDEX_HTML))
    print(f"FILE SIZE VERIFIED: {INDEX_HTML.stat().st_size}", flush=True)
    print("COMMAND CENTRAL 5050: SOVEREIGN_DATA_INTEGRATION_V9 READY", flush=True)
    print(f"SERVED FROM: {_BASE}", flush=True)

    server = ThreadingHTTPServer(("0.0.0.0", PORT), CommandHandler)
    threading.Thread(target=_open_browser, daemon=True).start()
    print(
        "GRASSROOTS: 8,806 wards (1:14) / 176,000 PU + AZK pulse corridor LIVE",
        flush=True,
    )
    print(f"Serving http://127.0.0.1:{PORT}/  (index: {INDEX_HTML})", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
