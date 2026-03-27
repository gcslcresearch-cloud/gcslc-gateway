#!/usr/bin/env bash
# Run when Streamlit is already listening on 8505. Prints a public loca.lt (or similar) URL.
set -euo pipefail
cd "$(dirname "$0")/.."
exec npx --yes localtunnel --port 8505
