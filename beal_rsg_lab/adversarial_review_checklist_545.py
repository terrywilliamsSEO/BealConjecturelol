"""Adversarial review checklist for the focused `(5,4,5)` route."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

from .assumption_dependency_graph_545 import AssumptionDependencyRecord
from .bad_prime_tate_checklist_545 import BadPrimeTateChecklistRecord
from .conductor_support_audit_545 import ConductorSupportAuditRecord
from .conditional_route_validity_score_545 import ConditionalRouteValidityScoreRecord
from .level_lowering_obligation_545 import LevelLoweringObligationRecord
from .quantifier_safety_audit_545 import QuantifierSafetyAuditRecord


def _aggregate_label(rows: Iterable[QuantifierSafetyAuditRecord]) -> str:
    for row in rows:
        if row.newform_index == -1:
            return row.quantifier_classification
    return "data_insufficient"


def adversarial_review_checklist_545_markdown(
    quantifier_rows: Iterable[QuantifierSafetyAuditRecord] = (),
    dependency_rows: Iterable[AssumptionDependencyRecord] = (),
    conductor_rows: Iterable[ConductorSupportAuditRecord] = (),
    bad_prime_rows: Iterable[BadPrimeTateChecklistRecord] = (),
    level_lowering_rows: Iterable[LevelLoweringObligationRecord] = (),
    validity_rows: Iterable[ConditionalRouteValidityScoreRecord] = (),
) -> str:
    """Render a human adversarial checklist."""
    qrows = list(quantifier_rows)
    drows = list(dependency_rows)
    crows = list(conductor_rows)
    brows = list(bad_prime_rows)
    lrows = list(level_lowering_rows)
    vrows = list(validity_rows)
    dependency_status = ";".join(f"{row.dependency_id}:{row.current_status}" for row in drows) or "not_generated"
    conductor_status = ";".join(f"{row.prime_or_symbol}:{row.audit_label}" for row in crows) or "not_generated"
    bad_prime_status = ";".join(f"q={row.prime}:{row.audit_label}" for row in brows) or "not_generated"
    level_status = ";".join(f"{row.obligation_id}:{row.current_status}" for row in lrows) or "not_generated"
    validity_label = vrows[0].validity_label if vrows else "not_scored"
    lines = [
        "# Adversarial Review Checklist For `(5,4,5)`",
        "",
        f"- Quantifier-safety label: `{_aggregate_label(qrows)}`.",
        f"- Conditional route validity label: `{validity_label}`.",
        f"- Dependency status summary: `{dependency_status}`.",
        f"- Conductor support summary: `{conductor_status}`.",
        f"- Bad-prime local summary: `{bad_prime_status}`.",
        f"- Level-lowering summary: `{level_status}`.",
        "- Route ceiling: `worth_human_modular_review`.",
        "",
        "## Core Modular-Method Checks",
        "",
        "- [ ] Is level `220` truly the lowered level for the attached Frey curve?",
        "- [ ] Is the proposed Frey curve attached to every primitive solution case, including signs and normalization?",
        "- [ ] Is the residual mod-5 representation irreducible in the exact sense required by the level-lowering theorem?",
        "- [ ] Are q=13, q=17, and q=41 good relative to the true conductor, not just relative to the candidate level?",
        "- [ ] If q=61 is used as support data, is it also good relative to the true conductor?",
        "",
        "## Local Branch Checks",
        "",
        "- [ ] Are the multiplicative branches A_only, B_only, and C_only correctly classified by a Tate algorithm or equivalent reduction analysis?",
        "- [ ] Is the mod-5 comparison `a_q(f) = +/-(q+1)` justified for every multiplicative branch where it is used?",
        "- [ ] Are all coefficient fields handled safely, including the choice of reduction above `5`?",
        "- [ ] Does each newform have at least one eliminating prime where unit, A_only, B_only, C_only, and all pairwise masks are covered?",
        "- [ ] Does the cross-prime argument avoid invalid fixed-branch coupling across different primes?",
        "- [ ] Are there surviving cases where q divides `ABC`, especially under A_only, B_only, or C_only?",
        "",
        "## Current Conditional Evidence To Recheck",
        "",
        "- [ ] Recompute the q-expansion coefficients for the two level-220 newform slots independently.",
        "- [ ] Recompute the allowed multiplicative residues `+/-(q+1) mod 5` at q=13, q=17, q=41, and q=61.",
        "- [ ] Verify newform 0 has complete same-prime branch coverage at q=17 or q=41.",
        "- [ ] Verify newform 1 has complete same-prime branch coverage at q=13.",
        "- [ ] Confirm q=3 is not required for the primary conditional route.",
        "",
        "## Failure Modes",
        "",
        "- [ ] If level 220 changes, rerun the newform and coefficient comparison pipeline.",
        "- [ ] If any single-mask formula is missing, downgrade the route to a human Tate-algorithm obligation.",
        "- [ ] If any eliminating prime lacks one tracked local branch, downgrade to `branch_coverage_gap`.",
        "- [ ] If elimination only works by matching one branch at q=13 with a different branch at q=17 or q=41, downgrade to `invalid_cross_prime_branch_dependency`.",
        "",
    ]
    return "\n".join(lines)


def write_adversarial_review_checklist_545_markdown(
    path: Path,
    quantifier_rows: Iterable[QuantifierSafetyAuditRecord] = (),
    dependency_rows: Iterable[AssumptionDependencyRecord] = (),
    conductor_rows: Iterable[ConductorSupportAuditRecord] = (),
    bad_prime_rows: Iterable[BadPrimeTateChecklistRecord] = (),
    level_lowering_rows: Iterable[LevelLoweringObligationRecord] = (),
    validity_rows: Iterable[ConditionalRouteValidityScoreRecord] = (),
) -> Path:
    """Write `ADVERSARIAL_REVIEW_CHECKLIST_545.md`."""
    path.write_text(
        adversarial_review_checklist_545_markdown(
            quantifier_rows,
            dependency_rows,
            conductor_rows,
            bad_prime_rows,
            level_lowering_rows,
            validity_rows,
        ),
        encoding="utf-8",
    )
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write focused 5-4-5 adversarial review checklist.")
    parser.add_argument("--output", default="ADVERSARIAL_REVIEW_CHECKLIST_545.md")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    write_adversarial_review_checklist_545_markdown(Path(args.output))
    print(Path(args.output).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
