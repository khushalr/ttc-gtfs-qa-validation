import pandas as pd


def find_orphan_route_ids(trips: pd.DataFrame, routes: pd.DataFrame) -> pd.DataFrame:
    """Return trips rows whose route_id does not exist in routes."""
    return trips[~trips["route_id"].isin(routes["route_id"])]


def find_orphan_trip_ids(stop_times: pd.DataFrame, trips: pd.DataFrame) -> pd.DataFrame:
    """Return stop_times rows whose trip_id does not exist in trips."""
    return stop_times[~stop_times["trip_id"].isin(trips["trip_id"])]


def find_orphan_stop_ids(stop_times: pd.DataFrame, stops: pd.DataFrame) -> pd.DataFrame:
    """Return stop_times rows whose stop_id does not exist in stops."""
    return stop_times[~stop_times["stop_id"].isin(stops["stop_id"])]
def find_orphan_stop_ids(stop_times: pd.DataFrame, stops: pd.DataFrame) -> pd.DataFrame:
    """Return stop_times rows whose stop_id is missing in stops."""
    return stop_times[~stop_times["stop_id"].isin(stops["stop_id"])]


def find_orphan_route_ids(trips: pd.DataFrame, routes: pd.DataFrame) -> pd.DataFrame:
    """Return trips rows whose route_id is missing in routes."""
    return trips[~trips["route_id"].isin(routes["route_id"])]
