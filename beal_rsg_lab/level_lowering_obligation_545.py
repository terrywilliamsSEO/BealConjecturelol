"""Level-lowering obligations for the focused `(5,4,5)` route."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SAFE_LEVEL_LOWERING_STATUS_LABELS = {
    "computed_route_evidence",
    "standard_input_needs_instantiation",
    "needs_human_review",
    "missing",
    "blocks_upgrade",
}


@dataclass(frozen=True)
class LevelLoweringObligationRecord:
    """One formal level-lowering obligation."""

    signature: str
    obligation_id: str
    obligation_name: str
    current_status: str
    blocks_upgrade: bool
    route_ceiling_label: str
    required_human_check: str

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


def build_level_lowering_obligations_545() -> list[LevelLoweringObligationRecord]:
    """Return the formal level-lowering obligations for `(5,4,5)`."""
    rows = [
        LevelLoweringObligationRecord(
            signature="5-4-5",
            obligation_id="LL545-001",
            obligation_name="Residual modulus is 5",
            current_status="needs_human_review",
            blocks_upgrade=True,
            route_ceiling_label="worth_human_modular_review",
            required_human_check="Justify that the mod-5 residual representation is the correct object for the comparison.",
        ),
        LevelLoweringObligationRecord(
            signature="5-4-5",
            obligation_id="LL545-002",
            obligation_name="Residual representation irreducible",
            current_status="missing",
            blocks_upgrade=True,
            route_ceiling_label="worth_human_modular_review",
            required_human_check="Prove irreducibility or state and eliminate all exceptional reducible cases.",
        ),
        LevelLoweringObligationRecord(
            signature="5-4-5",
            obligation_id="LL545-003",
            obligation_name="Modularity input",
            current_status="standard_input_needs_instantiation",
            blocks_upgrade=True,
            route_ceiling_label="worth_human_modular_review",
            required_human_check="Instantiate the modularity theorem for the exact elliptic curve over Q after the Frey attachment is proved.",
        ),
        LevelLoweringObligationRecord(
            signature="5-4-5",
            obligation_id="LL545-004",
            obligation_name="Level-lowering hypotheses",
            current_status="missing",
            blocks_upgrade=True,
            route_ceiling_label="worth_human_modular_review",
            required_human_check="Verify the ramification, minimality, and conductor-lowering hypotheses at every prime dividing the discriminant.",
        ),
        LevelLoweringObligationRecord(
            signature="5-4-5",
            obligation_id="LL545-005",
            obligation_name="Exact target level 220",
            current_status="blocks_upgrade",
            blocks_upgrade=True,
            route_ceiling_label="worth_human_modular_review",
            required_human_check="Prove the lowered level is exactly 220, including the roles of 2, 5, and 11.",
        ),
        LevelLoweringObligationRecord(
            signature="5-4-5",
            obligation_id="LL545-006",
            obligation_name="Good-prime trace comparison validity",
            current_status="computed_route_evidence",
            blocks_upgrade=True,
            route_ceiling_label="worth_human_modular_review",
            required_human_check="After the target level and coefficient-field reductions are justified, revalidate the q=13,17,41 trace comparisons.",
        ),
    ]
    return [
        row
        if row.current_status in SAFE_LEVEL_LOWERING_STATUS_LABELS
        else LevelLoweringObligationRecord(
            signature=row.signature,
            obligation_id=row.obligation_id,
            obligation_name=row.obligation_name,
            current_status="needs_human_review",
            blocks_upgrade=True,
            route_ceiling_label=row.route_ceiling_label,
            required_human_check="Unexpected level-lowering status was downgraded to needs_human_review.",
        )
        for row in rows
    ]


def level_lowering_obligations_545_markdown(rows: Iterable[LevelLoweringObligationRecord]) -> str:
    """Render level-lowering obligation rows."""
    row_list = list(rows)
    lines = [
        "# Level-Lowering Obligations For `(5,4,5)`",
        "",
        "These obligations must be discharged before the quantifier-safe trace elimination can become a valid modular-method argument.",
        "",
        "| id | obligation | status | blocks upgrade | required check |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in row_list:
        lines.append(
            f"| `{row.obligation_id}` | {row.obligation_name} | `{row.current_status}` | "
            f"`{row.blocks_upgrade}` | {row.required_human_check} |"
        )
    lines.extend(
        [
            "",
            "Until these obligations are supplied by hand, the route remains capped at `worth_human_modular_review`.",
            "",
        ]
    )
    return "\n".join(lines)


def write_level_lowering_obligations_545_csv(
    path: Path,
    rows: Iterable[LevelLoweringObligationRecord],
) -> Path:
    """Write `level_lowering_obligations_545.csv`."""
    _write_csv(path, [row.to_flat_dict() for row in rows])
    return path


def write_level_lowering_obligations_545_markdown(
    path: Path,
    rows: Iterable[LevelLoweringObligationRecord],
) -> Path:
    """Write `LEVEL_LOWERING_OBLIGATIONS_545.md`."""
    path.write_text(level_lowering_obligations_545_markdown(rows), encoding="utf-8")
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write focused 5-4-5 level-lowering obligation rows.")
    parser.add_argument("--output", default="level_lowering_obligations_545.csv")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows = build_level_lowering_obligations_545()
    write_level_lowering_obligations_545_csv(Path(args.output), rows)
    print(Path(args.output).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
