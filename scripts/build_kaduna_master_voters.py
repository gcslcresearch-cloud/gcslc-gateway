#!/usr/bin/env python3
"""
Merge Kaduna LGA Excel harvests into hidden `.kaduna_master_voters.csv`.
Duplicate filenames (e.g. KADUNA SOUTH vs KADUNA SOUTH (1)) → keep file with higher row count.
Also writes `.kaduna_harvest_meta.json` and `.kaduna_audit_feed.csv` (stratified sample for UI marquee).
"""
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


def _normalize_stem(stem: str) -> str:
    s = stem.upper().strip()
    if s.endswith(" (1)"):
        s = s[:-4].strip()
    return s


def _xlsx_body_row_count(path: Path) -> int:
    cmd = f'unzip -p "{path}" xl/worksheets/sheet1.xml 2>/dev/null | grep -o "<row " | wc -l'
    out = subprocess.check_output(cmd, shell=True).decode().strip()
    try:
        n = int(out)
    except ValueError:
        n = 0
    return max(0, n - 1)


def _norm_phone(v) -> str:
    if pd.isna(v):
        return ""
    s = str(v).strip()
    if s.endswith(".0") and s.replace(".", "").replace("-", "").isdigit():
        s = s[:-2]
    if s.endswith(".0"):
        try:
            s = str(int(float(s)))
        except ValueError:
            pass
    return s


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--source",
        type=Path,
        default=Path("/Users/user/Desktop/Kaduna_LGA_Data"),
        help="Folder containing Kaduna LGA .xlsx files",
    )
    ap.add_argument(
        "--dest",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repo root (writes dotfiles here)",
    )
    args = ap.parse_args()
    src: Path = args.source
    dest: Path = args.dest
    if not src.is_dir():
        raise SystemExit(f"Source not found: {src}")

    by_lga: dict[str, tuple[Path, int]] = {}
    for p in sorted(src.glob("*.xlsx")):
        key = _normalize_stem(p.stem)
        n = _xlsx_body_row_count(p)
        cur = by_lga.get(key)
        if cur is None or n > cur[1]:
            by_lga[key] = (p, n)

    if len(by_lga) != 23:
        raise SystemExit(f"Expected 23 unique LGAs, got {len(by_lga)}: {sorted(by_lga.keys())}")

    frames: list[pd.DataFrame] = []
    per_lga_rows: dict[str, int] = {}
    for lga_key in sorted(by_lga.keys()):
        path, _n = by_lga[lga_key]
        raw = pd.read_excel(path, header=1, engine="openpyxl")
        raw.columns = [str(c).strip() for c in raw.columns]
        need = {"Number", "First Name", "Last Name", "State", "LGA", "Gender"}
        if not need.issubset(set(raw.columns)):
            raise SystemExit(f"{path.name}: missing columns {need - set(raw.columns)}")
        d = raw[list(need)].copy()
        d["source_lga_file"] = lga_key
        d["pu_id"] = d["Number"].map(_norm_phone)
        d["voter_name"] = (
            d["First Name"].fillna("").astype(str).str.strip()
            + " "
            + d["Last Name"].fillna("").astype(str).str.strip()
        ).str.strip()
        d["verification_status"] = d["pu_id"].map(
            lambda x: "VERIFIED" if str(x).strip() else "PENDING"
        )
        d["verified"] = d["verification_status"] == "VERIFIED"
        frames.append(d)
        per_lga_rows[lga_key] = len(d)

    all_df = pd.concat(frames, ignore_index=True)
    before = len(all_df)
    deduped = all_df.drop_duplicates(subset=["pu_id", "LGA"], keep="first")
    after = len(deduped)

    out_csv = dest / ".kaduna_master_voters.csv"
    export = pd.DataFrame(
        {
            "voter_name": deduped["voter_name"],
            "first_name": deduped["First Name"],
            "last_name": deduped["Last Name"],
            "state": deduped["State"],
            "lga": deduped["LGA"],
            "gender": deduped["Gender"],
            "pu_id": deduped["pu_id"],
            "verification_status": deduped["verification_status"],
            "verified": deduped["verified"],
            "source_lga_file": deduped["source_lga_file"],
        }
    )
    export.to_csv(out_csv, index=False)

    # Stratified sample for sidebar marquee / pulse (max 36 rows per LGA)
    feed_parts: list[pd.DataFrame] = []
    for lk, g in export.groupby("lga", sort=True):
        feed_parts.append(g.head(36))
    feed_df = pd.concat(feed_parts, ignore_index=True)
    feed_path = dest / ".kaduna_audit_feed.csv"
    feed_df.to_csv(feed_path, index=False)

    meta = {
        "built_at": datetime.now(timezone.utc).isoformat(),
        "source_dir": str(src.resolve()),
        "lga_count": len(by_lga),
        "lgas": sorted(by_lga.keys()),
        "row_count_raw": int(before),
        "canvassed_rows": int(after),
        "per_lga_raw_rows": per_lga_rows,
        "south_pick": str(by_lga["KADUNA SOUTH"][0]) if "KADUNA SOUTH" in by_lga else "",
    }
    meta_path = dest / ".kaduna_harvest_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"Wrote {out_csv} ({after:,} deduped rows from {before:,} raw)")
    print(f"Wrote {feed_path} ({len(feed_df):,} feed rows)")
    print(f"Wrote {meta_path}")


if __name__ == "__main__":
    main()
