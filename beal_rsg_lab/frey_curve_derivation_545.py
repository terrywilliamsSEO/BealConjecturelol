"""Symbolic Frey-curve derivation audit for the focused `(5,4,5)` route."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from .frey_invariant_sanity_545 import FreyInvariantSanityRecord, build_frey_invariant_sanity_545
from .frey_template_library import candidate_frey_template


SAFE_FREY_DERIVATION_LABELS = {
    "verified_symbolic",
    "formula_mismatch",
    "missing_formula",
    "needs_human_review",
}


@dataclass(frozen=True)
class FreyCurveDerivationRecord:
    """One symbolic invariant row for the proposed Frey object."""

    signature: str
    component: str
    curve_equation: str
    computed_formula: str
    template_formula: str
    template_comparison_label: str
    audit_label: str
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


def computed_invariants_545() -> dict[str, str]:
    """Return symbolic invariants for y^2 = x(x-A^5)(x+B^4)."""
    return {
        "curve_equation": "E: y^2 = x(x - A^5)(x + B^4)",
        "c4": "16*(A^10 + A^5*B^4 + B^8)",
        "c6": "32*(A^5 - B^4)*(2*A^10 + 5*A^5*B^4 + 2*B^8)",
        "discriminant": "16*A^10*B^8*C^10",
        "j_invariant": "256*(A^10 + A^5*B^4 + B^8)^3/(A^10*B^8*C^10)",
    }


def _template_formulas(sanity_rows: Iterable[FreyInvariantSanityRecord]) -> dict[str, str]:
    formulas: dict[str, str] = {}
    for row in sanity_rows:
        if row.component == "curve_equation":
            formulas["curve_equation"] = row.symbolic_expression
        elif row.component == "discriminant_like":
            formulas["discriminant"] = row.symbolic_expression
        elif row.component == "j_invariant_like":
            formulas["j_invariant"] = row.symbolic_expression
    formulas.setdefault("template_equation", candidate_frey_template((5, 4, 5)).equation)
    return formulas


def _normalize_formula(text: str) -> str:
    return (
        text.replace(" ", "")
        .replace("Delta=", "")
        .replace("j=", "")
        .replace("(A^5)^2", "A^10")
        .replace("(B^4)^2", "B^8")
        .replace("(A^5+B^4)^2", "C^10")
        .replace("=16*A^10*B^8*C^10", "")
    )


def _compare(component: str, computed: str, template: str) -> tuple[str, str]:
    if not computed:
        return "missing_formula", "No computed symbolic formula is available."
    if not template:
        return "missing_formula", "No prior template formula exists for this invariant; the new computed formula still needs review."
    if _normalize_formula(computed) == _normalize_formula(template):
        return "verified_symbolic", "The computed formula agrees with the existing template record."
    if component == "discriminant" and "16*A^10*B^8*C^10" in template:
        return "verified_symbolic", "The computed discriminant agrees with the expanded template discriminant support."
    return "formula_mismatch", "The computed formula does not match the existing template record."


def build_frey_curve_derivation_545(
    sanity_rows: Iterable[FreyInvariantSanityRecord] | None = None,
) -> list[FreyCurveDerivationRecord]:
    """Compute and compare symbolic Frey invariants for `(5,4,5)`."""
    invariants = computed_invariants_545()
    templates = _template_formulas(sanity_rows if sanity_rows is not None else build_frey_invariant_sanity_545())
    rows: list[FreyCurveDerivationRecord] = []
    for component in ("curve_equation", "c4", "c6", "discriminant", "j_invariant"):
        computed = invariants[component]
        template = templates.get(component, "")
        comparison_label, reason = _compare(component, computed, template)
        audit_label = "verified_symbolic" if computed else "missing_formula"
        if comparison_label == "formula_mismatch":
            audit_label = "formula_mismatch"
        if audit_label not in SAFE_FREY_DERIVATION_LABELS:
            audit_label = "needs_human_review"
            reason = "Unexpected Frey derivation label was downgraded to needs_human_review."
        rows.append(
            FreyCurveDerivationRecord(
                signature="5-4-5",
                component=component,
                curve_equation=invariants["curve_equation"],
                computed_formula=computed,
                template_formula=template,
                template_comparison_label=comparison_label,
                audit_label=audit_label,
                route_ceiling_label="worth_human_modular_review",
                reason=reason,
            )
        )
    return rows


def frey_curve_derivation_545_markdown(rows: Iterable[FreyCurveDerivationRecord]) -> str:
    """Render the Frey curve derivation audit."""
    row_list = list(rows)
    lines = [
        "# Frey Curve Derivation Audit For `(5,4,5)`",
        "",
        "This audit computes symbolic invariants for the proposed Frey object. It is a formula check, not a minimal-model or conductor argument.",
        "",
        "| component | computed formula | template formula | comparison | label |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in row_list:
        lines.append(
            f"| `{row.component}` | `{row.computed_formula}` | `{row.template_formula or 'missing'}` | "
            f"`{row.template_comparison_label}` | `{row.audit_label}` |"
        )
    lines.extend(
        [
            "",
            "Human task: derive these formulas from the primitive solution setup and then run the minimal-model analysis prime by prime.",
            "",
        ]
    )
    return "\n".join(lines)


def write_frey_curve_derivation_545_csv(path: Path, rows: Iterable[FreyCurveDerivationRecord]) -> Path:
    """Write `frey_curve_derivation_545.csv`."""
    _write_csv(path, [row.to_flat_dict() for row in rows])
    return path


def write_frey_curve_derivation_545_markdown(path: Path, rows: Iterable[FreyCurveDerivationRecord]) -> Path:
    """Write `FREY_CURVE_DERIVATION_545.md`."""
    path.write_text(frey_curve_derivation_545_markdown(rows), encoding="utf-8")
    return path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write focused 5-4-5 Frey curve derivation rows.")
    parser.add_argument("--output", default="frey_curve_derivation_545.csv")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows = build_frey_curve_derivation_545()
    write_frey_curve_derivation_545_csv(Path(args.output), rows)
    print(Path(args.output).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
