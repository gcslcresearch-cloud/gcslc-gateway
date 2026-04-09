#!/usr/bin/env bash
set -u

ROOT="/Users/user/Desktop/GCSLC_Sovereign_Gateway"
APP_8505="$ROOT/14314/app.py"
APP_8506="$ROOT/14314/ops_app.py"
BRIDGE_SCRIPT="$ROOT/14314/sovereign_bridge.sh"
STATE_FILE="$ROOT/14314/presidential_terminal_8505_PURE.state"

start_if_down() {
  local port="$1"
  local app="$2"
  if ! lsof -iTCP:"$port" -sTCP:LISTEN -n -P >/dev/null 2>&1; then
    nohup python3 -m streamlit run "$app" --server.port "$port" --server.address 0.0.0.0 \
      > "$ROOT/14314/.streamlit_${port}.log" 2>&1 &
  fi
}

refresh_state() {
  {
    echo "alias=presidential_terminal_8505_PURE"
    echo "timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    if lsof -iTCP:8505 -sTCP:LISTEN -n -P >/dev/null 2>&1; then
      echo "port_8505=up"
    else
      echo "port_8505=down"
    fi
    if lsof -iTCP:8506 -sTCP:LISTEN -n -P >/dev/null 2>&1; then
      echo "port_8506=up"
    else
      echo "port_8506=down"
    fi
    if [ -f "$ROOT/14314/sovereign_urls.env" ]; then
      sed -n '1,40p' "$ROOT/14314/sovereign_urls.env"
    fi
  } > "$STATE_FILE"
}

echo "presidential_terminal_8505_PURE watchdog active (ports 8505/8506; tunnel 8505 only)."
while true; do
  start_if_down 8505 "$APP_8505"
  start_if_down 8506 "$APP_8506"
  bash "$BRIDGE_SCRIPT" >/dev/null 2>&1 || true
  refresh_state
  sleep 8
done
