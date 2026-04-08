"""Domain and range checks for GTFS values."""

from __future__ import annotations

import pandas as pd

from .base import to_numeric


def invalid_lat_lon(stops: pd.DataFrame) -> pd.DataFrame:
    """Return stops with invalid latitude/longitude values."""
    required = {"stop_lat", "stop_lon"}
    if not required.issubset(stops.columns):
        return stops.iloc[0:0].copy()

    working = stops.copy()
    lat = to_numeric(working["stop_lat"])
    lon = to_numeric(working["stop_lon"])

    bad_mask = lat.isna() | lon.isna() | (lat < -90) | (lat > 90) | (lon < -180) | (lon > 180)
    return working[bad_mask].copy()


def route_trip_consistency(trips: pd.DataFrame, routes: pd.DataFrame) -> pd.DataFrame:
    """Return trips using route_id values that do not exist in routes."""
    if "route_id" not in trips.columns or "route_id" not in routes.columns:
        return trips.iloc[0:0].copy()
    return trips[~trips["route_id"].isin(routes["route_id"].dropna().unique())].copy()


def shape_trip_consistency(trips: pd.DataFrame, shapes: pd.DataFrame) -> pd.DataFrame:
    """Return trips with shape_id not found in shapes, if shape tables are present."""
    if "shape_id" not in trips.columns or "shape_id" not in shapes.columns:
        return trips.iloc[0:0].copy()

    trip_with_shape = trips[trips["shape_id"].notna() & (trips["shape_id"].astype(str).str.strip() != "")]
    return trip_with_shape[~trip_with_shape["shape_id"].isin(shapes["shape_id"].dropna().unique())].copy()
