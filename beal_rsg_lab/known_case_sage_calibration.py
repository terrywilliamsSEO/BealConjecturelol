"""Known-case safety checks after Sage/newform result import."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Protocol


class KnownCaseSageInput(Protocol):
    case_id: str
    signature_text: str
    expected_route: str
    actual_route_label: str
    known_status_label: str
    collision_class: str


class SageJobCaseLike(Protocol):
    job_id: str
    signature: str
    candidate_case_ids: tuple[str, ...]


class SageImportCaseLike(Protocol):
    job_id: str
    sage_status: str
    trace_match_status: str


class ConfidenceCaseLike(Protocol):
    job_id: str
    signature: str
    updated_followup_label: str
    human_review_priority: float


@dataclass(frozen=True)
class KnownCaseSageCalibrationRecord:
    """Known-case calibration row after optional Sage import."""

    case_id: str
    signature: str
    expected_route: str
    pre_sage_label: str
    post_sage_label: str
    sage_status: str
    trace_match_status: str
    artifact_like_preserved: bool
    overpromoted: bool
    calibration_status: str
    rationale: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def _job_by_case(jobs: Iterable[SageJobCaseLike]) -> dict[str, SageJobCaseLike]:
    by_case: dict[str, SageJobCaseLike] = {}
    for job in jobs:
        for case_id in job.candidate_case_ids:
            by_case[case_id] = job
    return by_case


def _status_for_case(
    record: KnownCaseSageInput,
    post_label: str,
    sage_status: str,
) -> tuple[str, str]:
    if record.actual_route_label == "artifact_like":
        if post_label == "artifact_like":
            return "known_case_sage_ok", "Artifact calibrator remained demoted after Sage import."
        return "known_case_sage_overpromotion_risk", "Artifact calibrator did not remain demoted."
    if post_label in {"calibrated_route_candidate", "proof", "disproof"}:
        return "known_case_sage_overpromotion_risk", "Post-Sage label exceeds the permitted follow-up ceiling."
    if sage_status in {"unavailable", "partial"}:
        return "known_case_sage_pending", "Sage evidence is absent or incomplete, so the conservative route is unchanged."
    return "known_case_sage_ok", "Sage import did not overpromote this calibration case."


def calibrate_known_cases_with_sage(
    known_cases: Iterable[KnownCaseSageInput],
    jobs: Iterable[SageJobCaseLike],
    imports: Iterable[SageImportCaseLike],
    confidence_rows: Iterable[ConfidenceCaseLike],
) -> list[KnownCaseSageCalibrationRecord]:
    """Check known cases remain calibrated after Sage result import."""
    jobs_by_case = _job_by_case(jobs)
    imports_by_job = {row.job_id: row for row in imports}
    confidence_by_job = {row.job_id: row for row in confidence_rows}
    rows: list[KnownCaseSageCalibrationRecord] = []

    for record in known_cases:
        job = jobs_by_case.get(record.case_id)
        import_row = imports_by_job.get(job.job_id) if job is not None else None
        confidence = confidence_by_job.get(job.job_id) if job is not None else None
        if job is None:
            post_label = record.actual_route_label
            sage_status = "not_requested"
            trace_status = "not_checked"
        else:
            post_label = confidence.updated_followup_label if confidence is not None else record.actual_route_label
            sage_status = import_row.sage_status if import_row is not None else "partial"
            trace_status = import_row.trace_match_status if import_row is not None else "not_checked"
        artifact_preserved = record.actual_route_label != "artifact_like" or post_label == "artifact_like"
        status, rationale = _status_for_case(record, post_label, sage_status)
        overpromoted = status == "known_case_sage_overpromotion_risk"
        rows.append(
            KnownCaseSageCalibrationRecord(
                case_id=record.case_id,
                signature=record.signature_text,
                expected_route=record.expected_route,
                pre_sage_label=record.actual_route_label,
                post_sage_label=post_label,
                sage_status=sage_status,
                trace_match_status=trace_status,
                artifact_like_preserved=artifact_preserved,
                overpromoted=overpromoted,
                calibration_status=status,
                rationale=rationale,
            )
        )
    rows.sort(key=lambda row: (row.overpromoted, row.sage_status == "completed", row.signature), reverse=True)
    return rows
