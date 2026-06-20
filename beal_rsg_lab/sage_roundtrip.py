"""Report helpers for Sage execution and import roundtrips."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping

from .sage_docker_runner import docker_batch_command, docker_command_text, sage_docker_image
from .sage_environment_detector import SageEnvironmentReport


def _value(row: Mapping[str, Any], key: str, default: str = "") -> str:
    value = row.get(key, default)
    return "" if value is None else str(value)


def sage_execution_manifest_rows(
    *,
    job_rows: Iterable[Mapping[str, Any]],
    environment: SageEnvironmentReport,
    repo_root: Path,
    run_dir: Path,
) -> list[dict[str, object]]:
    """Return rows describing how each generated Sage job can be executed."""
    docker_command = docker_command_text(
        docker_batch_command(
            repo_root=repo_root,
            run_dir=run_dir,
            image=sage_docker_image(),
        )
    )
    rows: list[dict[str, object]] = []
    for row in job_rows:
        job_path = _value(row, "job_path")
        if environment.execution_mode == "native_sage":
            command = f"sage {job_path}"
        elif environment.execution_mode == "wsl_sage":
            command = f"wsl sage {job_path}"
        elif environment.execution_mode == "docker":
            command = docker_command
        elif environment.execution_mode == "ci":
            command = "Use .github/workflows/sage-followup.yml"
        else:
            command = "Install SageMath, enable WSL Sage, or run Docker/CI Sage follow-up."
        rows.append(
            {
                "job_id": _value(row, "job_id"),
                "signature": _value(row, "signature"),
                "execution_mode": environment.execution_mode,
                "detected_version": environment.detected_version,
                "command": command,
                "docker_image": sage_docker_image(),
                "job_path": job_path,
                "result_path": _value(row, "result_path"),
                "ready_to_run": environment.execution_mode != "unavailable",
            }
        )
    return rows


def sage_roundtrip_summary_rows(
    *,
    job_rows: Iterable[Mapping[str, Any]],
    import_rows: Iterable[Mapping[str, Any]],
    confidence_rows: Iterable[Mapping[str, Any]],
    known_case_sage_rows: Iterable[Mapping[str, Any]],
) -> list[dict[str, object]]:
    """Return one row per Sage job summarizing import and calibration status."""
    imports = {_value(row, "job_id"): row for row in import_rows}
    confidence = {_value(row, "job_id"): row for row in confidence_rows}
    overpromotion_by_signature = {
        _value(row, "signature"): _value(row, "overpromoted", "False")
        for row in known_case_sage_rows
    }
    rows: list[dict[str, object]] = []
    for job in job_rows:
        job_id = _value(job, "job_id")
        signature = _value(job, "signature")
        imported = imports.get(job_id, {})
        confidence_row = confidence.get(job_id, {})
        route_label = _value(confidence_row, "updated_followup_label", _value(job, "route_label"))
        review_label = "worth_human_modular_review" if route_label == "modular_followup_candidate" else route_label
        rows.append(
            {
                "job_id": job_id,
                "signature": signature,
                "source_route_label": _value(job, "route_label"),
                "sage_status": _value(imported, "sage_status", "not_imported"),
                "trace_match_status": _value(imported, "trace_match_status", "not_checked"),
                "newform_count": _value(imported, "newform_count", "0"),
                "updated_followup_label": route_label,
                "review_label": review_label,
                "contradiction_claim_allowed": "False",
                "known_case_overpromoted": overpromotion_by_signature.get(signature, "False"),
                "human_review_priority": _value(confidence_row, "human_review_priority", "0"),
            }
        )
    return rows
