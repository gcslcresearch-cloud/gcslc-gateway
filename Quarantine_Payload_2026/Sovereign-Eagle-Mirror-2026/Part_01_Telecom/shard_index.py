"""
Part_01 Telecom shard/index skeleton for high-volume Kaduna contact payloads.
This module is intentionally lightweight and browser-safe: it exposes aggregate
index stats and bounded previews, not full-record rendering.
"""

from __future__ import annotations

import hashlib
from collections import defaultdict
from dataclasses import dataclass
from typing import Any


def _stable_hash(value: str) -> int:
    return int(hashlib.sha256(value.encode("utf-8")).hexdigest()[:8], 16)


@dataclass(frozen=True)
class TelecomIndexConfig:
    shard_count: int = 256
    target_capacity: int = 2_000_000
    max_preview_rows: int = 150


class KadunaContactShardIndex:
    """
    In-memory skeleton index.
    Records can be streamed in batches; the UI consumes only shard aggregates.
    """

    def __init__(self, config: TelecomIndexConfig | None = None) -> None:
        self.config = config or TelecomIndexConfig()
        self._shard_sizes: dict[int, int] = defaultdict(int)
        self._ward_index: dict[str, int] = defaultdict(int)
        self._lga_index: dict[str, int] = defaultdict(int)
        self._sample_rows: list[dict[str, Any]] = []
        self._ingested_rows = 0

    def shard_for(self, phone_e164: str) -> int:
        return _stable_hash(phone_e164) % self.config.shard_count

    def ingest_batch(self, rows: list[dict[str, Any]]) -> None:
        for row in rows:
            phone = str(row.get("phone_e164", ""))
            if not phone:
                continue
            shard = self.shard_for(phone)
            self._shard_sizes[shard] += 1
            self._ward_index[str(row.get("ward_code", "unknown"))] += 1
            self._lga_index[str(row.get("lga_code", "unknown"))] += 1
            self._ingested_rows += 1
            if len(self._sample_rows) < self.config.max_preview_rows:
                self._sample_rows.append(row)

    def summary(self) -> dict[str, Any]:
        used_shards = sum(1 for size in self._shard_sizes.values() if size > 0)
        peak_shard = max(self._shard_sizes.values(), default=0)
        avg_active = (self._ingested_rows / used_shards) if used_shards else 0.0
        return {
            "target_capacity": self.config.target_capacity,
            "ingested_rows": self._ingested_rows,
            "shard_count": self.config.shard_count,
            "used_shards": used_shards,
            "peak_shard_load": peak_shard,
            "avg_active_shard_load": round(avg_active, 2),
            "indexed_wards": len(self._ward_index),
            "indexed_lgas": len(self._lga_index),
            "browser_safe_preview_rows": len(self._sample_rows),
        }

    def top_wards(self, limit: int = 10) -> list[dict[str, Any]]:
        top = sorted(self._ward_index.items(), key=lambda kv: kv[1], reverse=True)[:limit]
        return [{"ward_code": ward, "count": count} for ward, count in top]
