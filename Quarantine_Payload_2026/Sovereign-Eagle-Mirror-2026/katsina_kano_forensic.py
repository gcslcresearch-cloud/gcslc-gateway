"""
Katsina–Kano forensic injunction — statutory traditional chains only (GCSLC steel).

FORBIDDEN: proximity / geometry for emirate or traditional-domain assignment.
ALLOWED: Traditional statutory chain + chancellery-sealed LGA lists on the 774 lattice keys.
"""

from __future__ import annotations

import html
from typing import Any

from gcslc_deep_join import fetch_lga_catalog_raw

STATE_KT = "KT"
STATE_KN = "KN"

# --- Katsina / Daura Great Divide (774 catalogue orthography) ---
KATSINA_DAURA_STATUTORY_CORE_FIVE: tuple[str, ...] = (
    "Baure",
    "Daura",
    "Mai'Adua",
    "Sandamu",
    "Zango",  # Zangon Daura seat on statutory LGA row in this lattice
)

# Sixth Daura-cluster extension (774 lattice) — NOT Mai'Adua (Mai'Adua is core-five, not "the sixth").
KATSINA_DAURA_CLUSTER_SIXTH_LGA: str = "Mashi"

KATSINA_DAURA_CLUSTER_LGAS_SEALED: frozenset[str] = frozenset(
    tuple(KATSINA_DAURA_STATUTORY_CORE_FIVE) + (KATSINA_DAURA_CLUSTER_SIXTH_LGA,)
)

KATSINA_DAURA_CLUSTER_SIXTH_CHANCELLERY: dict[str, Any] = {
    "status": "PROVISIONAL_GCSLC_SEAL",
    "resolved_lga_lattice_name": KATSINA_DAURA_CLUSTER_SIXTH_LGA,
    "mai_adua_hierarchy": (
        "Mai'Adua is a peer anchor inside the statutory core-five Daura ring "
        "(Baure · Daura · Mai'Adua · Sandamu · Zango). It is not the sixth seat — "
        "the sixth extends the cluster per chancellery practice on the KT lattice."
    ),
    "sixth_hierarchy": (
        f"Mashi ({KATSINA_DAURA_CLUSTER_SIXTH_LGA}) carries the provisional sixth-node seal on the "
        "774 catalogue — replaces with gazette minute citation when palace publishes."
    ),
    "instruction": (
        "Forbidden: infer sixth from map proximity. Allowed: swap sixth string only when "
        "Emirate Chancellery minutes name an alternate KT row — maintain Mai'Adua core-five discipline."
    ),
}

KATSINA_EMIRATE_MANDATORY_LGAS: frozenset[str] = frozenset({"Ingawa", "Mani"})

# High-priority district nodes — Proponent audit benchmark (name mismatch = invalid row).
KATSINA_DISTRICT_HEAD_PRIORITY_NODES: tuple[dict[str, str], ...] = (
    {
        "node_id": "DH-MANI-01",
        "title": "District Head · Mani LGA",
        "lga_lattice": "Mani",
        "emirate_chain": "KATSINA_EMIRATE",
        "audit_benchmark_official_name": "Dr. Tukur Bello Ingawa",
        "audit_rule": "If incumbent display name ≠ benchmark, treat row as corrupt until reconciled.",
    },
    {
        "node_id": "MRK-KATSINA-01",
        "title": "Magajin Rafin Katsina",
        "lga_lattice": "Katsina",
        "emirate_chain": "KATSINA_EMIRATE",
        "audit_benchmark_official_name": "Magajin Rafin Katsina (title as sealed by chancellery)",
        "audit_rule": "Bind to Katsina LGA lattice + palace roster — not proximity.",
    },
)


def _norm_state(name: str) -> str:
    return str(name or "").strip().lower().replace("state", "").strip()


def is_katsina_state(name: str) -> bool:
    return _norm_state(name) == "katsina"


def is_kano_state(name: str) -> bool:
    return _norm_state(name) == "kano"


def _kt_lgas() -> frozenset[str]:
    raw = fetch_lga_catalog_raw()
    return frozenset(
        str(r.get("name") or "").strip()
        for r in raw
        if str(r.get("state_code") or "").upper() == STATE_KT
        if str(r.get("name") or "").strip()
    )


def katsina_statutory_emirate_chain(lga_lattice_name: str) -> str:
    """
    Return emirate chain key for KT LGA — statutory only (no proximity).
    """
    lg = str(lga_lattice_name or "").strip()
    if lg in KATSINA_DAURA_CLUSTER_LGAS_SEALED:
        return "DAURA_EMIRATE_CLUSTER"
    if lg in KATSINA_EMIRATE_MANDATORY_LGAS:
        return "KATSINA_EMIRATE"
    # All other KT LGAs default to Katsina Emirate umbrella unless chancellery publishes split.
    if lg in _kt_lgas():
        return "KATSINA_EMIRATE"
    return "UNKNOWN_LATTICE"


# --- Kano: Emir Aminu Ado Bayero metropolitan core (8 LGAs on 774 keys) ---
KANO_EMIR_METROPOLITAN_CORE_EIGHT: tuple[str, ...] = (
    "Kano Municipal",
    "Fagge",
    "Gwale",
    "Nasarawa",
    "Tarauni",
    "Dala",
    "Kumbotso",
    "Ungogo",
)

KANO_EMIR_EXCELLENCY = "His Royal Highness · Alhaji Aminu Ado Bayero · Emir of Kano"

KANO_STATE_COUNCIL_CHAIRMAN_METADATA: dict[str, str] = {
    "office": "Chairman · Kano State Council of Chiefs",
    "rotation_model": "Rotational",
    "notes": (
        "Chairmanship rotates among emirate council heads under current administrative practice — "
        "metadata must never be conflated with the metropolitan Emir core (8 LGAs) or the 44-LGA lattice."
    ),
}


def verify_kano_metropolitan_eight() -> None:
    kn = frozenset(
        str(r.get("name") or "").strip()
        for r in fetch_lga_catalog_raw()
        if str(r.get("state_code") or "").upper() == STATE_KN
        if str(r.get("name") or "").strip()
    )
    missing = [x for x in KANO_EMIR_METROPOLITAN_CORE_EIGHT if x not in kn]
    if missing:
        raise RuntimeError(f"Kano 8 verification failed — missing from 774 catalogue: {missing}")


def kano_forensic_mophi_glass_html() -> str:
    """Kano 44 lattice + Emir metropolitan core (8) + rotational council metadata — tooltips only."""
    verify_kano_metropolitan_eight()
    chair = KANO_STATE_COUNCIL_CHAIRMAN_METADATA
    core_list = ", ".join(KANO_EMIR_METROPOLITAN_CORE_EIGHT)
    tips = [
        (
            "Emir metropolitan core (8 LGAs)",
            f"{KANO_EMIR_EXCELLENCY} — lattice keys: {core_list}. "
            "Verified against gcslc KN catalogue; distinct from the 44-row administrative shell.",
        ),
        (
            chair["office"],
            f"Rotation model: {chair['rotation_model']}. {chair['notes']}",
        ),
    ]
    lis = []
    for label, tip in tips:
        lis.append(
            "<li><span class='kgec-mophi-glass-tip' "
            f"title=\"{html.escape(tip)}\">{html.escape(label)}</span></li>"
        )
    return (
        '<div class="kgec-kano-forensic-mophi" role="region" aria-label="Kano forensic tooltips">'
        "<p class='kgec-katsina-forensic-cap'>Kano forensic seal · 44 LGAs + Emir core (8) · hover for notes</p>"
        "<ul class='kgec-katsina-forensic-ul'>"
        + "".join(lis)
        + "</ul></div>"
    )


def katsina_forensic_mophi_glass_html() -> str:
    """
    Mophi Glass protocol — rivalry / divide notes live in native title tooltips (Goldman underline cue).
    """
    tips = [
        (
            "Katsina ↔ Daura divide",
            "Ingawa and Mani are HARD-WELDED to the Katsina Emirate by statutory chain — "
            "never re-route by geographic proximity to Daura.",
        ),
        (
            "Daura cluster (5 + sealed 6th)",
            "Core five: Baure, Daura, Mai'Adua, Sandamu, Zango (Zangon Daura). "
            "Sixth extension (provisional GCSLC seal): Mashi — Mai'Adua remains core-five (not the sixth). "
            "Replace sixth only with chancellery gazette naming.",
        ),
        (
            "District Head audit seal",
            "Mani node benchmark: Dr. Tukur Bello Ingawa — mismatch invalidates the row.",
        ),
    ]
    lis = []
    for label, tip in tips:
        lis.append(
            "<li><span class='kgec-mophi-glass-tip' "
            f"title=\"{html.escape(tip)}\">{html.escape(label)}</span></li>"
        )
    return (
        '<div class="kgec-katsina-forensic-mophi" role="region" aria-label="Katsina forensic tooltips">'
        "<p class='kgec-katsina-forensic-cap'>Katsina–Daura forensic seal · hover for rivalry notes (Mophi Glass)</p>"
        "<ul class='kgec-katsina-forensic-ul'>"
        + "".join(lis)
        + "</ul></div>"
    )


def katsina_forensic_payload() -> dict[str, Any]:
    """Embed into north_state_manifest KT block."""
    return {
        "guardrail": "FORBIDDEN: proximity_geometry_for_traditional_domain",
        "allowed": "traditional_statutory_chain_plus_chancellery_sealed_lists",
        "daura_cluster": {
            "statutory_core_five_lga": list(KATSINA_DAURA_STATUTORY_CORE_FIVE),
            "sixth_lga_lattice": KATSINA_DAURA_CLUSTER_SIXTH_LGA,
            "all_cluster_lgas_sealed": sorted(KATSINA_DAURA_CLUSTER_LGAS_SEALED),
            "sixth_chancellery_meta": KATSINA_DAURA_CLUSTER_SIXTH_CHANCELLERY,
        },
        "katsina_emirate_hard_weld": {
            "mandatory_katsina_pulse_lgas": sorted(KATSINA_EMIRATE_MANDATORY_LGAS),
            "note": "Ingawa & Mani — ancestral pulse with Katsina Emirate regardless of distance to Daura.",
        },
        "district_head_priority_nodes": list(KATSINA_DISTRICT_HEAD_PRIORITY_NODES),
    }


def kano_forensic_payload() -> dict[str, Any]:
    """Embed into north_state_manifest KN block."""
    verify_kano_metropolitan_eight()
    return {
        "lga_count_statutory": 44,
        "emir_metropolitan_core_eight": {
            "emir": KANO_EMIR_EXCELLENCY,
            "lga_lattice_names": list(KANO_EMIR_METROPOLITAN_CORE_EIGHT),
            "verification": "All eight names verified against gcslc_deep_join KN catalogue.",
        },
        "state_council_of_chiefs_chairman": KANO_STATE_COUNCIL_CHAIRMAN_METADATA,
    }
