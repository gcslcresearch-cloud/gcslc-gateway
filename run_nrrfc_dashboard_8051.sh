#!/usr/bin/env bash
# GCSLC Sovereign Gateway — Port 8051. Launch nrrfc_dashboard.py (GEC nodal).
# Path fix: use double-quote syntax so the terminal reads the path as a single address even with spaces.
# File is inside "8R Stealth B_files" folder on the desktop. No manual renames required.
# Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026 GCSLC.
# Run from project root: ./run_nrrfc_dashboard_8051.sh

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
  source ".venv/bin/activate"
fi
# Double-quoted path: forces shell to treat "8R Stealth B_files/..." as one argument (resolves "File does not exist: 8R")
DASHBOARD_SCRIPT="8R Stealth B_files/nrrfc_dashboard.py"
if [ ! -f "$DASHBOARD_SCRIPT" ]; then
  DASHBOARD_SCRIPT="B_Files/nrrfc_dashboard.py"
fi
exec python -m streamlit run "$DASHBOARD_SCRIPT" --server.port 8051 --server.headless true
