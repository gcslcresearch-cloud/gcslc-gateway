#!/usr/bin/env bash
set -u

ROOT="/Users/user/Desktop/GCSLC_Sovereign_Gateway"
LOG_DIR="$ROOT/14314"
URL_FILE="$LOG_DIR/sovereign_urls.env"

SUB_8505="${SOVEREIGN_SUBDOMAIN_8505:-sovereign-exec-8505}"
CONVENER_GATE="${CONVENER_GATE_KEY:-Camen@2027#}"

start_tunnel() {
  local port="$1"
  local subdomain="$2"
  local log_file="$LOG_DIR/.tunnel_${port}.log"
  local pid_file="$LOG_DIR/.tunnel_${port}.pid"

  if [ -f "$pid_file" ] && kill -0 "$(cat "$pid_file")" 2>/dev/null; then
    return 0
  fi

  nohup npx --yes localtunnel --port "$port" --subdomain "$subdomain" >"$log_file" 2>&1 &
  echo "$!" >"$pid_file"
}

start_tunnel 8505 "$SUB_8505"

{
  echo "SOVEREIGN_EXEC_URL=https://${SUB_8505}.loca.lt"
  echo "SOVEREIGN_OPS_URL=LOCAL_ONLY_8506"
  echo "SOVEREIGN_URL=https://${SUB_8505}.loca.lt"
  echo "CONVENER_GATE_KEY=${CONVENER_GATE}"
} > "$URL_FILE"

echo "Sovereign bridge initialized."
echo "Executive URL: https://${SUB_8505}.loca.lt"
echo "Operational URL: LOCAL_ONLY_8506"
