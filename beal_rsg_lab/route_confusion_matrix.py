"""Confusion-matrix summaries for known-case route calibration."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from typing import Iterable, Protocol


class CalibrationLike(Protocol):
    case_id: str
    signature_text: str
    known_status: str
    expected_route: str
    system_route_label: str
    actual_route_label: str
    comparison_flag: str


@dataclass(frozen=True)
class RouteConfusionRecord:
    """Aggregate count for one calibration confusion bucket."""

    bucket: str
    case_count: int
    signatures: tuple[str, ...]
    case_ids: tuple[str, ...]
    expected_routes: tuple[str, ...]
    actual_labels: tuple[str, ...]
    interpretation: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signatures"] = ";".join(self.signatures)
        data["case_ids"] = ";".join(self.case_ids)
        data["expected_routes"] = ";".join(self.expected_routes)
        data["actual_labels"] = ";".join(self.actual_labels)
        return data


BUCKET_INTERPRETATIONS = {
    "known_impossible_system_weak": "Known impossible calibration case was not recognized by current RSG route signals.",
    "known_possible_obstruction_like": "Known possible or imprimitive calibration case received an obstruction-like label.",
    "artifact_correctly_demoted": "Artifact calibration case was correctly demoted.",
    "modular_method_correctly_routed": "Expected modular-method case was routed to external modular follow-up.",
    "false_positive": "System produced a strong route label where calibration expects caution.",
    "false_negative": "System stayed weak on a known impossible or expected-route case.",
    "uncertain_case": "Open or calibration-only case without a decisive expected comparison.",
    "route_mismatch": "Expected and actual route families disagree.",
    "calibrated_match": "Expected and actual route families align.",
}


def confusion_bucket(record: CalibrationLike) -> str:
    """Return the matrix bucket for one calibration result."""
    strong_labels = {"calibrated_route_candidate", "needs_external_sage_check"}
    weak_labels = {"not_promising_yet", "artifact_like"}
    system_label = getattr(record, "system_route_label", record.actual_route_label)

    if record.known_status == "known_impossible" and system_label in weak_labels:
        return "known_impossible_system_weak"
    if record.known_status == "known_possible" and system_label in strong_labels:
        return "known_possible_obstruction_like"
    if record.expected_route == "artifact" and system_label == "artifact_like":
        return "artifact_correctly_demoted"
    if record.expected_route == "modular_method" and system_label in {
        "needs_external_sage_check",
        "calibrated_route_candidate",
    }:
        return "modular_method_correctly_routed"
    if record.comparison_flag == "overpromotion":
        return "false_positive"
    if record.comparison_flag == "underpromotion":
        return "false_negative"
    if record.comparison_flag == "route_mismatch":
        return "route_mismatch"
    if record.comparison_flag == "calibrated_match":
        return "calibrated_match"
    return "uncertain_case"


def build_route_confusion_matrix(records: Iterable[CalibrationLike]) -> list[RouteConfusionRecord]:
    """Aggregate calibration records into route-confusion buckets."""
    groups: dict[str, list[CalibrationLike]] = defaultdict(list)
    for record in records:
        groups[confusion_bucket(record)].append(record)

    rows: list[RouteConfusionRecord] = []
    for bucket, items in groups.items():
        expected_counter = Counter(item.expected_route for item in items)
        actual_counter = Counter(item.actual_route_label for item in items)
        rows.append(
            RouteConfusionRecord(
                bucket=bucket,
                case_count=len(items),
                signatures=tuple(sorted({item.signature_text for item in items})),
                case_ids=tuple(sorted(item.case_id for item in items)),
                expected_routes=tuple(f"{key}:{expected_counter[key]}" for key in sorted(expected_counter)),
                actual_labels=tuple(f"{key}:{actual_counter[key]}" for key in sorted(actual_counter)),
                interpretation=BUCKET_INTERPRETATIONS.get(bucket, "Calibration bucket."),
            )
        )
    rows.sort(
        key=lambda item: (
            item.bucket in {"false_positive", "known_possible_obstruction_like"},
            item.bucket in {"false_negative", "known_impossible_system_weak", "route_mismatch"},
            item.case_count,
        ),
        reverse=True,
    )
    return rows
