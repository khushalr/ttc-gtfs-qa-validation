# TTC GTFS QA Validation

A small QA-style validation project for **TTC GTFS static feeds**.

This repo is built as an undergraduate-friendly portfolio project: clear checks, readable code, and CSV outputs that look like QA deliverables.
A small QA-style data validation project for **TTC GTFS static feeds**.

This repository is designed as an undergraduate portfolio project that demonstrates how to:
- load real transit schedule data,
- run repeatable validation checks,
- and produce simple QA outputs (test results + defect log).

---

## Project Scope

The validator currently reads:
The current script validates four GTFS files:
- `routes.txt`
- `trips.txt`
- `stops.txt`
- `stop_times.txt`

---

## Validation Rules (Plain English)

The script runs 8 rules:

1. **R-01 Duplicate `route_id`**  
   Every `route_id` should appear only once in `routes.txt`.
2. **R-02 Duplicate `stop_id`**  
   Every `stop_id` should appear only once in `stops.txt`.
3. **R-03 Duplicate `trip_id`**  
   Every `trip_id` should appear only once in `trips.txt`.
4. **R-04 Duplicate (`trip_id`, `stop_sequence`)**  
   In `stop_times.txt`, a trip should not repeat the same `stop_sequence` value.
5. **R-05 Foreign key check: `trips.route_id -> routes.route_id`**  
   Every `route_id` used by `trips.txt` must exist in `routes.txt`.
6. **R-06 Foreign key check: `stop_times.trip_id -> trips.trip_id`**  
   Every `trip_id` used by `stop_times.txt` must exist in `trips.txt`.
7. **R-07 Foreign key check: `stop_times.stop_id -> stops.stop_id`**  
   Every `stop_id` used by `stop_times.txt` must exist in `stops.txt`.
8. **R-08 `stop_sequence` order within each trip**  
   For each trip, `stop_sequence` should never decrease as rows progress.
> Note: The script currently reads these four files only. It does **not** read `calendar.txt` or `calendar_dates.txt` yet.

---

## Implemented QA Checks

The script (`src/run_tests.py`) runs 4 checks:

1. **TC-12 – Duplicate `trip_id` check** (in `trips.txt`)
2. **TC-05 – Orphan `stop_id` check** (in `stop_times.txt` vs `stops.txt`)
3. **TC-04 – Stop sequence ordering check** (within each `trip_id` in `stop_times.txt`)
4. **TC-02 – Orphan `route_id` check** (in `trips.txt` vs `routes.txt`)

Each check is recorded as Pass/Fail and, when failing, added to a defect log with severity and count.

---

## Project Structure

```text
ttc-gtfs-qa-validation/
├── data/
│   └── gtfs_static/           # place GTFS .txt files here (not committed)
├── outputs/                   # generated reports (not committed)
├── outputs/                   # generated after running tests (not committed)
├── src/
│   ├── run_tests.py           # compatibility entrypoint
│   └── ttc_gtfs_qa/
│       ├── cli.py
│       ├── io.py
│       ├── reporting.py
│       └── validators/
│           ├── foreign_keys.py
│           ├── keys.py
│           └── sequencing.py
│   └── run_tests.py           # main validation script
├── requirements.txt
└── README.md
```

---

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Put GTFS files in:
- `data/gtfs_static/routes.txt`
- `data/gtfs_static/trips.txt`
- `data/gtfs_static/stops.txt`
- `data/gtfs_static/stop_times.txt`
### 1) Create and activate a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Add GTFS files

Place the following files in `data/gtfs_static/`:
- `routes.txt`
- `trips.txt`
- `stops.txt`
- `stop_times.txt`

---

## Run

From repo root:
From the repository root (either command works):

```bash
python src/run_tests.py
# or
PYTHONPATH=src python -m ttc_gtfs_qa.cli
```

From the repository root:

```bash
python src/run_tests.py
```

Expected console output:
- `Loading GTFS data...`
- `Testing complete.`
- paths to generated CSV outputs

---

## Outputs

After execution, two files are created:

1. `outputs/summary_report.csv`  
   Columns: `Rule ID`, `Rule`, `Plain English`, `Result`, `Issue Count`
2. `outputs/defect_log.csv`  
   Columns: `Defect ID`, `Rule ID`, `Title`, `Dataset`, `Severity`, `Count`

If all rules pass, `defect_log.csv` will contain headers only.
After running, the script creates:

- `outputs/test_results.csv`  
  Columns: `Test Case`, `Description`, `Result`

- `outputs/defect_log.csv`  
  Columns: `Defect ID`, `Title`, `Dataset`, `Severity`, `Count`

If all tests pass, `defect_log.csv` may contain headers only.

---

## Why this project is useful

This project shows practical QA/data skills:
- data integrity validation,
- traceable test case IDs,
- defect logging with severity and counts,
- reproducible execution via a single script.

It is intentionally simple and readable so it can be extended in future phases.
