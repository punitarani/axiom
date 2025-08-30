from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Set

from sqlalchemy.engine import Connection

_ensured_default: Set[str] = set()
_ensured_day: Set[str] = set()


def ensure_partition_for_timestamp(
    connection: Connection, base_table: str, ts: datetime
) -> None:
    """
    Ensure DEFAULT and daily partitions exist for the given UTC timestamp.
    Uses idempotent DDL and a small in-process cache to reduce redundant DDL.
    This runs in ORM events, so it must be synchronous and use the sync Connection.
    """
    # DEFAULT partition (once per process per table)
    default_key = f"{base_table}__default"
    if default_key not in _ensured_default:
        connection.exec_driver_sql(
            f'CREATE TABLE IF NOT EXISTS "{base_table}_default" PARTITION OF "{base_table}" DEFAULT'
        )
        _ensured_default.add(default_key)

    # Daily partition for the day of ts (UTC)
    ts_utc = ts.astimezone(timezone.utc)
    day_start = ts_utc.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = day_start + timedelta(days=1)
    part_name = (
        f"{base_table}_{day_start.year:04d}_{day_start.month:02d}_{day_start.day:02d}"
    )
    day_key = f"{base_table}__{day_start.date().isoformat()}"
    if day_key in _ensured_day:
        return

    ddl = (
        f'CREATE TABLE IF NOT EXISTS "{part_name}" PARTITION OF "{base_table}" '
        f"FOR VALUES FROM ('{day_start.isoformat()}') TO ('{day_end.isoformat()}')"
    )
    connection.exec_driver_sql(ddl)
    _ensured_day.add(day_key)


__all__ = ["ensure_partition_for_timestamp"]
