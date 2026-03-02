#!/usr/bin/env bash
# Aliyu Riyadh Mirror — Secure Remote Dashboard (AWC & GEC) on Port 8055
# GALADIMAN RUWA CENTER FOR STRATEGIC LEADERSHIP AND COMMUNICATION LTD/GTE — CAC: 176917792057
# Run from project root: ./run_aliyu_riyadh_8055.sh

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
fi
exec python -m streamlit run aliyu_riyadh_access.py --server.port 8055 --server.headless true
