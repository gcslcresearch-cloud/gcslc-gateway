#!/usr/bin/env bash
set -u

ROOT="/Users/user/Desktop/GCSLC_Sovereign_Gateway"
LOG_DIR="$ROOT/14314"
URL_FILE="$LOG_DIR/sovereign_urls.env"

SUB_8505="${SOVEREIGN_SUBDOMAIN_8505:-sovereign-exec-8505}"
SUB_8506="${SOVEREIGN_SUBDOMAIN_8506:-sovereign-ops-8506}"

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
start_tunnel 8506 "$SUB_8506"

{
  echo "SOVEREIGN_EXEC_URL=https://${SUB_8505}.loca.lt"
  echo "SOVEREIGN_OPS_URL=https://${SUB_8506}.loca.lt"
  echo "SOVEREIGN_URL=https://${SUB_8505}.loca.lt"
} > "$URL_FILE"

echo "Sovereign bridge initialized."
echo "Executive URL: https://${SUB_8505}.loca.lt"
echo "Operational URL: https://${SUB_8506}.loca.lt"
