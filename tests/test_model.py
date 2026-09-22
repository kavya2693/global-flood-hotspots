"""Evaluation-design tests.

These assert properties of the harness, not of any particular estimator. The
one that matters most is that no site appears in both sides of a split — that
is the defect that would inflate every number in the README.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import LeaveOneGroupOut

from floodhotspots.features import TARGET
from floodhotspots.model import evaluate

FEATURES = ["log10_rain_24h_mm", "log10_catchment_area_km2"]


def synthetic(n_sites=8, per_site=6, seed=1):
    """Area is a known function of rainfall and catchment, so a working harness
    must recover a strong rank correlation and a broken one must not."""
    rng = np.random.default_rng(seed)
    rows = []
    for site in range(n_sites):
        catchment = rng.uniform(2.0, 4.0)
        for event in range(per_site):
            rain = rng.uniform(1.5, 2.9)
            rows.append(
                {
                    "event_id": f"s{site}_e{event}",
                    "site_id": f"s{site}",
                    "log10_rain_24h_mm": rain,
                    "log10_catchment_area_km2": catchment,
                    TARGET: 0.8 * rain + 0.5 * catchment + rng.normal(0, 0.05),
                }
            )
    return pd.DataFrame(rows)


def test_no_site_appears_on_both_sides_of_a_split():
    table = synthetic()
    splitter = LeaveOneGroupOut()
    for train_idx, test_idx in splitter.split(table, table[TARGET], table["site_id"]):
        train_sites = set(table.iloc[train_idx]["site_id"])
        test_sites = set(table.iloc[test_idx]["site_id"])
        assert train_sites.isdisjoint(test_sites)


def test_every_row_is_predicted_exactly_once():
    table = synthetic()
    scores = evaluate(table, FEATURES, "ridge", "check")
    assert scores.n == len(table)
    assert scores.predictions["event_id"].is_unique


def test_harness_recovers_a_known_relationship():
    scores = evaluate(synthetic(), FEATURES, "ridge", "check")
    assert scores.spearman > 0.8
    assert scores.mae_log10 < 0.25


def test_median_baseline_cannot_order_events_within_a_site():
    """The baseline predicts one value per held-out site, so it has no ordering
    skill where ordering is actually being asked for."""
    scores = evaluate(synthetic(), FEATURES, "median", "baseline")
    per_site = scores.predictions.groupby("site_id")["predicted_log10"].nunique()
    assert (per_site == 1).all()


def test_median_baseline_is_anti_informative_across_sites():
    """Worth asserting because it is counterintuitive and it shapes how the
    baseline row in the results table must be read.

    Leaving a site out removes that site's values from the training median. Hold
    out the largest-extent site and the median the model is left with is lower
    than it should be; hold out the smallest and it is higher. The prediction
    therefore moves against the truth, and the global Spearman comes out
    negative rather than near zero. The baseline is not a neutral reference
    point under this split, and a positive rho elsewhere has to beat that."""
    scores = evaluate(synthetic(), FEATURES, "median", "baseline")
    assert scores.spearman < 0


def test_shuffling_rainfall_destroys_a_rainfall_driven_signal():
    table = synthetic()
    honest = evaluate(table, ["log10_rain_24h_mm"], "ridge", "honest")
    shuffled = evaluate(table, ["log10_rain_24h_mm"], "ridge", "shuffled", shuffle_rainfall=True)
    assert shuffled.mae_log10 > honest.mae_log10


def test_shuffle_permutes_rather_than_discards():
    table = synthetic()
    scores = evaluate(table, FEATURES, "ridge", "shuffled", shuffle_rainfall=True)
    assert scores.n == len(table)


def test_two_observations_produce_a_refusal_rather_than_a_score():
    """The live dataset hits this path. It must not silently return a number."""
    import pytest

    from floodhotspots.model import NotEstimable

    table = synthetic(n_sites=2, per_site=1)
    with pytest.raises(NotEstimable, match="Leave-one-site-out needs at least"):
        evaluate(table, FEATURES, "ridge", "too small")


def test_three_sites_is_enough_to_attempt_a_fit():
    scores = evaluate(synthetic(n_sites=3, per_site=4), FEATURES, "ridge", "small")
    assert scores.n == 12
