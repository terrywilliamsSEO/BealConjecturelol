"""Cross-prime compatibility checks for repeated sparse unit constraints."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass
from math import log10, prod

from .artifact_explainer import ArtifactAssessment
from .unit_survivor_geometry import UnitSurvivorGeometry


@dataclass(frozen=True)
class MultiPrimeCompatibilityRecord:
    """CRT-style compatibility summary for one signature across sparse primes."""

    signature: tuple[int, int, int]
    primes: tuple[int, ...]
    prime_count: int
    combined_modulus: int
    combined_survivor_count: int
    combined_pair_count: int
    combined_density: float
    cross_prime_rigidity_score: float
    independent_crt_empty: bool
    compatibility_status: str
    explanation: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signature"] = "-".join(str(part) for part in self.signature)
        data["primes"] = ";".join(str(prime) for prime in self.primes)
        return data


def analyze_multi_prime_compatibility(
    geometries: list[UnitSurvivorGeometry],
    assessments: list[ArtifactAssessment],
) -> list[MultiPrimeCompatibilityRecord]:
    """Combine sparse constraints across primes for the same signature.

    Independent CRT products of nonempty local unit sets are not empty. This
    module therefore ranks rigidity by combined density rather than pretending
    that independent local constraints alone create contradictions.
    """
    assessment_by_key = {(item.signature, item.ell): item for item in assessments}
    groups: dict[tuple[int, int, int], list[UnitSurvivorGeometry]] = defaultdict(list)
    for geometry in geometries:
        assessment = assessment_by_key.get((geometry.signature, geometry.ell))
        if assessment is not None and assessment.verdict == "artifact_explained":
            continue
        groups[geometry.signature].append(geometry)

    records: list[MultiPrimeCompatibilityRecord] = []
    for signature, rows in groups.items():
        prime_rows = sorted(rows, key=lambda item: item.ell)
        if len({row.ell for row in prime_rows}) < 2:
            continue
        primes = tuple(row.ell for row in prime_rows)
        combined_modulus = prod(primes)
        combined_survivors = prod(row.survivor_count for row in prime_rows)
        combined_pairs = prod(row.pair_count for row in prime_rows)
        combined_density = combined_survivors / combined_pairs if combined_pairs else 0.0
        rigidity_score = -log10(max(combined_density, 1e-300))
        empty = combined_survivors == 0
        if empty:
            status = "crt_empty"
            explanation = "at least one local survivor set is empty"
        elif rigidity_score >= 8:
            status = "cross_prime_rigid"
            explanation = "local unit constraints are compatible but extremely low-density under CRT product"
        else:
            status = "compatible_but_not_rigid"
            explanation = "independent local constraints remain CRT-compatible"
        records.append(
            MultiPrimeCompatibilityRecord(
                signature=signature,
                primes=primes,
                prime_count=len(primes),
                combined_modulus=combined_modulus,
                combined_survivor_count=combined_survivors,
                combined_pair_count=combined_pairs,
                combined_density=round(combined_density, 16),
                cross_prime_rigidity_score=round(rigidity_score, 10),
                independent_crt_empty=empty,
                compatibility_status=status,
                explanation=explanation,
            )
        )
    records.sort(key=lambda item: (item.compatibility_status == "cross_prime_rigid", item.cross_prime_rigidity_score), reverse=True)
    return records
