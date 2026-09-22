"""Loading the two committed tables, with validation wired in by default.

There is no code path that reads the dataset without checking it. Skipping the
check has to be asked for explicitly, and only the validator CLI asks.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .validate import Problem, validate

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
SITES_CSV = DATA_DIR / "sites.csv"
EVENTS_CSV = DATA_DIR / "events.csv"


class DatasetInvalid(RuntimeError):
    def __init__(self, problems: list[Problem]):
        self.problems = problems
        listing = "\n".join(f"  {p}" for p in problems[:40])
        more = "" if len(problems) <= 40 else f"\n  ... and {len(problems) - 40} more"
        super().__init__(f"{len(problems)} admissibility problems:\n{listing}{more}")


def load(data_dir: Path | None = None, check: bool = True) -> tuple[pd.DataFrame, pd.DataFrame]:
    directory = Path(data_dir) if data_dir else DATA_DIR
    sites = pd.read_csv(directory / "sites.csv", dtype={"site_id": str})
    events = pd.read_csv(directory / "events.csv", dtype={"event_id": str, "site_id": str})
    if check:
        problems = validate(sites, events)
        if problems:
            raise DatasetInvalid(problems)
    return sites, events
