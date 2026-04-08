# TTC GTFS QA Validation

Lightweight Python + pandas project that validates GTFS static files and generates reproducible QA reports.

This repo is designed as a student portfolio project for data analyst / researcher roles. It focuses on practical data-quality work: key integrity, referential integrity, required-field completeness, sequencing/time logic, and clean reporting outputs.

## Why this project matters

Transit analytics quality depends on schedule data quality. If GTFS keys or relationships are broken, downstream analysis can be misleading (route-level summaries, trip-level KPIs, stop-level coverage, etc.).

This project turns raw GTFS tables into a repeatable QA pipeline with:
- rule-level pass/fail status,
- defect counts with severity,
- summary metrics for quick review.

## What is implemented (actual rule set)

The current code runs **16 validation rules** from `src/ttc_gtfs_qa/engine.py`:

1. Duplicate `routes.route_id`
2. Duplicate `trips.trip_id`
3. Duplicate `stops.stop_id`
4. Duplicate `(trip_id, stop_sequence)` in `stop_times`
5. Missing required fields in `routes`
6. Missing required fields in `trips`
7. Missing required fields in `stop_times`
8. Orphan `trips.route_id -> routes.route_id`
9. Orphan `stop_times.trip_id -> trips.trip_id`
10. Orphan `stop_times.stop_id -> stops.stop_id`
11. Non-increasing `stop_sequence` within `trip_id`
12. `departure_time < arrival_time` or invalid times
13. Invalid stop latitude/longitude ranges
14. Route-trip consistency check (`route_id`)
15. `trips.service_id` not found in `calendar`/`calendar_dates` (when files exist)
16. `trips.shape_id` not found in `shapes` (when files exist)

## Project structure

```text
ttc-gtfs-qa-validation/
├── .github/workflows/ci.yml
├── examples/sample_reports/
├── src/
│   ├── run_tests.py
│   └── ttc_gtfs_qa/
│       ├── cli.py
│       ├── engine.py
│       ├── io.py
│       ├── models.py
│       ├── reporting.py
│       └── validators/
├── tests/
├── requirements.txt
├── pytest.ini
└── README.md
```

## Input files

Required GTFS files in `data/gtfs_static/`:
- `routes.txt`
- `trips.txt`
- `stops.txt`
- `stop_times.txt`

Optional (used only if present):
- `calendar.txt`
- `calendar_dates.txt`
- `shapes.txt`

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run validation:

```bash
python src/run_tests.py
```

Run tests:

```bash
pytest -q
```

## Outputs

Running the pipeline creates CSV files in `outputs/`:

- `summary_report.csv`
  - one row per rule
  - includes category, severity, status, affected record count, rule details
- `defect_log.csv`
  - failed rules only
  - includes defect ID, rule ID, severity, affected records, sample IDs
- `metrics_report.csv`
  - high-level QA metrics (total rules, failed rules, pass rate, total affected records)

Sample outputs are included in `examples/sample_reports/`.

## Testing and CI

- Unit tests are in `tests/` and use `pytest`.
- CI runs on push and pull requests via GitHub Actions (`.github/workflows/ci.yml`).

## Keep it extendable (without overengineering)

To add a rule:
1. Add a function in `src/ttc_gtfs_qa/validators/`.
2. Register it in `build_rules()` in `src/ttc_gtfs_qa/engine.py`.
3. Add/update tests in `tests/`.

## Optional future improvements

- Persist rule-level historical trends across multiple feed snapshots.
- Add configurable severity/threshold settings.
- Add a small HTML summary view on top of CSV outputs.

## License

MIT (see `LICENSE`).
