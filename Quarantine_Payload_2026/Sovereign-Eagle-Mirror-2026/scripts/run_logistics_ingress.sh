#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ -z "${GCSLC_INGRESS_SECRET:-}" ]]; then
  echo "error: export GCSLC_INGRESS_SECRET before starting gantry ingress" >&2
  exit 1
fi
PORT="${PORT:-8787}"
exec uvicorn logistics_ingress_server:app --host 0.0.0.0 --port "$PORT"
