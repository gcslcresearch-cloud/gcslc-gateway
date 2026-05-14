"""
Kaduna sovereign pilot · twin portrait on the Intelligent Map Page (IMP).

Institutional lattice + Zazzau eleven / thirty-one + councils — uses the same HDX spine shape as app.py phase-2.
"""

from __future__ import annotations

import html
from typing import Any

import streamlit as st

from kaduna_sovereign_pilot import (
    DISTRICT_LEDGER_NOTE,
    KADUNA_CHIEFS_COUNCIL_PRECEDENCE,
    KADUNA_INSTITUTIONS,
    KADUNA_MODERN_STATUTORY_LATTICE,
    ZAZZAU_APEX,
    ZAZZAU_ELEVEN_SOURCE_NOTE,
    ZAZZAU_THIRTY_ONE_DISTRICTS,
    build_zazzau_eleven_lga_weld_rows,
    html_zazzau_zd01_success_demo,
    kaduna_state_ward_total,
    lga_pcode_lookup,
    ward_count_for_lga,
)
from ng_connectivity import (
    GEOBOUNDARIES_API_NGA_ADM2,
    build_spine_table,
    fetch_geo_boundary_geojson,
    load_hdx_nga_geojson_zip_layers,
    prefer_hdx_or_geo_lga_geojson,
)


@st.cache_data(
    ttl=604800,
    show_spinner="Mounting HDX spine for Kaduna twin portrait…",
)
def load_phase2_spine_bundle_kaduna_portrait() -> dict[str, Any]:
    gb_lgas = fetch_geo_boundary_geojson(GEOBOUNDARIES_API_NGA_ADM2)
    hdx = load_hdx_nga_geojson_zip_layers()
    wards_fc = hdx.get("wards")
    lgas_fc = prefer_hdx_or_geo_lga_geojson(hdx.get("lgas"), gb_lgas)
    spine_df, spine_report = build_spine_table(wards_fc)
    return {
        "wards_fc": wards_fc,
        "lgas_fc": lgas_fc,
        "hdx": hdx,
        "spine_df": spine_df,
        "spine_report": spine_report,
    }


def render_kaduna_map_twin_portrait() -> None:
    """Twin columns: institutional lattice + Emirate / Council / Zazzau 31."""
    _phase2 = load_phase2_spine_bundle_kaduna_portrait()
    _wards_fc_kd = _phase2.get("wards_fc")

    with st.expander(
        "Buy-in · Success simulation · Zaria Birni da kewaye (ZD01) — one street, one Me Anguwa",
        expanded=False,
    ):
        st.markdown(html_zazzau_zd01_success_demo(), unsafe_allow_html=True)

    _pc_inst, _pc_trad = st.columns(2)
    with _pc_inst:
        st.markdown("**Institutional lattice · domains within Zazzau nodes**")
        for row in KADUNA_INSTITUTIONS:
            if int(row.get("sovereign_air_before_px") or 0) > 0:
                st.markdown(
                    '<div class="kgec-sovereign-air-96" aria-hidden="true"></div>',
                    unsafe_allow_html=True,
                )
            _ot = str(row.get("ownership_tier") or "").upper()
            if _ot == "FED":
                st.markdown(
                    '<p class="kgec-inst-ownership-fed">[FED] Federal ownership · Goldman seal</p>',
                    unsafe_allow_html=True,
                )
            elif _ot == "STA":
                st.markdown(
                    '<p class="kgec-inst-ownership-sta">[STA] Kaduna State Government · Goldman seal</p>',
                    unsafe_allow_html=True,
                )
            if row.get("campuses"):
                _reg = html.escape(row["regulator"])
                st.markdown(
                    f"<h4 class='kgec-nuba-heritage-head'>{html.escape(row['name'])} "
                    f"<span class='kgec-nuba-abbr'>({html.escape(row['abbr'])})</span></h4>"
                    f"<p class='kgec-nuba-sub'><code>[{_reg}]</code> · NBTE · lattice weld by campus</p>",
                    unsafe_allow_html=True,
                )
                if row.get("note"):
                    st.caption(str(row.get("note") or ""))
                for camp in row.get("campuses") or []:
                    _clp = lga_pcode_lookup(_wards_fc_kd, camp.get("lga_weld") or "")
                    _cz = camp.get("zazzau_districts") or []
                    _anchor = str(camp.get("district_anchor_en") or "").strip()
                    if _cz:
                        _cz_line = " · ".join(html.escape(str(x)) for x in _cz)
                    elif _anchor:
                        _cz_line = html.escape(_anchor)
                    else:
                        _cz_line = "— (southern node · not Zazzau-31)"
                    _dom = html.escape(str(camp.get("traditional_domain") or ""))
                    st.markdown(
                        f"<div class='kgec-nuba-campus-card'>"
                        f"<p class='kgec-nuba-campus-title'>{html.escape(str(camp.get('campus_title') or 'Campus'))}</p>"
                        f"<p><strong>LGA</strong> {html.escape(str(camp.get('lga_weld') or ''))} · "
                        f"<code>ADM2_PCODE {html.escape(str(_clp))}</code></p>"
                        f"<p><strong>Ancestral / statutory domain:</strong> {_dom}</p>"
                        f"<p><strong>Zazzau district weld:</strong> {_cz_line}</p>"
                        f"<p class='kgec-nuba-pulse-note'><em>{html.escape(str(camp.get('me_anguwa_pressure_note') or ''))}</em></p>"
                        "</div>",
                        unsafe_allow_html=True,
                    )
                continue
            _lp = lga_pcode_lookup(_wards_fc_kd, row["lga_weld"])
            _tag = row.get("subtag")
            _reg = html.escape(row["regulator"]) + (f" · {html.escape(_tag)}" if _tag else "")
            _doms = row.get("zazzau_districts") or []
            _dom_line = " · ".join(html.escape(str(x)) for x in _doms) if _doms else "—"
            _subreg = row.get("regulator_subline")
            _sov = bool(row.get("sovereign_asset_node"))
            if _sov:
                _parts = [
                    '<div class="kgec-sovereign-inst-node">',
                    '<p class="kgec-sovereign-asset-cap">Sovereign node · Zaria Hanwa ZD02</p>',
                    "<p>- "
                    f"<strong>{html.escape(row['name'])}</strong> "
                    f"({html.escape(row['abbr'])}) "
                    f"<code>[{_reg}]</code> · "
                    f"LGA <strong>{html.escape(row['lga_weld'])}</strong> · "
                    f"<code>ADM2_PCODE {html.escape(str(_lp))}</code></p>",
                    f"<p><strong>Zazzau districts:</strong> {_dom_line}</p>",
                ]
                if _subreg:
                    _parts.append(f"<p><em>{html.escape(_subreg)}</em></p>")
                _parts.append(f"<p><em>{html.escape(row.get('note') or '')}</em></p></div>")
                st.markdown("\n".join(_parts), unsafe_allow_html=True)
            else:
                _body_lines = [
                    f"- **{html.escape(row['name'])}** ({html.escape(row['abbr'])}) `[{_reg}]` · "
                    f"LGA **{html.escape(row['lga_weld'])}** · `ADM2_PCODE {_lp}`  ",
                    f"  **Zazzau districts:** {_dom_line}  ",
                ]
                if _subreg:
                    _body_lines.append(f"  _{html.escape(_subreg)}_")
                _body_lines.append(f"  _{html.escape(row.get('note') or '')}_")
                st.markdown("\n".join(_body_lines))
            for sub in row.get("poly_colleges") or []:
                _slp = lga_pcode_lookup(_wards_fc_kd, sub["lga_weld"])
                _sd = sub.get("zazzau_districts") or []
                _sd_line = " · ".join(html.escape(str(x)) for x in _sd) if _sd else "—"
                st.markdown(
                    f"  - **{html.escape(sub['name'])}** ({html.escape(sub['abbr'])}) · "
                    f"LGA **{html.escape(sub['lga_weld'])}** · `ADM2_PCODE {_slp}`  \n"
                    f"    **District weld:** {_sd_line}  \n"
                    f"    _{html.escape(sub.get('note') or '')}_"
                )

    with _pc_trad:
        st.markdown("**Zazzau eleven-LGA domain · hard-weld (ADM2_PCODE from spine)**")
        st.caption(
            "Ancestral command on the AZK corridor — Human API foreground: Me Anguwa "
            "Sovereign Clearance, Registry of Strangers vetting, and SPT frontier trace "
            "bind the Emirate lattice into Total Reality. "
            + ZAZZAU_ELEVEN_SOURCE_NOTE
        )
        _z11 = build_zazzau_eleven_lga_weld_rows(
            _wards_fc_kd,
            _phase2.get("spine_df") if _phase2 else None,
        )
        st.dataframe(
            [
                {
                    "LGA": r["lga_en"],
                    "ADM2_PCODE": r["adm2_pcode"],
                    "Wards (spine)": f'{int(r["ward_polygons_in_lga"]):,}',
                    "District nodes": f'{int(r["district_nodes_in_lga"]):,}',
                }
                for r in _z11
            ],
            hide_index=True,
            use_container_width=True,
            height=min(420, 42 + 28 * max(6, len(_z11))),
            column_config={
                "LGA": st.column_config.TextColumn("LGA", width=160),
                "ADM2_PCODE": st.column_config.TextColumn("ADM2_PCODE", width=120),
                "Wards (spine)": st.column_config.TextColumn("Wards (spine)", width=130),
                "District nodes": st.column_config.TextColumn("District nodes", width=130),
            },
        )
        st.markdown("**Zazzau 31 · ancestral district cascade**")
        st.caption(DISTRICT_LEDGER_NOTE)
        _z31_li = "".join(
            f"<li><code>{html.escape(d['district_id'])}</code> · {html.escape(d['district_en'])} "
            f"<span style='opacity:0.82'>→ {html.escape(d['parent_lga_en'])}</span></li>"
            for d in ZAZZAU_THIRTY_ONE_DISTRICTS
        )
        st.markdown(
            f'<div class="kgec-zazzau-31-scroll" role="region" aria-label="Zazzau thirty-one districts">'
            f'<ol class="kgec-zazzau-31-ol">{_z31_li}</ol></div>',
            unsafe_allow_html=True,
        )
        st.markdown("**Modern statutory lattice · GLASS (not Emirate apex)**")
        st.caption(
            "Warrant-chief discipline — Local Government Chairmen and council appointees exercise "
            "**constitutional / delegated** mandates; they do **not** carry Zazzau ancestral decree unless "
            "separately titled by Emirate chancellery."
        )
        for _mx in KADUNA_MODERN_STATUTORY_LATTICE:
            st.markdown(
                '<div class="kgec-modern-statutory-card">'
                '<p class="kgec-modern-statutory-cap">Administrative node · modern state</p>'
                f"<p><strong>{html.escape(_mx['office'])}</strong> · "
                f"<code>{html.escape(_mx['badge'])}</code></p>"
                f"<p><em>Domain:</em> {html.escape(_mx['domain'])}</p>"
                f"<p><em>{html.escape(_mx['note'])}</em></p>"
                "</div>",
                unsafe_allow_html=True,
            )
        st.markdown("**Council of Chiefs · STEEL · ancestral command lineage**")
        st.caption(
            "Indirect Rule clarity — Emirs and titled chiefs sit in **ancestral command** precedence "
            "(Traditional Apex); contrast with the statutory lattice above."
        )
        for _ch in KADUNA_CHIEFS_COUNCIL_PRECEDENCE:
            st.markdown(
                '<div class="kgec-ancestral-command-row">'
                f"<p><code>{html.escape(_ch['badge'])}</code> "
                f"<strong>{html.escape(_ch['title'])}</strong></p>"
                f"<p><em>Domain:</em> {html.escape(_ch['domain'])} · "
                f"<code>Rank: {html.escape(_ch['rank'])}</code></p>"
                "</div>",
                unsafe_allow_html=True,
            )
        st.markdown("**Zazzau ancestral command · pilot ledger**")
        _zw = ward_count_for_lga(_wards_fc_kd, "Zaria")
        _kad_tot = kaduna_state_ward_total(_wards_fc_kd)
        st.markdown(
            f"- **Apex:** {html.escape(ZAZZAU_APEX['title'])} · _{html.escape(ZAZZAU_APEX['role'])}_\n"
            f"- **District ledger nodes:** {int(ZAZZAU_APEX['district_nodes']):,}\n"
            f"- **Village heads (pilot ledger):** {int(ZAZZAU_APEX['village_heads']):,}\n"
            f"- **Masu Unguwanni (pilot ledger):** {int(ZAZZAU_APEX['masu_unguwanni']):,}\n"
            f"- **Zaria LGA ward polygons (8,806 spine):** {_zw:,}\n"
            f"- **Kaduna ADM1 ward polygons (same spine):** {_kad_tot:,}"
        )
        st.caption(ZAZZAU_APEX.get("ledger_note") or "")


__all__ = ["load_phase2_spine_bundle_kaduna_portrait", "render_kaduna_map_twin_portrait"]
