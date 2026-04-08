"""Command-line entry point for GTFS QA validation."""

from __future__ import annotations

from ttc_gtfs_qa.engine import run_validations
from ttc_gtfs_qa.io import OUTPUT_PATH, ensure_output_path, load_gtfs_data
from ttc_gtfs_qa.reporting import (
    build_defect_log,
    build_metrics_report,
    build_summary_report,
    save_reports,
)


def main() -> None:
    """Run the GTFS data-quality pipeline and write CSV reports."""
    ensure_output_path(OUTPUT_PATH)

    print("Loading GTFS data...")
    data = load_gtfs_data()

    print("Running validation checks...")
    issues, issue_frames = run_validations(data)

    summary_df = build_summary_report(issues)
    defect_df = build_defect_log(issues, issue_frames)
    metrics_df = build_metrics_report(summary_df)

    save_reports(summary_df, defect_df, metrics_df, OUTPUT_PATH)

    print("Validation complete.")
    print("- outputs/summary_report.csv")
    print("- outputs/defect_log.csv")
    print("- outputs/metrics_report.csv")


if __name__ == "__main__":
    main()
