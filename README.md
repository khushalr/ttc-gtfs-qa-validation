# TTC GTFS QA Validation

A lightweight Python + pandas project that validates GTFS static feeds and produces reproducible QA reports.

This repository is intended as a student portfolio project for data analyst / researcher roles. It demonstrates practical data-quality workflows: key integrity, referential integrity, required fields, sequencing/time logic, and clear reporting.

## Why this project matters

Transit analytics depends on clean schedule data. When GTFS keys, relationships, or times are invalid, downstream outputs (route summaries, trip KPIs, stop analyses) become unreliable.

This project provides a repeatable QA pipeline with:
- rule-level pass/fail results,
- defect counts with severity,
- summary metrics for quick review.

## Implemented validation rules (actual code)

The current implementation runs **16 rules** from `src/ttc_gtfs_qa/engine.py`:

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
12. `departure_time < arrival_time` (and invalid time parsing)
13. Invalid `stop_lat` / `stop_lon` ranges
14. Route-trip consistency (`route_id`)
15. `trips.service_id` missing from `calendar` / `calendar_dates` (when those files exist)
16. `trips.shape_id` missing from `shapes` (when file exists)

## Project structure

```text
ttc-gtfs-qa-validation/
├── .github/
│   └── workflows/
│       └── ci.yml
├── examples/
│   └── sample_reports/
│       ├── defect_log.csv
│       ├── metrics_report.csv
│       └── summary_report.csv
├── src/
│   ├── run_tests.py
│   └── ttc_gtfs_qa/
│       ├── __init__.py
│       ├── cli.py
│       ├── engine.py
│       ├── io.py
│       ├── models.py
│       ├── reporting.py
│       └── validators/
│           ├── base.py
│           ├── calendar.py
│           ├── domain.py
│           ├── foreign_keys.py
│           ├── keys.py
│           └── sequencing.py
├── tests/
│   ├── test_engine_reporting.py
│   └── test_validators.py
├── LICENSE
├── pytest.ini
├── requirements.txt
└── README.md
```

## Input files

Put GTFS files in `data/gtfs_static/`.

Required:
- `routes.txt`
- `trips.txt`
- `stops.txt`
- `stop_times.txt`

Optional (used only if present):
- `calendar.txt`
- `calendar_dates.txt`
- `shapes.txt`

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python src/run_tests.py
```

## Test

```bash
pytest -q
```

## Outputs

Pipeline outputs are written to `outputs/`:

- `summary_report.csv`: one row per rule with category, severity, status, affected record count, and details.
- `defect_log.csv`: failed rules only, with defect ID, severity, affected record count, and sample IDs.
- `metrics_report.csv`: aggregate QA metrics (total rules, failed rules, pass rate, total affected records).

Sample output files are provided in `examples/sample_reports/`.

## Future improvements

- Track quality trends across multiple GTFS snapshots.
- Add configurable severity or threshold settings.
- Add a lightweight HTML summary view on top of CSV outputs.

## License

MIT (see `LICENSE`).
