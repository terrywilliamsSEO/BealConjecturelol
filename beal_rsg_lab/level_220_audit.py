"""Focused level-220 audit for the `(5,4,5)` route."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from .number_theory import prime_factors


@dataclass(frozen=True)
class Level220PrimeRecord:
    """Why a prime appears in the level-220 route-audit target."""

    level: int
    prime: int
    exponent_in_level: int
    reason_in_candidate_support: str
    status: str
    required_assumption: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class Level220NewformRecord:
    """Known imported data for one level-220 newform slot."""

    level: int
    newform_index: int
    label: str
    q_expansion_data_available: bool
    coefficients: str
    source: str
    status: str
    notes: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def factorization_220() -> str:
    """Return the fixed factorization of 220."""
    return "2^2 * 5 * 11"


def _level_exponent(level: int, prime: int) -> int:
    exponent = 0
    while level % prime == 0:
        level //= prime
        exponent += 1
    return exponent


def build_level_220_prime_records() -> list[Level220PrimeRecord]:
    """Return candidate bad-prime explanations for level 220."""
    reasons = {
        2: "Included by the split full-2-torsion Frey template and even-prime minimal-model uncertainty.",
        5: "Included from exponent radical support for the two fifth-power positions.",
        11: "Included from the local sparse row used in the Sage route audit.",
    }
    assumptions = {
        2: "A minimal model analysis must determine the exact 2-adic conductor exponent.",
        5: "The residual representation and ramification at 5 must be justified.",
        11: "A human must justify why this local prime belongs in the conductor or lowered level, rather than only in the route-audit search.",
    }
    return [
        Level220PrimeRecord(
            level=220,
            prime=prime,
            exponent_in_level=_level_exponent(220, prime),
            reason_in_candidate_support=reasons[prime],
            status="candidate_bad_prime",
            required_assumption=assumptions[prime],
        )
        for prime in prime_factors(220)
    ]


def build_level_220_newform_records(sage_payload: Mapping[str, Any] | None) -> list[Level220NewformRecord]:
    """Return imported labels/q-expansion information for level 220.

    Older Sage JSON imports only include `newform_count`, so this function emits
    placeholder rows for the known count while marking coefficient data missing.
    """
    payload = sage_payload or {}
    trace_rows = payload.get("newform_trace_rows", [])
    if not isinstance(trace_rows, list):
        trace_rows = []
    grouped: dict[int, list[str]] = {}
    for row in trace_rows:
        if not isinstance(row, dict):
            continue
        try:
            if int(row.get("level", 0)) != 220:
                continue
            index = int(row.get("newform_index", 0))
        except (TypeError, ValueError):
            continue
        coeff = str(row.get("coefficient", ""))
        prime = str(row.get("prime", ""))
        if coeff and prime:
            grouped.setdefault(index, []).append(f"a_{prime}={coeff}")
    count = int(payload.get("newform_count", 0) or 0)
    if count <= 0:
        count = max(grouped.keys(), default=-1) + 1
    records: list[Level220NewformRecord] = []
    for index in range(count):
        coeffs = ";".join(sorted(grouped.get(index, [])))
        records.append(
            Level220NewformRecord(
                level=220,
                newform_index=index,
                label=f"level220_newform_{index}" if coeffs else "label_unavailable",
                q_expansion_data_available=bool(coeffs),
                coefficients=coeffs,
                source="sage_results/sage_5_4_5.json",
                status="computed_by_sage" if coeffs else "missing_q_expansion_data",
                notes=(
                    "Imported q-expansion coefficient rows are available."
                    if coeffs
                    else "Sage imported the count but not labels or q-expansion coefficients."
                ),
            )
        )
    return records

