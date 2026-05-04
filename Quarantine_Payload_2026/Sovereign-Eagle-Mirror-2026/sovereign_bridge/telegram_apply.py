"""
Apply queued Telegram commands to Streamlit session_state (K-GEC map + Gold Man).

Run from the Mirror process only — reads same SQLite queue as sovereign_telegram_gateway.
"""

from __future__ import annotations

import html
import json
import os
from typing import Any

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from kysah_sovereign_alert import (
    kysah_area_token,
    kysah_distress_records,
    kysah_home_token,
    load_kysah_stub_records,
)
from sovereign_active_intel import (
    build_total_reality_summary,
    canonical_state_name,
    state_label_from_props,
)
from sovereign_bridge.ingress_hooks import default_ingress_registry
from sovereign_bridge.prism_telegram_copy import format_prism_telegram_html, prism_lines_from_summary
from sovereign_bridge.telegram_notify import send_message_html
from sovereign_bridge.telegram_store import default_sqlite_path, mark_applied, peek_next_pending
from sovereign_nl_query import resolve_sovereign_nl_query


def _allowed_chat(chat_id: int) -> bool:
    raw = (os.environ.get("TELEGRAM_BRIDGE_ALLOWED_CHAT_IDS") or "").strip()
    if not raw:
        return True
    ok = {int(x.strip()) for x in raw.split(",") if x.strip().isdigit()}
    return int(chat_id) in ok


def _catalog_states(fused_df: pd.DataFrame | None) -> list[str]:
    if fused_df is not None and "state" in fused_df.columns:
        return sorted(fused_df["state"].astype(str).unique().tolist())
    from sovereign_active_intel import STATE_CODE_TO_STATE

    return list(STATE_CODE_TO_STATE.values())


def _geom_centroid_latlon(geom: dict[str, Any]) -> tuple[float, float] | None:
    rings: list[list[Any]] = []
    gtype = geom.get("type")
    coords = geom.get("coordinates")
    if gtype == "Polygon" and isinstance(coords, list) and coords:
        rings.append(coords[0])
    elif gtype == "MultiPolygon" and isinstance(coords, list):
        for poly in coords:
            if isinstance(poly, list) and poly:
                rings.append(poly[0])
    if not rings:
        return None
    lat_sum, lon_sum, n = 0.0, 0.0, 0
    for ring in rings:
        for pt in ring:
            if isinstance(pt, (list, tuple)) and len(pt) >= 2:
                lon_sum += float(pt[0])
                lat_sum += float(pt[1])
                n += 1
    if not n:
        return None
    return lat_sum / n, lon_sum / n


def _centroid_for_state(
    state_canon: str,
    *,
    states_geojson: dict[str, Any] | None,
    fused_df: pd.DataFrame | None,
) -> tuple[float, float] | None:
    if not states_geojson:
        return None
    catalog = _catalog_states(fused_df)
    for feat in states_geojson.get("features") or []:
        if not isinstance(feat, dict):
            continue
        props = feat.get("properties") or {}
        if not isinstance(props, dict):
            props = {}
        raw = state_label_from_props(props)
        if canonical_state_name(raw, catalog) != state_canon:
            continue
        geom = feat.get("geometry")
        if not isinstance(geom, dict):
            continue
        c = _geom_centroid_latlon(geom)
        if c:
            return c
    return None


def _parse_command(text: str) -> tuple[str, str]:
    t = (text or "").strip()
    if not t:
        return "noop", ""
    parts = t.split(maxsplit=1)
    cmd = parts[0].strip().lower()
    rest = parts[1].strip() if len(parts) > 1 else ""
    if "@" in cmd:
        cmd = cmd.split("@", 1)[0].strip().lower()
    return cmd, rest


def _build_sa_alert_patrol_bundle(rec: dict[str, Any]) -> dict[str, Any]:
    """Parent-window patrol JSON — eagle banks to distress Area→Home with 2.1s glide."""
    from sovereign_bridge.sentinel_geo import latlon_to_nigeria_fraction

    lat = float(rec["lat"])
    lon = float(rec["lon"])
    pt = latlon_to_nigeria_fraction(lat, lon)
    targets = [dict(pt) for _ in range(14)]
    weights = [0.97] * 14
    stn = str(rec.get("state") or "?").strip()
    area = kysah_area_token(rec)
    home = kysah_home_token(rec)
    return {
        "targets": targets,
        "targetWeights": weights,
        "sniffs": [
            f"SA_ALERT · Sovereign student alert · {stn} · Area {area} · Home {home} · "
            f"2.1s banking glide — K-GEC Sentinel ACK",
        ],
        "kysahSentinelOverride": True,
        "glideMs": 2100,
    }


def _help_text() -> str:
    return (
        "<b>Sovereign Bridge · K-GEC</b><br/>"
        "<code>/state Kaduna</code> — Gold Man monument + map pivot<br/>"
        "<code>/nl …</code> — same resolver as sidebar NL pivot<br/>"
        "<code>/sa_alert</code> or <code>/sa_alert Nasarawa</code> — eagle banks to Area→Home (2.1s glide)<br/>"
        "<code>/ping</code> — lattice heartbeat<br/>"
        "Alphabet standard: every reply uses vertical 🟡→🔵→⚪→🔴 monument order."
    )


def apply_pending_bridge_commands(
    *,
    fused_df: pd.DataFrame | None,
    national_pu_df: pd.DataFrame | None,
    fin_points: list[dict],
    trade_nodes: list[dict],
    ngecc_reg: dict[str, Any],
    states_geojson: dict[str, Any] | None,
    ncc_rows: list[dict],
    signal_rows: list[dict],
    ntw_proxy: dict[str, Any],
    store_path: Any | None = None,
) -> int:
    """
    Claim at most one pending Telegram update and apply to session_state.
    Returns 1 if applied, 0 otherwise.
    """
    path = store_path or default_sqlite_path()
    row = peek_next_pending(path)
    if not row:
        return 0
    uid = int(row["update_id"])
    chat_id = int(row["chat_id"])
    if not _allowed_chat(chat_id):
        send_message_html(chat_id=chat_id, html_body="<b>Sovereign Bridge</b><br/>chat not allowlisted.")
        mark_applied(uid, path)
        return 1
    text = str(row.get("text") or "")
    cmd, rest = _parse_command(text)
    reg = default_ingress_registry()
    extra_footer = reg.augment_prism_footer_lines()

    if cmd in ("/start", "/help"):
        send_message_html(chat_id=chat_id, html_body=_help_text())
        mark_applied(uid, path)
        return 1
    if cmd == "/ping":
        body = format_prism_telegram_html(
            title="Sovereign Bridge · PING",
            gold_line="GCSLC lattice armed",
            cyan_line="K-GEC mirror session live",
            white_line="PU national comparator channel open",
            red_line="Forensic heart · INEC scale-3 standby",
            footer_lines=extra_footer or None,
        )
        send_message_html(chat_id=chat_id, html_body=body)
        mark_applied(uid, path)
        return 1

    if cmd == "/state":
        if not rest:
            send_message_html(chat_id=chat_id, html_body="<b>Sovereign Bridge</b>\nusage: <code>/state Kaduna</code>")
            mark_applied(uid, path)
            return 1
        catalog = _catalog_states(fused_df)
        canon = canonical_state_name(rest, catalog)
        summary = build_total_reality_summary(
            canon,
            fused_df=fused_df,
            national_pu_df=national_pu_df,
            ncc_rows=ncc_rows,
            signal_rows=signal_rows,
            fin_points=fin_points,
            states_geojson=states_geojson,
            ntw_proxy=ntw_proxy,
        )
        st.session_state["total_reality_last"] = summary
        st.session_state["smart_click_total_reality"] = True
        ctr = _centroid_for_state(canon, states_geojson=states_geojson, fused_df=fused_df)
        if ctr:
            st.session_state["gv_center"] = (ctr[0], ctr[1])
            st.session_state["gv_zoom"] = 6.85
        n_pu_nat = int(summary.get("national_pu_total") or 176_846)
        g, cy, w, rd = prism_lines_from_summary(summary, national_pu_total=n_pu_nat)
        body = format_prism_telegram_html(
            title=f"Total Reality · {canon}",
            gold_line=g,
            cyan_line=cy,
            white_line=w,
            red_line=rd,
            footer_lines=extra_footer or None,
        )
        send_message_html(chat_id=chat_id, html_body=body)
        mark_applied(uid, path)
        return 1

    if cmd == "/nl":
        if not rest:
            send_message_html(
                chat_id=chat_id,
                html_body="<b>Sovereign Bridge</b><br/>usage: <code>/nl query…</code>",
            )
            mark_applied(uid, path)
            return 1
        nl = resolve_sovereign_nl_query(
            rest,
            fin_points,
            trade_points=trade_nodes,
            ngecc_reg=ngecc_reg,
            national_pu_df=national_pu_df,
        )
        if not nl:
            send_message_html(
                chat_id=chat_id,
                html_body="<b>Sovereign Bridge · NL</b><br/>No match — refine lattice tokens.",
            )
            mark_applied(uid, path)
            return 1
        st.session_state["gv_center"] = (float(nl["lat"]), float(nl["lon"]))
        st.session_state["gv_zoom"] = float(nl.get("zoom") or 9.0)
        st.session_state["sovereign_nl_last"] = nl
        if str(nl.get("intent") or "") == "top_pos_density":
            zt = str(nl.get("zone_token") or "").strip().lower()
            if zt:
                st.session_state["_nl_fin_zone_token"] = zt
            else:
                st.session_state.pop("_nl_fin_zone_token", None)
        else:
            st.session_state.pop("_nl_fin_zone_token", None)
        head = str(nl.get("headline") or "NL pivot")
        det = str(nl.get("detail") or "")
        body = format_prism_telegram_html(
            title="Sovereign NL · Remote pivot",
            gold_line=head[:220],
            cyan_line=det[:220] if det else "cyan channel idle",
            white_line=f"lat {nl['lat']:.4f} · lon {nl['lon']:.4f} · z {nl.get('zoom')}",
            red_line="Map viewport committed · mirror sync on next paint",
            footer_lines=extra_footer or None,
        )
        send_message_html(chat_id=chat_id, html_body=body)
        mark_applied(uid, path)
        return 1

    if cmd in ("/sa_alert", "/saalert"):
        distress = kysah_distress_records(load_kysah_stub_records())
        rest_key = rest.strip().lower() if rest else ""
        pool = distress
        if rest_key:
            pool = [
                r
                for r in distress
                if str(r.get("state") or "").strip().lower() == rest_key
            ]
        if not pool:
            body = format_prism_telegram_html(
                title="SA_ALERT · No distress bind",
                gold_line="No KYSAH distress rows in stub for this filter",
                cyan_line="Mount live JSONL ingest or add stub rows",
                white_line="Queue drained · mirror idle",
                red_line="Eagle patrol unchanged · awaiting Area→Home signal",
                footer_lines=extra_footer or None,
            )
            send_message_html(chat_id=chat_id, html_body=body)
            mark_applied(uid, path)
            return 1
        rec = pool[0]
        st.session_state["gv_center"] = (float(rec["lat"]), float(rec["lon"]))
        st.session_state["gv_zoom"] = 8.6
        st.session_state["smart_click_total_reality"] = True
        stn = str(rec.get("state") or "").strip()
        if stn:
            try:
                summary = build_total_reality_summary(
                    stn,
                    fused_df=fused_df,
                    national_pu_df=national_pu_df,
                    ncc_rows=ncc_rows,
                    signal_rows=signal_rows,
                    fin_points=fin_points,
                    states_geojson=states_geojson,
                    ntw_proxy=ntw_proxy,
                )
                st.session_state["total_reality_last"] = summary
            except Exception:
                st.session_state.pop("total_reality_last", None)
        bundle = _build_sa_alert_patrol_bundle(rec)
        components.html(
            "<script>try{var p=window.parent;var d="
            + json.dumps(bundle)
            + ";if(p&&p.__kgecSetPatrol)p.__kgecSetPatrol(d);}catch(e){}</script>",
            height=0,
            width=0,
        )
        area = kysah_area_token(rec)
        home = kysah_home_token(rec)
        body = format_prism_telegram_html(
            title="SA_ALERT · Sentinel sync",
            gold_line=f"State / FCT · {stn or 'Sovereign mesh'}",
            cyan_line=f"Area (LGA vicinage) · {area}",
            white_line=f"Home (PU mesh token) · {home}",
            red_line="Eagle patrol · 2.1s banking glide · map viewport locked to distress",
            footer_lines=extra_footer or None,
        )
        send_message_html(chat_id=chat_id, html_body=body)
        mark_applied(uid, path)
        return 1

    send_message_html(
        chat_id=chat_id,
        html_body=(
            f"<b>Sovereign Bridge</b><br/>unknown command <code>{html.escape(cmd)}</code><br/><br/>"
            f"{_help_text()}"
        ),
    )
    mark_applied(uid, path)
    return 1
