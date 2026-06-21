"""Conductor-exponent model for the focused `(5,4,5)` Frey route."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SAFE_REDUCTION_LABELS_545 = {
    "good",
    "multiplicative",
    "additive",
    "unknown",
}

SAFE_CONDUCTOR_EXPONENT_MODEL_LABELS = {
    "symbolic_multiplicative_model",
    "needs_human_tate_check",
    "bad_prime_tate_gap",
}


@dataclass(frozen=True)
class ConductorExponentModelRecord:
    """One symbolic conductor-exponent row."""

    signature: str
    prime_case: str
    prime_symbol: str
    c4_valuation: str
    c6_valuation: str
    discriminant_valuation: str
    expected_reduction: str
    conductor_exponent_estimate: str
    estimate_scope: str
    audit_label: str
    route_ceiling_label: str
    required_human_check: str

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


def _safe(row: ConductorExponentModelRecord) -> ConductorExponentModelRecord:
    reduction = row.expected_reduction
    audit_label = row.audit_label
    human_check = row.required_human_check
    if reduction not in SAFE_REDUCTION_LABELS_545:
        reduction = "unknown"
        audit_label = "needs_human_tate_check"
        human_check = "Unexpected reduction label was downgraded to a human Tate-algorithm check."
    if audit_label not in SAFE_CONDUCTOR_EXPONENT_MODEL_LABELS:
        audit_label = "needs_human_tate_check"
        human_check = "Unexpected conductor-exponent label was downgraded to a human Tate-algorithm check."
    return ConductorExponentModelRecord(
        signature=row.signature,
        prime_case=row.prime_case,
        prime_symbol=row.prime_symbol,
        c4_valuation=row.c4_valuation,
        c6_valuation=row.c6_valuation,
        discriminant_valuation=row.discriminant_valuation,
        expected_reduction=reduction,
        conductor_exponent_estimate=row.conductor_exponent_estimate,
        estimate_scope=row.estimate_scope,
        audit_label=audit_label,
        route_ceiling_label=row.route_ceiling_label,
        required_human_check=human_check,
    )


def build_conductor_exponent_model_545() -> list[ConductorExponentModelRecord]:
    """Build conservative symbolic valuation rows for the displayed Frey curve."""
    rows = [
        ConductorExponentModelRecord(
            signature="5-4-5",
            prime_case="ell_divides_A",
            prime_symbol="ell | A, ell not in {2,5,11}",
            c4_valuation="0 under primitivity",
            c6_valuation="0 under primitivity",
            discriminant_valuation="10*v_ell(A)",
            expected_reduction="multiplicative",
            conductor_exponent_estimate="1",
            estimate_scope="safe only for odd ell away from 2,5,11 with the displayed integral model and v_ell(c4)=0",
            audit_label="symbolic_multiplicative_model",
            route_ceiling_label="worth_human_modular_review",
            required_human_check="Verify local minimality and the level-lowering removal condition for primes dividing A.",
        ),
        ConductorExponentModelRecord(
            signature="5-4-5",
            prime_case="ell_divides_B",
            prime_symbol="ell | B, ell not in {2,5,11}",
            c4_valuation="0 under primitivity",
            c6_valuation="0 under primitivity",
            discriminant_valuation="8*v_ell(B)",
            expected_reduction="multiplicative",
            conductor_exponent_estimate="1",
            estimate_scope="safe only for odd ell away from 2,5,11 with the displayed integral model and v_ell(c4)=0",
            audit_label="symbolic_multiplicative_model",
            route_ceiling_label="worth_human_modular_review",
            required_human_check="Verify local minimality and the level-lowering removal condition for primes dividing B.",
        ),
        ConductorExponentModelRecord(
            signature="5-4-5",
            prime_case="ell_divides_C",
            prime_symbol="ell | C, ell not in {2,5,11}",
            c4_valuation="0 using A^5 + B^4 == 0 mod ell and primitivity",
            c6_valuation="0 using A^5 + B^4 == 0 mod ell and primitivity",
            discriminant_valuation="10*v_ell(C)",
            expected_reduction="multiplicative",
            conductor_exponent_estimate="1",
            estimate_scope="safe only for odd ell away from 2,5,11 with the displayed integral model and v_ell(c4)=0",
            audit_label="symbolic_multiplicative_model",
            route_ceiling_label="worth_human_modular_review",
            required_human_check="Verify local minimality and the level-lowering removal condition for primes dividing C.",
        ),
        ConductorExponentModelRecord(
            signature="5-4-5",
            prime_case="ell_equals_2",
            prime_symbol="2",
            c4_valuation="4 + v_2(A^10 + A^5*B^4 + B^8)",
            c6_valuation="5 + v_2((A^5 - B^4)*(2*A^10 + 5*A^5*B^4 + 2*B^8))",
            discriminant_valuation="4 + 10*v_2(A) + 8*v_2(B) + 10*v_2(C)",
            expected_reduction="unknown",
            conductor_exponent_estimate="unknown",
            estimate_scope="2-adic minimization is not supplied by the symbolic template",
            audit_label="needs_human_tate_check",
            route_ceiling_label="worth_human_modular_review",
            required_human_check="Run the 2-adic Tate algorithm and derive the exact conductor exponent.",
        ),
        ConductorExponentModelRecord(
            signature="5-4-5",
            prime_case="ell_equals_5",
            prime_symbol="5",
            c4_valuation="v_5(16*(A^10 + A^5*B^4 + B^8))",
            c6_valuation="v_5(32*(A^5 - B^4)*(2*A^10 + 5*A^5*B^4 + 2*B^8))",
            discriminant_valuation="10*v_5(A) + 8*v_5(B) + 10*v_5(C)",
            expected_reduction="unknown",
            conductor_exponent_estimate="unknown",
            estimate_scope="residual-prime conductor behavior is not derived by the symbolic template",
            audit_label="needs_human_tate_check",
            route_ceiling_label="worth_human_modular_review",
            required_human_check="Analyze the mod-5 residual representation and the 5-adic conductor exponent.",
        ),
        ConductorExponentModelRecord(
            signature="5-4-5",
            prime_case="ell_equals_11",
            prime_symbol="11",
            c4_valuation="v_11(16*(A^10 + A^5*B^4 + B^8))",
            c6_valuation="v_11(32*(A^5 - B^4)*(2*A^10 + 5*A^5*B^4 + 2*B^8))",
            discriminant_valuation="10*v_11(A) + 8*v_11(B) + 10*v_11(C)",
            expected_reduction="unknown",
            conductor_exponent_estimate="unknown",
            estimate_scope="11 is not forced by the displayed discriminant unless 11 divides ABC",
            audit_label="needs_human_tate_check",
            route_ceiling_label="worth_human_modular_review",
            required_human_check="Decide whether 11 has genuine conductor or lowered-level provenance.",
        ),
    ]
    return [_safe(row) for row in rows]


def conductor_exponent_model_545_markdown(rows: Iterable[ConductorExponentModelRecord]) -> str:
    """Render the conductor-exponent model."""
    row_list = list(rows)
    uncertain = ";".join(row.prime_symbol for row in row_list if row.audit_label == "needs_human_tate_check")
    lines = [
        "# Conductor Exponent Model For `(5,4,5)`",
        "",
        "Frey template:",
        "",
        "```text",
        "E: y^2 = x(x - A^5)(x + B^4)",
        "c4 = 16*(A^10 + A^5*B^4 + B^8)",
        "c6 = 32*(A^5 - B^4)*(2*A^10 + 5*A^5*B^4 + 2*B^8)",
        "Delta = 16*A^10*B^8*C^10",
        "```",
        "",
        f"- Uncertain Tate/conductor cases: `{uncertain or 'none'}`.",
        "- Generic odd primes dividing A, B, or C are modeled as multiplicative before level lowering when v_ell(c4)=0.",
        "- Bad-prime exponents at 2, 5, and 11 are not derived here and stay human-review obligations.",
        "",
        "| prime case | v(c4) | v(c6) | v(Delta) | reduction | conductor exponent estimate | label | required check |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in row_list:
        lines.append(
            f"| `{row.prime_symbol}` | `{row.c4_valuation}` | `{row.c6_valuation}` | "
            f"`{row.discriminant_valuation}` | `{row.expected_reduction}` | "
            f"`{row.conductor_exponent_estimate}` | `{row.audit_label}` | {row.required_human_check} |"
        )
    lines.extend(
        [
            "",
            "This model is a provenance audit. It does not replace minimal-model or level-lowering calculations.",
            "",
        ]
    )
    return "\n".join(lines)


def write_conductor_exponent_model_545_csv(
    path: Path,
    rows: Iterable[ConductorExponentModelRecord],
) -> Path:
    """Write `conductor_exponent_model_545.csv`."""
    _write_csv(path, [row.to_flat_dict() for row in rows])
    return path


def write_conductor_exponent_model_545_markdown(
    path: Path,
    rows: Iterable[ConductorExponentModelRecord],
) -> Path:
    """Write `CONDUCTOR_EXPONENT_MODEL_545.md`."""
    path.write_text(conductor_exponent_model_545_markdown(rows), encoding="utf-8")
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write focused 5-4-5 conductor exponent model rows.")
    parser.add_argument("--output", default="conductor_exponent_model_545.csv")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows = build_conductor_exponent_model_545()
    write_conductor_exponent_model_545_csv(Path(args.output), rows)
    print(Path(args.output).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
