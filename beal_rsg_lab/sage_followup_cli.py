"""CLI for Sage follow-up detection, generation, import, and dossiers."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from types import SimpleNamespace
from typing import Iterable, Mapping

from .candidate_dossier_generator import generate_candidate_dossiers
from .focused_candidate_audit_545 import generate_focused_545_review
from .known_case_sage_calibration import calibrate_known_cases_with_sage
from .level_explanation import explain_candidate_levels
from .modular_candidate_deep_audit import (
    build_modular_candidate_deep_audits,
    modular_candidate_audit_report_markdown,
)
from .modular_confidence_updater import sage_followup_report_markdown, update_modular_confidence
from .newform_trace_matrix import build_newform_trace_matrix
from .proof_obligation_generator import build_proof_obligation_records, proof_obligations_markdown
from .run_experiment import run_experiment
from .sage_environment_detector import detect_sage_environment, write_sage_environment_report
from .sage_job_runner import run_sage_jobs
from .sage_result_importer import import_sage_results
from .sage_roundtrip import sage_execution_manifest_rows, sage_roundtrip_summary_rows
from .timeout_retry_runner import (
    build_timeout_retry_manifest,
    timeout_retry_report_markdown,
    timeout_retry_summary_rows,
)


def _write_csv(path: Path, rows: Iterable[dict[str, object]]) -> None:
    row_list = list(rows)
    if not row_list:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in row_list:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(row_list)


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _bool(value: str) -> bool:
    return str(value).lower() in {"true", "1", "yes"}


def _tuple_str(value: str) -> tuple[str, ...]:
    return tuple(part for part in value.split(";") if part)


def _tuple_int(value: str) -> tuple[int, ...]:
    items: list[int] = []
    for part in value.split(";"):
        if not part:
            continue
        try:
            items.append(int(part))
        except ValueError:
            continue
    return tuple(items)


def _row_to_job(row: Mapping[str, str]) -> SimpleNamespace:
    return SimpleNamespace(
        job_id=row.get("job_id", ""),
        signature=row.get("signature", ""),
        route_label=row.get("route_label", ""),
        candidate_case_ids=_tuple_str(row.get("candidate_case_ids", "")),
        candidate_rows=_tuple_str(row.get("candidate_rows", "")),
        primes_involved=_tuple_int(row.get("primes_involved", "")),
        candidate_levels=_tuple_int(row.get("candidate_levels", "")),
        job_path=row.get("job_path", ""),
        result_path=row.get("result_path", ""),
        sage_available=_bool(row.get("sage_available", "False")),
    )


def _row_to_known_case(row: Mapping[str, str]) -> SimpleNamespace:
    return SimpleNamespace(
        case_id=row.get("case_id", ""),
        signature_text=row.get("signature", ""),
        expected_route=row.get("expected_route", ""),
        actual_route_label=row.get("actual_route_label", ""),
        known_status_label=row.get("known_status_label", ""),
        collision_class=row.get("collision_class", ""),
    )


def latest_run_dir(output_root: Path = Path("runs")) -> Path:
    """Return the most recently modified run directory."""
    runs = [path for path in output_root.iterdir() if path.is_dir()] if output_root.exists() else []
    if not runs:
        raise FileNotFoundError(f"no run directories found under {output_root}")
    return max(runs, key=lambda path: path.stat().st_mtime)


def _run_dir_arg(value: str | None) -> Path:
    return Path(value) if value else latest_run_dir()


def command_detect(args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir) if args.output_dir else _run_dir_arg(args.run_dir)
    report = write_sage_environment_report(output_dir, report=detect_sage_environment())
    print(report.execution_mode)
    return 0


def command_generate(args: argparse.Namespace) -> int:
    output = run_experiment(
        output_root=Path(args.output_root),
        prime_limit=args.prime_limit,
        control_samples=args.control_samples,
        compute_lift=not args.no_lift,
        timestamp=args.timestamp,
    )
    print(output.as_posix())
    return 0


def run_jobs_for_run(
    run_dir: Path,
    *,
    backend: str = "auto",
    timeout_seconds: int = 600,
) -> list[dict[str, object]]:
    """Run generated Sage jobs for a run and write execution results."""
    job_rows = _read_csv(run_dir / "sage_job_manifest.csv")
    jobs = [_row_to_job(row) for row in job_rows]
    environment = write_sage_environment_report(run_dir)
    execution_records = run_sage_jobs(
        run_dir=run_dir,
        jobs=jobs,
        repo_root=Path.cwd(),
        environment=environment,
        backend=backend,
        timeout_seconds=timeout_seconds,
    )
    execution_rows = [record.to_flat_dict() for record in execution_records]
    _write_csv(run_dir / "sage_execution_results.csv", execution_rows)
    return execution_rows


def import_run(run_dir: Path) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    """Import Sage JSON for a run and refresh summary CSVs."""
    job_rows = _read_csv(run_dir / "sage_job_manifest.csv")
    jobs = [_row_to_job(row) for row in job_rows]
    import_records = import_sage_results(jobs)
    confidence_records = update_modular_confidence(jobs, import_records)
    known_rows = _read_csv(run_dir / "known_case_calibration_summary.csv")
    unit_rows = _read_csv(run_dir / "unit_survivor_summary.csv")
    known_case_records = [_row_to_known_case(row) for row in known_rows]
    known_case_sage_records = calibrate_known_cases_with_sage(
        known_case_records,
        jobs,
        import_records,
        confidence_records,
    )
    import_rows = [record.to_flat_dict() for record in import_records]
    confidence_rows = [record.to_flat_dict() for record in confidence_records]
    known_case_sage_rows = [record.to_flat_dict() for record in known_case_sage_records]
    retry_records = build_timeout_retry_manifest(job_rows=job_rows, import_rows=import_rows)
    retry_rows = [record.to_flat_dict() for record in retry_records]
    retry_summary_rows = timeout_retry_summary_rows(retry_records)
    level_records = explain_candidate_levels(
        job_rows=job_rows,
        import_rows=import_rows,
        confidence_rows=confidence_rows,
    )
    level_rows = [record.to_flat_dict() for record in level_records]
    matrix_records = build_newform_trace_matrix(
        job_rows=job_rows,
        import_rows=import_rows,
        confidence_rows=confidence_rows,
    )
    matrix_rows = [record.to_flat_dict() for record in matrix_records]
    audit_records = build_modular_candidate_deep_audits(
        job_rows=job_rows,
        import_rows=import_rows,
        confidence_rows=confidence_rows,
        known_case_rows=known_rows,
        unit_rows=unit_rows,
    )
    audit_rows = [record.to_flat_dict() for record in audit_records]
    obligation_records = build_proof_obligation_records(audit_rows)
    obligation_rows = [record.to_flat_dict() for record in obligation_records]
    env_report = write_sage_environment_report(run_dir)
    execution_rows = sage_execution_manifest_rows(
        job_rows=job_rows,
        environment=env_report,
        repo_root=Path.cwd(),
        run_dir=run_dir,
    )
    roundtrip_rows = sage_roundtrip_summary_rows(
        job_rows=job_rows,
        import_rows=import_rows,
        confidence_rows=confidence_rows,
        known_case_sage_rows=known_case_sage_rows,
    )
    _write_csv(run_dir / "sage_import_results.csv", import_rows)
    _write_csv(run_dir / "modular_confidence_summary.csv", confidence_rows)
    _write_csv(run_dir / "sage_known_case_calibration.csv", known_case_sage_rows)
    _write_csv(run_dir / "timeout_retry_manifest.csv", retry_rows)
    _write_csv(run_dir / "timeout_retry_summary.csv", retry_summary_rows)
    _write_csv(run_dir / "level_explanations.csv", level_rows)
    _write_csv(run_dir / "newform_trace_matrix.csv", matrix_rows)
    _write_csv(run_dir / "modular_candidate_deep_audit.csv", audit_rows)
    _write_csv(run_dir / "proof_obligations.csv", obligation_rows)
    _write_csv(run_dir / "sage_execution_manifest.csv", execution_rows)
    _write_csv(run_dir / "sage_roundtrip_summary.csv", roundtrip_rows)
    (run_dir / "README_TIMEOUT_RETRY.md").write_text(
        timeout_retry_report_markdown(run_dir=run_dir, rows=retry_records),
        encoding="utf-8",
    )
    (run_dir / "proof_obligations.md").write_text(
        proof_obligations_markdown(obligation_records),
        encoding="utf-8",
    )
    (run_dir / "README_MODULAR_CANDIDATE_AUDIT.md").write_text(
        modular_candidate_audit_report_markdown(
            output_dir=run_dir,
            audit_rows=audit_records,
            timeout_count=len(retry_records),
        ),
        encoding="utf-8",
    )
    generate_focused_545_review(run_dir)
    (run_dir / "README_SAGE_FOLLOWUP_REPORT.md").write_text(
        sage_followup_report_markdown(
            output_dir=run_dir.as_posix(),
            jobs=jobs,
            imports=import_records,
            confidence_rows=confidence_records,
            known_case_rows=known_case_sage_records,
        ),
        encoding="utf-8",
    )
    return import_rows, confidence_rows, known_case_sage_rows


def command_import(args: argparse.Namespace) -> int:
    run_dir = _run_dir_arg(args.run_dir)
    import_run(run_dir)
    print(run_dir.as_posix())
    return 0


def command_run(args: argparse.Namespace) -> int:
    run_dir = _run_dir_arg(args.run_dir)
    rows = run_jobs_for_run(
        run_dir,
        backend=args.backend,
        timeout_seconds=args.timeout_seconds,
    )
    statuses: dict[str, int] = {}
    for row in rows:
        status = str(row["sage_status"])
        statuses[status] = statuses.get(status, 0) + 1
    print(statuses)
    return 1 if statuses.get("failed") or statuses.get("timeout") else 0


def summarize_run(run_dir: Path, dossier_dir: Path) -> list[dict[str, object]]:
    """Generate dossiers for a run and write the run-local dossier index."""
    job_rows = _read_csv(run_dir / "sage_job_manifest.csv")
    import_rows = _read_csv(run_dir / "sage_import_results.csv")
    confidence_rows = _read_csv(run_dir / "modular_confidence_summary.csv")
    known_rows = _read_csv(run_dir / "known_case_calibration_summary.csv")
    unit_rows = _read_csv(run_dir / "unit_survivor_summary.csv")
    audit_rows = _read_csv(run_dir / "modular_candidate_deep_audit.csv")
    matrix_rows = _read_csv(run_dir / "newform_trace_matrix.csv")
    level_rows = _read_csv(run_dir / "level_explanations.csv")
    obligation_rows = _read_csv(run_dir / "proof_obligations.csv")
    records, index_text = generate_candidate_dossiers(
        run_dir=run_dir,
        dossier_dir=dossier_dir,
        job_rows=job_rows,
        import_rows=import_rows,
        confidence_rows=confidence_rows,
        known_case_rows=known_rows,
        unit_rows=unit_rows,
        audit_rows=audit_rows,
        matrix_rows=matrix_rows,
        level_rows=level_rows,
        obligation_rows=obligation_rows,
    )
    (run_dir / "candidate_dossier_index.md").write_text(index_text, encoding="utf-8")
    _write_csv(run_dir / "candidate_dossier_manifest.csv", [record.to_flat_dict() for record in records])
    return [record.to_flat_dict() for record in records]


def command_summarize(args: argparse.Namespace) -> int:
    run_dir = _run_dir_arg(args.run_dir)
    dossier_dir = Path(args.dossier_dir)
    records = summarize_run(run_dir, dossier_dir)
    print(f"{len(records)} dossiers")
    return 0


def command_retry_manifest(args: argparse.Namespace) -> int:
    run_dir = _run_dir_arg(args.run_dir)
    job_rows = _read_csv(run_dir / "sage_job_manifest.csv")
    import_rows = _read_csv(run_dir / "sage_import_results.csv")
    retry_records = build_timeout_retry_manifest(
        job_rows=job_rows,
        import_rows=import_rows,
        base_timeout_seconds=args.base_timeout_seconds,
        timeout_multiplier=args.timeout_multiplier,
        explicit_timeout_seconds=args.explicit_timeout_seconds,
        include_completed=args.include_completed,
    )
    retry_rows = [record.to_flat_dict() for record in retry_records]
    _write_csv(run_dir / "timeout_retry_manifest.csv", retry_rows)
    _write_csv(run_dir / "timeout_retry_summary.csv", timeout_retry_summary_rows(retry_records))
    (run_dir / "README_TIMEOUT_RETRY.md").write_text(
        timeout_retry_report_markdown(run_dir=run_dir, rows=retry_records),
        encoding="utf-8",
    )
    print(f"{len(retry_rows)} retry jobs")
    return 0


def command_roundtrip(args: argparse.Namespace) -> int:
    if args.skip_generate:
        run_dir = _run_dir_arg(args.run_dir)
    else:
        run_dir = run_experiment(
            output_root=Path(args.output_root),
            prime_limit=args.prime_limit,
            control_samples=args.control_samples,
            compute_lift=not args.no_lift,
            timestamp=args.timestamp,
        )
    environment = write_sage_environment_report(run_dir)
    jobs = [_row_to_job(row) for row in _read_csv(run_dir / "sage_job_manifest.csv")]
    execution_records = run_sage_jobs(
        run_dir=run_dir,
        jobs=jobs,
        repo_root=Path.cwd(),
        environment=environment,
        backend=args.backend,
        timeout_seconds=args.timeout_seconds,
    )
    _write_csv(run_dir / "sage_execution_results.csv", [record.to_flat_dict() for record in execution_records])
    import_rows, confidence_rows, known_case_sage_rows = import_run(run_dir)
    dossier_rows = summarize_run(run_dir, Path(args.dossier_dir))
    status_counts: dict[str, int] = {}
    for row in import_rows:
        status = str(row["sage_status"])
        status_counts[status] = status_counts.get(status, 0) + 1
    print(
        {
            "run_dir": run_dir.as_posix(),
            "execution_mode": environment.execution_mode if args.backend == "auto" else args.backend,
            "import_statuses": status_counts,
            "confidence_rows": len(confidence_rows),
            "known_case_sage_rows": len(known_case_sage_rows),
            "dossiers": len(dossier_rows),
        }
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Sage follow-up support commands.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    detect = subparsers.add_parser("detect", help="Detect native, WSL, Docker, or CI Sage execution.")
    detect.add_argument("--run-dir", help="Run directory to receive environment reports. Defaults to latest run.")
    detect.add_argument("--output-dir", help="Explicit output directory for environment reports.")
    detect.set_defaults(func=command_detect)

    generate = subparsers.add_parser("generate", help="Generate a fresh experiment run with Sage jobs.")
    generate.add_argument("--output-root", default="runs")
    generate.add_argument("--prime-limit", type=int, default=31)
    generate.add_argument("--control-samples", type=int, default=16)
    generate.add_argument("--timestamp")
    generate.add_argument("--no-lift", action="store_true")
    generate.set_defaults(func=command_generate)

    importer = subparsers.add_parser("import", help="Import Sage JSON results for an existing run.")
    importer.add_argument("--run-dir", help="Run directory. Defaults to latest run.")
    importer.set_defaults(func=command_import)

    runner = subparsers.add_parser("run", help="Run generated Sage jobs through the selected backend.")
    runner.add_argument("--run-dir", help="Run directory. Defaults to latest run.")
    runner.add_argument("--backend", default="auto", choices=("auto", "native_sage", "wsl_sage", "docker", "unavailable"))
    runner.add_argument("--timeout-seconds", type=int, default=600)
    runner.set_defaults(func=command_run)

    summarize = subparsers.add_parser("summarize", help="Generate queued-signature dossiers.")
    summarize.add_argument("--run-dir", help="Run directory. Defaults to latest run.")
    summarize.add_argument("--dossier-dir", default="docs/dossiers")
    summarize.set_defaults(func=command_summarize)

    retry = subparsers.add_parser("retry-manifest", help="Write retry files for Sage jobs that timed out.")
    retry.add_argument("--run-dir", help="Run directory. Defaults to latest run.")
    retry.add_argument("--base-timeout-seconds", type=int, default=60)
    retry.add_argument("--timeout-multiplier", type=float, default=4.0)
    retry.add_argument("--explicit-timeout-seconds", type=int)
    retry.add_argument("--include-completed", action="store_true", help="Also include completed jobs for explicit reruns.")
    retry.set_defaults(func=command_retry_manifest)

    roundtrip = subparsers.add_parser("roundtrip", help="Detect, optionally generate, run Sage jobs, import, and summarize.")
    roundtrip.add_argument("--run-dir", help="Existing run directory. Defaults to latest run when --skip-generate is used.")
    roundtrip.add_argument("--skip-generate", action="store_true", help="Use an existing run instead of generating a new one.")
    roundtrip.add_argument("--output-root", default="runs")
    roundtrip.add_argument("--prime-limit", type=int, default=31)
    roundtrip.add_argument("--control-samples", type=int, default=16)
    roundtrip.add_argument("--timestamp")
    roundtrip.add_argument("--no-lift", action="store_true")
    roundtrip.add_argument("--backend", default="auto", choices=("auto", "native_sage", "wsl_sage", "docker", "unavailable"))
    roundtrip.add_argument("--timeout-seconds", type=int, default=600)
    roundtrip.add_argument("--dossier-dir", default="docs/dossiers")
    roundtrip.set_defaults(func=command_roundtrip)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
