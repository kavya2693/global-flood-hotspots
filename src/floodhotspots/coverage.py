"""What the public record actually contains, per site and per figure.

This started as a diagnostic and became the main result. The question the
project set out to answer — does rainfall depth predict how much area floods —
turns out to be unanswerable from published sources for most events, because
the two numbers are almost never published for the same flood. Rainfall is a
meteorological measurement that a met agency records as a matter of routine;
inundated extent is a remote-sensing product that somebody has to decide to
make, and for most floods nobody does.

Counting that is more useful than pretending otherwise, so it is counted here
and reported with the same rigour as any model score.
"""

from __future__ import annotations

import pandas as pd

FIGURES = {
    "rain_24h_mm": "peak 24h rainfall",
    "rain_event_total_mm": "event total rainfall",
    "affected_area_km2": "inundated area",
    "people_affected": "people affected",
    "deaths": "deaths",
}


def _has(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").notna()


def per_figure(events: pd.DataFrame) -> pd.DataFrame:
    """How often each figure is published at all, and how often at a tier you
    would defend in front of a hydrologist."""
    total = len(events)
    rows = []
    for column, label in FIGURES.items():
        present = _has(events[column])
        tier_column = {
            "rain_24h_mm": "rain_tier",
            "rain_event_total_mm": "rain_tier",
            "affected_area_km2": "area_tier",
        }.get(column)
        if tier_column:
            strong = int((present & events[tier_column].astype(str).str.strip().isin(["V1", "V2"])).sum())
        else:
            strong = None
        rows.append(
            {
                "figure": label,
                "events with a sourced value": int(present.sum()),
                "share of events": f"{present.sum() / total:.0%}",
                "of those, tier V1 or V2": strong if strong is not None else "n/a",
            }
        )
    return pd.DataFrame(rows)


def per_site(events: pd.DataFrame, sites: pd.DataFrame) -> pd.DataFrame:
    """The same count broken out by site, because the gap is not evenly spread.
    A site with a Copernicus EMS activation has extents; a site without one does
    not, regardless of how badly it flooded."""
    rows = []
    for _, site in sites.iterrows():
        subset = events.loc[events["site_id"] == site["site_id"]]
        if subset.empty:
            continue
        rain = _has(subset["rain_24h_mm"])
        area = _has(subset["affected_area_km2"])
        rows.append(
            {
                "site": site["site_name"],
                "country": site["country"],
                "events": len(subset),
                "with 24h rainfall": int(rain.sum()),
                "with inundated area": int(area.sum()),
                "with both": int((rain & area).sum()),
            }
        )
    frame = pd.DataFrame(rows)
    return frame.sort_values("with both", ascending=False, ignore_index=True)


def pairing_rate(events: pd.DataFrame) -> dict:
    """The single number this project exists to report."""
    rain = _has(events["rain_24h_mm"])
    area = _has(events["affected_area_km2"])
    paired = int((rain & area).sum())
    return {
        "events": len(events),
        "with rainfall": int(rain.sum()),
        "with area": int(area.sum()),
        "paired": paired,
        "pairing_rate": paired / len(events) if len(events) else 0.0,
    }


def area_method_mix(events: pd.DataFrame) -> pd.DataFrame:
    """Of the extents that do exist, how they were measured. Mixing these is
    what makes a pooled regression target incoherent."""
    present = events.loc[_has(events["affected_area_km2"])].copy()
    if present.empty:
        return pd.DataFrame(columns=["measurement method", "events"])
    method = present["area_method"].astype(str).str.lower()
    bucket = pd.Series("other", index=present.index)
    for marker, name in (
        ("administrative", "administrative district area, not an extent"),
        ("sentinel", "satellite SAR"),
        ("sar", "satellite SAR"),
        ("planetscope", "satellite optical"),
        ("satellite", "satellite, unspecified sensor"),
        ("model", "hydraulic model output"),
        ("simulated", "hydraulic model output"),
        ("aerial", "aerial or drone imagery"),
        ("government", "government estimate"),
    ):
        bucket = bucket.mask(method.str.contains(marker, na=False), name)
    counts = bucket.value_counts().rename_axis("measurement method").reset_index(name="events")
    return counts


def measurement_split(events: pd.DataFrame, sites: pd.DataFrame) -> pd.DataFrame:
    """Rainfall coverage against extent coverage, per site.

    The two are not independent and they are not positively related. Rainfall
    comes from a national gauge network; extent comes from somebody deciding to
    run a satellite mapping activation. Those decisions are made by different
    institutions responding to different kinds of flood, and the result is that
    a site tends to have one or the other."""
    frame = per_site(events, sites).copy()
    frame["rainfall coverage"] = frame["with 24h rainfall"] / frame["events"]
    frame["extent coverage"] = frame["with inundated area"] / frame["events"]
    frame["flood type"] = [
        "urban pluvial" if sid in URBAN_PLUVIAL else "riverine or deltaic"
        for sid in _site_ids_in_order(frame, sites)
    ]
    return frame[["site", "flood type", "events", "rainfall coverage", "extent coverage"]]


# Sites where the flooding is shallow, fast and inside a built-up area, which is
# both the easiest case to gauge and the hardest case to see from orbit.
URBAN_PLUVIAL = {"ind_mumbai", "idn_jakarta", "are_dubai", "are_fujairah", "deu_ahr", "usa_houston"}


def _site_ids_in_order(frame: pd.DataFrame, sites: pd.DataFrame) -> list[str]:
    lookup = dict(zip(sites["site_name"], sites["site_id"], strict=True))
    return [lookup[name] for name in frame["site"]]


def coverage_correlation(events: pd.DataFrame, sites: pd.DataFrame) -> dict:
    """One number for the claim above: the rank correlation between a site's
    rainfall coverage and its extent coverage. A positive value would mean
    well-documented floods are well documented in both respects. It is not."""
    from scipy.stats import spearmanr

    frame = measurement_split(events, sites)
    rho, p_value = spearmanr(frame["rainfall coverage"], frame["extent coverage"])
    return {"sites": len(frame), "spearman": float(rho), "p": float(p_value)}
