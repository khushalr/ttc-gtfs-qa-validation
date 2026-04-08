"""Sequence and time-order validation checks."""

from __future__ import annotations

import pandas as pd

from .base import to_numeric


def invalid_stop_sequence(stop_times: pd.DataFrame) -> pd.DataFrame:
    """Return rows where stop_sequence is not strictly increasing by trip."""
    if "trip_id" not in stop_times.columns or "stop_sequence" not in stop_times.columns:
        return stop_times.iloc[0:0].copy()

    working = stop_times.copy()
    working["stop_sequence_num"] = to_numeric(working["stop_sequence"])
    working["prev_stop_sequence"] = working.groupby("trip_id", sort=False)["stop_sequence_num"].shift(1)
    bad_mask = (
        working["stop_sequence_num"].isna()
        | (working["prev_stop_sequence"].notna() & (working["stop_sequence_num"] <= working["prev_stop_sequence"]))
    )
    return working[bad_mask].copy()


def invalid_time_order(stop_times: pd.DataFrame) -> pd.DataFrame:
    """Return rows where departure_time is earlier than arrival_time."""
    required = {"arrival_time", "departure_time"}
    if not required.issubset(stop_times.columns):
        return stop_times.iloc[0:0].copy()

    working = stop_times.copy()
    arrival = pd.to_timedelta(working["arrival_time"], errors="coerce")
    departure = pd.to_timedelta(working["departure_time"], errors="coerce")

    bad_mask = arrival.isna() | departure.isna() | (departure < arrival)
    return working[bad_mask].copy()
