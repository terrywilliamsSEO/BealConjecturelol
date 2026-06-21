"""Cross-prime branch compatibility for the focused `(5,4,5)` route."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from .local_case_closure_score_545 import PAIRWISE_PRIMITIVE_FORBIDDEN_MASKS_545
from .multiplicative_reduction_congruence_545 import MultiplicativeReductionCongruenceRecord
from .nonunit_elimination_545 import NonunitEliminationRecord
from .trace_congruence_filter_545 import TraceCongruenceFilterRecord


NON_Q3_COMPATIBILITY_PRIMES_545 = (13, 17, 41, 61)
COMPATIBILITY_BRANCHES_545 = ("unit", "A_only", "B_only", "C_only")
SAFE_CROSS_PRIME_COMPATIBILITY_LABELS = {
    "cross_prime_elimination_candidate",
    "cross_prime_survivor_exists",
    "branch_data_insufficient",
    "level_lowering_assumption_required",
}


@dataclass(frozen=True)
class CrossPrimeBranchCompatibilityRecord:
    """One newform or aggregate cross-prime compatibility row."""

    signature: str
    prime_set: str
    newform_index: int
    newform_label: str
    allowed_branch_sets: str
    eliminated_at_primes: str
    pairwise_primitive_forbidden_status: str
    compatible_prime_count: int
    incompatible_prime_count: int
    data_gap_count: int
    level_lowering_assumption_required_count: int
    compatible_branch_assignment_exists: bool
    compatibility_label: str
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
        return "data_gap"
    if row.filter_classification == "survives":
        return "survives"
    if row.filter_classification == "eliminated":
        return "eliminated"
    return "data_gap"


def _single_status(row: MultiplicativeReductionCongruenceRecord | None) -> str:
    if row is None:
        return "data_gap"
    if row.congruence_classification == "multiplicative_branch_survives":
        return "survives"
    if row.congruence_classification == "multiplicative_branch_eliminated":
        return "eliminated"
    if row.congruence_classification == "level_lowering_assumption_required":
        return "level_lowering_assumption_required"
    return "data_gap"


def _pairwise_status(prime: int, rows: list[NonunitEliminationRecord]) -> str:
    prime_rows = {row.valuation_mask: row for row in rows if row.prime == prime}
    missing = [mask for mask in PAIRWISE_PRIMITIVE_FORBIDDEN_MASKS_545 if mask not in prime_rows]
    if missing:
        return "pairwise_data_insufficient"
    if all(prime_rows[mask].primitive_forbidden for mask in PAIRWISE_PRIMITIVE_FORBIDDEN_MASKS_545):
        return "all_pairwise_primitive_forbidden"
    return "pairwise_not_all_forbidden"


def _classify_newform(
    *,
    allowed_by_prime: dict[int, tuple[str, ...]],
    data_gap_count: int,
    level_required_count: int,
) -> tuple[str, bool, str]:
    if level_required_count:
        return (
            "level_lowering_assumption_required",
            False,
            "At least one branch still needs level-lowering justification before cross-prime compatibility can be evaluated.",
        )
    if data_gap_count:
        return (
            "branch_data_insufficient",
            False,
            "At least one unit, single-mask, or pairwise branch datum is missing or unclear.",
        )
    if all(allowed_by_prime.get(prime) for prime in NON_Q3_COMPATIBILITY_PRIMES_545):
        return (
            "cross_prime_survivor_exists",
            True,
            "This newform has at least one surviving branch at every non-q=3 focused prime.",
        )
    return (
        "cross_prime_elimination_candidate",
        False,
        "At least one non-q=3 focused prime has no surviving branch for this newform.",
    )


def build_cross_prime_branch_compatibility_545(
    filter_rows: Iterable[TraceCongruenceFilterRecord],
    multiplicative_rows: Iterable[MultiplicativeReductionCongruenceRecord],
    nonunit_rows: Iterable[NonunitEliminationRecord],
    *,
    newform_count: int = 2,
    target_primes: tuple[int, ...] = NON_Q3_COMPATIBILITY_PRIMES_545,
) -> list[CrossPrimeBranchCompatibilityRecord]:
    """Build non-q=3 cross-prime branch compatibility rows."""
    filters = [row for row in filter_rows if row.prime in set(target_primes)]
    multiplicative = [row for row in multiplicative_rows if row.prime in set(target_primes)]
    nonunit = [row for row in nonunit_rows if row.prime in set(target_primes)]
    filter_by_key = {(row.prime, row.newform_index): row for row in filters}
    multiplicative_by_key = {
        (row.prime, row.newform_index, row.valuation_mask): row
        for row in multiplicative
    }
    indices = _newform_indices(filters, multiplicative, newform_count)
    prime_text = _join(target_primes)
    records: list[CrossPrimeBranchCompatibilityRecord] = []
    for index in indices:
        allowed_by_prime: dict[int, tuple[str, ...]] = {}
        pairwise_parts: list[str] = []
        data_gap_count = 0
        level_required_count = 0
        for prime in target_primes:
            allowed: list[str] = []
            pairwise = _pairwise_status(prime, nonunit)
            pairwise_parts.append(f"q={prime}:{pairwise}")
            if pairwise != "all_pairwise_primitive_forbidden":
                data_gap_count += 1
            unit = _unit_status(filter_by_key.get((prime, index)))
            if unit == "survives":
                allowed.append("unit")
            elif unit == "data_gap":
                data_gap_count += 1
            for mask in ("A_only", "B_only", "C_only"):
                single = _single_status(multiplicative_by_key.get((prime, index, mask)))
                if single == "survives":
                    allowed.append(mask)
                elif single == "level_lowering_assumption_required":
                    level_required_count += 1
                elif single == "data_gap":
                    data_gap_count += 1
            allowed_by_prime[prime] = tuple(allowed)
        label, compatible, reason = _classify_newform(
            allowed_by_prime=allowed_by_prime,
            data_gap_count=data_gap_count,
            level_required_count=level_required_count,
        )
        if label not in SAFE_CROSS_PRIME_COMPATIBILITY_LABELS:
            label = "branch_data_insufficient"
            compatible = False
            reason = "Unexpected cross-prime label was downgraded to branch_data_insufficient."
        eliminated_primes = [prime for prime in target_primes if not allowed_by_prime.get(prime)]
        records.append(
            CrossPrimeBranchCompatibilityRecord(
                signature="5-4-5",
                prime_set=prime_text,
                newform_index=index,
                newform_label=_newform_label(index, filters, multiplicative),
                allowed_branch_sets="|".join(
                    f"q={prime}:{','.join(allowed_by_prime[prime]) or 'none'}"
                    for prime in target_primes
                ),
                eliminated_at_primes=_join(eliminated_primes),
                pairwise_primitive_forbidden_status="|".join(pairwise_parts),
                compatible_prime_count=sum(1 for prime in target_primes if allowed_by_prime.get(prime)),
                incompatible_prime_count=len(eliminated_primes),
                data_gap_count=data_gap_count,
                level_lowering_assumption_required_count=level_required_count,
                compatible_branch_assignment_exists=compatible,
                compatibility_label=label,
                route_ceiling_label="worth_human_modular_review",
                reason=reason,
            )
        )
    aggregate_label = "cross_prime_elimination_candidate"
    aggregate_reason = "No level-220 newform has a compatible branch assignment across all non-q=3 focused primes."
    aggregate_compatible = False
    if any(row.compatibility_label == "level_lowering_assumption_required" for row in records):
        aggregate_label = "level_lowering_assumption_required"
        aggregate_reason = "At least one newform row needs level-lowering justification before cross-prime compatibility can be evaluated."
    elif any(row.compatibility_label == "branch_data_insufficient" for row in records):
        aggregate_label = "branch_data_insufficient"
        aggregate_reason = "At least one newform row has missing or unclear branch data."
    elif any(row.compatibility_label == "cross_prime_survivor_exists" for row in records):
        aggregate_label = "cross_prime_survivor_exists"
        aggregate_reason = "At least one level-220 newform has a compatible branch assignment across all non-q=3 focused primes."
        aggregate_compatible = True
    if aggregate_label not in SAFE_CROSS_PRIME_COMPATIBILITY_LABELS:
        aggregate_label = "branch_data_insufficient"
        aggregate_reason = "Unexpected aggregate label was downgraded to branch_data_insufficient."
    records.append(
        CrossPrimeBranchCompatibilityRecord(
            signature="5-4-5",
            prime_set=prime_text,
            newform_index=-1,
            newform_label="all_newforms",
            allowed_branch_sets=";".join(
                f"newform_{row.newform_index}:{row.allowed_branch_sets}"
                for row in records
            ),
            eliminated_at_primes=";".join(
                f"newform_{row.newform_index}:{row.eliminated_at_primes or 'none'}"
                for row in records
            ),
            pairwise_primitive_forbidden_status="see_newform_rows",
            compatible_prime_count=sum(1 for row in records if row.compatible_branch_assignment_exists),
            incompatible_prime_count=sum(1 for row in records if not row.compatible_branch_assignment_exists),
            data_gap_count=sum(row.data_gap_count for row in records),
            level_lowering_assumption_required_count=sum(
                row.level_lowering_assumption_required_count for row in records
            ),
            compatible_branch_assignment_exists=aggregate_compatible,
            compatibility_label=aggregate_label,
            route_ceiling_label="worth_human_modular_review",
            reason=aggregate_reason,
        )
    )
    return records


def write_cross_prime_branch_compatibility_545_csv(
    path: Path,
    rows: Iterable[CrossPrimeBranchCompatibilityRecord],
) -> Path:
    """Write `cross_prime_branch_compatibility_545.csv` rows."""
    _write_csv(path, [row.to_flat_dict() for row in rows])
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write focused 5-4-5 cross-prime compatibility rows.")
    parser.add_argument("--output", default="cross_prime_branch_compatibility_545.csv")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    write_cross_prime_branch_compatibility_545_csv(Path(args.output), [])
    print(Path(args.output).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
