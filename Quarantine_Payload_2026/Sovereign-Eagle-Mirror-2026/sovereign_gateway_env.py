"""
Sovereign Gateway environment — root `.env` + optional `gateway_ingress.env`.

Import `ensure_sovereign_gateway_env_loaded()` from KYSAH, Termii (DAPI), Part_* scripts, or app entry
before reading `os.environ` so the BotFather token and Termii keys activate the Command Center.

Root = directory containing this file (Sovereign-Eagle-Mirror-2026).
"""

from __future__ import annotations

import os
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent
_ENV_LOADED = False

_ALLOWED_KEYS = frozenset(
    {
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_WEBHOOK_SECRET",
        "GCSLC_BRIDGE_SQLITE",
        "TELEGRAM_BRIDGE_ALLOWED_CHAT_IDS",
        "GCSLC_NAFC_AUDIT_FEED_URL",
        "GCSLC_TERMII_AUDIT_FEED_URL",
        "TERMII_API_KEY",
        "TERMII_API_BASE",
        "TERMII_SENDER_ID",
        "TERMII_SENDER_NAME",
        "TERMII_OTP_CHANNEL",
        "TERMII_PIN_ATTEMPTS",
    }
)


def project_root() -> Path:
    return _REPO_ROOT


def _apply_env_file(path: Path, *, override: bool) -> int:
    if not path.is_file():
        return 0
    n = 0
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0
    for line in raw.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k not in _ALLOWED_KEYS:
            continue
        if not override and (os.environ.get(k) or "").strip():
            continue
        os.environ[k] = v
        n += 1
    return n


def ensure_sovereign_gateway_env_loaded(*, override: bool = False) -> int:
    """
    Load `.env` then `gateway_ingress.env` from repo root. Idempotent unless override=True.
    Returns number of key assignments applied across both files (first pass only).
    """
    global _ENV_LOADED
    if _ENV_LOADED and not override:
        return 0
    total = 0
    for name in (".env", "gateway_ingress.env"):
        total += _apply_env_file(_REPO_ROOT / name, override=override)
    _ENV_LOADED = True
    return total


def get_telegram_bot_token() -> str:
    ensure_sovereign_gateway_env_loaded()
    return (os.environ.get("TELEGRAM_BOT_TOKEN") or "").strip()


def telegram_gateway_armed() -> bool:
    return bool(get_telegram_bot_token())
