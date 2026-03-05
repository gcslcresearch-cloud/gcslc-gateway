#!/usr/bin/env bash
# Launch Port 8052 — Sovereign Asset Dashboard (delegates to GCSLC_DASHBOARDS)
# Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026 GCSLC.
# Run from project root: ./run_coal_corridor_8052.sh

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
exec "$ROOT/GCSLC_DASHBOARDS/2_AWC_Portal_Launcher.sh"
