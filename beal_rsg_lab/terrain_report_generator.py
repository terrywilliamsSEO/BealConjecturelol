"""Report helpers for theorem-terrain calibration outputs."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Protocol

from .calibration_confusion_matrix import CalibrationMatrixRecord
from .theorem_terrain_classifier import TheoremTerrainRecord


class TerrainCalibrationRecordLike(Protocol):
    case_id: str
    signature_text: str
    family_label: str
    expected_route: str
    terrain_label: str
    known_status_label: str
    theorem_route_label: str
    actual_route_label: str
    comparison_flag: str
    strongest_system_signal: str


@dataclass(frozen=True)
class TerrainSummaryRecord:
    """Joined terrain and calibration route summary."""

    case_id: str
    signature: str
    family_label: str
    terrain_label: str
    structural_terrain_labels: str
    known_status_label: str
    expected_route: str
    theorem_route_label: str
    actual_route_label: str
    comparison_flag: str
    strongest_system_signal: str
    should_promote_without_external_check: bool
    rationale: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def theorem_terrain_summary_rows(
    calibration_records: Iterable[TerrainCalibrationRecordLike],
    terrain_records: Iterable[TheoremTerrainRecord],
) -> list[dict[str, object]]:
    """Join terrain records to known-case calibration rows."""
    terrain_by_signature = {
        "-".join(str(part) for part in terrain.signature): terrain
        for terrain in terrain_records
    }
    rows: list[TerrainSummaryRecord] = []
    for record in calibration_records:
        terrain = terrain_by_signature[record.signature_text]
        rows.append(
            TerrainSummaryRecord(
                case_id=record.case_id,
                signature=record.signature_text,
                family_label=record.family_label,
                terrain_label=terrain.terrain_label,
                structural_terrain_labels=";".join(terrain.structural_terrain_labels),
                known_status_label=terrain.known_status_label,
                expected_route=terrain.expected_route,
                theorem_route_label=record.theorem_route_label,
                actual_route_label=record.actual_route_label,
                comparison_flag=record.comparison_flag,
                strongest_system_signal=record.strongest_system_signal,
                should_promote_without_external_check=terrain.should_promote_without_external_check,
                rationale=terrain.rationale,
            )
        )
    rows.sort(key=lambda item: (item.actual_route_label, item.signature))
    return [row.to_flat_dict() for row in rows]


def remaining_true_mismatch_rows(
    calibration_records: Iterable[TerrainCalibrationRecordLike],
    matrix_records: Iterable[CalibrationMatrixRecord],
) -> list[dict[str, object]]:
    """Return rows in true mismatch or overpromotion buckets."""
    mismatch_case_ids: set[str] = set()
    for matrix in matrix_records:
        if matrix.bucket in {"true_mismatch", "overpromoted_candidate"}:
            mismatch_case_ids.update(matrix.case_ids)
    rows: list[dict[str, object]] = []
    for record in calibration_records:
        if record.case_id not in mismatch_case_ids:
            continue
        rows.append(
            {
                "case_id": record.case_id,
                "signature": record.signature_text,
                "terrain_label": record.terrain_label,
                "known_status_label": record.known_status_label,
                "expected_route": record.expected_route,
                "actual_route_label": record.actual_route_label,
                "comparison_flag": record.comparison_flag,
                "strongest_system_signal": record.strongest_system_signal,
            }
        )
    return rows


def theorem_terrain_report_markdown(
    *,
    output_dir: Path,
    terrain_rows: list[dict[str, object]],
    matrix_rows: list[dict[str, object]],
    mismatch_rows: list[dict[str, object]],
) -> str:
    """Generate the theorem-terrain report."""
    generated = datetime.now().isoformat(timespec="seconds")
    label_counts: dict[str, int] = {}
    for row in terrain_rows:
        label = str(row["actual_route_label"])
        label_counts[label] = label_counts.get(label, 0) + 1
    lines = [
        "# Theorem-Terrain Calibration Report",
        "",
        f"Generated: `{generated}`",
        f"Output directory: `{output_dir.as_posix()}`",
        "",
        "## Interpretation Guardrail",
        "",
        "This report routes signatures to known theorem terrain. It does not prove any new generalized Fermat or Beal case.",
        "",
        "Known solved terrain calibrates the router. It should not be treated as a new proof claim or as local evidence.",
        "",
        "## Counts",
        "",
        f"- Terrain rows: `{len(terrain_rows)}`.",
        f"- Remaining true mismatches: `{len(mismatch_rows)}`.",
    ]
    for label in sorted(label_counts):
        lines.append(f"- `{label}`: `{label_counts[label]}`.")

    lines.extend(
        [
            "",
            "## Known Case Route Matrix",
            "",
            "| bucket | cases | interpretation |",
            "| --- | ---: | --- |",
        ]
    )
    for row in matrix_rows:
        lines.append(f"| {row['bucket']} | {row['case_count']} | {row['interpretation']} |")

    lines.extend(
        [
            "",
            "## Remaining True Mismatches",
            "",
        ]
    )
    if not mismatch_rows:
        lines.append("No true mismatches remain after theorem-terrain routing.")
    else:
        lines.extend(
            [
                "| case | signature | terrain | expected | actual | signal |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in mismatch_rows[:12]:
            lines.append(
                f"| {row['case_id']} | {row['signature']} | {row['terrain_label']} | "
                f"{row['expected_route']} | {row['actual_route_label']} | {row['strongest_system_signal']} |"
            )

    lines.extend(
        [
            "",
            "## Files",
            "",
            "- `theorem_terrain_summary.csv`: structural theorem-terrain route rows.",
            "- `known_case_route_matrix.csv`: theorem-terrain-aware calibration buckets.",
            "- `remaining_true_mismatches.csv`: cases still failing route calibration.",
            "",
            "## Promotion Rule",
            "",
            "A research route candidate still needs artifact controls plus terrain calibration. Local sparsity alone is not enough.",
            "",
        ]
    )
    return "\n".join(lines)
