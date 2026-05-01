"""
Nigeria federation connectivity spine — State ↔ LGA ↔ Ward join (Phase 2).
Sources: geoBoundaries (ADM1/ADM2) + HDX UN OCHA COD nga_admin boundaries bundle.
Validated row counts mirror INEC / operational ward inventory (774 LGAs · 8806 wards · 37 states+FCT).
"""

from __future__ import annotations

import io
import json
import zipfile
from typing import Any

import pandas as pd
import requests


GEOBOUNDARIES_API_NGA_ADM2 = (
    "https://www.geoboundaries.org/api/current/gbOpen/NGA/ADM2/"
)

HDX_NGA_ADMIN_GEOJSON_ZIP = (
    "https://data.humdata.org/dataset/81ac1d38-f603-4a98-804d-325c658599a3/resource/"
    "7e30ec96-7f29-4ee8-9f4c-77633b353cbb/download/nga_admin_boundaries.geojson.zip"
)

EXP_STATES_PLUS_FCT = 37
EXP_LGAS = 774
EXP_WARDS = 8806


def _http_get_binary(url: str, timeout: int = 240) -> bytes | None:
    try:
        r = requests.get(
            url,
            timeout=timeout,
            headers={"User-Agent": "Mozilla/5.0 GCSLC-Sovereign-Mirror"},
        )
        r.raise_for_status()
        return r.content
    except Exception:
        return None


def fetch_geo_boundary_geojson(meta_api_url: str) -> dict | None:
    try:
        meta = requests.get(meta_api_url, timeout=45).json()
        gj_url = meta.get("gjDownloadURL")
        if not gj_url:
            return None
        r = requests.get(gj_url, timeout=240, allow_redirects=True)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def _classify_boundary_fc(fc: dict) -> str:
    """Heuristic COD layer typing by row count (+/- tolerance)."""
    n = len(fc.get("features") or [])
    if abs(n - EXP_WARDS) <= 220:
        return "wards"
    if abs(n - EXP_LGAS) <= 8:
        return "lgas"
    if abs(n - EXP_STATES_PLUS_FCT) <= 6:
        return "states"
    return "unknown"


def load_hdx_nga_geojson_zip_layers() -> dict[str, dict | None]:
    """
    Downloads HDX nga_admin_boundaries.geojson.zip and resolves State / LGA / Ward FCs.
    Some builds ship one GeoJSON per level; others aggregate — we classify by count.
    Returns keys: states, lgas, wards (values may be None if unavailable).
    """
    blob = _http_get_binary(HDX_NGA_ADMIN_GEOJSON_ZIP)
    if not blob:
        return {"states": None, "lgas": None, "wards": None}

    out: dict[str, dict | None] = {"states": None, "lgas": None, "wards": None}
    assigned: dict[str, int] = {"wards": EXP_WARDS, "lgas": EXP_LGAS, "states": EXP_STATES_PLUS_FCT}

    try:
        zf = zipfile.ZipFile(io.BytesIO(blob))
    except zipfile.BadZipFile:
        return out

    for name in zf.namelist():
        if not name.lower().endswith(".geojson"):
            continue
        try:
            raw = zf.read(name).decode("utf-8")
            fc = json.loads(raw)
        except Exception:
            continue
        if not fc.get("type") == "FeatureCollection":
            continue
        kind = _classify_boundary_fc(fc)
        if kind in out and out[kind] is None:
            out[kind] = fc
            continue
        # If multiple geojson files match same bucket, prefer closest count delta
        if kind != "unknown" and kind in assigned:
            best = out[kind]
            if best is None:
                out[kind] = fc
            else:
                cur_best = len(best.get("features") or [])
                new_n = len(fc.get("features") or [])
                if abs(new_n - assigned[kind]) < abs(cur_best - assigned[kind]):
                    out[kind] = fc
    # Single consolidated file fallback: classify whole bundle
    if not any(out.values()):
        candidates: list[tuple[int, dict]] = []
        for name in zf.namelist():
            if not name.lower().endswith(".geojson"):
                continue
            try:
                raw = zf.read(name).decode("utf-8")
                fc = json.loads(raw)
            except Exception:
                continue
            if fc.get("type") != "FeatureCollection":
                continue
            kind = _classify_boundary_fc(fc)
            if kind != "unknown":
                candidates.append((len(fc["features"]), fc))
        if candidates:
            _, fc_pick = sorted(candidates, key=lambda x: abs(x[0] - EXP_WARDS))[0]
            out[_classify_boundary_fc(fc_pick)] = fc_pick
    return out


def _ward_row_from_properties(p: dict[str, Any]) -> dict[str, Any]:
    def pick(keys: tuple[str, ...]) -> tuple[str | None, Any]:
        for k in keys:
            if k in p and p[k] not in (None, ""):
                return k, p[k]
        return None, None

    _, st_c = pick(("ADM1_PCODE", "adm1_pcode", "ADM1_PC", "STA_CODE"))
    _, st_n = pick(("ADM1_EN", "adm1_en", "ADM1_REF", "STATENAME"))
    _, lga_c = pick(("ADM2_PCODE", "adm2_pcode", "ADM2_PC", "LGA_CODE"))
    _, lga_n = pick(("ADM2_EN", "adm2_en", "ADM2_REF", "LGA_NAME"))
    _, wd_c = pick(("ADM3_PCODE", "adm3_pcode", "WARD PCODE", "WARD_PCODE"))
    _, wd_n = pick(("ADM3_EN", "adm3_en", "WARD", "WARD_NAME"))
    return {
        "state_pcode": str(st_c).strip() if st_c is not None else "",
        "state_name": str(st_n).strip() if st_n is not None else "",
        "lga_pcode": str(lga_c).strip() if lga_c is not None else "",
        "lga_name": str(lga_n).strip() if lga_n is not None else "",
        "ward_pcode": str(wd_c).strip() if wd_c is not None else "",
        "ward_name": str(wd_n).strip() if wd_n is not None else "",
    }


def build_forensic_spine_table(wards_fc: dict | None) -> tuple[pd.DataFrame, dict[str, Any]]:
    """One row per ward; validates duplicate ward codes & LGA cardinality."""
    report: dict[str, Any] = {
        "ward_rows": 0,
        "expected_wards": EXP_WARDS,
        "distinct_lgas": None,
        "distinct_states": None,
        "ward_pcode_dupes": 0,
        "valid": False,
        "notes": [],
    }

    if not wards_fc or not wards_fc.get("features"):
        return pd.DataFrame(), report

    rows = []
    for f in wards_fc["features"]:
        p = f.get("properties") or {}
        rows.append(_ward_row_from_properties(p))

    df = pd.DataFrame(rows)
    report["ward_rows"] = len(df)
    nonempty = df[df["ward_pcode"].str.len() > 0].copy()
    dup = (
        int(nonempty["ward_pcode"].duplicated().sum()) if len(nonempty) else 0
    )
    report["ward_pcode_dupes"] = dup
    if len(nonempty) == 0:
        report["distinct_lgas"] = 0
        report["distinct_states"] = 0
        report["notes"].append("No ward pcode fields parsed — check COD attribute names.")
        return df, report

    report["distinct_lgas"] = int(nonempty.groupby(["state_pcode", "lga_pcode"]).ngroups)
    report["distinct_states"] = int(nonempty["state_pcode"].nunique())

    if abs(len(nonempty) - EXP_WARDS) <= 240 and dup == 0:
        report["valid"] = True
    else:
        report["notes"].append(
            f"Ward cardinality {len(nonempty)} ≠ target {EXP_WARDS} ±240 or pcode dupes detected."
        )
    short_pc = nonempty["ward_pcode"].str.len().lt(4)
    if short_pc.any():
        report["notes"].append(
            "Some ward pcode fields look malformed — inspect COD aliases."
        )

    dl = int(report["distinct_lgas"]) if report["distinct_lgas"] is not None else 0
    if abs(dl - EXP_LGAS) > 35:
        report["notes"].append(f"Distinct LGAs counted {dl}; expected ~{EXP_LGAS}.")
        report["valid"] = False
    elif report["valid"]:
        report["valid"] = True

    return df, report


def prefer_hdx_or_geo_lga_geojson(
    lgas_hdx: dict | None, lgas_gb: dict | None
) -> dict | None:
    """Prefer HDX (COD) LGA geometries when cardinality matches (~774); else geoBoundaries ADM2."""
    for fc in (lgas_hdx, lgas_gb):
        if fc and fc.get("features"):
            n = len(fc["features"])
            if abs(n - EXP_LGAS) <= 40:
                return fc
    for fc in (lgas_hdx, lgas_gb):
        if fc and fc.get("features"):
            return fc
    return None
