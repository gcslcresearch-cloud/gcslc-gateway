#!/usr/bin/env bash
# Launch 8R Strike Command on Port 8053 (8R Stealth — GCSLC_DASHBOARDS)
# Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026 GCSLC.
# Run from project root: ./run_strike_command_8053.sh

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
fi
# PRESIDENTIAL_STRIKE_V1_RESTORE: Port 8053 serves command_center.py (NWC/C&D logic)
exec python -m streamlit run command_center.py --server.port 8053 --server.headless true
