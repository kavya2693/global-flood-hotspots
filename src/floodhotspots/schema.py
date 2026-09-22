"""Column contract for the site and event tables.

Everything downstream reads these definitions rather than hard-coding column
names, so a rename is a one-line change and the validator cannot drift away
from what the loaders expect.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Evidence tiers, strongest first. A figure carrying no tier is not a figure.
TIERS = ("V1", "V2", "V3", "I")
TIER_MEANING = {
    "V1": "satellite-derived extent or official gauge record",
    "V2": "government or UN agency report",
    "V3": "reputable secondary reporting",
    "I": "inferred, requires an explanatory note",
}

# Plausibility bounds. These are deliberately generous: the job of a bound is to
# catch a decimal-point or unit error, not to second-guess a sourced measurement.
# The upper rainfall bound sits above the world 24h record (1825 mm, Foc-Foc,
# Reunion, 1966) so a real extreme passes and a mm/cm mixup does not.
BOUNDS = {
    "rain_24h_mm": (1.0, 2000.0),
    "rain_event_total_mm": (1.0, 6000.0),
    "affected_area_km2": (0.1, 500_000.0),
    "catchment_area_km2": (1.0, 4_000_000.0),
    "people_affected": (1, 200_000_000),
    "deaths": (0, 500_000),
}


@dataclass(frozen=True)
class Figure:
    """A numeric column that must carry provenance to be admissible."""

    value: str
    source_url: str
    tier: str | None = None
    method: str | None = None


SITE_COLUMNS = (
    "site_id",
    "site_name",
    "country",
    "iso3",
    "bbox_w",
    "bbox_s",
    "bbox_e",
    "bbox_n",
    "mechanism",
    "coastal",
    "catchment_area_km2",
    "catchment_area_source_url",
    "population",
    "population_source_url",
    "mean_elevation_m",
    "elevation_source_url",
    "selection_reason",
    "selection_source_url",
    "hotspot_subareas",
)

EVENT_COLUMNS = (
    "event_id",
    "site_id",
    "start_date",
    "end_date",
    "rain_24h_mm",
    "rain_station",
    "rain_event_total_mm",
    "rain_source_url",
    "rain_tier",
    "affected_area_km2",
    "area_method",
    "area_source_url",
    "area_tier",
    "people_affected",
    "people_source_url",
    "deaths",
    "deaths_source_url",
    "driver",
    "notes",
)

# Figures and the provenance columns that must accompany them.
EVENT_FIGURES = (
    Figure("rain_24h_mm", "rain_source_url", "rain_tier"),
    Figure("rain_event_total_mm", "rain_source_url", "rain_tier"),
    Figure("affected_area_km2", "area_source_url", "area_tier", "area_method"),
    Figure("people_affected", "people_source_url"),
    Figure("deaths", "deaths_source_url"),
)

SITE_FIGURES = (
    Figure("catchment_area_km2", "catchment_area_source_url"),
    Figure("population", "population_source_url"),
    Figure("mean_elevation_m", "elevation_source_url"),
)

# What actually produced the extent. A levee or dam failure decouples inundated
# area from rainfall depth, so those rows are excluded from the model fit and
# reported separately rather than deleted.
DRIVERS = ("rainfall", "rainfall+dam_release", "dam_failure", "levee_failure", "storm_surge")
RAINFALL_DRIVEN = ("rainfall", "rainfall+dam_release")

# Area methods that measure water, versus methods that measure administrative
# geography and therefore cannot be used as a regression target.
MEASURED_AREA_METHODS = ("satellite", "aerial", "model", "survey")
PROXY_AREA_METHOD_MARKER = "administrative"

EXPECTED_SITE_COUNT = 12
EXPECTED_UAE_SITES = 2
