"""Audit removal of primes dividing ABC for the focused `(5,4,5)` route."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SAFE_ABC_PRIME_REMOVAL_LABELS = {
    "abc_prime_removal_gap",
    "removed_if_level_lowering_verified",
    "needs_human_review",
}


@dataclass(frozen=True)
class ABCPrimeRemovalAuditRecord:
    """One row for a prime dividing A, B, or C."""

    signature: str
    prime_case: str
    prime_symbol: str
    appears_in_discriminant: bool
    discriminant_valuation: str
    appears_in_conductor_before_lowering: str
    expected_reduction_before_lowering: str
    expected_conductor_exponent_before_lowering: str
    required_level_lowering_condition: str
    residual_irreducibility_required: bool
    minimality_required: bool
    removal_label: str
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


def _safe(row: ABCPrimeRemovalAuditRecord) -> ABCPrimeRemovalAuditRecord:
    if row.removal_label in SAFE_ABC_PRIME_REMOVAL_LABELS:
        return row
    return ABCPrimeRemovalAuditRecord(
        signature=row.signature,
        prime_case=row.prime_case,
        prime_symbol=row.prime_symbol,
        appears_in_discriminant=row.appears_in_discriminant,
        discriminant_valuation=row.discriminant_valuation,
        appears_in_conductor_before_lowering=row.appears_in_conductor_before_lowering,
        expected_reduction_before_lowering=row.expected_reduction_before_lowering,
        expected_conductor_exponent_before_lowering=row.expected_conductor_exponent_before_lowering,
        required_level_lowering_condition=row.required_level_lowering_condition,
        residual_irreducibility_required=row.residual_irreducibility_required,
        minimality_required=row.minimality_required,
        removal_label="needs_human_review",
        route_ceiling_label=row.route_ceiling_label,
        required_human_check="Unexpected ABC-removal label was downgraded to needs_human_review.",
    )


def build_abc_prime_removal_audit_545() -> list[ABCPrimeRemovalAuditRecord]:
    """Build rows for primes dividing A, B, and C."""
    rows = [
        ABCPrimeRemovalAuditRecord(
            signature="5-4-5",
            prime_case="ell_divides_A",
            prime_symbol="ell | A",
            appears_in_discriminant=True,
            discriminant_valuation="10*v_ell(A)",
            appears_in_conductor_before_lowering="expected_yes_if_ell_not_in_{2,5,11}",
            expected_reduction_before_lowering="multiplicative under v_ell(c4)=0",
            expected_conductor_exponent_before_lowering="1 away from 2,5,11 if local minimality holds",
            required_level_lowering_condition="Show the residual representation is unramified or removable at ell under the applicable level-lowering theorem.",
            residual_irreducibility_required=True,
            minimality_required=True,
            removal_label="abc_prime_removal_gap",
            route_ceiling_label="worth_human_modular_review",
            required_human_check="Prove the local minimality and level-lowering hypotheses for every prime dividing A.",
        ),
        ABCPrimeRemovalAuditRecord(
            signature="5-4-5",
            prime_case="ell_divides_B",
            prime_symbol="ell | B",
            appears_in_discriminant=True,
            discriminant_valuation="8*v_ell(B)",
            appears_in_conductor_before_lowering="expected_yes_if_ell_not_in_{2,5,11}",
            expected_reduction_before_lowering="multiplicative under v_ell(c4)=0",
            expected_conductor_exponent_before_lowering="1 away from 2,5,11 if local minimality holds",
            required_level_lowering_condition="Show the residual representation is unramified or removable at ell under the applicable level-lowering theorem.",
            residual_irreducibility_required=True,
            minimality_required=True,
            removal_label="abc_prime_removal_gap",
            route_ceiling_label="worth_human_modular_review",
            required_human_check="Prove the local minimality and level-lowering hypotheses for every prime dividing B.",
        ),
        ABCPrimeRemovalAuditRecord(
            signature="5-4-5",
            prime_case="ell_divides_C",
            prime_symbol="ell | C",
            appears_in_discriminant=True,
            discriminant_valuation="10*v_ell(C)",
            appears_in_conductor_before_lowering="expected_yes_if_ell_not_in_{2,5,11}",
            expected_reduction_before_lowering="multiplicative under A^5 + B^4 == 0 mod ell and v_ell(c4)=0",
            expected_conductor_exponent_before_lowering="1 away from 2,5,11 if local minimality holds",
            required_level_lowering_condition="Show the residual representation is unramified or removable at ell under the applicable level-lowering theorem.",
            residual_irreducibility_required=True,
            minimality_required=True,
            removal_label="abc_prime_removal_gap",
            route_ceiling_label="worth_human_modular_review",
            required_human_check="Prove the local minimality and level-lowering hypotheses for every prime dividing C.",
        ),
    ]
    return [_safe(row) for row in rows]


def abc_prime_removal_audit_545_markdown(rows: Iterable[ABCPrimeRemovalAuditRecord]) -> str:
    """Render the ABC-prime removal audit."""
    row_list = list(rows)
    gap_count = sum(1 for row in row_list if row.removal_label == "abc_prime_removal_gap")
    lines = [
        "# ABC Prime Removal Audit For `(5,4,5)`",
        "",
        f"- ABC-prime removal gaps: `{gap_count}`.",
        "- Primes dividing A, B, or C appear in the displayed discriminant and cannot simply disappear from the comparison level without a level-lowering argument.",
        "",
        "| prime case | in Delta | v(Delta) | pre-lowering conductor | reduction | exponent before lowering | removal label | required condition |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in row_list:
        lines.append(
            f"| `{row.prime_symbol}` | `{row.appears_in_discriminant}` | `{row.discriminant_valuation}` | "
            f"`{row.appears_in_conductor_before_lowering}` | `{row.expected_reduction_before_lowering}` | "
            f"`{row.expected_conductor_exponent_before_lowering}` | `{row.removal_label}` | "
            f"{row.required_level_lowering_condition} |"
        )
    lines.extend(
        [
            "",
            "`abc_prime_removal_gap` means the current route has not yet justified removing those primes from the final level.",
            "",
        ]
    )
    return "\n".join(lines)


def write_abc_prime_removal_audit_545_csv(
    path: Path,
    rows: Iterable[ABCPrimeRemovalAuditRecord],
) -> Path:
    """Write `abc_prime_removal_audit_545.csv`."""
    _write_csv(path, [row.to_flat_dict() for row in rows])
    return path


def write_abc_prime_removal_audit_545_markdown(
    path: Path,
    rows: Iterable[ABCPrimeRemovalAuditRecord],
) -> Path:
    """Write `ABC_PRIME_REMOVAL_AUDIT_545.md`."""
    path.write_text(abc_prime_removal_audit_545_markdown(rows), encoding="utf-8")
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write focused 5-4-5 ABC-prime removal audit rows.")
    parser.add_argument("--output", default="abc_prime_removal_audit_545.csv")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows = build_abc_prime_removal_audit_545()
    write_abc_prime_removal_audit_545_csv(Path(args.output), rows)
    print(Path(args.output).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
