import pandas as pd


def find_duplicate_route_ids(routes: pd.DataFrame) -> pd.DataFrame:
    """Return all route rows with duplicated route_id values."""
    return routes[routes.duplicated("route_id", keep=False)]


def find_duplicate_stop_ids(stops: pd.DataFrame) -> pd.DataFrame:
    """Return all stop rows with duplicated stop_id values."""
    return stops[stops.duplicated("stop_id", keep=False)]


def find_duplicate_trip_ids(trips: pd.DataFrame) -> pd.DataFrame:
    """Return all trip rows with duplicated trip_id values."""
    return trips[trips.duplicated("trip_id", keep=False)]


def find_duplicate_trip_stop_sequence_pairs(stop_times: pd.DataFrame) -> pd.DataFrame:
    """Return stop_times rows with duplicated (trip_id, stop_sequence)."""
    return stop_times[stop_times.duplicated(["trip_id", "stop_sequence"], keep=False)]
