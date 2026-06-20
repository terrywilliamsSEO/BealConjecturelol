"""Detect Sage execution support across native, WSL, Docker, and CI modes."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import shutil
import subprocess
from typing import Callable, Mapping


CommandRunner = Callable[[list[str]], tuple[int, str, str]]
WhichFunc = Callable[[str], str | None]


@dataclass(frozen=True)
class SageEnvironmentReport:
    """Machine-readable Sage execution environment report."""

    execution_mode: str
    detected_version: str
    commands_tested: tuple[str, ...]
    failure_reason: str
    native_sage: bool
    wsl_sage: bool
    docker_available: bool
    ci_mode: bool
    wsl_command_attempted: str = ""
    wsl_timeout_seconds: int = 5
    wsl_launched: bool = False
    wsl_sage_binary_found: bool = False
    wsl_recommended_command: str = "wsl sh -lc 'command -v sage && sage --version'"

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["commands_tested"] = list(self.commands_tested)
        return data


def _default_runner(command: list[str]) -> tuple[int, str, str]:
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except Exception as exc:  # pragma: no cover - depends on local environment
        return 127, "", str(exc)
    return completed.returncode, completed.stdout.strip(), completed.stderr.strip()


def _command_text(command: list[str]) -> str:
    return " ".join(command)


def _version_from_output(stdout: str, stderr: str) -> str:
    text = (stdout or stderr).strip()
    return text.splitlines()[0] if text else ""


def detect_sage_environment(
    *,
    runner: CommandRunner | None = None,
    which: WhichFunc | None = None,
    environ: Mapping[str, str] | None = None,
) -> SageEnvironmentReport:
    """Detect the best available Sage execution mode."""
    run = runner or _default_runner
    which_func = which or shutil.which
    env = environ if environ is not None else os.environ
    commands: list[str] = []
    failures: list[str] = []
    timeout_seconds = 5

    ci_mode = bool(env.get("GITHUB_ACTIONS") or env.get("CI"))

    native_sage = False
    native_version = ""
    sage_path = which_func("sage")
    if sage_path:
        command = [sage_path, "--version"]
        commands.append(_command_text(command))
        code, stdout, stderr = run(command)
        if code == 0:
            native_sage = True
            native_version = _version_from_output(stdout, stderr)
        else:
            failures.append(f"native sage failed: {stderr or stdout or code}")
    else:
        failures.append("native sage not found on PATH")

    wsl_sage = False
    wsl_version = ""
    wsl_launched = False
    wsl_sage_binary_found = False
    wsl_command_attempted = ""
    wsl_recommended_command = "wsl sh -lc 'command -v sage && sage --version'"
    wsl_path = which_func("wsl")
    if wsl_path:
        launch_command = [wsl_path, "sh", "-lc", "printf wsl-ok"]
        commands.append(_command_text(launch_command))
        launch_code, launch_stdout, launch_stderr = run(launch_command)
        wsl_launched = launch_code == 0 and "wsl-ok" in launch_stdout
        if not wsl_launched:
            failures.append(f"WSL launch failed: {launch_stderr or launch_stdout or launch_code}")
        else:
            find_command = [wsl_path, "sh", "-lc", "command -v sage"]
            commands.append(_command_text(find_command))
            find_code, find_stdout, find_stderr = run(find_command)
            wsl_sage_binary_found = find_code == 0 and bool(find_stdout.strip())
            if not wsl_sage_binary_found:
                failures.append(f"WSL launched but Sage binary was not found: {find_stderr or find_stdout or find_code}")
            else:
                command = [wsl_path, "sh", "-lc", "sage --version"]
                wsl_command_attempted = _command_text(command)
                commands.append(wsl_command_attempted)
                code, stdout, stderr = run(command)
                if code == 0:
                    wsl_sage = True
                    wsl_version = _version_from_output(stdout, stderr)
                else:
                    failures.append(
                        f"WSL sage failed or timed out after {timeout_seconds} seconds: {stderr or stdout or code}; "
                        f"manual test: {wsl_recommended_command}"
                    )
    else:
        failures.append("wsl not found on PATH")

    docker_available = False
    docker_version = ""
    docker_path = which_func("docker")
    if docker_path:
        command = [docker_path, "--version"]
        commands.append(_command_text(command))
        code, stdout, stderr = run(command)
        if code == 0:
            docker_available = True
            docker_version = _version_from_output(stdout, stderr)
        else:
            failures.append(f"Docker failed: {stderr or stdout or code}")
    else:
        failures.append("docker not found on PATH")

    if native_sage:
        mode = "native_sage"
        version = native_version
        reason = ""
    elif wsl_sage:
        mode = "wsl_sage"
        version = wsl_version
        reason = ""
    elif docker_available:
        mode = "docker"
        version = docker_version
        reason = ""
    elif ci_mode:
        mode = "ci"
        version = ""
        reason = "CI mode detected, but no native Sage, WSL Sage, or Docker command succeeded."
    else:
        mode = "unavailable"
        version = ""
        reason = "; ".join(failures)

    return SageEnvironmentReport(
        execution_mode=mode,
        detected_version=version,
        commands_tested=tuple(commands),
        failure_reason=reason,
        native_sage=native_sage,
        wsl_sage=wsl_sage,
        docker_available=docker_available,
        ci_mode=ci_mode,
        wsl_command_attempted=wsl_command_attempted,
        wsl_timeout_seconds=timeout_seconds,
        wsl_launched=wsl_launched,
        wsl_sage_binary_found=wsl_sage_binary_found,
        wsl_recommended_command=wsl_recommended_command,
    )


def environment_report_markdown(report: SageEnvironmentReport) -> str:
    """Return a Markdown report for the detected Sage environment."""
    lines = [
        "# Sage Environment Report",
        "",
        f"- Execution mode: `{report.execution_mode}`.",
        f"- Detected version: `{report.detected_version or 'none'}`.",
        f"- Native Sage: `{report.native_sage}`.",
        f"- WSL Sage: `{report.wsl_sage}`.",
        f"- Docker available: `{report.docker_available}`.",
        f"- CI mode: `{report.ci_mode}`.",
        f"- WSL launched: `{report.wsl_launched}`.",
        f"- WSL Sage binary found: `{report.wsl_sage_binary_found}`.",
        f"- WSL timeout seconds: `{report.wsl_timeout_seconds}`.",
    ]
    if report.failure_reason:
        lines.append(f"- Failure reason: `{report.failure_reason}`.")
    lines.extend(["", "## Commands Tested", ""])
    if report.commands_tested:
        for command in report.commands_tested:
            lines.append(f"- `{command}`")
    else:
        lines.append("No executable probes were run.")
    lines.extend(
        [
            "",
            "## WSL Diagnosis",
            "",
            f"- Command attempted: `{report.wsl_command_attempted or 'none'}`",
            f"- Recommended manual command: `{report.wsl_recommended_command}`",
            "",
            "## Interpretation",
            "",
            "Use native Sage first, then WSL Sage, then Docker. If all are unavailable, generated jobs remain queued and candidates stay at `needs_external_sage_check`.",
            "",
        ]
    )
    return "\n".join(lines)


def write_sage_environment_report(
    output_dir: Path,
    *,
    report: SageEnvironmentReport | None = None,
) -> SageEnvironmentReport:
    """Write `sage_environment.json` and `sage_environment_report.md`."""
    output_dir.mkdir(parents=True, exist_ok=True)
    env_report = report or detect_sage_environment()
    (output_dir / "sage_environment.json").write_text(
        json.dumps(env_report.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "sage_environment_report.md").write_text(
        environment_report_markdown(env_report),
        encoding="utf-8",
    )
    return env_report
