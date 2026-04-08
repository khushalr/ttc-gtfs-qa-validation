from pathlib import Path

import pandas as pd


SUMMARY_COLUMNS = ["Rule ID", "Rule", "Plain English", "Result", "Issue Count"]
DEFECT_COLUMNS = ["Defect ID", "Rule ID", "Title", "Dataset", "Severity", "Count"]


def build_summary_df(summary_rows: list[list]) -> pd.DataFrame:
    return pd.DataFrame(summary_rows, columns=SUMMARY_COLUMNS)


def build_defects_df(defect_rows: list[list]) -> pd.DataFrame:
    return pd.DataFrame(defect_rows, columns=DEFECT_COLUMNS)


def save_reports(summary_df: pd.DataFrame, defects_df: pd.DataFrame, output_path: Path) -> None:
    summary_df.to_csv(output_path / "summary_report.csv", index=False)
    defects_df.to_csv(output_path / "defect_log.csv", index=False)
