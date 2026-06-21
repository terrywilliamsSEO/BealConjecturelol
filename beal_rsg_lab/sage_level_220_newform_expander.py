"""Generate a Sage script that exports level-220 newform coefficients."""

from __future__ import annotations

from pathlib import Path


def sage_level_220_newform_expander_text(*, good_prime_csv: Path, output_json: Path) -> str:
    """Return Sage code for exporting level-220 newform coefficients."""
    return f'''# Auto-generated Sage helper for the focused (5,4,5) audit.
# It exports q-expansion coefficients for level-220 newforms at selected good primes.
# This script is a data extractor only; it does not certify a theorem claim.

import builtins
import csv
import json
import os
import traceback

py_int = builtins.int
good_prime_csv = "{good_prime_csv.as_posix()}"
output_json = "{output_json.as_posix()}"


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


def _read_good_primes(path):
    primes = []
    with open(path, newline="") as handle:
        for row in csv.DictReader(handle):
            if str(row.get("selected", "")).lower() != "true":
                continue
            primes.append(py_int(row["prime"]))
    return primes


def _newforms_level_220():
    last_error = ""
    for kwargs in [{{"names": "a"}}, {{}}]:
        try:
            return Newforms(Gamma0(220), 2, **kwargs), ""
        except Exception as exc:
            last_error = str(exc)
    return [], last_error


payload = {{
    "signature": [5, 4, 5],
    "level": 220,
    "sage_status": "completed",
    "contradiction_claim_allowed": False,
    "good_primes": [],
    "newforms": [],
    "errors": [],
    "limitations": "coefficient extraction only; no proof claim",
}}

try:
    good_primes = _read_good_primes(good_prime_csv)
    payload["good_primes"] = good_primes
    forms, error = _newforms_level_220()
    if error:
        payload["sage_status"] = "partial"
        payload["errors"].append(error)
    for index, form in enumerate(forms):
        row = {{
            "newform_index": py_int(index),
            "label": "",
            "coefficient_field": "",
            "coefficients": {{}},
            "errors": [],
        }}
        try:
            row["label"] = str(form)
        except Exception as exc:
            row["errors"].append("label: " + str(exc))
        try:
            row["coefficient_field"] = str(form.base_ring())
        except Exception as exc:
            row["errors"].append("coefficient_field: " + str(exc))
        for prime in good_primes:
            try:
                try:
                    qexp = form.q_expansion(prime + 1)
                    coeff = qexp[prime]
                except Exception:
                    coeff = form[prime]
                row["coefficients"][str(prime)] = str(coeff)
            except Exception as exc:
                row["errors"].append("a_" + str(prime) + ": " + str(exc))
        payload["newforms"].append(row)
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


def write_sage_level_220_newform_expander(run_dir: Path) -> Path:
    """Write the level-220 coefficient expander into a run directory."""
    script_path = run_dir / "sage_level_220_newform_expander.sage"
    script_path.write_text(
        sage_level_220_newform_expander_text(
            good_prime_csv=run_dir / "good_prime_list_545.csv",
            output_json=run_dir / "level_220_newform_coefficients.json",
        ),
        encoding="utf-8",
    )
    return script_path

