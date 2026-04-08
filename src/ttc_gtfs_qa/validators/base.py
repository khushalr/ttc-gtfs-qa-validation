"""Shared validator helper functions."""

from __future__ import annotations

import pandas as pd


def empty_issue_frame(columns: list[str]) -> pd.DataFrame:
    """Return an empty DataFrame with a stable schema."""
    return pd.DataFrame(columns=columns)


def to_numeric(series: pd.Series) -> pd.Series:
    """Safely coerce a string series to numeric values."""
    return pd.to_numeric(series, errors="coerce")


def normalize_required_mask(series: pd.Series) -> pd.Series:
    """Find missing/blank GTFS values (NaN or whitespace)."""
    as_string = series.astype("string")
    return as_string.isna() | (as_string.str.strip() == "")
