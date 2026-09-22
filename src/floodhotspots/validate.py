"""Admissibility checks for the site and event tables.

Written before the dataset it validates. The rule it exists to enforce is that
a number without a resolvable source is not data, and a table that mixes
inundated extent with administrative area is not a regression target.

Every check returns a list of Problem records rather than raising, so one run
reports every defect instead of stopping at the first.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date

import pandas as pd

from .schema import (
    BOUNDS,
    DRIVERS,
    EVENT_COLUMNS,
    EVENT_FIGURES,
    EXPECTED_SITE_COUNT,
    EXPECTED_UAE_SITES,
    SITE_COLUMNS,
    SITE_FIGURES,
    TIERS,
)

URL_RE = re.compile(r"^https?://[^\s]+\.[^\s]+$")


@dataclass(frozen=True)
class Problem:
    table: str
    row: str
    column: str
    rule: str
    detail: str

    def __str__(self) -> str:
        return f"[{self.table}:{self.row}] {self.column}: {self.rule} — {self.detail}"


def _present(value) -> bool:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return False
    return str(value).strip() != ""


def _check_columns(df: pd.DataFrame, expected: tuple[str, ...], table: str) -> list[Problem]:
    missing = [c for c in expected if c not in df.columns]
    extra = [c for c in df.columns if c not in expected]
    problems = [
        Problem(table, "-", c, "missing_column", "declared in schema, absent from file")
        for c in missing
    ]
    problems += [
        Problem(table, "-", c, "unknown_column", "present in file, absent from schema")
        for c in extra
    ]
    return problems


def _check_provenance(df: pd.DataFrame, figures, key: str, table: str) -> list[Problem]:
    """A figure is admissible only with a resolvable URL, a tier, and a method
    where the schema demands one. This is the rule the whole project rests on."""
    problems: list[Problem] = []
    for _, row in df.iterrows():
        rid = str(row.get(key, "?"))
        for fig in figures:
            if fig.value not in df.columns or not _present(row.get(fig.value)):
                continue
            url = row.get(fig.source_url)
            if not _present(url):
                problems.append(
                    Problem(table, rid, fig.value, "no_source", "figure present, source URL empty")
                )
            elif not URL_RE.match(str(url).strip()):
                problems.append(
                    Problem(table, rid, fig.source_url, "bad_source", f"not a URL: {url!r}")
                )
            if fig.tier:
                tier = row.get(fig.tier)
                if not _present(tier):
                    problems.append(
                        Problem(table, rid, fig.tier, "no_tier", "figure present, tier empty")
                    )
                elif str(tier).strip() not in TIERS:
                    problems.append(
                        Problem(table, rid, fig.tier, "bad_tier", f"{tier!r} not in {TIERS}")
                    )
                elif str(tier).strip() == "I" and not _present(row.get("notes")):
                    problems.append(
                        Problem(table, rid, fig.tier, "unexplained_inference",
                                "tier I requires a note explaining the inference")
                    )
            if fig.method and not _present(row.get(fig.method)):
                problems.append(
                    Problem(table, rid, fig.method, "no_method",
                            "figure present, measurement method empty")
                )
    return problems


def _check_bounds(df: pd.DataFrame, key: str, table: str) -> list[Problem]:
    problems: list[Problem] = []
    for column, (low, high) in BOUNDS.items():
        if column not in df.columns:
            continue
        values = pd.to_numeric(df[column], errors="coerce")
        for idx, value in values.items():
            raw = df.at[idx, column]
            if _present(raw) and pd.isna(value):
                problems.append(
                    Problem(table, str(df.at[idx, key]), column, "not_numeric", repr(raw))
                )
            elif not pd.isna(value) and not (low <= value <= high):
                problems.append(
                    Problem(table, str(df.at[idx, key]), column, "out_of_bounds",
                            f"{value} outside [{low}, {high}] — check units")
                )
    return problems


def validate_sites(sites: pd.DataFrame) -> list[Problem]:
    problems = _check_columns(sites, SITE_COLUMNS, "sites")
    if any(p.rule == "missing_column" for p in problems):
        return problems

    problems += _check_provenance(sites, SITE_FIGURES, "site_id", "sites")
    problems += _check_bounds(sites, "site_id", "sites")

    duplicated = sites["site_id"][sites["site_id"].duplicated()].tolist()
    problems += [
        Problem("sites", sid, "site_id", "duplicate_id", "site_id appears more than once")
        for sid in duplicated
    ]

    if len(sites) != EXPECTED_SITE_COUNT:
        problems.append(
            Problem("sites", "-", "site_id", "wrong_site_count",
                    f"{len(sites)} sites, brief specifies {EXPECTED_SITE_COUNT}")
        )
    uae = int((sites["iso3"].astype(str).str.upper() == "ARE").sum())
    if uae != EXPECTED_UAE_SITES:
        problems.append(
            Problem("sites", "-", "iso3", "wrong_uae_count",
                    f"{uae} UAE sites, brief specifies {EXPECTED_UAE_SITES}")
        )

    for _, row in sites.iterrows():
        rid = str(row["site_id"])
        try:
            west, south, east, north = (
                float(row["bbox_w"]), float(row["bbox_s"]),
                float(row["bbox_e"]), float(row["bbox_n"]),
            )
        except (TypeError, ValueError):
            problems.append(Problem("sites", rid, "bbox", "not_numeric", "bbox is not four floats"))
            continue
        if not (-180 <= west < east <= 180):
            problems.append(
                Problem("sites", rid, "bbox", "bad_bbox", f"longitudes {west}, {east}")
            )
        if not (-90 <= south < north <= 90):
            problems.append(
                Problem("sites", rid, "bbox", "bad_bbox", f"latitudes {south}, {north}")
            )
    return problems


def validate_events(events: pd.DataFrame, sites: pd.DataFrame | None = None) -> list[Problem]:
    problems = _check_columns(events, EVENT_COLUMNS, "events")
    if any(p.rule == "missing_column" for p in problems):
        return problems

    problems += _check_provenance(events, EVENT_FIGURES, "event_id", "events")
    problems += _check_bounds(events, "event_id", "events")

    duplicated = events["event_id"][events["event_id"].duplicated()].tolist()
    problems += [
        Problem("events", eid, "event_id", "duplicate_id", "event_id appears more than once")
        for eid in duplicated
    ]

    if sites is not None:
        known = set(sites["site_id"].astype(str))
        for _, row in events.iterrows():
            if str(row["site_id"]) not in known:
                problems.append(
                    Problem("events", str(row["event_id"]), "site_id", "orphan_event",
                            f"{row['site_id']!r} is not in the sites table")
                )

    for _, row in events.iterrows():
        rid = str(row["event_id"])
        start = pd.to_datetime(row["start_date"], errors="coerce")
        end = pd.to_datetime(row["end_date"], errors="coerce")
        if pd.isna(start):
            problems.append(Problem("events", rid, "start_date", "bad_date", repr(row["start_date"])))
        if _present(row["end_date"]) and pd.isna(end):
            problems.append(Problem("events", rid, "end_date", "bad_date", repr(row["end_date"])))
        if not pd.isna(start) and not pd.isna(end) and end < start:
            problems.append(
                Problem("events", rid, "end_date", "reversed_dates", f"{end.date()} before {start.date()}")
            )
        if not pd.isna(start) and start.date() > date.today():
            problems.append(Problem("events", rid, "start_date", "future_date", str(start.date())))

        day = pd.to_numeric(row["rain_24h_mm"], errors="coerce")
        total = pd.to_numeric(row["rain_event_total_mm"], errors="coerce")
        if not pd.isna(day) and not pd.isna(total) and total < day:
            problems.append(
                Problem("events", rid, "rain_event_total_mm", "total_below_daily",
                        f"event total {total} mm is less than its own 24h peak {day} mm")
            )

        driver = row.get("driver")
        if not _present(driver):
            problems.append(Problem("events", rid, "driver", "no_driver", "driver must be declared"))
        elif str(driver).strip() not in DRIVERS:
            problems.append(
                Problem("events", rid, "driver", "bad_driver", f"{driver!r} not in {DRIVERS}")
            )
    return problems


def validate(sites: pd.DataFrame, events: pd.DataFrame) -> list[Problem]:
    return validate_sites(sites) + validate_events(events, sites)
