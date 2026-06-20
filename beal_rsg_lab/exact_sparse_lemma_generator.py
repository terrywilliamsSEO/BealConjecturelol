"""Generate human-readable sparse unit-survivor lemma candidates."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .artifact_explainer import ArtifactAssessment
from .character_fingerprint import CharacterFingerprint
from .padic_unit_lift import PadicUnitLiftRecord
from .rsg_residue_engine import power_residue_set
from .unit_survivor_geometry import UnitSurvivorGeometry


@dataclass(frozen=True)
class SparseLemmaExplanation:
    """Human-readable explanation for one sparse unit row."""

    signature: tuple[int, int, int]
    ell: int
    rank: str
    headline: str
    modular_explanation: str
    proof_gap: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["signature"] = "-".join(str(part) for part in self.signature)
        return data


def _subgroup_clause(variable: str, exponent: int, ell: int) -> str:
    residues = power_residue_set(exponent, ell)
    if len(residues) == 2 and set(residues) == {1, ell - 1}:
        return f"nonzero {exponent}th powers for {variable} are {{1,-1}}"
    if len(residues) <= 6:
        values = ",".join(str(value) for value in residues)
        return f"nonzero {exponent}th powers for {variable} are {{{values}}}"
    return f"nonzero {exponent}th powers for {variable} form a subgroup of size {len(residues)}"


def generate_sparse_lemma_explanation(
    geometry: UnitSurvivorGeometry,
    assessment: ArtifactAssessment,
    character: CharacterFingerprint,
    lift: PadicUnitLiftRecord,
) -> SparseLemmaExplanation:
    """Generate one sparse unit-survivor explanation."""
    p, q, r = geometry.signature
    clauses = [
        _subgroup_clause("A", p, geometry.ell),
        _subgroup_clause("B", q, geometry.ell),
        _subgroup_clause("C", r, geometry.ell),
    ]
    base = (
        f"At ell={geometry.ell}, {'; '.join(clauses)}. "
        f"The unit equation has {geometry.survivor_count} survivor triples out of "
        f"{geometry.pair_count} unit pairs, density {geometry.density}. "
        f"Dominant character pattern: {character.character_fingerprint}. "
        f"Unit lift status through ell^3: {lift.unit_lift_status}."
    )

    if assessment.verdict == "artifact_explained":
        rank = "artifact explained"
        headline = "sparsity explained by subgroup size"
        gap = "Not a lemma candidate unless a later modular-shadow layer separates it from subgroup-size controls."
    elif lift.collapse_or_rigid:
        rank = "lemma candidate"
        headline = "sparse unit geometry remains rigid under p-adic lift"
        gap = "Needs an exact p-adic lemma proving the observed lift rigidity persists."
    else:
        rank = "needs modular-shadow follow-up"
        headline = "sparse unit geometry not explained by first-pass controls"
        gap = "Needs stronger lift, character, or modular-shadow incompatibility checks."

    return SparseLemmaExplanation(
        signature=geometry.signature,
        ell=geometry.ell,
        rank=rank,
        headline=headline,
        modular_explanation=f"{base} {assessment.explanation}.",
        proof_gap=gap,
    )


def generate_sparse_lemma_explanations(
    geometries: list[UnitSurvivorGeometry],
    assessments: list[ArtifactAssessment],
    characters: list[CharacterFingerprint],
    lifts: list[PadicUnitLiftRecord],
    *,
    limit: int = 80,
) -> list[SparseLemmaExplanation]:
    """Generate explanations for sparse rows."""
    assessment_by_key = {(item.signature, item.ell): item for item in assessments}
    character_by_key = {(item.signature, item.ell): item for item in characters}
    lift_by_key = {(item.signature, item.ell): item for item in lifts}
    priority = {"lemma candidate": 3, "needs modular-shadow follow-up": 2, "artifact explained": 1}
    explanations = [
        generate_sparse_lemma_explanation(
            geometry,
            assessment_by_key[(geometry.signature, geometry.ell)],
            character_by_key[(geometry.signature, geometry.ell)],
            lift_by_key[(geometry.signature, geometry.ell)],
        )
        for geometry in geometries
    ]
    explanations.sort(key=lambda item: (priority[item.rank], item.ell), reverse=True)
    return explanations[:limit]
