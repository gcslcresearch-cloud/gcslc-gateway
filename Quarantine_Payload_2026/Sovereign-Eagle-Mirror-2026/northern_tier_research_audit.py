"""
Silent research audit — Northern traditional vs institutional tiers (GCSLC overnight bundle).

774 lattice (ADM2 / LGA names from gcslc_deep_join.fetch_lga_catalog_raw) is NEVER rewritten.
Emirate / friction layers are orthogonal overlays keyed by the same LGA string the spine uses.
"""

from __future__ import annotations

from typing import Any

from gcslc_deep_join import fetch_lga_catalog_raw

from katsina_kano_forensic import KANO_EMIR_METROPOLITAN_CORE_EIGHT

STATE_KANO = "KN"
STATE_KATSINA = "KT"

# Five statutory emirate seats (2019+) — four named capital LGAs + Kano Municipal (Kano emirate seat).
_KANO_STATUTORY_SEAT_LGAS: frozenset[str] = frozenset({"Bichi", "Gaya", "Karaye", "Rano"})

KATSINA_774_COUNT_VERIFIED = 34
KATSINA_EMIRATE_LEGACY_COUNT_CLAIM = 27
KATSINA_COUNT_DISCREPANCY_NOTE = (
    "Silent audit: the 774 Nigerian LGA catalogue used by gcslc_deep_join lists **34** LGAs for "
    "Katsina (KT), matching public administrative references (e.g. state LGA directories). "
    "A **27-LGA** figure under the Emir of Katsina is **not** the same as the statutory 774 row count — "
    "it may denote a historical traditional district bundle or oral chancellery lattice. "
    "Hard-weld MUST key on all **34** ADM2 names for spine parity; reconcile '27' only via a "
    "separate `traditional_domain_subset` overlay once the palace / council publishes an authoritative list."
)


def _lgas_for_state_code(state_code: str) -> tuple[str, ...]:
    raw = fetch_lga_catalog_raw()
    sc = str(state_code or "").strip().upper()
    names = sorted(str(r.get("name") or "").strip() for r in raw if str(r.get("state_code") or "").upper() == sc)
    return tuple(n for n in names if n)


def kano_44_lgas_hard_weld() -> tuple[str, ...]:
    """Exactly 44 Kano (KN) LGAs — same ordering as catalogue sort (deterministic)."""
    t = _lgas_for_state_code(STATE_KANO)
    if len(t) != 44:
        raise RuntimeError(f"Kano 774 invariant broken — expected 44 KN LGAs, got {len(t)}")
    return t


def katsina_34_lgas_hard_weld() -> tuple[str, ...]:
    """Exactly 34 Katsina (KT) LGAs — statutory 774 lattice truth for hard-weld."""
    t = _lgas_for_state_code(STATE_KATSINA)
    if len(t) != KATSINA_774_COUNT_VERIFIED:
        raise RuntimeError(
            f"Katsina 774 invariant broken — expected {KATSINA_774_COUNT_VERIFIED} KT LGAs, got {len(t)}"
        )
    return t


def primary_emirate_seat_kano(lga_en: str) -> str:
    """
    Pilot overlay — statutory five-emirate architecture: four seat LGAs + Kano Municipal (Kano seat);
    all other KN LGAs carry the **core umbrella** overlay (single-emirate historical memory vs five-seat law).
    """
    name = str(lga_en or "").strip()
    if name == "Kano Municipal":
        return "KANO_EMIRATE_STATUTORY_SEAT"
    if name in _KANO_STATUTORY_SEAT_LGAS:
        return f"{name.upper()}_EMIRATE_STATUTORY_SEAT"
    return "KANO_EMIRATE_CORE_OVERLAY"


def kano_44_emirate_friction_overlay() -> list[dict[str, Any]]:
    """
    D4 — Kano 44 schema: each LGA row carries `emirate_primary` + `friction_profile` without touching 774 keys.

    Friction model (documentation-first):
    - `lattice_key` == LGA display name (matches HDX / catalogue ADM2_EN when normalized upstream).
    - `emirate_primary` distinguishes five statutory seats vs core umbrella.
    - `friction_tags` annotate the 5-vs-1 narrative for UI / policy layers — never mutate pcode.
    """
    rows: list[dict[str, Any]] = []
    for lga in kano_44_lgas_hard_weld():
        seat = primary_emirate_seat_kano(lga)
        tags: tuple[str, ...]
        if seat.endswith("_EMIRATE_STATUTORY_SEAT") or seat == "KANO_EMIRATE_STATUTORY_SEAT":
            tags = (
                "774_lattice_fixed",
                "five_emirate_statute_overlay",
                "single_emirate_memory_parallel",
            )
        else:
            tags = (
                "774_lattice_fixed",
                "kano_emirate_core_overlay",
                "five_emirate_statute_context",
            )
        rows.append(
            {
                "lattice_key": lga,
                "state_code": STATE_KANO,
                "emirate_primary": seat,
                "emir_amimu_ado_bayero_metro_core_eligible": lga in KANO_EMIR_METROPOLITAN_CORE_EIGHT,
                "friction_tags": tags,
                "friction_note": (
                    "Statutory fragmentation (5 seats) vs unified Kano Emirate memory — "
                    "resolve in UI/policy layer; ADM2 pcode remains canonical."
                ),
            }
        )
    return rows


def katsina_hard_weld_report() -> dict[str, Any]:
    """Morning-ready checksum for Katsina pilot."""
    names = katsina_34_lgas_hard_weld()
    return {
        "state_code": STATE_KATSINA,
        "lga_count_774": len(names),
        "legacy_emirate_count_claim": KATSINA_EMIRATE_LEGACY_COUNT_CLAIM,
        "discrepancy_resolution": KATSINA_COUNT_DISCREPANCY_NOTE,
        "lgas_sorted": names,
    }


DAPI_VERIFICATION_SURGE_LOGIC = """
DAPI scaling — high-density KN / KD nodes (silent audit draft, no runtime wire-up yet):

1) **SQLite durability**
   - PRAGMA journal_mode=WAL; synchronous=NORMAL (tune per risk appetite).
   - Keep `student_uid` PRIMARY KEY — hot inserts stay O(log N) on B-tree.

2) **Write path**
   - Short transactions: one INSERT per verification (already minimal).
   - Optional `executemany` batch endpoint for bulk replay (migration / re-index jobs only).

3) **Read path**
   - `ward_pcode` + `principal_id` indexes already present — verify ANALYZE after bulk load.
   - For heatmaps: pre-aggregate `ward_pcode -> COUNT(*)` in-memory cache (TTL) refreshed on write burst.

4) **App tier**
   - Streamlit: move heavy `st.dataframe` loads for ledgers behind pagination / `limit` (already capped).
   - Background thread queue (future): accept writes, flush to SQLite with back-pressure.

5) **Ops**
   - Rotate `logs/dapi_verification.sqlite` to timestamped files before large demos; WAL + copy requires checkpoint.
"""


def dapi_surge_readiness_checklist() -> dict[str, str]:
    """Structured checklist for engineering stand-up (no side effects)."""
    return {
        "wal": "Enable WAL + checkpoint policy before Kano-scale demos.",
        "indexes": "Confirm ward + principal + zazzau indexes post-migration.",
        "ui_limits": "Cap verification / CDC dataframe rows; lazy expanders.",
        "backup": "Archive sqlite before surge tests (see logs/archive/).",
    }
