"""Bad-prime Tate-algorithm checklist for the focused `(5,4,5)` route."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SAFE_BAD_PRIME_TATE_LABELS = {
    "available_symbolic_valuation",
    "assumed_pending_tate_algorithm",
    "missing_local_analysis",
    "blocks_conductor_claim",
}


@dataclass(frozen=True)
class BadPrimeTateChecklistRecord:
    """One bad-prime local-analysis obligation."""

    signature: str
    prime: int
    candidate_level_exponent: int
    discriminant_valuation_formula: str
    c4_valuation_formula: str
    c6_valuation_formula: str
    reduction_type_status: str
    required_tate_checks: str
    conductor_gap: str
    audit_label: str
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


def build_bad_prime_tate_checklist_545() -> list[BadPrimeTateChecklistRecord]:
    """Return required local checks at 2, 5, and 11."""
    rows = [
        BadPrimeTateChecklistRecord(
            signature="5-4-5",
            prime=2,
            candidate_level_exponent=2,
            discriminant_valuation_formula="4 + 10*v_2(A) + 8*v_2(B) + 10*v_2(C)",
            c4_valuation_formula="v_2(16*(A^10 + A^5*B^4 + B^8))",
            c6_valuation_formula="v_2(32*(A^5 - B^4)*(2*A^10 + 5*A^5*B^4 + 2*B^8))",
            reduction_type_status="missing_tate_algorithm",
            required_tate_checks="Find a minimal integral model; run the full 2-adic Tate algorithm; derive the conductor exponent.",
            conductor_gap="2-adic exponent in level 220 is not proved.",
            audit_label="blocks_conductor_claim",
            route_ceiling_label="worth_human_modular_review",
        ),
        BadPrimeTateChecklistRecord(
            signature="5-4-5",
            prime=5,
            candidate_level_exponent=1,
            discriminant_valuation_formula="10*v_5(A) + 8*v_5(B) + 10*v_5(C)",
            c4_valuation_formula="v_5(16*(A^10 + A^5*B^4 + B^8))",
            c6_valuation_formula="v_5(32*(A^5 - B^4)*(2*A^10 + 5*A^5*B^4 + 2*B^8))",
            reduction_type_status="assumed_residual_prime_analysis",
            required_tate_checks="Analyze ramification at the residual prime 5 and verify the conductor exponent used after level lowering.",
            conductor_gap="The mod-5 representation and 5-adic conductor exponent are not proved.",
            audit_label="blocks_conductor_claim",
            route_ceiling_label="worth_human_modular_review",
        ),
        BadPrimeTateChecklistRecord(
            signature="5-4-5",
            prime=11,
            candidate_level_exponent=1,
            discriminant_valuation_formula="10*v_11(A) + 8*v_11(B) + 10*v_11(C)",
            c4_valuation_formula="v_11(16*(A^10 + A^5*B^4 + B^8))",
            c6_valuation_formula="v_11(32*(A^5 - B^4)*(2*A^10 + 5*A^5*B^4 + 2*B^8))",
            reduction_type_status="missing_route_support_justification",
            required_tate_checks="Decide whether 11 is genuinely in the conductor/lowered level or only entered through earlier route-audit data.",
            conductor_gap="11 is not forced by the displayed discriminant unless 11 divides ABC, so its level-220 role needs proof.",
            audit_label="blocks_conductor_claim",
            route_ceiling_label="worth_human_modular_review",
        ),
    ]
    return [
        row
        if row.audit_label in SAFE_BAD_PRIME_TATE_LABELS
        else BadPrimeTateChecklistRecord(
            signature=row.signature,
            prime=row.prime,
            candidate_level_exponent=row.candidate_level_exponent,
            discriminant_valuation_formula=row.discriminant_valuation_formula,
            c4_valuation_formula=row.c4_valuation_formula,
            c6_valuation_formula=row.c6_valuation_formula,
            reduction_type_status=row.reduction_type_status,
            required_tate_checks=row.required_tate_checks,
            conductor_gap=row.conductor_gap,
            audit_label="missing_local_analysis",
            route_ceiling_label=row.route_ceiling_label,
        )
        for row in rows
    ]


def bad_prime_tate_checklist_545_markdown(rows: Iterable[BadPrimeTateChecklistRecord]) -> str:
    """Render bad-prime checklist rows."""
    row_list = list(rows)
    lines = [
        "# Bad-Prime Tate Checklist For `(5,4,5)`",
        "",
        "These are the local checks blocking a proven conductor or lowered-level claim.",
        "",
        "| q | level exponent | v_q(Delta) | v_q(c4) | v_q(c6) | reduction status | label | gap |",
        "| ---: | ---: | --- | --- | --- | --- | --- | --- |",
    ]
    for row in row_list:
        lines.append(
            f"| {row.prime} | {row.candidate_level_exponent} | `{row.discriminant_valuation_formula}` | "
            f"`{row.c4_valuation_formula}` | `{row.c6_valuation_formula}` | "
            f"`{row.reduction_type_status}` | `{row.audit_label}` | {row.conductor_gap} |"
        )
    lines.extend(
        [
            "",
            "Human task: run or write the detailed local Tate-algorithm analysis at each listed bad prime.",
            "",
        ]
    )
    return "\n".join(lines)


def write_bad_prime_tate_checklist_545_csv(
    path: Path,
    rows: Iterable[BadPrimeTateChecklistRecord],
) -> Path:
    """Write `bad_prime_tate_checklist_545.csv`."""
    _write_csv(path, [row.to_flat_dict() for row in rows])
    return path


def write_bad_prime_tate_checklist_545_markdown(
    path: Path,
    rows: Iterable[BadPrimeTateChecklistRecord],
) -> Path:
    """Write `BAD_PRIME_TATE_CHECKLIST_545.md`."""
    path.write_text(bad_prime_tate_checklist_545_markdown(rows), encoding="utf-8")
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write focused 5-4-5 bad-prime Tate checklist rows.")
    parser.add_argument("--output", default="bad_prime_tate_checklist_545.csv")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows = build_bad_prime_tate_checklist_545()
    write_bad_prime_tate_checklist_545_csv(Path(args.output), rows)
    print(Path(args.output).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
