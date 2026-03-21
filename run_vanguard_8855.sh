#!/usr/bin/env bash
# NVFC–NRRFC Integrated Vanguard Dashboard — Node 8855
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
exec python -m streamlit run nvfc_nrrfc_vanguard_8855.py --server.port 8855 --server.headless true
