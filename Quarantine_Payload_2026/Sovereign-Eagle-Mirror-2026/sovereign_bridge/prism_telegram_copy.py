"""Sam-Sam fidelity — Gold · Cyan · White · Red hierarchy in every Telegram HTML reply."""

from __future__ import annotations

import html
from typing import Any


def format_prism_telegram_html(
    *,
    title: str,
    gold_line: str,
    cyan_line: str,
    white_line: str,
    red_line: str,
    footer_lines: list[str] | None = None,
) -> str:
    """Telegram HTML parse_mode — tier lines are plain text (escaped here)."""
    ft = html.escape(title)
    g, cy, w, rd = map(html.escape, (gold_line, cyan_line, white_line, red_line))
    parts = [
        f"<b>🟡 GOLD</b><br/>{g}",
        f"<b>🔵 CYAN</b><br/>{cy}",
        f"<b>⚪ WHITE</b><br/>{w}",
        f"<b>🔴 RED</b><br/>{rd}",
    ]
    body = "<br/><br/>".join(parts)
    if footer_lines:
        body += "<br/><br/><code>" + html.escape("\n".join(footer_lines)[:3500]) + "</code>"
    return f"<b>{ft}</b><br/><br/>{body}"


def prism_lines_from_summary(summary: dict[str, Any], *, national_pu_total: int) -> tuple[str, str, str, str]:
    """Map Total Reality summary dict to four plain-text tier lines."""
    st = str(summary.get("state") or "?")
    lg = int(summary.get("lgas") or 0)
    wd = int(summary.get("wards_forensic") or summary.get("wards") or 0)
    n_wd = int(summary.get("national_ward_total") or 8806)
    pu = int(summary.get("pu_forensic") or 0)
    n_pu = int(summary.get("national_pu_total") or national_pu_total or 176_846)
    pct = (100.0 * float(pu) / float(max(n_pu, 1))) if n_pu else 0.0
    gold = f"{st} · {lg:,} LGAs · administrative shell"
    cyan = f"{wd:,} wards · national comparator {n_wd:,}"
    white = f"PU national share {pct:.2f}% · {pu:,} / {n_pu:,} polling units"
    red = "INEC atomic lattice · Chairman forensic heart"
    return gold, cyan, white, red
