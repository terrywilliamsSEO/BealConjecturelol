"""Frey trace possibilities for `(5,4,5)` at good primes."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from .good_prime_selector import GoodPrimeRecord


@dataclass(frozen=True)
class FreyTracePossibilityRecord:
    """Possible Frey traces for one good prime."""

    signature: str
    prime: int
    survivor_triple_count: int
    nonsingular_curve_count: int
    singular_skipped_count: int
    possible_traces: tuple[int, ...]
    trace_count: int
    sample_triples: tuple[str, ...]
    enumeration_status: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["possible_traces"] = ";".join(str(item) for item in self.possible_traces)
        data["sample_triples"] = ";".join(self.sample_triples)
        return data


def _power_image(prime: int, exponent: int) -> tuple[int, ...]:
    return tuple(sorted({pow(value, exponent, prime) for value in range(1, prime)}))


def _legendre(value: int, prime: int) -> int:
    value %= prime
    if value == 0:
        return 0
    symbol = pow(value, (prime - 1) // 2, prime)
    return -1 if symbol == prime - 1 else symbol


def _frey_trace(prime: int, u: int, v: int) -> int:
    """Trace for E: y^2 = x(x-u)(x+v) over F_prime."""
    total = 0
    for x_value in range(prime):
        rhs = (x_value * (x_value - u) * (x_value + v)) % prime
        total += _legendre(rhs, prime)
    return -total


def _trace_possibility_for_prime(prime: int) -> FreyTracePossibilityRecord:
    fifth = _power_image(prime, 5)
    fourth = _power_image(prime, 4)
    target_fifth = set(fifth)
    traces: set[int] = set()
    triples: list[str] = []
    survivor_count = 0
    nonsingular_count = 0
    singular_skipped = 0
    for u_value in fifth:
        for v_value in fourth:
            w_value = (u_value + v_value) % prime
            if w_value not in target_fifth:
                continue
            survivor_count += 1
            if u_value == 0 or v_value == 0 or w_value == 0:
                singular_skipped += 1
                continue
            trace = _frey_trace(prime, u_value, v_value)
            traces.add(trace)
            nonsingular_count += 1
            if len(triples) < 8:
                triples.append(f"u={u_value},v={v_value},w={w_value},a={trace}")
    return FreyTracePossibilityRecord(
        signature="5-4-5",
        prime=prime,
        survivor_triple_count=survivor_count,
        nonsingular_curve_count=nonsingular_count,
        singular_skipped_count=singular_skipped,
        possible_traces=tuple(sorted(traces)),
        trace_count=len(traces),
        sample_triples=tuple(triples),
        enumeration_status="completed",
    )


def build_frey_trace_possibilities_545(
    good_prime_rows: Iterable[GoodPrimeRecord],
) -> list[FreyTracePossibilityRecord]:
    """Compute Frey trace possibilities for all selected good primes."""
    rows = [_trace_possibility_for_prime(row.prime) for row in good_prime_rows if row.selected]
    rows.sort(key=lambda row: row.prime)
    return rows

