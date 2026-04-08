"""Build reproducible CSV reports from validation outcomes."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .models import ValidationIssue

SUMMARY_COLUMNS = [
    "rule_id",
    "category",
    "rule_name",
    "dataset",
    "severity",
    "status",
    "affected_records",
    "details",
]

DEFECT_COLUMNS = [
    "defect_id",
    "rule_id",
    "severity",
    "dataset",
    "affected_records",
    "sample_record_count",
    "sample_record_ids",
]

METRICS_COLUMNS = [
    "metric",
    "value",
]


def build_summary_report(issues: list[ValidationIssue]) -> pd.DataFrame:
    """Build the top-level rule result report."""
    rows = [
        {
            "rule_id": issue.rule_id,
            "category": issue.category,
            "rule_name": issue.rule_name,
            "dataset": issue.dataset,
            "severity": issue.severity,
            "status": issue.status,
            "affected_records": issue.issue_count,
            "details": issue.details,
        }
        for issue in issues
    ]
    return pd.DataFrame(rows, columns=SUMMARY_COLUMNS)


def _sample_ids(df: pd.DataFrame) -> str:
    id_priority = ["trip_id", "route_id", "stop_id", "service_id"]
    for col in id_priority:
        if col in df.columns:
            values = df[col].dropna().astype(str).head(5).tolist()
            return ", ".join(values)
    return ""


def build_defect_log(issues: list[ValidationIssue], issue_frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Build detailed defect records for failed checks only."""
    rows: list[dict[str, str | int]] = []
    defect_index = 1

    for issue in issues:
        if issue.status == "Pass":
            continue

        frame = issue_frames[issue.rule_id]
        rows.append(
            {
                "defect_id": f"DEF-{defect_index:03d}",
                "rule_id": issue.rule_id,
                "severity": issue.severity,
                "dataset": issue.dataset,
                "affected_records": issue.issue_count,
                "sample_record_count": min(len(frame), 5),
                "sample_record_ids": _sample_ids(frame),
            }
        )
        defect_index += 1

    return pd.DataFrame(rows, columns=DEFECT_COLUMNS)


def build_metrics_report(summary_df: pd.DataFrame) -> pd.DataFrame:
    """Build high-level QA metrics for portfolio-style reporting."""
    total_rules = len(summary_df)
    failed_rules = int((summary_df["status"] == "Fail").sum())
    passed_rules = int((summary_df["status"] == "Pass").sum())
    total_affected = int(summary_df["affected_records"].sum())
    pass_rate = round((passed_rules / total_rules) * 100, 2) if total_rules else 0.0

    metrics = [
        {"metric": "total_rules", "value": total_rules},
        {"metric": "passed_rules", "value": passed_rules},
        {"metric": "failed_rules", "value": failed_rules},
        {"metric": "pass_rate_percent", "value": pass_rate},
        {"metric": "total_affected_records", "value": total_affected},
    ]
    return pd.DataFrame(metrics, columns=METRICS_COLUMNS)


def save_reports(
    summary_df: pd.DataFrame,
    defect_df: pd.DataFrame,
    metrics_df: pd.DataFrame,
    output_path: Path,
) -> None:
    """Persist all report CSV outputs."""
    summary_df.to_csv(output_path / "summary_report.csv", index=False)
    defect_df.to_csv(output_path / "defect_log.csv", index=False)
    metrics_df.to_csv(output_path / "metrics_report.csv", index=False)
