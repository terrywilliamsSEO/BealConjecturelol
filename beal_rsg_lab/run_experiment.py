"""Experiment runner for the Beal RSG lab."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
import json
from pathlib import Path
from typing import Iterable

from .number_theory import primes_up_to
from .rsg_modular_shadow import ShadowRecord, build_shadow_records
from .rsg_residue_engine import DEFAULT_EXPONENTS, parse_prime_list, run_sweep
from .rsg_valuation_engine import analyze_results


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


def _merged_summary_rows(results, valuations, shadows) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    shadow_by_key = {(shadow.signature, shadow.ell): shadow for shadow in shadows}
    valuation_by_key = {(valuation.signature, valuation.ell): valuation for valuation in valuations}
    for result in results:
        key = (result.signature, result.ell)
        row = result.to_flat_dict()
        valuation = valuation_by_key[key]
        shadow = shadow_by_key[key]
        for prefix, payload in (
            ("valuation", valuation.to_flat_dict()),
            ("shadow", shadow.to_flat_dict()),
        ):
            for field, value in payload.items():
                if field in {"signature", "ell"}:
                    continue
                row[f"{prefix}_{field}"] = value
        rows.append(row)
    return rows


def _interesting_rows(shadows: Iterable[ShadowRecord], limit: int | None = None) -> list[dict[str, object]]:
    interesting = [
        shadow
        for shadow in shadows
        if shadow.promotion_status in {"promoted_candidate", "watchlist"}
    ]
    interesting.sort(key=lambda shadow: (shadow.promotion_status == "promoted_candidate", shadow.candidate_score), reverse=True)
    if limit is not None:
        interesting = interesting[:limit]
    return [shadow.to_flat_dict() for shadow in interesting]


def _report_markdown(
    *,
    output_dir: Path,
    result_count: int,
    interesting_count: int,
    promoted_count: int,
    prime_values: tuple[int, ...],
    control_samples: int,
    compute_lift: bool,
    top_cases: list[dict[str, object]],
) -> str:
    generated = datetime.now().isoformat(timespec="seconds")
    prime_text = ", ".join(str(prime) for prime in prime_values)
    lines = [
        "# RSG Experiment Report",
        "",
        f"Generated: `{generated}`",
        f"Output directory: `{output_dir.as_posix()}`",
        "",
        "## Scope",
        "",
        f"- Rows: `{result_count}` signature/prime cases.",
        f"- Primes: `{prime_text}`.",
        f"- Control samples per row: `{control_samples}`.",
        f"- Lift survival computed: `{compute_lift}`.",
        "",
        "## Interpretation Guardrail",
        "",
        "This report ranks obstruction candidates. It does not claim a proof of Beal or any generalized Fermat case.",
        "",
        "A promoted candidate repeats across a cluster, beats randomized subgroup-coset controls, and carries a valuation or lift flag.",
        "",
        "## Candidate Counts",
        "",
        f"- Promoted candidates: `{promoted_count}`.",
        f"- Promoted plus watchlist rows: `{interesting_count}`.",
        "",
        "## Top Rows",
        "",
    ]
    if not top_cases:
        lines.append("No rows passed the promoted/watchlist filters in this run.")
    else:
        lines.extend(
            [
                "| rank | status | signature | ell | score | cluster_size | rationale |",
                "| ---: | --- | --- | ---: | ---: | ---: | --- |",
            ]
        )
        for index, row in enumerate(top_cases[:12], start=1):
            lines.append(
                "| {rank} | {status} | {signature} | {ell} | {score} | {cluster_size} | {rationale} |".format(
                    rank=index,
                    status=row["promotion_status"],
                    signature=row["signature"],
                    ell=row["ell"],
                    score=row["candidate_score"],
                    cluster_size=row["cluster_size"],
                    rationale=row["rationale"],
                )
            )
    lines.extend(
        [
            "",
            "## Files",
            "",
            "- `summary.csv`: complete row-level data.",
            "- `interesting_cases.csv`: promoted and watchlist candidates.",
            "- `clusters.csv`: repeated obstruction fingerprints.",
            "- `metadata.json`: run parameters.",
            "",
            "## Next Research Step",
            "",
            "Inspect the strongest clusters and try to restate them as exact local lemmas. Any lemma candidate should then be tested against additional primes and a stricter lift/modular-shadow consistency check.",
            "",
        ]
    )
    return "\n".join(lines)


def run_experiment(
    *,
    output_root: Path = Path("runs"),
    exponents: tuple[int, ...] = DEFAULT_EXPONENTS,
    prime_limit: int = 43,
    primes: tuple[int, ...] | None = None,
    compute_lift: bool = True,
    control_samples: int = 24,
    seed: int = 20260620,
    timestamp: str | None = None,
) -> Path:
    """Run an RSG experiment and write structured outputs."""
    prime_values = primes if primes is not None else primes_up_to(prime_limit, odd_only=True)
    run_id = timestamp or datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = output_root / run_id
    output_dir.mkdir(parents=True, exist_ok=False)

    results = run_sweep(
        exponents=exponents,
        primes=prime_values,
        prime_limit=prime_limit,
        compute_lift=compute_lift,
        control_samples=control_samples,
        seed=seed,
    )
    valuations = analyze_results(results)
    shadows, clusters = build_shadow_records(results, valuations)

    summary_rows = _merged_summary_rows(results, valuations, shadows)
    interesting_rows = _interesting_rows(shadows)
    cluster_rows = [cluster.to_flat_dict() for cluster in clusters]

    _write_csv(output_dir / "summary.csv", summary_rows)
    _write_csv(output_dir / "interesting_cases.csv", interesting_rows)
    _write_csv(output_dir / "clusters.csv", cluster_rows)

    promoted_count = sum(1 for shadow in shadows if shadow.promotion_status == "promoted_candidate")
    metadata = {
        "run_id": run_id,
        "exponents": exponents,
        "primes": prime_values,
        "compute_lift": compute_lift,
        "control_samples": control_samples,
        "seed": seed,
        "result_count": len(results),
        "interesting_count": len(interesting_rows),
        "promoted_count": promoted_count,
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    report = _report_markdown(
        output_dir=output_dir,
        result_count=len(results),
        interesting_count=len(interesting_rows),
        promoted_count=promoted_count,
        prime_values=prime_values,
        control_samples=control_samples,
        compute_lift=compute_lift,
        top_cases=interesting_rows,
    )
    (output_dir / "README_REPORT.md").write_text(report, encoding="utf-8")
    return output_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Beal RSG discovery sweep.")
    parser.add_argument("--output-root", default="runs", help="Directory that will receive timestamped run folders.")
    parser.add_argument("--prime-limit", type=int, default=43, help="Use odd primes up to this limit when --primes is absent.")
    parser.add_argument("--primes", help="Comma-separated prime list, for example 5,7,11.")
    parser.add_argument("--exponents", default=",".join(str(value) for value in DEFAULT_EXPONENTS))
    parser.add_argument("--control-samples", type=int, default=24)
    parser.add_argument("--seed", type=int, default=20260620)
    parser.add_argument("--timestamp", help="Optional deterministic run folder name.")
    parser.add_argument("--no-lift", action="store_true", help="Skip ell^2 lift survival for faster smoke runs.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    exponents = tuple(int(part.strip()) for part in args.exponents.split(",") if part.strip())
    if not exponents:
        parser.error("--exponents cannot be empty")
    primes = parse_prime_list(args.primes) if args.primes else None
    output_dir = run_experiment(
        output_root=Path(args.output_root),
        exponents=exponents,
        prime_limit=args.prime_limit,
        primes=primes,
        compute_lift=not args.no_lift,
        control_samples=args.control_samples,
        seed=args.seed,
        timestamp=args.timestamp,
    )
    print(output_dir.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
