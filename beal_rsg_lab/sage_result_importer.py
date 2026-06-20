"""Import JSON outputs from Sage/newform follow-up jobs."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any, Iterable, Protocol


VALID_SAGE_STATUSES = {"unavailable", "completed", "failed", "partial", "timeout"}
VALID_TRACE_STATUSES = {
    "not_checked",
    "inconclusive",
    "rigid",
    "narrow",
    "control_like",
    "artifact_like",
    "candidate_match",
}


class SageJobLike(Protocol):
    job_id: str
    signature: str
    route_label: str
    result_path: str
    sage_available: bool


@dataclass(frozen=True)
class SageImportRecord:
    """Validated import row for one Sage JSON result."""

    job_id: str
    signature: str
    route_label: str
    sage_status: str
    newform_count: int
    checked_levels: tuple[int, ...]
    trace_match_status: str
    contradiction_claim_allowed: bool
    followup_label: str
    result_path: str
    schema_valid: bool
    error_message: str
    raw_summary: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["checked_levels"] = ";".join(str(level) for level in self.checked_levels)
        return data


def _coerce_signature(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, (list, tuple)) and len(value) == 3:
        return "-".join(str(int(part)) for part in value)
    return ""


def _coerce_levels(value: Any) -> tuple[int, ...]:
    if not isinstance(value, list):
        return ()
    levels: list[int] = []
    for item in value:
        try:
            levels.append(int(item))
        except (TypeError, ValueError):
            continue
    return tuple(levels)


def validate_sage_result(payload: Any) -> tuple[bool, str]:
    """Validate the expected Sage JSON schema."""
    if not isinstance(payload, dict):
        return False, "payload is not a JSON object"
    required = {
        "job_id",
        "signature",
        "sage_status",
        "checked_levels",
        "newform_count",
        "trace_match_status",
        "contradiction_claim_allowed",
    }
    missing = sorted(required - set(payload))
    if missing:
        return False, "missing keys: " + ",".join(missing)
    if payload["sage_status"] not in VALID_SAGE_STATUSES:
        return False, f"invalid sage_status {payload['sage_status']!r}"
    if payload["trace_match_status"] not in VALID_TRACE_STATUSES:
        return False, f"invalid trace_match_status {payload['trace_match_status']!r}"
    if bool(payload["contradiction_claim_allowed"]):
        return False, "contradiction_claim_allowed must be false"
    try:
        int(payload["newform_count"])
    except (TypeError, ValueError):
        return False, "newform_count is not an integer"
    if not isinstance(payload["checked_levels"], list):
        return False, "checked_levels is not a list"
    if not _coerce_signature(payload["signature"]):
        return False, "signature is malformed"
    return True, ""


def _followup_label(sage_status: str, trace_match_status: str) -> str:
    if sage_status in {"unavailable", "partial", "failed", "timeout"}:
        return "needs_external_sage_check"
    if trace_match_status in {"rigid", "narrow", "candidate_match"}:
        return "modular_followup_candidate"
    if trace_match_status == "artifact_like":
        return "artifact_like"
    if trace_match_status == "control_like":
        return "not_promising_yet"
    return "sage_checked_inconclusive"


def _raw_summary(payload: dict[str, Any]) -> str:
    summary = {
        "sage_status": payload.get("sage_status", ""),
        "newform_count": payload.get("newform_count", 0),
        "checked_levels": payload.get("checked_levels", []),
        "trace_match_status": payload.get("trace_match_status", ""),
        "errors": payload.get("errors", [])[:3] if isinstance(payload.get("errors", []), list) else [],
    }
    return json.dumps(summary, sort_keys=True)


def _missing_record(job: SageJobLike, *, status: str, message: str) -> SageImportRecord:
    return SageImportRecord(
        job_id=job.job_id,
        signature=job.signature,
        route_label=job.route_label,
        sage_status=status,
        newform_count=0,
        checked_levels=(),
        trace_match_status="not_checked",
        contradiction_claim_allowed=False,
        followup_label="needs_external_sage_check",
        result_path=job.result_path,
        schema_valid=True,
        error_message=message,
        raw_summary=json.dumps({"message": message, "sage_status": status}, sort_keys=True),
    )


def import_sage_results(
    jobs: Iterable[SageJobLike],
    *,
    results_dir: Path | None = None,
) -> list[SageImportRecord]:
    """Read Sage JSON outputs and attach them to generated jobs."""
    rows: list[SageImportRecord] = []
    for job in jobs:
        result_path = Path(job.result_path)
        if results_dir is not None:
            result_path = results_dir / f"{job.job_id}.json"
        if not result_path.exists():
            status = "partial" if job.sage_available else "unavailable"
            message = "Sage result JSON not found; Sage job has not been run."
            if not job.sage_available:
                message = "SageMath executable was not found; job was skipped."
            rows.append(_missing_record(job, status=status, message=message))
            continue
        try:
            payload = json.loads(result_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            rows.append(
                SageImportRecord(
                    job_id=job.job_id,
                    signature=job.signature,
                    route_label=job.route_label,
                    sage_status="failed",
                    newform_count=0,
                    checked_levels=(),
                    trace_match_status="not_checked",
                    contradiction_claim_allowed=False,
                    followup_label="needs_external_sage_check",
                    result_path=result_path.as_posix(),
                    schema_valid=False,
                    error_message=f"invalid JSON: {exc}",
                    raw_summary="{}",
                )
            )
            continue
        valid, error = validate_sage_result(payload)
        if not valid:
            rows.append(
                SageImportRecord(
                    job_id=job.job_id,
                    signature=job.signature,
                    route_label=job.route_label,
                    sage_status="failed",
                    newform_count=0,
                    checked_levels=(),
                    trace_match_status="not_checked",
                    contradiction_claim_allowed=False,
                    followup_label="needs_external_sage_check",
                    result_path=result_path.as_posix(),
                    schema_valid=False,
                    error_message=error,
                    raw_summary=_raw_summary(payload) if isinstance(payload, dict) else "{}",
                )
            )
            continue
        sage_status = str(payload["sage_status"])
        trace_status = str(payload["trace_match_status"])
        rows.append(
            SageImportRecord(
                job_id=str(payload["job_id"]),
                signature=_coerce_signature(payload["signature"]),
                route_label=str(payload.get("route_label", job.route_label)),
                sage_status=sage_status,
                newform_count=int(payload["newform_count"]),
                checked_levels=_coerce_levels(payload["checked_levels"]),
                trace_match_status=trace_status,
                contradiction_claim_allowed=False,
                followup_label=str(payload.get("followup_label") or _followup_label(sage_status, trace_status)),
                result_path=result_path.as_posix(),
                schema_valid=True,
                error_message="",
                raw_summary=_raw_summary(payload),
            )
        )
    rows.sort(
        key=lambda row: (
            row.followup_label == "modular_followup_candidate",
            row.sage_status == "completed",
            row.signature,
        ),
        reverse=True,
    )
    return rows
