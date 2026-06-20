# Generic Sage/newform probe template for beal_rsg_lab.
# Generated per-signature jobs in run directories contain concrete metadata.
# This template documents the JSON contract. It is not a theorem-certification script.

import json


def write_probe_result(path, payload):
    payload["contradiction_claim_allowed"] = False
    with open(path, "w") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def newform_count_for_level(level):
    row = {"level": int(level), "status": "not_checked", "newform_count": 0, "error": ""}
    try:
        forms = Newforms(Gamma0(level), 2)
        row["newform_count"] = int(len(forms))
        row["status"] = "completed"
    except Exception as exc:
        row["status"] = "unsupported"
        row["error"] = str(exc)
    return row


def trace_rows_for_signature(signature, primes):
    p, q, r = [ZZ(value) for value in signature]
    rows = []
    for ell in primes:
        F = GF(ell)
        Hp = sorted(set(F(a) ** p for a in range(1, ell)), key=lambda item: int(item))
        Hq = sorted(set(F(a) ** q for a in range(1, ell)), key=lambda item: int(item))
        Hr = set(F(a) ** r for a in range(1, ell))
        trace_counts = {}
        nonsingular = 0
        skipped = 0
        triples = 0
        for u in Hp:
            for v in Hq:
                if u + v not in Hr:
                    continue
                triples += 1
                if u == 0 or v == 0 or u + v == 0:
                    skipped += 1
                    continue
                curve = EllipticCurve(F, [0, v - u, 0, -u * v, 0])
                trace = ZZ(ell + 1 - curve.cardinality())
                trace_counts[str(trace)] = trace_counts.get(str(trace), 0) + 1
                nonsingular += 1
        rows.append(
            {
                "ell": int(ell),
                "survivor_triple_count": int(triples),
                "nonsingular_triple_count": int(nonsingular),
                "singular_skipped_count": int(skipped),
                "trace_counts": trace_counts,
                "trace_support_size": int(len(trace_counts)),
            }
        )
    return rows


print("Use generated files under <run-dir>/sage_jobs for concrete beal_rsg_lab jobs.")
