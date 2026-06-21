"""Local case closure score for focused `(5,4,5)` eliminating-prime audits."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from .frey_reduction_diagnostics_545 import TARGET_PRIMES_545
from .multiplicative_reduction_congruence_545 import (
    MultiplicativeReductionCongruenceRecord,
    build_multiplicative_reduction_congruences_545,
)
from .trace_congruence_filter_545 import TraceCongruenceFilterRecord


PAIRWISE_PRIMITIVE_FORBIDDEN_MASKS_545 = ("AB", "ABC", "AC", "BC")
SINGLE_MASKS_545 = ("A_only", "B_only", "C_only")
SAFE_LOCAL_CASE_CLOSURE_LABELS = {
    "local_case_elimination_candidate",
    "unit_branch_survivor_exists",
    "single_mask_survivor_exists",
    "level_lowering_assumption_required",
    "local_coverage_gap",
}


@dataclass(frozen=True)
class LocalCaseClosureScoreRecord:
    """One q-level focused local case closure score."""

    signature: str
    prime: int
    newform_count: int
    unit_eliminated_newforms: str
    unit_surviving_newforms: str
    unit_unresolved_newforms: str
    unit_eliminated_branch_count: int
    unit_surviving_branch_count: int
    unit_unresolved_branch_count: int
    primitive_forbidden_masks: str
    single_mask_total_branches: int
    single_mask_eliminated_branches: int
    single_mask_surviving_branches: int
    coefficient_missing_branches: int
    formula_missing_branches: int
    level_lowering_assumption_required_branches: int
    fully_eliminated_newforms: str
    surviving_newforms: str
    unresolved_newforms: str
    surviving_branch_count: int
    closure_label: str
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


def _join_indices(indices: Iterable[int]) -> str:
    return ";".join(f"newform_{index}" for index in sorted(dict.fromkeys(indices)))


def _newform_indices(
    filter_rows: list[TraceCongruenceFilterRecord],
    multiplicative_rows: list[MultiplicativeReductionCongruenceRecord],
    newform_count: int,
) -> tuple[int, ...]:
    indices = set(range(max(newform_count, 0)))
    indices.update(row.newform_index for row in filter_rows)
    indices.update(row.newform_index for row in multiplicative_rows)
    if not indices:
        indices.update(range(2))
    return tuple(sorted(indices))


def _unit_status_by_newform(rows: list[TraceCongruenceFilterRecord]) -> dict[int, str]:
    statuses: dict[int, str] = {}
    for row in rows:
        if row.filter_classification == "eliminated":
            statuses[row.newform_index] = "eliminated"
        elif row.filter_classification == "survives":
            statuses.setdefault(row.newform_index, "survives")
        else:
            statuses.setdefault(row.newform_index, "unresolved")
    return statuses


def _single_status(rows: list[MultiplicativeReductionCongruenceRecord]) -> str:
    labels = {row.congruence_classification for row in rows}
    if "level_lowering_assumption_required" in labels:
        return "level_lowering_assumption_required"
    if labels & {"coefficient_missing", "formula_missing"}:
        return "unresolved"
    if "multiplicative_branch_survives" in labels:
        return "survives"
    if rows and all(row.congruence_classification == "multiplicative_branch_eliminated" for row in rows):
        return "eliminated"
    return "unresolved"


def build_local_case_closure_scores_545(
    filter_rows: Iterable[TraceCongruenceFilterRecord],
    multiplicative_rows: Iterable[MultiplicativeReductionCongruenceRecord] | None = None,
    *,
    newform_count: int = 2,
    target_primes: tuple[int, ...] = TARGET_PRIMES_545,
) -> list[LocalCaseClosureScoreRecord]:
    """Combine unit, primitive-forbidden, and multiplicative branch data by q."""
    filters = list(filter_rows)
    multiplicative = list(multiplicative_rows) if multiplicative_rows is not None else build_multiplicative_reduction_congruences_545()
    records: list[LocalCaseClosureScoreRecord] = []
    for prime in sorted(target_primes):
        prime_filters = [row for row in filters if row.prime == prime]
        prime_multiplicative = [row for row in multiplicative if row.prime == prime]
        indices = _newform_indices(prime_filters, prime_multiplicative, newform_count)
        unit_status = _unit_status_by_newform(prime_filters)
        unit_eliminated: list[int] = []
        unit_surviving: list[int] = []
        unit_unresolved: list[int] = []
        fully_eliminated: list[int] = []
        surviving: list[int] = []
        unresolved: list[int] = []
        for index in indices:
            unit = unit_status.get(index, "unresolved")
            if unit == "eliminated":
                unit_eliminated.append(index)
            elif unit == "survives":
                unit_surviving.append(index)
            else:
                unit_unresolved.append(index)
            single_rows = [row for row in prime_multiplicative if row.newform_index == index]
            single = _single_status(single_rows)
            if unit == "eliminated" and single == "eliminated":
                fully_eliminated.append(index)
            elif unit == "survives" or single == "survives":
                surviving.append(index)
            else:
                unresolved.append(index)
        single_survives = sum(
            1 for row in prime_multiplicative if row.congruence_classification == "multiplicative_branch_survives"
        )
        coefficient_missing = sum(
            1 for row in prime_multiplicative if row.congruence_classification == "coefficient_missing"
        )
        formula_missing = sum(
            1 for row in prime_multiplicative if row.congruence_classification == "formula_missing"
        )
        level_required = sum(
            1 for row in prime_multiplicative if row.congruence_classification == "level_lowering_assumption_required"
        )
        single_eliminated = sum(
            1 for row in prime_multiplicative if row.congruence_classification == "multiplicative_branch_eliminated"
        )
        if level_required:
            label = "level_lowering_assumption_required"
            reason = "At least one multiplicative branch needs the level-lowering congruence before it can be compared."
        elif coefficient_missing or formula_missing or unit_unresolved or unresolved:
            label = "local_coverage_gap"
            reason = "At least one unit or single-mask branch is missing data or remains unresolved."
        elif single_survives:
            label = "single_mask_survivor_exists"
            reason = "At least one single-mask multiplicative branch has an allowed newform congruence."
        elif unit_surviving:
            label = "unit_branch_survivor_exists"
            reason = "At least one unit trace branch survives for this q."
        elif len(fully_eliminated) == len(indices):
            label = "local_case_elimination_candidate"
            reason = "Unit, primitive-forbidden, and single-mask multiplicative congruence checks eliminate all tracked newform branches for this q."
        else:
            label = "local_coverage_gap"
            reason = "At least one tracked newform has a surviving branch after the focused local case split."
        if label not in SAFE_LOCAL_CASE_CLOSURE_LABELS:
            label = "local_coverage_gap"
            reason = "Unexpected closure label was downgraded to local_coverage_gap."
        records.append(
            LocalCaseClosureScoreRecord(
                signature="5-4-5",
                prime=prime,
                newform_count=len(indices),
                unit_eliminated_newforms=_join_indices(unit_eliminated),
                unit_surviving_newforms=_join_indices(unit_surviving),
                unit_unresolved_newforms=_join_indices(unit_unresolved),
                unit_eliminated_branch_count=len(unit_eliminated),
                unit_surviving_branch_count=len(unit_surviving),
                unit_unresolved_branch_count=len(unit_unresolved),
                primitive_forbidden_masks=";".join(PAIRWISE_PRIMITIVE_FORBIDDEN_MASKS_545),
                single_mask_total_branches=len(prime_multiplicative),
                single_mask_eliminated_branches=single_eliminated,
                single_mask_surviving_branches=single_survives,
                coefficient_missing_branches=coefficient_missing,
                formula_missing_branches=formula_missing,
                level_lowering_assumption_required_branches=level_required,
                fully_eliminated_newforms=_join_indices(fully_eliminated),
                surviving_newforms=_join_indices(surviving),
                unresolved_newforms=_join_indices(unresolved),
                surviving_branch_count=len(unit_surviving) + single_survives,
                closure_label=label,
                route_ceiling_label="worth_human_modular_review",
                reason=reason,
            )
        )
    return records


def write_local_case_closure_score_545_csv(
    path: Path,
    rows: Iterable[LocalCaseClosureScoreRecord] | None = None,
) -> Path:
    """Write `local_case_closure_score_545.csv` rows to `path`."""
    record_rows = list(rows) if rows is not None else build_local_case_closure_scores_545([])
    _write_csv(path, [row.to_flat_dict() for row in record_rows])
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write focused 5-4-5 local case closure score rows.")
    parser.add_argument("--output", default="local_case_closure_score_545.csv")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    write_local_case_closure_score_545_csv(Path(args.output))
    print(Path(args.output).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
