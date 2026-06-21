"""Nearby-level robustness audit for the focused `(5,4,5)` route."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from .newform_coefficient_importer import NewformCoefficientImportSummary
from .obstruction_progress_score import ObstructionProgressRecord


@dataclass(frozen=True)
class LevelRobustnessRecord:
    """One candidate comparison level in the robustness audit."""

    signature: str
    level: int
    factorization_hint: str
    level_source: str
    newform_count: int
    coefficient_status: str
    trace_filter_status: str
    robustness_label: str
    notes: str
    route_ceiling_label: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def _factorization_hint(level: int) -> str:
    value = level
    parts: list[str] = []
    for prime in (2, 5, 11):
        exponent = 0
        while value % prime == 0 and value > 0:
            value //= prime
            exponent += 1
        if exponent == 1:
            parts.append(str(prime))
        elif exponent > 1:
            parts.append(f"{prime}^{exponent}")
    if value != 1:
        parts.append(str(value))
    return " * ".join(parts) if parts else str(level)


def candidate_levels_545() -> tuple[int, ...]:
    """Return nearby levels built from powers of 2, 5, and 11 around 220."""
    levels: set[int] = {20, 44, 55, 110, 220, 440, 550, 880, 1100, 2420}
    for a_exp in range(0, 4):
        for b_exp in range(0, 3):
            for c_exp in range(0, 3):
                level = (2**a_exp) * (5**b_exp) * (11**c_exp)
                if 1 < level <= 2420 and any(level % prime == 0 for prime in (5, 11)):
                    levels.add(level)
    return tuple(sorted(levels))


def build_level_robustness_545(
    *,
    coefficient_summary: NewformCoefficientImportSummary,
    progress_row: ObstructionProgressRecord,
    levels: Iterable[int] | None = None,
) -> list[LevelRobustnessRecord]:
    """Build nearby-level robustness records without changing route labels."""
    records: list[LevelRobustnessRecord] = []
    for level in levels or candidate_levels_545():
        if level == 220:
            if coefficient_summary.sage_status == "completed" and progress_row.progress_label == "trace_mismatch_candidate":
                label = "level_220_mismatch_candidate"
                trace_status = progress_row.progress_label
            elif coefficient_summary.sage_status == "completed":
                label = "nearby_level_survivor_exists" if progress_row.newforms_surviving_all_filters else "level_data_insufficient"
                trace_status = progress_row.progress_label
            else:
                label = "level_data_insufficient"
                trace_status = "not_checked"
            records.append(
                LevelRobustnessRecord(
                    signature="5-4-5",
                    level=level,
                    factorization_hint=_factorization_hint(level),
                    level_source="current_route_target",
                    newform_count=coefficient_summary.newform_count,
                    coefficient_status=coefficient_summary.sage_status,
                    trace_filter_status=trace_status,
                    robustness_label=label,
                    notes="Level 220 is the only level with imported coefficient data in the current roundtrip.",
                    route_ceiling_label="worth_human_modular_review",
                )
            )
            continue
        records.append(
            LevelRobustnessRecord(
                signature="5-4-5",
                level=level,
                factorization_hint=_factorization_hint(level),
                level_source="nearby_2_5_11_support",
                newform_count=0,
                coefficient_status="not_checked",
                trace_filter_status="not_checked",
                robustness_label="level_data_insufficient",
                notes="No Sage coefficient extraction has been run for this nearby level.",
                route_ceiling_label="worth_human_modular_review",
            )
        )
    return records


def level_robustness_markdown(rows: Iterable[LevelRobustnessRecord]) -> str:
    """Render the nearby-level robustness report."""
    row_list = list(rows)
    survivor_like = [row for row in row_list if row.robustness_label == "nearby_level_survivor_exists"]
    lines = [
        "# Level 220 Robustness For `(5,4,5)`",
        "",
        "This report varies plausible levels supported by primes `{2,5,11}`. Only imported Sage coefficient data is used.",
        "",
        f"- Nearby levels with survivor evidence: `{len(survivor_like)}`.",
        "",
        "| level | factorization | source | newforms | coefficient status | trace status | label |",
        "| ---: | --- | --- | ---: | --- | --- | --- |",
    ]
    if not row_list:
        lines.append("| none | none | none | 0 | missing | not_checked | level_data_insufficient |")
    for row in row_list:
        lines.append(
            f"| {row.level} | `{row.factorization_hint}` | `{row.level_source}` | {row.newform_count} | "
            f"`{row.coefficient_status}` | `{row.trace_filter_status}` | `{row.robustness_label}` |"
        )
    lines.extend(
        [
            "",
            "If a nearby level later has surviving newforms, the safe record label is `nearby_level_survivor_exists`, and the route interpretation should be treated as level-formula uncertainty. Until those jobs are run, nearby levels are `level_data_insufficient`.",
            "",
        ]
    )
    return "\n".join(lines)
