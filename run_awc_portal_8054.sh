#!/usr/bin/env bash
# Launch African Wealth Cloud (AWC) Portal on Port 8054
# Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026 GCSLC.
# Run from project root: ./run_awc_portal_8054.sh

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
fi
exec python -m streamlit run "awc_portal_8054.py" --server.port 8054 --server.headless true
