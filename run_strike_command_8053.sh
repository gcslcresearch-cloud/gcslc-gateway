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
exec python -m streamlit run GCSLC_DASHBOARDS/3_AWC_Coal_Diamond.py --server.port 8053 --server.headless true
