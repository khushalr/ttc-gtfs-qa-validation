# TTC GTFS QA Validation

This project simulates a Test Analyst / QA engagement by validating TTC GTFS transit schedule data using automated test cases.

## Dataset
- TTC Routes and Schedules (GTFS Static)
- Files validated: routes.txt, trips.txt, stops.txt, stop_times.txt, calendar.txt, calendar_dates.txt

## What this project does
- Executes automated QA checks for schema and data integrity
- Produces a test execution report (pass/fail)
- Produces a defect log with severity and counts

## Implemented Test Cases
- TC-12 Duplicate trip_id detection
- TC-05 Orphan stop_id detection in stop_times
- TC-04 stop_sequence ordering within trip
- TC-02 Orphan route_id detection in trips

## How to run
1. Place GTFS files in `data/gtfs_static/`
2. Install dependencies:
   ```bash
   pip3 install pandas
