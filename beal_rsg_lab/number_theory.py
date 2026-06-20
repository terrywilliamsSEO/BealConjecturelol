"""Small number-theory helpers used by the RSG engines."""

from __future__ import annotations

from collections.abc import Iterable
from math import log2, sqrt


def is_prime(n: int) -> bool:
    """Return True when n is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    limit = int(sqrt(n))
    for factor in range(3, limit + 1, 2):
        if n % factor == 0:
            return False
    return True


def primes_up_to(limit: int, *, odd_only: bool = True) -> tuple[int, ...]:
    """Return primes up to limit."""
    primes = tuple(n for n in range(2, limit + 1) if is_prime(n))
    if odd_only:
        return tuple(p for p in primes if p != 2)
    return primes


def prime_factors(n: int) -> tuple[int, ...]:
    """Return distinct prime factors of abs(n)."""
    n = abs(n)
    if n < 2:
        return ()
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            factors.append(divisor)
            while n % divisor == 0:
                n //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if n > 1:
        factors.append(n)
    return tuple(factors)


def radical(values: Iterable[int]) -> tuple[int, ...]:
    """Return sorted distinct prime factors across values."""
    support: set[int] = set()
    for value in values:
        support.update(prime_factors(value))
    return tuple(sorted(support))


def shannon_entropy(counts: Iterable[int]) -> float:
    """Return Shannon entropy in bits for a sequence of nonnegative counts."""
    positive = [count for count in counts if count > 0]
    total = sum(positive)
    if total == 0:
        return 0.0
    entropy = 0.0
    for count in positive:
        probability = count / total
        entropy -= probability * log2(probability)
    return entropy


def primitive_root_mod_prime(prime: int) -> int:
    """Return the least primitive root modulo an odd prime."""
    if prime == 2:
        return 1
    if not is_prime(prime):
        raise ValueError(f"expected prime, got {prime}")
    factors = prime_factors(prime - 1)
    for candidate in range(2, prime):
        if all(pow(candidate, (prime - 1) // factor, prime) != 1 for factor in factors):
            return candidate
    raise ValueError(f"no primitive root found for {prime}")


def stable_float(value: float, digits: int = 10) -> float:
    """Round floats for deterministic CSV output without hiding signal."""
    return round(value, digits)
