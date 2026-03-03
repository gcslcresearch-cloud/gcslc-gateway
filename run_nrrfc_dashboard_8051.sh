#!/usr/bin/env bash
# GCSLC Sovereign Gateway — Port 8051. Launch nrrfc_dashboard.py (GEC-COAL-BASE-13 nodal).
# Path fix: project is NOT inside a folder with spaces; GEC-COAL-BASE-13 logic lives on Desktop path.
# All "File does not exist: 8R" errors resolved by using space-free path only.
# Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026 GCSLC.
# Run from project root: ./run_nrrfc_dashboard_8051.sh

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
  source ".venv/bin/activate"
fi
# Space-free path only (no manual moving/renaming)
DASHBOARD_SCRIPT="B_Files/nrrfc_dashboard.py"
exec python -m streamlit run "$DASHBOARD_SCRIPT" --server.port 8051 --server.headless true
