"""Multiplicative-character fingerprints for unit survivor geometry."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from math import log2

from .number_theory import primitive_root_mod_prime, shannon_entropy
from .unit_survivor_geometry import UnitSurvivorGeometry


@dataclass(frozen=True)
class CharacterFingerprint:
    """Character-class distribution data for one sparse row."""

    signature: tuple[int, int, int]
    ell: int
    legendre_distribution: dict[str, int]
    legendre_entropy: float
    dominant_legendre_pattern: str
    dominant_legendre_share: float
    higher_character_order: int
    higher_character_distribution: dict[str, int]
    higher_character_entropy: float
    dominant_higher_character_pattern: str
    dominant_higher_character_share: float
    repeated_character_constraint: bool
    character_fingerprint: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signature"] = "-".join(str(part) for part in self.signature)
        data["legendre_distribution"] = ";".join(
            f"{key}:{value}" for key, value in sorted(self.legendre_distribution.items())
        )
        data["higher_character_distribution"] = ";".join(
            f"{key}:{value}" for key, value in sorted(self.higher_character_distribution.items())
        )
        return data


def _discrete_log_table(ell: int) -> dict[int, int]:
    root = primitive_root_mod_prime(ell)
    table: dict[int, int] = {}
    value = 1
    for exponent in range(ell - 1):
        table[value] = exponent
        value = (value * root) % ell
    return table


def _legendre(value: int, ell: int) -> int:
    symbol = pow(value, (ell - 1) // 2, ell)
    return -1 if symbol == ell - 1 else symbol


def _best_character_order(ell: int) -> int:
    for order in (13, 11, 7, 5, 4, 3, 2):
        if (ell - 1) % order == 0:
            return order
    return 1


def _entropy(counts: Counter[str]) -> tuple[float, float]:
    entropy = shannon_entropy(counts.values())
    max_entropy = log2(len(counts)) if len(counts) > 1 else 0.0
    normalized = entropy / max_entropy if max_entropy else 0.0
    return round(entropy, 10), round(min(1.0, normalized), 10)


def compute_character_fingerprint(geometry: UnitSurvivorGeometry) -> CharacterFingerprint:
    """Compute Legendre and higher-character distributions for survivors."""
    log_table = _discrete_log_table(geometry.ell)
    order = _best_character_order(geometry.ell)
    legendre_counts: Counter[str] = Counter()
    higher_counts: Counter[str] = Counter()
    for u, v, w in geometry.survivor_triples:
        legendre_pattern = ",".join(str(_legendre(value, geometry.ell)) for value in (u, v, w))
        legendre_counts[legendre_pattern] += 1
        if order > 1:
            higher_pattern = ",".join(str(log_table[value] % order) for value in (u, v, w))
        else:
            higher_pattern = "0,0,0"
        higher_counts[higher_pattern] += 1

    legendre_entropy, _ = _entropy(legendre_counts)
    higher_entropy, _ = _entropy(higher_counts)
    total = max(1, len(geometry.survivor_triples))
    dominant_legendre, dominant_legendre_count = legendre_counts.most_common(1)[0] if legendre_counts else ("", 0)
    dominant_higher, dominant_higher_count = higher_counts.most_common(1)[0] if higher_counts else ("", 0)
    dominant_legendre_share = dominant_legendre_count / total
    dominant_higher_share = dominant_higher_count / total
    repeated = dominant_legendre_share >= 0.75 or dominant_higher_share >= 0.75
    fingerprint = (
        f"legendre={dominant_legendre}:{round(dominant_legendre_share, 4)}|"
        f"char{order}={dominant_higher}:{round(dominant_higher_share, 4)}"
    )
    return CharacterFingerprint(
        signature=geometry.signature,
        ell=geometry.ell,
        legendre_distribution=dict(legendre_counts),
        legendre_entropy=legendre_entropy,
        dominant_legendre_pattern=dominant_legendre,
        dominant_legendre_share=round(dominant_legendre_share, 10),
        higher_character_order=order,
        higher_character_distribution=dict(higher_counts),
        higher_character_entropy=higher_entropy,
        dominant_higher_character_pattern=dominant_higher,
        dominant_higher_character_share=round(dominant_higher_share, 10),
        repeated_character_constraint=repeated,
        character_fingerprint=fingerprint,
    )


def compute_character_fingerprints(geometries: list[UnitSurvivorGeometry]) -> list[CharacterFingerprint]:
    """Compute fingerprints for many sparse rows."""
    return [compute_character_fingerprint(geometry) for geometry in geometries]
