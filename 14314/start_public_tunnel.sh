#!/usr/bin/env bash
# SSMI-ACCESS-RESTORE-122 — Streamlit on 8505 + npx localtunnel (public .loca.lt URL for S24 / remote).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

while IFS= read -r pid; do
  [ -n "${pid}" ] && kill -9 "${pid}" 2>/dev/null || true
done < <(lsof -ti:8505,8506 2>/dev/null || true)

if command -v streamlit >/dev/null 2>&1; then
  streamlit run 14314/app.py --server.port 8505 &
else
  python3 -m streamlit run 14314/app.py --server.port 8505 &
fi

sleep 3
exec npx --yes localtunnel --port 8505
