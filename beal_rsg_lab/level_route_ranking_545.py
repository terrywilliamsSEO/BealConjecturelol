"""Rank candidate comparison levels for the focused `(5,4,5)` route."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from .candidate_level_generator_545 import CandidateLevelRecord545, build_candidate_levels_545
from .trace_filter_across_levels_545 import TraceFilterAcrossLevelsRecord545


SAFE_LEVEL_ROUTE_LABELS_545 = {
    "multi_level_trace_pressure_candidate",
    "level_sensitive_route",
    "level_data_insufficient",
    "conductor_gap_blocks_upgrade",
    "coefficient_field_blocked",
}


@dataclass(frozen=True)
class LevelRouteRankingRecord545:
    """One ranked candidate-level route row."""

    signature: str
    rank: int
    level: int
    factorization: str
    includes_11: bool
    conductor_plausibility_score: int
    conductor_plausibility_label: str
    newform_count: int
    level_trace_label: str
    surviving_newforms: str
    first_eliminators: str
    coefficient_field_status: str
    trace_strength_score: int
    coefficient_field_score: int
    human_review_priority_score: int
    aggregate_route_label: str
    route_ceiling_label: str
    reason: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def _write_csv(path: Path, rows: Iterable[dict[str, object]]) -> None:
    row_list = list(rows)
    if not row_list:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in row_list:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(row_list)


def _trace_strength(label: str) -> int:
    return {
        "level_trace_mismatch_candidate": 4,
        "level_survivor_exists": 2,
        "coefficient_field_blocked": 1,
        "level_data_insufficient": 0,
    }.get(label, 0)


def _field_score(status: str) -> int:
    return {
        "all_clear": 3,
        "mixed_or_unclear": 1,
        "coefficient_field_blocked": 0,
        "no_coefficients": 0,
    }.get(status, 0)


def _aggregate_label(trace_rows: list[TraceFilterAcrossLevelsRecord545]) -> tuple[str, str]:
    completed = [row for row in trace_rows if row.level_trace_label != "level_data_insufficient"]
    if not completed:
        return "level_data_insufficient", "Candidate-level Sage data is not available across the generated comparison levels."
    if any(row.level_trace_label == "coefficient_field_blocked" for row in completed):
        return "coefficient_field_blocked", "At least one candidate level is blocked by coefficient-field reduction data."
    mismatch_levels = [row.level for row in completed if row.level_trace_label == "level_trace_mismatch_candidate"]
    survivor_levels = [row.level for row in completed if row.level_trace_label == "level_survivor_exists"]
    if survivor_levels:
        return "level_sensitive_route", "At least one plausible candidate level has surviving newforms or branches."
    if len(mismatch_levels) > 1:
        return "multi_level_trace_pressure_candidate", "More than one candidate level has full trace-mismatch pressure."
    if mismatch_levels == [220]:
        return "conductor_gap_blocks_upgrade", "Only level 220 has trace-mismatch pressure and its conductor provenance is weak."
    if mismatch_levels:
        return "multi_level_trace_pressure_candidate", "A non-baseline candidate level has trace-mismatch pressure and needs conductor review."
    return "level_data_insufficient", "No candidate level produced a decisive trace-filter outcome."


def build_level_route_ranking_545(
    candidate_rows: Iterable[CandidateLevelRecord545] | None = None,
    trace_rows: Iterable[TraceFilterAcrossLevelsRecord545] | None = None,
) -> list[LevelRouteRankingRecord545]:
    """Rank candidate levels by conductor plausibility and cross-level trace behavior."""
    candidates = list(candidate_rows) if candidate_rows is not None else build_candidate_levels_545()
    traces = list(trace_rows or [])
    trace_by_level = {row.level: row for row in traces}
    aggregate_label, aggregate_reason = _aggregate_label(traces)
    if aggregate_label not in SAFE_LEVEL_ROUTE_LABELS_545:
        aggregate_label = "level_data_insufficient"
        aggregate_reason = "Unexpected level-route label was downgraded to level_data_insufficient."
    scored: list[tuple[tuple[int, int, int, int, int], LevelRouteRankingRecord545]] = []
    for candidate in candidates:
        trace = trace_by_level.get(candidate.level)
        trace_label = trace.level_trace_label if trace else "level_data_insufficient"
        field_status = trace.coefficient_field_status if trace else "no_coefficients"
        trace_score = _trace_strength(trace_label)
        coefficient_score = _field_score(field_status)
        no_11_bonus = 1 if not candidate.includes_11 else 0
        human_priority = (
            candidate.conductor_plausibility_score
            + trace_score
            + coefficient_score
            + no_11_bonus
            - min(trace.newform_count if trace else 0, 5)
        )
        scored.append(
            (
                (
                    -human_priority,
                    candidate.includes_11,
                    trace.newform_count if trace else 0,
                    -candidate.conductor_plausibility_score,
                    candidate.level,
                ),
                LevelRouteRankingRecord545(
                    signature="5-4-5",
                    rank=0,
                    level=candidate.level,
                    factorization=candidate.factorization,
                    includes_11=candidate.includes_11,
                    conductor_plausibility_score=candidate.conductor_plausibility_score,
                    conductor_plausibility_label=candidate.conductor_plausibility_label,
                    newform_count=trace.newform_count if trace else 0,
                    level_trace_label=trace_label,
                    surviving_newforms=trace.surviving_newforms if trace else "",
                    first_eliminators=trace.first_eliminators if trace else "",
                    coefficient_field_status=field_status,
                    trace_strength_score=trace_score,
                    coefficient_field_score=coefficient_score,
                    human_review_priority_score=human_priority,
                    aggregate_route_label=aggregate_label,
                    route_ceiling_label="worth_human_modular_review",
                    reason=aggregate_reason,
                ),
            )
        )
    records: list[LevelRouteRankingRecord545] = []
    for rank, (_, record) in enumerate(sorted(scored, key=lambda item: item[0]), start=1):
        records.append(
            LevelRouteRankingRecord545(
                signature=record.signature,
                rank=rank,
                level=record.level,
                factorization=record.factorization,
                includes_11=record.includes_11,
                conductor_plausibility_score=record.conductor_plausibility_score,
                conductor_plausibility_label=record.conductor_plausibility_label,
                newform_count=record.newform_count,
                level_trace_label=record.level_trace_label,
                surviving_newforms=record.surviving_newforms,
                first_eliminators=record.first_eliminators,
                coefficient_field_status=record.coefficient_field_status,
                trace_strength_score=record.trace_strength_score,
                coefficient_field_score=record.coefficient_field_score,
                human_review_priority_score=record.human_review_priority_score,
                aggregate_route_label=record.aggregate_route_label,
                route_ceiling_label=record.route_ceiling_label,
                reason=record.reason,
            )
        )
    return records


def level_route_ranking_545_markdown(rows: Iterable[LevelRouteRankingRecord545]) -> str:
    """Render the candidate-level route ranking."""
    row_list = list(rows)
    aggregate = row_list[0].aggregate_route_label if row_list else "level_data_insufficient"
    reason = row_list[0].reason if row_list else "No candidate-level ranking rows were generated."
    lines = [
        "# Level Route Ranking For `(5,4,5)`",
        "",
        f"- Aggregate route label: `{aggregate}`.",
        "- Route ceiling: `worth_human_modular_review`.",
        f"- Reason: {reason}",
        "",
        "| rank | level | factorization | includes 11 | trace label | newforms | field status | priority | first eliminators | survivors |",
        "| ---: | ---: | --- | --- | --- | ---: | --- | ---: | --- | --- |",
    ]
    for row in row_list:
        lines.append(
            f"| {row.rank} | {row.level} | `{row.factorization}` | `{row.includes_11}` | "
            f"`{row.level_trace_label}` | {row.newform_count} | `{row.coefficient_field_status}` | "
            f"{row.human_review_priority_score} | `{row.first_eliminators or 'none'}` | "
            f"`{row.surviving_newforms or 'none'}` |"
        )
    lines.extend(
        [
            "",
            "This ranking is a target-discovery aid. It does not establish which level is mathematically correct.",
            "",
        ]
    )
    return "\n".join(lines)


def write_level_route_ranking_545_csv(
    path: Path,
    rows: Iterable[LevelRouteRankingRecord545],
) -> Path:
    """Write `level_route_ranking_545.csv`."""
    _write_csv(path, [row.to_flat_dict() for row in rows])
    return path


def write_level_route_ranking_545_markdown(
    path: Path,
    rows: Iterable[LevelRouteRankingRecord545],
) -> Path:
    """Write `LEVEL_ROUTE_RANKING_545.md`."""
    path.write_text(level_route_ranking_545_markdown(rows), encoding="utf-8")
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write focused 5-4-5 level-route ranking rows.")
    parser.add_argument("--output", default="level_route_ranking_545.csv")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows = build_level_route_ranking_545()
    write_level_route_ranking_545_csv(Path(args.output), rows)
    print(Path(args.output).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
