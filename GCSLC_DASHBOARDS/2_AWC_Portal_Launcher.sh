#!/usr/bin/env bash
# Launch Port 8052 — Sovereign Asset Dashboard (12-State Coal and By-products Corridor)
# Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026 GCSLC.
# Run from project root or from GCSLC_DASHBOARDS: ./2_AWC_Portal_Launcher.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT"
if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
fi
exec python -m streamlit run coal_corridor_8052.py --server.port 8052 --server.headless true
