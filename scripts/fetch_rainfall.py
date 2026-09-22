#!/usr/bin/env python3
"""Re-derive event rainfall from ERA5 reanalysis instead of trusting the CSV.

This is deliberately optional. The committed dataset carries station rainfall
with a source URL per figure, so the repo runs from a clean clone with no
accounts. This script exists for the reader who wants to check the station
figures against an independent gridded product, and for extending the dataset
to events nobody has written up.

It fails immediately and loudly when credentials are absent, rather than
silently returning an empty array that would look like a legitimate zero.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from floodhotspots import io  # noqa: E402

REQUIRED = ("CDSAPI_URL", "CDSAPI_KEY")


def require_credentials() -> dict[str, str]:
    missing = [name for name in REQUIRED if not os.environ.get(name)]
    if missing:
        raise SystemExit(
            "missing credentials: " + ", ".join(missing) + "\n"
            "Copy .env.example to .env, register at https://cds.climate.copernicus.eu/ "
            "and fill in the key. This script will not guess."
        )
    return {name: os.environ[name] for name in REQUIRED}


def main() -> int:
    require_credentials()
    try:
        import cdsapi
    except ImportError:
        raise SystemExit("pip install cdsapi to use this script")

    sites, events = io.load()
    client = cdsapi.Client()
    out = ROOT / "data" / "raw" / "era5"
    out.mkdir(parents=True, exist_ok=True)

    for _, event in events.iterrows():
        site = sites.loc[sites["site_id"] == event["site_id"]].iloc[0]
        target = out / f"{event['event_id']}.nc"
        if target.exists():
            print(f"skip {target.name}, already present")
            continue
        start = str(event["start_date"])
        print(f"requesting {event['event_id']} ({start})")
        client.retrieve(
            "reanalysis-era5-single-levels",
            {
                "product_type": "reanalysis",
                "variable": "total_precipitation",
                "date": f"{start}/{event['end_date'] or start}",
                "time": [f"{hour:02d}:00" for hour in range(24)],
                # ERA5 wants north, west, south, east.
                "area": [site["bbox_n"], site["bbox_w"], site["bbox_s"], site["bbox_e"]],
                "format": "netcdf",
            },
            str(target),
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
