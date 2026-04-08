"""Referential integrity checks for GTFS relationships."""

from __future__ import annotations

import pandas as pd


def orphan_foreign_keys(
    child_df: pd.DataFrame,
    child_column: str,
    parent_df: pd.DataFrame,
    parent_column: str,
) -> pd.DataFrame:
    """Return child records whose foreign key does not exist in the parent table."""
    if child_column not in child_df.columns or parent_column not in parent_df.columns:
        return child_df.iloc[0:0].copy()

    parent_keys = parent_df[parent_column].dropna().unique()
    return child_df[~child_df[child_column].isin(parent_keys)].copy()
