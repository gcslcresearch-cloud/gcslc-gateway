#!/usr/bin/env bash
# Single command: kill port 7860 and any nvfc_gradio process, stop PM2 app, restart, save.
# Run from repo root: ./deploy/run_nvfc_clean_restart.sh

set -e
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

echo "--- Killing anything on port 7860 and any nvfc_gradio.py process ---"
pkill -9 -f "nvfc_gradio.py" 2>/dev/null || true
lsof -ti:7860 | xargs kill -9 2>/dev/null || true
sleep 3

echo "--- Stopping PM2 app(s) (if any) ---"
pm2 delete NVFC-COMMAND 2>/dev/null || true
pm2 delete nvfc-gradio 2>/dev/null || true
sleep 1

echo "--- Starting NVFC Gradio via PM2 (using .venv) ---"
pm2 start deploy/ecosystem.config.cjs
pm2 save

echo ""
echo "============================================================"
echo "  NVFC SOVEREIGN DASHBOARD (NVFC-COMMAND)"
echo "============================================================"
echo "  Local URL:   http://127.0.0.1:7860"
echo "  Public URL:  Run: pm2 logs NVFC-COMMAND  (look for 'Running on public URL')"
echo "============================================================"
echo ""
