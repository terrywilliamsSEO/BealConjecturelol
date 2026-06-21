"""Explain heuristic conductor-like levels used by Sage follow-up jobs."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping

from .number_theory import prime_factors, radical
from .signature_normalizer import normalize_signature


@dataclass(frozen=True)
class LevelExplanationRecord:
    """Human-readable explanation for one candidate level."""

    signature: str
    normalized_signature: str
    level: int
    level_factorization: str
    primes_involved: tuple[int, ...]
    template_bad_primes: tuple[int, ...]
    candidate_level_source: str
    sage_confirmed_level: bool
    symbolic_or_heuristic: str
    placeholder_warning: str
    explanation: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["primes_involved"] = ";".join(str(item) for item in self.primes_involved)
        data["template_bad_primes"] = ";".join(str(item) for item in self.template_bad_primes)
        return data


def _value(row: Mapping[str, Any], key: str, default: str = "") -> str:
    value = row.get(key, default)
    return "" if value is None else str(value)


def _split_ints(value: str) -> tuple[int, ...]:
    output: list[int] = []
    for part in value.split(";"):
        if not part:
            continue
        try:
            output.append(int(part))
        except ValueError:
            continue
    return tuple(output)


def _parse_signature(signature: str) -> tuple[int, int, int]:
    parts = tuple(int(part) for part in signature.split("-") if part)
    if len(parts) != 3:
        raise ValueError(f"bad signature {signature!r}")
    return parts  # type: ignore[return-value]


def _factorization_text(n: int) -> str:
    if n <= 1:
        return str(n)
    factors: list[str] = []
    remaining = n
    for prime in prime_factors(n):
        exponent = 0
        while remaining % prime == 0:
            remaining //= prime
            exponent += 1
        factors.append(str(prime) if exponent == 1 else f"{prime}^{exponent}")
    return " * ".join(factors)


def _import_by_job(import_rows: Iterable[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {_value(row, "job_id"): row for row in import_rows if _value(row, "job_id")}


def _confidence_by_signature(confidence_rows: Iterable[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {_value(row, "signature"): row for row in confidence_rows if _value(row, "signature")}


def explain_candidate_levels(
    *,
    job_rows: Iterable[Mapping[str, Any]],
    import_rows: Iterable[Mapping[str, Any]],
    confidence_rows: Iterable[Mapping[str, Any]],
    only_modular_followup: bool = True,
) -> list[LevelExplanationRecord]:
    """Explain candidate levels for modular follow-up signatures."""
    imports = _import_by_job(import_rows)
    confidence = _confidence_by_signature(confidence_rows)
    rows: list[LevelExplanationRecord] = []
    for job in job_rows:
        signature = _value(job, "signature")
        if not signature:
            continue
        conf = confidence.get(signature, {})
        label = _value(conf, "updated_followup_label") or _value(job, "route_label")
        if only_modular_followup and label != "modular_followup_candidate":
            continue
        parsed = _parse_signature(signature)
        normalized = normalize_signature(parsed)
        primes_involved = _split_ints(_value(job, "primes_involved"))
        candidate_levels = _split_ints(_value(job, "candidate_levels"))
        imported = imports.get(_value(job, "job_id"), {})
        checked_levels = set(_split_ints(_value(imported, "checked_levels")))
        bad_primes = tuple(sorted({2, *radical(parsed), *primes_involved}))
        for level in candidate_levels:
            source = (
                "Generated from support {2, exponent radicals, local primes}; "
                "levels are base, 2*base, 4*base, and base times each support prime."
            )
            confirmed = level in checked_levels
            warning = (
                "Placeholder conductor-like level; requires a minimal-model, conductor, "
                "level-lowering, and irreducibility audit before mathematical use."
            )
            explanation = (
                f"For `{signature}`, level {level} factors as {_factorization_text(level)}. "
                f"The template bad-prime support is {', '.join(str(item) for item in bad_primes)}. "
                f"Sage {'completed a newform count at this level' if confirmed else 'did not confirm this level in the imported result'}."
            )
            rows.append(
                LevelExplanationRecord(
                    signature=signature,
                    normalized_signature=normalized.canonical_signature_id,
                    level=level,
                    level_factorization=_factorization_text(level),
                    primes_involved=primes_involved,
                    template_bad_primes=bad_primes,
                    candidate_level_source=source,
                    sage_confirmed_level=confirmed,
                    symbolic_or_heuristic="heuristic_symbolic",
                    placeholder_warning=warning,
                    explanation=explanation,
                )
            )
    rows.sort(key=lambda row: (row.signature, not row.sage_confirmed_level, row.level))
    return rows

