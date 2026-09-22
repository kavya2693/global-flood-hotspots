"""Feature derivation, and in particular what gets excluded from the fit.

The exclusion rules are the part of this module most likely to be quietly
loosened to make n look better, so each one has a test.
"""

import numpy as np
import pandas as pd

from floodhotspots.features import TARGET, build, exclusion_report, modelling_table
from floodhotspots.schema import EVENT_COLUMNS, SITE_COLUMNS

SITE = {
    "site_id": "s1", "site_name": "Somewhere", "country": "Nowhere", "iso3": "NWH",
    "bbox_w": 0.0, "bbox_s": 0.0, "bbox_e": 1.0, "bbox_n": 1.0,
    "mechanism": "riverine", "coastal": 0, "catchment_area_km2": 1000.0,
    "population": 1_000_000, "population_source_url": "https://e.org/p",
    "mean_elevation_m": 40.0, "elevation_source_url": "https://e.org/d",
    "selection_reason": "floods often", "selection_source_url": "https://e.org/s",
    "hotspot_subareas": "the low bit",
}

EVENT = {
    "event_id": "e1", "site_id": "s1", "start_date": "2020-07-01", "end_date": "2020-07-03",
    "rain_24h_mm": 200.0, "rain_station": "Gauge", "rain_event_total_mm": 400.0,
    "rain_source_url": "https://e.org/r", "rain_tier": "V1",
    "affected_area_km2": 100.0, "area_method": "satellite SAR extent",
    "area_source_url": "https://e.org/a", "area_tier": "V1",
    "people_affected": 5000, "people_source_url": "https://e.org/i",
    "deaths": 3, "deaths_source_url": "https://e.org/i",
    "driver": "rainfall", "notes": "",
}


def frames(**event_overrides):
    site = pd.DataFrame([SITE], columns=list(SITE_COLUMNS))
    event = dict(EVENT)
    event.update(event_overrides)
    return site, pd.DataFrame([event], columns=list(EVENT_COLUMNS))


def test_target_is_log10_of_area():
    frame = build(*frames())
    assert np.isclose(frame.loc[0, TARGET], 2.0)


def test_burst_ratio_is_daily_over_event_total():
    frame = build(*frames())
    assert np.isclose(frame.loc[0, "rain_burst_ratio"], 0.5)


def test_a_clean_rainfall_event_is_admissible():
    assert bool(build(*frames()).loc[0, "admissible"])


def test_dam_failure_extent_is_excluded_from_the_fit():
    frame = build(*frames(driver="dam_failure"))
    assert not bool(frame.loc[0, "admissible"])
    assert "dam_failure" in exclusion_report(frame).loc[0, "exclusion_reason"]


def test_levee_failure_extent_is_excluded_from_the_fit():
    assert not bool(build(*frames(driver="levee_failure")).loc[0, "admissible"])


def test_dam_release_alongside_rainfall_stays_admissible():
    """A reservoir release that accompanies the rain is still a rainfall event.
    A dam that fails is not."""
    assert bool(build(*frames(driver="rainfall+dam_release")).loc[0, "admissible"])


def test_administrative_area_is_excluded_from_the_fit():
    frame = build(*frames(area_method="administrative area of affected districts"))
    assert not bool(frame.loc[0, "admissible"])
    assert "administrative" in exclusion_report(frame).loc[0, "exclusion_reason"]


def test_event_without_an_area_is_excluded_but_kept_in_the_table():
    frame = build(*frames(affected_area_km2=None, area_method="", area_source_url="", area_tier=""))
    assert len(frame) == 1
    assert not bool(frame.loc[0, "admissible"])
    assert modelling_table(frame).empty


def test_event_without_rainfall_is_excluded():
    frame = build(*frames(rain_24h_mm=None))
    assert not bool(frame.loc[0, "admissible"])
    assert "no sourced 24h rainfall" in exclusion_report(frame).loc[0, "exclusion_reason"]


def test_exclusion_reasons_accumulate():
    frame = build(*frames(rain_24h_mm=None, driver="dam_failure"))
    reason = exclusion_report(frame).loc[0, "exclusion_reason"]
    assert "rainfall" in reason and "dam_failure" in reason


def test_zero_area_does_not_become_negative_infinity():
    frame = build(*frames(affected_area_km2=0))
    assert pd.isna(frame.loc[0, TARGET])
