# TTC GTFS QA Validation

A small QA-style validation project for **TTC GTFS static feeds**.

This repo is built as an undergraduate-friendly portfolio project: clear checks, readable code, and CSV outputs that look like QA deliverables.

---

## Project Scope

The validator currently reads:
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

---

## Project Structure

```text
ttc-gtfs-qa-validation/
├── data/
│   └── gtfs_static/           # place GTFS .txt files here (not committed)
├── outputs/                   # generated reports (not committed)
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

---

## Run

From repo root:

```bash
python src/run_tests.py
# or
PYTHONPATH=src python -m ttc_gtfs_qa.cli
```

---

## Outputs

After execution, two files are created:

1. `outputs/summary_report.csv`  
   Columns: `Rule ID`, `Rule`, `Plain English`, `Result`, `Issue Count`
2. `outputs/defect_log.csv`  
   Columns: `Defect ID`, `Rule ID`, `Title`, `Dataset`, `Severity`, `Count`

If all rules pass, `defect_log.csv` will contain headers only.
