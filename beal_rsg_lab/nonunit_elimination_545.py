"""Focused nonunit branch elimination audit for q=13 and q=17."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from .good_prime_selector import GoodPrimeRecord
from .local_valuation_case_545 import build_local_valuation_cases_545
from .valuation_mask_lift_545 import build_valuation_mask_lifts_545


TARGET_PRIMES_545 = (13, 17)
NONUNIT_MASKS = ("A_only", "B_only", "C_only", "AB", "AC", "BC", "ABC")


@dataclass(frozen=True)
class NonunitEliminationRecord:
    """Nonunit branch status for q=13 or q=17."""

    signature: str
    prime: int
    valuation_mask: str
    possible_mod_q: bool
    possible_mod_q2: bool
    possible_mod_q3: bool
    primitive_forbidden: bool
    valuation_growth_detected: bool
    unresolved: bool
    branch_label: str
    reason: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def build_nonunit_eliminations_545(
    good_prime_rows: Iterable[GoodPrimeRecord],
    *,
    target_primes: tuple[int, ...] = TARGET_PRIMES_545,
) -> list[NonunitEliminationRecord]:
    """Classify nonunit branches for the target eliminating primes."""
    selected = [row for row in good_prime_rows if row.selected and row.prime in set(target_primes)]
    valuation_rows = [
        row for row in build_local_valuation_cases_545(selected) if row.valuation_mask in set(NONUNIT_MASKS)
    ]
    lift_rows = {
        (row.prime, row.valuation_mask): row for row in build_valuation_mask_lifts_545(valuation_rows)
    }
    records: list[NonunitEliminationRecord] = []
    for row in sorted(valuation_rows, key=lambda item: (item.prime, item.valuation_mask)):
        lift = lift_rows[(row.prime, row.valuation_mask)]
        primitive_forbidden = row.classification == "primitive_forbidden"
        possible_mod_q = row.classification == "locally_possible"
        possible_lift = lift.lift_classification == "valuation_stable"
        unresolved = possible_mod_q and row.valuation_mask in {"A_only", "B_only", "C_only"}
        if primitive_forbidden:
            branch_label = "primitive_forbidden"
        elif not possible_mod_q:
            branch_label = "impossible_mod_q"
        elif unresolved:
            branch_label = "unresolved"
        else:
            branch_label = "locally_possible"
        records.append(
            NonunitEliminationRecord(
                signature="5-4-5",
                prime=row.prime,
                valuation_mask=row.valuation_mask,
                possible_mod_q=possible_mod_q,
                possible_mod_q2=possible_lift and possible_mod_q,
                possible_mod_q3=possible_lift and possible_mod_q,
                primitive_forbidden=primitive_forbidden,
                valuation_growth_detected=lift.divisibility_strengthens,
                unresolved=unresolved,
                branch_label=branch_label,
                reason=(
                    "Single-divisibility branch is locally stable but not handled by the unit trace comparison."
                    if unresolved
                    else row.reason
                ),
            )
        )
    return records
