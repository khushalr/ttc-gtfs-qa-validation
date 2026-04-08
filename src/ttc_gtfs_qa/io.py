"""I/O utilities for reading GTFS files and writing outputs."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


DATA_PATH = Path("data/gtfs_static")
OUTPUT_PATH = Path("outputs")

REQUIRED_FILES = {
    "routes": "routes.txt",
    "trips": "trips.txt",
    "stops": "stops.txt",
    "stop_times": "stop_times.txt",
}

OPTIONAL_FILES = {
    "calendar": "calendar.txt",
    "calendar_dates": "calendar_dates.txt",
    "shapes": "shapes.txt",
}


def ensure_output_path(output_path: Path = OUTPUT_PATH) -> Path:
    """Create output directory if missing."""
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def _read_csv(path: Path) -> pd.DataFrame:
    """Read a GTFS CSV file as strings to keep IDs stable."""
    return pd.read_csv(path, dtype=str)


def load_gtfs_data(data_path: Path = DATA_PATH) -> dict[str, pd.DataFrame]:
    """Load required and optional GTFS data files.

    Raises:
        FileNotFoundError: if any required GTFS file is missing.
    """
    data: dict[str, pd.DataFrame] = {}

    for key, filename in REQUIRED_FILES.items():
        file_path = data_path / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Missing required GTFS file: {file_path}")
        data[key] = _read_csv(file_path)

    for key, filename in OPTIONAL_FILES.items():
        file_path = data_path / filename
        if file_path.exists():
            data[key] = _read_csv(file_path)

    return data
