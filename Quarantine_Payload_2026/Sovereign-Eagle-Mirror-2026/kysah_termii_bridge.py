"""
Termii API bridge — verification rail for KYSAH (Know Your Student to his Area and Home · OTP / SMS).

Production (Nigeria host — Termii docs):
  POST {BASE}/sms/otp/send   — Send Token (OTP)
  POST {BASE}/sms/otp/verify — Verify Token

Default BASE: https://api.ng.termii.com/api  (override with TERMII_API_BASE).

Required OTP send fields per Termii: api_key, pin_type, message_type, to, from, channel,
pin_attempts, pin_time_to_live, pin_length, pin_placeholder, message_text.
Transactional OTPs: use channel `dnd` when enabled on your account (TERMII_OTP_CHANNEL=dnd).

Area / Home facts: embedded in message_text (and mirrored server-side on verify); never log raw MSISDN.
"""

from __future__ import annotations

import os
from typing import Any

import requests

try:
    from sovereign_gateway_env import ensure_sovereign_gateway_env_loaded

    ensure_sovereign_gateway_env_loaded()
except ImportError:
    pass

TERMII_API_BASE = os.environ.get("TERMII_API_BASE", "https://api.ng.termii.com/api").rstrip("/")


def _kysah_otp_message_text(
    *,
    area_token: str,
    home_token: str,
    institution_id: str,
    pin_placeholder: str,
) -> str:
    """SMS body — Area before Home (Chairman protocol). Placeholder replaced by Termii with live PIN."""
    inst = (institution_id or "").strip()
    tail = f" · {inst}" if inst else ""
    return (
        f"KYSAH verification · Area {area_token.strip() or '?'} · "
        f"Home {home_token.strip() or '?'}{tail} · PIN {pin_placeholder}"
    )


def termii_send_otp(
    msisdn_e164: str,
    *,
    pin_length: int = 6,
    pin_ttl_minutes: int = 5,
    area_token: str = "",
    home_token: str = "",
    institution_id: str = "",
) -> dict[str, Any]:
    """
    Send numeric OTP — Termii Send Token API.

    `area_token` / `home_token` / `institution_id` are woven into message_text so the handset
    receipt matches the Guardian Mirror's Area→Home verification fact.
    """
    key = (os.environ.get("TERMII_API_KEY") or "").strip()
    if not key:
        tail = "".join(ch for ch in msisdn_e164 if ch.isdigit())[-4:]
        pin_len = max(4, min(8, int(pin_length)))
        ph = "< " + ("0" * pin_len) + " >"
        return {
            "status": "dry_run",
            "detail": "TERMII_API_KEY unset — no network call",
            "phone_tail": tail,
            "kysah_area": (area_token or "").strip(),
            "kysah_home": (home_token or "").strip(),
            "message_text_preview": _kysah_otp_message_text(
                area_token=area_token,
                home_token=home_token,
                institution_id=institution_id,
                pin_placeholder=ph,
            ),
            "endpoint_preview": f"{TERMII_API_BASE}/sms/otp/send",
        }
    sender = (os.environ.get("TERMII_SENDER_ID") or os.environ.get("TERMII_SENDER_NAME") or "KYSAH").strip()
    channel = (os.environ.get("TERMII_OTP_CHANNEL") or "dnd").strip().lower()
    if channel not in ("dnd", "generic"):
        channel = "dnd"
    pin_len = max(4, min(8, int(pin_length)))
    ph = "< " + ("0" * pin_len) + " >"
    url = f"{TERMII_API_BASE}/sms/otp/send"
    payload: dict[str, Any] = {
        "api_key": key,
        "pin_type": "NUMERIC",
        "message_type": "NUMERIC",
        "to": "".join(ch for ch in msisdn_e164 if ch.isdigit()),
        "from": sender,
        "channel": channel,
        "pin_attempts": max(1, int(os.environ.get("TERMII_PIN_ATTEMPTS", "3"))),
        "pin_time_to_live": max(1, min(60, int(pin_ttl_minutes))),
        "pin_length": pin_len,
        "pin_placeholder": ph,
        "message_text": _kysah_otp_message_text(
            area_token=area_token,
            home_token=home_token,
            institution_id=institution_id,
            pin_placeholder=ph,
        ),
    }
    headers = {"Content-Type": "application/json"}
    r = requests.post(url, json=payload, headers=headers, timeout=30)
    try:
        body: dict[str, Any] = r.json()
    except Exception:
        return {"status": "error", "http": r.status_code, "text": r.text[:500]}
    if isinstance(body, dict):
        body["_kysah_bind"] = {
            "area_token": (area_token or "").strip(),
            "home_token": (home_token or "").strip(),
            "institution_id": (institution_id or "").strip(),
        }
    return body


def termii_verify_otp(pin_id: str, otp: str) -> dict[str, Any]:
    """Verify OTP — Termii Verify Token API (`pin_id` from send response; user-entered `pin`)."""
    key = (os.environ.get("TERMII_API_KEY") or "").strip()
    if not key:
        return {"status": "dry_run", "detail": "TERMII_API_KEY unset"}
    url = f"{TERMII_API_BASE}/sms/otp/verify"
    payload = {"api_key": key, "pin_id": pin_id.strip(), "pin": str(otp).strip()}
    headers = {"Content-Type": "application/json"}
    r = requests.post(url, json=payload, headers=headers, timeout=30)
    try:
        return r.json()
    except Exception:
        return {"status": "error", "http": r.status_code, "text": r.text[:500]}
