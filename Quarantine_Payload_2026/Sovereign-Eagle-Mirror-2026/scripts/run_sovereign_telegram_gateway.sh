#!/usr/bin/env bash
# Sovereign Telegram webhook gateway — enqueue only; Mirror applies via SQLite poll.
# Requires: TELEGRAM_BOT_TOKEN, TELEGRAM_WEBHOOK_SECRET (recommended), GCSLC_BRIDGE_SQLITE (optional)
set -euo pipefail
cd "$(dirname "$0")/.."
exec uvicorn sovereign_bridge.telegram_gateway:app --host 0.0.0.0 --port "${PORT:-8790}"
