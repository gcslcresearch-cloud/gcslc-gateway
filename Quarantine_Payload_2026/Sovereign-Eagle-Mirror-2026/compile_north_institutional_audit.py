#!/usr/bin/env python3
"""
North institutional audit — NUC / NBTE / NCCE rows hard-weld to 774 LGA name keys.
Each row: regulator, institution, state_code, primary_campus_lga must match catalogue LGA string exactly.
Completeness: Phase-1 verified seed; import NUC/NBTE/NCCE bulk sheets to grow without breaking lattice.
"""

from __future__ import annotations

import json
from pathlib import Path

from gcslc_deep_join import STATE_CODE_TO_STATE, fetch_lga_catalog_raw

OUT = Path(__file__).resolve().parent / "north_institutional_audit.json"
NORTH_19 = (
    "SO", "KE", "ZA", "KT", "KN", "JI", "KD", "BA", "GO", "YO", "BO", "AD", "TA", "PL", "NI", "KW", "KO", "BE", "NA"
)

# --- Seed: (institution_name, regulator, state_code, lga_lattice_name, abbr_optional) ---
# LGA strings MUST match gcslc_deep_join catalogue exactly (case-sensitive).
SEED: tuple[tuple[str, str, str, str, str], ...] = (
    # Kaduna pilot (repo truth)
    ("Ahmadu Bello University", "NUC", "KD", "Sabon Gari", "ABU"),
    ("Kaduna State University", "NUC", "KD", "Kaduna North", "KASU"),
    ("Nigerian Defence Academy", "NUC", "KD", "Chikun", "NDA"),
    ("Federal University of Education Zaria", "NUC", "KD", "Zaria", "FUE Zaria"),
    ("Nigerian College of Aviation Technology", "NBTE", "KD", "Zaria", "NCAT"),
    ("Kaduna Polytechnic", "NBTE", "KD", "Kaduna South", "KADPOLY"),
    ("Nuhu Bamalli Polytechnic · Main Campus · Zaria", "NBTE", "KD", "Zaria", "NUBA-Zaria"),
    ("Nuhu Bamalli Polytechnic · Kafanchan Campus", "NBTE", "KD", "Jema'a", "NUBA-Kafanchan"),
    # Kano
    ("Bayero University Kano", "NUC", "KN", "Gwale", "BUK"),
    ("Kano University of Science and Technology", "NUC", "KN", "Wudil", "KUST"),
    ("Kano State Polytechnic", "NBTE", "KN", "Kano Municipal", "KSP"),
    ("Federal College of Education Kano", "NCCE", "KN", "Kumbotso", "FCET Kano"),
    # Katsina / Jigawa / Zamfara / Sokoto / Kebbi
    ("Umaru Musa Yar'adua University", "NUC", "KT", "Katsina", "UMYU"),
    ("Hassan Usman Katsina Polytechnic", "NBTE", "KT", "Katsina", "HUK Poly"),
    ("Federal University Dutsin-Ma", "NUC", "KT", "Dutsin Ma", "FUDMA"),
    ("Federal University Dutse", "NUC", "JI", "Dutse", "FUD"),
    ("Federal University Gusau", "NUC", "ZA", "Gusau", "FUGUS"),
    ("Sokoto State University", "NUC", "SO", "Sokoto North", "SSU"),
    ("Umaru Ali Shinkafi Polytechnic Sokoto", "NBTE", "SO", "Sokoto South", "UAS Poly"),
    ("Kebbi State University of Science and Technology", "NUC", "KE", "Aleiro", "KSUSTA"),
    # Bauchi / Gombe / Yobe / Borno / Adamawa
    ("Abubakar Tafawa Balewa University", "NUC", "BA", "Bauchi", "ATBU"),
    ("Federal Polytechnic Bauchi", "NBTE", "BA", "Bauchi", "FPT Bauchi"),
    ("Gombe State University", "NUC", "GO", "Gombe", "GSU"),
    ("Federal University Kashere", "NUC", "GO", "Akko", "FUKashere"),
    ("Yobe State University", "NUC", "YO", "Damaturu", "YSU"),
    ("University of Maiduguri", "NUC", "BO", "Maiduguri", "UNIMAID"),
    ("Modibbo Adama University of Technology", "NUC", "AD", "Yola North", "MAUTECH"),
    ("Adamawa State University Mubi", "NUC", "AD", "Mubi North", "ADSU"),
    # Niger / Nasarawa / Plateau / Taraba / Kwara / Kogi / Benue
    ("Federal University of Technology Minna", "NUC", "NI", "Chanchaga", "FUTMINNA"),
    ("Niger State Polytechnic", "NBTE", "NI", "Bida", "NSP"),
    ("Federal University Lafia", "NUC", "NA", "Lafia", "FULafia"),
    ("Nasarawa State University Keffi", "NUC", "NA", "Keffi", "NSUK"),
    ("Federal Polytechnic Nasarawa", "NBTE", "NA", "Nasarawa", "FP Nasarawa"),
    ("Federal College of Education Langtang", "NCCE", "PL", "Langtang North", "FCET Langtang"),
    ("University of Jos", "NUC", "PL", "Jos North", "UNIJOS"),
    ("Plateau State University Bokkos", "NUC", "PL", "Bokkos", "PLASU"),
    ("Taraba State University", "NUC", "TA", "Jalingo", "TSU"),
    ("Federal University Wukari", "NUC", "TA", "Wukari", "FUWukari"),
    ("University of Ilorin", "NUC", "KW", "Ilorin South", "UNILORIN"),
    ("Kwara State Polytechnic", "NBTE", "KW", "Ilorin West", "KWARA POLY"),
    ("Federal Polytechnic Offa", "NBTE", "KW", "Offa", "FP Offa"),
    ("Federal University Lokoja", "NUC", "KO", "Lokoja", "FUL"),
    ("Kogi State University", "NUC", "KO", "Dekina", "KSU"),
    ("Benue State University", "NUC", "BE", "Markudi", "BSU"),
    ("Joseph Sarwuan Tarka University Makurdi", "NUC", "BE", "Markudi", "JOSTUM"),
    ("Federal Polytechnic Idah", "NBTE", "KO", "Idah", "FP Idah"),
)


def _lga_sets() -> dict[str, set[str]]:
    raw = fetch_lga_catalog_raw()
    by: dict[str, set[str]] = {}
    for r in raw:
        sc = str(r.get("state_code") or "").upper().strip()
        name = str(r.get("name") or "").strip()
        if sc and name:
            by.setdefault(sc, set()).add(name)
    return by


def main() -> None:
    lgas = _lga_sets()
    rows: list[dict[str, object]] = []
    errors: list[str] = []
    for name, reg, sc, lga, abbr in SEED:
        if sc not in NORTH_19:
            errors.append(f"{name}: state {sc} not in North-19 manifest")
            continue
        bucket = lgas.get(sc, set())
        if lga not in bucket:
            errors.append(f"{name}: LGA `{lga}` not in 774 catalogue for {sc}")
            ok = False
        else:
            ok = True
        rows.append(
            {
                "abbreviation": abbr,
                "institution": name,
                "regulator": reg,
                "state_code": sc,
                "state_en": STATE_CODE_TO_STATE.get(sc, sc),
                "primary_campus_lga_lattice": lga,
                "lga_774_verified": ok,
                "lattice_key": f"{sc}:{lga}",
            }
        )
    audit = {
        "audit_version": "1.0.0",
        "lattice_source": "gcslc_deep_join.fetch_lga_catalog_raw",
        "north_state_codes": list(NORTH_19),
        "completeness_note": (
            "Phase-1 seed: representative NUC/NBTE/NCCE institutions across all 19 north states; "
            "every row is machine-checked against exact LGA orthography. "
            "Full national enumeration requires regulator bulk ingest (XLS/API) — append rows, "
            "re-run this compiler to verify LGA keys before merge."
        ),
        "seed_count": len(rows),
        "rows": sorted(rows, key=lambda x: (str(x["regulator"]), str(x["state_code"]), str(x["institution"]))),
        "compile_errors": errors,
    }
    OUT.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} — {len(rows)} rows, {len(errors)} lattice errors.")
    if errors:
        for e in errors[:20]:
            print("  ERR:", e)
        if len(errors) > 20:
            print("  ...")


if __name__ == "__main__":
    main()
