"""Valuation-style diagnostics for residue survivors."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from math import isinf
from typing import Iterable

from .rsg_residue_engine import ResidueSweepResult, Signature, count_survivors, power_residue_set


@dataclass(frozen=True)
class ValuationRecord:
    """Diagnostics that look for local collapse or descent-like behavior."""

    signature: Signature
    ell: int
    zero_solution_count: int
    zero_total_count: int
    zero_dominance: float
    zero_pattern_counts: dict[str, int]
    lift_failure_rate: float
    descent_score: float
    flags: tuple[str, ...]
    valuation_fingerprint: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["flags"] = ";".join(self.flags)
        data["zero_pattern_counts"] = ";".join(
            f"{key}:{value}" for key, value in sorted(self.zero_pattern_counts.items())
        )
        return data


def _zero_pattern_counts(signature: Signature, ell: int) -> tuple[int, int, dict[str, int]]:
    """Count solutions after zero classes are adjoined."""
    p, q, r = signature
    left = power_residue_set(p, ell, include_zero=True, units_only=False)
    right = power_residue_set(q, ell, include_zero=True, units_only=False)
    output = set(power_residue_set(r, ell, include_zero=True, units_only=False))
    counts: Counter[str] = Counter()
    total = 0
    nonzero = 0
    for u in left:
        for v in right:
            w = (u + v) % ell
            if w not in output:
                continue
            total += 1
            pattern = f"{int(u == 0)}{int(v == 0)}{int(w == 0)}"
            counts[pattern] += 1
            if pattern == "000":
                nonzero += 1
    return total - nonzero, total, dict(counts)


def _finite_control_pressure(z_score: float) -> float:
    """Return positive pressure when true density is below controls."""
    if isinf(z_score):
        return 4.0 if z_score < 0 else 0.0
    return max(0.0, -z_score)


def valuation_fingerprint(flags: Iterable[str], zero_dominance: float, lift_failure_rate: float) -> str:
    """Build a coarse valuation fingerprint."""
    if zero_dominance >= 0.75:
        zero_bucket = "zero_heavy"
    elif zero_dominance >= 0.35:
        zero_bucket = "zero_visible"
    else:
        zero_bucket = "zero_light"

    if lift_failure_rate >= 1.0:
        lift_bucket = "lift_blocked"
    elif lift_failure_rate >= 0.75:
        lift_bucket = "lift_fragile"
    elif lift_failure_rate >= 0.35:
        lift_bucket = "lift_mixed"
    else:
        lift_bucket = "lift_stable"

    flag_key = ",".join(sorted(flags)) or "no_flags"
    return f"{zero_bucket}|{lift_bucket}|{flag_key}"


def analyze_result(result: ResidueSweepResult) -> ValuationRecord:
    """Analyze one residue result for valuation-style patterns."""
    zero_count, zero_total, patterns = _zero_pattern_counts(result.signature, result.ell)
    zero_dominance = zero_count / zero_total if zero_total else 0.0
    if result.lift_trial_count:
        lift_failure_rate = 1.0 - result.lift_survival_rate
    else:
        lift_failure_rate = 0.0

    flags: list[str] = []
    if result.survivor_count == 0:
        flags.append("local_empty_nonzero_residue")
    if result.lift_trial_count and result.lift_survival_rate == 0:
        flags.append("no_unit_lifts")
    elif result.lift_trial_count and lift_failure_rate >= 0.75:
        flags.append("high_lift_failure")
    if zero_dominance >= 0.5:
        flags.append("zero_class_dominates")
    if result.survivor_count == 0 and zero_count > 0:
        flags.append("forced_zero_only")
    if zero_dominance >= 0.5 and lift_failure_rate >= 0.5:
        flags.append("descent_like_chain")

    control_pressure = _finite_control_pressure(result.control_z_score)
    descent_score = min(
        10.0,
        3.5 * lift_failure_rate + 2.5 * zero_dominance + min(4.0, control_pressure),
    )
    fingerprint = valuation_fingerprint(flags, zero_dominance, lift_failure_rate)
    return ValuationRecord(
        signature=result.signature,
        ell=result.ell,
        zero_solution_count=zero_count,
        zero_total_count=zero_total,
        zero_dominance=round(zero_dominance, 10),
        zero_pattern_counts=patterns,
        lift_failure_rate=round(lift_failure_rate, 10),
        descent_score=round(descent_score, 10),
        flags=tuple(flags),
        valuation_fingerprint=fingerprint,
    )


def analyze_results(results: Iterable[ResidueSweepResult]) -> list[ValuationRecord]:
    """Analyze many residue results."""
    return [analyze_result(result) for result in results]
