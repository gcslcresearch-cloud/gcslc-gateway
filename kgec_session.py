"""
V203 — K-GEC OS backbone: server-side session mint/verify only.
No tokens or secrets are meant for the public DOM; logic is not exposed to Inspect Element
beyond what Streamlit already renders (opaque session marker only).
"""

from __future__ import annotations

import hashlib
import hmac
import os
from typing import Optional

_V203_SALT = b"gcslc_sovereign_session_v203_kgec"


def _signing_secret() -> bytes:
    s = (os.environ.get("GCSLC_SOVEREIGN_SESSION_SECRET") or os.environ.get("GCSLC_CHAIRMAN_KEY") or "").strip()
    return s.encode("utf-8")


def mint_gcslc_sovereign_session() -> str:
    """Return opaque HMAC session token; empty if no vault secret is configured."""
    key = _signing_secret()
    if not key:
        return ""
    return hmac.new(key, _V203_SALT, hashlib.sha256).hexdigest()


def verify_gcslc_sovereign_session(token: Optional[str]) -> bool:
    if not token:
        return False
    expected = mint_gcslc_sovereign_session()
    if not expected:
        return False
    try:
        return hmac.compare_digest(str(token), expected)
    except Exception:
        return False


def kgec_os_may_respond(token: Optional[str]) -> bool:
    """Heavy Lock: K-GEC private core only responds when a valid Chairman session is minted server-side."""
    return verify_gcslc_sovereign_session(token)
