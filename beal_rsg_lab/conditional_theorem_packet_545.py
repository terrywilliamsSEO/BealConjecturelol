"""Conditional theorem packet for the focused `(5,4,5)` route."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from .assumption_dependency_graph_545 import AssumptionDependencyRecord
from .quantifier_safety_audit_545 import QuantifierSafetyAuditRecord


def _newform_rows(rows: Iterable[QuantifierSafetyAuditRecord]) -> list[QuantifierSafetyAuditRecord]:
    return [row for row in rows if row.newform_index >= 0]


def _aggregate_label(rows: Iterable[QuantifierSafetyAuditRecord]) -> str:
    for row in rows:
        if row.newform_index == -1:
            return row.quantifier_classification
    return "data_insufficient"


def _assumption_lines(rows: Iterable[AssumptionDependencyRecord]) -> list[str]:
    row_list = list(rows)
    if not row_list:
        return [
            "- Frey curve attachment for every primitive solution.",
            "- Invariant formulas and reduction classifications for the focused local branches.",
            "- Residual mod-5 irreducibility.",
            "- Level lowering to level 220.",
            "- Exhaustion of the relevant level-220 newforms and coefficient-field reductions.",
            "- Complete local branch coverage and quantifier-safety review.",
        ]
    return [
        f"- `{row.dependency_id}` {row.dependency_name}: `{row.current_status}`; next action: {row.review_action}"
        for row in row_list
    ]


def conditional_theorem_packet_545_markdown(
    quantifier_rows: Iterable[QuantifierSafetyAuditRecord],
    dependency_rows: Iterable[AssumptionDependencyRecord] = (),
) -> str:
    """Render the conditional theorem packet."""
    qrows = list(quantifier_rows)
    newforms = _newform_rows(qrows)
    aggregate_label = _aggregate_label(qrows)
    lines = [
        "# Conditional Theorem Packet For `(5,4,5)`",
        "",
        "This packet states the current focused route as a conditional modular-method argument for human review. It records what the computation currently supports and which mathematical assumptions still need to be supplied.",
        "",
        "## Hypothetical Primitive Solution",
        "",
        "Assume nonzero pairwise-coprime integers `A`, `B`, and `C` satisfy",
        "",
        "```text",
        "A^5 + B^4 = C^5.",
        "```",
        "",
        "All sign, parity, and normalization conventions still have to be fixed in the hand-written setup.",
        "",
        "## Proposed Frey Object",
        "",
        "The focused route uses the template",
        "",
        "```text",
        "E: y^2 = x(x - A^5)(x + B^4).",
        "```",
        "",
        "The attachment of this object to every primitive solution remains an assumption in this packet.",
        "",
        "## Assumed Modular Route",
        "",
        "- The residual representation is compared modulo `5`.",
        "- The representation is assumed irreducible in the required sense.",
        "- The conductor/level-lowering package is assumed to land at level `220`.",
        "- The level-220 target space is assumed to be exhausted by the two imported Sage newform slots.",
        "- Newform coefficients are compared in the justified residue field above `5`.",
        "",
        "## Local Branch Elimination Evidence",
        "",
        f"- Quantifier-safety label: `{aggregate_label}`.",
        "- The audit uses the exists-prime-per-newform quantifier: one fully covering prime is enough for a given newform.",
        "- It does not use a fixed branch assignment across different primes.",
        "",
        "| newform | eliminating non-q=3 primes | quantifier label |",
        "| --- | --- | --- |",
    ]
    for row in newforms:
        lines.append(
            f"| `{row.newform_label}` | `{row.eliminated_primes or 'none'}` | `{row.quantifier_classification}` |"
        )
    lines.extend(
        [
            "",
            "In the completed coefficient run, this records newform 0 as eliminated at q=17 and q=41, and newform 1 as eliminated at q=13, subject to the assumptions below.",
            "",
            "## Exact Assumptions Still Unverified",
            "",
            *_assumption_lines(dependency_rows),
            "",
            "## Why This Is Not A Completed Argument",
            "",
            "The packet is conditional route evidence only. The Frey attachment, minimal model/conductor computation, residual irreducibility, level-lowering hypotheses, coefficient-field reductions, multiplicative branch congruence, and local branch coverage still require independent mathematical verification.",
            "",
            "The route ceiling therefore remains `worth_human_modular_review`, even when the quantifier audit reports `quantifier_safe_cross_prime_candidate`.",
            "",
        ]
    )
    return "\n".join(lines)


def write_conditional_theorem_packet_545_markdown(
    path: Path,
    quantifier_rows: Iterable[QuantifierSafetyAuditRecord],
    dependency_rows: Iterable[AssumptionDependencyRecord] = (),
) -> Path:
    """Write `CONDITIONAL_THEOREM_PACKET_545.md`."""
    path.write_text(
        conditional_theorem_packet_545_markdown(quantifier_rows, dependency_rows),
        encoding="utf-8",
    )
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write the focused 5-4-5 conditional theorem packet.")
    parser.add_argument("--output", default="CONDITIONAL_THEOREM_PACKET_545.md")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    write_conditional_theorem_packet_545_markdown(Path(args.output), [])
    print(Path(args.output).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
