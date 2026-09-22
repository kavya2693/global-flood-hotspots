"""One entry point, five subcommands, and `run` does the lot.

    python -m floodhotspots run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

from . import features as feat
from . import io, model, report
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


def cmd_model(_: argparse.Namespace) -> int:
    sites, events = io.load()
    frame = feat.build(sites, events)
    table = feat.modelling_table(frame)
    if len(table) < 20:
        print(f"warning: only {len(table)} admissible events — every score below is fragile",
              file=sys.stderr)
    scores = model.run_all(table)
    REPORTS.mkdir(parents=True, exist_ok=True)
    rows = pd.DataFrame([s.as_row() for s in scores])
    rows.to_csv(REPORTS / "results.csv", index=False)
    print(rows.to_markdown(index=False))

    available = [c for c in feat.NUMERIC_FEATURES if c in table.columns]
    importance = model.permutation_importance_loso(table, available)
    importance.to_csv(REPORTS / "feature_importance.csv", index=False)
    print("\nPermutation importance on held-out sites:\n")
    print(importance.to_markdown(index=False))
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
    for step in (cmd_validate, cmd_features, cmd_model, cmd_report):
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
