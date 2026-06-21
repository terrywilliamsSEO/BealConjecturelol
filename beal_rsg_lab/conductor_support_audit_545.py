"""Conductor-support audit for the focused `(5,4,5)` route."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SAFE_CONDUCTOR_SUPPORT_LABELS = {
    "verified_symbolic",
    "expected_level_prime",
    "expected_lowered_away",
    "needs_human_review",
    "conductor_support_gap",
}


@dataclass(frozen=True)
class ConductorSupportAuditRecord:
    """One conductor-support row."""

    signature: str
    support_source: str
    prime_or_symbol: str
    appears_in_discriminant: bool
    appears_in_candidate_level_220: bool
    candidate_level_exponent: str
    expected_level_behavior: str
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


def build_conductor_support_audit_545() -> list[ConductorSupportAuditRecord]:
    """Return the expected bad-prime support audit for `(5,4,5)`."""
    rows = [
        ConductorSupportAuditRecord(
            signature="5-4-5",
            support_source="constant_discriminant_factor",
            prime_or_symbol="2",
            appears_in_discriminant=True,
            appears_in_candidate_level_220=True,
            candidate_level_exponent="2",
            expected_level_behavior="expected_remains_with_exact_exponent_unknown",
            audit_label="needs_human_review",
            route_ceiling_label="worth_human_modular_review",
            required_human_check="Run a 2-adic minimal-model and conductor exponent calculation for the exact Frey model.",
        ),
        ConductorSupportAuditRecord(
            signature="5-4-5",
            support_source="residual_prime_and_exponent_prime",
            prime_or_symbol="5",
            appears_in_discriminant=False,
            appears_in_candidate_level_220=True,
            candidate_level_exponent="1",
            expected_level_behavior="expected_remains_if_residual_ramification_requires_it",
            audit_label="needs_human_review",
            route_ceiling_label="worth_human_modular_review",
            required_human_check="Justify the mod-5 representation, ramification at 5, and the exact conductor exponent.",
        ),
        ConductorSupportAuditRecord(
            signature="5-4-5",
            support_source="route_audit_level_prime",
            prime_or_symbol="11",
            appears_in_discriminant=False,
            appears_in_candidate_level_220=True,
            candidate_level_exponent="1",
            expected_level_behavior="not_template_forced_needs_justification",
            audit_label="conductor_support_gap",
            route_ceiling_label="worth_human_modular_review",
            required_human_check="Explain why 11 remains in the true conductor or lowered level rather than only in the exploratory route level.",
        ),
        ConductorSupportAuditRecord(
            signature="5-4-5",
            support_source="discriminant_factor_A",
            prime_or_symbol="p | A",
            appears_in_discriminant=True,
            appears_in_candidate_level_220=False,
            candidate_level_exponent="0",
            expected_level_behavior="expected_lowered_away_if_level_lowering_hypotheses_hold",
            audit_label="expected_lowered_away",
            route_ceiling_label="worth_human_modular_review",
            required_human_check="Compute local conductor exponents for primes dividing A and verify the level-lowering removal hypotheses.",
        ),
        ConductorSupportAuditRecord(
            signature="5-4-5",
            support_source="discriminant_factor_B",
            prime_or_symbol="p | B",
            appears_in_discriminant=True,
            appears_in_candidate_level_220=False,
            candidate_level_exponent="0",
            expected_level_behavior="expected_lowered_away_if_level_lowering_hypotheses_hold",
            audit_label="expected_lowered_away",
            route_ceiling_label="worth_human_modular_review",
            required_human_check="Compute local conductor exponents for primes dividing B and verify the level-lowering removal hypotheses.",
        ),
        ConductorSupportAuditRecord(
            signature="5-4-5",
            support_source="discriminant_factor_C",
            prime_or_symbol="p | C",
            appears_in_discriminant=True,
            appears_in_candidate_level_220=False,
            candidate_level_exponent="0",
            expected_level_behavior="expected_lowered_away_if_level_lowering_hypotheses_hold",
            audit_label="expected_lowered_away",
            route_ceiling_label="worth_human_modular_review",
            required_human_check="Compute local conductor exponents for primes dividing C and verify the level-lowering removal hypotheses.",
        ),
    ]
    return [
        row
        if row.audit_label in SAFE_CONDUCTOR_SUPPORT_LABELS
        else ConductorSupportAuditRecord(
            signature=row.signature,
            support_source=row.support_source,
            prime_or_symbol=row.prime_or_symbol,
            appears_in_discriminant=row.appears_in_discriminant,
            appears_in_candidate_level_220=row.appears_in_candidate_level_220,
            candidate_level_exponent=row.candidate_level_exponent,
            expected_level_behavior=row.expected_level_behavior,
            audit_label="needs_human_review",
            route_ceiling_label=row.route_ceiling_label,
            required_human_check="Unexpected conductor label was downgraded to needs_human_review.",
        )
        for row in rows
    ]


def conductor_support_audit_545_markdown(rows: Iterable[ConductorSupportAuditRecord]) -> str:
    """Render the conductor-support audit."""
    row_list = list(rows)
    level_primes = [row.prime_or_symbol for row in row_list if row.appears_in_candidate_level_220]
    disappearing = [row.prime_or_symbol for row in row_list if row.expected_level_behavior.startswith("expected_lowered")]
    lines = [
        "# Conductor Support Audit For `(5,4,5)`",
        "",
        "Candidate level: `220 = 2^2 * 5 * 11`.",
        f"- Candidate level primes: `{';'.join(level_primes)}`.",
        f"- Prime symbols expected to disappear by level lowering: `{';'.join(disappearing)}`.",
        "",
        "| source | prime/symbol | in Delta | in level 220 | exponent | expected behavior | label | required check |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in row_list:
        lines.append(
            f"| `{row.support_source}` | `{row.prime_or_symbol}` | `{row.appears_in_discriminant}` | "
            f"`{row.appears_in_candidate_level_220}` | `{row.candidate_level_exponent}` | "
            f"`{row.expected_level_behavior}` | `{row.audit_label}` | {row.required_human_check} |"
        )
    lines.extend(
        [
            "",
            "The exact conductor is not established by this table. The table identifies which local conductor and level-lowering checks a human must supply.",
            "",
        ]
    )
    return "\n".join(lines)


def write_conductor_support_audit_545_csv(
    path: Path,
    rows: Iterable[ConductorSupportAuditRecord],
) -> Path:
    """Write `conductor_support_audit_545.csv`."""
    _write_csv(path, [row.to_flat_dict() for row in rows])
    return path


def write_conductor_support_audit_545_markdown(
    path: Path,
    rows: Iterable[ConductorSupportAuditRecord],
) -> Path:
    """Write `CONDUCTOR_SUPPORT_AUDIT_545.md`."""
    path.write_text(conductor_support_audit_545_markdown(rows), encoding="utf-8")
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write focused 5-4-5 conductor support audit rows.")
    parser.add_argument("--output", default="conductor_support_audit_545.csv")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows = build_conductor_support_audit_545()
    write_conductor_support_audit_545_csv(Path(args.output), rows)
    print(Path(args.output).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
