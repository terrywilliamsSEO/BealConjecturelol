"""Deep-audit records for modular follow-up candidates."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from .frey_template_library import candidate_frey_template
from .signature_normalizer import normalize_signature


@dataclass(frozen=True)
class ModularCandidateAuditRecord:
    """Structured human-review packet for one modular follow-up candidate."""

    signature: str
    normalized_signature: str
    equation_form: str
    route_label: str
    audit_review_label: str
    priority: float
    sage_status: str
    checked_levels: tuple[int, ...]
    candidate_levels: tuple[int, ...]
    newform_count: int
    trace_status: str
    frey_template_id: str
    frey_template_equation: str
    template_confidence: float
    terrain_classification: str
    artifact_risk_notes: str
    padic_lift_status: str
    local_sparse_rows_involved: str
    control_comparison_summary: str
    exact_reason_not_a_theorem: str
    recommended_next_mathematical_check: str
    obligation_explicit: bool
    known_case_clean: bool

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["checked_levels"] = ";".join(str(level) for level in self.checked_levels)
        data["candidate_levels"] = ";".join(str(level) for level in self.candidate_levels)
        return data


def _value(row: Mapping[str, Any] | None, key: str, default: str = "") -> str:
    if row is None:
        return default
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


def _first_by_signature(rows: Iterable[Mapping[str, Any]], key: str = "signature") -> dict[str, Mapping[str, Any]]:
    output: dict[str, Mapping[str, Any]] = {}
    for row in rows:
        signature = _value(row, key)
        if signature and signature not in output:
            output[signature] = row
    return output


def _by_signature(rows: Iterable[Mapping[str, Any]], key: str = "signature") -> dict[str, list[Mapping[str, Any]]]:
    output: dict[str, list[Mapping[str, Any]]] = {}
    for row in rows:
        signature = _value(row, key)
        if signature:
            output.setdefault(signature, []).append(row)
    return output


def _load_payload(job_row: Mapping[str, Any], results_dir: Path | None = None) -> dict[str, Any]:
    path = Path(_value(job_row, "result_path"))
    if results_dir is not None:
        path = results_dir / f"{_value(job_row, 'job_id')}.json"
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def _artifact_notes(known_row: Mapping[str, Any] | None, unit_rows: list[Mapping[str, Any]]) -> str:
    artifact_rows = int(_value(known_row, "artifact_rows", "0") or 0)
    sparse_rows = int(_value(known_row, "sparse_unit_rows", "0") or 0)
    notes = [
        f"known_case_artifact_rows={artifact_rows}",
        f"known_case_sparse_unit_rows={sparse_rows}",
        f"collision={_value(known_row, 'collision_class', 'none')}",
    ]
    artifact_ells = sorted({_value(row, "ell") for row in unit_rows if _value(row, "artifact_verdict") == "artifact_explained"})
    if artifact_ells:
        notes.append("artifact_prone_ells=" + ",".join(artifact_ells))
    if artifact_rows and sparse_rows and artifact_rows >= sparse_rows:
        notes.append("artifact risk is material; do not promote from local sparsity")
    return "; ".join(notes)


def _local_sparse_rows(unit_rows: list[Mapping[str, Any]]) -> str:
    if not unit_rows:
        return "No unit-survivor rows attached."
    parts: list[str] = []
    for row in unit_rows[:8]:
        parts.append(
            "ell={ell}:verdict={verdict}:survivors={survivors}".format(
                ell=_value(row, "ell"),
                verdict=_value(row, "artifact_verdict", "unknown"),
                survivors=_value(row, "geometry_survivor_count", "unknown"),
            )
        )
    return "; ".join(parts)


def _control_summary(unit_rows: list[Mapping[str, Any]]) -> str:
    if not unit_rows:
        return "No same-size unit controls attached to this signature."
    parts: list[str] = []
    for row in unit_rows[:6]:
        parts.append(
            "ell={ell}:same_size_explained={explained}:density_gap={gap}".format(
                ell=_value(row, "ell"),
                explained=_value(row, "artifact_same_size_explained", "unknown"),
                gap=_value(row, "artifact_residual_density_gap", "unknown"),
            )
        )
    return "; ".join(parts)


def _payload_trace_summary(payload: Mapping[str, Any]) -> str:
    trace_rows = payload.get("trace_rows", [])
    if not isinstance(trace_rows, list) or not trace_rows:
        return "No trace rows were imported."
    parts = []
    for row in trace_rows:
        if not isinstance(row, dict):
            continue
        parts.append(
            "ell={ell}:support={support}:nonsingular={count}".format(
                ell=row.get("ell", ""),
                support=row.get("trace_support_size", ""),
                count=row.get("nonsingular_triple_count", ""),
            )
        )
    return "; ".join(parts) if parts else "Trace rows were malformed or empty."


def _review_label(
    *,
    sage_status: str,
    trace_status: str,
    checked_levels: tuple[int, ...],
    newform_count: int,
    known_case_clean: bool,
    obligation_explicit: bool,
) -> str:
    if (
        sage_status == "completed"
        and trace_status in {"narrow", "rigid", "candidate_match"}
        and checked_levels
        and newform_count <= 2
        and known_case_clean
        and obligation_explicit
    ):
        return "worth_human_modular_review"
    if sage_status == "completed" and trace_status in {"narrow", "rigid", "candidate_match"}:
        return "modular_followup_candidate"
    return "needs_more_external_data"


def build_modular_candidate_deep_audits(
    *,
    job_rows: Iterable[Mapping[str, Any]],
    import_rows: Iterable[Mapping[str, Any]],
    confidence_rows: Iterable[Mapping[str, Any]],
    known_case_rows: Iterable[Mapping[str, Any]],
    unit_rows: Iterable[Mapping[str, Any]],
    results_dir: Path | None = None,
) -> list[ModularCandidateAuditRecord]:
    """Build deep-audit records for signatures labeled modular_followup_candidate."""
    jobs_by_signature = _first_by_signature(job_rows)
    imports_by_signature = _first_by_signature(import_rows)
    known_by_signature = _first_by_signature(known_case_rows)
    units_by_signature = _by_signature(unit_rows)
    rows: list[ModularCandidateAuditRecord] = []
    for confidence in confidence_rows:
        if _value(confidence, "updated_followup_label") != "modular_followup_candidate":
            continue
        signature = _value(confidence, "signature")
        if not signature:
            continue
        parsed = _parse_signature(signature)
        normalized = normalize_signature(parsed)
        template = candidate_frey_template(parsed)
        job = jobs_by_signature.get(signature, {})
        imported = imports_by_signature.get(signature, {})
        known = known_by_signature.get(signature)
        unit_list = units_by_signature.get(signature, [])
        payload = _load_payload(job, results_dir=results_dir)
        checked_levels = _split_ints(_value(imported, "checked_levels"))
        candidate_levels = _split_ints(_value(job, "candidate_levels"))
        newform_count = int(_value(imported, "newform_count", "0") or 0)
        sage_status = _value(imported, "sage_status", "missing")
        trace_status = _value(imported, "trace_match_status", "not_checked")
        obligation = (
            f"Verify the Frey object for `{signature}`, compute the exact conductor, "
            f"establish the needed level-lowering hypotheses, then compare survivor traces "
            f"({_payload_trace_summary(payload)}) against all newforms at the checked or candidate levels."
        )
        known_case_clean = _value(known, "actual_route_label") != "known_case_mismatch"
        overpromotion_clean = True
        review_label = _review_label(
            sage_status=sage_status,
            trace_status=trace_status,
            checked_levels=checked_levels,
            newform_count=newform_count,
            known_case_clean=known_case_clean and overpromotion_clean,
            obligation_explicit=bool(obligation),
        )
        rows.append(
            ModularCandidateAuditRecord(
                signature=signature,
                normalized_signature=normalized.canonical_signature_id,
                equation_form=f"A^{parsed[0]} + B^{parsed[1]} = C^{parsed[2]}",
                route_label=_value(confidence, "updated_followup_label"),
                audit_review_label=review_label,
                priority=float(_value(confidence, "human_review_priority", "0") or 0.0),
                sage_status=sage_status,
                checked_levels=checked_levels,
                candidate_levels=candidate_levels,
                newform_count=newform_count,
                trace_status=trace_status,
                frey_template_id=template.template_id,
                frey_template_equation=template.equation,
                template_confidence=template.template_confidence,
                terrain_classification=_value(known, "terrain_label", "unclassified"),
                artifact_risk_notes=_artifact_notes(known, unit_list),
                padic_lift_status=(
                    f"padic_descent_rows={_value(known, 'padic_descent_rows', '0')}; "
                    f"unit_lift_rigid_or_collapsed_rows={_value(known, 'unit_lift_rigid_or_collapsed_rows', '0')}"
                ),
                local_sparse_rows_involved=_local_sparse_rows(unit_list),
                control_comparison_summary=_control_summary(unit_list),
                exact_reason_not_a_theorem=(
                    "The Frey template, conductor level, irreducibility, level-lowering, and "
                    "newform-trace exclusion steps still require independent mathematical verification; "
                    "contradiction_claim_allowed is false."
                ),
                recommended_next_mathematical_check=obligation,
                obligation_explicit=bool(obligation),
                known_case_clean=known_case_clean,
            )
        )
    rows.sort(key=lambda row: (row.audit_review_label == "worth_human_modular_review", row.priority), reverse=True)
    return rows


def modular_candidate_audit_report_markdown(
    *,
    output_dir: Path,
    audit_rows: Iterable[ModularCandidateAuditRecord],
    timeout_count: int,
) -> str:
    """Return a Markdown report for modular candidate deep audit."""
    rows = list(audit_rows)
    review_count = sum(1 for row in rows if row.audit_review_label == "worth_human_modular_review")
    lines = [
        "# Modular Candidate Deep Audit",
        "",
        f"Output directory: `{output_dir.as_posix()}`",
        "",
        "This report ranks modular-method review packets. It does not certify theorem claims.",
        "",
        f"- Deep-audited modular candidates: `{len(rows)}`.",
        f"- Worth human modular review: `{review_count}`.",
        f"- Timed-out Sage jobs queued for retry: `{timeout_count}`.",
        "",
        "| rank | signature | audit label | Sage | trace | levels | newforms | priority |",
        "| ---: | --- | --- | --- | --- | --- | ---: | ---: |",
    ]
    if not rows:
        lines.append("| 0 | none | none | none | none | none | 0 | 0 |")
    for index, row in enumerate(rows, start=1):
        levels = ";".join(str(level) for level in row.checked_levels) or "none"
        lines.append(
            f"| {index} | `{row.signature}` | `{row.audit_review_label}` | `{row.sage_status}` | "
            f"`{row.trace_status}` | `{levels}` | {row.newform_count} | {row.priority} |"
        )
    lines.extend(
        [
            "",
            "## Guardrails",
            "",
            "- Local sparsity alone is not used as promotion evidence.",
            "- Candidate levels remain symbolic until conductor and minimal-model work is checked externally.",
            "- Every row keeps `contradiction_claim_allowed=false` in the Sage import layer.",
            "",
        ]
    )
    return "\n".join(lines)

