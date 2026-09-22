"""Coverage counting, including the case the project turns on: a figure that
exists for one variable and not the other."""

import pandas as pd

from floodhotspots.coverage import area_method_mix, pairing_rate, per_figure, per_site
from floodhotspots.schema import EVENT_COLUMNS

BLANK = {c: "" for c in EVENT_COLUMNS}


def events(*specs):
    rows = []
    for i, spec in enumerate(specs):
        row = dict(BLANK)
        row.update({"event_id": f"e{i}", "site_id": spec.get("site_id", "s1")})
        row.update(spec)
        rows.append(row)
    return pd.DataFrame(rows, columns=list(EVENT_COLUMNS))


def test_an_event_with_rainfall_but_no_area_is_not_paired():
    stats = pairing_rate(events({"rain_24h_mm": 200}))
    assert stats["with rainfall"] == 1
    assert stats["with area"] == 0
    assert stats["paired"] == 0


def test_an_event_with_area_but_no_rainfall_is_not_paired():
    stats = pairing_rate(events({"affected_area_km2": 500}))
    assert stats["paired"] == 0


def test_pairing_requires_both():
    stats = pairing_rate(events({"rain_24h_mm": 200, "affected_area_km2": 500}))
    assert stats["paired"] == 1
    assert stats["pairing_rate"] == 1.0


def test_blank_and_non_numeric_both_count_as_absent():
    stats = pairing_rate(events({"rain_24h_mm": ""}, {"rain_24h_mm": "about 200"}))
    assert stats["with rainfall"] == 0


def test_tier_counting_separates_strong_evidence():
    frame = per_figure(
        events(
            {"affected_area_km2": 10, "area_tier": "V1"},
            {"affected_area_km2": 20, "area_tier": "V3"},
        )
    )
    row = frame.loc[frame["figure"] == "inundated area"].iloc[0]
    assert row["events with a sourced value"] == 2
    assert row["of those, tier V1 or V2"] == 1


def test_per_site_orders_by_paired_events():
    sites = pd.DataFrame(
        [
            {"site_id": "s1", "site_name": "Thin", "country": "A"},
            {"site_id": "s2", "site_name": "Rich", "country": "B"},
        ]
    )
    frame = per_site(
        events(
            {"site_id": "s1", "rain_24h_mm": 100},
            {"site_id": "s2", "rain_24h_mm": 100, "affected_area_km2": 50},
        ),
        sites,
    )
    assert frame.loc[0, "site"] == "Rich"
    assert frame.loc[0, "with both"] == 1


def test_administrative_area_is_bucketed_apart_from_measured_extent():
    frame = area_method_mix(
        events(
            {"affected_area_km2": 10, "area_method": "administrative area of affected districts"},
            {"affected_area_km2": 20, "area_method": "Sentinel-1 SAR flood delineation"},
        )
    )
    methods = set(frame["measurement method"])
    assert "administrative district area, not an extent" in methods
    assert "satellite SAR" in methods
