"""Assumption dependency graph for the focused `(5,4,5)` route."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from .quantifier_safety_audit_545 import QuantifierSafetyAuditRecord


@dataclass(frozen=True)
class AssumptionDependencyRecord:
    """One dependency node in the focused conditional route."""

    signature: str
    dependency_id: str
    dependency_name: str
    depends_on: str
    current_status: str
    blocks_label_beyond_review: bool
    route_ceiling_label: str
    review_action: str

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


def _quantifier_status(rows: Iterable[QuantifierSafetyAuditRecord]) -> str:
    for row in rows:
        if row.newform_index == -1:
            return row.quantifier_classification
    return "data_insufficient"


def build_assumption_dependency_graph_545(
    quantifier_rows: Iterable[QuantifierSafetyAuditRecord] = (),
) -> list[AssumptionDependencyRecord]:
    """Return dependency records for the conditional focused route."""
    quantifier_label = _quantifier_status(list(quantifier_rows))
    signature = "5-4-5"
    ceiling = "worth_human_modular_review"
    return [
        AssumptionDependencyRecord(
            signature=signature,
            dependency_id="AD545-001",
            dependency_name="Frey curve attachment",
            depends_on="none",
            current_status="needs_human_derivation",
            blocks_label_beyond_review=True,
            route_ceiling_label=ceiling,
            review_action="Derive the Frey object from a primitive solution and check singular and normalization cases.",
        ),
        AssumptionDependencyRecord(
            signature=signature,
            dependency_id="AD545-002",
            dependency_name="Invariant formulas",
            depends_on="AD545-001",
            current_status="needs_human_verification",
            blocks_label_beyond_review=True,
            route_ceiling_label=ceiling,
            review_action="Verify discriminant, c4, c6, minimality, and valuation formulas at the focused primes.",
        ),
        AssumptionDependencyRecord(
            signature=signature,
            dependency_id="AD545-003",
            dependency_name="Multiplicative reduction classification",
            depends_on="AD545-002",
            current_status="conditional_route_evidence",
            blocks_label_beyond_review=True,
            route_ceiling_label=ceiling,
            review_action="Run the Tate algorithm or an equivalent reduction analysis for A_only, B_only, and C_only.",
        ),
        AssumptionDependencyRecord(
            signature=signature,
            dependency_id="AD545-004",
            dependency_name="Residual mod-5 irreducibility",
            depends_on="AD545-001;AD545-002",
            current_status="missing",
            blocks_label_beyond_review=True,
            route_ceiling_label=ceiling,
            review_action="Prove irreducibility and identify any exceptional residual cases.",
        ),
        AssumptionDependencyRecord(
            signature=signature,
            dependency_id="AD545-005",
            dependency_name="Level lowering to 220",
            depends_on="AD545-002;AD545-004",
            current_status="needs_human_derivation",
            blocks_label_beyond_review=True,
            route_ceiling_label=ceiling,
            review_action="Check the conductor and every level-lowering hypothesis leading to level 220.",
        ),
        AssumptionDependencyRecord(
            signature=signature,
            dependency_id="AD545-006",
            dependency_name="Newform coefficient comparison",
            depends_on="AD545-005",
            current_status="computed_route_evidence",
            blocks_label_beyond_review=True,
            route_ceiling_label=ceiling,
            review_action="Confirm the level-220 newforms, coefficient fields, and reductions above 5.",
        ),
        AssumptionDependencyRecord(
            signature=signature,
            dependency_id="AD545-007",
            dependency_name="Local branch coverage",
            depends_on="AD545-003;AD545-006",
            current_status="conditional_route_evidence",
            blocks_label_beyond_review=True,
            route_ceiling_label=ceiling,
            review_action="Verify unit, single-mask, and pairwise primitive-forbidden branches at each eliminating prime.",
        ),
        AssumptionDependencyRecord(
            signature=signature,
            dependency_id="AD545-008",
            dependency_name="Quantifier safety",
            depends_on="AD545-007",
            current_status=quantifier_label,
            blocks_label_beyond_review=True,
            route_ceiling_label=ceiling,
            review_action="Use only exists-prime-per-newform elimination; reject fixed-branch coupling across different primes.",
        ),
    ]


def assumption_dependency_graph_545_markdown(rows: Iterable[AssumptionDependencyRecord]) -> str:
    """Render dependency records as Markdown."""
    row_list = list(rows)
    edge_lines = []
    for row in row_list:
        if row.depends_on == "none":
            continue
        for parent in row.depends_on.split(";"):
            edge_lines.append(f'    "{parent}" --> "{row.dependency_id}"')
    lines = [
        "# Assumption Dependency Graph For `(5,4,5)`",
        "",
        "Every dependency remains capped at `worth_human_modular_review` until the hand checks are supplied.",
        "",
        "```mermaid",
        "graph TD",
        *edge_lines,
        "```",
        "",
        "| id | dependency | depends on | status | blocks beyond review | review action |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in row_list:
        lines.append(
            f"| `{row.dependency_id}` | {row.dependency_name} | `{row.depends_on}` | "
            f"`{row.current_status}` | `{row.blocks_label_beyond_review}` | {row.review_action} |"
        )
    lines.append("")
    return "\n".join(lines)


def write_assumption_dependency_graph_545_csv(
    path: Path,
    rows: Iterable[AssumptionDependencyRecord],
) -> Path:
    """Write `assumption_dependency_graph_545.csv`."""
    _write_csv(path, [row.to_flat_dict() for row in rows])
    return path


def write_assumption_dependency_graph_545_markdown(
    path: Path,
    rows: Iterable[AssumptionDependencyRecord],
) -> Path:
    """Write `ASSUMPTION_DEPENDENCY_GRAPH_545.md`."""
    path.write_text(assumption_dependency_graph_545_markdown(rows), encoding="utf-8")
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write focused 5-4-5 assumption dependency graph rows.")
    parser.add_argument("--output", default="assumption_dependency_graph_545.csv")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    write_assumption_dependency_graph_545_csv(Path(args.output), build_assumption_dependency_graph_545())
    print(Path(args.output).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
