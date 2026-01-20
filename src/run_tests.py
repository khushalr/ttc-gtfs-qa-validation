import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/gtfs_static")
OUTPUT_PATH = Path("outputs")

OUTPUT_PATH.mkdir(exist_ok=True)

print("Loading GTFS data...")

routes = pd.read_csv(DATA_PATH / "routes.txt")
trips = pd.read_csv(DATA_PATH / "trips.txt")
stops = pd.read_csv(DATA_PATH / "stops.txt")
stop_times = pd.read_csv(DATA_PATH / "stop_times.txt")

results = []
defects = []

# Test 1: Duplicate trip_id
duplicate_trips = trips[trips.duplicated("trip_id", keep=False)]

if len(duplicate_trips) == 0:
    results.append(["TC-12", "Duplicate trip_id check", "Pass"])
else:
    results.append(["TC-12", "Duplicate trip_id check", "Fail"])
    defects.append(["DEF-001", "Duplicate trip_id found", "trips.txt", "High", len(duplicate_trips)])

# Test 2: Orphan stop_id in stop_times
orphan_stops = stop_times[~stop_times["stop_id"].isin(stops["stop_id"])]

if len(orphan_stops) == 0:
    results.append(["TC-05", "Orphan stop_id check", "Pass"])
else:
    results.append(["TC-05", "Orphan stop_id check", "Fail"])
    defects.append(["DEF-002", "Orphan stop_id found", "stop_times.txt", "High", len(orphan_stops)])

# Test 3: stop_sequence increasing
bad_sequences = []

for trip_id, group in stop_times.groupby("trip_id"):
    seq = group.sort_values("stop_sequence")["stop_sequence"]
    if not seq.is_monotonic_increasing:
        bad_sequences.append(trip_id)

if len(bad_sequences) == 0:
    results.append(["TC-04", "Stop sequence ordering", "Pass"])
else:
    results.append(["TC-04", "Stop sequence ordering", "Fail"])
    defects.append(["DEF-003", "Invalid stop_sequence ordering", "stop_times.txt", "High", len(bad_sequences)])

# Test 4: Orphan route_id in trips
orphan_routes = trips[~trips["route_id"].isin(routes["route_id"])]

if len(orphan_routes) == 0:
    results.append(["TC-02", "Orphan route_id in trips", "Pass"])
else:
    results.append(["TC-02", "Orphan route_id in trips", "Fail"])
    defects.append(["DEF-004", "Orphan route_id found in trips", "trips.txt", "High", len(orphan_routes)])

# Save outputs
results_df = pd.DataFrame(results, columns=["Test Case", "Description", "Result"])
defects_df = pd.DataFrame(defects, columns=["Defect ID", "Title", "Dataset", "Severity", "Count"])

results_df.to_csv(OUTPUT_PATH / "test_results.csv", index=False)
defects_df.to_csv(OUTPUT_PATH / "defect_log.csv", index=False)

print("Testing complete.")
print("Results saved to outputs/test_results.csv")
print("Defects saved to outputs/defect_log.csv")
