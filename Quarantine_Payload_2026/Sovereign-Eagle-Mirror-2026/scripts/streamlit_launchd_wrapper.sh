#!/usr/bin/env bash
# LaunchAgent entry — cd guard + venv streamlit (matches vigil semantics).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPO="$(cd "$ROOT/../.." && pwd)"
exec "$REPO/.venv/bin/streamlit" run "$ROOT/app.py" \
  --server.address 0.0.0.0 \
  --server.port 8501 \
  --browser.gatherUsageStats false
