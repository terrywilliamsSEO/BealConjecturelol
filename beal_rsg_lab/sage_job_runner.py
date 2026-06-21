"""Timeout-aware execution for generated Sage jobs."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import subprocess
from types import SimpleNamespace
from typing import Iterable, Mapping, Protocol

from .sage_docker_runner import sage_docker_image
from .sage_environment_detector import SageEnvironmentReport, detect_sage_environment
from .sage_level_220_newform_expander import prepare_level_220_newform_expander_job
from .sage_smoke import SMOKE_JOB_ID, write_sage_smoke_job


class SageRunJobLike(Protocol):
    job_id: str
    signature: str
    route_label: str
    job_path: str
    result_path: str


@dataclass(frozen=True)
class SageExecutionRecord:
    """Execution result for one Sage job or smoke job."""

    job_id: str
    signature: str
    execution_mode: str
    command: str
    result_path: str
    sage_status: str
    return_code: int
    timed_out: bool
    stdout_excerpt: str
    stderr_excerpt: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def _parse_signature(signature: str) -> list[int]:
    try:
        parts = [int(part) for part in signature.split("-")]
    except ValueError:
        return [0, 0, 0]
    return parts if len(parts) == 3 else [0, 0, 0]


def _write_status_json(
    *,
    job_id: str,
    signature: str,
    route_label: str,
    result_path: Path,
    sage_status: str,
    message: str,
    command: list[str],
) -> None:
    result_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "job_id": job_id,
        "signature": _parse_signature(signature),
        "route_label": route_label,
        "source_run": "sage_job_runner",
        "sage_status": sage_status,
        "checked_levels": [],
        "newform_count": 0,
        "trace_match_status": "not_checked",
        "contradiction_claim_allowed": False,
        "followup_label": "needs_external_sage_check",
        "errors": [message],
        "execution": {
            "command": " ".join(command),
        },
    }
    result_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _has_valid_json(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return False
    return True


def _relative_to_repo(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _job_command(
    *,
    mode: str,
    job_path: Path,
    repo_root: Path,
    docker_image: str,
) -> list[str]:
    if mode == "native_sage":
        return ["sage", job_path.as_posix()]
    if mode == "wsl_sage":
        return ["wsl", "sage", job_path.as_posix()]
    if mode == "docker":
        return [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{repo_root.resolve().as_posix()}:/work",
            "-w",
            "/work",
            docker_image,
            "sage",
            _relative_to_repo(job_path, repo_root),
        ]
    raise ValueError(f"unsupported Sage execution mode {mode!r}")


def _run_command(
    command: list[str],
    *,
    timeout_seconds: int,
) -> tuple[str, int, bool, str, str]:
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        status = "completed" if completed.returncode == 0 else "failed"
        return status, completed.returncode, False, completed.stdout[-1000:], completed.stderr[-1000:]
    except subprocess.TimeoutExpired as exc:
        stdout = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
        stderr = (exc.stderr or "") if isinstance(exc.stderr, str) else ""
        return "timeout", 124, True, stdout[-1000:], stderr[-1000:]
    except Exception as exc:  # pragma: no cover - depends on local executables
        return "failed", 127, False, "", str(exc)


def _record_for_unavailable(job: SageRunJobLike, mode: str) -> SageExecutionRecord:
    result_path = Path(job.result_path)
    command = ["unavailable"]
    _write_status_json(
        job_id=job.job_id,
        signature=job.signature,
        route_label=job.route_label,
        result_path=result_path,
        sage_status="unavailable",
        message="No Sage execution backend is available.",
        command=command,
    )
    return SageExecutionRecord(
        job_id=job.job_id,
        signature=job.signature,
        execution_mode=mode,
        command=" ".join(command),
        result_path=result_path.as_posix(),
        sage_status="unavailable",
        return_code=127,
        timed_out=False,
        stdout_excerpt="",
        stderr_excerpt="No Sage execution backend is available.",
    )


def run_one_sage_job(
    job: SageRunJobLike,
    *,
    mode: str,
    repo_root: Path,
    timeout_seconds: int,
    docker_image: str | None = None,
) -> SageExecutionRecord:
    """Run one Sage job and write timeout/failure JSON if needed."""
    if mode not in {"native_sage", "wsl_sage", "docker"}:
        return _record_for_unavailable(job, mode)
    job_path = Path(job.job_path)
    result_path = Path(job.result_path)
    command = _job_command(
        mode=mode,
        job_path=job_path,
        repo_root=repo_root,
        docker_image=docker_image or sage_docker_image(),
    )
    status, return_code, timed_out, stdout, stderr = _run_command(command, timeout_seconds=timeout_seconds)
    if not _has_valid_json(result_path):
        fallback_status = status if status in {"timeout", "failed"} else "failed"
        if status == "completed":
            status = "failed"
            return_code = return_code or 1
        _write_status_json(
            job_id=job.job_id,
            signature=job.signature,
            route_label=job.route_label,
            result_path=result_path,
            sage_status=fallback_status,
            message=(
                f"Sage job timed out after {timeout_seconds} seconds."
                if timed_out
                else stderr or stdout or "Sage job did not write valid JSON."
            ),
            command=command,
        )
    return SageExecutionRecord(
        job_id=job.job_id,
        signature=job.signature,
        execution_mode=mode,
        command=" ".join(command),
        result_path=result_path.as_posix(),
        sage_status=status,
        return_code=return_code,
        timed_out=timed_out,
        stdout_excerpt=stdout,
        stderr_excerpt=stderr,
    )


def _smoke_job_like(run_dir: Path) -> SageRunJobLike:
    job_path, result_path = write_sage_smoke_job(run_dir)
    return SimpleNamespace(
        job_id=SMOKE_JOB_ID,
        signature="0-0-0",
        route_label="smoke_check",
        job_path=job_path.as_posix(),
        result_path=result_path.as_posix(),
    )


def run_sage_jobs(
    *,
    run_dir: Path,
    jobs: Iterable[SageRunJobLike],
    repo_root: Path,
    environment: SageEnvironmentReport | None = None,
    backend: str = "auto",
    timeout_seconds: int = 600,
    include_smoke: bool = True,
    include_level_220_expander: bool = True,
) -> list[SageExecutionRecord]:
    """Run smoke and generated Sage jobs through the selected backend."""
    env = environment or detect_sage_environment()
    mode = env.execution_mode if backend == "auto" else backend
    rows: list[SageExecutionRecord] = []
    if include_smoke:
        rows.append(
            run_one_sage_job(
                _smoke_job_like(run_dir),
                mode=mode,
                repo_root=repo_root,
                timeout_seconds=timeout_seconds,
            )
        )
        if rows[-1].sage_status in {"failed", "timeout", "unavailable"}:
            return rows
    if include_level_220_expander:
        rows.append(
            run_one_sage_job(
                prepare_level_220_newform_expander_job(run_dir),
                mode=mode,
                repo_root=repo_root,
                timeout_seconds=timeout_seconds,
            )
        )
    for job in jobs:
        rows.append(
            run_one_sage_job(
                job,
                mode=mode,
                repo_root=repo_root,
                timeout_seconds=timeout_seconds,
            )
        )
    return rows
