#!/usr/bin/env bash
# Launch Port 8052 — Sovereign Asset Dashboard (12-State Coal and By-products Corridor)
# Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026 GCSLC.
# Run from project root: ./run_coal_corridor_8052.sh
# Does not conflict with Wealth Cloud (8053) or Continental View (8054).

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
fi
exec python -m streamlit run coal_corridor_8052.py --server.port 8052 --server.headless true
