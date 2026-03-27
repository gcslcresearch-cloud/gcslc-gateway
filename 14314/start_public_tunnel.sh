#!/usr/bin/env bash
# SSMI-COMMAND-PALETTE-FINAL-126 — Streamlit on 8505 + persistent localtunnel bridge.
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
npx --yes localtunnel --port 8505 2>&1 | while IFS= read -r line; do
  printf '%s\n' "$line"
  case "$line" in
    *".loca.lt"*|*"localtunnel.me"*)
      printf 'PUBLIC URL: %s\n' "$line"
      ;;
  esac
done
