"""Rank focused `(5,4,5)` eliminating good primes for human review."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Mapping

from .local_case_closure_score_545 import (
    LocalCaseClosureScoreRecord,
    SAFE_LOCAL_CASE_CLOSURE_LABELS,
    build_local_case_closure_scores_545,
)


SAFE_BEST_ELIMINATING_PRIME_LABELS = set(SAFE_LOCAL_CASE_CLOSURE_LABELS)


@dataclass(frozen=True)
class BestEliminatingPrimeRecord:
    """One ranked focused eliminating-prime row."""

    signature: str
    rank: int
    prime: int
    closure_label: str
    best_priority_label: str
    unit_surviving_branch_count: int
    single_mask_surviving_branch_count: int
    multiplicative_coverage_gap_count: int
    coefficient_missing_branches: int
    formula_missing_branches: int
    level_lowering_assumption_required_branches: int
    clean_multiplicative_congruence_coverage: bool
    q3_reliance_penalty: int
    human_review_priority: int
    route_ceiling_label: str
    reason: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


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


def _int_value(value: object, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _bool_value(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).lower() in {"true", "1", "yes"}


def _closure_row_from_mapping(row: Mapping[str, object]) -> LocalCaseClosureScoreRecord:
    return LocalCaseClosureScoreRecord(
        signature=str(row.get("signature", "5-4-5")),
        prime=_int_value(row.get("prime")),
        newform_count=_int_value(row.get("newform_count")),
        unit_eliminated_newforms=str(row.get("unit_eliminated_newforms", "")),
        unit_surviving_newforms=str(row.get("unit_surviving_newforms", "")),
        unit_unresolved_newforms=str(row.get("unit_unresolved_newforms", "")),
        unit_eliminated_branch_count=_int_value(row.get("unit_eliminated_branch_count")),
        unit_surviving_branch_count=_int_value(row.get("unit_surviving_branch_count")),
        unit_unresolved_branch_count=_int_value(row.get("unit_unresolved_branch_count")),
        primitive_forbidden_masks=str(row.get("primitive_forbidden_masks", "")),
        single_mask_total_branches=_int_value(row.get("single_mask_total_branches")),
        single_mask_eliminated_branches=_int_value(row.get("single_mask_eliminated_branches")),
        single_mask_surviving_branches=_int_value(row.get("single_mask_surviving_branches")),
        coefficient_missing_branches=_int_value(row.get("coefficient_missing_branches")),
        formula_missing_branches=_int_value(row.get("formula_missing_branches")),
        level_lowering_assumption_required_branches=_int_value(
            row.get("level_lowering_assumption_required_branches")
        ),
        fully_eliminated_newforms=str(row.get("fully_eliminated_newforms", "")),
        surviving_newforms=str(row.get("surviving_newforms", "")),
        unresolved_newforms=str(row.get("unresolved_newforms", "")),
        surviving_branch_count=_int_value(row.get("surviving_branch_count")),
        closure_label=str(row.get("closure_label", "local_coverage_gap")),
        route_ceiling_label=str(row.get("route_ceiling_label", "worth_human_modular_review")),
        reason=str(row.get("reason", "")),
    )


def load_local_case_closure_score_csv(path: Path) -> list[LocalCaseClosureScoreRecord]:
    """Load `local_case_closure_score_545.csv` rows for standalone ranking."""
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return [_closure_row_from_mapping(row) for row in csv.DictReader(handle)]


def _coverage_gap_count(row: LocalCaseClosureScoreRecord) -> int:
    return (
        row.coefficient_missing_branches
        + row.formula_missing_branches
        + row.level_lowering_assumption_required_branches
        + row.unit_unresolved_branch_count
    )


def _priority_index(row: LocalCaseClosureScoreRecord) -> int:
    order = {
        "local_case_elimination_candidate": 0,
        "level_lowering_assumption_required": 1,
        "local_coverage_gap": 2,
        "single_mask_survivor_exists": 3,
        "unit_branch_survivor_exists": 4,
    }
    return order.get(row.closure_label, 5)


def _rank_key(row: LocalCaseClosureScoreRecord) -> tuple[int, int, int, int, int, int, int]:
    return (
        0 if row.closure_label == "local_case_elimination_candidate" else 1,
        row.unit_surviving_branch_count,
        row.single_mask_surviving_branches,
        _coverage_gap_count(row),
        1 if row.prime == 3 else 0,
        _priority_index(row),
        row.prime,
    )


def _reason(row: LocalCaseClosureScoreRecord, *, clean_coverage: bool) -> str:
    if row.closure_label == "local_case_elimination_candidate":
        return "This q has the strongest local-case closure route evidence, subject to human level-lowering review."
    if row.level_lowering_assumption_required_branches:
        return "This q is blocked by an unapplied level-lowering congruence assumption."
    if row.coefficient_missing_branches or row.formula_missing_branches or row.unit_unresolved_branch_count:
        return "This q still has missing coefficient, invariant, or unit-branch data."
    if row.single_mask_surviving_branches:
        return "This q has at least one surviving single-mask multiplicative branch."
    if row.unit_surviving_branch_count:
        return "This q has at least one surviving unit branch."
    if clean_coverage:
        return "This q has clean multiplicative coverage but is still not promoted beyond review."
    return row.reason or "This q remains a conservative local-coverage gap."


def build_best_eliminating_prime_545(
    closure_rows: Iterable[LocalCaseClosureScoreRecord] | None = None,
) -> list[BestEliminatingPrimeRecord]:
    """Rank focused eliminating primes by conservative closure evidence."""
    closures = list(closure_rows) if closure_rows is not None else build_local_case_closure_scores_545([])
    ranked = sorted(closures, key=_rank_key)
    records: list[BestEliminatingPrimeRecord] = []
    for index, row in enumerate(ranked, 1):
        label = row.closure_label if row.closure_label in SAFE_BEST_ELIMINATING_PRIME_LABELS else "local_coverage_gap"
        gap_count = _coverage_gap_count(row)
        clean_coverage = row.single_mask_total_branches > 0 and gap_count == 0
        records.append(
            BestEliminatingPrimeRecord(
                signature=row.signature,
                rank=index,
                prime=row.prime,
                closure_label=label,
                best_priority_label=label,
                unit_surviving_branch_count=row.unit_surviving_branch_count,
                single_mask_surviving_branch_count=row.single_mask_surviving_branches,
                multiplicative_coverage_gap_count=gap_count,
                coefficient_missing_branches=row.coefficient_missing_branches,
                formula_missing_branches=row.formula_missing_branches,
                level_lowering_assumption_required_branches=row.level_lowering_assumption_required_branches,
                clean_multiplicative_congruence_coverage=clean_coverage,
                q3_reliance_penalty=1 if row.prime == 3 else 0,
                human_review_priority=index,
                route_ceiling_label="worth_human_modular_review",
                reason=_reason(row, clean_coverage=clean_coverage),
            )
        )
    return records


def best_eliminating_prime_545_markdown(rows: Iterable[BestEliminatingPrimeRecord]) -> str:
    """Render `BEST_ELIMINATING_PRIME_545.md`."""
    row_list = list(rows)
    any_candidate = any(row.closure_label == "local_case_elimination_candidate" for row in row_list)
    if any_candidate:
        conclusion = (
            "At least one q is a `local_case_elimination_candidate`; this is route evidence only and remains capped at "
            "`worth_human_modular_review`."
        )
    else:
        conclusion = (
            "Every focused q has a surviving branch or coverage gap, so the focused local status remains "
            "`local_coverage_gap`."
        )
    lines = [
        "# Best Eliminating Prime Ranking For `(5,4,5)`",
        "",
        "This ranking searches the focused primes q in `{3,13,17,41,61}` for the cleanest local-case closure route. It is route evidence only and does not certify any theorem-level claim or exclusion.",
        "",
        "| rank | q | label | unit survivors | single-mask survivors | coverage gaps | q=3 penalty | reason |",
        "| ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in row_list:
        lines.append(
            f"| {row.rank} | {row.prime} | `{row.closure_label}` | "
            f"{row.unit_surviving_branch_count} | {row.single_mask_surviving_branch_count} | "
            f"{row.multiplicative_coverage_gap_count} | {row.q3_reliance_penalty} | {row.reason} |"
        )
    lines.extend(
        [
            "",
            "## Current Conclusion",
            "",
            conclusion,
            "",
            "- Highest allowed route label: `worth_human_modular_review`.",
            "",
        ]
    )
    return "\n".join(lines)


def write_best_eliminating_prime_545_csv(
    path: Path,
    rows: Iterable[BestEliminatingPrimeRecord] | None = None,
) -> Path:
    """Write `best_eliminating_prime_545.csv` rows to `path`."""
    record_rows = list(rows) if rows is not None else build_best_eliminating_prime_545()
    _write_csv(path, [row.to_flat_dict() for row in record_rows])
    return path


def write_best_eliminating_prime_545_markdown(
    path: Path,
    rows: Iterable[BestEliminatingPrimeRecord] | None = None,
) -> Path:
    """Write `BEST_ELIMINATING_PRIME_545.md` to `path`."""
    record_rows = list(rows) if rows is not None else build_best_eliminating_prime_545()
    path.write_text(best_eliminating_prime_545_markdown(record_rows), encoding="utf-8")
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Rank focused 5-4-5 eliminating good primes.")
    parser.add_argument("--closure-csv", default="local_case_closure_score_545.csv")
    parser.add_argument("--output-csv", default="best_eliminating_prime_545.csv")
    parser.add_argument("--output-md", default="BEST_ELIMINATING_PRIME_545.md")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    closure_rows = load_local_case_closure_score_csv(Path(args.closure_csv))
    rows = build_best_eliminating_prime_545(closure_rows if closure_rows else None)
    write_best_eliminating_prime_545_csv(Path(args.output_csv), rows)
    write_best_eliminating_prime_545_markdown(Path(args.output_md), rows)
    print(Path(args.output_csv).as_posix())
    print(Path(args.output_md).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
