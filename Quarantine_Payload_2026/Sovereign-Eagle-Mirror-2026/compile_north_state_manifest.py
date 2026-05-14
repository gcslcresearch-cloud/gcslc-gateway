#!/usr/bin/env python3
"""
Compile North-State Manifest (19 northern states) — apex traditional lattice ↔ 774 LGA domains.
LGA names are canonical from gcslc_deep_join.fetch_lga_catalog_raw() (same source as fused lattice).
"""

from __future__ import annotations

import json
from pathlib import Path

from gcslc_deep_join import STATE_CODE_TO_STATE, fetch_lga_catalog_raw

from katsina_kano_forensic import (
    kano_forensic_payload,
    katsina_forensic_payload,
    katsina_statutory_emirate_chain,
)

OUT = Path(__file__).resolve().parent / "north_state_manifest.json"

# Standard geopolitical North — 19 states (excludes Middle Belt contested definitions; FC not included).
NORTH_19_STATE_CODES: tuple[str, ...] = (
    "SO",  # Sokoto
    "KE",  # Kebbi
    "ZA",  # Zamfara
    "KT",  # Katsina
    "KN",  # Kano
    "JI",  # Jigawa
    "KD",  # Kaduna
    "BA",  # Bauchi
    "GO",  # Gombe
    "YO",  # Yobe
    "BO",  # Borno
    "AD",  # Adamawa
    "TA",  # Taraba
    "PL",  # Plateau
    "NI",  # Niger
    "KW",  # Kwara
    "KO",  # Kogi
    "BE",  # Benue
    "NA",  # Nasarawa
)

# Apex titles — documentary schema (chancellery titles vary; palace protocol is source of truth at runtime).
APEX_BY_STATE: dict[str, dict[str, str]] = {
    "SO": {"title": "Sultan of Sokoto", "traditional_order": "Sokoto Caliphate seat", "notes": "Spiritual & historical primacy — LGA domains are statutory 774, not caliphal boundary."},
    "KE": {"title": "Emir of Argungu", "traditional_order": "Kebbi traditional constellation", "notes": "Multiple emirate seats in-state; apex row is schema primary — sub-emirates via future child rows."},
    "ZA": {"title": "Emir of Anka", "traditional_order": "Zamfara emirate council", "notes": "Verify palace roster against statute — LGA list remains 774."},
    "KT": {"title": "Emir of Katsina", "traditional_order": "Katsina emirate", "notes": "Katsina vs Daura dual history — statutory LGAs 34 on 774 lattice."},
    "KN": {"title": "Emir of Kano", "traditional_order": "Kano Emirate", "notes": "Five-emirate statute vs single-emirate memory — overlay only (see northern_tier_research_audit)."},
    "JI": {"title": "Emir of Dutse", "traditional_order": "Jigawa emirate council", "notes": ""},
    "KD": {"title": "Emir of Zazzau", "traditional_order": "Zazzau Emirate", "notes": "Pilot sovereign bundle in repo — sub-district ledger separate from ADM2."},
    "BA": {"title": "Emir of Bauchi", "traditional_order": "Bauchi emirate", "notes": ""},
    "GO": {"title": "Emir of Gombe", "traditional_order": "Gombe emirate", "notes": ""},
    "YO": {"title": "Emir of Damaturu", "traditional_order": "Yobe traditional council", "notes": "Titular apex may be Pataskum el-Kanemi seat — confirm chancellery."},
    "BO": {"title": "Shehu of Borno", "traditional_order": "Borno Emirate", "notes": ""},
    "AD": {"title": "Lamido Adamawa", "traditional_order": "Adamawa Emirate", "notes": "Fombina historical lattice."},
    "TA": {"title": "Emir of Muri / Taraba mosaic", "traditional_order": "Taraba traditional tapestry", "notes": "Multiple chiefdoms — apex field is schema placeholder; split in v2."},
    "PL": {"title": "Gbong Gwom Jos", "traditional_order": "Plateau traditional council", "notes": "Multi-ethnic apex — LGA domains statutory."},
    "NI": {"title": "Emir of Minna", "traditional_order": "Niger traditional council", "notes": ""},
    "KW": {"title": "Emir of Ilorin", "traditional_order": "Ilorin Emirate", "notes": ""},
    "KO": {"title": "Attah Igala / Ohinoyi", "traditional_order": "Kogi traditional tapestry", "notes": "Multiple historic seats — schema primary is composite label."},
    "BE": {"title": "Tor Tiv", "traditional_order": "Tiv traditional authority", "notes": ""},
    "NA": {"title": "Emir of Lafia", "traditional_order": "Nasarawa emirate", "notes": ""},
}


def main() -> None:
    raw = fetch_lga_catalog_raw()
    by_state: dict[str, list[str]] = {}
    for r in raw:
        sc = str(r.get("state_code") or "").upper().strip()
        name = str(r.get("name") or "").strip()
        if not sc or not name:
            continue
        by_state.setdefault(sc, []).append(name)
    for k in by_state:
        by_state[k] = sorted(set(by_state[k]))

    states_out: list[dict[str, object]] = []
    for code in NORTH_19_STATE_CODES:
        lgas = by_state.get(code, [])
        apex = APEX_BY_STATE.get(code, {}).copy()
        lga_domains: list[dict[str, str]] = []
        for lg in lgas:
            dom: dict[str, str] = {
                "lga_lattice_name": lg,
                "lga_id_note": "Resolved at runtime via ADM2 + 774 fused row key = (state_code, name)",
            }
            if code == "KT":
                dom["statutory_emirate_chain"] = katsina_statutory_emirate_chain(lg)
            lga_domains.append(dom)
        row: dict[str, object] = {
            "state_code": code,
            "state_en": STATE_CODE_TO_STATE.get(code, code),
            "apex_traditional": apex,
            "lga_domains": lga_domains,
            "lga_count": len(lgas),
        }
        if code == "KT":
            row["forensic_injunction_overlay"] = katsina_forensic_payload()
        elif code == "KN":
            row["forensic_injunction_overlay"] = kano_forensic_payload()
        states_out.append(row)

    total_lgas = sum(s["lga_count"] for s in states_out)
    manifest = {
        "manifest_version": "1.0.0",
        "lattice_source": "gcslc_deep_join.fetch_lga_catalog_raw — hard-wired to 774 national cardinality",
        "north_state_count": len(NORTH_19_STATE_CODES),
        "north_lga_row_count": total_lgas,
        "schema_notes": {
            "apex_traditional": "Sovereign narrative row — does not replace statutory government.",
            "lga_domains": "Every name matches catalogue exactly; spine weld uses ADM2_EN alignment + pcode from HDX/geoBoundaries.",
            "friction": "Emirate splits / five-seat Kano overlays live in parallel JSON (northern_tier_research_audit), never in LGA renames.",
            "forensic_injunction_overlay": "KT/KN only — chancellery-first traditional chains; Kano 8 + rotational council metadata; no proximity geometry for emirate assignment.",
        },
        "states": states_out,
    }
    OUT.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} — {len(states_out)} states, {total_lgas} LGAs (north sum).")


if __name__ == "__main__":
    main()
