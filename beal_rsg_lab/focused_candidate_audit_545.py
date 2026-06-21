"""Focused modular-method review packet for `(5,4,5)`."""

from __future__ import annotations

import csv
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from .assumption_register import AssumptionRecord, build_assumption_register_545
from .adversarial_review_checklist_545 import adversarial_review_checklist_545_markdown
from .assumption_dependency_graph_545 import (
    AssumptionDependencyRecord,
    assumption_dependency_graph_545_markdown,
    build_assumption_dependency_graph_545,
)
from .best_eliminating_prime_545 import (
    BestEliminatingPrimeRecord,
    best_eliminating_prime_545_markdown,
    build_best_eliminating_prime_545,
)
from .best_route_summary_545 import (
    BestRouteSummaryRecord,
    best_route_summary_545_markdown,
    build_best_route_summary_545,
)
from .cross_prime_branch_compatibility_545 import (
    CrossPrimeBranchCompatibilityRecord,
    build_cross_prime_branch_compatibility_545,
)
from .conditional_theorem_packet_545 import conditional_theorem_packet_545_markdown
from .frey_trace_possibility_545 import FreyTracePossibilityRecord, build_frey_trace_possibilities_545
from .frey_template_validity_audit import (
    FreyTemplateValidityRecord,
    build_frey_template_validity_audit_545,
)
from .frey_invariant_sanity_545 import (
    FreyInvariantSanityRecord,
    build_frey_invariant_sanity_545,
    frey_invariant_sanity_markdown,
)
from .good_prime_selector import GoodPrimeRecord, select_good_primes_545
from .frey_reduction_case_router_545 import (
    FreyReductionCaseRecord,
    build_frey_reduction_cases_545,
)
from .frey_reduction_diagnostics_545 import (
    FreyReductionDiagnosticRecord,
    build_frey_reduction_diagnostics_545,
)
from .level_220_audit import (
    Level220NewformRecord,
    Level220PrimeRecord,
    build_level_220_newform_records,
    build_level_220_prime_records,
    factorization_220,
)
from .level_220_robustness_545 import (
    LevelRobustnessRecord,
    build_level_robustness_545,
    level_robustness_markdown,
)
from .local_gap_summary_545 import (
    LocalGapSummaryRecord,
    build_local_gap_summary_545,
    local_gap_summary_markdown,
)
from .local_case_closure_score_545 import (
    LocalCaseClosureScoreRecord,
    build_local_case_closure_scores_545,
)
from .local_coverage_audit_545 import (
    LocalCoverageAuditRecord,
    build_local_coverage_audit_545,
    local_coverage_audit_markdown,
)
from .local_valuation_case_545 import LocalValuationCaseRecord, build_local_valuation_cases_545
from .nonunit_elimination_545 import NonunitEliminationRecord, build_nonunit_eliminations_545
from .nonunit_newform_filter_545 import (
    NonunitNewformFilterRecord,
    build_nonunit_newform_filters_545,
    local_case_decision_tree_545_markdown,
)
from .newform_coefficient_importer import (
    NewformCoefficientImportSummary,
    NewformCoefficientRow,
    import_level_220_newform_coefficients,
)
from .multiplicative_reduction_congruence_545 import (
    MultiplicativeReductionCongruenceRecord,
    build_multiplicative_reduction_congruences_545,
)
from .obstruction_progress_score import ObstructionProgressRecord, score_obstruction_progress_545
from .proof_gap_report import ProofGapRecord, build_proof_gap_records_545, proof_gap_report_markdown
from .quantifier_safety_audit_545 import (
    QuantifierSafetyAuditRecord,
    build_quantifier_safety_audit_545,
    quantifier_safety_audit_545_markdown,
)
from .q3_exceptionality_audit_545 import (
    Q3ExceptionalityAuditRecord,
    build_q3_exceptionality_audit_545,
    q3_exceptionality_audit_545_markdown,
)
from .sage_level_220_newform_expander import write_sage_level_220_newform_expander
from .singular_reduction_trace_545 import (
    SingularReductionTraceRecord,
    build_singular_reduction_traces_545,
)
from .single_mask_newform_pressure_545 import (
    SingleMaskNewformPressureRecord,
    build_single_mask_newform_pressure_545,
)
from .small_prime_sensitivity_545 import (
    SmallPrimeSensitivityRecord,
    build_small_prime_sensitivity_545,
    small_prime_sensitivity_markdown,
)
from .theorem_skeleton_545 import (
    TheoremSkeletonObligationRecord,
    build_theorem_skeleton_obligations_545,
    theorem_skeleton_markdown,
)
from .trace_congruence_filter_545 import (
    TraceCongruenceFilterRecord,
    build_trace_congruence_filter_545,
    load_level_220_coefficients,
)
from .trace_comparison_audit import TraceComparisonAuditRecord, build_trace_comparison_audit_545
from .trace_mismatch_provenance_545 import (
    TraceMismatchProvenanceRecord,
    build_trace_mismatch_provenance_545,
    trace_mismatch_provenance_markdown,
)
from .trace_filter_case_coverage_545 import (
    TraceFilterCaseCoverageRecord,
    build_trace_filter_case_coverage_545,
)
from .tate_algorithm_stub_545 import TateAlgorithmStubRecord, build_tate_algorithm_stub_545
from .valuation_mask_lift_545 import ValuationMaskLiftRecord, build_valuation_mask_lifts_545


SIGNATURE_545 = "5-4-5"


@dataclass(frozen=True)
class Focused545Artifacts:
    """Paths written by the focused `(5,4,5)` audit."""

    focused_report_path: str
    frey_template_validity_path: str
    level_220_prime_audit_path: str
    level_220_newforms_path: str
    trace_comparison_path: str
    good_prime_list_path: str
    sage_newform_expander_path: str
    frey_trace_possibilities_path: str
    trace_congruence_filter_path: str
    obstruction_progress_path: str
    coefficient_import_summary_path: str
    coefficient_import_rows_path: str
    trace_mismatch_provenance_path: str
    trace_mismatch_provenance_report_path: str
    small_prime_sensitivity_path: str
    small_prime_sensitivity_report_path: str
    local_coverage_audit_path: str
    local_coverage_audit_report_path: str
    frey_invariant_sanity_path: str
    frey_invariant_sanity_report_path: str
    level_robustness_path: str
    level_robustness_report_path: str
    theorem_skeleton_path: str
    theorem_skeleton_obligations_path: str
    local_valuation_cases_path: str
    valuation_mask_lift_path: str
    frey_reduction_cases_path: str
    trace_filter_case_coverage_path: str
    local_gap_summary_path: str
    local_gap_summary_report_path: str
    nonunit_eliminations_path: str
    singular_reduction_traces_path: str
    frey_reduction_diagnostics_path: str
    tate_algorithm_stub_path: str
    single_mask_newform_pressure_path: str
    multiplicative_reduction_congruence_path: str
    local_case_closure_score_path: str
    best_eliminating_prime_path: str
    best_eliminating_prime_report_path: str
    cross_prime_branch_compatibility_path: str
    q3_exceptionality_audit_report_path: str
    best_route_summary_report_path: str
    quantifier_safety_audit_path: str
    quantifier_safety_audit_report_path: str
    conditional_theorem_packet_path: str
    assumption_dependency_graph_path: str
    assumption_dependency_graph_report_path: str
    adversarial_review_checklist_path: str
    nonunit_newform_filter_path: str
    local_case_decision_tree_path: str
    assumption_register_path: str
    proof_gap_summary_path: str
    proof_gap_report_path: str


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: Iterable[Mapping[str, object]]) -> None:
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


def _first(rows: Iterable[Mapping[str, Any]], *, signature: str = SIGNATURE_545) -> Mapping[str, Any] | None:
    for row in rows:
        if str(row.get("signature", "")) == signature:
            return row
    return None


def _filter(rows: Iterable[Mapping[str, Any]], *, signature: str = SIGNATURE_545) -> list[Mapping[str, Any]]:
    return [row for row in rows if str(row.get("signature", "")) == signature]


def _load_sage_payload(run_dir: Path) -> dict[str, Any]:
    path = run_dir / "sage_results" / "sage_5_4_5.json"
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _sage_fact_lines(payload: Mapping[str, Any], import_row: Mapping[str, Any] | None) -> list[str]:
    checked = payload.get("checked_levels", [])
    trace_rows = payload.get("trace_rows", [])
    trace_summary = "none"
    if isinstance(trace_rows, list) and trace_rows:
        parts = []
        for row in trace_rows:
            if isinstance(row, dict):
                parts.append(
                    f"ell={row.get('ell')} support={row.get('trace_support_size')} traces={row.get('trace_counts')}"
                )
        trace_summary = "; ".join(parts)
    return [
        f"- Sage status: `{payload.get('sage_status', import_row.get('sage_status', 'missing') if import_row else 'missing')}`.",
        f"- Checked levels: `{';'.join(str(item) for item in checked) or 'none'}`.",
        f"- Level-220 newform count: `{payload.get('newform_count', import_row.get('newform_count', '0') if import_row else '0')}`.",
        f"- Trace status: `{payload.get('trace_match_status', import_row.get('trace_match_status', 'missing') if import_row else 'missing')}`.",
        f"- Imported local trace rows: {trace_summary}.",
        f"- Contradiction claim allowed: `{payload.get('contradiction_claim_allowed', False)}`.",
    ]


def _unit_lines(unit_rows: Iterable[Mapping[str, Any]]) -> list[str]:
    rows = list(unit_rows)
    if not rows:
        return ["- No local unit-survivor rows were available in this run."]
    lines = []
    for row in rows:
        lines.append(
            "- ell `{ell}`: verdict `{verdict}`, survivors `{survivors}`, lift `{lift}`, explanation: {explanation}".format(
                ell=row.get("ell", ""),
                verdict=row.get("artifact_verdict", ""),
                survivors=row.get("geometry_survivor_count", ""),
                lift=row.get("unit_lift_unit_lift_status", ""),
                explanation=row.get("artifact_explanation", ""),
            )
        )
    return lines


def _status_counts(rows: Iterable[Mapping[str, Any]]) -> tuple[int, int]:
    known = list(rows)
    mismatches = sum(
        1
        for row in known
        if str(row.get("calibration_status", "")).find("mismatch") >= 0
        or str(row.get("post_sage_label", "")) == "known_case_mismatch"
    )
    overpromotions = sum(1 for row in known if str(row.get("overpromoted", "False")) != "False")
    return mismatches, overpromotions


def focused_545_markdown(
    *,
    run_dir: Path,
    sage_payload: Mapping[str, Any],
    import_row: Mapping[str, Any] | None,
    audit_row: Mapping[str, Any] | None,
    unit_rows: list[Mapping[str, Any]],
    validity_rows: list[FreyTemplateValidityRecord],
    prime_rows: list[Level220PrimeRecord],
    newform_rows: list[Level220NewformRecord],
    trace_rows: list[TraceComparisonAuditRecord],
    good_prime_rows: list[GoodPrimeRecord],
    frey_trace_rows: list[FreyTracePossibilityRecord],
    filter_rows: list[TraceCongruenceFilterRecord],
    progress_row: ObstructionProgressRecord,
    coefficient_summary: NewformCoefficientImportSummary,
    coefficient_rows: list[NewformCoefficientRow],
    provenance_rows: list[TraceMismatchProvenanceRecord],
    sensitivity_rows: list[SmallPrimeSensitivityRecord],
    coverage_rows: list[LocalCoverageAuditRecord],
    invariant_rows: list[FreyInvariantSanityRecord],
    robustness_rows: list[LevelRobustnessRecord],
    skeleton_rows: list[TheoremSkeletonObligationRecord],
    valuation_rows: list[LocalValuationCaseRecord],
    lift_rows: list[ValuationMaskLiftRecord],
    reduction_rows: list[FreyReductionCaseRecord],
    case_coverage_rows: list[TraceFilterCaseCoverageRecord],
    local_gap_summary: LocalGapSummaryRecord,
    nonunit_rows: list[NonunitEliminationRecord],
    singular_reduction_rows: list[SingularReductionTraceRecord],
    frey_reduction_diagnostic_rows: list[FreyReductionDiagnosticRecord],
    tate_stub_rows: list[TateAlgorithmStubRecord],
    single_mask_pressure_rows: list[SingleMaskNewformPressureRecord],
    multiplicative_congruence_rows: list[MultiplicativeReductionCongruenceRecord],
    closure_score_rows: list[LocalCaseClosureScoreRecord],
    best_prime_rows: list[BestEliminatingPrimeRecord],
    cross_prime_rows: list[CrossPrimeBranchCompatibilityRecord],
    q3_audit_row: Q3ExceptionalityAuditRecord,
    best_route_rows: list[BestRouteSummaryRecord],
    quantifier_rows: list[QuantifierSafetyAuditRecord],
    dependency_rows: list[AssumptionDependencyRecord],
    nonunit_filter_rows: list[NonunitNewformFilterRecord],
    assumption_rows: list[AssumptionRecord],
    gap_rows: list[ProofGapRecord],
    known_mismatches: int,
    known_overpromotions: int,
) -> str:
    """Return the focused 5-4-5 Markdown report."""
    audit_label = str(audit_row.get("audit_review_label", "not_available")) if audit_row else "not_available"
    priority = str(audit_row.get("priority", "")) if audit_row else ""
    provenance_firsts = sorted(
        {
            f"newform_{row.newform_index}:q={row.prime}"
            for row in provenance_rows
            if row.is_first_eliminating_prime
        }
    )
    q3_profile = next((row for row in sensitivity_rows if row.profile_name == "exclude_q_3"), None)
    q17_profile = next((row for row in sensitivity_rows if row.profile_name == "use_only_q_ge_17"), None)
    coverage_gap_count = sum(1 for row in coverage_rows if row.coverage_label == "local_coverage_gap")
    level_220_row = next((row for row in robustness_rows if row.level == 220), None)
    nearby_incomplete = sum(1 for row in robustness_rows if row.level != 220 and row.robustness_label == "level_data_insufficient")
    focused_prime_text = ";".join(str(row.prime) for row in closure_score_rows) or "none"
    best_prime = best_prime_rows[0] if best_prime_rows else None
    cross_prime_summary = next((row for row in cross_prime_rows if row.newform_index == -1), None)
    best_route = best_route_rows[0] if best_route_rows else None
    quantifier_summary = next((row for row in quantifier_rows if row.newform_index == -1), None)
    dependency_summary = ";".join(
        f"{row.dependency_id}:{row.current_status}" for row in dependency_rows
    ) or "none"
    pressure_labels = sorted({row.prime_local_label for row in single_mask_pressure_rows})
    closure_labels = sorted({row.closure_label for row in closure_score_rows})
    focused_nonunit_note = (
        (
            "At least one focused eliminating prime has all tracked local branches closed by the audit; this is only "
            "`local_case_elimination_candidate` route evidence and keeps the review ceiling unchanged."
        )
        if "local_case_elimination_candidate" in closure_labels
        else (
            "Every focused eliminating prime has at least one surviving branch or still needs level-lowering/Tate justification, "
            "so the route keeps `local_coverage_gap`."
        )
    )
    lines = [
        "# Focused Modular Review: `(5,4,5)`",
        "",
        "Equation form: `A^5 + B^4 = C^5`.",
        "",
        "This is a human-review packet. It separates imported Sage facts from symbolic-template assumptions and open mathematical obligations. It does not certify a theorem, contradiction, or exclusion.",
        "",
        "## Route Status",
        "",
        f"- Current focused label: `{audit_label}`.",
        f"- Priority: `{priority or 'unknown'}`.",
        f"- Known-case mismatches: `{known_mismatches}`.",
        f"- Known-case overpromotions: `{known_overpromotions}`.",
        f"- Highest allowed label in this pipeline: `worth_human_modular_review`.",
        "",
        "## Verified Sage Facts",
        "",
        *_sage_fact_lines(sage_payload, import_row),
        "",
        "## Local Survivor Rows",
        "",
        *_unit_lines(unit_rows),
        "",
        "## Frey Template Validity Audit",
        "",
        "| component | classification | risk | next action |",
        "| --- | --- | --- | --- |",
    ]
    for row in validity_rows:
        lines.append(f"| `{row.component}` | `{row.classification}` | `{row.risk_level}` | {row.next_action} |")
    lines.extend(
        [
            "",
            "## Level 220 Audit",
            "",
            f"- Factorization: `{factorization_220()}`.",
            "- Level 220 is currently a `heuristic_symbolic` route-audit target, not a verified conductor or lowered level.",
            "",
            "| prime | exponent in 220 | why it appears | required assumption |",
            "| ---: | ---: | --- | --- |",
        ]
    )
    for row in prime_rows:
        lines.append(
            f"| {row.prime} | {row.exponent_in_level} | {row.reason_in_candidate_support} | {row.required_assumption} |"
        )
    lines.extend(
        [
            "",
            "## Level 220 Newforms",
            "",
            "| index | label | q-expansion data | status | notes |",
            "| ---: | --- | --- | --- | --- |",
        ]
    )
    for row in newform_rows:
        lines.append(
            f"| {row.newform_index} | `{row.label}` | `{row.q_expansion_data_available}` | `{row.status}` | {row.notes} |"
        )
    lines.extend(
        [
            "",
            "## Trace Comparison Audit",
            "",
            "| level | prime | good for level | Frey traces | newform traces | mode | classification |",
            "| ---: | ---: | --- | --- | --- | --- | --- |",
        ]
    )
    for row in trace_rows:
        lines.append(
            f"| {row.level} | {row.prime} | `{row.good_prime_for_level}` | "
            f"`{';'.join(row.frey_survivor_trace_values) or 'none'}` | "
            f"`{';'.join(row.newform_trace_values) or 'missing'}` | `{row.comparison_mode}` | "
            f"`{row.comparison_classification}` |"
        )
    lines.extend(
        [
            "",
            "The key trace warning: the imported narrow row is at `ell=11`, and `11` divides `220`. That makes it local route evidence, not yet a clean good-prime newform trace comparison.",
            "",
            "## Good-Prime Trace Audit",
            "",
            "The good-prime audit excludes primes dividing `220` and excludes the residual-prime candidate `5` by default. It is designed to replace the weak `ell=11` signal with trace comparisons at primes where level-220 newform coefficients can be meaningfully tested.",
            "",
            f"- Selected good primes: `{';'.join(str(row.prime) for row in good_prime_rows if row.selected) or 'none'}`.",
            f"- Newform coefficient JSON expected at: `{(run_dir / 'level_220_newform_coefficients.json').as_posix()}`.",
            f"- Coefficient import status: `{coefficient_summary.sage_status}`; schema valid: `{coefficient_summary.schema_valid}`.",
            f"- Imported coefficient rows: `{coefficient_summary.coefficient_row_count}`.",
            f"- Rational/integer coefficients: `{coefficient_summary.rational_integer_coefficient_count}`; non-rational coefficients: `{coefficient_summary.nonrational_coefficient_count}`; unclear coefficients: `{coefficient_summary.unclear_coefficient_count}`.",
            f"- Aggregate progress label: `{progress_row.progress_label}`.",
            f"- Usable comparisons: `{progress_row.usable_comparison_count}`.",
            f"- Coefficient-field blocked comparisons: `{progress_row.coefficient_field_unclear_count}`.",
            f"- Newforms surviving all available filters: `{progress_row.newforms_surviving_all_filters}` of `{progress_row.newform_count}`.",
            f"- Unresolved reasons: `{progress_row.unresolved_reasons or 'none'}`.",
            "",
            "### Frey Trace Possibilities At Good Primes",
            "",
            "| q | survivors | nonsingular | possible traces |",
            "| ---: | ---: | ---: | --- |",
        ]
    )
    for row in frey_trace_rows[:24]:
        lines.append(
            f"| {row.prime} | {row.survivor_triple_count} | {row.nonsingular_curve_count} | "
            f"`{';'.join(str(item) for item in row.possible_traces) or 'none'}` |"
        )
    lines.extend(
        [
            "",
            "### Congruence Filter Results",
            "",
            "| q | newform | coefficient | mode | classification | reason |",
            "| ---: | ---: | --- | --- | --- | --- |",
        ]
    )
    for row in filter_rows[:48]:
        lines.append(
            f"| {row.prime} | {row.newform_index} | `{row.newform_coefficient or 'missing'}` | "
            f"`{row.comparison_mode}` | `{row.filter_classification}` | {row.reason} |"
        )
    lines.extend(
        [
            "",
            "### Coefficient Field Summary",
            "",
            "| newform | q | coefficient | field kind | mod-5 reduction | status |",
            "| ---: | ---: | --- | --- | --- | --- |",
        ]
    )
    if coefficient_rows:
        for row in coefficient_rows[:48]:
            lines.append(
                f"| {row.newform_index} | {row.prime} | `{row.coefficient}` | `{row.coefficient_field_kind}` | "
                f"`{row.coefficient_mod_5 or 'missing'}` | `{row.row_status}` |"
            )
    else:
        lines.append("| none | none | missing | missing | missing | coefficient JSON not imported |")
    lines.extend(
        [
            "",
            "If both level-220 newforms are eventually eliminated by good-prime congruence filters, this packet must call that `trace_mismatch_candidate`, not a proof or contradiction. With missing q-expansion data, the correct label is `trace_data_insufficient`; with non-rational coefficients and no justified reduction above `5`, the correct label is `coefficient_field_blocked`.",
            "",
            "If coefficient-field handling blocks comparison, the next human check is to choose and justify the prime above `5` in the newform coefficient field, then redo the trace congruence in that residue field.",
            "",
            "## Trace Mismatch Robustness",
            "",
            f"- First eliminating primes: `{';'.join(provenance_firsts) or 'none'}`.",
            f"- Excluding `q=3`: `{q3_profile.sensitivity_label if q3_profile else 'missing'}` with `{q3_profile.eliminated_newform_count if q3_profile else 0}` eliminated newforms.",
            f"- Using only `q >= 17`: `{q17_profile.sensitivity_label if q17_profile else 'missing'}` with `{q17_profile.eliminated_newform_count if q17_profile else 0}` eliminated newforms.",
            f"- Local coverage gaps: `{coverage_gap_count}` selected good primes.",
            f"- Level 220 robustness label: `{level_220_row.robustness_label if level_220_row else 'missing'}`.",
            f"- Nearby levels still lacking coefficient data: `{nearby_incomplete}`.",
            f"- Local valuation scope label: `{local_gap_summary.trace_mismatch_scope_label}`.",
            f"- Overall local gap label: `{local_gap_summary.overall_local_gap_label}`.",
            f"- Focused eliminating primes: `{focused_prime_text}`.",
            f"- Best ranked eliminating prime: `{best_prime.prime if best_prime else 'missing'}` with label `{best_prime.closure_label if best_prime else 'missing'}`.",
            "",
            "### Trace Mismatch Provenance",
            "",
            "| newform | q | a_q | mode | classification | first eliminator |",
            "| ---: | ---: | --- | --- | --- | --- |",
        ]
    )
    for row in provenance_rows[:48]:
        lines.append(
            f"| {row.newform_index} | {row.prime} | `{row.newform_coefficient or 'missing'}` | "
            f"`{row.comparison_mode}` | `{row.filter_classification}` | `{row.is_first_eliminating_prime}` |"
        )
    lines.extend(
        [
            "",
            "### Small-Prime Sensitivity",
            "",
            "| profile | surviving | eliminated | first eliminators | label |",
            "| --- | ---: | ---: | --- | --- |",
        ]
    )
    for row in sensitivity_rows:
        lines.append(
            f"| `{row.profile_name}` | {row.surviving_newform_count} | {row.eliminated_newform_count} | "
            f"`{row.first_eliminating_primes or 'none'}` | `{row.sensitivity_label}` |"
        )
    lines.extend(
        [
            "",
            "### Local Coverage Audit",
            "",
            "| q | unit residue cases | zero-support cases | excluded cases | label |",
            "| ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in coverage_rows[:24]:
        lines.append(
            f"| {row.prime} | {row.residue_unit_solution_count} | {row.zero_support_solution_count} | "
            f"{row.cases_excluded_from_trace_comparison} | `{row.coverage_label}` |"
        )
    lines.extend(
        [
            "",
            "### Local Valuation And Frey Reduction Coverage",
            "",
            "| q | eliminated newforms | nonunit possible | nonunit unresolved | full local coverage | label |",
            "| ---: | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for row in case_coverage_rows[:24]:
        lines.append(
            f"| {row.prime} | {row.trace_filter_eliminates_newform_count} | {row.nonunit_locally_possible_count} | "
            f"{row.nonunit_unresolved_count} | `{row.full_local_coverage}` | `{row.coverage_label}` |"
        )
    lines.extend(
        [
            "",
            f"Local gap summary: `{local_gap_summary.overall_local_gap_label}`. Exact next lemma: {local_gap_summary.exact_next_human_lemma}",
            "",
            "### Focused Frey Reduction Diagnostics",
            "",
            "| q | mask | v_q(Delta) | v_q(c4) | v_q(c6) | reduction | standard trace |",
            "| ---: | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in frey_reduction_diagnostic_rows:
        lines.append(
            f"| {row.prime} | `{row.valuation_mask}` | `{row.discriminant_valuation}` | "
            f"`{row.c4_valuation}` | `{row.c6_valuation}` | `{row.reduction_type}` | "
            f"`{row.standard_trace_behavior_available}` |"
        )
    lines.extend(
        [
            "",
            "### Tate Algorithm Stub",
            "",
            "| q | mask | stub reduction | status | needs human Tate |",
            "| ---: | --- | --- | --- | --- |",
        ]
    )
    for row in tate_stub_rows:
        lines.append(
            f"| {row.prime} | `{row.valuation_mask}` | `{row.stub_reduction_type}` | "
            f"`{row.tate_algorithm_status}` | `{row.needs_human_tate_algorithm}` |"
        )
    lines.extend(
        [
            "",
            "### Single-Mask Newform Pressure",
            "",
            "| q | mask | unit trace | coefficients | branch classification | prime label |",
            "| ---: | --- | --- | --- | --- | --- |",
        ]
    )
    for row in single_mask_pressure_rows:
        lines.append(
            f"| {row.prime} | `{row.valuation_mask}` | `{row.unit_trace_result}` | "
            f"`{row.newform_coefficients}` | `{row.branch_classification}` | `{row.prime_local_label}` |"
        )
    lines.extend(
        [
            "",
            f"- Focused pressure labels: `{';'.join(pressure_labels) or 'none'}`.",
            "",
            "### Multiplicative-Reduction Congruence Audit",
            "",
            "| q | mask | newform | a_q mod 5 | allowed | classification |",
            "| ---: | --- | ---: | --- | --- | --- |",
        ]
    )
    for row in multiplicative_congruence_rows:
        lines.append(
            f"| {row.prime} | `{row.valuation_mask}` | {row.newform_index} | "
            f"`{row.coefficient_mod_5 or 'missing'}` | `{row.allowed_multiplicative_values_mod_5}` | "
            f"`{row.congruence_classification}` |"
        )
    lines.extend(
        [
            "",
            "### Local Case Closure Score",
            "",
            "| q | unit survivors | single survivors | fully eliminated | surviving | unresolved | label |",
            "| ---: | ---: | ---: | --- | --- | --- | --- |",
        ]
    )
    for row in closure_score_rows:
        lines.append(
            f"| {row.prime} | {row.unit_surviving_branch_count} | "
            f"{row.single_mask_surviving_branches} | `{row.fully_eliminated_newforms or 'none'}` | "
            f"`{row.surviving_newforms or 'none'}` | `{row.unresolved_newforms or 'none'}` | `{row.closure_label}` |"
        )
    lines.extend(
        [
            "",
            f"- Closure labels: `{';'.join(closure_labels) or 'none'}`.",
            f"- Focused pressure note: {focused_nonunit_note}",
            "",
            "### Best Eliminating Prime Ranking",
            "",
            "| rank | q | label | unit survivors | single-mask survivors | coverage gaps | q=3 penalty |",
            "| ---: | ---: | --- | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in best_prime_rows:
        lines.append(
            f"| {row.rank} | {row.prime} | `{row.closure_label}` | "
            f"{row.unit_surviving_branch_count} | {row.single_mask_surviving_branch_count} | "
            f"{row.multiplicative_coverage_gap_count} | {row.q3_reliance_penalty} |"
        )
    lines.extend(
        [
            "",
            f"- Best-prime route ceiling: `worth_human_modular_review`.",
            "",
            "### Cross-Prime Branch Compatibility",
            "",
            f"- Non-q=3 aggregate label: `{cross_prime_summary.compatibility_label if cross_prime_summary else 'missing'}`.",
            "",
            "| newform | compatible assignment | eliminated at q | allowed branch sets | label |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in cross_prime_rows:
        if row.newform_index == -1:
            continue
        lines.append(
            f"| `{row.newform_label}` | `{row.compatible_branch_assignment_exists}` | "
            f"`{row.eliminated_at_primes or 'none'}` | `{row.allowed_branch_sets}` | `{row.compatibility_label}` |"
        )
    lines.extend(
        [
            "",
            "### q=3 Exceptionality",
            "",
            f"- q=3 good relative to level 220: `{q3_audit_row.is_good_prime_for_level}`.",
            f"- q=3 closure label: `{q3_audit_row.q3_closure_label}`.",
            f"- Non-q=3 cross-prime label: `{q3_audit_row.non_q3_cross_prime_label}`.",
            f"- q=3 exceptionality label: `{q3_audit_row.q3_exceptionality_label}`.",
            f"- Small-prime risk flags: `{q3_audit_row.small_prime_risk_flags}`.",
            "",
            "### Best Route Summary",
            "",
            f"- Best route label: `{best_route.route_label if best_route else 'missing'}`.",
            "",
            "| rank | route option | label | primes | q=3 penalty |",
            "| ---: | --- | --- | --- | ---: |",
        ]
    )
    for row in best_route_rows:
        lines.append(
            f"| {row.rank} | `{row.route_option}` | `{row.route_label}` | "
            f"`{row.supporting_primes}` | {row.q3_reliance_penalty} |"
        )
    lines.extend(
        [
            "",
            "### Quantifier Safety Audit",
            "",
            f"- Aggregate quantifier label: `{quantifier_summary.quantifier_classification if quantifier_summary else 'data_insufficient'}`.",
            "- Safe quantifier: each level-220 newform needs one eliminating prime with complete same-prime branch coverage.",
            "- The audit rejects fixed branch coupling across different primes.",
            "",
            "| newform | eliminating q | complete q count | branch gaps | data gaps | fixed-branch dependency | label |",
            "| --- | --- | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for row in quantifier_rows:
        if row.newform_index == -1:
            continue
        lines.append(
            f"| `{row.newform_label}` | `{row.eliminated_primes or 'none'}` | "
            f"{row.complete_coverage_prime_count} | {row.branch_coverage_gap_count} | "
            f"{row.data_insufficient_count} | `{row.fixed_branch_dependency_detected}` | "
            f"`{row.quantifier_classification}` |"
        )
    lines.extend(
        [
            "",
            "### Conditional Theorem Packet",
            "",
            f"- Conditional packet label: `{quantifier_summary.quantifier_classification if quantifier_summary else 'data_insufficient'}`.",
            "- The packet states the primitive-solution setup, Frey object, assumed level lowering to 220, newform exhaustion, local eliminations, and open assumptions.",
            "- It remains route evidence only and keeps the ceiling `worth_human_modular_review`.",
            "",
            "### Assumption Dependency Graph",
            "",
            f"- Dependency summary: `{dependency_summary}`.",
            "- Final dependency node: quantifier safety depends on local branch coverage, which depends on reduction classification and coefficient comparison.",
            "",
            "### Adversarial Review Checklist",
            "",
            "- Checklist sidecar asks whether level 220 is truly lowered, whether q=13/q=17/q=41 are good relative to the true conductor, whether multiplicative branches and mod-5 comparisons are justified, and whether q | ABC cases survive.",
            "",
            "### Focused Eliminating-Prime Nonunit Branch Audit",
            "",
            "| q | unit eliminations | possible nonunit masks | unresolved masks | condition masks | full nonunit resolution | safe label |",
            "| ---: | ---: | --- | --- | --- | --- | --- |",
        ]
    )
    for row in nonunit_filter_rows:
        lines.append(
            f"| {row.prime} | {row.unit_eliminated_newform_count} | `{row.possible_nonunit_masks or 'none'}` | "
            f"`{row.unresolved_nonunit_masks or 'none'}` | `{row.single_mask_condition_masks or row.reduction_argument_masks or 'none'}` | "
            f"`{row.full_nonunit_resolution}` | `{row.safe_label}` |"
        )
    lines.extend(
        [
            "",
            f"- Focused eliminating primes: `{focused_prime_text}`.",
            f"- Best ranked eliminating prime: `{best_prime.prime if best_prime else 'missing'}` with label `{best_prime.closure_label if best_prime else 'missing'}`.",
            "- Pairwise nonunit masks are primitive-forbidden, but `A_only`, `B_only`, and `C_only` remain locally stable and need a separate Frey reduction argument.",
            f"- {focused_nonunit_note}",
            "",
            "### Level Robustness",
            "",
            "| level | newforms | coefficient status | trace status | label |",
            "| ---: | ---: | --- | --- | --- |",
        ]
    )
    for row in robustness_rows:
        lines.append(
            f"| {row.level} | {row.newform_count} | `{row.coefficient_status}` | "
            f"`{row.trace_filter_status}` | `{row.robustness_label}` |"
        )
    lines.extend(
        [
            "",
            "### Theorem Skeleton Summary",
            "",
            "| obligation | status | risk | next action |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in skeleton_rows:
        lines.append(
            f"| `{row.obligation_id}` | `{row.status}` | `{row.risk_level}` | {row.next_action} |"
        )
    lines.extend(
        [
            "",
            "The exact next human mathematical task is to prove the Frey attachment, conductor/level-lowering, residual mod-5 irreducibility, level-220 target-space exhaustion, and local-coverage lemmas needed to turn this route evidence into a valid modular argument.",
            "",
            "## Assumption Register",
            "",
            "| id | status | risk | required for | next action |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in assumption_rows:
        lines.append(f"| `{row.assumption_id}` | `{row.status}` | `{row.risk_level}` | {row.required_for} | {row.next_action} |")
    lines.extend(
        [
            "",
            "## Gap Summary",
            "",
            "| category | status | risk | required next lemma |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in gap_rows:
        lines.append(
            f"| `{row.gap_category}` | `{row.gap_status}` | `{row.risk_level}` | {row.required_next_lemma} |"
        )
    lines.extend(
        [
            "",
            "## Exact Next Theorem Or Lemma",
            "",
            "A human should next prove the Frey-curve attachment and conductor/level-lowering package for `A^5 + B^4 = C^5`: every primitive solution gives the stated Frey object; the residual representation at the justified modulus is irreducible; the true conductor lowers to the claimed comparison level; the multiplicative branches satisfy `a_q(f) == +/-(q+1) mod 5` at q in `{3,13,17,41,61}` where used; the quantifier-safe cross-prime route uses an exists-prime-per-newform elimination; and the two level-220 newforms, with actual q-expansion coefficients at good primes, fail or pass the justified trace congruence test.",
            "",
            "## Timeout Retry Note",
            "",
            "The timeout retry manifest remains focused on `(3,5,5)`, `(5,5,7)`, and `(7,7,4)`. Those retries should not change the interpretation of this focused `(5,4,5)` packet unless new data is explicitly imported and this report is regenerated.",
            "",
            "## Generated Sidecars",
            "",
            f"- `{(run_dir / 'frey_template_validity_545.csv').as_posix()}`",
            f"- `{(run_dir / 'level_220_prime_audit.csv').as_posix()}`",
            f"- `{(run_dir / 'level_220_newforms.csv').as_posix()}`",
            f"- `{(run_dir / 'trace_comparison_545.csv').as_posix()}`",
            f"- `{(run_dir / 'good_prime_list_545.csv').as_posix()}`",
            f"- `{(run_dir / 'sage_level_220_newform_expander.sage').as_posix()}`",
            f"- `{(run_dir / 'frey_trace_possibilities_545.csv').as_posix()}`",
            f"- `{(run_dir / 'trace_congruence_filter_545.csv').as_posix()}`",
            f"- `{(run_dir / 'obstruction_progress_545.csv').as_posix()}`",
            f"- `{(run_dir / 'level_220_coefficient_import_summary.csv').as_posix()}`",
            f"- `{(run_dir / 'level_220_coefficient_rows.csv').as_posix()}`",
            f"- `{(run_dir / 'trace_mismatch_provenance_545.csv').as_posix()}`",
            f"- `{(run_dir / 'TRACE_MISMATCH_PROVENANCE_545.md').as_posix()}`",
            f"- `{(run_dir / 'small_prime_sensitivity_545.csv').as_posix()}`",
            f"- `{(run_dir / 'SMALL_PRIME_SENSITIVITY_545.md').as_posix()}`",
            f"- `{(run_dir / 'local_coverage_audit_545.csv').as_posix()}`",
            f"- `{(run_dir / 'LOCAL_COVERAGE_AUDIT_545.md').as_posix()}`",
            f"- `{(run_dir / 'frey_invariant_sanity_545.csv').as_posix()}`",
            f"- `{(run_dir / 'FREY_INVARIANT_SANITY_545.md').as_posix()}`",
            f"- `{(run_dir / 'level_robustness_545.csv').as_posix()}`",
            f"- `{(run_dir / 'LEVEL_220_ROBUSTNESS_545.md').as_posix()}`",
            f"- `{(run_dir / 'THEOREM_SKELETON_545.md').as_posix()}`",
            f"- `{(run_dir / 'theorem_skeleton_obligations_545.csv').as_posix()}`",
            f"- `{(run_dir / 'local_valuation_cases_545.csv').as_posix()}`",
            f"- `{(run_dir / 'valuation_mask_lift_545.csv').as_posix()}`",
            f"- `{(run_dir / 'frey_reduction_cases_545.csv').as_posix()}`",
            f"- `{(run_dir / 'trace_filter_case_coverage_545.csv').as_posix()}`",
            f"- `{(run_dir / 'local_gap_summary_545.csv').as_posix()}`",
            f"- `{(run_dir / 'LOCAL_GAP_SUMMARY_545.md').as_posix()}`",
            f"- `{(run_dir / 'nonunit_eliminations_545.csv').as_posix()}`",
            f"- `{(run_dir / 'singular_reduction_traces_545.csv').as_posix()}`",
            f"- `{(run_dir / 'frey_reduction_diagnostics_545.csv').as_posix()}`",
            f"- `{(run_dir / 'tate_algorithm_stub_545.csv').as_posix()}`",
            f"- `{(run_dir / 'single_mask_newform_pressure_545.csv').as_posix()}`",
            f"- `{(run_dir / 'multiplicative_reduction_congruence_545.csv').as_posix()}`",
            f"- `{(run_dir / 'local_case_closure_score_545.csv').as_posix()}`",
            f"- `{(run_dir / 'best_eliminating_prime_545.csv').as_posix()}`",
            f"- `{(run_dir / 'BEST_ELIMINATING_PRIME_545.md').as_posix()}`",
            f"- `{(run_dir / 'cross_prime_branch_compatibility_545.csv').as_posix()}`",
            f"- `{(run_dir / 'Q3_EXCEPTIONALITY_AUDIT_545.md').as_posix()}`",
            f"- `{(run_dir / 'BEST_ROUTE_SUMMARY_545.md').as_posix()}`",
            f"- `{(run_dir / 'quantifier_safety_audit_545.csv').as_posix()}`",
            f"- `{(run_dir / 'QUANTIFIER_SAFETY_AUDIT_545.md').as_posix()}`",
            f"- `{(run_dir / 'CONDITIONAL_THEOREM_PACKET_545.md').as_posix()}`",
            f"- `{(run_dir / 'assumption_dependency_graph_545.csv').as_posix()}`",
            f"- `{(run_dir / 'ASSUMPTION_DEPENDENCY_GRAPH_545.md').as_posix()}`",
            f"- `{(run_dir / 'ADVERSARIAL_REVIEW_CHECKLIST_545.md').as_posix()}`",
            f"- `{(run_dir / 'nonunit_newform_filter_545.csv').as_posix()}`",
            f"- `{(run_dir / 'LOCAL_CASE_DECISION_TREE_545.md').as_posix()}`",
            f"- `{(run_dir / 'assumption_register_545.csv').as_posix()}`",
            f"- `{(run_dir / 'proof_gap_summary.csv').as_posix()}`",
            f"- `{(run_dir / 'proof_gap_report.md').as_posix()}`",
            "",
        ]
    )
    return "\n".join(lines)


def generate_focused_545_review(run_dir: Path) -> Focused545Artifacts:
    """Generate the focused `(5,4,5)` review packet in `run_dir`."""
    run_dir.mkdir(parents=True, exist_ok=True)
    sage_payload = _load_sage_payload(run_dir)
    import_rows = _read_csv(run_dir / "sage_import_results.csv")
    audit_rows = _read_csv(run_dir / "modular_candidate_deep_audit.csv")
    unit_rows = _read_csv(run_dir / "unit_survivor_summary.csv")
    level_rows = _read_csv(run_dir / "level_explanations.csv")
    matrix_rows = _read_csv(run_dir / "newform_trace_matrix.csv")
    known_rows = _read_csv(run_dir / "sage_known_case_calibration.csv")
    if not known_rows:
        known_rows = _read_csv(run_dir / "known_case_calibration_summary.csv")

    import_row = _first(import_rows)
    audit_row = _first(audit_rows)
    level_220_row = next((row for row in level_rows if row.get("signature") == SIGNATURE_545 and row.get("level") == "220"), None)
    filtered_units = _filter(unit_rows)
    filtered_matrix = _filter(matrix_rows)
    known_mismatches, known_overpromotions = _status_counts(known_rows)

    validity_rows = build_frey_template_validity_audit_545(
        sage_payload=sage_payload,
        level_row=level_220_row,
        audit_row=audit_row,
    )
    prime_rows = build_level_220_prime_records()
    newform_rows = build_level_220_newform_records(sage_payload)
    trace_rows = build_trace_comparison_audit_545(filtered_matrix)
    good_prime_rows = select_good_primes_545(level=220, bound=100, allow_residual_prime=False)
    frey_trace_rows = build_frey_trace_possibilities_545(good_prime_rows)
    coefficient_path = run_dir / "level_220_newform_coefficients.json"
    coefficient_summary, coefficient_rows = import_level_220_newform_coefficients(coefficient_path)
    coefficient_payload = {
        "newform_count": coefficient_summary.newform_count,
        "coefficient_rows": [row.to_flat_dict() for row in coefficient_rows],
    }
    raw_coefficient_payload = load_level_220_coefficients(coefficient_path)
    if not coefficient_rows and raw_coefficient_payload:
        coefficient_payload = raw_coefficient_payload
    newform_count = coefficient_summary.newform_count or int(sage_payload.get("newform_count", 0) or 0)
    filter_rows = build_trace_congruence_filter_545(
        good_prime_rows=good_prime_rows,
        frey_trace_rows=frey_trace_rows,
        coefficient_payload=coefficient_payload,
        newform_count=newform_count,
        residual_modulus=5,
    )
    progress_row = score_obstruction_progress_545(filter_rows, newform_count=newform_count)
    provenance_rows = build_trace_mismatch_provenance_545(filter_rows)
    sensitivity_rows = build_small_prime_sensitivity_545(filter_rows, newform_count=newform_count)
    coverage_rows = build_local_coverage_audit_545(good_prime_rows, frey_trace_rows)
    invariant_rows = build_frey_invariant_sanity_545()
    robustness_rows = build_level_robustness_545(
        coefficient_summary=coefficient_summary,
        progress_row=progress_row,
    )
    valuation_rows = build_local_valuation_cases_545(good_prime_rows)
    lift_rows = build_valuation_mask_lifts_545(valuation_rows)
    reduction_rows = build_frey_reduction_cases_545(valuation_rows, lift_rows)
    frey_reduction_diagnostic_rows = build_frey_reduction_diagnostics_545(good_prime_rows)
    tate_stub_rows = build_tate_algorithm_stub_545(frey_reduction_diagnostic_rows)
    single_mask_pressure_rows = build_single_mask_newform_pressure_545(
        filter_rows,
        frey_reduction_diagnostic_rows,
        tate_stub_rows,
    )
    multiplicative_congruence_rows = build_multiplicative_reduction_congruences_545(
        coefficient_rows,
        frey_reduction_diagnostic_rows,
        newform_count=newform_count or 2,
    )
    closure_score_rows = build_local_case_closure_scores_545(
        filter_rows,
        multiplicative_congruence_rows,
        newform_count=newform_count or 2,
    )
    best_prime_rows = build_best_eliminating_prime_545(closure_score_rows)
    nonunit_rows = build_nonunit_eliminations_545(good_prime_rows)
    cross_prime_rows = build_cross_prime_branch_compatibility_545(
        filter_rows,
        multiplicative_congruence_rows,
        nonunit_rows,
        newform_count=newform_count or 2,
    )
    q3_audit_row = build_q3_exceptionality_audit_545(closure_score_rows, cross_prime_rows)
    best_route_rows = build_best_route_summary_545(closure_score_rows, cross_prime_rows, q3_audit_row)
    quantifier_rows = build_quantifier_safety_audit_545(
        filter_rows,
        multiplicative_congruence_rows,
        nonunit_rows,
        cross_prime_rows,
        newform_count=newform_count or 2,
    )
    dependency_rows = build_assumption_dependency_graph_545(quantifier_rows)
    case_coverage_rows = build_trace_filter_case_coverage_545(
        filter_rows,
        reduction_rows,
        pressure_rows=single_mask_pressure_rows,
        closure_rows=closure_score_rows,
    )
    local_gap_summary = build_local_gap_summary_545(case_coverage_rows)
    singular_reduction_rows = build_singular_reduction_traces_545(nonunit_rows)
    nonunit_filter_rows = build_nonunit_newform_filters_545(
        filter_rows,
        nonunit_rows,
        singular_reduction_rows,
        pressure_rows=single_mask_pressure_rows,
        closure_rows=closure_score_rows,
    )
    skeleton_rows = build_theorem_skeleton_obligations_545(
        progress_row=progress_row,
        sensitivity_rows=sensitivity_rows,
        coverage_rows=coverage_rows,
        level_rows=robustness_rows,
        local_gap_summary=local_gap_summary,
    )
    assumption_rows = build_assumption_register_545()
    gap_rows = build_proof_gap_records_545()

    focused_report_path = run_dir / "FOCUSED_545_REVIEW.md"
    frey_path = run_dir / "frey_template_validity_545.csv"
    prime_path = run_dir / "level_220_prime_audit.csv"
    newforms_path = run_dir / "level_220_newforms.csv"
    trace_path = run_dir / "trace_comparison_545.csv"
    good_prime_path = run_dir / "good_prime_list_545.csv"
    sage_expander_path = write_sage_level_220_newform_expander(run_dir)
    frey_trace_path = run_dir / "frey_trace_possibilities_545.csv"
    filter_path = run_dir / "trace_congruence_filter_545.csv"
    progress_path = run_dir / "obstruction_progress_545.csv"
    coefficient_summary_path = run_dir / "level_220_coefficient_import_summary.csv"
    coefficient_rows_path = run_dir / "level_220_coefficient_rows.csv"
    provenance_path = run_dir / "trace_mismatch_provenance_545.csv"
    provenance_report_path = run_dir / "TRACE_MISMATCH_PROVENANCE_545.md"
    sensitivity_path = run_dir / "small_prime_sensitivity_545.csv"
    sensitivity_report_path = run_dir / "SMALL_PRIME_SENSITIVITY_545.md"
    coverage_path = run_dir / "local_coverage_audit_545.csv"
    coverage_report_path = run_dir / "LOCAL_COVERAGE_AUDIT_545.md"
    invariant_path = run_dir / "frey_invariant_sanity_545.csv"
    invariant_report_path = run_dir / "FREY_INVARIANT_SANITY_545.md"
    robustness_path = run_dir / "level_robustness_545.csv"
    robustness_report_path = run_dir / "LEVEL_220_ROBUSTNESS_545.md"
    skeleton_path = run_dir / "THEOREM_SKELETON_545.md"
    skeleton_obligations_path = run_dir / "theorem_skeleton_obligations_545.csv"
    valuation_path = run_dir / "local_valuation_cases_545.csv"
    lift_path = run_dir / "valuation_mask_lift_545.csv"
    reduction_path = run_dir / "frey_reduction_cases_545.csv"
    case_coverage_path = run_dir / "trace_filter_case_coverage_545.csv"
    local_gap_path = run_dir / "local_gap_summary_545.csv"
    local_gap_report_path = run_dir / "LOCAL_GAP_SUMMARY_545.md"
    nonunit_path = run_dir / "nonunit_eliminations_545.csv"
    singular_reduction_path = run_dir / "singular_reduction_traces_545.csv"
    frey_reduction_diagnostics_path = run_dir / "frey_reduction_diagnostics_545.csv"
    tate_algorithm_stub_path = run_dir / "tate_algorithm_stub_545.csv"
    single_mask_pressure_path = run_dir / "single_mask_newform_pressure_545.csv"
    multiplicative_congruence_path = run_dir / "multiplicative_reduction_congruence_545.csv"
    closure_score_path = run_dir / "local_case_closure_score_545.csv"
    best_prime_path = run_dir / "best_eliminating_prime_545.csv"
    best_prime_report_path = run_dir / "BEST_ELIMINATING_PRIME_545.md"
    cross_prime_path = run_dir / "cross_prime_branch_compatibility_545.csv"
    q3_exceptionality_path = run_dir / "Q3_EXCEPTIONALITY_AUDIT_545.md"
    best_route_path = run_dir / "BEST_ROUTE_SUMMARY_545.md"
    quantifier_safety_path = run_dir / "quantifier_safety_audit_545.csv"
    quantifier_safety_report_path = run_dir / "QUANTIFIER_SAFETY_AUDIT_545.md"
    conditional_packet_path = run_dir / "CONDITIONAL_THEOREM_PACKET_545.md"
    dependency_graph_path = run_dir / "assumption_dependency_graph_545.csv"
    dependency_graph_report_path = run_dir / "ASSUMPTION_DEPENDENCY_GRAPH_545.md"
    adversarial_checklist_path = run_dir / "ADVERSARIAL_REVIEW_CHECKLIST_545.md"
    nonunit_filter_path = run_dir / "nonunit_newform_filter_545.csv"
    local_case_decision_tree_path = run_dir / "LOCAL_CASE_DECISION_TREE_545.md"
    assumptions_path = run_dir / "assumption_register_545.csv"
    gaps_path = run_dir / "proof_gap_summary.csv"
    gap_report_path = run_dir / "proof_gap_report.md"

    _write_csv(frey_path, [row.to_flat_dict() for row in validity_rows])
    _write_csv(prime_path, [row.to_flat_dict() for row in prime_rows])
    _write_csv(newforms_path, [row.to_flat_dict() for row in newform_rows])
    _write_csv(trace_path, [row.to_flat_dict() for row in trace_rows])
    _write_csv(good_prime_path, [row.to_flat_dict() for row in good_prime_rows])
    _write_csv(frey_trace_path, [row.to_flat_dict() for row in frey_trace_rows])
    _write_csv(filter_path, [row.to_flat_dict() for row in filter_rows])
    _write_csv(progress_path, [progress_row.to_flat_dict()])
    _write_csv(coefficient_summary_path, [coefficient_summary.to_flat_dict()])
    _write_csv(coefficient_rows_path, [row.to_flat_dict() for row in coefficient_rows])
    _write_csv(provenance_path, [row.to_flat_dict() for row in provenance_rows])
    _write_csv(sensitivity_path, [row.to_flat_dict() for row in sensitivity_rows])
    _write_csv(coverage_path, [row.to_flat_dict() for row in coverage_rows])
    _write_csv(invariant_path, [row.to_flat_dict() for row in invariant_rows])
    _write_csv(robustness_path, [row.to_flat_dict() for row in robustness_rows])
    _write_csv(skeleton_obligations_path, [row.to_flat_dict() for row in skeleton_rows])
    _write_csv(valuation_path, [row.to_flat_dict() for row in valuation_rows])
    _write_csv(lift_path, [row.to_flat_dict() for row in lift_rows])
    _write_csv(reduction_path, [row.to_flat_dict() for row in reduction_rows])
    _write_csv(case_coverage_path, [row.to_flat_dict() for row in case_coverage_rows])
    _write_csv(local_gap_path, [local_gap_summary.to_flat_dict()])
    _write_csv(nonunit_path, [row.to_flat_dict() for row in nonunit_rows])
    _write_csv(singular_reduction_path, [row.to_flat_dict() for row in singular_reduction_rows])
    _write_csv(frey_reduction_diagnostics_path, [row.to_flat_dict() for row in frey_reduction_diagnostic_rows])
    _write_csv(tate_algorithm_stub_path, [row.to_flat_dict() for row in tate_stub_rows])
    _write_csv(single_mask_pressure_path, [row.to_flat_dict() for row in single_mask_pressure_rows])
    _write_csv(multiplicative_congruence_path, [row.to_flat_dict() for row in multiplicative_congruence_rows])
    _write_csv(closure_score_path, [row.to_flat_dict() for row in closure_score_rows])
    _write_csv(best_prime_path, [row.to_flat_dict() for row in best_prime_rows])
    _write_csv(cross_prime_path, [row.to_flat_dict() for row in cross_prime_rows])
    _write_csv(quantifier_safety_path, [row.to_flat_dict() for row in quantifier_rows])
    _write_csv(dependency_graph_path, [row.to_flat_dict() for row in dependency_rows])
    _write_csv(nonunit_filter_path, [row.to_flat_dict() for row in nonunit_filter_rows])
    _write_csv(assumptions_path, [row.to_flat_dict() for row in assumption_rows])
    _write_csv(gaps_path, [row.to_flat_dict() for row in gap_rows])
    provenance_report_path.write_text(trace_mismatch_provenance_markdown(provenance_rows), encoding="utf-8")
    sensitivity_report_path.write_text(small_prime_sensitivity_markdown(sensitivity_rows), encoding="utf-8")
    coverage_report_path.write_text(local_coverage_audit_markdown(coverage_rows), encoding="utf-8")
    invariant_report_path.write_text(frey_invariant_sanity_markdown(invariant_rows), encoding="utf-8")
    robustness_report_path.write_text(level_robustness_markdown(robustness_rows), encoding="utf-8")
    skeleton_path.write_text(theorem_skeleton_markdown(skeleton_rows), encoding="utf-8")
    local_gap_report_path.write_text(local_gap_summary_markdown(local_gap_summary), encoding="utf-8")
    best_prime_report_path.write_text(best_eliminating_prime_545_markdown(best_prime_rows), encoding="utf-8")
    q3_exceptionality_path.write_text(q3_exceptionality_audit_545_markdown(q3_audit_row), encoding="utf-8")
    best_route_path.write_text(best_route_summary_545_markdown(best_route_rows), encoding="utf-8")
    quantifier_safety_report_path.write_text(quantifier_safety_audit_545_markdown(quantifier_rows), encoding="utf-8")
    conditional_packet_path.write_text(
        conditional_theorem_packet_545_markdown(quantifier_rows, dependency_rows),
        encoding="utf-8",
    )
    dependency_graph_report_path.write_text(
        assumption_dependency_graph_545_markdown(dependency_rows),
        encoding="utf-8",
    )
    adversarial_checklist_path.write_text(
        adversarial_review_checklist_545_markdown(quantifier_rows, dependency_rows),
        encoding="utf-8",
    )
    local_case_decision_tree_path.write_text(
        local_case_decision_tree_545_markdown(
            filter_rows=filter_rows,
            nonunit_rows=nonunit_rows,
            reduction_rows=singular_reduction_rows,
            newform_filter_rows=nonunit_filter_rows,
            pressure_rows=single_mask_pressure_rows,
            multiplicative_rows=multiplicative_congruence_rows,
            closure_rows=closure_score_rows,
        ),
        encoding="utf-8",
    )
    gap_report_path.write_text(proof_gap_report_markdown(output_dir=run_dir, rows=gap_rows), encoding="utf-8")
    focused_report_path.write_text(
        focused_545_markdown(
            run_dir=run_dir,
            sage_payload=sage_payload,
            import_row=import_row,
            audit_row=audit_row,
            unit_rows=filtered_units,
            validity_rows=validity_rows,
            prime_rows=prime_rows,
            newform_rows=newform_rows,
            trace_rows=trace_rows,
            good_prime_rows=good_prime_rows,
            frey_trace_rows=frey_trace_rows,
            filter_rows=filter_rows,
            progress_row=progress_row,
            coefficient_summary=coefficient_summary,
            coefficient_rows=coefficient_rows,
            provenance_rows=provenance_rows,
            sensitivity_rows=sensitivity_rows,
            coverage_rows=coverage_rows,
            invariant_rows=invariant_rows,
            robustness_rows=robustness_rows,
            skeleton_rows=skeleton_rows,
            valuation_rows=valuation_rows,
            lift_rows=lift_rows,
            reduction_rows=reduction_rows,
            case_coverage_rows=case_coverage_rows,
            local_gap_summary=local_gap_summary,
            nonunit_rows=nonunit_rows,
            singular_reduction_rows=singular_reduction_rows,
            frey_reduction_diagnostic_rows=frey_reduction_diagnostic_rows,
            tate_stub_rows=tate_stub_rows,
            single_mask_pressure_rows=single_mask_pressure_rows,
            multiplicative_congruence_rows=multiplicative_congruence_rows,
            closure_score_rows=closure_score_rows,
            best_prime_rows=best_prime_rows,
            cross_prime_rows=cross_prime_rows,
            q3_audit_row=q3_audit_row,
            best_route_rows=best_route_rows,
            quantifier_rows=quantifier_rows,
            dependency_rows=dependency_rows,
            nonunit_filter_rows=nonunit_filter_rows,
            assumption_rows=assumption_rows,
            gap_rows=gap_rows,
            known_mismatches=known_mismatches,
            known_overpromotions=known_overpromotions,
        ),
        encoding="utf-8",
    )
    return Focused545Artifacts(
        focused_report_path=focused_report_path.as_posix(),
        frey_template_validity_path=frey_path.as_posix(),
        level_220_prime_audit_path=prime_path.as_posix(),
        level_220_newforms_path=newforms_path.as_posix(),
        trace_comparison_path=trace_path.as_posix(),
        good_prime_list_path=good_prime_path.as_posix(),
        sage_newform_expander_path=sage_expander_path.as_posix(),
        frey_trace_possibilities_path=frey_trace_path.as_posix(),
        trace_congruence_filter_path=filter_path.as_posix(),
        obstruction_progress_path=progress_path.as_posix(),
        coefficient_import_summary_path=coefficient_summary_path.as_posix(),
        coefficient_import_rows_path=coefficient_rows_path.as_posix(),
        trace_mismatch_provenance_path=provenance_path.as_posix(),
        trace_mismatch_provenance_report_path=provenance_report_path.as_posix(),
        small_prime_sensitivity_path=sensitivity_path.as_posix(),
        small_prime_sensitivity_report_path=sensitivity_report_path.as_posix(),
        local_coverage_audit_path=coverage_path.as_posix(),
        local_coverage_audit_report_path=coverage_report_path.as_posix(),
        frey_invariant_sanity_path=invariant_path.as_posix(),
        frey_invariant_sanity_report_path=invariant_report_path.as_posix(),
        level_robustness_path=robustness_path.as_posix(),
        level_robustness_report_path=robustness_report_path.as_posix(),
        theorem_skeleton_path=skeleton_path.as_posix(),
        theorem_skeleton_obligations_path=skeleton_obligations_path.as_posix(),
        local_valuation_cases_path=valuation_path.as_posix(),
        valuation_mask_lift_path=lift_path.as_posix(),
        frey_reduction_cases_path=reduction_path.as_posix(),
        trace_filter_case_coverage_path=case_coverage_path.as_posix(),
        local_gap_summary_path=local_gap_path.as_posix(),
        local_gap_summary_report_path=local_gap_report_path.as_posix(),
        nonunit_eliminations_path=nonunit_path.as_posix(),
        singular_reduction_traces_path=singular_reduction_path.as_posix(),
        frey_reduction_diagnostics_path=frey_reduction_diagnostics_path.as_posix(),
        tate_algorithm_stub_path=tate_algorithm_stub_path.as_posix(),
        single_mask_newform_pressure_path=single_mask_pressure_path.as_posix(),
        multiplicative_reduction_congruence_path=multiplicative_congruence_path.as_posix(),
        local_case_closure_score_path=closure_score_path.as_posix(),
        best_eliminating_prime_path=best_prime_path.as_posix(),
        best_eliminating_prime_report_path=best_prime_report_path.as_posix(),
        cross_prime_branch_compatibility_path=cross_prime_path.as_posix(),
        q3_exceptionality_audit_report_path=q3_exceptionality_path.as_posix(),
        best_route_summary_report_path=best_route_path.as_posix(),
        quantifier_safety_audit_path=quantifier_safety_path.as_posix(),
        quantifier_safety_audit_report_path=quantifier_safety_report_path.as_posix(),
        conditional_theorem_packet_path=conditional_packet_path.as_posix(),
        assumption_dependency_graph_path=dependency_graph_path.as_posix(),
        assumption_dependency_graph_report_path=dependency_graph_report_path.as_posix(),
        adversarial_review_checklist_path=adversarial_checklist_path.as_posix(),
        nonunit_newform_filter_path=nonunit_filter_path.as_posix(),
        local_case_decision_tree_path=local_case_decision_tree_path.as_posix(),
        assumption_register_path=assumptions_path.as_posix(),
        proof_gap_summary_path=gaps_path.as_posix(),
        proof_gap_report_path=gap_report_path.as_posix(),
    )
