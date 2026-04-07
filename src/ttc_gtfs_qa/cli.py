from ttc_gtfs_qa.io import OUTPUT_PATH, ensure_output_path, load_gtfs_data
from ttc_gtfs_qa.reporting import build_defects_df, build_results_df, save_reports
from ttc_gtfs_qa.validators.foreign_keys import find_orphan_route_ids, find_orphan_stop_ids
from ttc_gtfs_qa.validators.keys import find_duplicate_trip_ids
from ttc_gtfs_qa.validators.sequencing import find_bad_stop_sequences


def main() -> None:
    ensure_output_path(OUTPUT_PATH)

    print("Loading GTFS data...")
    data = load_gtfs_data()

    routes = data["routes"]
    trips = data["trips"]
    stops = data["stops"]
    stop_times = data["stop_times"]

    results: list[list] = []
    defects: list[list] = []

    duplicate_trips = find_duplicate_trip_ids(trips)
    if len(duplicate_trips) == 0:
        results.append(["TC-12", "Duplicate trip_id check", "Pass"])
    else:
        results.append(["TC-12", "Duplicate trip_id check", "Fail"])
        defects.append(["DEF-001", "Duplicate trip_id found", "trips.txt", "High", len(duplicate_trips)])

    orphan_stops = find_orphan_stop_ids(stop_times, stops)
    if len(orphan_stops) == 0:
        results.append(["TC-05", "Orphan stop_id check", "Pass"])
    else:
        results.append(["TC-05", "Orphan stop_id check", "Fail"])
        defects.append(["DEF-002", "Orphan stop_id found", "stop_times.txt", "High", len(orphan_stops)])

    bad_sequences = find_bad_stop_sequences(stop_times)
    if len(bad_sequences) == 0:
        results.append(["TC-04", "Stop sequence ordering", "Pass"])
    else:
        results.append(["TC-04", "Stop sequence ordering", "Fail"])
        defects.append(["DEF-003", "Invalid stop_sequence ordering", "stop_times.txt", "High", len(bad_sequences)])

    orphan_routes = find_orphan_route_ids(trips, routes)
    if len(orphan_routes) == 0:
        results.append(["TC-02", "Orphan route_id in trips", "Pass"])
    else:
        results.append(["TC-02", "Orphan route_id in trips", "Fail"])
        defects.append(["DEF-004", "Orphan route_id found in trips", "trips.txt", "High", len(orphan_routes)])

    results_df = build_results_df(results)
    defects_df = build_defects_df(defects)
    save_reports(results_df, defects_df, OUTPUT_PATH)

    print("Testing complete.")
    print("Results saved to outputs/test_results.csv")
    print("Defects saved to outputs/defect_log.csv")


if __name__ == "__main__":
    main()
