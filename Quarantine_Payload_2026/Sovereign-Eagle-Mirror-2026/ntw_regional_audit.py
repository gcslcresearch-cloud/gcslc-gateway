"""
NTW Regional Corridor Audit — Plotly grouped bars (coverage vs SIM verification).
Brand colours only (lettermarks in UI) — Sovereign Eagle Mirror 2026.
"""

from __future__ import annotations

import hashlib
import html
import json
import math
from pathlib import Path
from typing import Any

# Identity-inspired palette (vector-safe; replace with official artwork where licensed)
NTW_BRAND_HEX: dict[str, str] = {
    "MTN": "#FFCB05",
    "Airtel": "#ED1C24",
    "Glo": "#00A859",
    "9mobile": "#00843D",
}


def load_ntw_regional_audit(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"corridors": [], "meta": {}}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"corridors": [], "meta": {}}


def build_ntw_corridor_figure(blob: dict[str, Any]) -> Any:
    """Return Plotly figure or None if plotly missing."""
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
    except ImportError:
        return None

    rows_data = blob.get("corridors") or []
    if not rows_data:
        return None

    labels = [str(r.get("label") or r.get("id") or "?") for r in rows_data]
    ops_order = ["MTN", "Airtel", "Glo", "9mobile"]

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            "Radio / site coverage proxy (%)",
            "SIM verification proxy (%)",
        ),
        horizontal_spacing=0.08,
    )

    for op in ops_order:
        y_cov: list[float] = []
        y_sim: list[float] = []
        for r in rows_data:
            od = (r.get("operators") or {}).get(op) or {}
            try:
                y_cov.append(float(od.get("coverage_pct", 0)))
            except (TypeError, ValueError):
                y_cov.append(0.0)
            try:
                y_sim.append(float(od.get("sim_verification_pct", 0)))
            except (TypeError, ValueError):
                y_sim.append(0.0)
        color = NTW_BRAND_HEX.get(op, "#888888")
        fig.add_trace(
            go.Bar(
                name=op,
                x=labels,
                y=y_cov,
                marker_color=color,
                marker_line=dict(width=0.6, color="rgba(0,0,0,0.35)"),
                legendgroup=op,
                showlegend=True,
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Bar(
                name=op,
                x=labels,
                y=y_sim,
                marker_color=color,
                marker_line=dict(width=0.6, color="rgba(0,0,0,0.35)"),
                legendgroup=op,
                showlegend=False,
            ),
            row=1,
            col=2,
        )

    fig.update_layout(
        barmode="group",
        height=420,
        margin=dict(l=48, r=24, t=48, b=120),
        paper_bgcolor="rgba(0,0,128,0.42)",
        plot_bgcolor="rgba(0,0,128,0.28)",
        font=dict(color="rgba(240,244,255,0.92)", size=11),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(0,0,128,0.55)",
            bordercolor="rgba(212,175,55,0.35)",
            borderwidth=1,
        ),
        title=dict(
            text="NTW · 6 regional corridors (forensic staging)",
            font=dict(size=13, color="#D4AF37"),
            x=0.5,
            xanchor="center",
        ),
    )
    fig.update_xaxes(tickangle=-35, row=1, col=1)
    fig.update_xaxes(tickangle=-35, row=1, col=2)
    fig.update_yaxes(range=[0, 105], row=1, col=1)
    fig.update_yaxes(range=[0, 105], row=1, col=2)
    return fig


def ntw_single_lettermark_html(operator: str) -> str:
    """Single NTW lettermark — column header (compact)."""
    hx = NTW_BRAND_HEX.get(operator, "#888888")
    tc = "#000000" if operator == "MTN" else "#f8fafc"
    return (
        "<div style='text-align:center;margin-bottom:8px;'>"
        f"<span style='display:inline-block;padding:6px 14px;border-radius:8px;"
        f"background:{hx};color:{tc};font-weight:900;font-size:0.85rem;"
        f"letter-spacing:0.06em;border:1px solid rgba(212,175,55,0.45);"
        f"box-shadow:0 2px 8px rgba(0,0,0,0.35);'>{operator}</span></div>"
    )


def ntw_big4_lettermarks_row_html() -> str:
    """High-contrast Big 4 row — first visual below the hero map (iPhone-safe)."""
    ops_order = ["MTN", "Airtel", "Glo", "9mobile"]
    chips: list[str] = []
    for op in ops_order:
        hx = NTW_BRAND_HEX.get(op, "#888888")
        tc = "#0a0a0a" if op == "MTN" else "#ffffff"
        outline = "rgba(0,0,0,0.92)" if op == "MTN" else "rgba(255,255,255,0.35)"
        chips.append(
            "<span class='sovereign-ntw-chip' style="
            f"'flex:1 1 0;min-width:0;text-align:center;display:block;padding:10px 8px;"
            f"border-radius:10px;background:{hx};color:{tc};font-weight:900;"
            f"font-size:clamp(0.72rem,3.8vw,0.95rem);letter-spacing:0.04em;"
            f"border:2px solid {outline};box-shadow:0 0 0 1px rgba(212,175,55,0.55),"
            f"0 4px 14px rgba(0,0,0,0.45);text-shadow:0 1px 2px rgba(0,0,0,0.25);'"
            f">{op}</span>"
        )
    inner = "".join(chips)
    return (
        "<div class='sovereign-ntw-big4' role='region' aria-label='NTW Big 4 operators'>"
        "<div class='sovereign-ntw-big4-inner'>"
        f"{inner}"
        "</div></div>"
    )


def _operator_corridor_means(blob: dict[str, Any], operator: str) -> tuple[float, float]:
    """Mean coverage % and SIM verification % for one operator across corridors."""
    rows_data = blob.get("corridors") or []
    cvs: list[float] = []
    sms: list[float] = []
    for r in rows_data:
        od = (r.get("operators") or {}).get(operator) or {}
        try:
            cvs.append(float(od.get("coverage_pct", 0)))
        except (TypeError, ValueError):
            pass
        try:
            sms.append(float(od.get("sim_verification_pct", 0)))
        except (TypeError, ValueError):
            pass
    cov_m = sum(cvs) / len(cvs) if cvs else 0.0
    sim_m = sum(sms) / len(sms) if sms else 0.0
    return cov_m, sim_m


def html_ntw_resonance_push_inject(
    operator: str,
    audit_blob: dict[str, Any],
    proxy_blob: dict[str, Any],
) -> str:
    """Forced-visible operator banner — eliminates empty/black perception on Big-4 click."""
    cov_m, sim_m = _operator_corridor_means(audit_blob, operator)
    rows_data = audit_blob.get("corridors") or []
    n_corr = len(rows_data)
    raw_def = proxy_blob.get("default") if isinstance(proxy_blob.get("default"), dict) else {}
    try:
        sub_pct = float(raw_def.get(operator) or 0.0) * 100.0
    except (TypeError, ValueError):
        sub_pct = 0.0
    hex_c = NTW_BRAND_HEX.get(operator, "#888888")
    op_esc = html.escape(operator)
    line = (
        f"PUSH · {operator} · National Resonance LIVE · corridor RAN μ {cov_m:.1f}% · "
        f"SIM μ {sim_m:.1f}% · audit rows {n_corr} · modeled subscriber share {sub_pct:.1f}%"
    )
    mq = _kgec_marquee_pair(line, seconds=88.0)
    return (
        "<div class='ntw-push-inject' role='status' "
        f"style='--ntw-push-accent:{hex_c};border-left:4px solid {hex_c};'>"
        "<div class='ntw-push-inject-op'>" + op_esc + "</div>"
        "<div class='ntw-push-inject-body'>" + mq + "</div>"
        "</div>"
    )


def _kgec_marquee_pair(text: str, seconds: float = 22.0) -> str:
    """Dual-span horizontal slow ticker (seamless loop; GPU-friendly transform).

    ``seconds`` may be passed positionally or by keyword (Chairman widgets must not throw TypeError).
    """
    esc = html.escape(text)
    dur = max(32.0, min(120.0, float(seconds)))
    return (
        "<span class='kgec-mq' style='"
        f"--kgec-mq-dur:{dur:.1f}s"
        "'><span class='kgec-mq-track'><span>"
        f"{esc}</span><span aria-hidden='true'>{esc}</span></span></span>"
    )


def html_ntw_meter_strip_row(audit_blob: dict[str, Any]) -> str:
    """Four horizontal CSS meter bars + slow-motion RAN/SIM tickers."""
    ops_order = ["MTN", "Airtel", "Glo", "9mobile"]
    cells: list[str] = []
    for i, op in enumerate(ops_order):
        cov_m, sim_m = _operator_corridor_means(audit_blob, op)
        hx = NTW_BRAND_HEX.get(op, "#888")
        fill_pct = min(100.0, max(0.0, (cov_m * 0.55 + sim_m * 0.45)))
        sub_txt = f"RAN {cov_m:.0f}% · SIM {sim_m:.0f}% · SPECTRUM · BROADBAND"
        mq = _kgec_marquee_pair(sub_txt, seconds=38.0 + (i % 4) * 4.5)
        op_kinetic = _kgec_marquee_pair(
            f"{op} · BIG-4 · RESONANCE · METER · RAN/SIM · {op} live deck",
            seconds=44.0 + (i % 5) * 3.2,
        )
        cells.append(
            "<div class='ntw-meter-cell'>"
            f"<div class='ntw-meter-label ntw-meter-label-mq' style='color:{hx};'>{op_kinetic}</div>"
            "<div class='ntw-meter-track'>"
            f"<div class='ntw-meter-fill' style='width:{fill_pct:.1f}%;background:{hx};"
            "box-shadow:0 0 12px rgba(0,229,255,0.35);'></div>"
            "</div>"
            f"<div class='ntw-meter-sub'><div class='ntw-meter-mq-shell'>{mq}</div></div>"
            "</div>"
        )
    return (
        "<div class='national-resonance-meterdeck' aria-label='K-GEC · Komi-Generative Cloud · meter deck'>"
        "<div class='ntw-meter-strip' role='group'>"
        + "".join(cells)
        + "</div></div>"
    )


def html_ntw_resonance_typewriter_stream(
    operator: str,
    audit_blob: dict[str, Any],
    proxy_blob: dict[str, Any],
    *,
    audit_path: Path | None = None,
) -> str:
    """
    National Resonance Chamber · cyan–green forensic stream (staggered reveal via CSS).
    Always includes an AUDIT_FEED line when audit_path is set (live disk → stream; never blank).
    """
    rows_data = audit_blob.get("corridors") or []

    cov_m, sim_m = _operator_corridor_means(audit_blob, operator)
    raw_sub = (proxy_blob.get("default") or {}).get(operator)
    try:
        pct_sub = float(raw_sub) * 100.0 if raw_sub is not None else 25.0
    except (TypeError, ValueError):
        pct_sub = 25.0

    all_cov: list[float] = []
    op_covs: list[float] = []
    for r in rows_data:
        if not isinstance(r, dict):
            continue
        for op in ("MTN", "Airtel", "Glo", "9mobile"):
            od = (r.get("operators") or {}).get(op) or {}
            try:
                v = float(od.get("coverage_pct", 0))
            except (TypeError, ValueError):
                v = 0.0
            all_cov.append(v)
            if op == operator:
                op_covs.append(v)
    nat_ran_mean = sum(all_cov) / len(all_cov) if all_cov else 0.0
    delta_pp = cov_m - nat_ran_mean
    sig = hashlib.sha256(
        f"{operator}|{len(rows_data)}|{cov_m:.4f}".encode()
    ).hexdigest()[:20].upper()

    def _sigma(xs: list[float]) -> float:
        if len(xs) < 2:
            return 0.0
        m = sum(xs) / len(xs)
        var = sum((x - m) ** 2 for x in xs) / len(xs)
        return math.sqrt(var)

    sig_ran = _sigma(op_covs)

    lines: list[str] = []
    lines.append(html_ntw_resonance_push_inject(operator, audit_blob, proxy_blob))
    li = 0
    # Instant ignition — entire row kinetic (no static glyphs in Resonance Chamber).
    _ign_lbl = _kgec_marquee_pair(
        "IGNITION · K-GEC · CHAMBER · RESONANCE ARMED · SOVEREIGN DECK",
        seconds=48.0,
    )
    _ign_body = _kgec_marquee_pair(
        f"{operator} · RESONANCE LIVE · SUBSCRIBER_BASE · SPECTRUM · BROADBAND · corridor audit binding · pivot LIVE",
        seconds=56.0,
    )
    lines.append(
        "<div class='ntw-tw-instant' role='status' aria-live='polite'>"
        "<span class='ntw-tw-k ntw-tw-k-mq'>" + _ign_lbl + "</span>"
        "<span class='ntw-tw-v ntw-tw-v-mq'>" + _ign_body + "</span>"
        "</div>"
    )

    def _tw(extra_class: str, inner: str) -> None:
        nonlocal li
        li += 1
        ec = f" {extra_class}" if extra_class else ""
        lines.append(
            f"<div class='ntw-tw-line{ec}' style='--tw-i:{li}'>{inner}</div>"
        )

    if audit_path is not None:
        if audit_path.is_file():
            st = audit_path.stat()
            feed_raw = (
                f"LIVE_DISK {audit_path.name} · corridors={len(rows_data)} · "
                f"bytes={st.st_size} · mtime_epoch={int(st.st_mtime)} · "
                "K-GEC pulls this file on every resonance ignition"
            )
        else:
            feed_raw = (
                f"FILE_MISSING {audit_path} — place Part_01_Telecom/data/ntw_regional_corridor_audit.json "
                "for full corridor rain"
            )
    else:
        feed_raw = (
            "AUDIT_PATH_UNBOUND — bind ntw_regional_corridor_audit.json for Chairman-grade forensic stream"
        )
    _tw(
        "ntw-audit-feed",
        "<span class='ntw-tw-k'>AUDIT_FEED</span>"
        f"<span class='ntw-tw-v'>{_kgec_marquee_pair(feed_raw, seconds=68.0)}</span>",
    )

    head_v = _kgec_marquee_pair(
        f"Komi-Generative Cloud · CHAMBER · {operator} · SECURED · SUBSCRIBER · SPECTRUM · BROADBAND",
        seconds=58.0,
    )
    _tw(
        "ntw-tw-head",
        "<span class='ntw-tw-k'>K-GEC</span> "
        f"<span class='ntw-tw-v'>{head_v}</span>",
    )
    _tw(
        "",
        "<span class='ntw-tw-k'>FORENSIC_SIG</span> "
        f"<span class='ntw-tw-v'>{_kgec_marquee_pair(f'SHA256-proxy · {sig} · rows={len(rows_data)}', seconds=52.0)}</span>",
    )
    _tw(
        "",
        "<span class='ntw-tw-k'>SUBSCRIBER_BASE</span> "
        f"<span class='ntw-tw-v'>{_kgec_marquee_pair(f'modeled national mass share → {pct_sub:.2f}% · registry: state_ntw_operator_proxy.json · NCC audit path pending', seconds=54.0)}</span>",
    )
    _tw(
        "",
        "<span class='ntw-tw-k'>SPECTRUM_STACK</span> "
        f"<span class='ntw-tw-v'>{_kgec_marquee_pair(f'LTE/NR RAN aggregate {cov_m:.2f}% · SIM reg {sim_m:.2f}% · Δ vs Big-4 RAN mean {delta_pp:+.2f} pp · corridor σ={sig_ran:.2f}', seconds=50.0)}</span>",
    )
    _tw(
        "",
        "<span class='ntw-tw-k'>BENCHMARK</span> "
        f"<span class='ntw-tw-v'>{_kgec_marquee_pair(f'national RAN sample mean (all ops×corridors) = {nat_ran_mean:.2f}%', seconds=46.0)}</span>",
    )
    _tw(
        "ntw-tw-div",
        "<span class='ntw-tw-k'>BROADBAND_COVERAGE</span> "
        f"<span class='ntw-tw-v'>{_kgec_marquee_pair('six-corridor disaggregation · forensic staging · corridor rain', seconds=62.0)}</span>",
    )
    if not rows_data:
        _tw(
            "",
            "<span class='ntw-tw-k'>REGISTRY</span> "
            "<span class='ntw-tw-v'>"
            + _kgec_marquee_pair(
                "corridor audit JSON has no rows — mount Part_01_Telecom/data/ntw_regional_corridor_audit.json",
                seconds=58.0,
            )
            + "</span>",
        )
    for j, r in enumerate(rows_data):
        if not isinstance(r, dict):
            continue
        cid = str(r.get("id") or "?")
        lab = str(r.get("label") or r.get("id") or "?")
        od = (r.get("operators") or {}).get(operator) or {}
        try:
            c = float(od.get("coverage_pct", 0))
        except (TypeError, ValueError):
            c = 0.0
        try:
            s = float(od.get("sim_verification_pct", 0))
        except (TypeError, ValueError):
            s = 0.0
        gap = c - s
        mq_dur = 42.0 + (j % 9) * 2.8
        row_raw = f"RAN {c:.1f}% │ SIM {s:.1f}% │ Δ(reg) {gap:+.1f} pp │ {lab} · [{cid}] · forensic corridor"
        _tw(
            "ntw-tw-region",
            f"<span class='ntw-tw-idx'>[{html.escape(cid)}]</span>"
            f"<span class='ntw-tw-r'>{html.escape(lab)}</span>"
            f"<span class='ntw-tw-v'>{_kgec_marquee_pair(row_raw, seconds=mq_dur)}</span>",
        )
    return (
        "<div class='ntw-cyan-green-stream ntw-tw-rain national-tw-ignite kgec-forensic-rain'>"
        + "".join(lines)
        + "</div>"
    )


def build_ntw_resonance_chamber_figure(blob: dict[str, Any]) -> Any:
    """
    Horizontal Resonance Chamber — grouped horizontal bars (coverage vs SIM) × Big 4.
    Corridor rows are averaged into one meter per operator (below-map dashboard).
    """
    try:
        import plotly.graph_objects as go
    except ImportError:
        return None

    rows_data = blob.get("corridors") or []
    if not rows_data:
        return None

    ops_order = ["MTN", "Airtel", "Glo", "9mobile"]
    cov_mean: list[float] = []
    sim_mean: list[float] = []
    for op in ops_order:
        cvs: list[float] = []
        sms: list[float] = []
        for r in rows_data:
            od = (r.get("operators") or {}).get(op) or {}
            try:
                cvs.append(float(od.get("coverage_pct", 0)))
            except (TypeError, ValueError):
                pass
            try:
                sms.append(float(od.get("sim_verification_pct", 0)))
            except (TypeError, ValueError):
                pass
        cov_mean.append(sum(cvs) / len(cvs) if cvs else 0.0)
        sim_mean.append(sum(sms) / len(sms) if sms else 0.0)

    colors = [NTW_BRAND_HEX[o] for o in ops_order]
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            name="Coverage proxy %",
            x=cov_mean,
            y=ops_order,
            orientation="h",
            marker=dict(color=colors, line=dict(width=1, color="rgba(0,0,0,0.45)")),
        )
    )
    fig.add_trace(
        go.Bar(
            name="SIM verification %",
            x=sim_mean,
            y=ops_order,
            orientation="h",
            marker=dict(
                color=colors,
                opacity=0.78,
                line=dict(width=1, color="rgba(255,255,255,0.22)"),
            ),
        )
    )
    fig.update_layout(
        barmode="group",
        height=280,
        margin=dict(l=12, r=12, t=40, b=36),
        paper_bgcolor="rgba(0,0,0,0.92)",
        plot_bgcolor="rgba(0,0,40,0.55)",
        font=dict(color="rgba(240,244,255,0.94)", size=11),
        title=dict(
            text="K-GEC · corridor-mean resonance (Big 4)",
            font=dict(size=13, color="#D4AF37"),
            x=0.5,
            xanchor="center",
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(0,0,128,0.5)",
        ),
        xaxis=dict(range=[0, 105], gridcolor="rgba(212,175,55,0.15)", zeroline=False),
        yaxis=dict(gridcolor="rgba(212,175,55,0.08)"),
    )
    return fig


def build_ntw_single_operator_figure(blob: dict[str, Any], operator: str) -> Any:
    """One operator · two rows (coverage / SIM) × six corridors — horizontal strip column."""
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
    except ImportError:
        return None

    rows_data = blob.get("corridors") or []
    if not rows_data:
        return None

    labels = [str(r.get("id") or r.get("label") or "?")[:8] for r in rows_data]
    y_cov: list[float] = []
    y_sim: list[float] = []
    for r in rows_data:
        od = (r.get("operators") or {}).get(operator) or {}
        try:
            y_cov.append(float(od.get("coverage_pct", 0)))
        except (TypeError, ValueError):
            y_cov.append(0.0)
        try:
            y_sim.append(float(od.get("sim_verification_pct", 0)))
        except (TypeError, ValueError):
            y_sim.append(0.0)

    color = NTW_BRAND_HEX.get(operator, "#888888")

    fig = make_subplots(
        rows=2,
        cols=1,
        vertical_spacing=0.14,
        subplot_titles=("Coverage proxy %", "SIM verification proxy %"),
    )
    fig.add_trace(
        go.Bar(
            x=labels,
            y=y_cov,
            marker_color=color,
            marker_line=dict(width=0.5, color="rgba(0,0,0,0.3)"),
            showlegend=False,
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Bar(
            x=labels,
            y=y_sim,
            marker_color=color,
            marker_line=dict(width=0.5, color="rgba(0,0,0,0.3)"),
            opacity=0.88,
            showlegend=False,
        ),
        row=2,
        col=1,
    )
    fig.update_layout(
        height=260,
        margin=dict(l=36, r=8, t=28, b=28),
        paper_bgcolor="rgba(0,0,128,0.35)",
        plot_bgcolor="rgba(0,0,128,0.22)",
        font=dict(color="rgba(240,244,255,0.9)", size=9),
    )
    fig.update_yaxes(range=[0, 105], row=1, col=1, gridcolor="rgba(212,175,55,0.12)")
    fig.update_yaxes(range=[0, 105], row=2, col=1, gridcolor="rgba(212,175,55,0.12)")
    fig.update_xaxes(tickangle=-25, row=1, col=1)
    fig.update_xaxes(tickangle=-25, row=2, col=1)
    return fig


def ntw_brand_legend_html() -> str:
    """Lettermarks in brand colours — Deep Blue strip."""
    chips = []
    for op, hx in NTW_BRAND_HEX.items():
        tc = "#000000" if op == "MTN" else "#f8fafc"
        chips.append(
            f"<span style='display:inline-block;padding:3px 10px;border-radius:6px;"
            f"background:{hx};color:{tc};font-weight:800;font-size:0.72rem;"
            f"border:1px solid rgba(212,175,55,0.35);margin:2px 4px 2px 0;'>{op}</span>"
        )
    return (
        "<div style='display:flex;flex-wrap:wrap;align-items:center;gap:4px;margin-bottom:8px;'>"
        + "".join(chips)
        + "</div>"
    )
