"""Generate Sage/newform follow-up jobs for external modular review."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from math import prod
from pathlib import Path
import shutil
from typing import Iterable, Protocol

from .frey_template_library import candidate_frey_template
from .number_theory import radical
from .rsg_residue_engine import Signature


SAGE_ROUTE_LABELS = {
    "needs_external_sage_check",
    "mixed_needs_external_check",
    "newform_check_candidate",
    "trace_rigid_candidate",
}


class SageCalibrationInput(Protocol):
    case_id: str
    signature: Signature
    signature_text: str
    expected_route: str
    actual_route_label: str
    collision_class: str
    collision_resolved_route_label: str
    strongest_prime: int
    strongest_system_signal: str
    notes: str


class SagePriorInput(Protocol):
    case_id: str
    signature: str
    output_label: str
    proof_route_priority: float
    discovery_readiness_score: float


class SageModularRouteInput(Protocol):
    signature: Signature
    canonical_signature_id: str
    ell: int
    route_classification: str
    route_rank_score: float
    promotion_status: str
    rationale: str


@dataclass(frozen=True)
class SageJobRecord:
    """Manifest row for one generated Sage/newform follow-up job."""

    job_id: str
    signature: str
    canonical_signature_id: str
    route_label: str
    source_run: str
    candidate_case_ids: tuple[str, ...]
    candidate_rows: tuple[str, ...]
    primes_involved: tuple[int, ...]
    candidate_levels: tuple[int, ...]
    frey_template_id: str
    frey_template_equation: str
    limitations: str
    job_path: str
    result_path: str
    batch_path: str
    sage_available: bool
    job_status: str
    command_hint: str

    def to_flat_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["candidate_case_ids"] = ";".join(self.candidate_case_ids)
        data["candidate_rows"] = ";".join(self.candidate_rows)
        data["primes_involved"] = ";".join(str(item) for item in self.primes_involved)
        data["candidate_levels"] = ";".join(str(item) for item in self.candidate_levels)
        return data


def _parse_signature_text(signature_text: str) -> Signature:
    parts = tuple(int(part) for part in signature_text.split("-"))
    if len(parts) != 3:
        raise ValueError(f"bad signature text {signature_text!r}")
    return parts  # type: ignore[return-value]


def _signature_text(signature: Signature) -> str:
    return "-".join(str(part) for part in signature)


def _job_id(signature: Signature) -> str:
    return "sage_" + "_".join(str(part) for part in signature)


def _canonical_signature_id(signature: Signature) -> str:
    p, q, r = signature
    left = tuple(sorted((p, q)))
    return f"{left[0]}-{left[1]}-{r}"


def _route_priority(label: str) -> int:
    priority = {
        "trace_rigid_candidate": 4,
        "newform_check_candidate": 3,
        "mixed_needs_external_check": 2,
        "needs_external_sage_check": 1,
    }
    return priority.get(label, 0)


def _best_route_label(labels: Iterable[str]) -> str:
    label_list = list(labels)
    if not label_list:
        return "needs_external_sage_check"
    return max(label_list, key=_route_priority)


def _candidate_levels(signature: Signature, primes_involved: Iterable[int]) -> tuple[int, ...]:
    """Return conservative conductor-like levels for Sage exploration.

    These are route-audit levels only. They are not asserted to be exact Frey
    conductors.
    """
    support = {2, *radical(signature)}
    support.update(prime for prime in primes_involved if prime > 1)
    base = prod(sorted(support))
    levels = {base, 2 * base, 4 * base}
    for prime in sorted(support):
        levels.add(base * prime)
    bounded = sorted(level for level in levels if 1 < level <= 5000)
    return tuple(bounded[:16])


def _metadata_json(
    *,
    job_id: str,
    signature: Signature,
    route_label: str,
    source_run: str,
    candidate_case_ids: tuple[str, ...],
    candidate_rows: tuple[str, ...],
    primes_involved: tuple[int, ...],
    candidate_levels: tuple[int, ...],
    frey_template_id: str,
    frey_template_equation: str,
    limitations: str,
    result_path: Path,
) -> str:
    payload = {
        "job_id": job_id,
        "signature": list(signature),
        "route_label": route_label,
        "source_run": source_run,
        "candidate_case_ids": list(candidate_case_ids),
        "candidate_rows": list(candidate_rows),
        "primes_involved": list(primes_involved),
        "candidate_levels": list(candidate_levels),
        "frey_template_id": frey_template_id,
        "frey_template_equation": frey_template_equation,
        "limitations": limitations,
        "result_path": result_path.as_posix(),
        "contradiction_claim_allowed": False,
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def sage_job_script_text(
    *,
    job_id: str,
    signature: Signature,
    route_label: str,
    source_run: str,
    candidate_case_ids: tuple[str, ...],
    candidate_rows: tuple[str, ...],
    primes_involved: tuple[int, ...],
    candidate_levels: tuple[int, ...],
    frey_template_id: str,
    frey_template_equation: str,
    limitations: str,
    result_path: Path,
) -> str:
    """Return a standalone Sage job that writes machine-readable JSON."""
    metadata = _metadata_json(
        job_id=job_id,
        signature=signature,
        route_label=route_label,
        source_run=source_run,
        candidate_case_ids=candidate_case_ids,
        candidate_rows=candidate_rows,
        primes_involved=primes_involved,
        candidate_levels=candidate_levels,
        frey_template_id=frey_template_id,
        frey_template_equation=frey_template_equation,
        limitations=limitations,
        result_path=result_path,
    )
    p, q, r = signature
    return f'''# Auto-generated Sage/newform follow-up job.
# This is a route-audit helper only. It cannot certify theorem claims.
# job_id: {job_id}
# signature: ({p}, {q}, {r})
# route_label: {route_label}
# source_run: {source_run}
# candidate_rows: {"; ".join(candidate_rows)}
# primes_involved: {", ".join(str(item) for item in primes_involved) or "none"}
# Frey template: {frey_template_id} - {frey_template_equation}
# limitations: {limitations}

import json
import builtins
import os
import traceback

JOB = {metadata}
py_int = builtins.int


def _json_safe(value):
    if isinstance(value, dict):
        return {{str(key): _json_safe(item) for key, item in value.items()}}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(item) for item in value]
    if value is None or isinstance(value, (str, bool, builtins.int, float)):
        return value
    try:
        json.dumps(value)
        return value
    except TypeError:
        try:
            return py_int(value)
        except Exception:
            return str(value)


def _power_image(F, ell, exponent):
    return sorted(set(F(a) ** exponent for a in range(1, ell)), key=lambda item: int(item))


def _trace_data_for_prime(ell, p, q, r):
    F = GF(ell)
    Hp = _power_image(F, ell, p)
    Hq = _power_image(F, ell, q)
    Hr = set(_power_image(F, ell, r))
    trace_counts = {{}}
    triple_count = 0
    nonsingular_count = 0
    singular_skipped = 0
    errors = []
    for u in Hp:
        for v in Hq:
            w = u + v
            if w not in Hr:
                continue
            triple_count += 1
            if u == 0 or v == 0 or u + v == 0:
                singular_skipped += 1
                continue
            try:
                curve = EllipticCurve(F, [0, v - u, 0, -u * v, 0])
                trace = ZZ(ell + 1 - curve.cardinality())
                trace_counts[str(trace)] = trace_counts.get(str(trace), 0) + 1
                nonsingular_count += 1
            except Exception as exc:
                singular_skipped += 1
                errors.append(str(exc))
    return {{
        "ell": int(ell),
        "survivor_triple_count": int(triple_count),
        "nonsingular_triple_count": int(nonsingular_count),
        "singular_skipped_count": int(singular_skipped),
        "trace_counts": trace_counts,
        "trace_support_size": int(len(trace_counts)),
        "errors": errors[:5],
    }}


def _newform_count_for_level(level):
    row = {{"level": int(level), "status": "not_checked", "newform_count": 0, "error": ""}}
    try:
        forms = Newforms(Gamma0(level), 2)
        row["newform_count"] = int(len(forms))
        row["status"] = "completed"
    except Exception as exc:
        row["status"] = "unsupported"
        row["error"] = str(exc)
    return row


def _trace_match_status(trace_rows, level_rows):
    supports = [row["trace_support_size"] for row in trace_rows if row["nonsingular_triple_count"] > 0]
    completed_levels = [row for row in level_rows if row["status"] == "completed"]
    total_newforms = sum(row["newform_count"] for row in completed_levels)
    if not trace_rows and not completed_levels:
        return "not_checked"
    if supports and max(supports) <= 1 and total_newforms <= 1:
        return "rigid"
    if supports and max(supports) <= 2 and total_newforms <= 2:
        return "narrow"
    return "inconclusive"


payload = {{
    "job_id": JOB["job_id"],
    "signature": JOB["signature"],
    "route_label": JOB["route_label"],
    "source_run": JOB["source_run"],
    "sage_status": "completed",
    "checked_levels": [],
    "newform_count": 0,
    "level_rows": [],
    "trace_rows": [],
    "trace_match_status": "not_checked",
    "contradiction_claim_allowed": False,
    "followup_label": "sage_checked_inconclusive",
    "errors": [],
    "metadata": JOB,
}}

try:
    p, q, r = [ZZ(value) for value in JOB["signature"]]
    for ell in JOB["primes_involved"]:
        if ell and ell > 2:
            payload["trace_rows"].append(_trace_data_for_prime(ZZ(ell), p, q, r))
    for level in JOB["candidate_levels"]:
        level_row = _newform_count_for_level(ZZ(level))
        payload["level_rows"].append(level_row)
        if level_row["status"] == "completed":
            payload["checked_levels"].append(int(level))
            payload["newform_count"] += int(level_row["newform_count"])
    payload["trace_match_status"] = _trace_match_status(payload["trace_rows"], payload["level_rows"])
    if payload["trace_match_status"] in ["rigid", "narrow"]:
        payload["followup_label"] = "modular_followup_candidate"
    elif payload["trace_match_status"] == "not_checked":
        payload["sage_status"] = "partial"
        payload["followup_label"] = "needs_external_sage_check"
    else:
        payload["followup_label"] = "sage_checked_inconclusive"
except Exception:
    payload["sage_status"] = "failed"
    payload["followup_label"] = "needs_external_sage_check"
    payload["errors"].append(traceback.format_exc())

payload["contradiction_claim_allowed"] = False
safe_payload = _json_safe(payload)
result_path = JOB["result_path"]
result_dir = os.path.dirname(result_path)
if result_dir:
    os.makedirs(result_dir, exist_ok=True)
with open(result_path, "w") as handle:
    json.dump(safe_payload, handle, indent=2, sort_keys=True)
    handle.write("\\n")
print(json.dumps(safe_payload, sort_keys=True))
'''


def _batch_script_text(job_paths: Iterable[Path]) -> str:
    lines = [
        "# Auto-generated Sage batch runner.",
        "# Loads each route-audit job. Outputs remain non-proof JSON evidence.",
        "",
    ]
    for path in job_paths:
        lines.append(f'load("{path.as_posix()}")')
    lines.append("")
    return "\n".join(lines)


def generate_sage_jobs(
    *,
    output_dir: Path,
    source_run: str,
    calibration_records: Iterable[SageCalibrationInput],
    route_prior_scores: Iterable[SagePriorInput],
    modular_route_classifications: Iterable[SageModularRouteInput] = (),
) -> list[SageJobRecord]:
    """Write Sage follow-up jobs and return manifest records."""
    score_by_case = {score.case_id: score for score in route_prior_scores}
    candidates: dict[Signature, dict[str, object]] = {}

    def ensure(signature: Signature) -> dict[str, object]:
        return candidates.setdefault(
            signature,
            {
                "labels": [],
                "case_ids": [],
                "rows": [],
                "primes": set(),
            },
        )

    for record in calibration_records:
        score = score_by_case.get(record.case_id)
        labels = {
            record.actual_route_label,
            record.collision_class,
            record.collision_resolved_route_label,
        }
        if score is not None:
            labels.add(score.output_label)
        if not (labels & SAGE_ROUTE_LABELS):
            continue
        entry = ensure(record.signature)
        label = _best_route_label(labels & SAGE_ROUTE_LABELS)
        entry["labels"].append(label)
        entry["case_ids"].append(record.case_id)
        entry["rows"].append(
            f"known_case:{record.case_id}:{label}:prime={int(record.strongest_prime or 0)}"
        )
        if int(record.strongest_prime or 0) > 2:
            entry["primes"].add(int(record.strongest_prime))

    for route in modular_route_classifications:
        if route.route_classification not in SAGE_ROUTE_LABELS:
            continue
        entry = ensure(route.signature)
        entry["labels"].append(route.route_classification)
        entry["rows"].append(
            f"modular_row:{route.route_classification}:ell={route.ell}:score={route.route_rank_score}"
        )
        if route.ell > 2:
            entry["primes"].add(route.ell)

    job_dir = output_dir / "sage_jobs"
    result_dir = output_dir / "sage_results"
    job_dir.mkdir(parents=True, exist_ok=True)
    result_dir.mkdir(parents=True, exist_ok=True)
    batch_path = job_dir / "run_all_sage_jobs.sage"
    sage_available = shutil.which("sage") is not None
    limitations = (
        "route-audit only; conductor levels are heuristic; Frey template needs "
        "independent validation; contradiction_claim_allowed is false"
    )
    records: list[SageJobRecord] = []
    job_paths: list[Path] = []

    for signature, entry in sorted(candidates.items(), key=lambda item: _signature_text(item[0])):
        labels = tuple(str(label) for label in entry["labels"])
        route_label = _best_route_label(labels)
        case_ids = tuple(sorted(set(str(case_id) for case_id in entry["case_ids"])))
        rows = tuple(sorted(set(str(row) for row in entry["rows"])))
        primes = tuple(sorted(int(prime) for prime in entry["primes"]))
        if not primes:
            primes = (5,)
        levels = _candidate_levels(signature, primes)
        template = candidate_frey_template(signature)
        job_id = _job_id(signature)
        job_path = job_dir / f"{job_id}.sage"
        result_path = result_dir / f"{job_id}.json"
        job_path.write_text(
            sage_job_script_text(
                job_id=job_id,
                signature=signature,
                route_label=route_label,
                source_run=source_run,
                candidate_case_ids=case_ids,
                candidate_rows=rows,
                primes_involved=primes,
                candidate_levels=levels,
                frey_template_id=template.template_id,
                frey_template_equation=template.equation,
                limitations=limitations,
                result_path=result_path,
            ),
            encoding="utf-8",
        )
        job_paths.append(job_path)
        records.append(
            SageJobRecord(
                job_id=job_id,
                signature=_signature_text(signature),
                canonical_signature_id=_canonical_signature_id(signature),
                route_label=route_label,
                source_run=source_run,
                candidate_case_ids=case_ids,
                candidate_rows=rows,
                primes_involved=primes,
                candidate_levels=levels,
                frey_template_id=template.template_id,
                frey_template_equation=template.equation,
                limitations=limitations,
                job_path=job_path.as_posix(),
                result_path=result_path.as_posix(),
                batch_path=batch_path.as_posix(),
                sage_available=sage_available,
                job_status="job_written_sage_available" if sage_available else "job_written_sage_unavailable",
                command_hint=f"sage {job_path.as_posix()}",
            )
        )

    batch_path.write_text(_batch_script_text(job_paths), encoding="utf-8")
    return records
