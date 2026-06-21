"""Conservative validity score for the focused `(5,4,5)` route."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from .bad_prime_tate_checklist_545 import BadPrimeTateChecklistRecord
from .conductor_support_audit_545 import ConductorSupportAuditRecord
from .frey_curve_derivation_545 import FreyCurveDerivationRecord
from .level_lowering_obligation_545 import LevelLoweringObligationRecord
from .quantifier_safety_audit_545 import QuantifierSafetyAuditRecord


SAFE_CONDITIONAL_ROUTE_VALIDITY_LABELS = {
    "conditional_route_strong_computational",
    "conductor_gap_blocks_upgrade",
    "frey_template_gap_blocks_upgrade",
    "level_lowering_gap_blocks_upgrade",
}


@dataclass(frozen=True)
class ConditionalRouteValidityScoreRecord:
    """Aggregate conservative score for the focused route."""

    signature: str
    trace_logic_completeness: str
    quantifier_safety: str
    symbolic_frey_validity: str
    conductor_support_confidence: str
    bad_prime_local_confidence: str
    level_lowering_confidence: str
    irreducibility_confidence: str
    validity_label: str
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


def _quantifier_label(rows: Iterable[QuantifierSafetyAuditRecord]) -> str:
    for row in rows:
        if row.newform_index == -1:
            return row.quantifier_classification
    return "data_insufficient"


def _derive_label(
    frey_rows: list[FreyCurveDerivationRecord],
    conductor_rows: list[ConductorSupportAuditRecord],
    bad_prime_rows: list[BadPrimeTateChecklistRecord],
    level_rows: list[LevelLoweringObligationRecord],
) -> tuple[str, str]:
    if any(row.audit_label == "formula_mismatch" for row in frey_rows):
        return "frey_template_gap_blocks_upgrade", "At least one symbolic Frey invariant disagrees with the template records."
    if any(row.audit_label in {"conductor_support_gap", "needs_human_review"} for row in conductor_rows):
        return "conductor_gap_blocks_upgrade", "The conductor support audit still has unresolved support or exponent gaps."
    if any(row.audit_label in {"blocks_conductor_claim", "missing_local_analysis"} for row in bad_prime_rows):
        return "conductor_gap_blocks_upgrade", "Bad-prime local Tate analysis still blocks a conductor claim."
    if any(row.current_status in {"missing", "blocks_upgrade", "needs_human_review"} for row in level_rows):
        return "level_lowering_gap_blocks_upgrade", "Level-lowering obligations remain missing or unverified."
    return "conditional_route_strong_computational", "All tracked computational checks are present, still capped at human review."


def build_conditional_route_validity_score_545(
    quantifier_rows: Iterable[QuantifierSafetyAuditRecord],
    frey_rows: Iterable[FreyCurveDerivationRecord],
    conductor_rows: Iterable[ConductorSupportAuditRecord],
    bad_prime_rows: Iterable[BadPrimeTateChecklistRecord],
    level_rows: Iterable[LevelLoweringObligationRecord],
) -> list[ConditionalRouteValidityScoreRecord]:
    """Build a conservative route validity score."""
    qrows = list(quantifier_rows)
    frows = list(frey_rows)
    crows = list(conductor_rows)
    brows = list(bad_prime_rows)
    lrows = list(level_rows)
    quantifier = _quantifier_label(qrows)
    symbolic = "symbolic_formulas_available" if frows and all(row.audit_label == "verified_symbolic" for row in frows) else "frey_formula_gap"
    conductor = "conductor_support_gap" if any(row.audit_label in {"conductor_support_gap", "needs_human_review"} for row in crows) else "conductor_support_reviewed"
    bad_prime = "bad_prime_tate_gap" if any(row.audit_label == "blocks_conductor_claim" for row in brows) else "bad_prime_local_reviewed"
    level = "level_lowering_gap" if any(row.current_status in {"missing", "blocks_upgrade", "needs_human_review"} for row in lrows) else "level_lowering_reviewed"
    irreducibility = "missing" if any(row.obligation_name == "Residual representation irreducible" and row.current_status == "missing" for row in lrows) else "reviewed"
    label, reason = _derive_label(frows, crows, brows, lrows)
    if label not in SAFE_CONDITIONAL_ROUTE_VALIDITY_LABELS:
        label = "level_lowering_gap_blocks_upgrade"
        reason = "Unexpected validity label was downgraded to level_lowering_gap_blocks_upgrade."
    return [
        ConditionalRouteValidityScoreRecord(
            signature="5-4-5",
            trace_logic_completeness="quantifier_safe_trace_candidate" if quantifier == "quantifier_safe_cross_prime_candidate" else quantifier,
            quantifier_safety=quantifier,
            symbolic_frey_validity=symbolic,
            conductor_support_confidence=conductor,
            bad_prime_local_confidence=bad_prime,
            level_lowering_confidence=level,
            irreducibility_confidence=irreducibility,
            validity_label=label,
            route_ceiling_label="worth_human_modular_review",
            reason=reason,
        )
    ]


def conditional_route_validity_score_545_markdown(
    rows: Iterable[ConditionalRouteValidityScoreRecord],
) -> str:
    """Render the conditional route validity score."""
    row_list = list(rows)
    row = row_list[0] if row_list else None
    lines = [
        "# Conditional Route Validity Score For `(5,4,5)`",
        "",
        f"- Validity label: `{row.validity_label if row else 'level_lowering_gap_blocks_upgrade'}`.",
        f"- Route ceiling: `{row.route_ceiling_label if row else 'worth_human_modular_review'}`.",
        "",
        "| component | status |",
        "| --- | --- |",
    ]
    if row is not None:
        lines.extend(
            [
                f"| trace logic completeness | `{row.trace_logic_completeness}` |",
                f"| quantifier safety | `{row.quantifier_safety}` |",
                f"| symbolic Frey validity | `{row.symbolic_frey_validity}` |",
                f"| conductor support confidence | `{row.conductor_support_confidence}` |",
                f"| bad-prime local confidence | `{row.bad_prime_local_confidence}` |",
                f"| level-lowering confidence | `{row.level_lowering_confidence}` |",
                f"| irreducibility confidence | `{row.irreducibility_confidence}` |",
            ]
        )
    lines.extend(
        [
            "",
            f"Reason: {row.reason if row else 'No score rows were available.'}",
            "",
        ]
    )
    return "\n".join(lines)


def write_conditional_route_validity_score_545_csv(
    path: Path,
    rows: Iterable[ConditionalRouteValidityScoreRecord],
) -> Path:
    """Write `conditional_route_validity_score_545.csv`."""
    _write_csv(path, [row.to_flat_dict() for row in rows])
    return path


def write_conditional_route_validity_score_545_markdown(
    path: Path,
    rows: Iterable[ConditionalRouteValidityScoreRecord],
) -> Path:
    """Write `CONDITIONAL_ROUTE_VALIDITY_SCORE_545.md`."""
    path.write_text(conditional_route_validity_score_545_markdown(rows), encoding="utf-8")
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write focused 5-4-5 conditional route validity score rows.")
    parser.add_argument("--output", default="conditional_route_validity_score_545.csv")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    write_conditional_route_validity_score_545_csv(Path(args.output), [])
    print(Path(args.output).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
