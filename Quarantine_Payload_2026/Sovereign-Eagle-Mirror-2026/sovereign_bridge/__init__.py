"""
Sovereign Bridge — Telegram ↔ K-GEC Mirror ingress (modular spine).

NAFC / Termii audit feeds plug in via ingress_hooks.Protocol implementations.
Do not embed write paths to third-party command surfaces; Chairman provisions URLs via env only.
"""

from sovereign_bridge.ingress_hooks import (
    IngressRegistry,
    NetworkAuditSource,
    StubNetworkAuditSource,
    StubTermiiAuditSource,
    TermiiAuditSource,
)

__all__ = [
    "IngressRegistry",
    "NetworkAuditSource",
    "TermiiAuditSource",
    "StubNetworkAuditSource",
    "StubTermiiAuditSource",
]
