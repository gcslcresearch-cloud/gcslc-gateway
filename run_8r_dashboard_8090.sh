#!/usr/bin/env bash
# Serve NRRFC pulsing dashboard (8RStealthBfiles/app.html) on localhost:8090
# Run from project root: ./run_8r_dashboard_8090.sh

set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
python3 serve_8r_dashboard_8090.py
