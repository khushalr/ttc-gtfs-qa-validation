"""Calendar relationship checks for GTFS service IDs."""

from __future__ import annotations

import pandas as pd


def service_id_relationships(
    trips: pd.DataFrame,
    calendar: pd.DataFrame | None,
    calendar_dates: pd.DataFrame | None,
) -> pd.DataFrame:
    """Return trip rows whose service_id does not exist in calendar sources.

    If neither calendar file exists, this check returns an empty frame.
    """
    if "service_id" not in trips.columns:
        return trips.iloc[0:0].copy()

    service_ids: set[str] = set()

    if calendar is not None and "service_id" in calendar.columns:
        service_ids.update(calendar["service_id"].dropna().astype(str).tolist())

    if calendar_dates is not None and "service_id" in calendar_dates.columns:
        service_ids.update(calendar_dates["service_id"].dropna().astype(str).tolist())

    if not service_ids:
        return trips.iloc[0:0].copy()

    return trips[~trips["service_id"].astype(str).isin(service_ids)].copy()
