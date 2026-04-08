import pandas as pd


def find_bad_stop_sequences(stop_times: pd.DataFrame) -> list[str]:
    """Return trip_ids where stop_sequence decreases in file order."""
    bad_sequences: list[str] = []

    for trip_id, group in stop_times.groupby("trip_id", sort=False):
        sequence = group["stop_sequence"]
        if (sequence.diff() < 0).any():
            bad_sequences.append(trip_id)

    return bad_sequences
