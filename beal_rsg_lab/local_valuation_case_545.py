"""Local valuation-mask classification for the focused `(5,4,5)` route."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from .good_prime_selector import GoodPrimeRecord


VALUATION_MASKS = ("unit", "A_only", "B_only", "C_only", "AB", "AC", "BC", "ABC")
PAIRWISE_OR_TRIPLE_MASKS = {"AB", "AC", "BC", "ABC"}


@dataclass(frozen=True)
class LocalValuationCaseRecord:
    """One mod-q valuation-mask case for `A^5 + B^4 = C^5`."""

    signature: str
    prime: int
    valuation_mask: str
    solution_count_mod_q: int
    classification: str
    primitive_compatible: bool
    reason: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def _power_image(prime: int, exponent: int) -> tuple[int, ...]:
    return tuple(sorted({pow(value, exponent, prime) for value in range(1, prime)}))


def _solution_count_for_mask(prime: int, mask: str) -> int:
    fifth = _power_image(prime, 5)
    fourth = _power_image(prime, 4)
    fifth_set = set(fifth)
    fourth_set = set(fourth)
    if mask == "unit":
        return sum(1 for a_value in fifth for b_value in fourth if (a_value + b_value) % prime in fifth_set)
    if mask == "A_only":
        return len(fourth_set & fifth_set)
    if mask == "B_only":
        return len(fifth_set)
    if mask == "C_only":
        return sum(1 for a_value in fifth for b_value in fourth if (a_value + b_value) % prime == 0)
    if mask == "ABC":
        return 1
    return 0


def _classify_mask(prime: int, mask: str, solution_count: int) -> tuple[str, bool, str]:
    if mask in PAIRWISE_OR_TRIPLE_MASKS:
        return (
            "primitive_forbidden",
            False,
            "If a primitive solution has q dividing at least two of A,B,C, the equation forces common q-divisibility or is excluded by primitivity.",
        )
    if solution_count == 0:
        return "impossible_mod_q", False, "No residue pattern of this valuation mask solves the equation modulo q."
    if mask == "unit":
        return "locally_possible", True, "Unit residue triples exist and are the cases tested by the current trace filter."
    return (
        "locally_possible",
        True,
        "Single-variable q-divisibility has mod-q unit solutions but gives singular reduction for the current Frey template.",
    )


def build_local_valuation_cases_545(good_prime_rows: Iterable[GoodPrimeRecord]) -> list[LocalValuationCaseRecord]:
    """Classify valuation masks for each selected good prime."""
    records: list[LocalValuationCaseRecord] = []
    for good_row in sorted((row for row in good_prime_rows if row.selected), key=lambda row: row.prime):
        for mask in VALUATION_MASKS:
            count = _solution_count_for_mask(good_row.prime, mask)
            classification, compatible, reason = _classify_mask(good_row.prime, mask, count)
            records.append(
                LocalValuationCaseRecord(
                    signature="5-4-5",
                    prime=good_row.prime,
                    valuation_mask=mask,
                    solution_count_mod_q=count,
                    classification=classification,
                    primitive_compatible=compatible,
                    reason=reason,
                )
            )
    return records
