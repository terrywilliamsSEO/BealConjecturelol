"""Known-case calibration harness for the RSG pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
import random
from pathlib import Path
from typing import Iterable

from .artifact_explainer import explain_artifacts
from .calibration_confusion_matrix import CalibrationMatrixRecord, build_calibration_confusion_matrix
from .cross_prime_trace_compatibility import analyze_cross_prime_traces
from .finite_field_trace_probe import trace_probes_for_geometries
from .frey_template_library import build_template_records, candidate_frey_template
from .known_case_library import KnownCase, load_known_cases
from .modular_route_classifier import classify_modular_routes
from .modular_shadow_engine import build_modular_shadow_routes
from .padic_lift_audit import audit_padic_lifts
from .padic_unit_lift import analyze_padic_unit_lifts
from .primitive_obstruction_classifier import classify_primitive_obstructions
from .route_prior_model import RoutePriorScore, score_route_priors
from .route_collision_resolver import (
    RouteCollisionRecord,
    resolved_known_mismatch_rows,
    resolve_route_collision,
    route_collision_report_markdown,
    still_blocked_mismatch_rows,
)
from .rsg_residue_engine import ResidueSweepResult, Signature, run_signature_prime
from .sage_export_scripts import SageExportRecord, export_sage_scripts
from .signature_family_expander import FamilyExpansionRecord, expand_signature_families
from .terrain_report_generator import (
    remaining_true_mismatch_rows,
    theorem_terrain_report_markdown,
    theorem_terrain_summary_rows,
)
from .theorem_terrain_classifier import TheoremTerrainRecord, classify_theorem_terrain
from .unit_survivor_geometry import analyze_sparse_unit_geometries
from .zero_support_engine import analyze_zero_support_results


@dataclass(frozen=True)
class KnownCaseCalibrationRecord:
    """Aggregate route comparison for one known-case signature."""

    case_id: str
    signature: Signature
    signature_text: str
    family_label: str
    known_status: str
    expected_route: str
    terrain_label: str
    structural_terrain_labels: tuple[str, ...]
    known_status_label: str
    theorem_route_label: str
    theorem_match_id: str
    should_promote_without_external_check: bool
    artifact_collision_expected: bool
    should_resolve_to: str
    pre_collision_route_label: str
    collision_class: str
    collision_resolved_route_label: str
    collision_rationale: str
    prime_count: int
    local_obstruction_rows: int
    mandatory_single_divisor_rows: int
    sparse_unit_rows: int
    artifact_rows: int
    nonartifact_sparse_rows: int
    padic_descent_rows: int
    unit_lift_rigid_or_collapsed_rows: int
    trace_rigid_rows: int
    newform_check_rows: int
    frey_template_candidate_rows: int
    average_template_confidence: float
    strongest_prime: int
    strongest_system_signal: str
    system_route_label: str
    actual_route_label: str
    comparison_flag: str
    notes: str
    source_placeholder: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signature"] = self.signature_text
        data["structural_terrain_labels"] = ";".join(self.structural_terrain_labels)
        return data


@dataclass(frozen=True)
class KnownCaseCalibrationArtifacts:
    """All generated calibration artifacts."""

    case_records: list[KnownCaseCalibrationRecord]
    terrain_records: list[TheoremTerrainRecord]
    collision_records: list[RouteCollisionRecord]
    route_matrix_records: list[CalibrationMatrixRecord]
    terrain_summary_rows: list[dict[str, object]]
    remaining_true_mismatch_rows: list[dict[str, object]]
    resolved_known_mismatch_rows: list[dict[str, object]]
    still_blocked_mismatch_rows: list[dict[str, object]]
    family_expansion_records: list[FamilyExpansionRecord]
    route_prior_scores: list[RoutePriorScore]
    sage_export_records: list[SageExportRecord]
    report_markdown: str
    terrain_report_markdown: str
    collision_report_markdown: str


def _signature_text(signature: Signature) -> str:
    return "-".join(str(part) for part in signature)


def _run_known_case_residues(
    signatures: Iterable[Signature],
    primes: Iterable[int],
    *,
    compute_lift: bool,
    control_samples: int,
    seed: int,
) -> list[ResidueSweepResult]:
    results: list[ResidueSweepResult] = []
    for sig_index, signature in enumerate(sorted(set(signatures))):
        for prime_index, ell in enumerate(primes):
            rng = random.Random(seed + sig_index * 503 + prime_index * 3251 + ell)
            results.append(
                run_signature_prime(
                    signature,
                    ell,
                    compute_lift=compute_lift,
                    control_samples=control_samples,
                    rng=rng,
                )
            )
    return results


def _system_label(
    *,
    terrain_route_label: str,
    local_obstruction_rows: int,
    mandatory_single_divisor_rows: int,
    padic_descent_rows: int,
    sparse_unit_rows: int,
    artifact_rows: int,
    nonartifact_sparse_rows: int,
    trace_rigid_rows: int,
    newform_check_rows: int,
    frey_template_candidate_rows: int,
    expected_route: str,
) -> str:
    if terrain_route_label in {"artifact_like", "theorem_terrain_route"}:
        return terrain_route_label
    if sparse_unit_rows and artifact_rows == sparse_unit_rows:
        return "artifact_like"
    if local_obstruction_rows or (mandatory_single_divisor_rows and padic_descent_rows) or trace_rigid_rows:
        return "calibrated_route_candidate"
    if terrain_route_label == "needs_external_sage_check" or newform_check_rows or (expected_route == "modular_method" and frey_template_candidate_rows and nonartifact_sparse_rows):
        return "needs_external_sage_check"
    return "not_promising_yet"


def _comparison_flag(case: KnownCase, terrain: TheoremTerrainRecord, system_label: str) -> str:
    strong = {"calibrated_route_candidate", "needs_external_sage_check"}
    if terrain.expected_route == "artifact" or terrain.known_status_label == "subgroup_artifact":
        return "artifact_match" if system_label == "artifact_like" else "route_mismatch"
    if terrain.known_status_label in {"known_solved_terrain", "follows_FLT_style_reduction", "descent_terrain"}:
        return "terrain_match" if system_label == "theorem_terrain_route" else "route_mismatch"
    if terrain.expected_route == "modular_method":
        return "calibrated_match" if system_label == "needs_external_sage_check" else "route_mismatch"
    if case.known_status == "known_possible" and system_label in strong:
        return "overpromotion"
    if case.known_status == "known_impossible" and system_label in {"not_promising_yet", "artifact_like"}:
        return "underpromotion"
    if case.expected_route == "artifact":
        return "artifact_match" if system_label == "artifact_like" else "route_mismatch"
    if case.expected_route == "modular_method":
        return "calibrated_match" if system_label in strong else "underpromotion"
    if case.expected_route in {"descent", "local_obstruction", "FLT_style"}:
        return "calibrated_match" if system_label == "calibrated_route_candidate" else "underpromotion"
    return "uncertain"


def _final_label(system_label: str, comparison_flag: str) -> str:
    if comparison_flag in {"overpromotion", "underpromotion", "route_mismatch", "true_mismatch"}:
        return "known_case_mismatch"
    return system_label


def _strongest_signal(
    signature: Signature,
    primes: Iterable[int],
    primitive_by_key,
    route_by_key,
    artifact_by_key,
) -> tuple[int, str]:
    candidates: list[tuple[float, int, str]] = []
    for ell in primes:
        key = (signature, ell)
        primitive = primitive_by_key.get(key)
        if primitive is not None:
            candidates.append((float(primitive.lemma_candidate_score), ell, f"primitive:{primitive.classification}"))
        route = route_by_key.get(key)
        if route is not None:
            candidates.append((float(route.route_rank_score), ell, f"modular:{route.route_classification}"))
        artifact = artifact_by_key.get(key)
        if artifact is not None and artifact.verdict == "artifact_explained":
            candidates.append((1.0 + float(artifact.residual_density_gap), ell, "artifact:artifact_explained"))
    if not candidates:
        return 0, "none"
    _, ell, signal = max(candidates, key=lambda item: (item[0], item[1]))
    return ell, signal


def _calibration_records(
    cases: list[KnownCase],
    primes: tuple[int, ...],
    results: list[ResidueSweepResult],
    primitive_classifications,
    padic_audits,
    unit_geometries,
    artifact_assessments,
    padic_unit_lifts,
    trace_records,
    route_classifications,
) -> tuple[list[KnownCaseCalibrationRecord], list[TheoremTerrainRecord], list[RouteCollisionRecord]]:
    primitive_by_key = {(item.signature, item.ell): item for item in primitive_classifications}
    artifact_by_key = {(item.signature, item.ell): item for item in artifact_assessments}
    unit_lift_by_key = {(item.signature, item.ell): item for item in padic_unit_lifts}
    trace_by_key = {(item.signature, item.ell): item for item in trace_records}
    route_by_key = {(item.signature, item.ell): item for item in route_classifications}
    padic_by_key = {(item.signature, item.ell): item for item in padic_audits}
    sparse_keys = {(item.signature, item.ell) for item in unit_geometries}
    result_keys = {(item.signature, item.ell) for item in results}

    records: list[KnownCaseCalibrationRecord] = []
    terrain_records: list[TheoremTerrainRecord] = []
    collision_records: list[RouteCollisionRecord] = []
    for case in cases:
        keys = [(case.signature, ell) for ell in primes if (case.signature, ell) in result_keys]
        local_rows = sum(1 for key in keys if primitive_by_key[key].classification == "direct_primitive_obstruction")
        mandatory_rows = sum(1 for key in keys if primitive_by_key[key].classification == "mandatory_single_divisor")
        sparse_rows = sum(1 for key in keys if primitive_by_key[key].classification == "sparse_unit_survivor")
        artifact_rows = sum(1 for key in keys if key in artifact_by_key and artifact_by_key[key].verdict == "artifact_explained")
        nonartifact_sparse_rows = sum(1 for key in keys if key in sparse_keys and artifact_by_key.get(key) is not None and artifact_by_key[key].verdict != "artifact_explained")
        padic_descent_rows = sum(1 for key in keys if key in padic_by_key and padic_by_key[key].descent_like_lift)
        unit_rigid_rows = sum(1 for key in keys if key in unit_lift_by_key and unit_lift_by_key[key].collapse_or_rigid)
        trace_rigid_rows = sum(1 for key in keys if key in trace_by_key and trace_by_key[key].unusually_narrow_trace)
        newform_rows = sum(1 for key in keys if key in route_by_key and route_by_key[key].route_classification == "newform_check_candidate")
        frey_rows = sum(1 for key in keys if key in route_by_key and route_by_key[key].route_classification == "frey_template_candidate")
        template_confidence = candidate_frey_template(case.signature).template_confidence
        strongest_prime, strongest_signal = _strongest_signal(
            case.signature,
            primes,
            primitive_by_key,
            route_by_key,
            artifact_by_key,
        )
        terrain_key = (case.signature, strongest_prime)
        terrain = classify_theorem_terrain(
            case.signature,
            ell=strongest_prime or None,
            primitive_classification=primitive_by_key.get(terrain_key),
            artifact_assessment=artifact_by_key.get(terrain_key),
            trace_record=trace_by_key.get(terrain_key),
            route_classification=route_by_key.get(terrain_key),
        )
        terrain_records.append(terrain)
        expected_route = terrain.expected_route if terrain.expected_route != "unknown" else case.expected_route
        pre_collision_label = _system_label(
            terrain_route_label=terrain.terrain_route_label,
            local_obstruction_rows=local_rows,
            mandatory_single_divisor_rows=mandatory_rows,
            padic_descent_rows=padic_descent_rows,
            sparse_unit_rows=sparse_rows,
            artifact_rows=artifact_rows,
            nonartifact_sparse_rows=nonartifact_sparse_rows,
            trace_rigid_rows=trace_rigid_rows,
            newform_check_rows=newform_rows,
            frey_template_candidate_rows=frey_rows,
            expected_route=expected_route,
        )
        collision = resolve_route_collision(
            case_id=case.case_id,
            signature=case.signature,
            keys=keys,
            terrain=terrain,
            primitive_by_key=primitive_by_key,
            artifact_by_key=artifact_by_key,
            route_by_key=route_by_key,
            unit_lift_by_key=unit_lift_by_key,
            padic_by_key=padic_by_key,
            expected_route=expected_route,
            initial_route_label=pre_collision_label,
        )
        collision_records.append(collision)
        system_label = collision.resolved_route_label
        flag = _comparison_flag(case, terrain, system_label)
        records.append(
            KnownCaseCalibrationRecord(
                case_id=case.case_id,
                signature=case.signature,
                signature_text=_signature_text(case.signature),
                family_label=case.family_label,
                known_status=case.known_status,
                expected_route=expected_route,
                terrain_label=terrain.terrain_label,
                structural_terrain_labels=terrain.structural_terrain_labels,
                known_status_label=terrain.known_status_label,
                theorem_route_label=terrain.terrain_route_label,
                theorem_match_id=terrain.theorem_match_id,
                should_promote_without_external_check=terrain.should_promote_without_external_check,
                artifact_collision_expected=terrain.artifact_collision_expected,
                should_resolve_to=terrain.should_resolve_to,
                pre_collision_route_label=pre_collision_label,
                collision_class=collision.collision_class,
                collision_resolved_route_label=collision.resolved_route_label,
                collision_rationale=collision.rationale,
                prime_count=len(keys),
                local_obstruction_rows=local_rows,
                mandatory_single_divisor_rows=mandatory_rows,
                sparse_unit_rows=sparse_rows,
                artifact_rows=artifact_rows,
                nonartifact_sparse_rows=nonartifact_sparse_rows,
                padic_descent_rows=padic_descent_rows,
                unit_lift_rigid_or_collapsed_rows=unit_rigid_rows,
                trace_rigid_rows=trace_rigid_rows,
                newform_check_rows=newform_rows,
                frey_template_candidate_rows=frey_rows,
                average_template_confidence=template_confidence,
                strongest_prime=strongest_prime,
                strongest_system_signal=strongest_signal,
                system_route_label=system_label,
                actual_route_label=_final_label(system_label, flag),
                comparison_flag=flag,
                notes=case.notes,
                source_placeholder=case.source_placeholder,
            )
        )
    records.sort(
        key=lambda item: (
            item.actual_route_label == "known_case_mismatch",
            item.actual_route_label == "needs_external_sage_check",
            item.actual_route_label == "calibrated_route_candidate",
            item.case_id,
        ),
        reverse=True,
    )
    return records, terrain_records, collision_records


def _report_markdown(
    *,
    output_dir: Path,
    records: list[KnownCaseCalibrationRecord],
    confusion: list[CalibrationMatrixRecord],
    priors: list[RoutePriorScore],
    sage_exports: list[SageExportRecord],
) -> str:
    generated = datetime.now().isoformat(timespec="seconds")
    label_counts: dict[str, int] = {}
    for record in records:
        label_counts[record.actual_route_label] = label_counts.get(record.actual_route_label, 0) + 1
    lines = [
        "# Known-Case Calibration Report",
        "",
        f"Generated: `{generated}`",
        f"Output directory: `{output_dir.as_posix()}`",
        "",
        "## Interpretation Guardrail",
        "",
        "This harness calibrates RSG route behavior against known or calibration-only generalized Fermat terrain. It is not a theorem database and does not claim completeness.",
        "",
        "A Beal-style discovery candidate should not be promoted unless the same route type behaves correctly on these calibration cases and avoids known artifact behavior.",
        "",
        "## Counts",
        "",
        f"- Known/calibration cases: `{len(records)}`.",
    ]
    for label in sorted(label_counts):
        lines.append(f"- `{label}`: `{label_counts[label]}`.")
    lines.extend(
        [
            f"- Sage scripts exported: `{len(sage_exports)}`.",
            "",
            "## Known Case Route Matrix",
            "",
            "| bucket | cases | interpretation |",
            "| --- | ---: | --- |",
        ]
    )
    for row in confusion:
        lines.append(f"| {row.bucket} | {row.case_count} | {row.interpretation} |")

    lines.extend(
        [
            "",
            "## Highest Route-Prior Scores",
            "",
            "| rank | signature | label | readiness | artifact likelihood | rationale |",
            "| ---: | --- | --- | ---: | ---: | --- |",
        ]
    )
    for index, row in enumerate(priors[:12], start=1):
        lines.append(
            f"| {index} | {row.signature} | {row.output_label} | {row.discovery_readiness_score} | "
            f"{row.artifact_likelihood} | {row.rationale} |"
        )

    lines.extend(
        [
            "",
            "## Files",
            "",
            "- `known_case_calibration_summary.csv`: expected-vs-actual route comparison per calibration case.",
            "- `route_confusion_matrix.csv`: compatibility copy of the terrain-aware route matrix.",
            "- `known_case_route_matrix.csv`: theorem-terrain-aware route buckets.",
            "- `theorem_terrain_summary.csv`: structural terrain route rows.",
            "- `remaining_true_mismatches.csv`: true mismatch and overpromotion rows.",
            "- `family_expansion_results.csv`: structured nearby-signature fingerprint comparisons.",
            "- `route_prior_scores.csv`: calibrated route-priority and artifact-likelihood scores.",
            "- `sage_export_manifest.csv`: optional Sage scripts for modular follow-up sketches.",
            "",
            "## Next Work",
            "",
            "Treat `true_mismatch` and `overpromoted_candidate` rows as calibration debt. Treat `artifact_like` rows as useful controls. Theorem-terrain rows calibrate known proof terrain without creating new proof claims.",
            "",
        ]
    )
    return "\n".join(lines)


def build_known_case_calibration(
    *,
    output_dir: Path,
    cases: list[KnownCase] | None = None,
    primes: tuple[int, ...],
    exponents: tuple[int, ...],
    compute_lift: bool,
    control_samples: int,
    seed: int = 20260620,
) -> KnownCaseCalibrationArtifacts:
    """Run the known-case calibration harness and return output records."""
    case_list = cases if cases is not None else load_known_cases()
    signatures = tuple(case.signature for case in case_list)
    results = _run_known_case_residues(
        signatures,
        primes,
        compute_lift=compute_lift,
        control_samples=control_samples,
        seed=seed,
    )
    zero_records = analyze_zero_support_results(results)
    primitive_classifications = classify_primitive_obstructions(results, zero_records)
    padic_audits = audit_padic_lifts(primitive_classifications)
    unit_geometries = analyze_sparse_unit_geometries(results, primitive_classifications)
    artifact_assessments = explain_artifacts(unit_geometries)
    padic_unit_lifts = analyze_padic_unit_lifts(unit_geometries)
    templates = build_template_records([geometry.signature for geometry in unit_geometries])
    trace_records = trace_probes_for_geometries(unit_geometries)
    modular_routes = build_modular_shadow_routes(
        unit_geometries,
        artifact_assessments,
        templates,
        trace_records,
    )
    cross_prime_records = analyze_cross_prime_traces(trace_records, artifact_assessments)
    route_classifications = classify_modular_routes(
        modular_routes,
        artifact_assessments,
        trace_records,
        templates,
        cross_prime_records,
    )
    case_records, terrain_records, collision_records = _calibration_records(
        case_list,
        primes,
        results,
        primitive_classifications,
        padic_audits,
        unit_geometries,
        artifact_assessments,
        padic_unit_lifts,
        trace_records,
        route_classifications,
    )
    family_expansions = expand_signature_families(
        case_list,
        exponents=exponents,
        primes=primes,
        compute_lift=compute_lift,
        control_samples=control_samples,
        seed=seed + 9001,
    )
    route_matrix = build_calibration_confusion_matrix(case_records)
    priors = score_route_priors(case_records, family_expansions)
    sage_exports = export_sage_scripts(priors, case_records, output_dir)
    terrain_rows = theorem_terrain_summary_rows(case_records, terrain_records)
    matrix_rows = [record.to_flat_dict() for record in route_matrix]
    mismatch_rows = remaining_true_mismatch_rows(case_records, route_matrix)
    resolved_collision_rows = resolved_known_mismatch_rows(case_records, collision_records)
    blocked_collision_rows = still_blocked_mismatch_rows(case_records, collision_records)
    collision_rows = [record.to_flat_dict() for record in collision_records]
    report = _report_markdown(
        output_dir=output_dir,
        records=case_records,
        confusion=route_matrix,
        priors=priors,
        sage_exports=sage_exports,
    )
    terrain_report = theorem_terrain_report_markdown(
        output_dir=output_dir,
        terrain_rows=terrain_rows,
        matrix_rows=matrix_rows,
        mismatch_rows=mismatch_rows,
    )
    collision_report = route_collision_report_markdown(
        output_dir=output_dir,
        collision_rows=collision_rows,
        resolved_rows=resolved_collision_rows,
        blocked_rows=blocked_collision_rows,
    )
    return KnownCaseCalibrationArtifacts(
        case_records=case_records,
        terrain_records=terrain_records,
        collision_records=collision_records,
        route_matrix_records=route_matrix,
        terrain_summary_rows=terrain_rows,
        remaining_true_mismatch_rows=mismatch_rows,
        resolved_known_mismatch_rows=resolved_collision_rows,
        still_blocked_mismatch_rows=blocked_collision_rows,
        family_expansion_records=family_expansions,
        route_prior_scores=priors,
        sage_export_records=sage_exports,
        report_markdown=report,
        terrain_report_markdown=terrain_report,
        collision_report_markdown=collision_report,
    )
