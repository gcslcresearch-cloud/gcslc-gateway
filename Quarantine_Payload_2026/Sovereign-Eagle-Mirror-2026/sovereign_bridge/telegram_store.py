"""SQLite queue — Telegram webhook / long-poll enqueues; Streamlit claims and applies."""

from __future__ import annotations

import os
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_lock = threading.Lock()


def default_sqlite_path() -> Path:
    raw = (os.environ.get("GCSLC_BRIDGE_SQLITE") or "").strip()
    if raw:
        return Path(raw).expanduser()
    base = Path(__file__).resolve().parent.parent
    p = base / ".sovereign_bridge"
    p.mkdir(parents=True, exist_ok=True)
    return p / "ingress.sqlite"


def _conn(path: Path) -> sqlite3.Connection:
    c = sqlite3.connect(str(path), check_same_thread=False, timeout=30)
    c.row_factory = sqlite3.Row
    return c


def init_store(path: Path | None = None) -> Path:
    p = path or default_sqlite_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    with _lock:
        c = _conn(p)
        try:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS tg_updates (
                  update_id INTEGER PRIMARY KEY,
                  chat_id INTEGER NOT NULL,
                  text TEXT NOT NULL,
                  created_iso TEXT NOT NULL,
                  applied_iso TEXT
                )
                """
            )
            c.commit()
        finally:
            c.close()
    return p


def enqueue_update(
    *,
    update_id: int,
    chat_id: int,
    text: str,
    path: Path | None = None,
) -> bool:
    p = init_store(path)
    created = datetime.now(timezone.utc).isoformat()
    with _lock:
        c = _conn(p)
        try:
            c.execute(
                "INSERT OR IGNORE INTO tg_updates (update_id, chat_id, text, created_iso) VALUES (?,?,?,?)",
                (int(update_id), int(chat_id), str(text)[:8000], created),
            )
            c.commit()
            return c.total_changes > 0
        finally:
            c.close()


def peek_next_pending(path: Path | None = None) -> dict[str, Any] | None:
    p = init_store(path)
    with _lock:
        c = _conn(p)
        try:
            row = c.execute(
                "SELECT update_id, chat_id, text FROM tg_updates WHERE applied_iso IS NULL "
                "ORDER BY update_id ASC LIMIT 1"
            ).fetchone()
            return dict(row) if row else None
        finally:
            c.close()


def mark_applied(update_id: int, path: Path | None = None) -> None:
    p = init_store(path)
    now = datetime.now(timezone.utc).isoformat()
    with _lock:
        c = _conn(p)
        try:
            c.execute(
                "UPDATE tg_updates SET applied_iso = ? WHERE update_id = ?",
                (now, int(update_id)),
            )
            c.commit()
        finally:
            c.close()
