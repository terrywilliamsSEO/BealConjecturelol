"""Primitive obstruction classification using exact zero-support records."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass
from math import isinf, log2
from statistics import mean
from typing import Iterable

from .rsg_residue_engine import ResidueSweepResult, density_bucket
from .zero_support_engine import ZeroSupportRecord

CONTROL_Z_GATE = -1.5


@dataclass(frozen=True)
class PrimitiveClassification:
    """Classification and ranking data for one local row."""

    signature: tuple[int, int, int]
    ell: int
    classification: str
    lemma_candidate_tier: str
    lemma_candidate_score: float
    forced_variable: str
    artifact_reasons: tuple[str, ...]
    subgroup_control_key: str
    subgroup_control_class_size: int
    subgroup_control_density_mean: float
    subgroup_control_density_min: float
    subgroup_control_density_max: float
    subgroup_size_explained: bool
    structured_independent: bool
    rationale: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signature"] = "-".join(str(part) for part in self.signature)
        data["artifact_reasons"] = ";".join(self.artifact_reasons)
        return data


@dataclass(frozen=True)
class SparseUnitCluster:
    """Cluster summary for sparse unit-survivor candidates."""

    cluster_key: str
    size: int
    prime_count: int
    signature_count: int
    subgroup_shape_count: int
    best_score: float
    primes: tuple[int, ...]
    signatures: tuple[str, ...]
    rationale: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["primes"] = ";".join(str(prime) for prime in self.primes)
        data["signatures"] = ";".join(self.signatures)
        return data


def _control_key(record: ZeroSupportRecord) -> str:
    return f"ell={record.ell}|sizes={'-'.join(str(part) for part in record.subgroup_size_shape)}"


def _artifact_reasons(result: ResidueSweepResult, zero: ZeroSupportRecord, class_size: int) -> tuple[str, ...]:
    reasons: list[str] = []
    if result.ell <= 5:
        reasons.append("tiny_prime")
    if min(result.residue_sizes) <= 1:
        reasons.append("trivial_power_subgroup")
    if class_size > 1 and result.ell <= 7:
        reasons.append("small_prime_subgroup_size_duplicate")
    return tuple(reasons)


def _score(result: ResidueSweepResult, zero: ZeroSupportRecord, classification: str, structured_independent: bool) -> float:
    sparsity = -log2(max(result.density, 1e-12))
    if isinf(result.control_z_score):
        control_pressure = 5.0 if result.control_z_score < 0 else 0.0
    else:
        control_pressure = max(0.0, -result.control_z_score)
    tier_bonus = {
        "direct_primitive_obstruction": 20.0,
        "mandatory_single_divisor": 12.0,
        "sparse_unit_survivor": 6.0,
        "likely_small_prime_artifact": -6.0,
        "control_like": 0.0,
    }[classification]
    structure_bonus = 1.5 if structured_independent else -1.5
    support_bonus = 2.0 * zero.minimum_zero_support_size
    return round(tier_bonus + sparsity + control_pressure + support_bonus + structure_bonus, 10)


def classify_primitive_obstructions(
    results: Iterable[ResidueSweepResult],
    zero_records: Iterable[ZeroSupportRecord],
    *,
    control_z_gate: float = CONTROL_Z_GATE,
) -> list[PrimitiveClassification]:
    """Classify rows using exact zero-support and subgroup-size controls."""
    result_list = list(results)
    zero_list = list(zero_records)
    if len(result_list) != len(zero_list):
        raise ValueError("results and zero_records must have the same length")

    groups: dict[str, list[int]] = defaultdict(list)
    for index, zero in enumerate(zero_list):
        groups[_control_key(zero)].append(index)

    classifications: list[PrimitiveClassification] = []
    for index, (result, zero) in enumerate(zip(result_list, zero_list)):
        key = _control_key(zero)
        indexes = groups[key]
        densities = [result_list[item].density for item in indexes]
        class_size = len(indexes)
        shape_count = len({zero_list[item].subgroup_size_shape for item in indexes})
        structured_independent = class_size == 1 or len({zero_list[item].signature for item in indexes}) == 1
        subgroup_size_explained = class_size > 1
        artifacts = _artifact_reasons(result, zero, class_size)

        if artifacts:
            classification = "likely_small_prime_artifact"
            tier = "demoted_artifact"
            forced_variable = ""
            rationale = "demoted because tiny-prime or trivial subgroup shape explains the obstruction"
        elif zero.zero_adjoined_survivor_count and zero.minimum_zero_support_size >= 2:
            classification = "direct_primitive_obstruction"
            tier = "tier_1_direct"
            forced_variable = ";".join(zero.variable_forced_zero_if_any)
            rationale = "every local survivor has at least two variables zero modulo ell"
        elif zero.exact_single_variable_mask:
            classification = "mandatory_single_divisor"
            tier = "tier_2_single_divisor"
            forced_variable = zero.exact_single_variable_mask.split("_", maxsplit=1)[0]
            rationale = f"every local survivor has exact zero mask {zero.exact_single_variable_mask}"
        elif (
            zero.nonzero_survivor_count > 0
            and result.control_z_score <= control_z_gate
            and result.density < result.control_mean_density
        ):
            classification = "sparse_unit_survivor"
            tier = "tier_3_sparse_units"
            forced_variable = ""
            rationale = "unit survivors exist but are sparse against randomized subgroup-coset controls"
        else:
            classification = "control_like"
            tier = "not_a_candidate"
            forced_variable = ""
            rationale = "no forced primitive obstruction or controlled sparsity signal"

        classifications.append(
            PrimitiveClassification(
                signature=result.signature,
                ell=result.ell,
                classification=classification,
                lemma_candidate_tier=tier,
                lemma_candidate_score=_score(result, zero, classification, structured_independent),
                forced_variable=forced_variable,
                artifact_reasons=artifacts,
                subgroup_control_key=key,
                subgroup_control_class_size=class_size,
                subgroup_control_density_mean=round(mean(densities), 10),
                subgroup_control_density_min=round(min(densities), 10),
                subgroup_control_density_max=round(max(densities), 10),
                subgroup_size_explained=subgroup_size_explained,
                structured_independent=structured_independent,
                rationale=rationale,
            )
        )

    classifications.sort(key=lambda item: item.lemma_candidate_score, reverse=True)
    return classifications


def sparse_unit_clusters(classifications: Iterable[PrimitiveClassification]) -> list[SparseUnitCluster]:
    """Cluster sparse unit-survivor candidates by actual subgroup-size shape."""
    sparse = [item for item in classifications if item.classification == "sparse_unit_survivor"]
    groups: dict[str, list[PrimitiveClassification]] = defaultdict(list)
    for item in sparse:
        size_key = item.subgroup_control_key.split("|", maxsplit=1)[1]
        groups[size_key].append(item)

    clusters: list[SparseUnitCluster] = []
    for key, rows in groups.items():
        primes = tuple(sorted({row.ell for row in rows}))
        signatures = tuple(sorted({"-".join(str(part) for part in row.signature) for row in rows}))
        shape_count = len({row.subgroup_control_key.split("|", maxsplit=1)[1] for row in rows})
        clusters.append(
            SparseUnitCluster(
                cluster_key=key,
                size=len(rows),
                prime_count=len(primes),
                signature_count=len(signatures),
                subgroup_shape_count=shape_count,
                best_score=max(row.lemma_candidate_score for row in rows),
                primes=primes,
                signatures=signatures,
                rationale="sparse unit survivors after exact zero-support filtering",
            )
        )
    clusters.sort(key=lambda item: (item.prime_count, item.signature_count, item.best_score), reverse=True)
    return clusters
