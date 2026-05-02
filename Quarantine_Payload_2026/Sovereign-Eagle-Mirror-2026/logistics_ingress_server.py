"""
Gantry webhook ingress — append-only JSONL consumed by the Sovereign Mirror.

Run (from this directory):
  export GCSLC_INGRESS_SECRET='…'
  export GCSLC_MSISDN_SALT='…'   # required only when POST includes msisdn
  uvicorn logistics_ingress_server:app --host 0.0.0.0 --port 8787

Or: scripts/run_logistics_ingress.sh
"""

from __future__ import annotations

import os

from fastapi import FastAPI, Header, HTTPException, Request

from sovereign_logistics_joint import append_gantry_live_event, normalize_gantry_webhook_payload

app = FastAPI(title="GCSLC Gantry Ingress", version="1.0.0")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok", "service": "gantry_ingress"}


@app.post("/v1/gantry/event")
async def post_gantry_event(
    request: Request,
    x_gcslc_ingress_secret: str | None = Header(None, alias="X-GCSLC-Ingress-Secret"),
) -> dict[str, object]:
    secret = (os.environ.get("GCSLC_INGRESS_SECRET") or "").strip()
    if not secret:
        raise HTTPException(status_code=503, detail="GCSLC_INGRESS_SECRET not configured")
    if (x_gcslc_ingress_secret or "").strip() != secret:
        raise HTTPException(status_code=401, detail="invalid ingress secret")
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="invalid json")
    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="body must be a JSON object")
    try:
        rec = normalize_gantry_webhook_payload(body)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    append_gantry_live_event(rec)
    return {"ok": True, "event_id": rec.get("event_id")}
