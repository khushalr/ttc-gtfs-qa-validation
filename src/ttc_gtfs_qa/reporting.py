from pathlib import Path

import pandas as pd


RESULT_COLUMNS = ["Test Case", "Description", "Result"]
DEFECT_COLUMNS = ["Defect ID", "Title", "Dataset", "Severity", "Count"]


def build_results_df(results: list[list]) -> pd.DataFrame:
    return pd.DataFrame(results, columns=RESULT_COLUMNS)


def build_defects_df(defects: list[list]) -> pd.DataFrame:
    return pd.DataFrame(defects, columns=DEFECT_COLUMNS)


def save_reports(results_df: pd.DataFrame, defects_df: pd.DataFrame, output_path: Path) -> None:
    results_df.to_csv(output_path / "test_results.csv", index=False)
    defects_df.to_csv(output_path / "defect_log.csv", index=False)
