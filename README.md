# TTC GTFS QA Validation Pipeline

Portfolio-ready Python project for validating public transit GTFS static feeds with **reproducible QA outputs**.

This project demonstrates how to turn raw transit schedule data into a structured data-quality process using:
- **Python + pandas**
- modular validation rules
- referential integrity checks
- anomaly detection checks
- reproducible CSV reporting
- automated tests and CI

Transit analytics quality depends on schedule data quality. If GTFS keys or relationships are broken, downstream analysis can be misleading (route-level summaries, trip-level KPIs, stop-level coverage, etc.).

## Why this matters (analytics/business value)

Transit analytics depends on trustworthy GTFS data. Small data errors can create big downstream problems:
- broken trip matching in ridership analysis,
- inaccurate stop-level dashboards,
- schedule-based KPIs that are wrong,
- failed map visualizations and routing logic.

This pipeline makes data-quality risks visible early by producing clear defect logs and summary metrics that can be shared with analysts, planners, and engineers.

---

## 30-second recruiter summary

- Built a modular GTFS QA pipeline in Python/pandas with **16 validation rules** across primary keys, required fields, referential integrity, sequencing, time logic, and domain/range checks.
- Implemented reproducible outputs (`summary_report.csv`, `defect_log.csv`, `metrics_report.csv`) with severities and affected record counts.
- Added unit tests with `pytest` and CI automation using GitHub Actions.
- Designed rule architecture to be easy to extend for additional agencies or datasets.

---

## Implemented validation checks

### 1) Primary key checks
- Duplicate `routes.route_id`
- Duplicate `trips.trip_id`
- Duplicate `stops.stop_id`
- Duplicate composite key `stop_times (trip_id, stop_sequence)`

### 2) Required field checks
- Missing required values in `routes`
- Missing required values in `trips`
- Missing required values in `stop_times`

### 3) Referential integrity checks
- `trips.route_id -> routes.route_id`
- `stop_times.trip_id -> trips.trip_id`
- `stop_times.stop_id -> stops.stop_id`

### 4) Sequence/time logic checks
- `stop_sequence` strictly increases within each `trip_id`
- `departure_time >= arrival_time`

### 5) Domain/range and consistency checks
- Valid `stop_lat` / `stop_lon` ranges
- Route-trip consistency
- `service_id` relationship validation with `calendar.txt` / `calendar_dates.txt` (if present)
- `shape_id` consistency with `shapes.txt` (if present)

---

## Project structure

```text
ttc-gtfs-qa-validation/
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   └── gtfs_static/                  # input GTFS files (not committed)
├── examples/
│   └── sample_reports/                # sample output CSVs for portfolio screenshots
├── outputs/                          # generated after running pipeline
├── src/
│   ├── run_tests.py                  # compatibility runner
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
├── pytest.ini
├── requirements.txt
├── pytest.ini
└── README.md
```

## Input files

## How to run

### 1) Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Add GTFS input files
Place these files in `data/gtfs_static/`:
- `routes.txt`
- `trips.txt`
- `stops.txt`
- `stop_times.txt`

Optional:
- `calendar.txt`
- `calendar_dates.txt`
- `shapes.txt`

### 3) Execute pipeline
```bash
python src/run_tests.py
```

### 4) Run tests
```bash
pytest -q
```

---

## Outputs

Running the pipeline writes:
- `outputs/summary_report.csv` → one row per validation rule with Pass/Fail and affected records.
- `outputs/defect_log.csv` → failed checks only, with severity and sample IDs.
- `outputs/metrics_report.csv` → QA KPIs (total rules, pass rate, total affected records).

Example files are included in `examples/sample_reports/`.

---

## Extending checks

To add a new rule:
1. Create a function in `src/ttc_gtfs_qa/validators/`.
2. Register it in `build_rules()` inside `src/ttc_gtfs_qa/engine.py`.
3. Add/extend unit tests under `tests/`.

This keeps additions simple and beginner-friendly while preserving a professional, modular structure.

## Optional future improvements

## Future improvements

- Add trend analysis over multiple feed snapshots.
- Add rule-level threshold configuration by agency.
- Export HTML dashboard reports in addition to CSV.
- Add optional Great Expectations integration for enterprise-style validation docs.

---

## Suggested resume bullets

- Built a modular **GTFS data-quality validation pipeline** in Python/pandas with 16 checks for primary keys, required fields, referential integrity, sequencing, and domain constraints.
- Designed reproducible QA reporting outputs (summary, defect log, and metrics) with severity levels and affected-record counts for stakeholder-friendly data quality monitoring.
- Implemented automated tests (`pytest`) and CI (GitHub Actions) to ensure reliability and maintainability of validation logic.
- Structured the project as an extensible analytics codebase with clear rule registration, reusable validators, and professional documentation.
