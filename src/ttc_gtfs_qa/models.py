"""Data models used across the GTFS QA pipeline."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationIssue:
    """A single validation result for a rule.

    Attributes:
        rule_id: Stable rule identifier for traceability.
        category: High-level rule category for reporting.
        rule_name: Human-readable rule title.
        dataset: GTFS file name where issue was detected.
        severity: Business impact level (High/Medium/Low).
        issue_count: Number of affected records.
        status: Pass or Fail.
        details: Optional short explanation.
    """

    rule_id: str
    category: str
    rule_name: str
    dataset: str
    severity: str
    issue_count: int
    status: str
    details: str
