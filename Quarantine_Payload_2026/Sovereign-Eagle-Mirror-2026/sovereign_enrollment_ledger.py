"""
Sovereign Enrollment Ledger — national notional seat counts (36 states + FCT) with Kaduna pilot steel.

Kaduna figures are sourced from kaduna_pilot_student_deep_weld.json (ABU, KASU, NUBA split, etc.).
Other states carry proportional notional placeholders totalling the national seed alongside Kaduna.
"""

from __future__ import annotations

import html
from typing import Any

from gcslc_deep_join import STATE_CODE_TO_STATE
from kaduna_student_deep_weld import load_kaduna_student_deep_weld

# Order-of-magnitude national tertiary envelope for economics widgets — regulator bulk replaces this.
NATIONAL_NOTIONAL_TOTAL_STUDENTS = 2_500_000

# Default 1k verification economics — MOU-tunable (must sum to 1.0).
# Steel opinion: gateway (Termii) sufficient margin without starving transport;
# MNOs carry USSD/SMS/WhatsApp pipes; sovereign hub retains majority for clearance + audit rail.
DEFAULT_TERMII_SHARE = 0.15
DEFAULT_NETWORKS_SHARE = 0.25
DEFAULT_US_GNL_SHARE = 0.60

# Commander's Albasa specification — economics (onions) bound to enrollment (meat); MOU stamps percentages.
SOVEREIGN_ALBASA_SPEC: dict[str, Any] = {
    "schema": "sovereign_albasa.v1",
    "title": "Albasa · ₦1k Airtime Verification Economics",
    "mandate": {
        "retail_verification_fee_ngn": 1000,
        "per_fee_partner_take_ngn_at_defaults": {
            "termii_gateway": 150,
            "networks_transport": 250,
            "us_gnl_sovereign_hub": 600,
        },
        "collection_rail_primary": "Individual airtime / telco wallet debit",
        "collection_rail_parallel": (
            "Institutional bulk-vetting lane — same audit chain, invoiced pool, "
            "preserves inclusion without breaking individual accountability class"
        ),
    },
    "partner_split_default_pct": {
        "termii_gateway": {
            "share": 15,
            "role": "OTP issuance, handshake API, delivery receipts, reconciliation exports · Digital Gateway",
        },
        "networks_transport": {
            "share": 25,
            "role": "MNO interconnect, bearer, USSD/SMS/WhatsApp transport · Transport Layer",
        },
        "us_gnl_sovereign_hub": {
            "share": 60,
            "role": (
                "Sovereign clearance core — Human API weld, ledger seals, criminal-trace protocol hooks, "
                "fund recycling / sovereign fund mandate · Strategic Brain (lion's share)"
            ),
        },
    },
    "national_ledger_layout": {
        "surface": "Sovereign Audit — single expander, tabbed: Enrollment | Albasa Revenue | Specification",
        "forensic_strip": "Always-visible headline band above Audit (ABU · KASU · NUBA · Kaduna Σ · National Σ)",
        "enrollment_table": (
            "37 rows (36 states + FCT); columns include notional heads + "
            "Albasa monthly pool (= heads × fee × verification intensity) so meat carries onions inline"
        ),
        "sovereign_air_rule": "96px airway column remains prose-free — ledger lives in Audit strip + tabs, not over aviation chrome",
    },
    "ledger_to_revenue_formula": (
        "monthly_gross_albasa_pool = Σ(enrollment_basis) × verifications_per_student_per_month × fee_ngn; "
        "partner_slice = monthly_gross × MOU_pct"
    ),
}


def bind_albasa_monthly_pool_to_ledger_rows(
    rows: list[dict[str, Any]],
    *,
    ngn_per_verification: float = 1000.0,
    verifications_per_student_per_month: float = 1.0,
) -> list[dict[str, Any]]:
    """
    Fuse Albasa economics into each jurisdiction row — implied monthly toll pool at stated fee × intensity.

    This is not statutory revenue recognition; it is a planning envelope tied to enrollment seeds.
    """
    fee = max(0.0, float(ngn_per_verification))
    vpm = max(0.0, float(verifications_per_student_per_month))
    out: list[dict[str, Any]] = []
    for r in rows:
        n = int(r.get("notional_students") or 0)
        pool = int(round(n * vpm * fee))
        row = dict(r)
        row["albasa_monthly_pool_ngn"] = pool
        out.append(row)
    return out


def bind_albasa_pool_to_kaduna_institution_rows(
    institution_rows: list[dict[str, Any]],
    *,
    ngn_per_verification: float = 1000.0,
    verifications_per_student_per_month: float = 1.0,
) -> list[dict[str, Any]]:
    """Per-institution Albasa monthly pool for Kaduna pilot drill-down."""
    fee = max(0.0, float(ngn_per_verification))
    vpm = max(0.0, float(verifications_per_student_per_month))
    out: list[dict[str, Any]] = []
    for r in institution_rows:
        try:
            stu = int(r.get("students") or 0)
        except (TypeError, ValueError):
            stu = 0
        pool = int(round(stu * vpm * fee))
        row = dict(r)
        row["albasa_monthly_pool_ngn"] = pool
        out.append(row)
    return out


def kaduna_headline_enrollment_counts(cfg: dict[str, Any] | None = None) -> dict[str, int]:
    """ABU / KASU / NUBA totals from the Kaduna pilot weld JSON (forensic headline strip)."""
    raw = cfg if cfg is not None else load_kaduna_student_deep_weld()
    out = {"ABU": 0, "KASU": 0, "NUBA": 0}
    for row in raw.get("institutions") or []:
        abbr = str(row.get("abbr") or "").strip().upper()
        camps = list(row.get("campus_enrolments") or [])
        if camps:
            sub = 0
            for c in camps:
                try:
                    sub += int(c.get("notional_students_2025_26") or 0)
                except (TypeError, ValueError):
                    pass
            if abbr == "NUBA":
                out["NUBA"] = sub
            continue
        try:
            n = int(row.get("notional_students_2025_26") or 0)
        except (TypeError, ValueError):
            n = 0
        if abbr == "ABU":
            out["ABU"] = n
        elif abbr == "KASU":
            out["KASU"] = n
    return out


def national_ledger_population_sum(rows: list[dict[str, Any]]) -> int:
    """Σ state notionals — must match configured national envelope when ledger was built."""
    return sum(int(r.get("notional_students") or 0) for r in rows)


def _kaduna_pilot_breakdown(cfg: dict[str, Any]) -> tuple[int, list[dict[str, Any]], str]:
    """Total heads, detail rows for Kaduna-only drill-down, one-line pilot highlight."""
    lines: list[dict[str, Any]] = []
    total = 0
    parts: list[str] = []
    for row in cfg.get("institutions") or []:
        abbr = str(row.get("abbr") or "").strip().upper()
        name = str(row.get("name") or "").strip()
        camps = list(row.get("campus_enrolments") or [])
        if camps:
            sub = 0
            for c in camps:
                try:
                    sub += int(c.get("notional_students_2025_26") or 0)
                except (TypeError, ValueError):
                    pass
            total += sub
            lines.append(
                {
                    "abbr": abbr or "—",
                    "institution": name,
                    "students": sub,
                    "campuses": len(camps),
                    "note": "Multi-campus roll-up (pilot JSON)",
                }
            )
            if abbr == "NUBA":
                parts.append(f"NUBA (total): ~{sub:,}")
            continue
        try:
            n = int(row.get("notional_students_2025_26") or 0)
        except (TypeError, ValueError):
            n = 0
        total += n
        lines.append(
            {
                "abbr": abbr or "—",
                "institution": name,
                "students": n,
                "campuses": 1,
                "note": str(row.get("primary_campus_lga_lattice") or ""),
            }
        )
        if abbr == "ABU":
            parts.append(f"ABU Zaria: ~{n:,}")
        elif abbr == "KASU":
            parts.append(f"KASU: ~{n:,}")
    summary = " · ".join(parts) if parts else ""
    return total, lines, summary


def build_sovereign_enrollment_ledger_rows(
    *, national_total: int | None = None
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """
    Return (rows for st.dataframe, meta).

    Kaduna total comes from the pilot weld JSON; remaining national mass is split evenly across
    the other 36 codes so Σ(state totals) == national_total.
    """
    nat = int(national_total or NATIONAL_NOTIONAL_TOTAL_STUDENTS)
    cfg = load_kaduna_student_deep_weld()
    kd_total, kd_detail, kd_highlight = _kaduna_pilot_breakdown(cfg)
    others_pool = max(0, nat - kd_total)
    codes_other = sorted(sc for sc in STATE_CODE_TO_STATE if sc != "KD")
    n_other = len(codes_other)
    base = others_pool // n_other if n_other else 0
    rem = others_pool % n_other if n_other else 0
    rows: list[dict[str, Any]] = []
    for i, sc in enumerate(codes_other):
        tot = base + (1 if i < rem else 0)
        rows.append(
            {
                "state_code": sc,
                "state_en": STATE_CODE_TO_STATE[sc],
                "notional_students": tot,
                "pilot_highlight": "",
                "source_note": "Notional seed — regulator bulk ingest pending",
            }
        )
    rows.append(
        {
            "state_code": "KD",
            "state_en": "Kaduna",
            "notional_students": kd_total,
            "pilot_highlight": kd_highlight,
            "source_note": "Kaduna pilot weld · Part_04_Social/data/kaduna_pilot_student_deep_weld.json",
        }
    )
    rows.sort(key=lambda r: str(r["state_en"]))
    meta = {
        "national_notional_total": nat,
        "kaduna_total": kd_total,
        "kaduna_institution_rows": kd_detail,
        "academic_cycle": str(cfg.get("academic_cycle") or "2025-2026"),
    }
    return rows, meta


def verification_revenue_projection(
    *,
    student_population: float,
    ngn_per_verification: float = 1000.0,
    verifications_per_student_per_month: float = 1.0,
    termii_share: float = DEFAULT_TERMII_SHARE,
    networks_share: float = DEFAULT_NETWORKS_SHARE,
    us_gnl_share: float = DEFAULT_US_GNL_SHARE,
) -> dict[str, Any]:
    """
    Gross verification toll assuming uniform ₦/verification × population × monthly verification intensity.

    Three-way split defaults: Termii 15% · Networks 25% · US GNL 60% (MOU-tunable).
    Shares must sum to 1.0.
    """
    s_sum = termii_share + networks_share + us_gnl_share
    if abs(s_sum - 1.0) > 1e-6:
        raise ValueError("Revenue shares must sum to 1.0")
    pop = max(0.0, float(student_population))
    rate = max(0.0, float(ngn_per_verification))
    vpm = max(0.0, float(verifications_per_student_per_month))
    monthly_gross = pop * vpm * rate
    quarterly_gross = monthly_gross * 3.0
    annual_gross = monthly_gross * 12.0

    def _split(gross: float) -> dict[str, float]:
        t = round(gross * termii_share, 2)
        n = round(gross * networks_share, 2)
        u = round(gross * us_gnl_share, 2)
        drift = round(gross - (t + n + u), 2)
        u = round(u + drift, 2)
        return {
            "termii_gateway": t,
            "networks_transport": n,
            "us_gnl_hub": u,
        }

    return {
        "monthly_gross": monthly_gross,
        "quarterly_gross": quarterly_gross,
        "annual_gross": annual_gross,
        "monthly_split": _split(monthly_gross),
        "quarterly_split": _split(quarterly_gross),
        "annual_split": _split(annual_gross),
        "shares": {
            "termii": termii_share,
            "networks": networks_share,
            "us_gnl": us_gnl_share,
        },
    }


def html_albasa_commander_benchmark_table(rows: list[dict[str, Any]]) -> str:
    """Commander-fixed scenarios — Kaduna 150k vs national 2.5M; 15% / 25% / 60% on ₦1k."""
    body: list[str] = []
    for r in rows:
        body.append(
            "<tr>"
            f"<td>{html.escape(str(r.get('scenario') or ''))}</td>"
            f"<td class='kgec-mophi-num'>{int(r.get('population') or 0):,}</td>"
            f"<td class='kgec-mophi-num'>₦ {int(r.get('monthly_gross_ngn') or 0):,}</td>"
            f"<td class='kgec-mophi-num'>₦ {int(r.get('annual_gross_ngn') or 0):,}</td>"
            f"<td class='kgec-mophi-num'>₦ {int(r.get('monthly_termii_ngn') or 0):,}</td>"
            f"<td class='kgec-mophi-num'>₦ {int(r.get('monthly_networks_ngn') or 0):,}</td>"
            f"<td class='kgec-mophi-num'>₦ {int(r.get('monthly_us_gnl_ngn') or 0):,}</td>"
            "</tr>"
        )
    return (
        "<div class='kgec-mophi-revenue-wrap kgec-albasa-commander-benchmark'>"
        "<table class='kgec-mophi-revenue-table' role='table' aria-label='Albasa commander benchmark'>"
        "<thead><tr><th>Scenario</th><th>Population</th><th>Monthly gross</th><th>Annual gross</th>"
        "<th>Termii 15%</th><th>Networks 25%</th><th>US GNL 60%</th></tr></thead><tbody>"
        + "".join(body)
        + "</tbody></table>"
        "<p class='kgec-albasa-fee-foot'>₦1,000 / verification · Termii ₦150 · Networks ₦250 · "
        "US GNL ₦600 · intensity 1× / student / month.</p></div>"
    )


def html_albasa_split_math_panel(
    *,
    student_population: int,
    ngn_per_verification: float,
    verifications_per_student_per_month: float,
    proj: dict[str, Any],
) -> str:
    """
    Commander-facing algebra strip — gross pool then 15% / 25% / 60% slices (comma-separated NGN).
    """
    pop = max(0, int(student_population))
    fee = max(0.0, float(ngn_per_verification))
    vpm = max(0.0, float(verifications_per_student_per_month))
    mg = float(proj["monthly_gross"])
    ms = proj["monthly_split"]
    ag = float(proj["annual_gross"])
    ay = proj["annual_split"]
    sh = proj["shares"]

    def _ngn(x: float) -> str:
        return f"₦{int(round(x)):,}"

    stamp600 = ""
    if abs(fee - 1000.0) < 0.01 and abs(sh["us_gnl"] - 0.6) < 1e-5:
        stamp600 = (
            "<br/><span style='display:inline-block;margin-top:6px;line-height:1.45'>"
            "<strong>₦600 stamp (annual treasury lift):</strong> ₦600 × "
            f"{pop:,} students × {vpm:g} verification/month × 12 months = "
            f"<strong>{_ngn(ay['us_gnl_hub'])}</strong> / year.</span>"
        )

    lines = [
        "<div class='kgec-albasa-math-panel' role='region' aria-label='Albasa split mathematics'>",
        "<p class='kgec-albasa-math-cap'><strong>National envelope · algebra (government-grade)</strong></p>",
        "<ul class='kgec-albasa-math-ul'>",
        f"<li><strong>Students (basis):</strong> {pop:,}</li>",
        f"<li><strong>Fee per verification:</strong> {_ngn(fee)}</li>",
        f"<li><strong>Verifications / student / month:</strong> {vpm:g}</li>",
        "<li><strong>Monthly gross pool</strong> = students × verifications × fee → "
        f"<code>{pop:,} × {vpm:g} × {_ngn(fee)}</code> = <strong>{_ngn(mg)}</strong></li>",
        f"<li><strong>Termii gateway ({sh['termii']:.0%}):</strong> monthly {_ngn(ms['termii_gateway'])} · "
        f"annual {_ngn(ay['termii_gateway'])}</li>",
        f"<li><strong>Networks transport ({sh['networks']:.0%}):</strong> monthly {_ngn(ms['networks_transport'])} · "
        f"annual {_ngn(ay['networks_transport'])}</li>",
        f"<li><strong>US GNL sovereign hub ({sh['us_gnl']:.0%}):</strong> monthly {_ngn(ms['us_gnl_hub'])} · "
        f"annual <strong>{_ngn(ay['us_gnl_hub'])}</strong> — <em>lion's share</em>{stamp600}</li>",
        f"<li><strong>Annual gross pool:</strong> {_ngn(ag)} (= monthly {_ngn(mg)} × 12)</li>",
        "</ul>",
        "<p class='kgec-albasa-math-foot'>Per-fee retail decomposition at ₦1k: Termii ₦150 · Networks ₦250 · US GNL ₦600.</p>",
        "</div>",
    ]
    return "".join(lines)


def html_verification_revenue_mophi_table(proj: dict[str, Any]) -> str:
    """Mophi-glass revenue split — Termii / Networks / US GNL."""
    sh = proj["shares"]
    rs = (
        ("Monthly gross", proj["monthly_gross"], proj["monthly_split"]),
        ("Quarterly gross", proj["quarterly_gross"], proj["quarterly_split"]),
        ("Annual gross", proj["annual_gross"], proj["annual_split"]),
    )
    tip = (
        f"Assumed shares · Termii gateway {sh['termii']:.0%} · "
        f"Networks transport {sh['networks']:.0%} · US GNL hub {sh['us_gnl']:.0%}"
    )
    rows_html = []
    for label, gross, sp in rs:
        rows_html.append(
            "<tr>"
            f"<td>{html.escape(label)}</td>"
            f"<td class='kgec-mophi-num'>₦ {gross:,.0f}</td>"
            f"<td class='kgec-mophi-num'>₦ {sp['termii_gateway']:,.0f}</td>"
            f"<td class='kgec-mophi-num'>₦ {sp['networks_transport']:,.0f}</td>"
            f"<td class='kgec-mophi-num'>₦ {sp['us_gnl_hub']:,.0f}</td>"
            "</tr>"
        )
    return (
        f"<div class='kgec-mophi-revenue-wrap' title=\"{html.escape(tip)}\">"
        "<table class='kgec-mophi-revenue-table' role='table' aria-label='Verification revenue projection'>"
        "<thead><tr>"
        "<th>Period</th><th>Gross</th>"
        "<th>Termii · gateway</th><th>Networks · transport</th><th>US GNL · hub</th>"
        "</tr></thead><tbody>"
        + "".join(rows_html)
        + "</tbody></table></div>"
    )


def albasa_commander_benchmark_rows(
    *,
    fee_ngn: float = 1000.0,
    verifications_per_student_per_month: float = 1.0,
    termii_share: float = DEFAULT_TERMII_SHARE,
    networks_share: float = DEFAULT_NETWORKS_SHARE,
    us_gnl_share: float = DEFAULT_US_GNL_SHARE,
) -> list[dict[str, Any]]:
    """
    Fixed Commander scenarios — Kaduna ~150k vs national 2.5M at MOU split on ₦1k × intensity.
    """
    scenarios = (
        ("Kaduna (~150,000 students)", 150_000),
        ("National envelope (2,500,000 students)", 2_500_000),
    )
    out: list[dict[str, Any]] = []
    for label, pop in scenarios:
        p = verification_revenue_projection(
            student_population=float(pop),
            ngn_per_verification=fee_ngn,
            verifications_per_student_per_month=verifications_per_student_per_month,
            termii_share=termii_share,
            networks_share=networks_share,
            us_gnl_share=us_gnl_share,
        )
        ms = p["monthly_split"]
        out.append(
            {
                "scenario": label,
                "population": pop,
                "monthly_gross_ngn": int(round(p["monthly_gross"])),
                "annual_gross_ngn": int(round(p["annual_gross"])),
                "monthly_termii_ngn": int(round(ms["termii_gateway"])),
                "monthly_networks_ngn": int(round(ms["networks_transport"])),
                "monthly_us_gnl_ngn": int(round(ms["us_gnl_hub"])),
            }
        )
    return out


__all__ = [
    "DEFAULT_NETWORKS_SHARE",
    "DEFAULT_TERMII_SHARE",
    "DEFAULT_US_GNL_SHARE",
    "NATIONAL_NOTIONAL_TOTAL_STUDENTS",
    "SOVEREIGN_ALBASA_SPEC",
    "albasa_commander_benchmark_rows",
    "html_albasa_commander_benchmark_table",
    "html_albasa_split_math_panel",
    "html_verification_revenue_mophi_table",
    "bind_albasa_monthly_pool_to_ledger_rows",
    "bind_albasa_pool_to_kaduna_institution_rows",
    "build_sovereign_enrollment_ledger_rows",
    "kaduna_headline_enrollment_counts",
    "national_ledger_population_sum",
    "verification_revenue_projection",
]
