"""format_schema_date — ISO 8601 with America/Santiago offset for JSON-LD."""
from __future__ import annotations

from datetime import date, datetime
from zoneinfo import ZoneInfo

_CL = ZoneInfo("America/Santiago")


def format_schema_date(value: str | date | datetime, wall_time: str = "12:00:00") -> str:
    """Return e.g. '2026-09-04T12:00:00-04:00'. Never invent calendar days."""
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=_CL)
        return value.astimezone(_CL).isoformat(timespec="seconds")

    if isinstance(value, date) and not isinstance(value, datetime):
        hh, mm, ss = (int(x) for x in wall_time.split(":"))
        return datetime(value.year, value.month, value.day, hh, mm, ss, tzinfo=_CL).isoformat(
            timespec="seconds"
        )

    s = str(value).strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"

    # Date-only YYYY-MM-DD → noon Chile by default (Google-friendly, avoids "missing timezone")
    if len(s) == 10 and s[4] == "-" and s[7] == "-":
        d = date.fromisoformat(s)
        hh, mm, ss = (int(x) for x in wall_time.split(":"))
        return datetime(d.year, d.month, d.day, hh, mm, ss, tzinfo=_CL).isoformat(timespec="seconds")

    # Datetime with or without offset
    try:
        dt = datetime.fromisoformat(s)
    except ValueError as e:
        raise ValueError(f"format_schema_date: invalid date {value!r}") from e

    if dt.tzinfo is not None:
        return dt.isoformat(timespec="seconds")
    return dt.replace(tzinfo=_CL).isoformat(timespec="seconds")


formatSchemaDate = format_schema_date
