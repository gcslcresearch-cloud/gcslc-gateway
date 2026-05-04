"""
Compatibility shim — delegates to root `sovereign_gateway_env` (`.env` + gateway_ingress.env).
"""

from __future__ import annotations

from sovereign_gateway_env import ensure_sovereign_gateway_env_loaded as load_gateway_ingress_env

__all__ = ["load_gateway_ingress_env"]
