"""
Kaduna State sovereign operational pilot — institutional weld + Zazzau ancestral ledger.
31 district nodes under 11 LGAs (Galadiman Ruwa bundle); ward spine = HDX attributes.
"""

from __future__ import annotations

import html
from typing import Any

import pandas as pd

STATE_MATCH = "kaduna"

# Security Proximity Tag (SPT) — frontier LGAs where lattice mismatch escalates to District Head.
KADUNA_SPT_FRONTIER_LGA_EN: frozenset[str] = frozenset(
    {"Birnin Gwari", "Giwa", "Chikun", "Kajuru"}
)


def normalize_lga_key(name: str) -> str:
    return " ".join(str(name or "").strip().lower().split())


def normalize_state_name(name: str) -> str:
    return str(name or "").strip().lower().replace("state", "").strip()


def is_kaduna_state(name: str) -> bool:
    return normalize_state_name(name) == STATE_MATCH


# Eleven LGAs — Zazzau pilot lattice (ADM2_EN keys for HDX spine weld).
ZAZZAU_ELEVEN_LGA_EN: tuple[str, ...] = (
    "Zaria",
    "Sabon Gari",
    "Soba",
    "Ikara",
    "Kudan",
    "Makarfi",
    "Giwa",
    "Kaduna North",
    "Kaduna South",
    "Igabi",
    "Kubau",
)
ZAZZAU_ELEVEN_SOURCE_NOTE = (
    "Galadiman Ruwa eleven-LGA bundle — ADM2_PCODE from live 774 ward spine; "
    "31 ancestral districts below are pilot ledger nodes under Me Anguwa attribution."
)

# Thirty-one ancestral districts — beneath LGA; stable IDs for DAPI weld (ZD01–ZD31).
ZAZZAU_THIRTY_ONE_DISTRICTS: tuple[dict[str, str], ...] = (
    {"district_id": "ZD01", "district_en": "Birni da kewaye", "parent_lga_en": "Zaria"},
    {"district_id": "ZD02", "district_en": "Hanwa", "parent_lga_en": "Zaria"},
    {"district_id": "ZD03", "district_en": "Gyellesu", "parent_lga_en": "Zaria"},
    {"district_id": "ZD04", "district_en": "Basawa", "parent_lga_en": "Zaria"},
    {"district_id": "ZD05", "district_en": "Turaki Uku", "parent_lga_en": "Zaria"},
    {"district_id": "ZD06", "district_en": "Anguwan Fatika", "parent_lga_en": "Zaria"},
    {"district_id": "ZD07", "district_en": "Shika", "parent_lga_en": "Sabon Gari"},
    {"district_id": "ZD08", "district_en": "Panbeguwa", "parent_lga_en": "Sabon Gari"},
    {"district_id": "ZD09", "district_en": "Samaru belt", "parent_lga_en": "Sabon Gari"},
    {"district_id": "ZD10", "district_en": "Wusasa ring", "parent_lga_en": "Sabon Gari"},
    {"district_id": "ZD11", "district_en": "Giwa urban", "parent_lga_en": "Giwa"},
    {"district_id": "ZD12", "district_en": "Gangimi", "parent_lga_en": "Giwa"},
    {"district_id": "ZD13", "district_en": "Kakangi", "parent_lga_en": "Giwa"},
    {"district_id": "ZD14", "district_en": "Anchau", "parent_lga_en": "Soba"},
    {"district_id": "ZD15", "district_en": "Maigana corridor", "parent_lga_en": "Soba"},
    {"district_id": "ZD16", "district_en": "Ikara central", "parent_lga_en": "Ikara"},
    {"district_id": "ZD17", "district_en": "Pali cluster", "parent_lga_en": "Ikara"},
    {"district_id": "ZD18", "district_en": "Kudan urban", "parent_lga_en": "Kudan"},
    {"district_id": "ZD19", "district_en": "Lilia fringe", "parent_lga_en": "Kudan"},
    {"district_id": "ZD20", "district_en": "Makarfi urban", "parent_lga_en": "Makarfi"},
    {"district_id": "ZD21", "district_en": "Munbir axis", "parent_lga_en": "Makarfi"},
    {"district_id": "ZD22", "district_en": "Rigasa", "parent_lga_en": "Igabi"},
    {"district_id": "ZD23", "district_en": "Narayi", "parent_lga_en": "Igabi"},
    {"district_id": "ZD24", "district_en": "Kubau urban", "parent_lga_en": "Kubau"},
    {"district_id": "ZD25", "district_en": "Kwassallo", "parent_lga_en": "Kubau"},
    {"district_id": "ZD26", "district_en": "Doka", "parent_lga_en": "Kaduna North"},
    {"district_id": "ZD27", "district_en": "Kawo", "parent_lga_en": "Kaduna North"},
    {"district_id": "ZD28", "district_en": "Badarawa", "parent_lga_en": "Kaduna North"},
    {"district_id": "ZD29", "district_en": "Barnawa", "parent_lga_en": "Kaduna South"},
    {"district_id": "ZD30", "district_en": "Kakuri", "parent_lga_en": "Kaduna South"},
    {"district_id": "ZD31", "district_en": "Makera", "parent_lga_en": "Kaduna South"},
)

DISTRICT_LEDGER_NOTE = (
    "Pilot ancestral ledger — chancellery may rename/re-split nodes; IDs remain stable for DAPI routing."
)


def _zazzau_district_geo_anchors() -> dict[str, tuple[float, float]]:
    """
    Pilot WGS84 anchors per ZD node — NIN / address distance vetting vs declared district.
    Coarse LGA-centered offsets (not survey-grade); sufficient for stranger-vetting simulation.
    """
    _lga_base: dict[str, tuple[float, float]] = {
        "Zaria": (11.1115, 7.7227),
        "Sabon Gari": (11.075, 7.708),
        "Giwa": (11.31, 7.44),
        "Soba": (10.98, 8.15),
        "Ikara": (11.18, 8.02),
        "Kudan": (11.24, 7.61),
        "Makarfi": (11.04, 7.87),
        "Kaduna North": (10.596, 7.442),
        "Kaduna South": (10.518, 7.438),
        "Igabi": (10.79, 7.40),
        "Kubau": (11.25, 7.52),
    }
    out: dict[str, tuple[float, float]] = {}
    for i, row in enumerate(ZAZZAU_THIRTY_ONE_DISTRICTS):
        did = row["district_id"]
        lg = row["parent_lga_en"]
        lat0, lon0 = _lga_base.get(lg, (10.6, 7.44))
        lat = lat0 + (i % 7) * 0.004 - 0.012
        lon = lon0 + (i % 5) * 0.004 - 0.008
        out[did] = (round(lat, 6), round(lon, 6))
    return out


# Immutable lookup — stranger vetting distance vs NIN / claimed address coordinates.
# GUARDRAIL: these anchors are for Kaduna pilot SPT / address simulation only — they MUST NOT
# drive emirate or traditional-domain assignment elsewhere (e.g. Katsina vs Daura chains use chancellery, not proximity).
ZAZZAU_DISTRICT_GEO_ANCHORS: dict[str, tuple[float, float]] = _zazzau_district_geo_anchors()
STRANGER_VETTING_DISTANCE_KM = 35.0


def district_geo_anchor(district_id: str) -> tuple[float, float] | None:
    """Pilot-only WGS84 stub for distance vetting — not an emirate-boundary primitive."""
    did = str(district_id or "").strip().upper()
    return ZAZZAU_DISTRICT_GEO_ANCHORS.get(did)


def district_record_by_id(district_id: str) -> dict[str, str] | None:
    did = str(district_id or "").strip().upper()
    for row in ZAZZAU_THIRTY_ONE_DISTRICTS:
        if row["district_id"].upper() == did:
            return dict(row)
    return None


def districts_grouped_by_lga() -> dict[str, list[dict[str, str]]]:
    out: dict[str, list[dict[str, str]]] = {}
    for row in ZAZZAU_THIRTY_ONE_DISTRICTS:
        lg = row["parent_lga_en"]
        out.setdefault(lg, []).append(dict(row))
    return out


def zazzau_district_ledger_count(lga_en: str) -> int:
    """Authoritative Zazzau-31 district nodes under each eleven-LGA pilot row."""
    lg = str(lga_en or "").strip()
    return sum(1 for d in ZAZZAU_THIRTY_ONE_DISTRICTS if d["parent_lga_en"] == lg)


def _pick_prop(props: dict[str, Any], keys: tuple[str, ...]) -> str:
    for k in keys:
        v = props.get(k)
        if v not in (None, ""):
            return str(v).strip().lower()
    return ""


# Institutional portrait — domains within Zazzau district nodes + lattice LGA
KADUNA_INSTITUTIONS: list[dict[str, Any]] = [
    {
        "name": "Ahmadu Bello University",
        "abbr": "ABU",
        "regulator": "NUC",
        "ownership": "Federal",
        "lga_weld": "Sabon Gari",
        "zazzau_districts": ["ZD07 · Shika", "ZD09 · Samaru belt"],
        "note": "Samaru / main campus belt → Sabon Gari · Shika + Samaru domain nodes.",
    },
    {
        "name": "Federal University of Education, Zaria",
        "abbr": "FUE Zaria",
        "regulator": "NUC",
        "regulator_subline": "[NCCE] Transitioning from Federal College of Education.",
        "ownership": "Federal",
        "lga_weld": "Zaria",
        "zazzau_districts": ["ZD01 · Birni da kewaye"],
        "note": "Federal teacher-education anchor → Zaria · Birni da kewaye district.",
    },
    {
        "name": "Nigerian College of Aviation Technology",
        "abbr": "NCAT",
        "regulator": "NBTE",
        "subtag": "Aviation",
        "ownership": "Federal",
        "lga_weld": "Zaria",
        "zazzau_districts": ["ZD02 · Hanwa (aviation corridor)"],
        "note": "Sovereign aviation asset · Hanwa ZD02 weld — dedicated NBTE node on the Zaria lattice.",
        "sovereign_asset_node": True,
    },
    {
        "name": "Nigerian Defence Academy",
        "abbr": "NDA",
        "regulator": "NUC",
        "subtag": "Special",
        "ownership": "Federal",
        "lga_weld": "Chikun",
        "zazzau_districts": [
            "ZD26 · Doka (Kaduna North frontier)",
            "Lattice: Chikun LGA (Afaka) — Kaduna North/Chikun strategic weld",
        ],
        "note": "Afaka campus · primary ADM2 spine Chikun; ancestral pilot ties Kaduna North frontier nodes.",
    },
    {
        "name": "Kaduna State University",
        "abbr": "KASU",
        "regulator": "NUC",
        "ownership": "State",
        "lga_weld": "Kaduna North",
        "zazzau_districts": ["ZD26 · Doka"],
        "note": "Main campus cadence → Kaduna North · Doka district.",
    },
    {
        "name": "Kaduna Polytechnic",
        "abbr": "KADPOLY",
        "regulator": "NBTE",
        "ownership_tier": "FED",
        "ownership": "Federal",
        "lga_weld": "Kaduna South",
        "zazzau_districts": ["ZD29 · Barnawa", "ZD31 · Makera", "ZD30 · Kakuri"],
        "note": (
            "Federal polytechnic · main campus lattice on Kaduna South — distinct from the state-owned "
            "Nuhu Bamalli Polytechnic (NUBA) Zaria / Kafanchan architecture below (dual-poly separation)."
        ),
        "poly_colleges": [
            {
                "name": "College of Administrative and Business Studies",
                "abbr": "CABS",
                "lga_weld": "Kaduna South",
                "zazzau_districts": ["ZD29 · Barnawa"],
                "note": "Administrative & business studies — Barnawa district weld.",
            },
            {
                "name": "College of Environmental Studies",
                "abbr": "CES",
                "lga_weld": "Kaduna South",
                "zazzau_districts": ["ZD31 · Makera"],
                "note": "Environmental studies — Makera district weld.",
            },
            {
                "name": "College of Engineering",
                "abbr": "Engineering",
                "lga_weld": "Kaduna South",
                "zazzau_districts": ["ZD30 · Kakuri"],
                "note": "Engineering programmes — Kakuri corridor (Kaduna South lattice).",
            },
        ],
    },
    {
        "name": "Nuhu Bamalli Polytechnic",
        "abbr": "NUBA",
        "regulator": "NBTE",
        "ownership_tier": "STA",
        "ownership": "State",
        "sovereign_air_before_px": 96,
        "lga_weld": "Zaria",
        "zazzau_districts": [],
        "note": (
            "Kaduna State Government [STA] — ancestral naming: Nuhu Bamalli Polytechnic (NUBA). "
            "HQ main campus on Zaria welds to Zazzau district heads Hanwa + Birni da kewaye; "
            "southern Kafanchan campus welds to Jema'a Emirate domain (not Zazzau 31)."
        ),
        "campuses": [
            {
                "campus_title": "Main Campus · Zaria (HQ node)",
                "lga_weld": "Zaria",
                "zazzau_districts": ["ZD01 · Birni da kewaye", "ZD02 · Hanwa"],
                "traditional_domain": "Zazzau Emirate",
                "me_anguwa_pressure_note": (
                    "Dense Samaru-adjacent student pulse — Me Anguwa verification load concentrates on "
                    "ZD01/ZD02 ward spine; coordinate with ABU / Samaru belt ledger rows."
                ),
            },
            {
                "campus_title": "Kafanchan Campus (Southern node)",
                "lga_weld": "Jema'a",
                "zazzau_districts": [],
                "district_anchor_en": "Kafanchan town · Jema'a LGA · Jema'a Emirate",
                "traditional_domain": "Jema'a Emirate",
                "me_anguwa_pressure_note": (
                    "Southern Kaduna corridor — verification pressure follows Jema'a ward heads and "
                    "southern council lattice; do not route this campus through Zazzau district IDs."
                ),
            },
        ],
    },
]

# Modern statutory lattice — NOT Emirate / ancestral command (warrant-chief vs apex clarity).
KADUNA_MODERN_STATUTORY_LATTICE: list[dict[str, str]] = [
    {
        "office": "Local Government Chairman",
        "badge": "Statutory council · tenure office",
        "domain": "774 ADM2 local-government lattice",
        "note": (
            "Administrative mandate under state law — distinct from Emirate decree lineage. "
            "Never conflate with Traditional Apex (no ancestral command seal)."
        ),
    },
    {
        "office": "Councilors & supervisory appointees",
        "badge": "Political / delegated mandate",
        "domain": "Ward & council wards (modern)",
        "note": (
            "Contrast with District Head / Village Head Human API — modern appointment does not "
            "inherit Zazzau ancestral weld unless separately titled by Emirate chancellery."
        ),
    },
]

# Kaduna State Council of Chiefs — precedence order (rank badges for Traditional Portrait).
KADUNA_CHIEFS_COUNCIL_PRECEDENCE: list[dict[str, str]] = [
    {
        "rank": "Chairman",
        "badge": "Apex · Council of Chiefs",
        "domain": "Zazzau Emirate",
        "title": "Emir of Zazzau",
    },
    {
        "rank": "1st Class",
        "badge": "1st Class Chief",
        "domain": "Kagoro / Moro’a",
        "title": "Chief of Kagoro (Moro’a)",
    },
    {
        "rank": "Emir",
        "badge": "2nd rank · Emirate seat",
        "domain": "Jema’a Emirate",
        "title": "Emir of Jema’a",
    },
    {
        "rank": "Emir",
        "badge": "3rd rank · Emirate seat",
        "domain": "Lere Emirate",
        "title": "Emir of Lere",
    },
    {
        "rank": "Emir",
        "badge": "4th rank · Emirate seat",
        "domain": "Birnin Gwari Emirate",
        "title": "Emir of Birnin Gwari",
    },
]

ZAZZAU_APEX: dict[str, Any] = {
    "title": "Emir of Zazzau",
    "role": "Traditional apex · Zazzau Emirate (Kaduna pilot)",
    "district_nodes": 31,
    "village_heads": 84,
    "masu_unguwanni": 220,
    "ledger_note": "Thirty-one district ledger nodes — Me Anguwa verification must bind ZD** + ward spine.",
    "eleven_lgas": ZAZZAU_ELEVEN_LGA_EN,
    "thirty_one_districts": ZAZZAU_THIRTY_ONE_DISTRICTS,
}


def resolve_kaduna_ward_spine_row(
    wards_fc: dict | None, ward_pcode: str
) -> dict[str, str] | None:
    """
    Resolve one ward row on the Kaduna ADM1 slice of the HDX spine (774 lattice).
    Returns ward_pcode, ward_en, lga_en (display strings from properties).
    """
    if not wards_fc or not wards_fc.get("features"):
        return None
    needle_pc = str(ward_pcode or "").strip()
    if not needle_pc:
        return None
    for feat in wards_fc["features"]:
        p = feat.get("properties") or {}
        st_name = _pick_prop(p, ("ADM1_EN", "adm1_en", "ADM1_REF", "STATENAME"))
        if STATE_MATCH not in st_name:
            continue
        wp = str(p.get("ADM3_PCODE") or p.get("adm3_pcode") or "").strip()
        if wp != needle_pc:
            continue
        lga_raw = ""
        for k in ("ADM2_EN", "adm2_en", "ADM2_REF", "LGA_NAME"):
            v = p.get(k)
            if v not in (None, ""):
                lga_raw = str(v).strip()
                break
        wd_raw = ""
        for k in ("ADM3_EN", "adm3_en", "WARD", "WARD_NAME"):
            v = p.get(k)
            if v not in (None, ""):
                wd_raw = str(v).strip()
                break
        return {"ward_pcode": wp, "ward_en": wd_raw, "lga_en": lga_raw}
    return None


def is_kaduna_frontier_lga(lga_en: str) -> bool:
    g = normalize_lga_key(lga_en)
    return any(normalize_lga_key(x) == g for x in KADUNA_SPT_FRONTIER_LGA_EN)


def lga_pcode_lookup(wards_fc: dict | None, lga_name: str) -> str:
    """Resolve first ADM2_PCODE for Kaduna + matching ADM2_EN (774 lattice)."""
    if not wards_fc or not wards_fc.get("features"):
        return "—"
    needle = " ".join(lga_name.strip().lower().split())
    for feat in wards_fc["features"]:
        p = feat.get("properties") or {}
        st_name = _pick_prop(p, ("ADM1_EN", "adm1_en", "ADM1_REF", "STATENAME"))
        if STATE_MATCH not in st_name:
            continue
        lga_en = _pick_prop(p, ("ADM2_EN", "adm2_en", "ADM2_REF", "LGA_NAME"))
        if lga_en != needle:
            continue
        for key in ("ADM2_PCODE", "adm2_pcode", "LGA_CODE"):
            v = p.get(key)
            if v not in (None, ""):
                return str(v).strip()
    return "—"


def ward_count_for_lga(wards_fc: dict | None, lga_name: str) -> int:
    """Count ward polygons for Kaduna + LGA (must match Intelligent Map spine)."""
    if not wards_fc or not wards_fc.get("features"):
        return 0
    needle = " ".join(lga_name.strip().lower().split())
    n = 0
    for feat in wards_fc["features"]:
        p = feat.get("properties") or {}
        st_name = _pick_prop(p, ("ADM1_EN", "adm1_en", "ADM1_REF", "STATENAME"))
        if STATE_MATCH not in st_name:
            continue
        lga_en = _pick_prop(p, ("ADM2_EN", "adm2_en", "ADM2_REF", "LGA_NAME"))
        if lga_en == needle:
            n += 1
    return n


def kaduna_state_ward_total(wards_fc: dict | None) -> int:
    if not wards_fc or not wards_fc.get("features"):
        return 0
    n = 0
    for feat in wards_fc["features"]:
        p = feat.get("properties") or {}
        st_name = _pick_prop(p, ("ADM1_EN", "adm1_en", "ADM1_REF", "STATENAME"))
        if STATE_MATCH in st_name:
            n += 1
    return n


def find_ward_pcode_rigasa_igabi(wards_fc: dict | None) -> str | None:
    """
    Rigasa — atomic ADM3_PCODE only (Igabi + label contains Rigasa). No LGA fallback.
    """
    if not wards_fc or not wards_fc.get("features"):
        return None
    matches: list[tuple[str, str]] = []
    for feat in wards_fc["features"]:
        p = feat.get("properties") or {}
        st_name = _pick_prop(p, ("ADM1_EN", "adm1_en", "ADM1_REF", "STATENAME"))
        if STATE_MATCH not in st_name:
            continue
        lga_en = _pick_prop(p, ("ADM2_EN", "adm2_en", "ADM2_REF", "LGA_NAME"))
        if lga_en != "igabi":
            continue
        wd_name_raw = str(p.get("ADM3_EN") or p.get("adm3_en") or "")
        wd_name = wd_name_raw.strip().lower()
        wd_pc = str(p.get("ADM3_PCODE") or p.get("adm3_pcode") or "").strip()
        if not wd_pc:
            continue
        if "rigasa" in wd_name:
            matches.append((wd_pc, wd_name_raw.strip()))
    if not matches:
        return None
    if len(matches) == 1:
        return matches[0][0]
    for pc, nm in sorted(matches, key=lambda x: x[1].lower()):
        nml = nm.lower()
        if nml == "rigasa" or nml.startswith("rigasa "):
            return pc
    return sorted(matches, key=lambda x: x[0])[0][0]


def ward_count_from_spine_df(spine_df: pd.DataFrame | None, lga_name: str) -> int:
    """HDX spine table path — aligns property aliases with ng_connectivity.build_spine_table."""
    if spine_df is None or len(spine_df) == 0:
        return 0
    if "state_name" not in spine_df.columns or "lga_name" not in spine_df.columns:
        return 0
    needle = " ".join(lga_name.strip().lower().split())
    sn = (
        spine_df["state_name"]
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace("state", "", regex=False)
        .str.strip()
    )
    kad_mask = sn.str.contains(STATE_MATCH, na=False)
    ln = (
        spine_df["lga_name"]
        .astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", " ", regex=True)
    )
    return int((kad_mask & (ln == needle)).sum())


def build_zazzau_eleven_lga_weld_rows(
    wards_fc: dict | None,
    spine_df: pd.DataFrame | None = None,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for name in ZAZZAU_ELEVEN_LGA_EN:
        pcode = lga_pcode_lookup(wards_fc, name)
        wn = max(ward_count_for_lga(wards_fc, name), ward_count_from_spine_df(spine_df, name))
        rows.append(
            {
                "lga_en": name,
                "adm2_pcode": pcode,
                "ward_polygons_in_lga": wn,
                "district_nodes_in_lga": zazzau_district_ledger_count(name),
            }
        )
    return rows


RIGASA_DISTRICT_ID = "ZD22"

# --- Human-centric trust (GCSLC buy-in weld) — parent-facing copy for DAPI tooltips ---
DAPI_PARENT_FACING_PRIVACY: dict[str, str] = {
    "sha256_digest": (
        "SHA-256 is a one-way fingerprint of each verification line. Parents can see that the record "
        "was not tampered with—like a palace seal on wax—without exposing the child’s full story in plain sight."
    ),
    "encryption_steel": (
        "Data moves inside an encrypted tunnel (HTTPS), the same kind of lock banks use. What lands in the "
        "ledger is an attestation, not gossip. Your child’s row is treated as Locked in Steel."
    ),
}


def html_zazzau_zd01_success_demo() -> str:
    """
    Single-district success simulation — Zaria · Birni da kewaye (ZD01).
    Narrative demo for skeptics: Me Anguwa + DAPI secure one street without cold-database prose.
    """
    steps = (
        (
            "Dawn · Birni da kewaye",
            "The Me Anguwa walks the lane she already knows by name. Parents stop her: "
            "“Who is the new face in the compound?” She opens DAPI on her phone—not as IT staff, "
            "but as the ward’s living memory.",
        ),
        (
            "One sovereign certificate",
            "She selects ZD01, taps the ward spine code the palace agreed with INEC, and records a handshake "
            "for a student_uid. The child’s institution and residence nodes bind in the same breath as the "
            "Haraji rhythm her grandmother knew.",
        ),
        (
            "Steel without chill",
            "Behind the gentle screen, SHA-256 presses a seal on the line; encryption carries it home. "
            "No spreadsheet shouts—only a gold banner: Sovereign Clearance acknowledged.",
        ),
        (
            "The street wins",
            "By noon the lane has one verifiable truth: who belongs to which care circle. "
            "Skeptics see the cyan pulse on the map and understand—this is a digital palace, not a database raid.",
        ),
    )
    parts: list[str] = [
        '<div class="kgec-zd01-success-demo" role="region" aria-label="Zaria ZD01 success simulation">',
        '<p class="kgec-zd01-success-kicker">Galadiman Ruwa · buy-in simulation</p>',
        '<p class="kgec-zd01-success-lede">One district · one Me Anguwa · one street made legible with dignity.</p>',
        "<ol>",
    ]
    for title, body in steps:
        parts.append(
            "<li>"
            f'<p class="kgec-zd01-success-step-title">{html.escape(title)}</p>'
            f'<p class="kgec-zd01-success-step-body">{html.escape(body)}</p>'
            "</li>"
        )
    parts.append("</ol>")
    parts.append(
        '<p class="kgec-zd01-success-foot">ZD01 · Birni da kewaye · Zaria LGA — '
        "pilot narrative; bind live verifications to your own ward_pcode + district node.</p>"
        "</div>"
    )
    return "".join(parts)
