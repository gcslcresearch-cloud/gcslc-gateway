"""
Ingress spine — NAFC (network) and Termii audit sources plug in here without breaking the terminal.

Implementations return optional advisory dicts (merged into Telegram prism footers later).
Chairman sets read-only feed URLs via env when ready; stubs return None today.

VERCEL / NAFC PERIMETER: optional `GCSLC_NAFC_AUDIT_FEED_URL` is **read-only HTTP GET** (listener / ingest
when audits are finalized). This package never performs writes to external command surfaces.
`GCSLC_TERMII_AUDIT_FEED_URL` — same contract for Termii audit payloads.
"""

from __future__ import annotations

import os
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class NetworkAuditSource(Protocol):
    def fetch_advisory(self) -> dict[str, Any] | None:
        """Latest network / NAFC-class advisory blob, or None if idle."""


@runtime_checkable
class TermiiAuditSource(Protocol):
    def fetch_advisory(self) -> dict[str, Any] | None:
        """Latest Termii / messaging audit advisory, or None if idle."""


class StubNetworkAuditSource:
    def fetch_advisory(self) -> dict[str, Any] | None:
        return None


class StubTermiiAuditSource:
    def fetch_advisory(self) -> dict[str, Any] | None:
        return None


class _EnvHttpPeekSource:
    """Optional GET to Chairman-provided read URL (e.g. future NAFC JSON); never mutates remote."""

    def __init__(self, env_key: str, *, label: str) -> None:
        self._env_key = env_key
        self._label = label

    def fetch_advisory(self) -> dict[str, Any] | None:
        url = (os.environ.get(self._env_key) or "").strip()
        if not url:
            return None
        try:
            import requests

            r = requests.get(url, timeout=6)
            if r.status_code != 200:
                return {self._label: f"http_{r.status_code}"}
            ct = (r.headers.get("Content-Type") or "").lower()
            if "json" in ct:
                body = r.json()
                return {self._label: body} if isinstance(body, dict) else {self._label: str(body)[:800]}
            return {self._label: r.text[:1200]}
        except Exception as exc:  # noqa: BLE001
            return {self._label: f"peek_error:{type(exc).__name__}"}


class IngressRegistry:
    """Holds pluggable sources; Streamlit / gateway read without importing NAFC internals."""

    def __init__(self) -> None:
        self.network: NetworkAuditSource = StubNetworkAuditSource()
        self.termii: TermiiAuditSource = StubTermiiAuditSource()
        if (os.environ.get("GCSLC_NAFC_AUDIT_FEED_URL") or "").strip():
            self.network = _EnvHttpPeekSource("GCSLC_NAFC_AUDIT_FEED_URL", label="nafc_feed_peek")
        if (os.environ.get("GCSLC_TERMII_AUDIT_FEED_URL") or "").strip():
            self.termii = _EnvHttpPeekSource("GCSLC_TERMII_AUDIT_FEED_URL", label="termii_feed_peek")

    def augment_prism_footer_lines(self) -> list[str]:
        lines: list[str] = []
        n = self.network.fetch_advisory()
        if n:
            lines.append(f"NETWORK · {n}")
        t = self.termii.fetch_advisory()
        if t:
            lines.append(f"TERMII · {t}")
        return lines[:6]


_DEFAULT_REGISTRY = IngressRegistry()


def default_ingress_registry() -> IngressRegistry:
    return _DEFAULT_REGISTRY
