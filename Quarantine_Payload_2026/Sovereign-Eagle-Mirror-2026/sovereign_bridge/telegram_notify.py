"""Outbound Telegram Bot API — uses TELEGRAM_BOT_TOKEN from environment."""

from __future__ import annotations

import os
from typing import Any

import requests


def send_message_html(*, chat_id: int, html_body: str, disable_preview: bool = True) -> dict[str, Any] | None:
    token = (os.environ.get("TELEGRAM_BOT_TOKEN") or "").strip()
    if not token:
        return None
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": html_body[:4090],
        "parse_mode": "HTML",
        "disable_web_page_preview": disable_preview,
    }
    try:
        r = requests.post(url, json=payload, timeout=25)
        if not r.ok:
            return {"ok": False, "status": r.status_code, "body": r.text[:500]}
        return r.json()
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": type(exc).__name__, "detail": str(exc)[:400]}
