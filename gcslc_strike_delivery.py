# GCSLC — optional WhatsApp delivery helpers (Twilio / Whapi.cloud).
# Use from a worker or admin path; do not block Streamlit UI with bulk sends.
# Secrets: set in Hugging Face / Streamlit Cloud / private cloud "Secrets" — never commit values.

from __future__ import annotations

import base64
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


def _env(name: str, default: str = "") -> str:
    return str(os.environ.get(name, default) or "").strip()


def twilio_whatsapp_send(
    *,
    account_sid: str,
    auth_token: str,
    from_whatsapp: str,
    to_whatsapp: str,
    body: str,
    media_url: str | None = None,
    timeout: float = 45.0,
) -> tuple[bool, str, dict[str, Any]]:
    """
    Twilio REST: create a WhatsApp message (optionally with MediaUrl).
    from_whatsapp / to_whatsapp must be whatsapp:+E164 (e.g. whatsapp:+2348012345678).
    """
    sid = account_sid.strip()
    token = auth_token.strip()
    if not sid or not token:
        return False, "missing_account_sid_or_token", {}
    url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"
    data: dict[str, str] = {
        "From": from_whatsapp.strip(),
        "To": to_whatsapp.strip(),
        "Body": body,
    }
    if media_url:
        data["MediaUrl"] = media_url.strip()

    payload = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    cred = base64.b64encode(f"{sid}:{token}".encode("utf-8")).decode("ascii")
    req.add_header("Authorization", f"Basic {cred}")

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return True, "", (json.loads(raw) if raw.strip() else {})
    except urllib.error.HTTPError as e:
        try:
            raw = e.read().decode("utf-8", errors="replace")
            return False, raw, (json.loads(raw) if raw.strip() else {})
        except Exception:
            return False, str(e), {}
    except Exception as e:
        return False, str(e), {}


def whapi_send_message_json(
    *,
    api_token: str,
    api_base: str,
    to_phone: str,
    body: str,
    media_url: str | None = None,
    timeout: float = 60.0,
) -> tuple[bool, str, dict[str, Any]]:
    """
    Whapi.cloud-style JSON POST (Bearer token). Paths differ by workspace — set GCSLC_WHAPI_SEND_PATH.

    Typical fields: to, body, optional media / media_url (depends on your Whapi channel schema).
    """
    token = api_token.strip()
    if not token:
        return False, "missing_whapi_token", {}

    base = (api_base or "https://gate.whapi.cloud").rstrip("/")
    path = _env("GCSLC_WHAPI_SEND_PATH", "/messages/text")
    url = urllib.parse.urljoin(base + "/", path.lstrip("/"))

    payload_obj: dict[str, Any] = {"to": to_phone, "body": body}
    if media_url:
        payload_obj["media"] = media_url.strip()

    payload = json.dumps(payload_obj).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return True, "", (json.loads(raw) if raw.strip() else {})
    except urllib.error.HTTPError as e:
        try:
            raw = e.read().decode("utf-8", errors="replace")
            return False, raw, (json.loads(raw) if raw.strip() else {})
        except Exception:
            return False, str(e), {}
    except Exception as e:
        return False, str(e), {}


def load_phone_column_from_parquet(path: Path, *, max_rows: int, phone_col: str | None = None) -> list[str]:
    """
    Read up to max_rows from a parquet file and return normalized E.164-ish strings from phone column.
    Does not load the full file: uses pyarrow batched read when available.
    """
    try:
        import pyarrow.parquet as pq  # type: ignore
    except Exception:
        df = __import__("pandas").read_parquet(path)
        col = phone_col or _guess_phone_col(df.columns)
        if not col:
            return []
        s = df[col].astype(str).head(max_rows)
        return [x.strip() for x in s.tolist() if x and str(x).strip()]

    pf = pq.ParquetFile(path)
    col = phone_col
    if col is None:
        col = _guess_phone_col(pf.schema.names)
        if not col:
            return []
    out: list[str] = []
    for batch in pf.iter_batches(batch_size=8192, columns=[col]):
        df = batch.to_pandas()
        if col not in df.columns:
            return []
        for c in df[col].astype(str).tolist():
            c = str(c).strip()
            if c:
                out.append(c)
            if len(out) >= max_rows:
                return out
    return out


def _guess_phone_col(columns: Any) -> str | None:
    norm = {str(c).strip().lower().replace(" ", "_"): c for c in columns}
    for key in ("phone", "msisdn", "phone_number", "mobile", "whatsapp", "wa_number"):
        if key in norm:
            return str(norm[key])
    return None


def twilio_broadcast_whatsapp_media(
    *,
    recipients: list[str],
    body: str,
    media_url: str | None = None,
    from_whatsapp: str | None = None,
    sleep_s: float = 0.35,
) -> tuple[int, int, list[str]]:
    """
    Fire-and-forget style sequential broadcast (use a real job queue in production).
    Returns (ok_count, fail_count, last_errors tail).
    """
    import time

    sid = _env("TWILIO_ACCOUNT_SID")
    token = _env("TWILIO_AUTH_TOKEN")
    from_wa = (from_whatsapp or _env("TWILIO_WHATSAPP_FROM")).strip()
    if not (sid and token and from_wa):
        return 0, len(recipients), ["missing_TWILIO_ACCOUNT_SID_or_TWILIO_AUTH_TOKEN_or_TWILIO_WHATSAPP_FROM"]

    errs: list[str] = []
    ok = 0
    fail = 0
    for to in recipients:
        to_wa = to.strip()
        if not to_wa.startswith("whatsapp:"):
            to_wa = f"whatsapp:{to_wa}" if to_wa.startswith("+") else f"whatsapp:+{to_wa}"
        good, err, _js = twilio_whatsapp_send(
            account_sid=sid,
            auth_token=token,
            from_whatsapp=from_wa,
            to_whatsapp=to_wa,
            body=body,
            media_url=media_url,
        )
        if good:
            ok += 1
        else:
            fail += 1
            errs.append(err[:500])
        time.sleep(max(0.0, float(sleep_s)))
        if len(errs) > 12:
            errs = errs[-12:]
    return ok, fail, errs
