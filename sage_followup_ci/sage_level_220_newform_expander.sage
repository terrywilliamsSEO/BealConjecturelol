# Auto-generated Sage helper for the focused (5,4,5) audit.
# It exports q-expansion coefficients for level-220 newforms at selected good primes.
# This script is a data extractor only; it does not certify a theorem claim.

import builtins
import csv
import json
import os
import traceback

py_int = builtins.int
good_prime_csv = "runs/sage_followup_ci/good_prime_list_545.csv"
output_json = "runs/sage_followup_ci/level_220_newform_coefficients.json"


def _json_safe(value):
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
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
    for kwargs in [{"names": "a"}, {}]:
        try:
            return Newforms(Gamma0(220), 2, **kwargs), ""
        except Exception as exc:
            last_error = str(exc)
    return [], last_error


payload = {
    "signature": [5, 4, 5],
    "level": 220,
    "weight": 2,
    "sage_status": "completed",
    "contradiction_claim_allowed": False,
    "selected_good_primes": [],
    "newform_count": 0,
    "newforms": [],
    "coefficient_rows": [],
    "errors": [],
    "limitations": "coefficient extraction only; no proof claim",
}


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
        return True, str(py_int(coeff) % 5), ""
    except Exception:
        return False, "", ""


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
            rows.append({
                "prime_above_5": str(ideal),
                "residue_field": str(residue_field),
                "coefficient_mod_5": str(reduced),
            })
        except Exception as exc:
            rows.append({
                "prime_above_5": str(ideal),
                "error": str(exc),
            })
    return rows

try:
    good_primes = _read_good_primes(good_prime_csv)
    payload["selected_good_primes"] = good_primes
    forms, error = _newforms_level_220()
    if error:
        payload["sage_status"] = "partial"
        payload["errors"].append(error)
    payload["newform_count"] = py_int(len(forms))
    for index, form in enumerate(forms):
        row = {
            "newform_index": py_int(index),
            "label": "",
            "coefficient_field": "",
            "coefficient_field_kind": "",
            "defining_polynomial": "",
            "coefficients": {},
            "errors": [],
        }
        try:
            row["label"] = str(form)
        except Exception as exc:
            row["errors"].append("label: " + str(exc))
        try:
            row["coefficient_field"] = str(form.base_ring())
        except Exception as exc:
            row["errors"].append("coefficient_field: " + str(exc))
        for prime in good_primes:
            coeff_row = {
                "level": 220,
                "weight": 2,
                "newform_index": py_int(index),
                "newform_label": row["label"],
                "prime": py_int(prime),
                "coefficient": "",
                "coefficient_field": row["coefficient_field"],
                "coefficient_field_kind": "",
                "defining_polynomial": "",
                "is_rational_integer": False,
                "reduction_mod_5_available": False,
                "coefficient_mod_5": "",
                "prime_above_5_metadata": "",
                "row_status": "not_checked",
                "error": "",
            }
            try:
                try:
                    qexp = form.q_expansion(prime + 1)
                    coeff = qexp[prime]
                except Exception:
                    coeff = form[prime]
                field_text, field_kind, defining = _field_metadata(coeff)
                row["coefficient_field"] = field_text
                row["coefficient_field_kind"] = field_kind
                row["defining_polynomial"] = defining
                row["coefficients"][str(prime)] = str(coeff)
                coeff_row["coefficient"] = str(coeff)
                coeff_row["coefficient_field"] = field_text
                coeff_row["coefficient_field_kind"] = field_kind
                coeff_row["defining_polynomial"] = defining
                integer_ok, coeff_mod_5, _ = _integer_coeff_mod_5(coeff)
                coeff_row["is_rational_integer"] = integer_ok
                if integer_ok:
                    coeff_row["reduction_mod_5_available"] = True
                    coeff_row["coefficient_mod_5"] = coeff_mod_5
                elif field_kind == "number_field":
                    reductions = _number_field_mod_5_reductions(coeff)
                    successful_reductions = [item for item in reductions if "coefficient_mod_5" in item]
                    coeff_row["prime_above_5_metadata"] = json.dumps(_json_safe(reductions), sort_keys=True)
                    if successful_reductions:
                        coeff_row["reduction_mod_5_available"] = True
                        coeff_row["coefficient_mod_5"] = ";".join(
                            str(item.get("coefficient_mod_5", "")) for item in successful_reductions
                        )
                    else:
                        coeff_row["row_status"] = "coefficient_field_unclear"
                coeff_row["row_status"] = (
                    "completed"
                    if coeff_row["reduction_mod_5_available"] or coeff_row["is_rational_integer"]
                    else "coefficient_field_unclear"
                )
            except Exception as exc:
                row["errors"].append("a_" + str(prime) + ": " + str(exc))
                coeff_row["row_status"] = "unsupported"
                coeff_row["error"] = str(exc)
            payload["coefficient_rows"].append(coeff_row)
        payload["newforms"].append(row)
except Exception:
    payload["sage_status"] = "failed"
    payload["errors"].append(traceback.format_exc())

payload["contradiction_claim_allowed"] = False
safe_payload = _json_safe(payload)
os.makedirs(os.path.dirname(output_json), exist_ok=True)
with open(output_json, "w") as handle:
    json.dump(safe_payload, handle, indent=2, sort_keys=True)
    handle.write("\n")
print(json.dumps(safe_payload, sort_keys=True))
