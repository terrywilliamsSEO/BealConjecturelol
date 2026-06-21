"""Generate explicit modular-method obligations for human review."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class ProofObligationRecord:
    """One candidate's next mathematical obligations."""

    signature: str
    audit_review_label: str
    primary_obligation: str
    level_obligation: str
    trace_obligation: str
    calibration_obligation: str
    nonclaim_guardrail: str
    next_sage_command: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def _value(row: Mapping[str, Any], key: str, default: str = "") -> str:
    value = row.get(key, default)
    return "" if value is None else str(value)


def _levels(row: Mapping[str, Any]) -> str:
    checked = _value(row, "checked_levels")
    candidates = _value(row, "candidate_levels")
    return checked or candidates or "candidate levels from Sage manifest"


def build_proof_obligation_records(
    audit_rows: Iterable[Mapping[str, Any]],
) -> list[ProofObligationRecord]:
    """Build obligation rows without emitting theorem/contradiction claims."""
    records: list[ProofObligationRecord] = []
    for row in audit_rows:
        signature = _value(row, "signature")
        if not signature:
            continue
        levels = _levels(row)
        template = _value(row, "frey_template_id", "frey_template")
        primary = (
            f"For `{signature}`, verify that every primitive solution gives the `{template}` "
            "Frey object with the stated local hypotheses."
        )
        level = (
            f"Derive the exact conductor and justify any level-lowering route to `{levels}`; "
            "the current levels are route-audit data."
        )
        trace = (
            "Compare all survivor trace values against all relevant newform coefficients at small good primes, "
            "using exact equality first and modular comparison only when the representation prime is justified."
        )
        calibration = (
            "Confirm the route type remains clean on known calibration cases and remains separated from subgroup artifacts."
        )
        guardrail = (
            "This packet is a human-review checklist only; it does not certify a theorem, contradiction, or exclusion."
        )
        records.append(
            ProofObligationRecord(
                signature=signature,
                audit_review_label=_value(row, "audit_review_label", "modular_followup_candidate"),
                primary_obligation=primary,
                level_obligation=level,
                trace_obligation=trace,
                calibration_obligation=calibration,
                nonclaim_guardrail=guardrail,
                next_sage_command=f"sage runs/<run_id>/sage_jobs/sage_{signature.replace('-', '_')}.sage",
            )
        )
    records.sort(key=lambda item: (item.audit_review_label == "worth_human_modular_review", item.signature), reverse=True)
    return records


def proof_obligations_markdown(records: Iterable[ProofObligationRecord]) -> str:
    """Return Markdown checklist for modular-method review."""
    record_list = list(records)
    lines = [
        "# Modular Candidate Obligations",
        "",
        "These are human-review obligations for modular-route candidates. They are not theorem certificates.",
        "",
    ]
    if not record_list:
        lines.append("No modular follow-up candidates were available for deep audit.")
        lines.append("")
        return "\n".join(lines)
    for index, record in enumerate(record_list, start=1):
        lines.extend(
            [
                f"## {index}. `{record.signature}`",
                "",
                f"- Audit label: `{record.audit_review_label}`.",
                f"- Frey-object obligation: {record.primary_obligation}",
                f"- Level obligation: {record.level_obligation}",
                f"- Trace obligation: {record.trace_obligation}",
                f"- Calibration obligation: {record.calibration_obligation}",
                f"- Next Sage command: `{record.next_sage_command}`.",
                f"- Guardrail: {record.nonclaim_guardrail}",
                "",
            ]
        )
    return "\n".join(lines)

