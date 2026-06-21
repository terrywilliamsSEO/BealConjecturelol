"""Small-prime sensitivity profiles for the focused `(5,4,5)` trace filter."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Callable, Iterable

from .trace_congruence_filter_545 import TraceCongruenceFilterRecord


PrimePredicate = Callable[[int], bool]


@dataclass(frozen=True)
class SmallPrimeSensitivityRecord:
    """Sensitivity result for one good-prime profile."""

    signature: str
    profile_name: str
    profile_description: str
    primes_used: tuple[int, ...]
    surviving_newform_count: int
    eliminated_newform_count: int
    first_eliminating_primes: str
    mismatch_depends_entirely_on_q3: bool
    sensitivity_label: str
    route_ceiling_label: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["primes_used"] = ";".join(str(item) for item in self.primes_used)
        return data


def sensitivity_profiles_545() -> list[tuple[str, str, PrimePredicate]]:
    """Return the fixed sensitivity profiles requested for `(5,4,5)`."""
    return [
        ("exclude_q_3", "Exclude q=3.", lambda prime: prime != 3),
        ("exclude_q_3_7", "Exclude q in {3,7}.", lambda prime: prime not in {3, 7}),
        ("exclude_q_lt_11", "Use only q >= 11.", lambda prime: prime >= 11),
        ("exclude_q_lt_17", "Use only q >= 17.", lambda prime: prime >= 17),
        ("use_only_q_ge_17", "Use only q >= 17.", lambda prime: prime >= 17),
    ]


def _profile_counts(
    rows: list[TraceCongruenceFilterRecord],
    *,
    newform_indices: tuple[int, ...],
) -> tuple[int, int, str]:
    surviving = 0
    eliminated = 0
    firsts: list[str] = []
    by_newform: dict[int, list[TraceCongruenceFilterRecord]] = {}
    for row in rows:
        by_newform.setdefault(row.newform_index, []).append(row)
    for index in newform_indices:
        newform_rows = sorted(by_newform.get(index, []), key=lambda row: row.prime)
        first = next((row for row in newform_rows if row.filter_classification == "eliminated"), None)
        if first is None:
            surviving += 1
        else:
            eliminated += 1
            firsts.append(f"newform_{index}:q={first.prime}")
    return surviving, eliminated, ";".join(firsts)


def build_small_prime_sensitivity_545(
    filter_rows: Iterable[TraceCongruenceFilterRecord],
    *,
    newform_count: int,
) -> list[SmallPrimeSensitivityRecord]:
    """Rerun trace-filter summaries under small-prime exclusion profiles."""
    rows = list(filter_rows)
    indices = tuple(range(newform_count))
    exclude_q3_rows = [row for row in rows if row.prime != 3]
    q3_surviving, q3_eliminated, _ = _profile_counts(exclude_q3_rows, newform_indices=indices)
    full_mismatch = newform_count > 0 and _profile_counts(rows, newform_indices=indices)[1] == newform_count
    depends_on_q3 = full_mismatch and q3_eliminated < newform_count
    records: list[SmallPrimeSensitivityRecord] = []
    for name, description, predicate in sensitivity_profiles_545():
        profile_rows = [row for row in rows if predicate(row.prime)]
        primes_used = tuple(sorted({row.prime for row in profile_rows}))
        surviving, eliminated, firsts = _profile_counts(profile_rows, newform_indices=indices)
        if name == "use_only_q_ge_17" and eliminated == newform_count and newform_count > 0:
            label = "robust_trace_mismatch_candidate"
        elif name == "exclude_q_3" and depends_on_q3:
            label = "small_prime_dependent"
        elif eliminated == newform_count and newform_count > 0:
            label = "trace_mismatch_candidate"
        elif not profile_rows:
            label = "trace_data_insufficient"
        else:
            label = "trace_survivor_exists"
        records.append(
            SmallPrimeSensitivityRecord(
                signature="5-4-5",
                profile_name=name,
                profile_description=description,
                primes_used=primes_used,
                surviving_newform_count=surviving,
                eliminated_newform_count=eliminated,
                first_eliminating_primes=firsts,
                mismatch_depends_entirely_on_q3=depends_on_q3,
                sensitivity_label=label,
                route_ceiling_label="worth_human_modular_review",
            )
        )
    return records


def small_prime_sensitivity_markdown(rows: Iterable[SmallPrimeSensitivityRecord]) -> str:
    """Render the small-prime sensitivity report."""
    row_list = list(rows)
    lines = [
        "# Small-Prime Sensitivity For `(5,4,5)`",
        "",
        "This report checks whether the current trace mismatch is driven by the smallest good primes.",
        "",
        "| profile | primes used | surviving | eliminated | first eliminators | label | q=3 only |",
        "| --- | --- | ---: | ---: | --- | --- | --- |",
    ]
    if not row_list:
        lines.append("| none | none | 0 | 0 | none | trace_data_insufficient | False |")
    for row in row_list:
        primes = ";".join(str(item) for item in row.primes_used) or "none"
        lines.append(
            f"| `{row.profile_name}` | `{primes}` | {row.surviving_newform_count} | "
            f"{row.eliminated_newform_count} | `{row.first_eliminating_primes or 'none'}` | "
            f"`{row.sensitivity_label}` | `{row.mismatch_depends_entirely_on_q3}` |"
        )
    lines.extend(
        [
            "",
            "Interpretation: if removing `q=3` restores a survivor, the safe label is `small_prime_dependent`. If the mismatch survives using only `q >= 17`, the safe label is `robust_trace_mismatch_candidate`.",
            "",
        ]
    )
    return "\n".join(lines)
