"""Multiplicative-reduction congruence audit for focused `(5,4,5)` branches."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from .frey_reduction_diagnostics_545 import (
    FreyReductionDiagnosticRecord,
    TARGET_PRIMES_545,
    build_frey_reduction_diagnostics_545,
)
from .newform_coefficient_importer import (
    NewformCoefficientRow,
    import_level_220_newform_coefficients,
)


SAFE_MULTIPLICATIVE_CONGRUENCE_LABELS = {
    "multiplicative_branch_survives",
    "multiplicative_branch_eliminated",
    "coefficient_missing",
    "formula_missing",
    "level_lowering_assumption_required",
}


@dataclass(frozen=True)
class MultiplicativeReductionCongruenceRecord:
    """One q/mask/newform multiplicative-reduction congruence row."""

    signature: str
    level: int
    residual_modulus: int
    prime: int
    valuation_mask: str
    newform_index: int
    newform_label: str
    newform_coefficient: str
    coefficient_mod_5: str
    allowed_multiplicative_values_mod_5: str
    reduction_type: str
    formula_status: str
    level_lowering_assumption_status: str
    congruence_classification: str
    branch_eliminated: bool
    branch_survives: bool
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


def allowed_multiplicative_values_mod_5(prime: int, residual_modulus: int = 5) -> tuple[int, ...]:
    """Return the safe multiplicative values `+/-(q+1)` modulo the residual modulus."""
    value = (prime + 1) % residual_modulus
    return tuple(sorted({value, (-value) % residual_modulus}))


def _coefficient_as_int(value: str) -> int | None:
    text = value.strip()
    if not text:
        return None
    try:
        return int(text)
    except ValueError:
        return None


def _coefficient_mod_5(row: NewformCoefficientRow | None, residual_modulus: int) -> tuple[str, int | None]:
    if row is None:
        return "", None
    if row.coefficient_mod_5.strip():
        parts = [
            part.strip()
            for part in row.coefficient_mod_5.split(";")
            if part.strip().lstrip("-").isdigit()
        ]
        if parts:
            value = int(parts[0]) % residual_modulus
            return str(value), value
    coeff_int = _coefficient_as_int(row.coefficient)
    if coeff_int is not None:
        value = coeff_int % residual_modulus
        return str(value), value
    return "", None


def _newform_indices(coefficient_rows: list[NewformCoefficientRow], newform_count: int) -> tuple[int, ...]:
    indices = set(range(max(newform_count, 0)))
    indices.update(row.newform_index for row in coefficient_rows)
    if not indices:
        indices.update(range(2))
    return tuple(sorted(indices))


def _newform_label(index: int, rows: list[NewformCoefficientRow]) -> str:
    for row in rows:
        if row.newform_index == index and row.newform_label:
            return row.newform_label
    return f"newform_{index}"


def _classify(
    *,
    diagnostic: FreyReductionDiagnosticRecord,
    coefficient_row: NewformCoefficientRow | None,
    coefficient_mod_5: int | None,
    allowed_values: tuple[int, ...],
    level_lowering_congruence_available: bool,
) -> tuple[str, bool, bool, str, str, str]:
    if diagnostic.reduction_type != "multiplicative_reduction":
        return (
            "formula_missing",
            False,
            False,
            diagnostic.diagnostic_status,
            "not_checked",
            "The focused invariant formulas do not currently certify multiplicative reduction for this branch.",
        )
    if coefficient_row is None or coefficient_mod_5 is None:
        return (
            "coefficient_missing",
            False,
            False,
            diagnostic.diagnostic_status,
            "not_checked",
            "No usable level-220 coefficient modulo 5 is available for this q and newform.",
        )
    if not level_lowering_congruence_available:
        return (
            "level_lowering_assumption_required",
            False,
            False,
            diagnostic.diagnostic_status,
            "required",
            "The multiplicative congruence was not applied because the level-lowering condition still needs justification.",
        )
    if coefficient_mod_5 in set(allowed_values):
        return (
            "multiplicative_branch_survives",
            False,
            True,
            diagnostic.diagnostic_status,
            "used_as_conditional_audit",
            "The newform coefficient is congruent to one of the allowed multiplicative values modulo 5.",
        )
    return (
        "multiplicative_branch_eliminated",
        True,
        False,
        diagnostic.diagnostic_status,
        "used_as_conditional_audit",
        "The newform coefficient is not congruent to +/-(q+1) modulo 5 for this multiplicative branch.",
    )


def build_multiplicative_reduction_congruences_545(
    coefficient_rows: Iterable[NewformCoefficientRow] | None = None,
    diagnostic_rows: Iterable[FreyReductionDiagnosticRecord] | None = None,
    *,
    newform_count: int = 2,
    target_primes: tuple[int, ...] = TARGET_PRIMES_545,
    residual_modulus: int = 5,
    level_lowering_congruence_available: bool = True,
) -> list[MultiplicativeReductionCongruenceRecord]:
    """Compare level-220 coefficients with `+/-(q+1)` for focused multiplicative branches."""
    coefficients = list(coefficient_rows or [])
    diagnostics = list(diagnostic_rows) if diagnostic_rows is not None else build_frey_reduction_diagnostics_545()
    coefficient_by_key = {
        (row.prime, row.newform_index): row
        for row in coefficients
        if row.level == 220 and row.prime in set(target_primes)
    }
    diagnostics_by_key = {
        (row.prime, row.valuation_mask): row
        for row in diagnostics
        if row.prime in set(target_primes)
    }
    indices = _newform_indices(coefficients, newform_count)
    records: list[MultiplicativeReductionCongruenceRecord] = []
    for prime, mask in sorted(diagnostics_by_key):
        diagnostic = diagnostics_by_key[(prime, mask)]
        allowed_values = allowed_multiplicative_values_mod_5(prime, residual_modulus)
        allowed_text = ";".join(str(item) for item in allowed_values)
        for newform_index in indices:
            coefficient_row = coefficient_by_key.get((prime, newform_index))
            coefficient_mod_text, coefficient_mod_value = _coefficient_mod_5(coefficient_row, residual_modulus)
            classification, eliminated, survives, formula_status, assumption_status, reason = _classify(
                diagnostic=diagnostic,
                coefficient_row=coefficient_row,
                coefficient_mod_5=coefficient_mod_value,
                allowed_values=allowed_values,
                level_lowering_congruence_available=level_lowering_congruence_available,
            )
            if classification not in SAFE_MULTIPLICATIVE_CONGRUENCE_LABELS:
                classification = "formula_missing"
                eliminated = False
                survives = False
                reason = "Unexpected multiplicative congruence label was downgraded to formula_missing."
            records.append(
                MultiplicativeReductionCongruenceRecord(
                    signature="5-4-5",
                    level=220,
                    residual_modulus=residual_modulus,
                    prime=prime,
                    valuation_mask=mask,
                    newform_index=newform_index,
                    newform_label=_newform_label(newform_index, coefficients),
                    newform_coefficient=coefficient_row.coefficient if coefficient_row else "",
                    coefficient_mod_5=coefficient_mod_text,
                    allowed_multiplicative_values_mod_5=allowed_text,
                    reduction_type=diagnostic.reduction_type,
                    formula_status=formula_status,
                    level_lowering_assumption_status=assumption_status,
                    congruence_classification=classification,
                    branch_eliminated=eliminated,
                    branch_survives=survives,
                    route_ceiling_label="worth_human_modular_review",
                    reason=reason,
                )
            )
    return records


def write_multiplicative_reduction_congruence_545_csv(
    path: Path,
    rows: Iterable[MultiplicativeReductionCongruenceRecord] | None = None,
) -> Path:
    """Write `multiplicative_reduction_congruence_545.csv` rows to `path`."""
    record_rows = list(rows) if rows is not None else build_multiplicative_reduction_congruences_545()
    _write_csv(path, [row.to_flat_dict() for row in record_rows])
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write focused 5-4-5 multiplicative congruence rows.")
    parser.add_argument("--coefficient-json", default="level_220_newform_coefficients.json")
    parser.add_argument("--output", default="multiplicative_reduction_congruence_545.csv")
    parser.add_argument(
        "--require-level-lowering-proof",
        action="store_true",
        help="Do not apply the congruence; emit level_lowering_assumption_required rows.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    summary, coefficient_rows = import_level_220_newform_coefficients(Path(args.coefficient_json))
    rows = build_multiplicative_reduction_congruences_545(
        coefficient_rows,
        newform_count=summary.newform_count or 2,
        level_lowering_congruence_available=not args.require_level_lowering_proof,
    )
    write_multiplicative_reduction_congruence_545_csv(Path(args.output), rows)
    print(Path(args.output).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
