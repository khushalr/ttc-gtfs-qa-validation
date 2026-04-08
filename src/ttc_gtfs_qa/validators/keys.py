"""Primary-key and required-field checks."""

from __future__ import annotations

import pandas as pd

from .base import normalize_required_mask


def duplicate_primary_keys(df: pd.DataFrame, key_columns: list[str]) -> pd.DataFrame:
    """Return rows that duplicate a primary key definition."""
    return df[df.duplicated(subset=key_columns, keep=False)].copy()


def missing_required_values(df: pd.DataFrame, required_columns: list[str]) -> pd.DataFrame:
    """Return rows with missing required values in any required column."""
    mask = pd.Series(False, index=df.index)
    for column in required_columns:
        if column not in df.columns:
            continue
        mask |= normalize_required_mask(df[column])
    return df[mask].copy()
