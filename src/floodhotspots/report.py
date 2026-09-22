"""Generating the two written outputs: per-site profiles and the results table.

Rainfall is stored in millimetres everywhere upstream and converted to
centimetres exactly once, here, because that is the unit the brief asked for
and a second conversion site is how mm/cm errors get in.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .features import TARGET
from .schema import TIER_MEANING


def markdown_table(frame: pd.DataFrame) -> str:
    """A GitHub-flavoured table, so the repo does not carry a formatting
    dependency for the sake of six tables."""
    if frame.empty:
        return "_no rows_"

    def cell(value) -> str:
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return ""
        if isinstance(value, float):
            return f"{value:.3f}".rstrip("0").rstrip(".")
        return str(value).replace("|", "\\|")

    header = [str(c) for c in frame.columns]
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join(["---"] * len(header)) + "|"]
    for _, row in frame.iterrows():
        lines.append("| " + " | ".join(cell(row[c]) for c in frame.columns) + " |")
    return "\n".join(lines)


def mm_to_cm(value) -> str:
    number = pd.to_numeric(value, errors="coerce")
    return "" if pd.isna(number) else f"{number / 10:.1f}"


def _link(text: str, url) -> str:
    if not isinstance(url, str) or not url.strip():
        return text
    return f"[{text}]({url.strip()})"


def site_profiles(sites: pd.DataFrame, frame: pd.DataFrame) -> str:
    lines = [
        "# Site profiles",
        "",
        "Twelve regions, ten selected on recurring global flood impact and two in the UAE.",
        "Rainfall is the peak 24-hour depth at the named station, converted from the stored",
        "millimetre value. Affected area is inundated extent, not the administrative area of",
        "the affected districts, except where the method column says otherwise.",
        "",
        "Evidence tiers: " + "; ".join(f"**{k}** {v}" for k, v in TIER_MEANING.items()) + ".",
        "",
    ]
    for _, site in sites.iterrows():
        events = frame.loc[frame["site_id"] == site["site_id"]].sort_values("start_date")
        lines += [
            f"## {site['site_name']}, {site['country']}",
            "",
            f"`{site['site_id']}` · bbox {site['bbox_w']}, {site['bbox_s']}, "
            f"{site['bbox_e']}, {site['bbox_n']} (EPSG:4326)",
            "",
            f"**Mechanism.** {site['mechanism']}",
            "",
            f"**Why it is here.** {site['selection_reason']} "
            f"({_link('source', site.get('selection_source_url'))})",
            "",
            f"**Where it floods first.** {site['hotspot_subareas']}",
            "",
            f"**Exposure.** {_link(f'{int(pd.to_numeric(site['population'], errors='coerce')):,} people', site.get('population_source_url'))} "
            f"over a {pd.to_numeric(site['catchment_area_km2'], errors='coerce'):,.0f} km² catchment.",
            "",
            "| Event | Dates | Peak 24h rain (cm) | Station | Inundated area (km²) | Area method | Driver | Deaths |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for _, event in events.iterrows():
            area = pd.to_numeric(event["affected_area_km2"], errors="coerce")
            deaths = pd.to_numeric(event["deaths"], errors="coerce")
            lines.append(
                "| {id} | {start} to {end} | {rain} | {station} | {area} | {method} | {driver} | {deaths} |".format(
                    id=event["event_id"],
                    start=event["start_date"],
                    end=event["end_date"] if isinstance(event["end_date"], str) else "",
                    rain=_link(mm_to_cm(event["rain_24h_mm"]), event.get("rain_source_url"))
                    + (f" `{event['rain_tier']}`" if isinstance(event.get("rain_tier"), str) else ""),
                    station=event["rain_station"] if isinstance(event["rain_station"], str) else "",
                    area=_link(f"{area:,.0f}", event.get("area_source_url")) if not pd.isna(area) else "not published",
                    method=event["area_method"] if isinstance(event["area_method"], str) else "",
                    driver=event["driver"],
                    deaths="" if pd.isna(deaths) else f"{int(deaths):,}",
                )
            )
        lines.append("")
    return "\n".join(lines)


def results_table(scores) -> str:
    return markdown_table(pd.DataFrame([s.as_row() for s in scores]))


def exclusions_table(excluded: pd.DataFrame) -> str:
    if excluded.empty:
        return "No events were excluded."
    return markdown_table(excluded)


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    return path
