#!/usr/bin/env bash
# Sovereign Nodal Mirror Terminal — GCSLC Mirror Vault (port 8056)
# Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026 GCSLC.
# Run from project root. Open http://localhost:8056

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
if [ -d ".venv" ] && [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
fi
exec python -m streamlit run GCSLC_MIRROR_VAULT/sovereign_mirror_terminal.py --server.port 8056 --server.headless true
