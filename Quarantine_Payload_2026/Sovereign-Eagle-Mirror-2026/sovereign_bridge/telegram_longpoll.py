"""
Long-poll Telegram updates into the same SQLite queue (local dev / no public HTTPS).

  export TELEGRAM_BOT_TOKEN='…'
  python -m sovereign_bridge.telegram_longpoll

Delete webhook first if you were using webhook mode:
  curl "https://api.telegram.org/bot<TOKEN>/deleteWebhook"
"""

from __future__ import annotations

import os
import sys
import time

import requests

from sovereign_bridge.env_socket import load_gateway_ingress_env
from sovereign_bridge.telegram_store import enqueue_update


def main() -> None:
    load_gateway_ingress_env()
    token = (os.environ.get("TELEGRAM_BOT_TOKEN") or "").strip()
    if not token:
        print("TELEGRAM_BOT_TOKEN required", file=sys.stderr)
        sys.exit(1)
    base = f"https://api.telegram.org/bot{token}"
    offset = 0
    print("Sovereign Bridge long-poll · enqueue to SQLite · Ctrl+C to stop", flush=True)
    while True:
        try:
            r = requests.get(
                f"{base}/getUpdates",
                params={"timeout": 45, "offset": offset},
                timeout=50,
            )
            data = r.json()
        except Exception as exc:  # noqa: BLE001
            print("poll error:", exc, flush=True)
            time.sleep(3.0)
            continue
        if not data.get("ok"):
            print("getUpdates not ok:", data, flush=True)
            time.sleep(2.0)
            continue
        for upd in data.get("result") or []:
            if not isinstance(upd, dict):
                continue
            uid = int(upd.get("update_id") or 0)
            offset = max(offset, uid + 1)
            msg = upd.get("message") or upd.get("edited_message")
            if not isinstance(msg, dict):
                continue
            chat = msg.get("chat")
            if not isinstance(chat, dict) or chat.get("id") is None:
                continue
            text = msg.get("text") or msg.get("caption") or ""
            if enqueue_update(update_id=uid, chat_id=int(chat["id"]), text=str(text)):
                print(f"enqueued update {uid}", flush=True)
        time.sleep(0.05)


if __name__ == "__main__":
    main()
