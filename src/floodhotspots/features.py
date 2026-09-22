"""Turning sourced event records into a modelling table.

Two decisions here carry most of the weight. The first is which rows are
admissible as a regression target at all: an extent produced by a dam or levee
failure is not a function of the rainfall that preceded it, and an
administrative district area is not an extent. Both are kept in the dataset and
dropped from the fit, because dropping them silently is how a flattering result
gets manufactured.

The second is that area and catchment are logged. Inundated extent spans four
orders of magnitude across these sites, and an unlogged target would make the
Indus basin the only observation the model cares about.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .schema import PROXY_AREA_METHOD_MARKER, RAINFALL_DRIVEN

TARGET = "log10_affected_area_km2"

NUMERIC_FEATURES = [
    "log10_rain_24h_mm",
    "log10_rain_event_total_mm",
    "rain_burst_ratio",
    "log10_catchment_area_km2",
    "log10_population",
    "log10_population_density",
    "mean_elevation_m",
    "coastal",
    "event_year",
]

# Rainfall columns, named so the ablation can remove exactly these and nothing else.
RAINFALL_FEATURES = ["log10_rain_24h_mm", "log10_rain_event_total_mm", "rain_burst_ratio"]
EXPOSURE_FEATURES = [f for f in NUMERIC_FEATURES if f not in RAINFALL_FEATURES]


def _log10(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce")
    return np.log10(values.where(values > 0))


def build(sites: pd.DataFrame, events: pd.DataFrame) -> pd.DataFrame:
    """Join, derive and label. Returns every event, with an `admissible` flag,
    so the caller can report on what was excluded instead of never seeing it."""
    frame = events.merge(sites, on="site_id", how="left", validate="many_to_one")

    frame["event_year"] = pd.to_datetime(frame["start_date"], errors="coerce").dt.year
    frame["log10_rain_24h_mm"] = _log10(frame["rain_24h_mm"])
    frame["log10_rain_event_total_mm"] = _log10(frame["rain_event_total_mm"])

    # How much of the event's rain fell in its worst day. A ratio near 1 is a
    # cloudburst; near 0.2 is a long monsoon soak. These flood very differently.
    total = pd.to_numeric(frame["rain_event_total_mm"], errors="coerce")
    daily = pd.to_numeric(frame["rain_24h_mm"], errors="coerce")
    frame["rain_burst_ratio"] = (daily / total).where(total > 0)

    frame["log10_catchment_area_km2"] = _log10(frame["catchment_area_km2"])
    frame["log10_population"] = _log10(frame["population"])
    density = pd.to_numeric(frame["population"], errors="coerce") / pd.to_numeric(
        frame["catchment_area_km2"], errors="coerce"
    )
    frame["log10_population_density"] = _log10(density)
    frame["coastal"] = pd.to_numeric(frame["coastal"], errors="coerce").fillna(0)

    frame[TARGET] = _log10(frame["affected_area_km2"])

    frame["area_is_measured"] = ~frame["area_method"].astype(str).str.lower().str.contains(
        PROXY_AREA_METHOD_MARKER, na=False
    )
    frame["driver_is_rainfall"] = frame["driver"].astype(str).str.strip().isin(RAINFALL_DRIVEN)
    frame["has_target"] = frame[TARGET].notna()
    frame["has_rainfall"] = frame["log10_rain_24h_mm"].notna()

    frame["admissible"] = (
        frame["has_target"] & frame["has_rainfall"]
        & frame["area_is_measured"] & frame["driver_is_rainfall"]
    )
    return frame


def exclusion_report(frame: pd.DataFrame) -> pd.DataFrame:
    """Why each excluded row was excluded. Goes in the README verbatim."""
    excluded = frame.loc[~frame["admissible"]].copy()
    reasons = []
    for _, row in excluded.iterrows():
        why = []
        if not row["has_target"]:
            why.append("no sourced inundated area")
        if not row["has_rainfall"]:
            why.append("no sourced 24h rainfall")
        if not row["area_is_measured"]:
            why.append("area is administrative, not inundated")
        if not row["driver_is_rainfall"]:
            why.append(f"extent driven by {row['driver']}")
        reasons.append("; ".join(why))
    excluded["exclusion_reason"] = reasons
    return excluded[["event_id", "site_id", "start_date", "exclusion_reason"]]


def modelling_table(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.loc[frame["admissible"]].reset_index(drop=True)
