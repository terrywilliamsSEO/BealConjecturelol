"""Optional Sage sanity script generator for the focused `(5,4,5)` conductor route."""

from __future__ import annotations

import argparse
import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class SageConductorSanityManifestRecord:
    """One generated Sage sanity artifact row."""

    signature: str
    artifact: str
    sample_type: str
    purpose: str
    primes: str
    output_path: str
    mathematical_status: str
    route_ceiling_label: str

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


def sage_conductor_sanity_545_script() -> str:
    """Return a Sage script for symbolic and synthetic conductor sanity checks."""
    return """# Synthetic Sage sanity checks for the focused (5,4,5) route.
# This file is for formula and behavior sanity checks only. It is not mathematical evidence.

R.<A,B,C> = PolynomialRing(QQ)
c4 = 16*(A^10 + A^5*B^4 + B^8)
c6 = 32*(A^5 - B^4)*(2*A^10 + 5*A^5*B^4 + 2*B^8)
Delta = 16*A^10*B^8*C^10
j = 256*(A^10 + A^5*B^4 + B^8)^3/(A^10*B^8*C^10)

print("c4 =", c4)
print("c6 =", c6)
print("Delta =", Delta)
print("j =", j)

def frey_curve_from_pair(a, b):
    # y^2 = x(x - a^5)(x + b^4)
    return EllipticCurve([0, b^4 - a^5, 0, -a^5*b^4, 0])

print("\\nFinite-field local residue samples for A^5 + B^4 = C^5:")
for p in [3, 13, 17, 41, 61]:
    F = GF(p)
    found = []
    for a in F:
        for b in F:
            for c in F:
                if a != 0 and b != 0 and c != 0 and a^5 + b^4 == c^5:
                    found.append((Integer(a), Integer(b), Integer(c)))
                    break
            if found:
                break
        if found:
            break
    print("p =", p, "sample =", found[0] if found else None)

print("\\nOptional exact integral samples:")
print("Add exact integer triples manually before interpreting minimal models or conductors.")
manual_exact_triples = []
for a, b, c in manual_exact_triples:
    if a^5 + b^4 != c^5:
        print("skipping non-exact triple", (a, b, c))
        continue
    E = frey_curve_from_pair(a, b)
    print("triple", (a, b, c), "minimal discriminant", E.minimal_discriminant(), "conductor", E.conductor())
"""


def build_sage_conductor_sanity_manifest_545(script_path: Path) -> list[SageConductorSanityManifestRecord]:
    """Build the manifest for the optional Sage sanity script."""
    return [
        SageConductorSanityManifestRecord(
            signature="5-4-5",
            artifact=script_path.name,
            sample_type="symbolic_formulas_and_finite_field_residue_samples",
            purpose="Sanity-check displayed invariant formulas and provide optional finite-field residue samples.",
            primes="3;13;17;41;61",
            output_path=script_path.as_posix(),
            mathematical_status="synthetic_sanity_only",
            route_ceiling_label="worth_human_modular_review",
        )
    ]


def write_sage_conductor_sanity_samples_545(
    run_dir: Path,
) -> tuple[Path, Path, list[SageConductorSanityManifestRecord]]:
    """Write `sage_conductor_sanity_545.sage` and its manifest CSV."""
    script_path = run_dir / "sage_conductor_sanity_545.sage"
    manifest_path = run_dir / "sage_conductor_sanity_manifest_545.csv"
    script_path.write_text(sage_conductor_sanity_545_script(), encoding="utf-8")
    rows = build_sage_conductor_sanity_manifest_545(script_path)
    _write_csv(manifest_path, [row.to_flat_dict() for row in rows])
    return script_path, manifest_path, rows


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Write focused 5-4-5 Sage conductor sanity artifacts.")
    parser.add_argument("--output-dir", default=".")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    script_path, manifest_path, _ = write_sage_conductor_sanity_samples_545(Path(args.output_dir))
    print(script_path.as_posix())
    print(manifest_path.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
