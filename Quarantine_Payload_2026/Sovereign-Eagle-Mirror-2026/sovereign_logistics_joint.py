"""
Sovereign Logistics Joint — forensic spine (stub JSON + optional live gantry JSONL).

Live ingress appends rows to Part_02_Finance/data/logistics_gantry_live.jsonl;
Streamlit merges per GCSLC_LOGISTICS_SOURCE (merge | stub_only | live_only).

Production MSISDN: hash at edge per production_msisdn_protocol.json; counsel approval required.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import math
import os
import re
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
CONSENT_MANIFEST_JSON = BASE_DIR / "Part_02_Finance" / "data" / "fleet_consent_manifest.json"
LOGISTICS_INGEST_STUB_JSON = BASE_DIR / "Part_02_Finance" / "data" / "logistics_sms_ingest_stub.json"
LOGISTICS_GANTRY_LIVE_JSONL = BASE_DIR / "Part_02_Finance" / "data" / "logistics_gantry_live.jsonl"
PRODUCTION_MSISDN_PROTOCOL_JSON = (
    BASE_DIR / "Part_02_Finance" / "data" / "production_msisdn_protocol.json"
)

_LOGISTICS_SOURCE_MODES = frozenset({"merge", "stub_only", "live_only"})


def load_fleet_consent_manifest(path: Path | None = None) -> dict[str, Any]:
    p = path or CONSENT_MANIFEST_JSON
    if not p.is_file():
        return {"meta": {}, "fleets": []}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"meta": {}, "fleets": []}


def load_logistics_ingest_stub(path: Path | None = None) -> dict[str, Any]:
    p = path or LOGISTICS_INGEST_STUB_JSON
    if not p.is_file():
        return {"meta": {}, "records": []}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"meta": {}, "records": []}


def load_production_msisdn_protocol(path: Path | None = None) -> dict[str, Any]:
    """Counsel-locked production subscriber handling — referenced by consent manifest meta."""
    p = path or PRODUCTION_MSISDN_PROTOCOL_JSON
    if not p.is_file():
        return {"meta": {}, "rules": []}
    try:
        blob = json.loads(p.read_text(encoding="utf-8"))
        return blob if isinstance(blob, dict) else {"meta": {}, "rules": []}
    except (json.JSONDecodeError, OSError):
        return {"meta": {}, "rules": []}


def logistics_joint_cache_buster() -> str:
    """Mtime + size of live JSONL + ingest mode — bust Streamlit cache when gantry file grows."""
    mode = os.environ.get("GCSLC_LOGISTICS_SOURCE", "merge").strip().lower()
    if mode not in _LOGISTICS_SOURCE_MODES:
        mode = "merge"
    p = LOGISTICS_GANTRY_LIVE_JSONL
    if not p.is_file():
        return f"{mode}:0:0"
    try:
        st = p.stat()
        return f"{mode}:{st.st_mtime_ns}:{st.st_size}"
    except OSError:
        return f"{mode}:0:0"


def load_logistics_live_records(
    path: Path | None = None, *, max_records: int = 400
) -> list[dict[str, Any]]:
    """Tail-read append-only gantry truth (JSONL)."""
    p = path or LOGISTICS_GANTRY_LIVE_JSONL
    if not p.is_file():
        return []
    try:
        lines = p.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    out: list[dict[str, Any]] = []
    for line in lines[-max_records:]:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            out.append(obj)
    return out


def msisdn_storage_fingerprint(msisdn: str, *, salt: str) -> str:
    """HMAC-SHA256 truncated — never persist raw MSISDN at rest."""
    digits = re.sub(r"\D+", "", msisdn or "")
    if not digits:
        raise ValueError("empty_msisdn_digits")
    digest = hmac.new(salt.encode("utf-8"), digits.encode("utf-8"), hashlib.sha256).hexdigest()
    return digest[:32]


def normalize_gantry_webhook_payload(body: dict[str, Any]) -> dict[str, Any]:
    """
    Validate HTTP/SMPP-adjacent gantry POST body. Drops raw MSISDN; optional msisdn → msisdn_fp.
    Raises ValueError with a short code for HTTP mapping.
    """
    for k in ("event_id", "fleet_id", "fleet_operator", "gantry_id"):
        if not str(body.get(k) or "").strip():
            raise ValueError(f"missing_{k}")
    out: dict[str, Any] = {
        "event_id": str(body["event_id"]).strip(),
        "fleet_id": str(body["fleet_id"]).strip(),
        "fleet_operator": str(body["fleet_operator"]).strip().upper(),
        "gantry_id": str(body["gantry_id"]).strip(),
        "source": "gantry_webhook",
    }
    if body.get("ts_iso") is not None:
        out["ts_iso"] = str(body["ts_iso"]).strip()
    for opt in ("lat", "lon", "azk_segment_index", "raw_text", "joint_confidence", "msisdn_last4"):
        if body.get(opt) is None:
            continue
        out[opt] = body[opt]
    adm = body.get("admin")
    if isinstance(adm, dict):
        out["admin"] = adm
    chain = body.get("source_chain")
    if isinstance(chain, list):
        out["source_chain"] = list(chain) + ["gantry_webhook", "normalize_gantry_webhook_payload"]
    else:
        out["source_chain"] = ["gantry_webhook", "normalize_gantry_webhook_payload"]
    raw_msisdn = body.get("msisdn")
    if raw_msisdn not in (None, ""):
        salt = os.environ.get("GCSLC_MSISDN_SALT", "").strip()
        if not salt:
            raise ValueError("msisdn_requires_GCSLC_MSISDN_SALT")
        out["msisdn_fp"] = msisdn_storage_fingerprint(str(raw_msisdn), salt=salt)
    # Hard ban on accidental passthrough
    out.pop("msisdn", None)
    return out


def append_gantry_live_event(record: dict[str, Any], path: Path | None = None) -> None:
    """Append one normalized gantry record (single line JSON)."""
    p = path or LOGISTICS_GANTRY_LIVE_JSONL
    p.parent.mkdir(parents=True, exist_ok=True)
    safe = dict(record)
    safe.pop("msisdn", None)
    line = json.dumps(safe, ensure_ascii=False, separators=(",", ":")) + "\n"
    with p.open("a", encoding="utf-8") as f:
        f.write(line)


def _merge_raw_record_streams(
    live: list[dict[str, Any]], stub: list[dict[str, Any]], mode: str
) -> list[dict[str, Any]]:
    if mode == "stub_only":
        return list(stub)
    if mode == "live_only":
        return list(live)
    merged: list[dict[str, Any]] = []
    merged.extend(stub)
    merged.extend(live)
    by_id: dict[str, dict[str, Any]] = {}
    anon_i = 0
    for rec in merged:
        if not isinstance(rec, dict):
            continue
        eid = str(rec.get("event_id") or "").strip()
        key = eid if eid else f"__anon_{anon_i}"
        if not eid:
            anon_i += 1
        by_id[key] = rec
    return list(by_id.values())


def _sort_events_newest_first(rows: list[dict[str, Any]]) -> None:
    def _key(r: dict[str, Any]) -> str:
        return str(r.get("ts_iso") or "")

    rows.sort(key=_key, reverse=True)


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * r * math.asin(min(1.0, math.sqrt(a)))


def nearest_azk_segment_index(lat: float, lon: float, azk_nodes: list[dict[str, Any]]) -> int:
    if not azk_nodes:
        return 0
    best_i = 0
    best_d = 1e18
    for i, n in enumerate(azk_nodes):
        try:
            d = _haversine_km(lat, lon, float(n["lat"]), float(n["lon"]))
        except (KeyError, TypeError, ValueError):
            continue
        if d < best_d:
            best_d = d
            best_i = i
    return best_i


def enrich_record_with_azk_geometry(rec: dict[str, Any], azk_nodes: list[dict[str, Any]]) -> dict[str, Any]:
    """Attach lat/lon from AZK spine node index when absent."""
    out = dict(rec)
    idx = int(out.get("azk_segment_index") or 0)
    idx = max(0, min(len(azk_nodes) - 1, idx)) if azk_nodes else 0
    node = azk_nodes[idx] if azk_nodes else {}
    try:
        lat0 = float(out.get("lat")) if out.get("lat") is not None else float(node.get("lat", 0))
        lon0 = float(out.get("lon")) if out.get("lon") is not None else float(node.get("lon", 0))
    except (TypeError, ValueError):
        lat0 = float(node.get("lat", 9.05))
        lon0 = float(node.get("lon", 7.5))
    out["lat"] = lat0
    out["lon"] = lon0
    out["azk_segment_index"] = idx
    if out.get("azk_chainage_km") is None and azk_nodes:
        out["azk_chainage_km"] = round(
            sum(
                _haversine_km(
                    float(azk_nodes[j]["lat"]),
                    float(azk_nodes[j]["lon"]),
                    float(azk_nodes[j + 1]["lat"]),
                    float(azk_nodes[j + 1]["lon"]),
                )
                for j in range(idx)
            ),
            2,
        )
    return out


def event_passes_consent_gate(ev: dict[str, Any], manifest: dict[str, Any]) -> tuple[bool, str]:
    """
    Legal / contract gate stub — fleet-owned SIM + explicit fleet registration only.

    Returns (allowed, reason_code).
    """
    fleets = manifest.get("fleets") if isinstance(manifest.get("fleets"), list) else []
    fid = str(ev.get("fleet_id") or "").strip()
    op = str(ev.get("fleet_operator") or "").strip().upper()
    if not fid:
        return False, "missing_fleet_id"
    for row in fleets:
        if not isinstance(row, dict):
            continue
        if str(row.get("fleet_id") or "").strip() != fid:
            continue
        st = str(row.get("status") or "").lower()
        if st in ("revoked", "suspended", "denied"):
            return False, f"consent_status_{st}"
        if str(row.get("operator") or "").strip().upper() != op and op not in ("UNKNOWN", ""):
            return False, "operator_mismatch"
        own = str(row.get("sim_ownership") or "").lower()
        if own and own != "fleet_owned":
            return False, "sim_not_fleet_owned"
        return True, "consent_ok"
    return False, "fleet_not_registered"


def normalize_sms_stub(text: str, meta: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    Normalize raw SMS body to a partial joint record (no network I/O).

    Meta may include fleet_id, fleet_operator, gantry_id, azk_segment_index.
    """
    meta = meta or {}
    t = re.sub(r"\s+", " ", (text or "").strip())
    upper = t.upper()
    gantry_guess = meta.get("gantry_id") or ""
    if not gantry_guess:
        if "KEFFI" in upper:
            gantry_guess = "AZK-KEFFI-STUB"
        elif "KADUNA" in upper:
            gantry_guess = "AZK-KADUNA-STUB"
        elif "ZARIA" in upper:
            gantry_guess = "AZK-ZARIA-STUB"
        elif "KANO" in upper:
            gantry_guess = "AZK-KANO-STUB"
        elif "ABUJA" in upper or "FCT" in upper:
            gantry_guess = "AZK-ABUJA-STUB"
    seg = meta.get("azk_segment_index")
    if seg is None:
        if "KEFFI" in upper:
            seg = 1
        elif "KADUNA" in upper:
            seg = 2
        elif "ZARIA" in upper:
            seg = 3
        elif "KANO" in upper:
            seg = 4
        else:
            seg = 0
    return {
        "source": "sms_stub",
        "raw_text": t[:500],
        "gantry_id": str(gantry_guess),
        "fleet_id": str(meta.get("fleet_id") or ""),
        "fleet_operator": str(meta.get("fleet_operator") or "UNKNOWN").upper(),
        "azk_segment_index": int(seg),
        "source_chain": ["sms_stub", "normalize_sms_stub"],
    }


def joint_confidence_roll_up(ev: dict[str, Any]) -> float:
    """Determinants-4 rollup: weakest admin tier caps declared joint confidence."""
    adm = ev.get("admin") if isinstance(ev.get("admin"), dict) else {}
    try:
        declared = float(ev.get("joint_confidence") or 0.75)
    except (TypeError, ValueError):
        declared = 0.75
    try:
        tiers = [
            float(adm.get("state_conf") or 0),
            float(adm.get("lga_conf") or 0),
            float(adm.get("ward_conf") or 0),
            float(adm.get("pu_conf") or 0),
        ]
    except (TypeError, ValueError):
        return max(0.12, min(1.0, declared))
    chain_cap = min(tiers) if tiers else 0.35
    return max(0.12, min(1.0, declared, chain_cap))


def events_to_azk_fractional_targets(
    events: list[dict[str, Any]],
    corridor_fractions: list[dict[str, float]],
) -> tuple[list[dict[str, float]], list[float]]:
    """Map approved events to Folium-normalized corridor fractions + Sentinel weights."""
    if not corridor_fractions:
        corridor_fractions = [{"x": 0.5, "y": 0.45}]
    targets: list[dict[str, float]] = []
    weights: list[float] = []
    for ev in events:
        if not isinstance(ev, dict):
            continue
        idx = int(ev.get("azk_segment_index") or 0)
        idx = idx % len(corridor_fractions)
        pt = dict(corridor_fractions[idx])
        jc = joint_confidence_roll_up(ev)
        reps = max(1, min(6, int(1 + jc * 5)))
        for _ in range(reps):
            targets.append(pt)
            weights.append(round(min(1.0, jc + 0.08 * reps / 6), 4))
    return targets, weights


def merge_patrol_with_logistics(
    base_targets: list[dict[str, float]],
    base_weights: list[float] | None,
    logistics_targets: list[dict[str, float]],
    logistics_weights: list[float],
    *,
    cap: int = 145,
) -> tuple[list[dict[str, float]], list[float]]:
    """Prepend confidence-dense logistics nodes; pad base weights to ~0.42."""
    bw = list(base_weights or [])
    if len(bw) < len(base_targets):
        bw.extend([0.42] * (len(base_targets) - len(bw)))
    if not logistics_targets:
        return base_targets[:cap], bw[:cap]
    out_t = list(logistics_targets) + base_targets
    out_w = list(logistics_weights) + bw
    out_t = out_t[:cap]
    out_w = out_w[:cap]
    if len(out_w) < len(out_t):
        out_w.extend([0.42] * (len(out_t) - len(out_w)))
    return out_t, out_w[: len(out_t)]


def sniff_lines_from_joint_events(events: list[dict[str, Any]], *, limit: int = 6) -> list[str]:
    lines: list[str] = []
    for ev in events[:limit]:
        if not isinstance(ev, dict):
            continue
        gid = str(ev.get("gantry_id") or "?")
        jc = joint_confidence_roll_up(ev)
        seg = ev.get("azk_segment_index", "?")
        op = ev.get("fleet_operator", "?")
        raw = str(ev.get("raw_text") or "")[:100]
        lines.append(
            f"Sovereign Joint · AZK seg {seg} · {op} · {gid} · conf {jc:.2f} · {raw}"
        )
    if not lines:
        lines.append(
            "Sovereign Joint · ingest IDLE — mount logistics_sms_ingest_stub.json + fleet consent manifest"
        )
    return lines


def build_approved_logistics_bundle(
    azk_nodes: list[dict[str, Any]],
    corridor_fractions: list[dict[str, float]],
) -> dict[str, Any]:
    """Load live JSONL + stub → consent filter → enrich → targets/weights/sniffs."""
    mode = os.environ.get("GCSLC_LOGISTICS_SOURCE", "merge").strip().lower()
    if mode not in _LOGISTICS_SOURCE_MODES:
        mode = "merge"
    manifest = load_fleet_consent_manifest()
    protocol = load_production_msisdn_protocol()
    live_recs = load_logistics_live_records()
    blob = load_logistics_ingest_stub()
    stub_recs = [r for r in (blob.get("records") or []) if isinstance(r, dict)]
    raw_recs = _merge_raw_record_streams(live_recs, stub_recs, mode)
    _sort_events_newest_first(raw_recs)
    approved: list[dict[str, Any]] = []
    rejected: list[tuple[str, str]] = []
    for rec in raw_recs:
        ev = enrich_record_with_azk_geometry(rec, azk_nodes)
        ok, reason = event_passes_consent_gate(ev, manifest)
        if ok:
            ev["joint_confidence"] = joint_confidence_roll_up(ev)
            ev["source_chain"] = list(ev.get("source_chain") or []) + ["consent_gate_ok"]
            approved.append(ev)
        else:
            rejected.append((str(ev.get("event_id") or "?"), reason))
    lt, lw = events_to_azk_fractional_targets(approved, corridor_fractions)
    return {
        "approved_events": approved,
        "rejected": rejected,
        "logistics_targets": lt,
        "logistics_weights": lw,
        "sniffs": sniff_lines_from_joint_events(approved),
        "manifest_meta": manifest.get("meta") or {},
        "production_msisdn_protocol": protocol,
        "ingest_mode": mode,
        "live_ingest_rows": len(live_recs),
        "stub_rows": len(stub_recs),
    }
