#!/usr/bin/env bash
# March Automations: run, test, manifest NVFC-COMMAND. No manual risk. Sovereign Victory only.
# Run from repo root: ./deploy/run_march_automations.sh

set -e
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"
VENV_PYTHON="${REPO_ROOT}/.venv/bin/python"

echo "--- March Automations: Validate build ---"
"$VENV_PYTHON" -c "from nvfc_gradio import demo; print('Build OK')"
echo "--- Restart NVFC-COMMAND ---"
if pm2 describe NVFC-COMMAND &>/dev/null; then
  pm2 restart NVFC-COMMAND && pm2 save 2>/dev/null || true
else
  pm2 start deploy/ecosystem.config.cjs && pm2 save 2>/dev/null || true
fi
echo "--- March Automations complete. Sovereign Victory."
