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


def load_gtfs_data(data_path: Path = DATA_PATH) -> dict[str, pd.DataFrame]:
    """Load required GTFS files into pandas DataFrames."""
    return {
        key: pd.read_csv(data_path / filename)
        for key, filename in REQUIRED_FILES.items()
    }


def ensure_output_path(output_path: Path = OUTPUT_PATH) -> Path:
    """Create outputs directory when missing."""
    output_path.mkdir(exist_ok=True)
    return output_path
