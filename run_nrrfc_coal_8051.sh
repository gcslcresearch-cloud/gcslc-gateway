#!/usr/bin/env bash
# Launch NRRFC Coal SSMV dashboard on Port 8051 (8R Stealth — GCSLC_DASHBOARDS)
# Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026 GCSLC.
# Run from project root: ./run_nrrfc_coal_8051.sh

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
fi
exec python -m streamlit run GCSLC_DASHBOARDS/1_NRRFC_9.6x_Multiplier.py --server.port 8051 --server.headless true
