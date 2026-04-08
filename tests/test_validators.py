import pandas as pd

from ttc_gtfs_qa.validators.domain import invalid_lat_lon
from ttc_gtfs_qa.validators.foreign_keys import orphan_foreign_keys
from ttc_gtfs_qa.validators.keys import duplicate_primary_keys, missing_required_values
from ttc_gtfs_qa.validators.sequencing import invalid_stop_sequence, invalid_time_order


def test_duplicate_primary_keys_finds_duplicates() -> None:
    routes = pd.DataFrame({"route_id": ["1", "1", "2"]})
    result = duplicate_primary_keys(routes, ["route_id"])
    assert len(result) == 2


def test_missing_required_values_detects_blank_and_null() -> None:
    trips = pd.DataFrame(
        {
            "route_id": ["1", "2"],
            "service_id": ["WKD", None],
            "trip_id": ["", "T2"],
        }
    )
    result = missing_required_values(trips, ["route_id", "service_id", "trip_id"])
    assert len(result) == 2


def test_orphan_foreign_keys_detects_orphans() -> None:
    stop_times = pd.DataFrame({"trip_id": ["T1", "T2", "T3"]})
    trips = pd.DataFrame({"trip_id": ["T1", "T2"]})
    result = orphan_foreign_keys(stop_times, "trip_id", trips, "trip_id")
    assert result["trip_id"].tolist() == ["T3"]


def test_invalid_stop_sequence_finds_non_increasing_values() -> None:
    stop_times = pd.DataFrame(
        {
            "trip_id": ["A", "A", "A"],
            "stop_sequence": ["1", "3", "2"],
        }
    )
    result = invalid_stop_sequence(stop_times)
    assert len(result) == 1


def test_invalid_time_order_finds_departure_before_arrival() -> None:
    stop_times = pd.DataFrame(
        {
            "arrival_time": ["08:00:00", "09:10:00"],
            "departure_time": ["08:05:00", "09:00:00"],
        }
    )
    result = invalid_time_order(stop_times)
    assert len(result) == 1


def test_invalid_lat_lon_finds_out_of_range_values() -> None:
    stops = pd.DataFrame(
        {
            "stop_id": ["S1", "S2"],
            "stop_lat": ["43.65", "99.0"],
            "stop_lon": ["-79.38", "-79.4"],
        }
    )
    result = invalid_lat_lon(stops)
    assert result["stop_id"].tolist() == ["S2"]
