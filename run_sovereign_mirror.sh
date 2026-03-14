#!/usr/bin/env bash
# Sovereign Mirror — Digital Doorstep (GCSLC)
# Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026 GCSLC.
# Run from project root: ./run_sovereign_mirror.sh
# Then open http://localhost:8055 — decode: 8R-DECODE-2026 → K-GEC Terminal (8054)

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
fi
exec python -m streamlit run sovereign_mirror.py --server.port 8055 --server.headless true
