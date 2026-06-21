"""Deterministic Sage smoke-job generation."""

from __future__ import annotations

from pathlib import Path


SMOKE_JOB_ID = "sage_smoke"


def sage_smoke_script_text(result_path: Path) -> str:
    """Return a tiny Sage script that writes importer-compatible JSON."""
    return f'''# Sage smoke job for beal_rsg_lab.
# Verifies Sage starts, basic elliptic curve point counts work, and JSON can be written.

import json
import builtins
import os
import traceback

py_int = builtins.int
result_path = "{result_path.as_posix()}"
payload = {{
    "job_id": "{SMOKE_JOB_ID}",
    "signature": [0, 0, 0],
    "route_label": "smoke_check",
    "source_run": "sage_smoke",
    "sage_status": "completed",
    "checked_levels": [],
    "newform_count": 0,
    "trace_match_status": "not_checked",
    "contradiction_claim_allowed": False,
    "followup_label": "sage_checked_inconclusive",
    "errors": [],
    "smoke": {{}},
}}


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


try:
    F = GF(5)
    curve = EllipticCurve(F, [0, 0, 0, 1, 1])
    payload["smoke"]["field_order"] = py_int(F.order())
    payload["smoke"]["curve_cardinality"] = py_int(curve.cardinality())
    payload["smoke"]["trace"] = py_int(F.order() + 1 - curve.cardinality())
    try:
        forms = Newforms(Gamma0(11), 2)
        payload["checked_levels"] = [py_int(11)]
        payload["newform_count"] = py_int(len(forms))
    except Exception as exc:
        payload["smoke"]["newforms_status"] = "unsupported"
        payload["smoke"]["newforms_error"] = str(exc)
except Exception:
    payload["sage_status"] = "failed"
    payload["followup_label"] = "needs_external_sage_check"
    payload["errors"].append(traceback.format_exc())

payload["contradiction_claim_allowed"] = False
os.makedirs(os.path.dirname(result_path), exist_ok=True)
safe_payload = _json_safe(payload)
with open(result_path, "w") as handle:
    json.dump(safe_payload, handle, indent=2, sort_keys=True)
    handle.write("\\n")
print(json.dumps(safe_payload, sort_keys=True))
'''


def write_sage_smoke_job(run_dir: Path) -> tuple[Path, Path]:
    """Write the smoke Sage job and return `(job_path, result_path)`."""
    job_dir = run_dir / "sage_jobs"
    result_dir = run_dir / "sage_results"
    job_dir.mkdir(parents=True, exist_ok=True)
    result_dir.mkdir(parents=True, exist_ok=True)
    job_path = job_dir / f"{SMOKE_JOB_ID}.sage"
    result_path = result_dir / f"{SMOKE_JOB_ID}.json"
    job_path.write_text(sage_smoke_script_text(result_path), encoding="utf-8")
    return job_path, result_path
