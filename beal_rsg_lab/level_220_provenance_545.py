"""Level-220 provenance audit for the focused `(5,4,5)` route."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SAFE_LEVEL_220_PROVENANCE_LABELS = {
    "level_2_factor_needs_tate",
    "level_5_factor_needs_residual_analysis",
    "level_11_factor_unjustified",
    "abc_primes_expected_removed",
    "level_220_heuristic_target",
}


@dataclass(frozen=True)
class Level220ProvenanceRecord:
    """One row explaining a factor or removal step behind candidate level 220."""

    signature: str
    candidate_level: int
    factor: str
    exponent_in_220: str
    factorization: str
    provenance_source: str
    formula_derived: bool
    local_audit_derived: bool
    heuristic_component: bool
    expected_role: str
    abc_prime_removal_required: bool
    assumptions_needed: str
    provenance_label: str
    route_ceiling_label: str

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


def _safe(row: Level220ProvenanceRecord) -> Level220ProvenanceRecord:
    if row.provenance_label in SAFE_LEVEL_220_PROVENANCE_LABELS:
        return row
    return Level220ProvenanceRecord(
        signature=row.signature,
        candidate_level=row.candidate_level,
        factor=row.factor,
        exponent_in_220=row.exponent_in_220,
        factorization=row.factorization,
        provenance_source=row.provenance_source,
        formula_derived=row.formula_derived,
        local_audit_derived=row.local_audit_derived,
        heuristic_component=True,
        expected_role=row.expected_role,
        abc_prime_removal_required=row.abc_prime_removal_required,
        assumptions_needed="Unexpected level-provenance label was downgraded to level_220_heuristic_target.",
        provenance_label="level_220_heuristic_target",
        route_ceiling_label=row.route_ceiling_label,
    )


def build_level_220_provenance_545() -> list[Level220ProvenanceRecord]:
    """Explain the current provenance of `220 = 2^2 * 5 * 11`."""
    factorization = "2^2 * 5 * 11"
    rows = [
        Level220ProvenanceRecord(
            signature="5-4-5",
            candidate_level=220,
            factor="220",
            exponent_in_220="2,1,1",
            factorization=factorization,
            provenance_source="route_target_aggregate",
            formula_derived=False,
            local_audit_derived=True,
            heuristic_component=True,
            expected_role="candidate comparison level only",
            abc_prime_removal_required=True,
            assumptions_needed="Derive the conductor, remove eligible ABC primes, and justify every remaining factor.",
            provenance_label="level_220_heuristic_target",
            route_ceiling_label="worth_human_modular_review",
        ),
        Level220ProvenanceRecord(
            signature="5-4-5",
            candidate_level=220,
            factor="2",
            exponent_in_220="2",
            factorization=factorization,
            provenance_source="constant_discriminant_factor_and_2_adic_model",
            formula_derived=True,
            local_audit_derived=False,
            heuristic_component=True,
            expected_role="expected bad prime with exact exponent not yet derived",
            abc_prime_removal_required=False,
            assumptions_needed="Run the 2-adic minimal-model and Tate-algorithm calculation.",
            provenance_label="level_2_factor_needs_tate",
            route_ceiling_label="worth_human_modular_review",
        ),
        Level220ProvenanceRecord(
            signature="5-4-5",
            candidate_level=220,
            factor="5",
            exponent_in_220="1",
            factorization=factorization,
            provenance_source="residual_modulus_and_5_adic_ramification",
            formula_derived=False,
            local_audit_derived=False,
            heuristic_component=True,
            expected_role="residual-prime factor needing representation-theoretic justification",
            abc_prime_removal_required=False,
            assumptions_needed="Justify mod-5 residual ramification and the target-level exponent at 5.",
            provenance_label="level_5_factor_needs_residual_analysis",
            route_ceiling_label="worth_human_modular_review",
        ),
        Level220ProvenanceRecord(
            signature="5-4-5",
            candidate_level=220,
            factor="11",
            exponent_in_220="1",
            factorization=factorization,
            provenance_source="route_audit_level_prime",
            formula_derived=False,
            local_audit_derived=True,
            heuristic_component=True,
            expected_role="not forced by the displayed discriminant unless 11 divides ABC",
            abc_prime_removal_required=False,
            assumptions_needed="Explain whether 11 belongs to the true conductor or lowered level; otherwise remove it from the target.",
            provenance_label="level_11_factor_unjustified",
            route_ceiling_label="worth_human_modular_review",
        ),
        Level220ProvenanceRecord(
            signature="5-4-5",
            candidate_level=220,
            factor="ell | ABC",
            exponent_in_220="0",
            factorization=factorization,
            provenance_source="level_lowering_removal_expectation",
            formula_derived=True,
            local_audit_derived=False,
            heuristic_component=True,
            expected_role="expected to disappear from the lowered comparison level",
            abc_prime_removal_required=True,
            assumptions_needed="Prove residual irreducibility, minimality, and the exact level-lowering hypotheses at each prime dividing ABC.",
            provenance_label="abc_primes_expected_removed",
            route_ceiling_label="worth_human_modular_review",
        ),
    ]
    return [_safe(row) for row in rows]


def level_220_provenance_545_markdown(rows: Iterable[Level220ProvenanceRecord]) -> str:
    """Render the level-220 provenance audit."""
    row_list = list(rows)
    aggregate = next((row for row in row_list if row.factor == "220"), None)
    eleven = next((row for row in row_list if row.factor == "11"), None)
    lines = [
        "# Level 220 Provenance For `(5,4,5)`",
        "",
        "Candidate level: `220 = 2^2 * 5 * 11`.",
        f"- Aggregate status: `{aggregate.provenance_label if aggregate else 'level_220_heuristic_target'}`.",
        f"- Factor 11 status: `{eleven.provenance_label if eleven else 'level_11_factor_unjustified'}`.",
        "- Level 220 remains a heuristic target until the conductor and level-lowering package is supplied.",
        "",
        "| factor | exponent | source | formula derived | local audit derived | role | label | assumptions |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in row_list:
        lines.append(
            f"| `{row.factor}` | `{row.exponent_in_220}` | `{row.provenance_source}` | "
            f"`{row.formula_derived}` | `{row.local_audit_derived}` | "
            f"`{row.expected_role}` | `{row.provenance_label}` | {row.assumptions_needed} |"
        )
    lines.extend(
        [
            "",
            "`level_11_factor_unjustified` means the current symbolic formulas do not by themselves explain the factor 11 in level 220.",
            "",
        ]
    )
    return "\n".join(lines)


def write_level_220_provenance_545_csv(
    path: Path,
    rows: Iterable[Level220ProvenanceRecord],
) -> Path:
    """Write `level_220_provenance_545.csv`."""
    _write_csv(path, [row.to_flat_dict() for row in rows])
    return path


def write_level_220_provenance_545_markdown(
    path: Path,
    rows: Iterable[Level220ProvenanceRecord],
) -> Path:
    """Write `LEVEL_220_PROVENANCE_545.md`."""
    path.write_text(level_220_provenance_545_markdown(rows), encoding="utf-8")
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write focused 5-4-5 level-220 provenance rows.")
    parser.add_argument("--output", default="level_220_provenance_545.csv")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows = build_level_220_provenance_545()
    write_level_220_provenance_545_csv(Path(args.output), rows)
    print(Path(args.output).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
