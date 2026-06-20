"""Generate human-review dossiers for queued modular-route signatures."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Mapping, Any

from .signature_normalizer import normalize_signature


@dataclass(frozen=True)
class CandidateDossierRecord:
    """Manifest row for a generated candidate dossier."""

    signature: str
    canonical_signature_id: str
    current_route_label: str
    sage_status: str
    dossier_path: str
    recommended_next_check: str

    def to_flat_dict(self) -> dict[str, object]:
        return asdict(self)


def _value(row: Mapping[str, Any], key: str, default: str = "") -> str:
    value = row.get(key, default)
    return "" if value is None else str(value)


def _parse_signature(signature: str) -> tuple[int, int, int]:
    parts = tuple(int(part) for part in signature.replace(",", "-").split("-") if part)
    if len(parts) != 3:
        raise ValueError(f"bad signature {signature!r}")
    return parts  # type: ignore[return-value]


def _split_semicolon(value: str) -> list[str]:
    return [part for part in value.split(";") if part]


def _by_signature(rows: Iterable[Mapping[str, Any]], key: str = "signature") -> dict[str, list[Mapping[str, Any]]]:
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for row in rows:
        signature = _value(row, key)
        if signature:
            grouped.setdefault(signature, []).append(row)
    return grouped


def _first_by_signature(rows: Iterable[Mapping[str, Any]], key: str = "signature") -> dict[str, Mapping[str, Any]]:
    grouped: dict[str, Mapping[str, Any]] = {}
    for row in rows:
        signature = _value(row, key)
        if signature and signature not in grouped:
            grouped[signature] = row
    return grouped


def _recommended_next_check(route_label: str, sage_status: str, trace_status: str) -> str:
    if sage_status in {"unavailable", "partial", "failed"}:
        return "Run the generated Sage job through native Sage, WSL, Docker, or CI and import the JSON result."
    if route_label == "modular_followup_candidate" or trace_status in {"rigid", "narrow", "candidate_match"}:
        return "Have a human verify the Frey model, exact conductor, irreducibility conditions, and newform trace comparison."
    if route_label == "sage_checked_inconclusive":
        return "Refine conductor candidates and compare against validated Frey templates before escalating."
    if route_label == "artifact_like":
        return "Treat as an artifact control unless independent non-artifact modular evidence appears."
    return "Keep as a low-priority route until stronger non-artifact evidence appears."


def _artifact_notes(known_row: Mapping[str, Any] | None, unit_rows: list[Mapping[str, Any]]) -> str:
    notes: list[str] = []
    if known_row is not None:
        notes.append(
            f"collision={_value(known_row, 'collision_class', 'none')}; "
            f"artifact_rows={_value(known_row, 'artifact_rows', '0')}; "
            f"sparse_unit_rows={_value(known_row, 'sparse_unit_rows', '0')}"
        )
    artifact_ells = [
        _value(row, "ell")
        for row in unit_rows
        if _value(row, "artifact_verdict") == "artifact_explained"
    ]
    if artifact_ells:
        notes.append("artifact-prone local primes: " + ", ".join(sorted(set(artifact_ells))))
    return "; ".join(notes) if notes else "No artifact row was attached in the current run data."


def _sparse_unit_summary(unit_rows: list[Mapping[str, Any]]) -> str:
    if not unit_rows:
        return "No sparse unit rows were attached to this dossier."
    parts = []
    for row in unit_rows[:8]:
        ell = _value(row, "ell")
        verdict = _value(row, "artifact_verdict", "unknown")
        survivor_count = _value(row, "geometry_survivor_count", _value(row, "survivor_count", ""))
        parts.append(f"`ell={ell}` {verdict} survivors={survivor_count or 'unknown'}")
    return "; ".join(parts)


def _trace_summary(import_row: Mapping[str, Any] | None) -> str:
    if import_row is None:
        return "No Sage import row is available."
    status = _value(import_row, "sage_status")
    summary = (
        f"sage_status={_value(import_row, 'sage_status')}; "
        f"trace_match_status={_value(import_row, 'trace_match_status')}; "
        f"newform_count={_value(import_row, 'newform_count')}; "
        f"checked_levels={_value(import_row, 'checked_levels') or 'none'}"
    )
    if status != "completed":
        error = _value(import_row, "error_message") or _value(import_row, "raw_summary")
        if error:
            summary += f"; failure_or_timeout_reason={error}"
    return summary


def _dossier_text(
    *,
    signature: str,
    job_row: Mapping[str, Any],
    import_row: Mapping[str, Any] | None,
    confidence_row: Mapping[str, Any] | None,
    known_row: Mapping[str, Any] | None,
    unit_rows: list[Mapping[str, Any]],
) -> tuple[str, CandidateDossierRecord]:
    parsed = _parse_signature(signature)
    normalized = normalize_signature(parsed)
    route_label = (
        _value(confidence_row, "updated_followup_label")
        if confidence_row is not None
        else _value(job_row, "route_label", "needs_external_sage_check")
    )
    sage_status = _value(import_row, "sage_status", "not_imported") if import_row is not None else "not_imported"
    trace_status = _value(import_row, "trace_match_status", "not_checked") if import_row is not None else "not_checked"
    recommended = _recommended_next_check(route_label, sage_status, trace_status)
    known_status = _value(known_row, "known_status_label", "not_in_known_case_library") if known_row else "not_in_known_case_library"
    terrain = _value(known_row, "terrain_label", "unclassified") if known_row else "unclassified"
    theorem_route = _value(known_row, "theorem_route_label", "") if known_row else ""
    frey_confidence = _value(known_row, "average_template_confidence", "unknown") if known_row else "unknown"
    padic_status = (
        f"padic_descent_rows={_value(known_row, 'padic_descent_rows', '0')}; "
        f"unit_lift_rigid_or_collapsed_rows={_value(known_row, 'unit_lift_rigid_or_collapsed_rows', '0')}"
        if known_row
        else "No p-adic lift status was attached."
    )
    proof_gap = (
        "This is not a proof: the Frey template is symbolic, conductor levels are heuristic, "
        "Sage output is route evidence only, and `contradiction_claim_allowed` remains false."
    )
    candidate_rows = _split_semicolon(_value(job_row, "candidate_rows"))
    case_ids = _split_semicolon(_value(job_row, "candidate_case_ids"))
    lines = [
        f"# Candidate Dossier: `{signature}`",
        "",
        "## Route Snapshot",
        "",
        f"- Signature: `({signature.replace('-', ',')})`.",
        f"- Canonical signature: `{normalized.canonical_signature_id}`.",
        f"- Current route label: `{route_label}`.",
        f"- Sage status: `{sage_status}`.",
        f"- Known-case status: `{known_status}`.",
        f"- Terrain classification: `{terrain}`.",
        f"- Terrain route: `{theorem_route or 'none'}`.",
        "",
        "## Evidence",
        "",
        f"- Artifact-risk notes: { _artifact_notes(known_row, unit_rows) }.",
        f"- Sparse unit rows involved: { _sparse_unit_summary(unit_rows) }.",
        f"- p-adic lift status: {padic_status}.",
        f"- Frey template confidence: `{frey_confidence}`.",
        f"- Sage job path: `{_value(job_row, 'job_path')}`.",
        f"- Sage result path: `{_value(job_row, 'result_path')}`.",
        f"- Trace/newform summary: {_trace_summary(import_row)}.",
        "",
        "## Candidate Rows",
        "",
    ]
    if candidate_rows:
        for item in candidate_rows:
            lines.append(f"- `{item}`")
    else:
        lines.append("- No candidate rows were attached.")
    lines.extend(
        [
            "",
            "## Known-Case Links",
            "",
            f"- Candidate case IDs: `{';'.join(case_ids) or 'none'}`.",
            "",
            "## Why This Is Not A Proof",
            "",
            proof_gap,
            "",
            "## Recommended Next Mathematical Check",
            "",
            recommended,
            "",
        ]
    )
    record = CandidateDossierRecord(
        signature=signature,
        canonical_signature_id=normalized.canonical_signature_id,
        current_route_label=route_label,
        sage_status=sage_status,
        dossier_path="",
        recommended_next_check=recommended,
    )
    return "\n".join(lines), record


def generate_candidate_dossiers(
    *,
    run_dir: Path,
    dossier_dir: Path,
    job_rows: list[Mapping[str, Any]],
    import_rows: list[Mapping[str, Any]],
    confidence_rows: list[Mapping[str, Any]],
    known_case_rows: list[Mapping[str, Any]],
    unit_rows: list[Mapping[str, Any]] | None = None,
) -> tuple[list[CandidateDossierRecord], str]:
    """Write queued-signature dossiers and return manifest rows plus index text."""
    del run_dir
    dossier_dir.mkdir(parents=True, exist_ok=True)
    import_by_signature = _first_by_signature(import_rows)
    confidence_by_signature = _first_by_signature(confidence_rows)
    known_by_signature = _first_by_signature(known_case_rows)
    units_by_signature = _by_signature(unit_rows or [])
    records: list[CandidateDossierRecord] = []

    for job_row in sorted(job_rows, key=lambda row: _value(row, "signature")):
        signature = _value(job_row, "signature")
        if not signature:
            continue
        text, record = _dossier_text(
            signature=signature,
            job_row=job_row,
            import_row=import_by_signature.get(signature),
            confidence_row=confidence_by_signature.get(signature),
            known_row=known_by_signature.get(signature),
            unit_rows=units_by_signature.get(signature, []),
        )
        path = dossier_dir / f"{signature}.md"
        path.write_text(text, encoding="utf-8")
        records.append(
            CandidateDossierRecord(
                signature=record.signature,
                canonical_signature_id=record.canonical_signature_id,
                current_route_label=record.current_route_label,
                sage_status=record.sage_status,
                dossier_path=path.as_posix(),
                recommended_next_check=record.recommended_next_check,
            )
        )

    index_lines = [
        "# Candidate Dossier Index",
        "",
        "These dossiers summarize queued Sage/newform follow-up signatures. They are research-route notes, not theorem claims.",
        "",
        "| signature | canonical | route label | Sage status | dossier |",
        "| --- | --- | --- | --- | --- |",
    ]
    for record in records:
        name = Path(record.dossier_path).name
        index_lines.append(
            f"| `{record.signature}` | `{record.canonical_signature_id}` | `{record.current_route_label}` | "
            f"`{record.sage_status}` | [{name}]({name}) |"
        )
    index_lines.append("")
    index_text = "\n".join(index_lines)
    (dossier_dir / "candidate_dossier_index.md").write_text(index_text, encoding="utf-8")
    return records, index_text
