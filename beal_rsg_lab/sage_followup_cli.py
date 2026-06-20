"""CLI for Sage follow-up detection, generation, import, and dossiers."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from types import SimpleNamespace
from typing import Iterable, Mapping

from .candidate_dossier_generator import generate_candidate_dossiers
from .known_case_sage_calibration import calibrate_known_cases_with_sage
from .modular_confidence_updater import sage_followup_report_markdown, update_modular_confidence
from .run_experiment import run_experiment
from .sage_environment_detector import detect_sage_environment, write_sage_environment_report
from .sage_result_importer import import_sage_results
from .sage_roundtrip import sage_execution_manifest_rows, sage_roundtrip_summary_rows


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


def import_run(run_dir: Path) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    """Import Sage JSON for a run and refresh summary CSVs."""
    job_rows = _read_csv(run_dir / "sage_job_manifest.csv")
    jobs = [_row_to_job(row) for row in job_rows]
    import_records = import_sage_results(jobs)
    confidence_records = update_modular_confidence(jobs, import_records)
    known_rows = _read_csv(run_dir / "known_case_calibration_summary.csv")
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
    _write_csv(run_dir / "sage_execution_manifest.csv", execution_rows)
    _write_csv(run_dir / "sage_roundtrip_summary.csv", roundtrip_rows)
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


def summarize_run(run_dir: Path, dossier_dir: Path) -> list[dict[str, object]]:
    """Generate dossiers for a run and write the run-local dossier index."""
    job_rows = _read_csv(run_dir / "sage_job_manifest.csv")
    import_rows = _read_csv(run_dir / "sage_import_results.csv")
    confidence_rows = _read_csv(run_dir / "modular_confidence_summary.csv")
    known_rows = _read_csv(run_dir / "known_case_calibration_summary.csv")
    unit_rows = _read_csv(run_dir / "unit_survivor_summary.csv")
    records, index_text = generate_candidate_dossiers(
        run_dir=run_dir,
        dossier_dir=dossier_dir,
        job_rows=job_rows,
        import_rows=import_rows,
        confidence_rows=confidence_rows,
        known_case_rows=known_rows,
        unit_rows=unit_rows,
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

    summarize = subparsers.add_parser("summarize", help="Generate queued-signature dossiers.")
    summarize.add_argument("--run-dir", help="Run directory. Defaults to latest run.")
    summarize.add_argument("--dossier-dir", default="docs/dossiers")
    summarize.set_defaults(func=command_summarize)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
