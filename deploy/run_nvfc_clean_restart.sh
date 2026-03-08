#!/usr/bin/env bash
# Single command: kill port 7860, stop old PM2 app, restart NVFC Gradio, show URLs.
# Run from repo root: ./deploy/run_nvfc_clean_restart.sh

set -e
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

echo "--- Cleaning port 7860 ---"
lsof -ti:7860 | xargs kill -9 2>/dev/null || true
sleep 1

echo "--- Stopping existing PM2 app (if any) ---"
pm2 delete nvfc-gradio 2>/dev/null || true

echo "--- Starting NVFC Gradio via PM2 ---"
pm2 start deploy/ecosystem.config.cjs

echo ""
echo "============================================================"
echo "  NVFC SOVEREIGN DASHBOARD"
echo "============================================================"
echo "  Local URL:   http://127.0.0.1:7860"
echo "  Public URL:  (see below — run: pm2 logs nvfc-gradio)"
echo "============================================================"
echo ""
echo "To see the Public Gradio URL and logs: pm2 logs nvfc-gradio"
echo ""
