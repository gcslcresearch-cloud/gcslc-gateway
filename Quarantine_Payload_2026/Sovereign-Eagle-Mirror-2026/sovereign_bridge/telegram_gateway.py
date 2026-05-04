"""
Telegram webhook receiver — enqueues updates for the Streamlit Mirror to claim.

Run (separate terminal from Streamlit):
  # Optional: secrets in gateway_ingress.env (see gateway_ingress.env.example) — auto-loaded on import.
  export TELEGRAM_BOT_TOKEN='…'
  export TELEGRAM_WEBHOOK_SECRET='…'   # required in production; must match setWebhook secret_token
  export GCSLC_BRIDGE_SQLITE='…'         # optional; defaults to .sovereign_bridge/ingress.sqlite
  uvicorn sovereign_bridge.telegram_gateway:app --host 0.0.0.0 --port 8790

setWebhook (Chairman / ops):
  https://api.telegram.org/bot<TOKEN>/setWebhook?url=https://<HOST>/telegram/webhook
  + secret_token field matching TELEGRAM_WEBHOOK_SECRET

This service does not modify third-party NAFC deployments; optional read feeds are env-driven only.
"""

import hmac
import os
from typing import Optional

from fastapi import FastAPI, Header, HTTPException, Request

from sovereign_bridge.env_socket import load_gateway_ingress_env
from sovereign_bridge.telegram_store import enqueue_update

load_gateway_ingress_env()

app = FastAPI(title="GCSLC Sovereign Telegram Gateway", version="1.0.0")


@app.get("/healthz")
def healthz():
    return {"status": "ok", "service": "sovereign_telegram_gateway"}


@app.post("/telegram/webhook")
async def telegram_webhook(
    request: Request,
    x_telegram_bot_api_secret_token: Optional[str] = Header(
        None, alias="X-Telegram-Bot-Api-Secret-Token"
    ),
) -> dict:
    expected = (os.environ.get("TELEGRAM_WEBHOOK_SECRET") or "").strip()
    if expected:
        got = (x_telegram_bot_api_secret_token or "").strip()
        if not hmac.compare_digest(got, expected):
            raise HTTPException(status_code=403, detail="invalid webhook secret")
    try:
        body = await request.json()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail="invalid json") from exc
    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="body must be object")
    uid = body.get("update_id")
    msg = body.get("message")
    if msg is None:
        msg = body.get("edited_message")
    if not isinstance(msg, dict):
        return {"ok": True}
    chat = msg.get("chat")
    if not isinstance(chat, dict):
        return {"ok": True}
    cid = chat.get("id")
    text = msg.get("text") or msg.get("caption") or ""
    if cid is None or uid is None:
        return {"ok": True}
    enqueue_update(update_id=int(uid), chat_id=int(cid), text=str(text))
    return {"ok": True}
