"""Normalize generalized Fermat signatures for modular-shadow routing."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass

from .number_theory import radical
from .rsg_residue_engine import Signature


TARGET_SIGNATURES: tuple[Signature, ...] = (
    (4, 7, 7),
    (7, 4, 7),
    (5, 4, 5),
    (4, 5, 5),
    (3, 5, 5),
    (5, 3, 5),
    (7, 7, 4),
    (3, 4, 3),
)


@dataclass(frozen=True)
class NormalizedSignature:
    """Signature metadata, normalized up to swapping A and B."""

    signature: Signature
    canonical_signature: Signature
    canonical_signature_id: str
    swapped_ab: bool
    symmetric_ab: bool
    repeated_exponents: tuple[int, ...]
    has_repeated_exponent: bool
    fourth_power_involvement: bool
    mixed_prime_structure: bool
    exponent_radical_support: tuple[int, ...]
    target_route: bool

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signature"] = "-".join(str(part) for part in self.signature)
        data["canonical_signature"] = "-".join(str(part) for part in self.canonical_signature)
        data["repeated_exponents"] = ";".join(str(part) for part in self.repeated_exponents)
        data["exponent_radical_support"] = ";".join(str(part) for part in self.exponent_radical_support)
        return data


def canonicalize_signature(signature: Signature) -> tuple[Signature, bool]:
    """Canonicalize a signature up to swapping the A/B exponents."""
    p, q, r = signature
    swapped = (q, p, r)
    if swapped < signature:
        return swapped, True
    return signature, False


def normalize_signature(signature: Signature) -> NormalizedSignature:
    """Return normalization metadata for a signature."""
    canonical, swapped = canonicalize_signature(signature)
    counts = Counter(signature)
    repeated = tuple(sorted(exponent for exponent, count in counts.items() if count > 1))
    support = radical(signature)
    target_canonicals = {canonicalize_signature(item)[0] for item in TARGET_SIGNATURES}
    return NormalizedSignature(
        signature=signature,
        canonical_signature=canonical,
        canonical_signature_id="-".join(str(part) for part in canonical),
        swapped_ab=swapped,
        symmetric_ab=signature[0] == signature[1],
        repeated_exponents=repeated,
        has_repeated_exponent=bool(repeated),
        fourth_power_involvement=4 in signature,
        mixed_prime_structure=len(set(support)) >= 2,
        exponent_radical_support=support,
        target_route=canonical in target_canonicals,
    )


def normalize_signatures(signatures: list[Signature] | tuple[Signature, ...]) -> list[NormalizedSignature]:
    """Normalize many signatures."""
    return [normalize_signature(signature) for signature in signatures]
