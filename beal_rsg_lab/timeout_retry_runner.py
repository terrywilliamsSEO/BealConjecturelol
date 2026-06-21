"""Retry planning for Sage jobs that timed out."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import ceil
from pathlib import Path
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class TimeoutRetryRecord:
    """One Sage job selected for a longer retry run."""

    job_id: str
    signature: str
    previous_sage_status: str
    route_label: str
    job_path: str
    result_path: str
    previous_timeout_seconds: int
    retry_timeout_seconds: int
    timeout_multiplier: float
    rerun_completed: bool
    retry_reason: str
    command_hint: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def _value(row: Mapping[str, Any], key: str, default: str = "") -> str:
    value = row.get(key, default)
    return "" if value is None else str(value)


def _import_by_job_id(import_rows: Iterable[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {_value(row, "job_id"): row for row in import_rows if _value(row, "job_id")}


def build_timeout_retry_manifest(
    *,
    job_rows: Iterable[Mapping[str, Any]],
    import_rows: Iterable[Mapping[str, Any]],
    base_timeout_seconds: int = 60,
    timeout_multiplier: float = 4.0,
    explicit_timeout_seconds: int | None = None,
    include_completed: bool = False,
) -> list[TimeoutRetryRecord]:
    """Return retry rows for timed-out Sage jobs.

    Completed jobs are intentionally excluded unless `include_completed` is set.
    """
    imports = _import_by_job_id(import_rows)
    retry_timeout = explicit_timeout_seconds or ceil(base_timeout_seconds * timeout_multiplier)
    rows: list[TimeoutRetryRecord] = []
    for job in job_rows:
        job_id = _value(job, "job_id")
        if not job_id:
            continue
        imported = imports.get(job_id, {})
        status = _value(imported, "sage_status", "missing")
        if status != "timeout" and not (include_completed and status == "completed"):
            continue
        signature = _value(job, "signature") or _value(imported, "signature")
        reason = (
            f"Previous Sage execution timed out; retry with {retry_timeout} seconds."
            if status == "timeout"
            else "Completed job explicitly selected for rerun."
        )
        rows.append(
            TimeoutRetryRecord(
                job_id=job_id,
                signature=signature,
                previous_sage_status=status,
                route_label=_value(job, "route_label") or _value(imported, "route_label"),
                job_path=_value(job, "job_path"),
                result_path=_value(job, "result_path"),
                previous_timeout_seconds=base_timeout_seconds,
                retry_timeout_seconds=retry_timeout,
                timeout_multiplier=float(timeout_multiplier),
                rerun_completed=bool(include_completed and status == "completed"),
                retry_reason=reason,
                command_hint=f"sage {_value(job, 'job_path')}",
            )
        )
    rows.sort(key=lambda row: (row.previous_sage_status != "timeout", row.signature))
    return rows


def timeout_retry_summary_rows(rows: Iterable[TimeoutRetryRecord]) -> list[dict[str, object]]:
    """Return compact status counts for the retry manifest."""
    row_list = list(rows)
    by_status: dict[str, int] = {}
    for row in row_list:
        by_status[row.previous_sage_status] = by_status.get(row.previous_sage_status, 0) + 1
    if not row_list:
        return [
            {
                "summary_key": "retry_jobs",
                "summary_value": 0,
                "notes": "No timed-out Sage jobs were selected for retry.",
            }
        ]
    output = [
        {
            "summary_key": "retry_jobs",
            "summary_value": len(row_list),
            "notes": "Only timed-out jobs are selected unless rerun_completed is true.",
        }
    ]
    for status in sorted(by_status):
        output.append(
            {
                "summary_key": f"previous_status_{status}",
                "summary_value": by_status[status],
                "notes": "",
            }
        )
    return output


def timeout_retry_report_markdown(
    *,
    run_dir: Path,
    rows: Iterable[TimeoutRetryRecord],
) -> str:
    """Return Markdown instructions for retrying timed-out Sage jobs."""
    row_list = list(rows)
    lines = [
        "# Timeout Retry Plan",
        "",
        f"Run directory: `{run_dir.as_posix()}`",
        "",
        "This retry plan is execution plumbing only. It does not change route labels, and it does not certify any theorem claim.",
        "",
        f"Timed-out jobs selected: `{len(row_list)}`.",
        "",
    ]
    if not row_list:
        lines.append("No retry is needed because no imported Sage row has `sage_status=timeout`.")
    else:
        lines.extend(
            [
                "| signature | job | previous status | retry timeout | command hint |",
                "| --- | --- | --- | ---: | --- |",
            ]
        )
        for row in row_list:
            lines.append(
                f"| `{row.signature}` | `{row.job_id}` | `{row.previous_sage_status}` | "
                f"{row.retry_timeout_seconds} | `{row.command_hint}` |"
            )
        lines.extend(
            [
                "",
                "After running retries, place JSON outputs in `sage_results/`, then run:",
                "",
                "`python -m beal_rsg_lab.sage_followup_cli import --run-dir " + run_dir.as_posix() + "`",
                "`python -m beal_rsg_lab.sage_followup_cli summarize --run-dir " + run_dir.as_posix() + "`",
            ]
        )
    lines.append("")
    return "\n".join(lines)

