#!/usr/bin/env bash
# GCSLC Sovereign Gateway — 8R Stealth Paradigm: launch all three dashboards on 8051, 8052, 8053
# Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026 GCSLC.
# Run from project root: ./GCSLC_DASHBOARDS/LAUNCH_ALL.sh
# Or from this folder: ./LAUNCH_ALL.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT"
if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
fi

echo "GCSLC 8R Stealth — Launching dashboards on 8051, 8052, 8053..."
python -m streamlit run "$SCRIPT_DIR/1_NRRFC_9.6x_Multiplier.py" --server.port 8051 --server.headless true &
python -m streamlit run coal_corridor_8052.py --server.port 8052 --server.headless true &
python -m streamlit run "$SCRIPT_DIR/3_AWC_Coal_Diamond.py" --server.port 8053 --server.headless true &
wait
