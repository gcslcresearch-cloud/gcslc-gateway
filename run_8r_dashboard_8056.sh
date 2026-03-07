#!/usr/bin/env bash
# Serve NRRFC pulsing dashboard (8RStealthFiles/app.html) on localhost:8056
# Run from project root: ./run_8r_dashboard_8056.sh

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
python3 serve_8r_dashboard_8056.py
