"""Leave-one-site-out evaluation of a rainfall-to-extent regression.

The evaluation design matters more than the estimator. Events at the same site
share a catchment, a drainage standard and a reporting agency, so a random
split hands the test set rows whose neighbours the model has already memorised.
Every score below is produced by holding an entire site out.

Two scores are reported because they can disagree. MAE in log10 space asks how
close the predicted extent is in magnitude; Spearman asks only whether the
model ranks events correctly. A model that has learned "big basin, big flood"
and nothing else scores respectably on the first and can still be useless on
the second.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from scipy.stats import spearmanr

from .features import EXPOSURE_FEATURES, NUMERIC_FEATURES, RAINFALL_FEATURES, TARGET

SEED = 20260922


@dataclass
class Scores:
    name: str
    n: int
    mae_log10: float
    median_fold_error: float
    spearman: float
    spearman_p: float
    within_half_order: float
    predictions: pd.DataFrame = field(repr=False, default_factory=pd.DataFrame)

    def as_row(self) -> dict:
        return {
            "model": self.name,
            "n": self.n,
            "MAE (log10 km2)": round(self.mae_log10, 3),
            "Spearman rho": round(self.spearman, 3),
            "p": round(self.spearman_p, 4),
            "within 0.5 order": f"{self.within_half_order:.0%}",
        }


def _estimator(kind: str):
    if kind == "median":
        return DummyRegressor(strategy="median")
    if kind == "ridge":
        return Pipeline(
            [
                ("impute", SimpleImputer(strategy="median")),
                ("scale", StandardScaler()),
                ("fit", Ridge(alpha=1.0, random_state=None)),
            ]
        )
    if kind == "gbm":
        return Pipeline(
            [
                ("impute", SimpleImputer(strategy="median")),
                (
                    "fit",
                    GradientBoostingRegressor(
                        n_estimators=300,
                        learning_rate=0.05,
                        max_depth=2,
                        subsample=0.9,
                        random_state=SEED,
                    ),
                ),
            ]
        )
    raise ValueError(f"unknown estimator {kind!r}")


def evaluate(
    table: pd.DataFrame,
    features: list[str],
    kind: str,
    name: str,
    shuffle_rainfall: bool = False,
) -> Scores:
    """Leave-one-site-out. `shuffle_rainfall` breaks the rainfall-to-extent link
    while leaving every other feature intact — if the score survives that, the
    model was never using rainfall."""
    frame = table.copy()
    if shuffle_rainfall:
        rng = np.random.default_rng(SEED)
        present = [c for c in RAINFALL_FEATURES if c in frame.columns]
        frame[present] = frame[present].to_numpy()[rng.permutation(len(frame))]

    X = frame[features].astype(float)
    y = frame[TARGET].astype(float)
    groups = frame["site_id"]

    rows, fold_errors = [], []
    splitter = LeaveOneGroupOut()
    for train_idx, test_idx in splitter.split(X, y, groups):
        if len(train_idx) < 5:
            continue
        estimator = _estimator(kind)
        estimator.fit(X.iloc[train_idx], y.iloc[train_idx])
        predicted = estimator.predict(X.iloc[test_idx])
        fold_errors.append(float(np.mean(np.abs(predicted - y.iloc[test_idx]))))
        for position, index in enumerate(test_idx):
            rows.append(
                {
                    "event_id": frame.at[index, "event_id"],
                    "site_id": frame.at[index, "site_id"],
                    "actual_log10": float(y.iloc[index]),
                    "predicted_log10": float(predicted[position]),
                }
            )

    predictions = pd.DataFrame(rows)
    errors = (predictions["predicted_log10"] - predictions["actual_log10"]).abs()
    rho, p_value = spearmanr(predictions["actual_log10"], predictions["predicted_log10"])
    return Scores(
        name=name,
        n=len(predictions),
        mae_log10=float(errors.mean()),
        median_fold_error=float(np.median(fold_errors)) if fold_errors else float("nan"),
        spearman=float(rho),
        spearman_p=float(p_value),
        within_half_order=float((errors <= 0.5).mean()),
        predictions=predictions,
    )


def run_all(table: pd.DataFrame) -> list[Scores]:
    """The full arm list, including the two arms most likely to embarrass the
    headline: exposure with no rainfall at all, and rainfall shuffled."""
    available = [c for c in NUMERIC_FEATURES if c in table.columns]
    exposure_only = [c for c in EXPOSURE_FEATURES if c in table.columns]
    rainfall_only = [c for c in RAINFALL_FEATURES if c in table.columns]

    return [
        evaluate(table, available, "median", "baseline: site-blind median"),
        evaluate(table, rainfall_only, "ridge", "rainfall only (ridge)"),
        evaluate(table, exposure_only, "ridge", "exposure only, no rainfall (ridge)"),
        evaluate(table, available, "ridge", "rainfall + exposure (ridge)"),
        evaluate(table, available, "gbm", "rainfall + exposure (gradient boosting)"),
        evaluate(table, available, "gbm", "rainfall shuffled (gradient boosting)",
                 shuffle_rainfall=True),
    ]


def permutation_importance_loso(table: pd.DataFrame, features: list[str], repeats: int = 20) -> pd.DataFrame:
    """Importance measured on held-out sites, not on the training fit. A feature
    that only helps in-sample scores zero here, which is the point."""
    rng = np.random.default_rng(SEED)
    base = evaluate(table, features, "gbm", "base").mae_log10
    rows = []
    for feature in features:
        deltas = []
        for _ in range(repeats):
            shuffled = table.copy()
            shuffled[feature] = rng.permutation(shuffled[feature].to_numpy())
            deltas.append(evaluate(shuffled, features, "gbm", "perm").mae_log10 - base)
        rows.append({"feature": feature, "mae_increase_when_shuffled": float(np.mean(deltas))})
    return pd.DataFrame(rows).sort_values("mae_increase_when_shuffled", ascending=False)
