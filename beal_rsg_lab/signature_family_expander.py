"""Structured signature expansion around known generalized Fermat families."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import random
from typing import Iterable

from .known_case_library import KnownCase
from .rsg_residue_engine import ResidueSweepResult, Signature, run_signature_prime
from .signature_normalizer import TARGET_SIGNATURES, canonicalize_signature


@dataclass(frozen=True)
class FamilyExpansionRecord:
    """Residue-fingerprint comparison for one nearby signature."""

    family_label: str
    base_case_id: str
    base_signature: Signature
    nearby_signature: Signature
    canonical_nearby_signature: Signature
    ell: int
    base_residue_fingerprint: str
    nearby_residue_fingerprint: str
    fingerprint_relation: str
    density_delta: float
    lift_rate_delta: float
    known_neighbor: bool
    expansion_notes: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["base_signature"] = "-".join(str(part) for part in self.base_signature)
        data["nearby_signature"] = "-".join(str(part) for part in self.nearby_signature)
        data["canonical_nearby_signature"] = "-".join(str(part) for part in self.canonical_nearby_signature)
        return data


def _signature_text(signature: Signature) -> str:
    return "-".join(str(part) for part in signature)


def _signature_distance(left: Signature, right: Signature) -> int:
    return sum(1 for a, b in zip(left, right) if a != b)


def _nearest_case(signature: Signature, cases: list[KnownCase]) -> KnownCase:
    canonical, _ = canonicalize_signature(signature)
    return min(
        cases,
        key=lambda case: (
            _signature_distance(canonicalize_signature(case.signature)[0], canonical),
            _signature_distance(case.signature, signature),
            case.case_id,
        ),
    )


def expanded_signatures(
    *,
    exponents: Iterable[int],
    include_beal_neighborhoods: bool = True,
) -> dict[Signature, str]:
    """Return structured expansion signatures keyed by signature."""
    values = tuple(sorted({int(value) for value in exponents if int(value) > 2}))
    signatures: dict[Signature, str] = {}

    for p in values:
        signatures[(p, p, p)] = "diagonal_family"

    for p in values:
        for q in values:
            if p != q:
                signatures[(p, p, q)] = "repeated_family"

    if 4 in values:
        for p in values:
            if p == 4:
                continue
            signatures[(4, p, p)] = "fourth_power_bridge"
            signatures[(p, 4, p)] = "fourth_power_bridge"
            signatures[(p, p, 4)] = "fourth_power_bridge"

    if 3 in values and 4 in values:
        for p in values:
            if p in {3, 4}:
                continue
            signatures[(3, 4, p)] = "mixed_bridge"
            signatures[(4, 3, p)] = "mixed_bridge"

    if include_beal_neighborhoods:
        for signature in TARGET_SIGNATURES:
            if all(part in values for part in signature):
                signatures[signature] = "beal_candidate_neighborhood"
            for index in range(3):
                for exponent in values:
                    nearby = list(signature)
                    nearby[index] = exponent
                    nearby_signature = tuple(nearby)  # type: ignore[assignment]
                    if all(part in values for part in nearby_signature):
                        signatures.setdefault(nearby_signature, "beal_candidate_neighborhood")

    return signatures


def expand_signature_families(
    cases: list[KnownCase],
    *,
    exponents: Iterable[int],
    primes: Iterable[int],
    compute_lift: bool,
    control_samples: int,
    seed: int = 20260620,
    max_signatures: int | None = None,
) -> list[FamilyExpansionRecord]:
    """Expand around known families and compare residue fingerprints."""
    if not cases:
        return []
    known_signatures = {case.signature for case in cases}
    signatures_by_family = expanded_signatures(exponents=exponents)
    ordered_signatures = sorted(signatures_by_family)
    if max_signatures is not None:
        ordered_signatures = ordered_signatures[:max_signatures]

    cache: dict[tuple[Signature, int], ResidueSweepResult] = {}

    def result_for(signature: Signature, ell: int) -> ResidueSweepResult:
        key = (signature, ell)
        if key not in cache:
            rng = random.Random(seed + ell * 7919 + sum(signature) * 101 + signature[0] * 17)
            cache[key] = run_signature_prime(
                signature,
                ell,
                compute_lift=compute_lift,
                control_samples=control_samples,
                rng=rng,
            )
        return cache[key]

    rows: list[FamilyExpansionRecord] = []
    for signature in ordered_signatures:
        base_case = _nearest_case(signature, cases)
        for ell in primes:
            base = result_for(base_case.signature, ell)
            nearby = result_for(signature, ell)
            relation = "preserved" if base.residue_fingerprint == nearby.residue_fingerprint else "broken"
            if base.residue_sizes == nearby.residue_sizes and relation == "broken":
                relation = "same_size_different_fingerprint"
            rows.append(
                FamilyExpansionRecord(
                    family_label=signatures_by_family[signature],
                    base_case_id=base_case.case_id,
                    base_signature=base_case.signature,
                    nearby_signature=signature,
                    canonical_nearby_signature=canonicalize_signature(signature)[0],
                    ell=ell,
                    base_residue_fingerprint=base.residue_fingerprint,
                    nearby_residue_fingerprint=nearby.residue_fingerprint,
                    fingerprint_relation=relation,
                    density_delta=round(nearby.density - base.density, 10),
                    lift_rate_delta=round(nearby.lift_survival_rate - base.lift_survival_rate, 10),
                    known_neighbor=signature in known_signatures,
                    expansion_notes=(
                        f"{_signature_text(signature)} compared with nearest calibration case "
                        f"{base_case.case_id}; relation={relation}"
                    ),
                )
            )
    rows.sort(key=lambda item: (item.fingerprint_relation == "preserved", item.known_neighbor), reverse=True)
    return rows
