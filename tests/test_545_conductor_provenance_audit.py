from __future__ import annotations

import csv
import json
from pathlib import Path
import tempfile
import unittest

from beal_rsg_lab.abc_prime_removal_audit_545 import (
    SAFE_ABC_PRIME_REMOVAL_LABELS,
    build_abc_prime_removal_audit_545,
)
from beal_rsg_lab.bad_prime_tate_checklist_545 import build_bad_prime_tate_checklist_545
from beal_rsg_lab.conditional_route_validity_score_545 import (
    SAFE_CONDITIONAL_ROUTE_VALIDITY_LABELS,
    build_conditional_route_validity_score_545,
)
from beal_rsg_lab.conductor_exponent_model_545 import (
    SAFE_CONDUCTOR_EXPONENT_MODEL_LABELS,
    SAFE_REDUCTION_LABELS_545,
    build_conductor_exponent_model_545,
)
from beal_rsg_lab.conductor_support_audit_545 import build_conductor_support_audit_545
from beal_rsg_lab.focused_candidate_audit_545 import generate_focused_545_review
from beal_rsg_lab.frey_curve_derivation_545 import build_frey_curve_derivation_545
from beal_rsg_lab.level_220_audit import factorization_220
from beal_rsg_lab.level_220_provenance_545 import (
    SAFE_LEVEL_220_PROVENANCE_LABELS,
    build_level_220_provenance_545,
)
from beal_rsg_lab.level_lowering_obligation_545 import build_level_lowering_obligations_545


FORBIDDEN_LABELS = {"proof", "proven", "solved", "contradiction", "disproof", "disproven"}


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _seed_minimal_focused_run(run_dir: Path) -> None:
    (run_dir / "sage_results").mkdir()
    (run_dir / "sage_results" / "sage_5_4_5.json").write_text(
        json.dumps(
            {
                "checked_levels": [220],
                "contradiction_claim_allowed": False,
                "job_id": "sage_5_4_5",
                "newform_count": 2,
                "sage_status": "completed",
                "signature": [5, 4, 5],
                "trace_match_status": "narrow",
            }
        ),
        encoding="utf-8",
    )
    _write_csv(
        run_dir / "modular_candidate_deep_audit.csv",
        [{"signature": "5-4-5", "audit_review_label": "worth_human_modular_review", "priority": "7.25"}],
    )
    _write_csv(
        run_dir / "sage_known_case_calibration.csv",
        [{"signature": "5-4-5", "post_sage_label": "modular_followup_candidate", "overpromoted": "False"}],
    )


class ConductorProvenance545Tests(unittest.TestCase):
    def test_level_220_factorization_and_11_provenance_status(self) -> None:
        rows = build_level_220_provenance_545()
        by_factor = {row.factor: row for row in rows}
        self.assertEqual(factorization_220(), "2^2 * 5 * 11")
        self.assertEqual(by_factor["220"].factorization, "2^2 * 5 * 11")
        self.assertEqual(by_factor["220"].provenance_label, "level_220_heuristic_target")
        self.assertEqual(by_factor["11"].provenance_label, "level_11_factor_unjustified")
        labels = {row.provenance_label for row in rows}
        self.assertTrue(labels <= SAFE_LEVEL_220_PROVENANCE_LABELS)
        self.assertTrue(labels.isdisjoint(FORBIDDEN_LABELS))

    def test_conductor_exponent_valuation_schema_and_safe_uncertainty(self) -> None:
        rows = build_conductor_exponent_model_545()
        by_case = {row.prime_case: row for row in rows}
        self.assertEqual(set(by_case), {"ell_divides_A", "ell_divides_B", "ell_divides_C", "ell_equals_2", "ell_equals_5", "ell_equals_11"})
        self.assertEqual(by_case["ell_divides_A"].discriminant_valuation, "10*v_ell(A)")
        self.assertEqual(by_case["ell_divides_B"].discriminant_valuation, "8*v_ell(B)")
        self.assertEqual(by_case["ell_divides_C"].expected_reduction, "multiplicative")
        self.assertEqual(by_case["ell_equals_11"].audit_label, "needs_human_tate_check")
        self.assertTrue({row.expected_reduction for row in rows} <= SAFE_REDUCTION_LABELS_545)
        self.assertTrue({row.audit_label for row in rows} <= SAFE_CONDUCTOR_EXPONENT_MODEL_LABELS)

    def test_abc_prime_removal_gap_requires_irreducibility_and_minimality(self) -> None:
        rows = build_abc_prime_removal_audit_545()
        self.assertEqual({row.prime_case for row in rows}, {"ell_divides_A", "ell_divides_B", "ell_divides_C"})
        self.assertTrue(all(row.appears_in_discriminant for row in rows))
        self.assertTrue(all(row.residual_irreducibility_required for row in rows))
        self.assertTrue(all(row.minimality_required for row in rows))
        self.assertTrue(all(row.removal_label == "abc_prime_removal_gap" for row in rows))
        self.assertTrue({row.removal_label for row in rows} <= SAFE_ABC_PRIME_REMOVAL_LABELS)

    def test_route_score_keeps_ceiling_and_no_overpromotion(self) -> None:
        score = build_conditional_route_validity_score_545(
            [],
            build_frey_curve_derivation_545(),
            build_conductor_support_audit_545(),
            build_bad_prime_tate_checklist_545(),
            build_level_lowering_obligations_545(),
            build_conductor_exponent_model_545(),
            build_level_220_provenance_545(),
            build_abc_prime_removal_audit_545(),
        )[0]
        self.assertEqual(score.validity_label, "conductor_gap_blocks_upgrade")
        self.assertEqual(score.level_220_provenance_confidence, "level_220_heuristic_target")
        self.assertEqual(score.abc_prime_removal_confidence, "abc_prime_removal_gap")
        self.assertEqual(score.bad_prime_local_confidence, "bad_prime_tate_gap")
        self.assertIn(score.validity_label, SAFE_CONDITIONAL_ROUTE_VALIDITY_LABELS)
        self.assertNotIn(score.validity_label, FORBIDDEN_LABELS)
        self.assertEqual(score.route_ceiling_label, "worth_human_modular_review")

    def test_focused_generation_writes_provenance_sidecars(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)
            _seed_minimal_focused_run(run_dir)
            artifacts = generate_focused_545_review(run_dir)
            for path_text in [
                artifacts.conductor_exponent_model_path,
                artifacts.conductor_exponent_model_report_path,
                artifacts.level_220_provenance_path,
                artifacts.level_220_provenance_report_path,
                artifacts.abc_prime_removal_audit_path,
                artifacts.abc_prime_removal_audit_report_path,
                artifacts.sage_conductor_sanity_script_path,
                artifacts.sage_conductor_sanity_manifest_path,
            ]:
                self.assertTrue(Path(path_text).exists(), path_text)
            focused = Path(artifacts.focused_report_path).read_text(encoding="utf-8")
            self.assertIn("level_11_factor_unjustified", focused)
            self.assertIn("abc_prime_removal_gap", focused)
            self.assertIn("Level 220 remains a heuristic target", focused)
            self.assertIn("Known-case mismatches: `0`", focused)
            self.assertIn("Known-case overpromotions: `0`", focused)
            packet = Path(artifacts.conditional_theorem_packet_path).read_text(encoding="utf-8")
            self.assertIn("level_220_heuristic_target", packet)
            self.assertIn("ABC-prime removal status", packet)


if __name__ == "__main__":
    unittest.main()
