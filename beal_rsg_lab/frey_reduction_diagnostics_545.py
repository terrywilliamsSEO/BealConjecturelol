"""Focused Frey-reduction diagnostics for `(5,4,5)` single masks."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from .good_prime_selector import GoodPrimeRecord


TARGET_PRIMES_545 = (3, 13, 17, 41, 61)
SINGLE_MASKS_545 = ("A_only", "B_only", "C_only")
SAFE_REDUCTION_TYPES_545 = {
    "good_reduction",
    "multiplicative_reduction",
    "additive_reduction",
    "template_unknown",
}


@dataclass(frozen=True)
class FreyInvariantFormulaAvailability:
    """Which invariant formulas are available for the displayed template."""

    discriminant_available: bool = True
    c4_available: bool = True
    c6_available: bool = True


@dataclass(frozen=True)
class FreyReductionDiagnosticRecord:
    """One valuation-based reduction diagnostic for a single-mask branch."""

    signature: str
    prime: int
    valuation_mask: str
    valuation_assumption: str
    discriminant_formula_available: bool
    c4_formula_available: bool
    c6_formula_available: bool
    discriminant_valuation: str
    c4_valuation: str
    c6_valuation: str
    discriminant_valuation_lower_bound: int | str
    c4_valuation_lower_bound: int | str
    c6_valuation_lower_bound: int | str
    reduction_type: str
    standard_trace_behavior_available: bool
    route_ceiling_label: str
    diagnostic_status: str
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


def _target_primes(
    good_prime_rows: Iterable[GoodPrimeRecord] | None,
    target_primes: tuple[int, ...],
) -> tuple[int, ...]:
    if good_prime_rows is None:
        return tuple(sorted(target_primes))
    target_set = set(target_primes)
    selected = {row.prime for row in good_prime_rows if row.selected and row.prime in target_set}
    return tuple(sorted(selected or target_set))


def _mask_valuation_data(mask: str) -> tuple[str, str, int]:
    if mask == "A_only":
        return "v_q(A)>=1; v_q(B)=v_q(C)=0", "10*v_q(A)", 10
    if mask == "B_only":
        return "v_q(B)>=1; v_q(A)=v_q(C)=0", "8*v_q(B)", 8
    if mask == "C_only":
        return "v_q(C)>=1; v_q(A)=v_q(B)=0", "10*v_q(C)", 10
    raise ValueError(f"unsupported single mask: {mask}")


def _classify_from_valuations(
    *,
    formulas: FreyInvariantFormulaAvailability,
    discriminant_lower_bound: int,
    c4_valuation: str,
) -> tuple[str, bool, str, str]:
    if not formulas.discriminant_available:
        return (
            "template_unknown",
            False,
            "missing_invariant_formula",
            "The discriminant formula is unavailable, so the reduction type is not inferred.",
        )
    if not formulas.c4_available:
        return (
            "template_unknown",
            False,
            "missing_invariant_formula",
            "The c4 formula is unavailable, so the Tate-relevant valuation test is not inferred.",
        )
    if discriminant_lower_bound == 0:
        return (
            "good_reduction",
            True,
            "valuation_classified",
            "The displayed invariant valuations have v_q(Delta)=0.",
        )
    if c4_valuation == "0":
        return (
            "multiplicative_reduction",
            False,
            "valuation_classified",
            "The displayed template has v_q(Delta)>0 and v_q(c4)=0, so the valuation diagnostic is multiplicative.",
        )
    return (
        "additive_reduction",
        False,
        "valuation_classified",
        "The displayed template has v_q(Delta)>0 and positive c4 valuation, so the valuation diagnostic is additive.",
    )


def build_frey_reduction_diagnostics_545(
    good_prime_rows: Iterable[GoodPrimeRecord] | None = None,
    *,
    target_primes: tuple[int, ...] = TARGET_PRIMES_545,
    masks: tuple[str, ...] = SINGLE_MASKS_545,
    formulas: FreyInvariantFormulaAvailability = FreyInvariantFormulaAvailability(),
) -> list[FreyReductionDiagnosticRecord]:
    """Build valuation diagnostics for the focused eliminating good-prime single-mask branches."""
    records: list[FreyReductionDiagnosticRecord] = []
    for prime in _target_primes(good_prime_rows, target_primes):
        for mask in masks:
            assumption, discriminant_valuation, discriminant_lower_bound = _mask_valuation_data(mask)
            c4_valuation = "0" if formulas.c4_available else "formula_missing"
            c6_valuation = "0" if formulas.c6_available else "formula_missing"
            c4_bound: int | str = 0 if formulas.c4_available else "unknown"
            c6_bound: int | str = 0 if formulas.c6_available else "unknown"
            reduction, standard_trace, status, reason = _classify_from_valuations(
                formulas=formulas,
                discriminant_lower_bound=discriminant_lower_bound,
                c4_valuation=c4_valuation,
            )
            if reduction not in SAFE_REDUCTION_TYPES_545:
                reduction = "template_unknown"
                standard_trace = False
                status = "safe_downgrade"
                reason = "Unexpected reduction label was downgraded to template_unknown."
            records.append(
                FreyReductionDiagnosticRecord(
                    signature="5-4-5",
                    prime=prime,
                    valuation_mask=mask,
                    valuation_assumption=assumption,
                    discriminant_formula_available=formulas.discriminant_available,
                    c4_formula_available=formulas.c4_available,
                    c6_formula_available=formulas.c6_available,
                    discriminant_valuation=(
                        discriminant_valuation if formulas.discriminant_available else "formula_missing"
                    ),
                    c4_valuation=c4_valuation,
                    c6_valuation=c6_valuation,
                    discriminant_valuation_lower_bound=(
                        discriminant_lower_bound if formulas.discriminant_available else "unknown"
                    ),
                    c4_valuation_lower_bound=c4_bound,
                    c6_valuation_lower_bound=c6_bound,
                    reduction_type=reduction,
                    standard_trace_behavior_available=standard_trace,
                    route_ceiling_label="worth_human_modular_review",
                    diagnostic_status=status,
                    reason=reason,
                )
            )
    return records


def write_frey_reduction_diagnostics_545_csv(
    path: Path,
    rows: Iterable[FreyReductionDiagnosticRecord] | None = None,
) -> Path:
    """Write `frey_reduction_diagnostics_545.csv` rows to `path`."""
    record_rows = list(rows) if rows is not None else build_frey_reduction_diagnostics_545()
    _write_csv(path, [row.to_flat_dict() for row in record_rows])
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write focused 5-4-5 Frey reduction diagnostics.")
    parser.add_argument("--output", default="frey_reduction_diagnostics_545.csv")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    write_frey_reduction_diagnostics_545_csv(Path(args.output))
    print(Path(args.output).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
