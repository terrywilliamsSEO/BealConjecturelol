"""Candidate comparison-level generator for the focused `(5,4,5)` route."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SAFE_CANDIDATE_LEVEL_LABELS_545 = {
    "current_baseline_heuristic",
    "plausible_without_11",
    "plausible_with_11",
    "exploratory_low_bad_prime_support",
}


@dataclass(frozen=True)
class CandidateLevelRecord545:
    """One candidate lowered comparison level."""

    signature: str
    level: int
    factorization: str
    exponent_2: int
    exponent_5: int
    exponent_11: int
    includes_11: bool
    is_current_baseline_220: bool
    conductor_plausibility_score: int
    conductor_plausibility_label: str
    bad_prime_core_source: str
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


def _factorization(level: int, exp2: int, exp5: int, exp11: int) -> str:
    if level == 1:
        return "1"
    parts = []
    if exp2:
        parts.append("2" if exp2 == 1 else f"2^{exp2}")
    if exp5:
        parts.append("5" if exp5 == 1 else f"5^{exp5}")
    if exp11:
        parts.append("11" if exp11 == 1 else f"11^{exp11}")
    return " * ".join(parts)


def _plausibility(exp2: int, exp5: int, exp11: int, level: int) -> tuple[int, str, str]:
    score = 0
    score += {0: 1, 1: 2, 2: 3, 3: 2}[exp2]
    score += {0: 2, 1: 3, 2: 2}[exp5]
    score += 2 if exp11 == 0 else 1
    if level == 220:
        return score, "current_baseline_heuristic", "Current level-220 route target retained as the baseline, but factor 11 remains unjustified."
    if exp2 == 0 and exp5 == 0:
        return score, "exploratory_low_bad_prime_support", "Both 2 and 5 are absent, so this is a low-support exploratory comparison level."
    if exp11 == 0:
        return score, "plausible_without_11", "This level tests the route after removing the currently unjustified factor 11."
    return score, "plausible_with_11", "This level keeps factor 11 as an exploratory variant pending conductor provenance."


def build_candidate_levels_545() -> list[CandidateLevelRecord545]:
    """Generate candidate levels from 2-, 5-, and optional 11-adic exponent variants."""
    rows: list[CandidateLevelRecord545] = []
    for exp2 in range(4):
        for exp5 in range(3):
            for exp11 in range(2):
                level = (2**exp2) * (5**exp5) * (11**exp11)
                score, label, reason = _plausibility(exp2, exp5, exp11, level)
                if label not in SAFE_CANDIDATE_LEVEL_LABELS_545:
                    label = "exploratory_low_bad_prime_support"
                    reason = "Unexpected candidate-level label was downgraded to exploratory_low_bad_prime_support."
                rows.append(
                    CandidateLevelRecord545(
                        signature="5-4-5",
                        level=level,
                        factorization=_factorization(level, exp2, exp5, exp11),
                        exponent_2=exp2,
                        exponent_5=exp5,
                        exponent_11=exp11,
                        includes_11=bool(exp11),
                        is_current_baseline_220=level == 220,
                        conductor_plausibility_score=score,
                        conductor_plausibility_label=label,
                        bad_prime_core_source="2^0..3 * 5^0..2 * 11^0..1",
                        route_ceiling_label="worth_human_modular_review",
                        reason=reason,
                    )
                )
    rows.sort(key=lambda row: (-row.conductor_plausibility_score, row.includes_11, row.level))
    return rows


def candidate_levels_545_markdown(rows: Iterable[CandidateLevelRecord545]) -> str:
    """Render candidate levels as Markdown."""
    row_list = list(rows)
    no_11 = [row.level for row in row_list if not row.includes_11]
    baseline = next((row for row in row_list if row.is_current_baseline_220), None)
    lines = [
        "# Candidate Comparison Levels For `(5,4,5)`",
        "",
        "Level 220 is no longer treated as the only target. This table expands the possible lowered comparison levels from bad-prime exponent variants.",
        "",
        f"- Candidate count: `{len(row_list)}`.",
        f"- Baseline level present: `{baseline is not None}`.",
        f"- Variants without factor 11: `{';'.join(str(item) for item in no_11)}`.",
        "- Every row remains capped at `worth_human_modular_review`.",
        "",
        "| level | factorization | e2 | e5 | e11 | includes 11 | score | label | reason |",
        "| ---: | --- | ---: | ---: | ---: | --- | ---: | --- | --- |",
    ]
    for row in row_list:
        lines.append(
            f"| {row.level} | `{row.factorization}` | {row.exponent_2} | {row.exponent_5} | "
            f"{row.exponent_11} | `{row.includes_11}` | {row.conductor_plausibility_score} | "
            f"`{row.conductor_plausibility_label}` | {row.reason} |"
        )
    lines.extend(
        [
            "",
            "The scores are only triage weights for human review. They do not establish a conductor or lowered level.",
            "",
        ]
    )
    return "\n".join(lines)


def write_candidate_levels_545_csv(path: Path, rows: Iterable[CandidateLevelRecord545]) -> Path:
    """Write `candidate_levels_545.csv`."""
    _write_csv(path, [row.to_flat_dict() for row in rows])
    return path


def write_candidate_levels_545_markdown(path: Path, rows: Iterable[CandidateLevelRecord545]) -> Path:
    """Write `CANDIDATE_LEVELS_545.md`."""
    path.write_text(candidate_levels_545_markdown(rows), encoding="utf-8")
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write focused 5-4-5 candidate level rows.")
    parser.add_argument("--output", default="candidate_levels_545.csv")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows = build_candidate_levels_545()
    write_candidate_levels_545_csv(Path(args.output), rows)
    print(Path(args.output).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
