"""Focused eliminating-prime nonunit branch filter for `(5,4,5)`."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from .local_case_closure_score_545 import LocalCaseClosureScoreRecord
from .multiplicative_reduction_congruence_545 import MultiplicativeReductionCongruenceRecord
from .nonunit_elimination_545 import NonunitEliminationRecord, TARGET_PRIMES_545
from .singular_reduction_trace_545 import SingularReductionTraceRecord
from .single_mask_newform_pressure_545 import SingleMaskNewformPressureRecord
from .trace_congruence_filter_545 import TraceCongruenceFilterRecord


SAFE_NONUNIT_FILTER_LABELS = {
    "unit_only_elimination",
    "local_case_elimination_candidate",
    "local_coverage_gap",
    "level_lowering_assumption_required",
    "unit_branch_survivor_exists",
    "single_mask_survivor_exists",
    "nonunit_survivor_exists",
    "nonunit_unresolved",
    "reduction_argument_required",
}


@dataclass(frozen=True)
class NonunitNewformFilterRecord:
    """Focused-prime status after combining unit trace filters and nonunit branches."""

    signature: str
    prime: int
    unit_eliminated_newform_count: int
    unit_surviving_newform_count: int
    possible_nonunit_masks: str
    unresolved_nonunit_masks: str
    primitive_forbidden_masks: str
    reduction_argument_masks: str
    single_mask_condition_masks: str
    single_mask_pressure_label: str
    local_case_closure_label: str
    local_case_closure_summary: str
    full_nonunit_resolution: bool
    safe_label: str
    route_ceiling_label: str
    reason: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def _join_masks(masks: Iterable[str]) -> str:
    return ";".join(sorted(dict.fromkeys(masks)))


def build_nonunit_newform_filters_545(
    filter_rows: Iterable[TraceCongruenceFilterRecord],
    nonunit_rows: Iterable[NonunitEliminationRecord],
    reduction_rows: Iterable[SingularReductionTraceRecord],
    *,
    pressure_rows: Iterable[SingleMaskNewformPressureRecord] = (),
    closure_rows: Iterable[LocalCaseClosureScoreRecord] = (),
    target_primes: tuple[int, ...] = TARGET_PRIMES_545,
) -> list[NonunitNewformFilterRecord]:
    """Combine unit trace elimination with focused-prime nonunit coverage."""
    targets = set(target_primes)
    filters_by_prime: dict[int, list[TraceCongruenceFilterRecord]] = {}
    for row in filter_rows:
        if row.prime in targets:
            filters_by_prime.setdefault(row.prime, []).append(row)

    nonunit_by_prime: dict[int, list[NonunitEliminationRecord]] = {}
    for row in nonunit_rows:
        if row.prime in targets:
            nonunit_by_prime.setdefault(row.prime, []).append(row)

    reduction_by_prime: dict[int, list[SingularReductionTraceRecord]] = {}
    for row in reduction_rows:
        if row.prime in targets:
            reduction_by_prime.setdefault(row.prime, []).append(row)

    pressure_by_prime: dict[int, list[SingleMaskNewformPressureRecord]] = {}
    for row in pressure_rows:
        if row.prime in targets:
            pressure_by_prime.setdefault(row.prime, []).append(row)

    closure_by_prime = {row.prime: row for row in closure_rows if row.prime in targets}

    records: list[NonunitNewformFilterRecord] = []
    for prime in sorted(targets):
        prime_filters = filters_by_prime.get(prime, [])
        prime_nonunit = nonunit_by_prime.get(prime, [])
        prime_reductions = reduction_by_prime.get(prime, [])
        prime_pressure = pressure_by_prime.get(prime, [])
        eliminated = sum(1 for row in prime_filters if row.filter_classification == "eliminated")
        survives = sum(1 for row in prime_filters if row.filter_classification == "survives")
        possible_masks = [
            row.valuation_mask for row in prime_nonunit if row.possible_mod_q and not row.primitive_forbidden
        ]
        if prime_pressure:
            unresolved_masks = [
                row.valuation_mask
                for row in prime_pressure
                if row.branch_classification in {"needs_human_tate_algorithm", "unresolved_single_mask"}
            ]
            condition_masks = [
                row.valuation_mask
                for row in prime_pressure
                if row.branch_classification
                in {"multiplicative_reduction_condition", "additive_reduction_condition"}
            ]
        else:
            unresolved_masks = [row.valuation_mask for row in prime_nonunit if row.unresolved]
            condition_masks = []
        primitive_forbidden = [row.valuation_mask for row in prime_nonunit if row.primitive_forbidden]
        if prime_pressure:
            reduction_argument_masks = [
                row.valuation_mask
                for row in prime_pressure
                if row.branch_classification == "needs_human_tate_algorithm"
            ]
        else:
            reduction_argument_masks = [
                row.valuation_mask for row in prime_reductions if row.needs_human_reduction_argument
            ]
        full_resolution = not unresolved_masks and (bool(prime_pressure) or not reduction_argument_masks)
        pressure_label = (
            next((row.prime_local_label for row in prime_pressure), "")
            if prime_pressure
            else ""
        )
        closure = closure_by_prime.get(prime)
        closure_label = closure.closure_label if closure else ""
        closure_summary = (
            f"fully_eliminated={closure.fully_eliminated_newforms or 'none'}; "
            f"surviving={closure.surviving_newforms or 'none'}; "
            f"unresolved={closure.unresolved_newforms or 'none'}"
            if closure
            else ""
        )
        if closure is not None:
            label = closure.closure_label
            reason = closure.reason
            full_resolution = closure.closure_label == "local_case_elimination_candidate"
        elif prime_pressure and pressure_label == "local_coverage_gap":
            label = "local_coverage_gap"
            reason = "At least one single-mask branch remains unresolved or needs human Tate analysis."
        elif eliminated and full_resolution:
            label = "local_case_elimination_candidate"
            reason = "The unit trace filter eliminates a newform and all focused single-mask branches are classified by the reduction diagnostic layer."
        elif reduction_argument_masks:
            label = "reduction_argument_required"
            reason = "At least one single-divisibility branch needs a separate Frey reduction argument."
        elif unresolved_masks:
            label = "nonunit_unresolved"
            reason = "At least one nonunit branch remains locally possible and unresolved."
        elif possible_masks:
            label = "nonunit_survivor_exists"
            reason = "Nonunit branches remain possible after the current focused filter."
        else:
            label = "unit_only_elimination" if eliminated else "nonunit_unresolved"
            reason = "Only the unit trace filter has active eliminating data for this prime."
        if label not in SAFE_NONUNIT_FILTER_LABELS:
            label = "nonunit_unresolved"
            reason = "Unexpected branch state was downgraded to a conservative unresolved label."
        records.append(
            NonunitNewformFilterRecord(
                signature="5-4-5",
                prime=prime,
                unit_eliminated_newform_count=eliminated,
                unit_surviving_newform_count=survives,
                possible_nonunit_masks=_join_masks(possible_masks),
                unresolved_nonunit_masks=_join_masks(unresolved_masks),
                primitive_forbidden_masks=_join_masks(primitive_forbidden),
                reduction_argument_masks=_join_masks(reduction_argument_masks),
                single_mask_condition_masks=_join_masks(condition_masks),
                single_mask_pressure_label=pressure_label or label,
                local_case_closure_label=closure_label or label,
                local_case_closure_summary=closure_summary,
                full_nonunit_resolution=full_resolution,
                safe_label=label,
                route_ceiling_label="worth_human_modular_review",
                reason=reason,
            )
        )
    return records


def local_case_decision_tree_545_markdown(
    *,
    filter_rows: Iterable[TraceCongruenceFilterRecord],
    nonunit_rows: Iterable[NonunitEliminationRecord],
    reduction_rows: Iterable[SingularReductionTraceRecord],
    newform_filter_rows: Iterable[NonunitNewformFilterRecord],
    pressure_rows: Iterable[SingleMaskNewformPressureRecord] = (),
    multiplicative_rows: Iterable[MultiplicativeReductionCongruenceRecord] = (),
    closure_rows: Iterable[LocalCaseClosureScoreRecord] = (),
) -> str:
    """Render the focused eliminating-prime branch decision tree."""
    filters_by_prime: dict[int, list[TraceCongruenceFilterRecord]] = {}
    for row in filter_rows:
        if row.prime in TARGET_PRIMES_545:
            filters_by_prime.setdefault(row.prime, []).append(row)
    nonunit_by_prime: dict[int, list[NonunitEliminationRecord]] = {}
    for row in nonunit_rows:
        nonunit_by_prime.setdefault(row.prime, []).append(row)
    reduction_by_key = {(row.prime, row.valuation_mask): row for row in reduction_rows}
    decision_by_prime = {row.prime: row for row in newform_filter_rows}
    pressure_by_prime: dict[int, list[SingleMaskNewformPressureRecord]] = {}
    for row in pressure_rows:
        pressure_by_prime.setdefault(row.prime, []).append(row)
    multiplicative_by_prime: dict[int, list[MultiplicativeReductionCongruenceRecord]] = {}
    for row in multiplicative_rows:
        multiplicative_by_prime.setdefault(row.prime, []).append(row)
    closure_by_prime = {row.prime: row for row in closure_rows}

    lines = [
        "# Local Case Decision Tree For `(5,4,5)` At Eliminating Good Primes",
        "",
        "This decision tree narrows the local coverage gap for `A^5 + B^4 = C^5`. It is a route audit only: unit trace eliminations do not become global eliminations until every nonunit branch has a justified local reduction argument.",
        "",
    ]
    for prime in TARGET_PRIMES_545:
        decision = decision_by_prime.get(prime)
        lines.extend(
            [
                f"## q={prime}",
                "",
                "### Unit Case",
                "",
                "| newform | classification | mode | reason |",
                "| ---: | --- | --- | --- |",
            ]
        )
        for row in sorted(filters_by_prime.get(prime, []), key=lambda item: item.newform_index):
            lines.append(
                f"| {row.newform_index} | `{row.filter_classification}` | `{row.comparison_mode}` | {row.reason} |"
            )
        if not filters_by_prime.get(prime):
            lines.append("| none | `insufficient_data` | `unknown` | No unit trace filter rows were imported for this prime. |")
        lines.extend(
            [
                "",
                "### Nonunit Branches",
                "",
                "| mask | mod q | mod q^2 | mod q^3 | primitive | reduction route | branch status |",
                "| --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in sorted(nonunit_by_prime.get(prime, []), key=lambda item: item.valuation_mask):
            reduction = reduction_by_key.get((row.prime, row.valuation_mask))
            lines.append(
                f"| `{row.valuation_mask}` | `{row.possible_mod_q}` | `{row.possible_mod_q2}` | "
                f"`{row.possible_mod_q3}` | `{not row.primitive_forbidden}` | "
                f"`{reduction.frey_reduction_classification if reduction else 'template_unknown'}` | `{row.branch_label}` |"
            )
        if pressure_by_prime.get(prime):
            lines.extend(
                [
                    "",
                    "### Single-Mask Frey Reduction Pressure",
                    "",
                    "| mask | reduction type | Tate stub | branch classification | prime label |",
                    "| --- | --- | --- | --- | --- |",
                ]
            )
            for row in sorted(pressure_by_prime.get(prime, []), key=lambda item: item.valuation_mask):
                lines.append(
                    f"| `{row.valuation_mask}` | `{row.reduction_type}` | `{row.tate_algorithm_status}` | "
                    f"`{row.branch_classification}` | `{row.prime_local_label}` |"
                )
        if multiplicative_by_prime.get(prime):
            lines.extend(
                [
                    "",
                    "### Multiplicative-Reduction Congruence",
                    "",
                    "| mask | newform | a_q mod 5 | allowed | classification |",
                    "| --- | ---: | --- | --- | --- |",
                ]
            )
            for row in sorted(
                multiplicative_by_prime.get(prime, []),
                key=lambda item: (item.valuation_mask, item.newform_index),
            ):
                lines.append(
                    f"| `{row.valuation_mask}` | {row.newform_index} | `{row.coefficient_mod_5 or 'missing'}` | "
                    f"`{row.allowed_multiplicative_values_mod_5}` | `{row.congruence_classification}` |"
                )
        closure = closure_by_prime.get(prime)
        lines.extend(
            [
                "",
                "### Focused Decision",
                "",
                f"- Safe label: `{decision.safe_label if decision else 'nonunit_unresolved'}`.",
                f"- Full nonunit resolution: `{decision.full_nonunit_resolution if decision else False}`.",
                f"- Reduction argument masks: `{decision.reduction_argument_masks if decision and decision.reduction_argument_masks else 'none'}`.",
                f"- Single-mask condition masks: `{decision.single_mask_condition_masks if decision and decision.single_mask_condition_masks else 'none'}`.",
                f"- Closure label: `{closure.closure_label if closure else (decision.local_case_closure_label if decision else 'missing')}`.",
                f"- Closure summary: `{decision.local_case_closure_summary if decision and decision.local_case_closure_summary else 'none'}`.",
                f"- Reason: {decision.reason if decision else 'No focused decision row was generated.'}",
                "",
            ]
        )
    decisions = list(decision_by_prime.values())
    if any(
        row.safe_label
        in {
            "local_coverage_gap",
            "level_lowering_assumption_required",
            "unit_branch_survivor_exists",
            "single_mask_survivor_exists",
            "nonunit_unresolved",
            "reduction_argument_required",
        }
        for row in decisions
    ):
        conclusion = (
            "At least one focused branch survives or still needs a level-lowering/Tate justification, so the current label remains "
            "`local_coverage_gap` with `unit_only_trace_mismatch_candidate` scope."
        )
    else:
        conclusion = "The focused single-mask branches are classified by the diagnostic layer, so any closed q can be logged only as `local_case_elimination_candidate` route evidence."
    lines.extend(["## Current Conclusion", "", conclusion, ""])
    return "\n".join(lines)
