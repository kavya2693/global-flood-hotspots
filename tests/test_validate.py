"""The validator is tested against deliberately broken tables.

A validator that has only ever seen good input proves nothing. Each test here
breaks exactly one thing and asserts that exactly that rule fires.
"""

import pandas as pd
import pytest

from floodhotspots.schema import EVENT_COLUMNS, SITE_COLUMNS
from floodhotspots.validate import validate_events, validate_sites

GOOD_SITE = {
    "site_id": "are_dubai",
    "site_name": "Dubai-Sharjah",
    "country": "United Arab Emirates",
    "iso3": "ARE",
    "bbox_w": 55.0,
    "bbox_s": 25.0,
    "bbox_e": 55.6,
    "bbox_n": 25.5,
    "mechanism": "arid urban pluvial",
    "coastal": 1,
    "catchment_area_km2": 900.0,
    "population": 3_600_000,
    "population_source_url": "https://example.gov/population",
    "mean_elevation_m": 12.0,
    "elevation_source_url": "https://example.org/dem",
    "selection_reason": "recurring urban pluvial flooding",
    "selection_source_url": "https://example.org/report",
    "hotspot_subareas": "Mirdif; Al Qusais",
}

GOOD_EVENT = {
    "event_id": "are_dubai_2024_04",
    "site_id": "are_dubai",
    "start_date": "2024-04-16",
    "end_date": "2024-04-17",
    "rain_24h_mm": 254.0,
    "rain_station": "Khatm Al Shakla",
    "rain_event_total_mm": 260.0,
    "rain_source_url": "https://www.ncm.gov.ae/report",
    "rain_tier": "V1",
    "affected_area_km2": 120.0,
    "area_method": "satellite SAR-derived extent",
    "area_source_url": "https://example.org/sar",
    "area_tier": "V1",
    "people_affected": 100_000,
    "people_source_url": "https://example.org/impact",
    "deaths": 4,
    "deaths_source_url": "https://example.org/impact",
    "driver": "rainfall",
    "notes": "",
}


def sites_frame(**overrides):
    """Twelve sites, two of them UAE, so a clean frame raises nothing."""
    rows = []
    for i in range(12):
        row = dict(GOOD_SITE)
        row["site_id"] = f"site_{i:02d}"
        row["iso3"] = "ARE" if i < 2 else "IND"
        rows.append(row)
    rows[0].update(overrides)
    return pd.DataFrame(rows, columns=list(SITE_COLUMNS))


def events_frame(**overrides):
    row = dict(GOOD_EVENT)
    row["site_id"] = "site_00"
    row.update(overrides)
    return pd.DataFrame([row], columns=list(EVENT_COLUMNS))


def rules(problems):
    return {p.rule for p in problems}


def test_clean_tables_raise_nothing():
    assert validate_sites(sites_frame()) == []
    assert validate_events(events_frame(), sites_frame()) == []


# --- the rule the project rests on -------------------------------------------

def test_figure_without_source_url_is_rejected():
    problems = validate_events(events_frame(rain_source_url=""), sites_frame())
    assert "no_source" in rules(problems)


def test_figure_with_non_url_source_is_rejected():
    problems = validate_events(events_frame(area_source_url="Reuters, April 2024"), sites_frame())
    assert "bad_source" in rules(problems)


def test_figure_without_tier_is_rejected():
    problems = validate_events(events_frame(area_tier=""), sites_frame())
    assert "no_tier" in rules(problems)


def test_inferred_figure_without_a_note_is_rejected():
    problems = validate_events(events_frame(area_tier="I", notes=""), sites_frame())
    assert "unexplained_inference" in rules(problems)


def test_inferred_figure_with_a_note_is_accepted():
    problems = validate_events(
        events_frame(area_tier="I", notes="scaled from the 2016 event extent"), sites_frame()
    )
    assert "unexplained_inference" not in rules(problems)


def test_area_without_a_method_is_rejected():
    problems = validate_events(events_frame(area_method=""), sites_frame())
    assert "no_method" in rules(problems)


# --- unit and typo traps ------------------------------------------------------

def test_rainfall_recorded_in_centimetres_is_caught_as_a_bound_violation():
    """25.4 cm entered where 254 mm belongs is silently plausible to a human.
    It is not plausible for a national daily record, so the bound catches it."""
    problems = validate_events(events_frame(rain_24h_mm=25_400.0), sites_frame())
    assert "out_of_bounds" in rules(problems)


def test_event_total_below_its_own_daily_peak_is_rejected():
    problems = validate_events(
        events_frame(rain_24h_mm=254.0, rain_event_total_mm=100.0), sites_frame()
    )
    assert "total_below_daily" in rules(problems)


def test_non_numeric_figure_is_rejected():
    problems = validate_events(events_frame(affected_area_km2="about 120"), sites_frame())
    assert "not_numeric" in rules(problems)


# --- structural ---------------------------------------------------------------

def test_event_pointing_at_an_unknown_site_is_rejected():
    problems = validate_events(events_frame(site_id="atlantis"), sites_frame())
    assert "orphan_event" in rules(problems)


def test_reversed_dates_are_rejected():
    problems = validate_events(
        events_frame(start_date="2024-04-17", end_date="2024-04-16"), sites_frame()
    )
    assert "reversed_dates" in rules(problems)


def test_future_event_is_rejected():
    problems = validate_events(
        events_frame(start_date="2099-01-01", end_date="2099-01-02"), sites_frame()
    )
    assert "future_date" in rules(problems)


def test_undeclared_driver_is_rejected():
    problems = validate_events(events_frame(driver=""), sites_frame())
    assert "no_driver" in rules(problems)


def test_unknown_driver_is_rejected():
    problems = validate_events(events_frame(driver="volcano"), sites_frame())
    assert "bad_driver" in rules(problems)


def test_missing_column_is_reported_and_stops_further_checks():
    frame = events_frame().drop(columns=["driver"])
    problems = validate_events(frame, sites_frame())
    assert rules(problems) == {"missing_column"}


def test_wrong_site_count_is_rejected():
    frame = sites_frame().iloc[:5]
    assert "wrong_site_count" in rules(validate_sites(frame))


def test_wrong_uae_count_is_rejected():
    frame = sites_frame()
    frame.loc[0, "iso3"] = "IND"
    assert "wrong_uae_count" in rules(validate_sites(frame))


def test_duplicate_site_id_is_rejected():
    frame = sites_frame()
    frame.loc[1, "site_id"] = "site_00"
    assert "duplicate_id" in rules(validate_sites(frame))


@pytest.mark.parametrize(
    "overrides",
    [
        {"bbox_w": 55.6, "bbox_e": 55.0},
        {"bbox_s": 25.5, "bbox_n": 25.0},
        {"bbox_n": 991.0},
    ],
)
def test_malformed_bbox_is_rejected(overrides):
    assert "bad_bbox" in rules(validate_sites(sites_frame(**overrides)))
