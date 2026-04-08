import pandas as pd

from ttc_gtfs_qa.engine import run_validations
from ttc_gtfs_qa.reporting import build_defect_log, build_metrics_report, build_summary_report


def minimal_gtfs_data() -> dict[str, pd.DataFrame]:
    return {
        "routes": pd.DataFrame(
            {
                "route_id": ["1"],
                "route_short_name": ["Line1"],
                "route_type": ["3"],
            }
        ),
        "trips": pd.DataFrame(
            {
                "route_id": ["1", "999"],
                "service_id": ["WKD", "BAD"],
                "trip_id": ["T1", "T2"],
                "shape_id": ["SH1", "MISSING_SHAPE"],
            }
        ),
        "stops": pd.DataFrame(
            {
                "stop_id": ["S1"],
                "stop_lat": ["43.65"],
                "stop_lon": ["-79.38"],
            }
        ),
        "stop_times": pd.DataFrame(
            {
                "trip_id": ["T1", "T1", "UNKNOWN_TRIP"],
                "arrival_time": ["08:00:00", "08:10:00", "bad_time"],
                "departure_time": ["08:00:00", "08:05:00", "08:00:00"],
                "stop_id": ["S1", "S1", "BAD_STOP"],
                "stop_sequence": ["1", "1", "2"],
            }
        ),
        "calendar": pd.DataFrame({"service_id": ["WKD"]}),
        "shapes": pd.DataFrame({"shape_id": ["SH1"]}),
    }


def test_run_validations_returns_issues() -> None:
    issues, issue_frames = run_validations(minimal_gtfs_data())

    assert len(issues) == 16
    assert "R-008" in issue_frames
    assert any(issue.status == "Fail" for issue in issues)


def test_reporting_outputs_have_expected_columns() -> None:
    issues, issue_frames = run_validations(minimal_gtfs_data())

    summary = build_summary_report(issues)
    defects = build_defect_log(issues, issue_frames)
    metrics = build_metrics_report(summary)

    assert {"rule_id", "status", "affected_records"}.issubset(summary.columns)
    assert {"defect_id", "rule_id", "affected_records"}.issubset(defects.columns)
    assert {"metric", "value"}.issubset(metrics.columns)
