"""Good-prime selection for focused modular trace audits."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .number_theory import prime_factors, primes_up_to


@dataclass(frozen=True)
class GoodPrimeRecord:
    """One prime selected or excluded for a good-prime trace audit."""

    signature: str
    level: int
    prime: int
    selected: bool
    exclusion_reason: str
    level_prime_factors: tuple[int, ...]

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["level_prime_factors"] = ";".join(str(item) for item in self.level_prime_factors)
        return data


def select_good_primes_545(
    *,
    level: int = 220,
    bound: int = 100,
    allow_residual_prime: bool = False,
) -> list[GoodPrimeRecord]:
    """Return selected good primes for the `(5,4,5)` level-220 audit."""
    factors = prime_factors(level)
    rows: list[GoodPrimeRecord] = []
    for prime in primes_up_to(bound, odd_only=False):
        reason = ""
        selected = True
        if level % prime == 0:
            selected = False
            reason = "divides_target_level"
        elif prime == 5 and not allow_residual_prime:
            selected = False
            reason = "residual_prime_excluded_by_default"
        if selected:
            reason = "selected_good_prime"
        rows.append(
            GoodPrimeRecord(
                signature="5-4-5",
                level=level,
                prime=prime,
                selected=selected,
                exclusion_reason=reason,
                level_prime_factors=factors,
            )
        )
    return rows


def selected_good_prime_values(rows: list[GoodPrimeRecord]) -> tuple[int, ...]:
    """Return just the selected prime values from good-prime rows."""
    return tuple(row.prime for row in rows if row.selected)

