"""Symbolic modular-shadow records and candidate ranking."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from math import isinf, log2
from typing import Iterable

from .number_theory import radical
from .rsg_residue_engine import ResidueSweepResult, Signature, density_bucket, lift_bucket
from .rsg_valuation_engine import ValuationRecord


@dataclass(frozen=True)
class ShadowRecord:
    """Symbolic obstruction record for a residue/valuation row."""

    signature: Signature
    ell: int
    radical_support: tuple[int, ...]
    bad_prime_support: tuple[int, ...]
    conductor_complexity: float
    frey_curve_placeholder: str
    obstruction_fingerprint: str
    cluster_key: str
    cluster_size: int
    cluster_prime_count: int
    cluster_signature_count: int
    candidate_score: float
    promotion_status: str
    rationale: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signature"] = "-".join(str(part) for part in self.signature)
        data["radical_support"] = ";".join(str(part) for part in self.radical_support)
        data["bad_prime_support"] = ";".join(str(part) for part in self.bad_prime_support)
        return data


@dataclass(frozen=True)
class ClusterSummary:
    """Summary for a repeated obstruction fingerprint."""

    cluster_key: str
    size: int
    prime_count: int
    signature_count: int
    best_score: float
    promoted_count: int
    primes: tuple[int, ...]
    signatures: tuple[str, ...]

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["primes"] = ";".join(str(prime) for prime in self.primes)
        data["signatures"] = ";".join(self.signatures)
        return data


def _support_for(result: ResidueSweepResult) -> tuple[tuple[int, ...], tuple[int, ...]]:
    p, q, r = result.signature
    radical_support = radical((p, q, r, result.ell))
    bad_prime_support = tuple(sorted(set((2, result.ell, *radical((p, q, r))))))
    return radical_support, bad_prime_support


def _control_bonus(z_score: float) -> float:
    if isinf(z_score):
        return 4.0 if z_score < 0 else 0.0
    return max(0.0, -z_score)


def _conductor_complexity(
    result: ResidueSweepResult,
    valuation: ValuationRecord,
    radical_support: tuple[int, ...],
) -> float:
    support_weight = sum(log2(prime) for prime in radical_support)
    density_penalty = -log2(max(result.density, 1e-12))
    if result.lift_trial_count:
        lift_penalty = -log2(max(result.lift_survival_rate, 1e-6))
    else:
        lift_penalty = 0.0
    return round(
        support_weight
        + density_penalty
        + lift_penalty
        + valuation.descent_score
        + _control_bonus(result.control_z_score),
        10,
    )


def _cluster_key(result: ResidueSweepResult, valuation: ValuationRecord) -> str:
    p, q, r = result.signature
    exponent_radical = radical((p, q, r))
    return (
        f"exp_rad={exponent_radical}|"
        f"density={density_bucket(result.density)}|"
        f"lift={lift_bucket(result.lift_survival_rate, result.lift_trial_count)}|"
        f"valuation={valuation.valuation_fingerprint}"
    )


def _obstruction_fingerprint(
    result: ResidueSweepResult,
    valuation: ValuationRecord,
    radical_support: tuple[int, ...],
    bad_prime_support: tuple[int, ...],
) -> str:
    return (
        f"rad={radical_support}|bad={bad_prime_support}|"
        f"residue={result.residue_fingerprint}|valuation={valuation.valuation_fingerprint}"
    )


def _frey_placeholder(result: ResidueSweepResult, radical_support: tuple[int, ...]) -> str:
    p, q, r = result.signature
    support = ",".join(str(value) for value in radical_support)
    return (
        f"placeholder: Frey data for A^{p}+B^{q}=C^{r}; "
        f"local prime ell={result.ell}; radical support {{{support}}}; "
        "requires later curve family selection"
    )


def _base_score(result: ResidueSweepResult, valuation: ValuationRecord, conductor_complexity: float) -> float:
    sparsity = -log2(max(result.density, 1e-12))
    lift_pressure = 1.0 - result.lift_survival_rate if result.lift_trial_count else 0.0
    return round(
        0.35 * conductor_complexity
        + 1.25 * _control_bonus(result.control_z_score)
        + 2.0 * lift_pressure
        + 0.35 * sparsity
        + 0.5 * len(valuation.flags),
        10,
    )


def build_shadow_records(
    results: Iterable[ResidueSweepResult],
    valuations: Iterable[ValuationRecord],
    *,
    control_z_gate: float = -1.5,
) -> tuple[list[ShadowRecord], list[ClusterSummary]]:
    """Build symbolic shadow records and cluster summaries."""
    result_list = list(results)
    valuation_list = list(valuations)
    if len(result_list) != len(valuation_list):
        raise ValueError("results and valuations must have the same length")

    preliminary: list[dict[str, object]] = []
    cluster_members: dict[str, list[int]] = defaultdict(list)
    for index, (result, valuation) in enumerate(zip(result_list, valuation_list)):
        radical_support, bad_prime_support = _support_for(result)
        complexity = _conductor_complexity(result, valuation, radical_support)
        cluster_key = _cluster_key(result, valuation)
        cluster_members[cluster_key].append(index)
        preliminary.append(
            {
                "result": result,
                "valuation": valuation,
                "radical_support": radical_support,
                "bad_prime_support": bad_prime_support,
                "complexity": complexity,
                "cluster_key": cluster_key,
                "obstruction_fingerprint": _obstruction_fingerprint(
                    result,
                    valuation,
                    radical_support,
                    bad_prime_support,
                ),
                "frey": _frey_placeholder(result, radical_support),
                "base_score": _base_score(result, valuation, complexity),
            }
        )

    cluster_stats: dict[str, dict[str, object]] = {}
    for key, indexes in cluster_members.items():
        primes = sorted({result_list[index].ell for index in indexes})
        signatures = sorted({"-".join(map(str, result_list[index].signature)) for index in indexes})
        cluster_stats[key] = {
            "size": len(indexes),
            "prime_count": len(primes),
            "signature_count": len(signatures),
            "primes": tuple(primes),
            "signatures": tuple(signatures),
        }

    records: list[ShadowRecord] = []
    promoted_counter: Counter[str] = Counter()
    for row in preliminary:
        result = row["result"]
        valuation = row["valuation"]
        assert isinstance(result, ResidueSweepResult)
        assert isinstance(valuation, ValuationRecord)
        cluster_key = str(row["cluster_key"])
        stats = cluster_stats[cluster_key]
        repeats_broadly = int(stats["prime_count"]) >= 2 and int(stats["signature_count"]) >= 2
        repeats_narrowly = int(stats["prime_count"]) >= 2 or int(stats["signature_count"]) >= 2
        beats_control = result.control_z_score <= control_z_gate
        has_math_signal = bool(valuation.flags)
        score = float(row["base_score"]) + log2(int(stats["size"]) + 1)

        if repeats_broadly and beats_control and has_math_signal:
            status = "promoted_candidate"
            rationale = "repeats across primes and signatures, beats controls, and carries valuation flags"
            promoted_counter[cluster_key] += 1
        elif repeats_narrowly and (beats_control or has_math_signal):
            status = "watchlist"
            rationale = "repeats, but misses at least one promotion gate"
        else:
            status = "control_like"
            rationale = "not promoted; lacks repeated controlled obstruction signal"

        records.append(
            ShadowRecord(
                signature=result.signature,
                ell=result.ell,
                radical_support=row["radical_support"],
                bad_prime_support=row["bad_prime_support"],
                conductor_complexity=float(row["complexity"]),
                frey_curve_placeholder=str(row["frey"]),
                obstruction_fingerprint=str(row["obstruction_fingerprint"]),
                cluster_key=cluster_key,
                cluster_size=int(stats["size"]),
                cluster_prime_count=int(stats["prime_count"]),
                cluster_signature_count=int(stats["signature_count"]),
                candidate_score=round(score, 10),
                promotion_status=status,
                rationale=rationale,
            )
        )

    summaries: list[ClusterSummary] = []
    for key, stats in cluster_stats.items():
        member_scores = [record.candidate_score for record in records if record.cluster_key == key]
        summaries.append(
            ClusterSummary(
                cluster_key=key,
                size=int(stats["size"]),
                prime_count=int(stats["prime_count"]),
                signature_count=int(stats["signature_count"]),
                best_score=round(max(member_scores), 10),
                promoted_count=promoted_counter[key],
                primes=stats["primes"],
                signatures=stats["signatures"],
            )
        )
    summaries.sort(key=lambda item: (item.promoted_count, item.best_score, item.size), reverse=True)
    records.sort(key=lambda item: item.candidate_score, reverse=True)
    return records, summaries
