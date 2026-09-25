"""One entry point, five subcommands, and `run` does the lot.

    python -m floodhotspots run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

from . import coverage, io, model, report
from . import features as feat
from .validate import validate

ROOT = Path(__file__).resolve().parents[2]
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"


def cmd_validate(_: argparse.Namespace) -> int:
    sites, events = io.load(check=False)
    problems = validate(sites, events)
    if not problems:
        print(f"ok: {len(sites)} sites, {len(events)} events, no admissibility problems")
        return 0
    for problem in problems:
        print(problem)
    print(f"\n{len(problems)} problems", file=sys.stderr)
    return 1


def cmd_features(_: argparse.Namespace) -> int:
    sites, events = io.load()
    frame = feat.build(sites, events)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    frame.to_csv(PROCESSED / "events_features.csv", index=False)
    excluded = feat.exclusion_report(frame)
    excluded.to_csv(PROCESSED / "excluded_events.csv", index=False)
    print(f"{len(frame)} events, {int(frame['admissible'].sum())} admissible, {len(excluded)} excluded")
    return 0


def cmd_coverage(_: argparse.Namespace) -> int:
    """The headline result, so it runs before the model and prints first."""
    sites, events = io.load()
    REPORTS.mkdir(parents=True, exist_ok=True)

    stats = coverage.pairing_rate(events)
    print(
        f"{stats['events']} events across {len(sites)} sites. "
        f"{stats['with rainfall']} carry a sourced 24h rainfall, "
        f"{stats['with area']} a sourced inundated area, "
        f"{stats['paired']} carry both ({stats['pairing_rate']:.1%})."
    )

    figures = coverage.per_figure(events)
    by_site = coverage.per_site(events, sites)
    split = coverage.measurement_split(events, sites)
    methods = coverage.area_method_mix(events)
    correlation = coverage.coverage_correlation(events, sites)

    for name, frame in (
        ("coverage_by_figure", figures),
        ("coverage_by_site", by_site),
        ("coverage_measurement_split", split),
        ("area_methods", methods),
    ):
        frame.to_csv(REPORTS / f"{name}.csv", index=False)

    print("\n" + report.markdown_table(figures))
    print("\n" + report.markdown_table(by_site))
    print(
        f"\nRainfall coverage against extent coverage across {correlation['sites']} sites: "
        f"Spearman {correlation['spearman']:.2f}, p = {correlation['p']:.4f}. "
        "The two measurements are made in different places."
    )
    pd.DataFrame([correlation]).to_csv(REPORTS / "coverage_correlation.csv", index=False)
    return 0


def cmd_model(_: argparse.Namespace) -> int:
    sites, events = io.load()
    frame = feat.build(sites, events)
    table = feat.modelling_table(frame)
    print(f"{len(table)} of {len(frame)} events are admissible for the fit")
    try:
        scores = model.run_all(table)
    except model.NotEstimable as refusal:
        print(f"\nNo model fitted. {refusal}")
        print(
            "This is the project's result, not a failure to reach it. See "
            "reports/coverage_by_site.csv for where the record breaks."
        )
        (REPORTS / "results.md").parent.mkdir(parents=True, exist_ok=True)
        (REPORTS / "results.md").write_text(
            f"# Model results\n\nNo model was fitted.\n\n{refusal}\n", encoding="utf-8"
        )
        return 0
    REPORTS.mkdir(parents=True, exist_ok=True)
    rows = pd.DataFrame([s.as_row() for s in scores])
    rows.to_csv(REPORTS / "results.csv", index=False)
    print(report.markdown_table(rows))

    available = model.usable_features(table, feat.NUMERIC_FEATURES)
    importance = model.permutation_importance_loso(table, available)
    importance.to_csv(REPORTS / "feature_importance.csv", index=False)
    print("\nPermutation importance on held-out sites:\n")
    print(report.markdown_table(importance))
    return 0


def cmd_report(_: argparse.Namespace) -> int:
    sites, events = io.load()
    frame = feat.build(sites, events)
    report.write(REPORTS / "site-profiles.md", report.site_profiles(sites, frame))
    report.write(
        REPORTS / "excluded-events.md",
        "# Events excluded from the model fit\n\n"
        "Kept in the dataset, dropped from the regression, and listed here so the\n"
        "exclusion is visible rather than silent.\n\n"
        + report.exclusions_table(feat.exclusion_report(frame)),
    )
    print(f"wrote {REPORTS / 'site-profiles.md'} and {REPORTS / 'excluded-events.md'}")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    for step in (cmd_validate, cmd_coverage, cmd_features, cmd_model, cmd_report):
        print(f"\n=== {step.__name__.removeprefix('cmd_')} ===")
        code = step(args)
        if code != 0:
            return code
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="floodhotspots")
    sub = parser.add_subparsers(dest="command", required=True)
    for name, handler, help_text in (
        ("validate", cmd_validate, "check the committed tables for admissibility problems"),
        ("coverage", cmd_coverage, "audit what the public record actually contains"),
        ("features", cmd_features, "build the modelling table and the exclusion list"),
        ("model", cmd_model, "run every evaluation arm, leave-one-site-out"),
        ("report", cmd_report, "write the site profiles and exclusion report"),
        ("run", cmd_run, "all of the above, in order"),
    ):
        sub.add_parser(name, help=help_text).set_defaults(handler=handler)
    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
