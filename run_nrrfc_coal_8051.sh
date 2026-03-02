#!/usr/bin/env bash
# Launch NRRFC Coal SSMV dashboard on Port 8051
# Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026 GCSLC.
# Run from project root: ./run_nrrfc_coal_8051.sh

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
fi
exec python -m streamlit run nrrfc_coal_8051.py --server.port 8051 --server.headless true
