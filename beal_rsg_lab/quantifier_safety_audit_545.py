"""Quantifier-safety audit for the focused `(5,4,5)` cross-prime route."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from .cross_prime_branch_compatibility_545 import (
    CrossPrimeBranchCompatibilityRecord,
    NON_Q3_COMPATIBILITY_PRIMES_545,
)
from .local_case_closure_score_545 import PAIRWISE_PRIMITIVE_FORBIDDEN_MASKS_545
from .multiplicative_reduction_congruence_545 import MultiplicativeReductionCongruenceRecord
from .nonunit_elimination_545 import NonunitEliminationRecord
from .trace_congruence_filter_545 import TraceCongruenceFilterRecord


SINGLE_MASKS_545 = ("A_only", "B_only", "C_only")
SAFE_QUANTIFIER_SAFETY_LABELS = {
    "valid_exists_prime_elimination",
    "quantifier_safe_cross_prime_candidate",
    "invalid_cross_prime_branch_dependency",
    "branch_coverage_gap",
    "data_insufficient",
}


@dataclass(frozen=True)
class QuantifierSafetyAuditRecord:
    """One newform or aggregate quantifier-safety row."""

    signature: str
    prime_set: str
    newform_index: int
    newform_label: str
    eliminated_primes: str
    complete_coverage_prime_count: int
    branch_coverage_gap_count: int
    data_insufficient_count: int
    fixed_branch_dependency_detected: bool
    per_prime_branch_coverage: str
    pairwise_coverage_status: str
    quantifier_classification: str
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


def _join(items: Iterable[object]) -> str:
    return ";".join(str(item) for item in items)


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


def _newform_label(
    index: int,
    filter_rows: list[TraceCongruenceFilterRecord],
    multiplicative_rows: list[MultiplicativeReductionCongruenceRecord],
) -> str:
    for row in filter_rows:
        if row.newform_index == index and row.newform_label:
            return row.newform_label
    for row in multiplicative_rows:
        if row.newform_index == index and row.newform_label:
            return row.newform_label
    return f"newform_{index}"


def _unit_status(row: TraceCongruenceFilterRecord | None) -> str:
    if row is None:
        return "data_insufficient"
    if row.filter_classification == "eliminated":
        return "eliminated"
    if row.filter_classification == "survives":
        return "survives"
    return "data_insufficient"


def _single_status(row: MultiplicativeReductionCongruenceRecord | None) -> str:
    if row is None:
        return "data_insufficient"
    if row.congruence_classification == "multiplicative_branch_eliminated":
        return "eliminated"
    if row.congruence_classification == "multiplicative_branch_survives":
        return "survives"
    return "data_insufficient"


def _pairwise_status(prime: int, rows: list[NonunitEliminationRecord]) -> tuple[str, bool, bool]:
    by_mask = {row.valuation_mask: row for row in rows if row.prime == prime}
    missing = [mask for mask in PAIRWISE_PRIMITIVE_FORBIDDEN_MASKS_545 if mask not in by_mask]
    if missing:
        return f"missing:{_join(missing)}", False, True
    not_forbidden = [
        mask
        for mask in PAIRWISE_PRIMITIVE_FORBIDDEN_MASKS_545
        if not by_mask[mask].primitive_forbidden
    ]
    if not_forbidden:
        return f"not_primitive_forbidden:{_join(not_forbidden)}", False, False
    return "all_pairwise_primitive_forbidden", True, False


def _cross_prime_label(
    index: int,
    cross_prime_rows: list[CrossPrimeBranchCompatibilityRecord],
) -> str:
    for row in cross_prime_rows:
        if row.newform_index == index:
            return row.compatibility_label
    return ""


def _classify_newform(
    *,
    eliminated_primes: list[int],
    data_insufficient_count: int,
    cross_prime_label: str,
) -> tuple[str, bool, str]:
    if eliminated_primes:
        return (
            "valid_exists_prime_elimination",
            False,
            "This newform has at least one non-q=3 prime where unit, single-mask, and pairwise branches are all covered.",
        )
    if data_insufficient_count:
        return (
            "data_insufficient",
            False,
            "At least one branch needed to test an eliminating prime is missing or not safely classified.",
        )
    if cross_prime_label == "cross_prime_elimination_candidate":
        return (
            "invalid_cross_prime_branch_dependency",
            True,
            "The cross-prime claim would require coupling branch choices across different primes instead of using one fully eliminating prime.",
        )
    return (
        "branch_coverage_gap",
        False,
        "No non-q=3 prime currently covers every local branch for this newform.",
    )


def build_quantifier_safety_audit_545(
    filter_rows: Iterable[TraceCongruenceFilterRecord],
    multiplicative_rows: Iterable[MultiplicativeReductionCongruenceRecord],
    nonunit_rows: Iterable[NonunitEliminationRecord],
    cross_prime_rows: Iterable[CrossPrimeBranchCompatibilityRecord] = (),
    *,
    newform_count: int = 2,
    target_primes: tuple[int, ...] = NON_Q3_COMPATIBILITY_PRIMES_545,
) -> list[QuantifierSafetyAuditRecord]:
    """Check the exists-prime-per-newform quantifier for the cross-prime route."""
    target_set = set(target_primes)
    filters = [row for row in filter_rows if row.prime in target_set]
    multiplicative = [row for row in multiplicative_rows if row.prime in target_set]
    nonunit = [row for row in nonunit_rows if row.prime in target_set]
    cross_rows = [row for row in cross_prime_rows if row.newform_index >= 0]
    filter_by_key = {(row.prime, row.newform_index): row for row in filters}
    multiplicative_by_key = {
        (row.prime, row.newform_index, row.valuation_mask): row
        for row in multiplicative
    }
    indices = _newform_indices(filters, multiplicative, newform_count)
    prime_text = _join(target_primes)
    records: list[QuantifierSafetyAuditRecord] = []
    for index in indices:
        eliminated_primes: list[int] = []
        details: list[str] = []
        pairwise_details: list[str] = []
        branch_gap_count = 0
        data_gap_count = 0
        for prime in target_primes:
            unit = _unit_status(filter_by_key.get((prime, index)))
            singles = {
                mask: _single_status(multiplicative_by_key.get((prime, index, mask)))
                for mask in SINGLE_MASKS_545
            }
            pairwise, pairwise_covered, pairwise_data_gap = _pairwise_status(prime, nonunit)
            pairwise_details.append(f"q={prime}:{pairwise}")
            branch_statuses = [unit, *singles.values()]
            has_data_gap = pairwise_data_gap or any(status == "data_insufficient" for status in branch_statuses)
            complete = pairwise_covered and all(status == "eliminated" for status in branch_statuses)
            if complete:
                eliminated_primes.append(prime)
            elif has_data_gap:
                data_gap_count += 1
            else:
                branch_gap_count += 1
            details.append(
                "q={prime}:unit={unit},A_only={a},B_only={b},C_only={c},pairwise={pairwise},complete={complete}".format(
                    prime=prime,
                    unit=unit,
                    a=singles["A_only"],
                    b=singles["B_only"],
                    c=singles["C_only"],
                    pairwise=pairwise,
                    complete=str(complete),
                )
            )
        label, fixed_dependency, reason = _classify_newform(
            eliminated_primes=eliminated_primes,
            data_insufficient_count=data_gap_count,
            cross_prime_label=_cross_prime_label(index, cross_rows),
        )
        if label not in SAFE_QUANTIFIER_SAFETY_LABELS:
            label = "data_insufficient"
            fixed_dependency = False
            reason = "Unexpected quantifier label was downgraded to data_insufficient."
        records.append(
            QuantifierSafetyAuditRecord(
                signature="5-4-5",
                prime_set=prime_text,
                newform_index=index,
                newform_label=_newform_label(index, filters, multiplicative),
                eliminated_primes=_join(eliminated_primes),
                complete_coverage_prime_count=len(eliminated_primes),
                branch_coverage_gap_count=branch_gap_count,
                data_insufficient_count=data_gap_count,
                fixed_branch_dependency_detected=fixed_dependency,
                per_prime_branch_coverage="|".join(details),
                pairwise_coverage_status="|".join(pairwise_details),
                quantifier_classification=label,
                route_ceiling_label="worth_human_modular_review",
                reason=reason,
            )
        )
    aggregate_label = "quantifier_safe_cross_prime_candidate"
    aggregate_reason = "Every level-220 newform has at least one non-q=3 prime with complete local branch coverage."
    if any(row.quantifier_classification == "invalid_cross_prime_branch_dependency" for row in records):
        aggregate_label = "invalid_cross_prime_branch_dependency"
        aggregate_reason = "At least one newform lacks an exists-prime elimination and would require invalid cross-prime branch coupling."
    elif any(row.quantifier_classification == "data_insufficient" for row in records):
        aggregate_label = "data_insufficient"
        aggregate_reason = "At least one newform row has missing or unsafe branch data."
    elif any(row.quantifier_classification == "branch_coverage_gap" for row in records):
        aggregate_label = "branch_coverage_gap"
        aggregate_reason = "At least one newform has no non-q=3 prime with complete branch coverage."
    if aggregate_label not in SAFE_QUANTIFIER_SAFETY_LABELS:
        aggregate_label = "data_insufficient"
        aggregate_reason = "Unexpected aggregate label was downgraded to data_insufficient."
    records.append(
        QuantifierSafetyAuditRecord(
            signature="5-4-5",
            prime_set=prime_text,
            newform_index=-1,
            newform_label="all_newforms",
            eliminated_primes=";".join(
                f"newform_{row.newform_index}:{row.eliminated_primes or 'none'}"
                for row in records
            ),
            complete_coverage_prime_count=sum(row.complete_coverage_prime_count for row in records),
            branch_coverage_gap_count=sum(row.branch_coverage_gap_count for row in records),
            data_insufficient_count=sum(row.data_insufficient_count for row in records),
            fixed_branch_dependency_detected=any(row.fixed_branch_dependency_detected for row in records),
            per_prime_branch_coverage="see_newform_rows",
            pairwise_coverage_status="see_newform_rows",
            quantifier_classification=aggregate_label,
            route_ceiling_label="worth_human_modular_review",
            reason=aggregate_reason,
        )
    )
    return records


def quantifier_safety_audit_545_markdown(rows: Iterable[QuantifierSafetyAuditRecord]) -> str:
    """Render the quantifier-safety audit as Markdown."""
    row_list = list(rows)
    aggregate = next((row for row in row_list if row.newform_index == -1), None)
    lines = [
        "# Quantifier Safety Audit For `(5,4,5)`",
        "",
        "This audit checks the theorem-safe quantifier: for each level-220 newform, there must be at least one non-q=3 prime where every tracked local branch is covered. It does not use a fixed branch assignment across different primes.",
        "",
        f"- Aggregate label: `{aggregate.quantifier_classification if aggregate else 'data_insufficient'}`.",
        f"- Route ceiling: `{aggregate.route_ceiling_label if aggregate else 'worth_human_modular_review'}`.",
        "",
        "| newform | eliminating q | complete q count | branch gaps | data gaps | fixed-branch dependency | label |",
        "| --- | --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in row_list:
        if row.newform_index == -1:
            continue
        lines.append(
            f"| `{row.newform_label}` | `{row.eliminated_primes or 'none'}` | "
            f"{row.complete_coverage_prime_count} | {row.branch_coverage_gap_count} | "
            f"{row.data_insufficient_count} | `{row.fixed_branch_dependency_detected}` | "
            f"`{row.quantifier_classification}` |"
        )
    lines.extend(
        [
            "",
            "## Branch Coverage Details",
            "",
            "| newform | per-prime branch status | pairwise masks |",
            "| --- | --- | --- |",
        ]
    )
    for row in row_list:
        if row.newform_index == -1:
            continue
        lines.append(
            f"| `{row.newform_label}` | `{row.per_prime_branch_coverage}` | `{row.pairwise_coverage_status}` |"
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `valid_exists_prime_elimination` means a single q eliminates that newform across unit, A_only, B_only, C_only, and pairwise masks.",
            "- `invalid_cross_prime_branch_dependency` means the argument would depend on coupling branch choices across different primes.",
            "- `quantifier_safe_cross_prime_candidate` is still conditional route evidence and remains capped at `worth_human_modular_review`.",
            "",
        ]
    )
    return "\n".join(lines)


def write_quantifier_safety_audit_545_csv(
    path: Path,
    rows: Iterable[QuantifierSafetyAuditRecord],
) -> Path:
    """Write `quantifier_safety_audit_545.csv`."""
    _write_csv(path, [row.to_flat_dict() for row in rows])
    return path


def write_quantifier_safety_audit_545_markdown(
    path: Path,
    rows: Iterable[QuantifierSafetyAuditRecord],
) -> Path:
    """Write `QUANTIFIER_SAFETY_AUDIT_545.md`."""
    path.write_text(quantifier_safety_audit_545_markdown(rows), encoding="utf-8")
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write focused 5-4-5 quantifier-safety rows.")
    parser.add_argument("--output", default="quantifier_safety_audit_545.csv")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    write_quantifier_safety_audit_545_csv(Path(args.output), [])
    print(Path(args.output).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
