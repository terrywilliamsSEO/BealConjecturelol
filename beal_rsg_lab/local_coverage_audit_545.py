"""Local coverage audit for the focused `(5,4,5)` trace comparison."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from .frey_trace_possibility_545 import FreyTracePossibilityRecord
from .good_prime_selector import GoodPrimeRecord


ZERO_MASKS = ("A_only", "B_only", "C_only", "AB", "AC", "BC", "ABC")


@dataclass(frozen=True)
class LocalCoverageAuditRecord:
    """Coverage counts for one good prime."""

    signature: str
    prime: int
    residue_unit_solution_count: int
    zero_A_only_count: int
    zero_B_only_count: int
    zero_C_only_count: int
    zero_AB_count: int
    zero_AC_count: int
    zero_BC_count: int
    zero_ABC_count: int
    zero_support_solution_count: int
    power_image_unit_survivor_count: int
    nonsingular_frey_reduction_count: int
    singular_or_bad_reduction_count: int
    cases_excluded_from_trace_comparison: int
    trace_comparison_assumes_q_not_dividing_ABC: bool
    coverage_label: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def _zero_mask(a_value: int, b_value: int, c_value: int) -> str:
    zeros = "".join(name for name, value in (("A", a_value), ("B", b_value), ("C", c_value)) if value == 0)
    if not zeros:
        return "none"
    return {
        "A": "A_only",
        "B": "B_only",
        "C": "C_only",
        "AB": "AB",
        "AC": "AC",
        "BC": "BC",
        "ABC": "ABC",
    }[zeros]


def _residue_counts(prime: int) -> dict[str, int]:
    counts = {"none": 0, **{mask: 0 for mask in ZERO_MASKS}}
    fifth = [pow(value, 5, prime) for value in range(prime)]
    fourth = [pow(value, 4, prime) for value in range(prime)]
    for a_value in range(prime):
        a_pow = fifth[a_value]
        for b_value in range(prime):
            left = (a_pow + fourth[b_value]) % prime
            for c_value in range(prime):
                if left != fifth[c_value]:
                    continue
                counts[_zero_mask(a_value, b_value, c_value)] += 1
    return counts


def build_local_coverage_audit_545(
    good_prime_rows: Iterable[GoodPrimeRecord],
    frey_trace_rows: Iterable[FreyTracePossibilityRecord],
) -> list[LocalCoverageAuditRecord]:
    """Audit which local cases are covered by the current unit trace comparison."""
    frey_by_prime = {row.prime: row for row in frey_trace_rows}
    records: list[LocalCoverageAuditRecord] = []
    for good_row in sorted((row for row in good_prime_rows if row.selected), key=lambda row: row.prime):
        counts = _residue_counts(good_row.prime)
        frey_row = frey_by_prime.get(good_row.prime)
        zero_total = sum(counts[mask] for mask in ZERO_MASKS)
        nonsingular = frey_row.nonsingular_curve_count if frey_row else 0
        singular = frey_row.singular_skipped_count if frey_row else 0
        label = "local_coverage_gap" if zero_total or singular else "unit_cases_covered"
        records.append(
            LocalCoverageAuditRecord(
                signature="5-4-5",
                prime=good_row.prime,
                residue_unit_solution_count=counts["none"],
                zero_A_only_count=counts["A_only"],
                zero_B_only_count=counts["B_only"],
                zero_C_only_count=counts["C_only"],
                zero_AB_count=counts["AB"],
                zero_AC_count=counts["AC"],
                zero_BC_count=counts["BC"],
                zero_ABC_count=counts["ABC"],
                zero_support_solution_count=zero_total,
                power_image_unit_survivor_count=frey_row.survivor_triple_count if frey_row else 0,
                nonsingular_frey_reduction_count=nonsingular,
                singular_or_bad_reduction_count=singular,
                cases_excluded_from_trace_comparison=zero_total + singular,
                trace_comparison_assumes_q_not_dividing_ABC=True,
                coverage_label=label,
            )
        )
    return records


def local_coverage_audit_markdown(rows: Iterable[LocalCoverageAuditRecord]) -> str:
    """Render a Markdown local coverage audit."""
    row_list = list(rows)
    gap_count = sum(1 for row in row_list if row.coverage_label == "local_coverage_gap")
    lines = [
        "# Local Coverage Audit For `(5,4,5)`",
        "",
        "The current good-prime trace comparison enumerates unit power-image triples. It assumes the selected prime does not divide `ABC`.",
        "",
        f"- Primes with local coverage gaps: `{gap_count}` of `{len(row_list)}`.",
        "",
        "| q | unit residue cases | zero-support cases | power-image unit survivors | nonsingular Frey reductions | excluded cases | label |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    if not row_list:
        lines.append("| none | 0 | 0 | 0 | 0 | 0 | local_coverage_gap |")
    for row in row_list:
        lines.append(
            f"| {row.prime} | {row.residue_unit_solution_count} | {row.zero_support_solution_count} | "
            f"{row.power_image_unit_survivor_count} | {row.nonsingular_frey_reduction_count} | "
            f"{row.cases_excluded_from_trace_comparison} | `{row.coverage_label}` |"
        )
    lines.extend(
        [
            "",
            "A `local_coverage_gap` means the trace packet still needs a human argument handling reductions with `q | A`, `q | B`, or `q | C`, or showing those cases are irrelevant for the intended good-prime comparison.",
            "",
        ]
    )
    return "\n".join(lines)
