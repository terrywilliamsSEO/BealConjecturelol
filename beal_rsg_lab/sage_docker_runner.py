"""Docker command helpers for running generated Sage jobs."""

from __future__ import annotations

import os
from pathlib import Path


DEFAULT_SAGE_DOCKER_IMAGE = "sagemath/sagemath:latest"


def sage_docker_image(environ: dict[str, str] | None = None) -> str:
    """Return the configured Sage Docker image."""
    env = environ if environ is not None else os.environ
    return env.get("SAGE_DOCKER_IMAGE", DEFAULT_SAGE_DOCKER_IMAGE)


def docker_batch_command(
    *,
    repo_root: Path,
    run_dir: Path,
    image: str | None = None,
) -> list[str]:
    """Return a Docker command that runs the generated Sage batch file."""
    resolved_root = repo_root.resolve()
    resolved_run = run_dir.resolve()
    try:
        relative_run = resolved_run.relative_to(resolved_root)
    except ValueError:
        relative_run = Path("runs") / resolved_run.name
    batch_path = relative_run / "sage_jobs" / "run_all_sage_jobs.sage"
    return [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{resolved_root.as_posix()}:/work",
        "-w",
        "/work",
        image or sage_docker_image(),
        "sage",
        batch_path.as_posix(),
    ]


def docker_command_text(command: list[str]) -> str:
    """Return a shell-friendly display string for a Docker command."""
    return " ".join(command)
