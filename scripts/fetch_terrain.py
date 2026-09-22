#!/usr/bin/env python3
"""Pull Copernicus GLO-30 elevation for each site bounding box.

Same contract as fetch_rainfall.py: optional, and it refuses to run rather than
degrade when the key is missing. Output is one GeoTIFF per site under
data/raw/dem/, which nothing in the default pipeline reads.
"""

from __future__ import annotations

import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from floodhotspots import io  # noqa: E402

ENDPOINT = "https://portal.opentopography.org/API/globaldem"


def main() -> int:
    key = os.environ.get("OPENTOPOGRAPHY_API_KEY")
    if not key:
        raise SystemExit(
            "missing OPENTOPOGRAPHY_API_KEY. Copy .env.example to .env and register at "
            "https://portal.opentopography.org/ . This script will not guess."
        )

    sites, _ = io.load()
    out = ROOT / "data" / "raw" / "dem"
    out.mkdir(parents=True, exist_ok=True)

    for _, site in sites.iterrows():
        target = out / f"{site['site_id']}.tif"
        if target.exists():
            print(f"skip {target.name}, already present")
            continue
        query = urllib.parse.urlencode(
            {
                "demtype": "COP30",
                "south": site["bbox_s"],
                "north": site["bbox_n"],
                "west": site["bbox_w"],
                "east": site["bbox_e"],
                "outputFormat": "GTiff",
                "API_Key": key,
            }
        )
        print(f"requesting {site['site_id']}")
        with urllib.request.urlopen(f"{ENDPOINT}?{query}") as response:
            if response.status != 200:
                raise SystemExit(f"{site['site_id']}: HTTP {response.status}")
            target.write_bytes(response.read())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
