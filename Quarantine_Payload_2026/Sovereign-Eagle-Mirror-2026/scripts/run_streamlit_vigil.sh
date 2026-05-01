#!/usr/bin/env bash
# Sovereign Eagle Mirror — persistent vigil launcher.
# Always runs from the mirror root so local imports (atomic_spie, gcslc_deep_join, …) resolve.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MIRROR_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$MIRROR_ROOT/../.." && pwd)"
STREAMLIT="${STREAMLIT_BIN:-$REPO_ROOT/.venv/bin/streamlit}"
PORT="${STREAMLIT_PORT:-8501}"
LOG_DIR="$MIRROR_ROOT/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/streamlit_vigil.log"
PID_FILE="$LOG_DIR/streamlit_vigil.pid"

cd "$MIRROR_ROOT"

if lsof -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  if [[ "${VIGIL_REPLACE:-}" != "1" ]]; then
    echo "Port ${PORT} is already in use. Refusing to stack vigils." >&2
    echo "Stop the listener or re-run with: VIGIL_REPLACE=1 $0" >&2
    exit 1
  fi
  echo "VIGIL_REPLACE=1 — releasing port ${PORT}…" >&2
  lsof -tiTCP:"$PORT" -sTCP:LISTEN | xargs kill -9 2>/dev/null || true
  sleep 1
fi

ARGS=(
  run app.py
  --server.address 0.0.0.0
  --server.port "$PORT"
  --browser.gatherUsageStats false
)

if [[ "${VIGIL_FOREGROUND:-}" == "1" ]]; then
  exec "$STREAMLIT" "${ARGS[@]}" "$@"
fi

nohup "$STREAMLIT" "${ARGS[@]}" "$@" >>"$LOG_FILE" 2>&1 &
echo $! >"$PID_FILE"
echo "Vigil started PID $(cat "$PID_FILE") · log $LOG_FILE · LAN http://0.0.0.0:${PORT}"
