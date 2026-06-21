"""Generate Sage code for candidate-level newform coefficient extraction."""

from __future__ import annotations

import csv
from pathlib import Path
from types import SimpleNamespace

from .candidate_level_generator_545 import build_candidate_levels_545


FOCUSED_TRACE_PRIMES_545 = (3, 13, 17, 41, 61)


def sage_candidate_level_expander_545_text(*, candidate_level_csv: Path, output_json: Path) -> str:
    """Return Sage code that expands newform coefficients across candidate levels."""
    primes = ", ".join(str(prime) for prime in FOCUSED_TRACE_PRIMES_545)
    return f'''# Auto-generated Sage helper for focused (5,4,5) candidate-level discovery.
# It extracts weight-2 newform coefficients for candidate comparison levels.
# This script is a data extractor only; it does not certify a theorem claim.

import builtins
import csv
import json
import os
import traceback

py_int = builtins.int
candidate_level_csv = "{candidate_level_csv.as_posix()}"
output_json = "{output_json.as_posix()}"
focused_primes = [{primes}]


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


def _read_candidate_levels(path):
    rows = []
    with open(path, newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append(row)
    return rows


def _field_metadata(coeff):
    field = coeff.parent()
    text = str(field)
    kind = "unknown"
    defining = ""
    if field == QQ or field == ZZ:
        kind = "rational_integer"
    else:
        kind = "number_field"
        try:
            defining = str(field.defining_polynomial())
        except Exception:
            defining = ""
    return text, kind, defining


def _integer_coeff_mod_5(coeff):
    try:
        return True, str(py_int(coeff) % 5)
    except Exception:
        return False, ""


def _number_field_mod_5_reductions(coeff):
    rows = []
    field = coeff.parent()
    try:
        primes_above = field.primes_above(5)
    except Exception:
        return rows
    for ideal in primes_above:
        try:
            residue_field, residue_map = field.residue_field(ideal, names="r")
            reduced = residue_map(coeff)
            rows.append({{
                "prime_above_5": str(ideal),
                "residue_field": str(residue_field),
                "coefficient_mod_5": str(reduced),
            }})
        except Exception as exc:
            rows.append({{"prime_above_5": str(ideal), "error": str(exc)}})
    return rows


payload = {{
    "signature": [5, 4, 5],
    "weight": 2,
    "sage_status": "completed",
    "contradiction_claim_allowed": False,
    "focused_primes": focused_primes,
    "levels": [],
    "coefficient_rows": [],
    "errors": [],
    "limitations": "candidate-level coefficient extraction only; no theorem claim",
}}

try:
    candidate_rows = _read_candidate_levels(candidate_level_csv)
    for candidate in candidate_rows:
        level = py_int(candidate.get("level", 0))
        level_row = {{
            "level": level,
            "factorization": candidate.get("factorization", ""),
            "conductor_plausibility_label": candidate.get("conductor_plausibility_label", ""),
            "newform_count": 0,
            "selected_good_primes": [p for p in focused_primes if level % p != 0],
            "level_status": "completed",
            "errors": [],
        }}
        try:
            try:
                forms = Newforms(Gamma0(level), 2, names="a")
            except Exception:
                forms = Newforms(Gamma0(level), 2)
            level_row["newform_count"] = py_int(len(forms))
            for index, form in enumerate(forms):
                label = ""
                try:
                    label = str(form)
                except Exception as exc:
                    level_row["errors"].append("label: " + str(exc))
                for prime in level_row["selected_good_primes"]:
                    coeff_row = {{
                        "level": level,
                        "weight": 2,
                        "newform_index": py_int(index),
                        "newform_label": label,
                        "prime": py_int(prime),
                        "coefficient": "",
                        "coefficient_field": "",
                        "coefficient_field_kind": "",
                        "defining_polynomial": "",
                        "is_rational_integer": False,
                        "reduction_mod_5_available": False,
                        "coefficient_mod_5": "",
                        "prime_above_5_metadata": "",
                        "row_status": "not_checked",
                        "error": "",
                    }}
                    try:
                        try:
                            qexp = form.q_expansion(prime + 1)
                            coeff = qexp[prime]
                        except Exception:
                            coeff = form[prime]
                        field_text, field_kind, defining = _field_metadata(coeff)
                        coeff_row["coefficient"] = str(coeff)
                        coeff_row["coefficient_field"] = field_text
                        coeff_row["coefficient_field_kind"] = field_kind
                        coeff_row["defining_polynomial"] = defining
                        integer_ok, coeff_mod_5 = _integer_coeff_mod_5(coeff)
                        coeff_row["is_rational_integer"] = integer_ok
                        if integer_ok:
                            coeff_row["reduction_mod_5_available"] = True
                            coeff_row["coefficient_mod_5"] = coeff_mod_5
                        elif field_kind == "number_field":
                            reductions = _number_field_mod_5_reductions(coeff)
                            coeff_row["prime_above_5_metadata"] = json.dumps(_json_safe(reductions), sort_keys=True)
                            successful = [item for item in reductions if "coefficient_mod_5" in item]
                            if successful:
                                coeff_row["reduction_mod_5_available"] = True
                                coeff_row["coefficient_mod_5"] = ";".join(str(item.get("coefficient_mod_5", "")) for item in successful)
                        coeff_row["row_status"] = "completed" if coeff_row["reduction_mod_5_available"] or coeff_row["is_rational_integer"] else "coefficient_field_unclear"
                    except Exception as exc:
                        coeff_row["row_status"] = "unsupported"
                        coeff_row["error"] = str(exc)
                        level_row["errors"].append("a_" + str(prime) + ": " + str(exc))
                    payload["coefficient_rows"].append(coeff_row)
        except Exception:
            level_row["level_status"] = "failed"
            level_row["errors"].append(traceback.format_exc())
            payload["sage_status"] = "partial"
        if level_row["errors"] and level_row["level_status"] == "completed":
            level_row["level_status"] = "partial"
            payload["sage_status"] = "partial"
        payload["levels"].append(level_row)
except Exception:
    payload["sage_status"] = "failed"
    payload["errors"].append(traceback.format_exc())

payload["contradiction_claim_allowed"] = False
safe_payload = _json_safe(payload)
os.makedirs(os.path.dirname(output_json), exist_ok=True)
with open(output_json, "w") as handle:
    json.dump(safe_payload, handle, indent=2, sort_keys=True)
    handle.write("\\n")
print(json.dumps(safe_payload, sort_keys=True))
'''


def write_sage_candidate_level_expander_545(run_dir: Path) -> Path:
    """Write `sage_candidate_level_expander_545.sage` into a run directory."""
    script_path = run_dir / "sage_candidate_level_expander_545.sage"
    script_path.write_text(
        sage_candidate_level_expander_545_text(
            candidate_level_csv=run_dir / "candidate_levels_545.csv",
            output_json=run_dir / "candidate_level_newforms_545.json",
        ),
        encoding="utf-8",
    )
    return script_path


def write_candidate_levels_for_sage_545(run_dir: Path) -> Path:
    """Write `candidate_levels_545.csv` for the Sage candidate-level expander."""
    rows = [row.to_flat_dict() for row in build_candidate_levels_545()]
    path = run_dir / "candidate_levels_545.csv"
    if not rows:
        path.write_text("", encoding="utf-8")
        return path
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def prepare_candidate_level_expander_job_545(run_dir: Path):
    """Create the candidate-level Sage job and return a runner-compatible object."""
    write_candidate_levels_for_sage_545(run_dir)
    script_path = write_sage_candidate_level_expander_545(run_dir)
    result_path = run_dir / "candidate_level_newforms_545.json"
    return SimpleNamespace(
        job_id="candidate_level_newforms_545",
        signature="5-4-5",
        route_label="candidate_level_discovery",
        job_path=script_path.as_posix(),
        result_path=result_path.as_posix(),
    )
