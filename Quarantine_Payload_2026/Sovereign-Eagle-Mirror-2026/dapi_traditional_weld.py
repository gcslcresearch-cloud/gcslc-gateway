"""
DAPI ↔ Traditional hierarchy weld — verification event store, OAuth session stub,
ward-level aggregates for the 8,806 ward spine (Sovereign Eagle Mirror 2026).
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import sqlite3
import time
import uuid
from collections import defaultdict
from pathlib import Path
from typing import Any

import requests

from kaduna_sovereign_pilot import (
    STRANGER_VETTING_DISTANCE_KM,
    district_geo_anchor,
    district_record_by_id,
    is_kaduna_frontier_lga,
    normalize_lga_key,
    resolve_kaduna_ward_spine_row,
)

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DB_PATH = BASE_DIR / "logs" / "dapi_verification.sqlite"

TRADITIONAL_PRINCIPAL_ROLES = frozenset({"me_anguwa", "village_head", "district_head"})


def _connect(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or DEFAULT_DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_verification_store(db_path: Path | None = None) -> None:
    conn = _connect(db_path)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS verification_events (
              student_uid TEXT PRIMARY KEY,
              ward_pcode TEXT NOT NULL,
              principal_id TEXT NOT NULL,
              traditional_role TEXT NOT NULL,
              pu_code TEXT,
              zazzau_district_id TEXT DEFAULT '',
              created_at REAL NOT NULL,
              cert_digest TEXT NOT NULL
            )
            """
        )
        _cols = {
            str(r[1])
            for r in conn.execute("PRAGMA table_info(verification_events)").fetchall()
        }
        if "zazzau_district_id" not in _cols:
            conn.execute(
                "ALTER TABLE verification_events ADD COLUMN zazzau_district_id TEXT DEFAULT ''"
            )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_verification_ward ON verification_events(ward_pcode)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_verification_principal ON verification_events(principal_id)"
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_verification_zazzau_district "
            "ON verification_events(zazzau_district_id)"
        )
        _migrate_verification_columns(conn)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS haraji_cdc_ledger (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              principal_id TEXT NOT NULL,
              ward_pcode TEXT NOT NULL,
              zazzau_district_id TEXT DEFAULT '',
              naira_amount REAL NOT NULL,
              levy_class TEXT NOT NULL,
              narrative TEXT DEFAULT '',
              created_at REAL NOT NULL
            )
            """
        )
        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_haraji_principal ON haraji_cdc_ledger(principal_id)"
        )
        conn.commit()
    finally:
        conn.close()


def _migrate_verification_columns(conn: sqlite3.Connection) -> None:
    _cols = {
        str(r[1]) for r in conn.execute("PRAGMA table_info(verification_events)").fetchall()
    }
    adds = [
        ("nin", "TEXT DEFAULT ''"),
        ("claimant_lat", "REAL"),
        ("claimant_lon", "REAL"),
        ("stranger_vetting_status", "TEXT DEFAULT ''"),
        ("vetting_distance_km", "REAL"),
        ("vetting_note", "TEXT DEFAULT ''"),
    ]
    for col, decl in adds:
        if col not in _cols:
            conn.execute(f"ALTER TABLE verification_events ADD COLUMN {col} {decl}")


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    h = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * r * math.asin(min(1.0, math.sqrt(h)))


def evaluate_stranger_vetting_status(
    zazzau_district_id: str,
    claimant_lat: float | None,
    claimant_lon: float | None,
    *,
    threshold_km: float | None = None,
) -> tuple[str, float | None, str]:
    """
    Stranger vetting vs Zazzau district geo anchor (NIN / address coordinate simulation).
    Returns (status, distance_km_or_none, note).
    """
    thr = float(threshold_km if threshold_km is not None else STRANGER_VETTING_DISTANCE_KM)
    zd = str(zazzau_district_id or "").strip().upper()
    if not zd:
        return "not_evaluated", None, ""
    if claimant_lat is None or claimant_lon is None:
        return (
            "pending_coordinates",
            None,
            "NIN-address coordinates absent — vetting distance not evaluated (Me Anguwa deferred).",
        )
    anch = district_geo_anchor(zd)
    if not anch:
        return "not_evaluated", None, ""
    try:
        la, lo = float(claimant_lat), float(claimant_lon)
    except (TypeError, ValueError):
        return "pending_coordinates", None, "Invalid coordinate payload — vetting deferred."
    dist = _haversine_km(la, lo, anch[0], anch[1])
    if dist > thr:
        return (
            "vetting_required",
            dist,
            (
                f"Vetting Required — NIN / claimed address ~{dist:.1f} km from district anchor "
                f"{zd} (threshold {thr:.0f} km). Me Anguwa firewall must reconcile."
            ),
        )
    return (
        "cleared",
        dist,
        f"Coordinate weld within ancestral corridor (~{dist:.1f} km vs anchor {zd}).",
    )


def _digest_payload(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def verification_preflight(
    *,
    ward_pcode: str,
    traditional_role: str,
    zazzau_district_id: str,
    wards_fc: dict | None,
) -> tuple[bool, str, dict[str, Any]]:
    """
    774 lattice + ancestral ZD weld gate; Security Proximity Tag (SPT) on frontier mismatch.
    Returns (allow_insert, message, meta_for_ui).
    """
    meta: dict[str, Any] = {
        "lattice_ok": True,
        "ward_spine_lga": "",
        "ward_spine_label": "",
        "zd_parent_lga": "",
        "frontier_lga": False,
        "spt_escalate": False,
        "spt_message": "",
        "sovereign_clearance": False,
    }
    if not wards_fc or not wards_fc.get("features"):
        return True, "", meta

    spine_row = resolve_kaduna_ward_spine_row(wards_fc, ward_pcode)
    if not spine_row:
        meta["lattice_ok"] = False
        return (
            False,
            "774 Lattice breach — ward_pcode not found on Kaduna spine (ghost-profile risk).",
            meta,
        )

    meta["ward_spine_lga"] = spine_row.get("lga_en") or ""
    meta["ward_spine_label"] = spine_row.get("ward_en") or ""
    meta["frontier_lga"] = is_kaduna_frontier_lga(meta["ward_spine_lga"])

    zd = str(zazzau_district_id or "").strip().upper()
    role = str(traditional_role or "").strip().lower()
    if role not in TRADITIONAL_PRINCIPAL_ROLES:
        return True, "", meta

    rec = district_record_by_id(zd) if zd else None
    if not rec:
        return False, "Traditional weld blocked — select a valid Zazzau district (ZD01–ZD31).", meta

    parent_raw = str(rec.get("parent_lga_en") or "").strip()
    meta["zd_parent_lga"] = parent_raw
    spine_key = normalize_lga_key(meta["ward_spine_lga"])
    parent_key = normalize_lga_key(parent_raw)
    if spine_key and parent_key and spine_key != parent_key:
        base = (
            f"Ancestral command breach — district ledger parent `{parent_raw}` "
            f"≠ spine LGA `{meta['ward_spine_lga']}` for this ward_pcode."
        )
        if meta["frontier_lga"]:
            meta["spt_escalate"] = True
            meta["spt_message"] = (
                "SPT · Security Proximity Tag — alert District Head node immediately; "
                "frontier LGA + lattice/ZD mismatch (24h criminal-trace protocol)."
            )
            return False, f"{base} {meta['spt_message']}", meta
        return False, base, meta

    return True, "", meta


def record_verification(
    *,
    student_uid: str,
    ward_pcode: str,
    principal_id: str,
    traditional_role: str,
    pu_code: str | None = None,
    zazzau_district_id: str | None = None,
    wards_fc: dict | None = None,
    nin: str | None = None,
    claimant_lat: float | None = None,
    claimant_lon: float | None = None,
    db_path: Path | None = None,
) -> tuple[bool, str, dict[str, Any]]:
    """
    Insert one sovereign verification. UNIQUE(student_uid) enforces zero ghosts.
    Returns (accepted, message, meta) — meta carries Sovereign Clearance + SPT + stranger vetting.
    """
    meta_out: dict[str, Any] = {
        "lattice_ok": True,
        "spt_escalate": False,
        "spt_message": "",
        "sovereign_clearance": False,
        "clearance_message": "",
        "stranger_vetting_status": "not_evaluated",
        "vetting_distance_km": None,
        "vetting_note": "",
        "vetting_required_alert": False,
    }
    student_uid = str(student_uid).strip()
    ward_pcode = str(ward_pcode).strip()
    principal_id = str(principal_id).strip()
    traditional_role = str(traditional_role).strip()
    zd = str(zazzau_district_id or "").strip()
    nin_s = str(nin or "").strip()
    if not student_uid or not ward_pcode or not principal_id:
        return False, "Missing student_uid, ward_pcode, or principal_id.", meta_out

    ok_pre, msg_pre, meta_pre = verification_preflight(
        ward_pcode=ward_pcode,
        traditional_role=traditional_role,
        zazzau_district_id=zd,
        wards_fc=wards_fc,
    )
    meta_out.update(meta_pre)
    if not ok_pre:
        return False, msg_pre, meta_out

    vs, vdist, vnote = evaluate_stranger_vetting_status(zd, claimant_lat, claimant_lon)
    meta_out["stranger_vetting_status"] = vs
    meta_out["vetting_distance_km"] = vdist
    meta_out["vetting_note"] = vnote
    if vs == "vetting_required":
        meta_out["vetting_required_alert"] = True

    ts = time.time()
    payload = {
        "student_uid": student_uid,
        "ward_pcode": ward_pcode,
        "principal_id": principal_id,
        "traditional_role": traditional_role,
        "pu_code": pu_code or "",
        "zazzau_district_id": zd,
        "nin": nin_s,
        "claimant_lat": claimant_lat if claimant_lat is not None else "",
        "claimant_lon": claimant_lon if claimant_lon is not None else "",
        "stranger_vetting_status": vs,
        "vetting_distance_km": vdist if vdist is not None else "",
        "vetting_note": vnote,
        "created_at": ts,
    }
    cert = _digest_payload(payload)
    conn = _connect(db_path)
    try:
        conn.execute(
            """
            INSERT INTO verification_events
              (student_uid, ward_pcode, principal_id, traditional_role, pu_code,
               zazzau_district_id, created_at, cert_digest,
               nin, claimant_lat, claimant_lon, stranger_vetting_status, vetting_distance_km, vetting_note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                student_uid,
                ward_pcode,
                principal_id,
                traditional_role,
                pu_code or "",
                zd,
                ts,
                cert,
                nin_s,
                claimant_lat,
                claimant_lon,
                vs,
                vdist,
                vnote,
            ),
        )
        conn.commit()
        ok_msg = "Sovereign certificate recorded — lattice weld OK."
        if traditional_role.strip().lower() == "me_anguwa":
            meta_out["sovereign_clearance"] = True
            meta_out["clearance_message"] = (
                "Sovereign Clearance — Me Anguwa firewall acknowledgement bound to 774 spine + ZD ledger."
            )
            ok_msg = f"{ok_msg} {meta_out['clearance_message']}"
        if vs == "vetting_required":
            ok_msg = f"{ok_msg} Vetting Required — Me Anguwa review per stranger firewall."
        elif vs == "pending_coordinates":
            ok_msg = f"{ok_msg} Stranger vetting deferred — supply NIN-address coordinates."
        return True, ok_msg, meta_out
    except sqlite3.IntegrityError:
        return False, "Ghost blocked — student_uid already verified (UNIQUE).", meta_out
    finally:
        conn.close()


def ward_verification_counts(db_path: Path | None = None) -> dict[str, int]:
    conn = _connect(db_path)
    try:
        rows = conn.execute(
            "SELECT ward_pcode, COUNT(*) AS n FROM verification_events GROUP BY ward_pcode"
        ).fetchall()
    finally:
        conn.close()
    out: dict[str, int] = {}
    for r in rows:
        k = str(r["ward_pcode"]).strip()
        if k:
            out[k] = int(r["n"])
    return out


def record_haraji_cdc_line(
    *,
    principal_id: str,
    ward_pcode: str,
    zazzau_district_id: str | None,
    naira_amount: float,
    levy_class: str,
    narrative: str = "",
    db_path: Path | None = None,
) -> tuple[bool, str]:
    pid = str(principal_id or "").strip()
    wp = str(ward_pcode or "").strip()
    if not pid or not wp:
        return False, "Haraji ledger blocked — principal_id and ward_pcode required."
    try:
        amt = float(naira_amount)
    except (TypeError, ValueError):
        return False, "Invalid naira_amount."
    if amt <= 0:
        return False, "Haraji / CDC amount must be positive."
    zd = str(zazzau_district_id or "").strip()
    lc = str(levy_class or "").strip() or "community_development"
    nar = str(narrative or "").strip()
    ts = time.time()
    conn = _connect(db_path)
    try:
        conn.execute(
            """
            INSERT INTO haraji_cdc_ledger
              (principal_id, ward_pcode, zazzau_district_id, naira_amount, levy_class, narrative, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (pid, wp, zd, amt, lc, nar, ts),
        )
        conn.commit()
    finally:
        conn.close()
    return True, f"Haraji-class CDC line recorded — ₦{amt:,.2f} · {lc}."


def haraji_cdc_recent_rows(
    limit: int = 40,
    *,
    db_path: Path | None = None,
) -> list[dict[str, Any]]:
    conn = _connect(db_path)
    try:
        rows = conn.execute(
            """
            SELECT principal_id, ward_pcode, zazzau_district_id, naira_amount, levy_class, narrative, created_at
            FROM haraji_cdc_ledger
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (int(limit),),
        ).fetchall()
    finally:
        conn.close()
    out: list[dict[str, Any]] = []
    for r in rows:
        out.append({k: r[k] for k in r.keys()})
    return out


def haraji_cdc_total_naira_for_principal(
    principal_id: str,
    *,
    db_path: Path | None = None,
) -> float:
    pid = str(principal_id or "").strip()
    if not pid:
        return 0.0
    conn = _connect(db_path)
    try:
        row = conn.execute(
            "SELECT COALESCE(SUM(naira_amount), 0) AS s FROM haraji_cdc_ledger WHERE principal_id = ?",
            (pid,),
        ).fetchone()
    finally:
        conn.close()
    return float(row["s"] if row else 0.0)


def verification_ledger_recent(
    limit: int = 35,
    *,
    db_path: Path | None = None,
) -> list[dict[str, Any]]:
    conn = _connect(db_path)
    try:
        rows = conn.execute(
            """
            SELECT student_uid, ward_pcode, principal_id, traditional_role, zazzau_district_id,
                   stranger_vetting_status, vetting_distance_km, nin, created_at
            FROM verification_events
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (int(limit),),
        ).fetchall()
    finally:
        conn.close()
    out: list[dict[str, Any]] = []
    for r in rows:
        out.append({k: r[k] for k in r.keys()})
    return out


def principal_jurisdiction_stats(
    principal_id: str,
    *,
    db_path: Path | None = None,
) -> dict[str, Any]:
    pid = str(principal_id).strip()
    if not pid:
        return {
            "verified_total": 0,
            "by_ward": {},
            "by_role": {},
            "me_anguwa_firewall_count": 0,
            "sovereign_clearance_status": (
                "STANDBY — awaiting Me Anguwa attestations on the AZK corridor"
            ),
            "recent_digest": None,
            "haraji_cdc_total_naira": 0.0,
        }
    conn = _connect(db_path)
    try:
        total = conn.execute(
            "SELECT COUNT(*) FROM verification_events WHERE principal_id = ?",
            (pid,),
        ).fetchone()[0]
        rows = conn.execute(
            """
            SELECT ward_pcode, COUNT(*) AS n
            FROM verification_events
            WHERE principal_id = ?
            GROUP BY ward_pcode
            ORDER BY n DESC
            """,
            (pid,),
        ).fetchall()
        last = conn.execute(
            "SELECT cert_digest FROM verification_events WHERE principal_id = ? ORDER BY created_at DESC LIMIT 1",
            (pid,),
        ).fetchone()
        role_rows = conn.execute(
            """
            SELECT traditional_role, COUNT(*) AS n
            FROM verification_events
            WHERE principal_id = ?
            GROUP BY traditional_role
            """,
            (pid,),
        ).fetchall()
        hj = conn.execute(
            "SELECT COALESCE(SUM(naira_amount), 0) AS s FROM haraji_cdc_ledger WHERE principal_id = ?",
            (pid,),
        ).fetchone()
        haraji_n = float(hj["s"] if hj else 0.0)
    finally:
        conn.close()
    by_ward = {str(r["ward_pcode"]): int(r["n"]) for r in rows}
    by_role = {str(r["traditional_role"]): int(r["n"]) for r in role_rows}
    ma_n = int(by_role.get("me_anguwa", 0))
    return {
        "verified_total": int(total),
        "by_ward": by_ward,
        "by_role": by_role,
        "me_anguwa_firewall_count": ma_n,
        "sovereign_clearance_status": (
            "OPERATIONAL — Village Head firewall engaged (Human API foreground)"
            if ma_n > 0
            else "STANDBY — awaiting Me Anguwa attestations on the AZK corridor"
        ),
        "recent_digest": str(last[0]) if last else None,
        "haraji_cdc_total_naira": haraji_n,
    }


def _norm_state_token(name: str) -> str:
    s = str(name or "").strip().lower()
    for suf in (" state", "state"):
        if s.endswith(suf):
            s = s[: -len(suf)].strip()
    return s


def leaderboard_for_state_wards(
    state_name_substring: str,
    *,
    wards_fc: dict | None,
    db_path: Path | None = None,
) -> list[tuple[str, str, str, int]]:
    """
    Returns sorted list of (ward_pcode, ward_name, lga_name, count) for wards in state.
    """
    counts = ward_verification_counts(db_path)
    if not wards_fc or not wards_fc.get("features"):
        return []
    needle = _norm_state_token(state_name_substring)
    rows: list[tuple[str, str, str, int]] = []
    for feat in wards_fc["features"]:
        p = feat.get("properties") or {}
        st_raw = str(p.get("ADM1_EN") or p.get("adm1_en") or "").strip()
        st_n = _norm_state_token(st_raw)
        if needle and needle not in st_n and st_n not in needle:
            continue
        wp = str(p.get("ADM3_PCODE") or p.get("adm3_pcode") or "").strip()
        if not wp:
            continue
        wname = str(p.get("ADM3_EN") or p.get("adm3_en") or "").strip()
        lga = str(p.get("ADM2_EN") or p.get("adm2_en") or "").strip()
        c = int(counts.get(wp, 0))
        if c > 0:
            rows.append((wp, wname, lga, c))
    rows.sort(key=lambda x: -x[3])
    return rows


def fetch_oauth_token() -> dict[str, Any]:
    """
    Client-credentials handshake. Env:
      DAPI_TOKEN_URL, DAPI_CLIENT_ID, DAPI_CLIENT_SECRET
    Returns dict with access_token (or empty), expires_at epoch, error message if any.
    """
    url = (os.environ.get("DAPI_TOKEN_URL") or "").strip()
    cid = (os.environ.get("DAPI_CLIENT_ID") or "").strip()
    csec = (os.environ.get("DAPI_CLIENT_SECRET") or "").strip()
    if not url or not cid or not csec:
        return {
            "access_token": "",
            "expires_at": 0.0,
            "token_type": "",
            "error": "DAPI_TOKEN_URL / DAPI_CLIENT_ID / DAPI_CLIENT_SECRET not set — demo/offline.",
        }
    try:
        r = requests.post(
            url,
            data={
                "grant_type": "client_credentials",
                "client_id": cid,
                "client_secret": csec,
            },
            timeout=45,
            headers={"Accept": "application/json"},
        )
        r.raise_for_status()
        blob = r.json()
        token = str(blob.get("access_token") or blob.get("token") or "")
        ttl = int(blob.get("expires_in") or blob.get("expires_in_seconds") or 3600)
        return {
            "access_token": token,
            "expires_at": time.time() + max(60, ttl),
            "token_type": str(blob.get("token_type") or "Bearer"),
            "error": "",
        }
    except Exception as exc:
        return {
            "access_token": "",
            "expires_at": 0.0,
            "token_type": "",
            "error": str(exc),
        }


def ensure_browser_session_id(session_dict: dict[str, Any]) -> str:
    key = "_dapi_browser_session_id"
    if key not in session_dict or not str(session_dict.get(key) or "").strip():
        session_dict[key] = str(uuid.uuid4())
    return str(session_dict[key])

