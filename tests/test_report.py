"""The unit conversion happens in exactly one place, so it is tested there."""

import pandas as pd
import pytest

from floodhotspots.report import mm_to_cm


@pytest.mark.parametrize(
    "millimetres,expected",
    [(254.0, "25.4"), (944, "94.4"), (0.0, "0.0"), (10, "1.0")],
)
def test_millimetres_convert_to_centimetres(millimetres, expected):
    assert mm_to_cm(millimetres) == expected


@pytest.mark.parametrize("missing", [None, "", float("nan"), pd.NA])
def test_missing_rainfall_reports_as_blank_not_zero(missing):
    """A blank cell means nobody published the figure. A zero would mean it did
    not rain, which is a different and false claim."""
    assert mm_to_cm(missing) == ""
