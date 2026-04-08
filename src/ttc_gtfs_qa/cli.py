from ttc_gtfs_qa.io import OUTPUT_PATH, ensure_output_path, load_gtfs_data
from ttc_gtfs_qa.reporting import build_defects_df, build_summary_df, save_reports
from ttc_gtfs_qa.validators.foreign_keys import (
    find_orphan_route_ids,
    find_orphan_stop_ids,
    find_orphan_trip_ids,
)
from ttc_gtfs_qa.validators.keys import (
    find_duplicate_route_ids,
    find_duplicate_stop_ids,
    find_duplicate_trip_ids,
    find_duplicate_trip_stop_sequence_pairs,
)
from ttc_gtfs_qa.validators.sequencing import find_bad_stop_sequences


def evaluate_rule(summary_rows: list[list], defect_rows: list[list], rule: dict) -> None:
    issue_count = int(rule["issue_count"])
    passed = issue_count == 0

    summary_rows.append([
        rule["rule_id"],
        rule["rule_name"],
        rule["plain_english"],
        "Pass" if passed else "Fail",
        issue_count,
    ])

    if not passed:
        defect_rows.append([
            rule["defect_id"],
            rule["rule_id"],
            rule["defect_title"],
            rule["dataset"],
            "High",
            issue_count,
        ])


def main() -> None:
    ensure_output_path(OUTPUT_PATH)

    print("Loading GTFS data...")
    data = load_gtfs_data()

    routes = data["routes"]
    trips = data["trips"]
    stops = data["stops"]
    stop_times = data["stop_times"]

    summary_rows: list[list] = []
    defect_rows: list[list] = []

    rules = [
        {
            "rule_id": "R-01",
            "rule_name": "Duplicate route_id",
            "plain_english": "Each route_id should appear only once in routes.txt.",
            "issue_count": len(find_duplicate_route_ids(routes)),
            "defect_id": "DEF-001",
            "defect_title": "Duplicate route_id found",
            "dataset": "routes.txt",
        },
        {
            "rule_id": "R-02",
            "rule_name": "Duplicate stop_id",
            "plain_english": "Each stop_id should appear only once in stops.txt.",
            "issue_count": len(find_duplicate_stop_ids(stops)),
            "defect_id": "DEF-002",
            "defect_title": "Duplicate stop_id found",
            "dataset": "stops.txt",
        },
        {
            "rule_id": "R-03",
            "rule_name": "Duplicate trip_id",
            "plain_english": "Each trip_id should appear only once in trips.txt.",
            "issue_count": len(find_duplicate_trip_ids(trips)),
            "defect_id": "DEF-003",
            "defect_title": "Duplicate trip_id found",
            "dataset": "trips.txt",
        },
        {
            "rule_id": "R-04",
            "rule_name": "Duplicate (trip_id, stop_sequence)",
            "plain_english": "Within stop_times.txt, a trip should not repeat the same stop_sequence value.",
            "issue_count": len(find_duplicate_trip_stop_sequence_pairs(stop_times)),
            "defect_id": "DEF-004",
            "defect_title": "Duplicate (trip_id, stop_sequence) found",
            "dataset": "stop_times.txt",
        },
        {
            "rule_id": "R-05",
            "rule_name": "Foreign key: trips.route_id -> routes.route_id",
            "plain_english": "Every route_id in trips.txt must exist in routes.txt.",
            "issue_count": len(find_orphan_route_ids(trips, routes)),
            "defect_id": "DEF-005",
            "defect_title": "Orphan route_id found in trips",
            "dataset": "trips.txt",
        },
        {
            "rule_id": "R-06",
            "rule_name": "Foreign key: stop_times.trip_id -> trips.trip_id",
            "plain_english": "Every trip_id in stop_times.txt must exist in trips.txt.",
            "issue_count": len(find_orphan_trip_ids(stop_times, trips)),
            "defect_id": "DEF-006",
            "defect_title": "Orphan trip_id found in stop_times",
            "dataset": "stop_times.txt",
        },
        {
            "rule_id": "R-07",
            "rule_name": "Foreign key: stop_times.stop_id -> stops.stop_id",
            "plain_english": "Every stop_id in stop_times.txt must exist in stops.txt.",
            "issue_count": len(find_orphan_stop_ids(stop_times, stops)),
            "defect_id": "DEF-007",
            "defect_title": "Orphan stop_id found in stop_times",
            "dataset": "stop_times.txt",
        },
        {
            "rule_id": "R-08",
            "rule_name": "stop_sequence order within trip",
            "plain_english": "Within each trip, stop_sequence should never decrease as rows progress.",
            "issue_count": len(find_bad_stop_sequences(stop_times)),
            "defect_id": "DEF-008",
            "defect_title": "Invalid stop_sequence ordering",
            "dataset": "stop_times.txt",
        },
    ]

    for rule in rules:
        evaluate_rule(summary_rows, defect_rows, rule)

    summary_df = build_summary_df(summary_rows)
    defects_df = build_defects_df(defect_rows)
    save_reports(summary_df, defects_df, OUTPUT_PATH)

    print("Testing complete.")
    print("Results saved to outputs/summary_report.csv")
    print("Defects saved to outputs/defect_log.csv")


if __name__ == "__main__":
    main()
