"""Validation engine that orchestrates GTFS quality checks."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import pandas as pd

from .models import ValidationIssue
from .validators.calendar import service_id_relationships
from .validators.domain import invalid_lat_lon, route_trip_consistency, shape_trip_consistency
from .validators.foreign_keys import orphan_foreign_keys
from .validators.keys import duplicate_primary_keys, missing_required_values
from .validators.sequencing import invalid_stop_sequence, invalid_time_order

RuleFunction = Callable[[dict[str, pd.DataFrame]], pd.DataFrame]


@dataclass(frozen=True)
class ValidationRule:
    rule_id: str
    category: str
    name: str
    dataset: str
    severity: str
    details: str
    evaluator: RuleFunction


def build_rules() -> list[ValidationRule]:
    """Return the full portfolio rule set."""

    return [
        ValidationRule(
            "R-001",
            "primary_key",
            "Duplicate route_id in routes",
            "routes.txt",
            "High",
            "route_id must be unique in routes.txt",
            lambda d: duplicate_primary_keys(d["routes"], ["route_id"]),
        ),
        ValidationRule(
            "R-002",
            "primary_key",
            "Duplicate trip_id in trips",
            "trips.txt",
            "High",
            "trip_id must be unique in trips.txt",
            lambda d: duplicate_primary_keys(d["trips"], ["trip_id"]),
        ),
        ValidationRule(
            "R-003",
            "primary_key",
            "Duplicate stop_id in stops",
            "stops.txt",
            "High",
            "stop_id must be unique in stops.txt",
            lambda d: duplicate_primary_keys(d["stops"], ["stop_id"]),
        ),
        ValidationRule(
            "R-004",
            "primary_key",
            "Duplicate (trip_id, stop_sequence) in stop_times",
            "stop_times.txt",
            "High",
            "trip_id + stop_sequence should be unique per stop_times row",
            lambda d: duplicate_primary_keys(d["stop_times"], ["trip_id", "stop_sequence"]),
        ),
        ValidationRule(
            "R-005",
            "required_fields",
            "Missing required values in routes",
            "routes.txt",
            "Medium",
            "route_id, route_short_name, and route_type should be populated",
            lambda d: missing_required_values(d["routes"], ["route_id", "route_short_name", "route_type"]),
        ),
        ValidationRule(
            "R-006",
            "required_fields",
            "Missing required values in trips",
            "trips.txt",
            "Medium",
            "route_id, service_id, and trip_id should be populated",
            lambda d: missing_required_values(d["trips"], ["route_id", "service_id", "trip_id"]),
        ),
        ValidationRule(
            "R-007",
            "required_fields",
            "Missing required values in stop_times",
            "stop_times.txt",
            "Medium",
            "trip_id, arrival_time, departure_time, stop_id, and stop_sequence should be populated",
            lambda d: missing_required_values(
                d["stop_times"],
                ["trip_id", "arrival_time", "departure_time", "stop_id", "stop_sequence"],
            ),
        ),
        ValidationRule(
            "R-008",
            "referential_integrity",
            "Trips route_id exists in routes",
            "trips.txt",
            "High",
            "Every trips.route_id should exist in routes.route_id",
            lambda d: orphan_foreign_keys(d["trips"], "route_id", d["routes"], "route_id"),
        ),
        ValidationRule(
            "R-009",
            "referential_integrity",
            "Stop times trip_id exists in trips",
            "stop_times.txt",
            "High",
            "Every stop_times.trip_id should exist in trips.trip_id",
            lambda d: orphan_foreign_keys(d["stop_times"], "trip_id", d["trips"], "trip_id"),
        ),
        ValidationRule(
            "R-010",
            "referential_integrity",
            "Stop times stop_id exists in stops",
            "stop_times.txt",
            "High",
            "Every stop_times.stop_id should exist in stops.stop_id",
            lambda d: orphan_foreign_keys(d["stop_times"], "stop_id", d["stops"], "stop_id"),
        ),
        ValidationRule(
            "R-011",
            "sequencing",
            "Stop sequence strictly increases within trip",
            "stop_times.txt",
            "High",
            "stop_sequence should increase for each subsequent stop in a trip",
            lambda d: invalid_stop_sequence(d["stop_times"]),
        ),
        ValidationRule(
            "R-012",
            "time_logic",
            "Departure time not earlier than arrival time",
            "stop_times.txt",
            "Medium",
            "departure_time should be >= arrival_time",
            lambda d: invalid_time_order(d["stop_times"]),
        ),
        ValidationRule(
            "R-013",
            "domain_range",
            "Latitude/longitude ranges are valid",
            "stops.txt",
            "Medium",
            "stop_lat must be [-90, 90] and stop_lon must be [-180, 180]",
            lambda d: invalid_lat_lon(d["stops"]),
        ),
        ValidationRule(
            "R-014",
            "consistency",
            "Route-trip consistency",
            "trips.txt",
            "High",
            "trip route references should match valid routes",
            lambda d: route_trip_consistency(d["trips"], d["routes"]),
        ),
        ValidationRule(
            "R-015",
            "calendar",
            "Trips service_id exists in calendar data",
            "trips.txt",
            "Medium",
            "trip service_id should exist in calendar.txt or calendar_dates.txt when present",
            lambda d: service_id_relationships(d["trips"], d.get("calendar"), d.get("calendar_dates")),
        ),
        ValidationRule(
            "R-016",
            "shape_consistency",
            "Trips shape_id exists in shapes",
            "trips.txt",
            "Low",
            "when shape_id is populated, it should exist in shapes.txt",
            lambda d: shape_trip_consistency(d["trips"], d.get("shapes", pd.DataFrame())),
        ),
    ]


def run_validations(data: dict[str, pd.DataFrame]) -> tuple[list[ValidationIssue], dict[str, pd.DataFrame]]:
    """Execute all rules and return rule outcomes plus failed records."""
    issues: list[ValidationIssue] = []
    issue_frames: dict[str, pd.DataFrame] = {}

    for rule in build_rules():
        failed_rows = rule.evaluator(data)
        failed_count = len(failed_rows)
        status = "Pass" if failed_count == 0 else "Fail"

        issues.append(
            ValidationIssue(
                rule_id=rule.rule_id,
                category=rule.category,
                rule_name=rule.name,
                dataset=rule.dataset,
                severity=rule.severity,
                issue_count=failed_count,
                status=status,
                details=rule.details,
            )
        )
        issue_frames[rule.rule_id] = failed_rows

    return issues, issue_frames
