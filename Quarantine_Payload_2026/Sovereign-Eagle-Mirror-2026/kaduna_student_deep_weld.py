"""
Kaduna pilot deep-weld — notional student mass → Zazzau-31 district keys + Me Anguwa overload signals.

Ward overload uses DAPI verification counts vs configurable thresholds (Rigasa stricter by mandate).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
_DEEP_JSON = BASE_DIR / "Part_04_Social" / "data" / "kaduna_pilot_student_deep_weld.json"


def load_kaduna_student_deep_weld() -> dict[str, Any]:
    try:
        return json.loads(_DEEP_JSON.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}


def _nuba_row_from_config(cfg: dict[str, Any]) -> dict[str, Any] | None:
    for row in cfg.get("institutions") or []:
        if str(row.get("abbr") or "").strip().upper() == "NUBA":
            return dict(row)
    return None


def nuba_enrolment_split_lines(cfg: dict[str, Any] | None = None) -> tuple[str, str, int, int, int]:
    """
    Return (zaria_caption, kafanchan_caption, total_nuba_heads, zaria_n, kafanchan_n) from campus_enrolments.
    """
    raw = cfg if cfg is not None else load_kaduna_student_deep_weld()
    row = _nuba_row_from_config(raw) or {}
    camps = list(row.get("campus_enrolments") or [])
    z_n = k_n = 0
    z_lbl = ""
    k_lbl = ""
    for c in camps:
        lab = str(c.get("campus_label") or "")
        try:
            n = int(c.get("notional_students_2025_26") or 0)
        except (TypeError, ValueError):
            n = 0
        low = lab.lower()
        if "kafanchan" in low:
            k_n = n
            k_lbl = lab.strip() or "Kafanchan Campus"
        else:
            z_n += n
            if not z_lbl and lab:
                z_lbl = lab.strip()
    if not z_lbl:
        z_lbl = "Main Campus · Zaria (HQ)"
    if not k_lbl:
        k_lbl = "Kafanchan Campus"
    total = z_n + k_n
    z_line = f"NUBA · {z_lbl} · {z_n:,} (2025–26 notional)"
    k_anchor = str(raw.get("kafanchan_district_anchor_en") or "").strip()
    k_tail = f" · {k_anchor}" if k_anchor else " · Kafanchan · Jema'a LGA · Jema'a Emirate"
    k_line = f"NUBA · {k_lbl} · {k_n:,} (2025–26 notional){k_tail}"
    return z_line, k_line, total, z_n, k_n


def nuba_campus_inference_text() -> str:
    """
    NUBA Zaria vs Kafanchan split + Me Anguwa pressure logic — one clean string for DAPI captions.

    Always derives enrolment figures from JSON campus rows when present; appends chancellery-style
    inference prose from `nuba_me_anguwa_inference` when non-empty.
    """
    cfg = load_kaduna_student_deep_weld()
    z_line, k_line, total, _zn, _kn = nuba_enrolment_split_lines(cfg)
    prose = str(cfg.get("nuba_me_anguwa_inference") or "").strip()
    head = f"Nuhu Bamalli Polytechnic (NUBA) — notional headcount {total:,} (cycle {cfg.get('academic_cycle') or '2025–2026'}): {z_line}; {k_line}."
    if prose:
        return f"{head} Pressure logic: {prose}"
    return head


def nuba_for_pulse_tooltip() -> str:
    """Short hover line for Live Student Pulse strip — no layout HTML (Mophi title attribute safe)."""
    cfg = load_kaduna_student_deep_weld()
    z_line, k_line, total, z_n, k_n = nuba_enrolment_split_lines(cfg)
    return (
        f"NUBA (Nuhu Bamalli Polytechnic) pilot notional {total:,} "
        f"(Zaria {z_n:,} · Kafanchan {k_n:,}) — {z_line}; {k_line}."
    )


def compute_ward_overload_wpcodes(
    verify_counts: dict[str, int],
    *,
    rigasa_ward_pcode: str | None,
    default_threshold: int | None = None,
    rigasa_threshold: int | None = None,
) -> frozenset[str]:
    """Return ward_pcode keys whose verification totals exceed Me Anguwa-safe thresholds."""
    cfg = load_kaduna_student_deep_weld()
    d_thr = int(cfg.get("default_verification_overload_threshold") or 650) if default_threshold is None else int(default_threshold)
    r_thr = int(cfg.get("rigasa_verification_overload_threshold") or 2200) if rigasa_threshold is None else int(rigasa_threshold)
    out: set[str] = set()
    rig = str(rigasa_ward_pcode or "").strip()
    for wp, raw in (verify_counts or {}).items():
        try:
            c = int(raw)
        except (TypeError, ValueError):
            continue
        thr = r_thr if rig and str(wp).strip() == rig else d_thr
        if c >= thr:
            out.add(str(wp).strip())
    return frozenset(out)


def kaduna_me_anguwa_pressure_summary(
    verify_counts: dict[str, int],
    *,
    rigasa_ward_pcode: str | None,
) -> dict[str, Any]:
    """
    Student-to-Me-Anguwa style ratio for pilot districts (proxy + live verifications on Rigasa spine).
    """
    cfg = load_kaduna_student_deep_weld()
    inst = cfg.get("institutions") or []
    total_students = 0
    for x in inst:
        try:
            total_students += int(x.get("notional_students_2025_26") or 0)
        except (TypeError, ValueError):
            pass
        for c in x.get("campus_enrolments", []) or []:
            try:
                total_students += int(c.get("notional_students_2025_26") or 0)
            except (TypeError, ValueError):
                pass
    zd_rows = list(cfg.get("district_student_proxy") or [])
    zd22 = next((z for z in zd_rows if str(z.get("zazzau_district_id") or "") == "ZD22"), None)
    rig = str(rigasa_ward_pcode or "").strip()
    rv = int(verify_counts.get(rig, 0)) if rig else 0
    heads = int(zd22.get("me_anguwa_heads_assumed") or 1) if isinstance(zd22, dict) else 1
    stud = int(zd22.get("notional_students_proxy") or 0) if isinstance(zd22, dict) else 0
    verif_per_head = rv / float(max(heads, 1))
    stud_per_head = stud / float(max(heads, 1))
    overloaded = bool(rig) and rig in compute_ward_overload_wpcodes(
        verify_counts, rigasa_ward_pcode=rigasa_ward_pcode
    )
    return {
        "kaduna_notional_students_institutions_sum": total_students,
        "zd22_rigasa_verifications": rv,
        "zd22_me_anguwa_heads_assumed": heads,
        "zd22_notional_students_proxy": stud,
        "zd22_verifications_per_me_anguwa": round(verif_per_head, 2),
        "zd22_students_per_me_anguwa_proxy": round(stud_per_head, 2),
        "zd22_overloaded": overloaded,
        "copy_line": (
            f"ZD22 Rigasa proxy · {stud:,} notional students / {heads} Me Anguwa heads ≈ {stud_per_head:,.0f} · "
            f"{rv:,} live verifications on spine ward → {verif_per_head:,.1f} verifs / head"
            + (" · OVERLOAD" if overloaded else "")
        ),
    }


__all__ = [
    "load_kaduna_student_deep_weld",
    "nuba_campus_inference_text",
    "nuba_enrolment_split_lines",
    "nuba_for_pulse_tooltip",
    "compute_ward_overload_wpcodes",
    "kaduna_me_anguwa_pressure_summary",
]
