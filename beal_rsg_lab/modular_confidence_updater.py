"""Conservative route-confidence updates from Sage/newform imports."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Protocol


class SageJobConfidenceLike(Protocol):
    job_id: str
    signature: str
    route_label: str
    candidate_case_ids: tuple[str, ...]
    primes_involved: tuple[int, ...]
    candidate_levels: tuple[int, ...]


class SageImportConfidenceLike(Protocol):
    job_id: str
    signature: str
    sage_status: str
    newform_count: int
    checked_levels: tuple[int, ...]
    trace_match_status: str
    contradiction_claim_allowed: bool
    followup_label: str
    schema_valid: bool
    error_message: str


@dataclass(frozen=True)
class ModularConfidenceRecord:
    """Updated modular-route confidence after optional Sage import."""

    job_id: str
    signature: str
    previous_route_label: str
    sage_status: str
    trace_match_status: str
    newform_count: int
    checked_levels: tuple[int, ...]
    updated_followup_label: str
    route_confidence_score: float
    human_review_priority: float
    contradiction_claim_allowed: bool
    rationale: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["checked_levels"] = ";".join(str(level) for level in self.checked_levels)
        return data


def _updated_label(import_record: SageImportConfidenceLike) -> str:
    if import_record.sage_status == "unavailable":
        return "needs_external_sage_check"
    if import_record.sage_status in {"partial", "failed"}:
        return "needs_external_sage_check"
    if import_record.trace_match_status in {"rigid", "narrow", "candidate_match"}:
        return "modular_followup_candidate"
    if import_record.trace_match_status in {"artifact_like"}:
        return "artifact_like"
    if import_record.trace_match_status in {"control_like"}:
        return "not_promising_yet"
    return "sage_checked_inconclusive"


def _confidence_score(import_record: SageImportConfidenceLike) -> float:
    if import_record.sage_status == "unavailable":
        return 1.5
    if import_record.sage_status == "failed":
        return 1.0
    if import_record.sage_status == "partial":
        return 2.0
    if import_record.trace_match_status in {"rigid", "candidate_match"}:
        return 6.5
    if import_record.trace_match_status == "narrow":
        return 5.5
    if import_record.trace_match_status == "inconclusive":
        return 3.5
    if import_record.trace_match_status in {"control_like", "artifact_like"}:
        return 0.5
    return 2.5


def _rationale(label: str, import_record: SageImportConfidenceLike) -> str:
    if import_record.sage_status == "unavailable":
        return "SageMath was unavailable, so the signature remains queued for external Sage/newform review."
    if import_record.sage_status == "failed":
        return "Sage JSON import failed or the job reported failure; keep the route as an external-check item."
    if import_record.sage_status == "partial":
        return "Sage output is missing or incomplete; keep the route as an external-check item."
    if label == "modular_followup_candidate":
        return "Sage trace/newform data looked narrow enough to justify human modular-method review, without any proof claim."
    if label == "artifact_like":
        return "Sage output matched artifact-like behavior, so the route is demoted."
    if label == "not_promising_yet":
        return "Sage output was control-like, so the route is not prioritized."
    return "Sage completed but did not produce decisive route evidence."


def update_modular_confidence(
    jobs: Iterable[SageJobConfidenceLike],
    imports: Iterable[SageImportConfidenceLike],
) -> list[ModularConfidenceRecord]:
    """Update route labels conservatively from imported Sage rows."""
    job_by_id = {job.job_id: job for job in jobs}
    rows: list[ModularConfidenceRecord] = []
    for import_record in imports:
        job = job_by_id.get(import_record.job_id)
        previous = job.route_label if job is not None else import_record.followup_label
        label = _updated_label(import_record)
        score = _confidence_score(import_record)
        if previous in {"trace_rigid_candidate", "newform_check_candidate"}:
            score += 0.75
        if import_record.newform_count and import_record.newform_count <= 2:
            score += 0.25
        priority = score
        if label == "modular_followup_candidate":
            priority += 1.5
        elif label == "needs_external_sage_check":
            priority += 0.5
        rows.append(
            ModularConfidenceRecord(
                job_id=import_record.job_id,
                signature=import_record.signature,
                previous_route_label=previous,
                sage_status=import_record.sage_status,
                trace_match_status=import_record.trace_match_status,
                newform_count=import_record.newform_count,
                checked_levels=import_record.checked_levels,
                updated_followup_label=label,
                route_confidence_score=round(score, 10),
                human_review_priority=round(priority, 10),
                contradiction_claim_allowed=False,
                rationale=_rationale(label, import_record),
            )
        )
    rows.sort(key=lambda row: (row.human_review_priority, row.route_confidence_score, row.signature), reverse=True)
    return rows


def sage_followup_report_markdown(
    *,
    output_dir: object,
    jobs: list[SageJobConfidenceLike],
    imports: list[SageImportConfidenceLike],
    confidence_rows: list[ModularConfidenceRecord],
    known_case_rows: list[object],
) -> str:
    """Return the Markdown Sage follow-up report."""
    status_counts: dict[str, int] = {}
    label_counts: dict[str, int] = {}
    for row in imports:
        status_counts[row.sage_status] = status_counts.get(row.sage_status, 0) + 1
    for row in confidence_rows:
        label_counts[row.updated_followup_label] = label_counts.get(row.updated_followup_label, 0) + 1
    overpromoted = sum(1 for row in known_case_rows if getattr(row, "overpromoted", False))
    lines = [
        "# Sage/Newform Follow-Up Report",
        "",
        f"Output directory: `{output_dir}`",
        "",
        "## Guardrail",
        "",
        "This pipeline exports Sage jobs, imports machine-readable Sage JSON, and updates route confidence. It does not certify theorem claims for Beal or any generalized Fermat case.",
        "",
        "Every imported row sets `contradiction_claim_allowed` to `False`. The strongest allowed label is `modular_followup_candidate`, meaning worth human modular-method review.",
        "",
        "## Counts",
        "",
        f"- Sage jobs generated: `{len(jobs)}`.",
        f"- Sage import rows: `{len(imports)}`.",
        f"- Known-case Sage calibration rows: `{len(known_case_rows)}`.",
        f"- Known-case overpromotion rows: `{overpromoted}`.",
    ]
    for status in sorted(status_counts):
        lines.append(f"- Sage status `{status}`: `{status_counts[status]}`.")
    for label in sorted(label_counts):
        lines.append(f"- Updated label `{label}`: `{label_counts[label]}`.")
    if status_counts.get("unavailable"):
        lines.extend(
            [
                "",
                "SageMath was not available on this machine, so jobs were generated and imports were marked `unavailable` until the scripts are run externally.",
            ]
        )
    lines.extend(
        [
            "",
            "## Human Review Queue",
            "",
        ]
    )
    if not confidence_rows:
        lines.append("No Sage follow-up jobs were generated.")
    else:
        lines.extend(
            [
                "| rank | signature | previous label | Sage status | trace status | updated label | priority |",
                "| ---: | --- | --- | --- | --- | --- | ---: |",
            ]
        )
        for index, row in enumerate(confidence_rows[:16], start=1):
            lines.append(
                f"| {index} | `{row.signature}` | `{row.previous_route_label}` | `{row.sage_status}` | "
                f"`{row.trace_match_status}` | `{row.updated_followup_label}` | {row.human_review_priority} |"
            )
    lines.extend(
        [
            "",
            "## Files",
            "",
            "- `sage_job_manifest.csv`: generated Sage jobs and metadata.",
            "- `sage_import_results.csv`: validated Sage JSON imports or skip rows.",
            "- `sage_known_case_calibration.csv`: known-case safety check after Sage import.",
            "- `modular_confidence_summary.csv`: conservative confidence updates.",
            "- `sage_jobs/`: per-signature `.sage` jobs and batch runner.",
            "- `sage_results/`: expected JSON output directory.",
            "",
            "## Next Work",
            "",
            "Run the generated Sage jobs with `scripts/run_sage_jobs.sh` or `scripts/run_sage_jobs.ps1`, then rerun the experiment or importer to refresh the JSON-backed confidence rows.",
            "",
        ]
    )
    return "\n".join(lines)
