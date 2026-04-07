import pandas as pd


def find_duplicate_trip_ids(trips: pd.DataFrame) -> pd.DataFrame:
    """Return all rows with duplicated trip_id values."""
    return trips[trips.duplicated("trip_id", keep=False)]
