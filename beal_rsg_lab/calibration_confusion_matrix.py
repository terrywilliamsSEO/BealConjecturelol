"""Theorem-terrain-aware calibration matrix."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from typing import Iterable, Protocol


class TerrainCalibrationLike(Protocol):
    case_id: str
    signature_text: str
    expected_route: str
    terrain_label: str
    known_status_label: str
    system_route_label: str
    actual_route_label: str
    comparison_flag: str


@dataclass(frozen=True)
class CalibrationMatrixRecord:
    """Aggregate theorem-terrain calibration bucket."""

    bucket: str
    case_count: int
    signatures: tuple[str, ...]
    case_ids: tuple[str, ...]
    terrain_labels: tuple[str, ...]
    expected_routes: tuple[str, ...]
    actual_labels: tuple[str, ...]
    interpretation: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signatures"] = ";".join(self.signatures)
        data["case_ids"] = ";".join(self.case_ids)
        data["terrain_labels"] = ";".join(self.terrain_labels)
        data["expected_routes"] = ";".join(self.expected_routes)
        data["actual_labels"] = ";".join(self.actual_labels)
        return data


BUCKET_INTERPRETATIONS = {
    "correct_artifact_demotion": "Known artifact terrain was demoted instead of promoted.",
    "correct_theorem_terrain_route": "Known solved or descent terrain was routed structurally, not mistaken for a local failure.",
    "correct_external_sage_route": "Modular-method terrain was sent to external Sage/newform follow-up.",
    "route_unknown": "Open or unknown terrain was not promoted.",
    "true_mismatch": "Expected terrain and actual route still disagree.",
    "overpromoted_candidate": "A candidate was promoted without matching validated terrain controls.",
}


def calibration_bucket(record: TerrainCalibrationLike) -> str:
    """Classify one terrain-aware calibration record."""
    system_label = getattr(record, "system_route_label", record.actual_route_label)
    if system_label == "calibrated_route_candidate" and getattr(record, "should_promote_without_external_check", False) is False:
        return "overpromoted_candidate"
    if record.expected_route == "artifact" or record.known_status_label == "subgroup_artifact":
        return "correct_artifact_demotion" if system_label == "artifact_like" else "true_mismatch"
    if record.known_status_label in {"known_solved_terrain", "follows_FLT_style_reduction", "descent_terrain"}:
        return "correct_theorem_terrain_route" if system_label == "theorem_terrain_route" else "true_mismatch"
    if record.expected_route == "modular_method":
        return "correct_external_sage_route" if system_label == "needs_external_sage_check" else "true_mismatch"
    if record.expected_route == "unknown" or record.known_status_label in {"unclassified_terrain", "calibration_only"}:
        return "route_unknown" if system_label in {"not_promising_yet", "theorem_terrain_route"} else "overpromoted_candidate"
    if record.comparison_flag in {"route_mismatch", "underpromotion"}:
        return "true_mismatch"
    if record.comparison_flag == "overpromotion":
        return "overpromoted_candidate"
    return "route_unknown"


def build_calibration_confusion_matrix(records: Iterable[TerrainCalibrationLike]) -> list[CalibrationMatrixRecord]:
    """Build the theorem-terrain-aware route matrix."""
    groups: dict[str, list[TerrainCalibrationLike]] = defaultdict(list)
    for record in records:
        groups[calibration_bucket(record)].append(record)

    rows: list[CalibrationMatrixRecord] = []
    for bucket, items in groups.items():
        terrain_counter = Counter(item.terrain_label for item in items)
        expected_counter = Counter(item.expected_route for item in items)
        actual_counter = Counter(item.actual_route_label for item in items)
        rows.append(
            CalibrationMatrixRecord(
                bucket=bucket,
                case_count=len(items),
                signatures=tuple(sorted({item.signature_text for item in items})),
                case_ids=tuple(sorted(item.case_id for item in items)),
                terrain_labels=tuple(f"{key}:{terrain_counter[key]}" for key in sorted(terrain_counter)),
                expected_routes=tuple(f"{key}:{expected_counter[key]}" for key in sorted(expected_counter)),
                actual_labels=tuple(f"{key}:{actual_counter[key]}" for key in sorted(actual_counter)),
                interpretation=BUCKET_INTERPRETATIONS[bucket],
            )
        )
    rows.sort(
        key=lambda item: (
            item.bucket == "overpromoted_candidate",
            item.bucket == "true_mismatch",
            item.bucket == "correct_theorem_terrain_route",
            item.case_count,
        ),
        reverse=True,
    )
    return rows
