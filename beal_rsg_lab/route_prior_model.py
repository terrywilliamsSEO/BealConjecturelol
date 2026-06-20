"""Calibrated scoring model for proof-route readiness."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Protocol

from .signature_family_expander import FamilyExpansionRecord


class CalibrationScoreInput(Protocol):
    case_id: str
    signature_text: str
    family_label: str
    known_status: str
    expected_route: str
    terrain_label: str
    known_status_label: str
    theorem_route_label: str
    actual_route_label: str
    comparison_flag: str
    should_promote_without_external_check: bool
    prime_count: int
    local_obstruction_rows: int
    mandatory_single_divisor_rows: int
    sparse_unit_rows: int
    artifact_rows: int
    nonartifact_sparse_rows: int
    padic_descent_rows: int
    trace_rigid_rows: int
    newform_check_rows: int
    frey_template_candidate_rows: int
    average_template_confidence: float


@dataclass(frozen=True)
class RoutePriorScore:
    """Calibrated priority scores for one known-case signature."""

    case_id: str
    signature: str
    family_label: str
    known_status: str
    expected_route: str
    actual_route_label: str
    theorem_route_label: str
    terrain_label: str
    known_status_label: str
    local_obstruction_score: float
    artifact_score: float
    zero_support_score: float
    unit_geometry_score: float
    padic_persistence_score: float
    trace_rigidity_score: float
    frey_template_confidence: float
    known_family_similarity_score: float
    proof_route_priority: float
    artifact_likelihood: float
    known_route_similarity: float
    discovery_readiness_score: float
    output_label: str
    rationale: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def _ratio(count: int, total: int) -> float:
    return count / total if total else 0.0


def _known_route_similarity(record: CalibrationScoreInput) -> float:
    if record.actual_route_label == "theorem_terrain_route" and record.known_status_label in {
        "known_solved_terrain",
        "follows_FLT_style_reduction",
        "descent_terrain",
    }:
        return 1.0
    if record.expected_route == "artifact":
        return 1.0 if record.actual_route_label == "artifact_like" else 0.0
    if record.expected_route == "modular_method":
        return 1.0 if record.actual_route_label in {"needs_external_sage_check", "calibrated_route_candidate"} else 0.25
    if record.expected_route in {"descent", "descent_or_modularity", "local_obstruction", "FLT_style"}:
        return 1.0 if record.actual_route_label in {"calibrated_route_candidate", "theorem_terrain_route"} else 0.15
    if record.expected_route == "unknown":
        return 0.5 if record.actual_route_label in {"not_promising_yet", "artifact_like"} else 0.25
    return 0.0


def _family_similarity(case_id: str, expansions: list[FamilyExpansionRecord]) -> float:
    related = [item for item in expansions if item.base_case_id == case_id]
    if not related:
        return 0.0
    preserved = sum(1 for item in related if item.fingerprint_relation == "preserved")
    same_size = sum(1 for item in related if item.fingerprint_relation == "same_size_different_fingerprint")
    return round((preserved + 0.5 * same_size) / len(related), 10)


def _output_label(
    record: CalibrationScoreInput,
    *,
    artifact_likelihood: float,
    route_similarity: float,
    readiness: float,
) -> str:
    if artifact_likelihood >= 0.65 or record.actual_route_label == "artifact_like":
        return "artifact_like"
    if record.actual_route_label == "theorem_terrain_route":
        return "theorem_terrain_route"
    if record.comparison_flag in {"overpromotion", "underpromotion", "route_mismatch", "true_mismatch"}:
        return "known_case_mismatch"
    if record.actual_route_label == "needs_external_sage_check":
        return "needs_external_sage_check"
    terrain_validated = record.comparison_flag == "calibrated_match" and record.should_promote_without_external_check
    if record.actual_route_label == "calibrated_route_candidate" and readiness >= 5.0 and route_similarity >= 0.65 and terrain_validated:
        return "calibrated_route_candidate"
    return "not_promising_yet"


def score_route_priors(
    records: Iterable[CalibrationScoreInput],
    family_expansions: Iterable[FamilyExpansionRecord],
) -> list[RoutePriorScore]:
    """Score known-case route priority using calibrated RSG features."""
    expansion_list = list(family_expansions)
    scores: list[RoutePriorScore] = []
    for record in records:
        total = max(1, record.prime_count)
        local_score = round(4.0 * _ratio(record.local_obstruction_rows, total), 10)
        zero_score = round(2.5 * _ratio(record.mandatory_single_divisor_rows, total), 10)
        unit_score = round(2.0 * _ratio(record.nonartifact_sparse_rows, total), 10)
        artifact_score = round(_ratio(record.artifact_rows, max(1, record.sparse_unit_rows)), 10)
        padic_score = round(3.0 * _ratio(record.padic_descent_rows, total), 10)
        trace_score = round(4.0 * _ratio(record.trace_rigid_rows, total), 10)
        terrain_score = 1.0 if record.actual_route_label == "theorem_terrain_route" else 0.0
        family_score = _family_similarity(record.case_id, expansion_list)
        route_similarity = _known_route_similarity(record)
        frey_confidence = round(record.average_template_confidence, 10)
        priority = round(
            local_score
            + zero_score
            + unit_score
            + padic_score
            + trace_score
            + terrain_score
            + 2.0 * frey_confidence
            + family_score
            + route_similarity,
            10,
        )
        artifact_likelihood = round(min(1.0, artifact_score + (0.25 if record.expected_route == "artifact" else 0.0)), 10)
        mismatch_penalty = 3.0 if record.comparison_flag in {"overpromotion", "underpromotion", "route_mismatch"} else 0.0
        readiness = round(max(0.0, priority - 4.0 * artifact_likelihood - mismatch_penalty), 10)
        label = _output_label(
            record,
            artifact_likelihood=artifact_likelihood,
            route_similarity=route_similarity,
            readiness=readiness,
        )
        scores.append(
            RoutePriorScore(
                case_id=record.case_id,
                signature=record.signature_text,
                family_label=record.family_label,
                known_status=record.known_status,
                expected_route=record.expected_route,
                actual_route_label=record.actual_route_label,
                theorem_route_label=record.theorem_route_label,
                terrain_label=record.terrain_label,
                known_status_label=record.known_status_label,
                local_obstruction_score=local_score,
                artifact_score=artifact_score,
                zero_support_score=zero_score,
                unit_geometry_score=unit_score,
                padic_persistence_score=padic_score,
                trace_rigidity_score=trace_score,
                frey_template_confidence=frey_confidence,
                known_family_similarity_score=family_score,
                proof_route_priority=priority,
                artifact_likelihood=artifact_likelihood,
                known_route_similarity=round(route_similarity, 10),
                discovery_readiness_score=readiness,
                output_label=label,
                rationale=(
                    f"label={label}; route_similarity={round(route_similarity, 4)}; "
                    f"artifact_likelihood={artifact_likelihood}; readiness={readiness}"
                ),
            )
        )
    scores.sort(
        key=lambda item: (
            item.output_label == "calibrated_route_candidate",
            item.output_label == "needs_external_sage_check",
            item.discovery_readiness_score,
            item.proof_route_priority,
        ),
        reverse=True,
    )
    return scores
