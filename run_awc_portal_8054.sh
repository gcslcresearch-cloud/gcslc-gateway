#!/usr/bin/env bash
# Launch African Wealth Cloud (AWC) Portal on port 8054
# Galadiman Ruwa Center (GCSLC) LTD/GTE — © 2026 GCSLC.

set -e
cd "$(dirname "$0")"
exec python -m streamlit run awc_portal_8054.py --server.port 8054 --server.headless true
