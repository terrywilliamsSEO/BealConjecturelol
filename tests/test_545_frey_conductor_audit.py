from __future__ import annotations

import csv
import json
from pathlib import Path
import tempfile
import unittest

from beal_rsg_lab.bad_prime_tate_checklist_545 import (
    SAFE_BAD_PRIME_TATE_LABELS,
    build_bad_prime_tate_checklist_545,
)
from beal_rsg_lab.conditional_route_validity_score_545 import (
    SAFE_CONDITIONAL_ROUTE_VALIDITY_LABELS,
    build_conditional_route_validity_score_545,
)
from beal_rsg_lab.conductor_support_audit_545 import (
    SAFE_CONDUCTOR_SUPPORT_LABELS,
    build_conductor_support_audit_545,
)
from beal_rsg_lab.focused_candidate_audit_545 import generate_focused_545_review
from beal_rsg_lab.frey_curve_derivation_545 import (
    SAFE_FREY_DERIVATION_LABELS,
    build_frey_curve_derivation_545,
)
from beal_rsg_lab.frey_reduction_diagnostics_545 import build_frey_reduction_diagnostics_545
from beal_rsg_lab.good_prime_selector import select_good_primes_545
from beal_rsg_lab.level_lowering_obligation_545 import (
    SAFE_LEVEL_LOWERING_STATUS_LABELS,
    build_level_lowering_obligations_545,
)
from beal_rsg_lab.multiplicative_reduction_congruence_545 import (
    build_multiplicative_reduction_congruences_545,
)
from beal_rsg_lab.newform_coefficient_importer import NewformCoefficientRow
from beal_rsg_lab.nonunit_elimination_545 import build_nonunit_eliminations_545
from beal_rsg_lab.quantifier_safety_audit_545 import build_quantifier_safety_audit_545
from beal_rsg_lab.cross_prime_branch_compatibility_545 import build_cross_prime_branch_compatibility_545
from beal_rsg_lab.trace_congruence_filter_545 import TraceCongruenceFilterRecord


FORBIDDEN_LABELS = {"proof", "proven", "solved", "contradiction", "disproof", "disproven"}


def _coefficient(prime: int, newform_index: int, coefficient: str) -> NewformCoefficientRow:
    return NewformCoefficientRow(
        signature="5-4-5",
        level=220,
        weight=2,
        newform_index=newform_index,
        newform_label=f"f{newform_index}",
        prime=prime,
        coefficient=coefficient,
        coefficient_field="Rational Field",
        coefficient_field_kind="rational_integer",
        is_rational_integer=True,
        reduction_mod_5_available=True,
        coefficient_mod_5=str(int(coefficient) % 5),
        prime_above_5_metadata="",
        row_status="completed",
    )


def _coefficient_rows() -> list[NewformCoefficientRow]:
    return [
        _coefficient(3, 0, "-2"),
        _coefficient(3, 1, "2"),
        _coefficient(13, 0, "-4"),
        _coefficient(13, 1, "0"),
        _coefficient(17, 0, "0"),
        _coefficient(17, 1, "-4"),
        _coefficient(41, 0, "6"),
        _coefficient(41, 1, "-10"),
        _coefficient(61, 0, "2"),
        _coefficient(61, 1, "-14"),
    ]


def _filter_row(prime: int, newform_index: int, classification: str, coefficient: str = "0") -> TraceCongruenceFilterRecord:
    return TraceCongruenceFilterRecord(
        signature="5-4-5",
        level=220,
        prime=prime,
        newform_index=newform_index,
        newform_label=f"f{newform_index}",
        coefficient_field="Rational Field",
        coefficient_field_kind="rational_integer",
        frey_trace_values=(0,),
        newform_coefficient=coefficient,
        coefficient_mod_5=str(int(coefficient) % 5) if coefficient.lstrip("-").isdigit() else "",
        prime_above_5_metadata="",
        comparison_mode="mod_5",
        filter_classification=classification,
        reason="synthetic conductor-audit row",
        contradiction_claim_allowed=False,
    )


def _unit_rows() -> list[TraceCongruenceFilterRecord]:
    return [
        _filter_row(3, 0, "eliminated", "-2"),
        _filter_row(3, 1, "eliminated", "2"),
        _filter_row(13, 0, "survives", "-4"),
        _filter_row(13, 1, "eliminated", "0"),
        _filter_row(17, 0, "eliminated", "0"),
        _filter_row(17, 1, "survives", "-4"),
        _filter_row(41, 0, "eliminated", "6"),
        _filter_row(41, 1, "survives", "-10"),
        _filter_row(61, 0, "eliminated", "2"),
        _filter_row(61, 1, "survives", "-14"),
    ]


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


def _quantifier_rows():
    diagnostics = build_frey_reduction_diagnostics_545()
    multiplicative = build_multiplicative_reduction_congruences_545(_coefficient_rows(), diagnostics, newform_count=2)
    nonunit = build_nonunit_eliminations_545(select_good_primes_545(level=220, bound=61))
    cross = build_cross_prime_branch_compatibility_545(_unit_rows(), multiplicative, nonunit, newform_count=2)
    return build_quantifier_safety_audit_545(_unit_rows(), multiplicative, nonunit, cross, newform_count=2)


class FreyConductorAudit545Tests(unittest.TestCase):
    def test_symbolic_invariant_output_schema(self) -> None:
        rows = build_frey_curve_derivation_545()
        by_component = {row.component: row for row in rows}
        self.assertEqual(set(by_component), {"curve_equation", "c4", "c6", "discriminant", "j_invariant"})
        self.assertIn("16*(A^10 + A^5*B^4 + B^8)", by_component["c4"].computed_formula)
        self.assertIn("32*(A^5 - B^4)", by_component["c6"].computed_formula)
        self.assertEqual(by_component["discriminant"].computed_formula, "16*A^10*B^8*C^10")
        labels = {row.audit_label for row in rows}
        self.assertTrue(labels <= SAFE_FREY_DERIVATION_LABELS)
        self.assertTrue(labels.isdisjoint(FORBIDDEN_LABELS))

    def test_level_220_factor_support_and_conductor_rows(self) -> None:
        rows = build_conductor_support_audit_545()
        by_symbol = {row.prime_or_symbol: row for row in rows}
        self.assertEqual(by_symbol["2"].candidate_level_exponent, "2")
        self.assertEqual(by_symbol["5"].candidate_level_exponent, "1")
        self.assertEqual(by_symbol["11"].candidate_level_exponent, "1")
        self.assertEqual(by_symbol["11"].audit_label, "conductor_support_gap")
        self.assertEqual(by_symbol["p | A"].expected_level_behavior, "expected_lowered_away_if_level_lowering_hypotheses_hold")
        labels = {row.audit_label for row in rows}
        self.assertTrue(labels <= SAFE_CONDUCTOR_SUPPORT_LABELS)
        self.assertTrue(labels.isdisjoint(FORBIDDEN_LABELS))

    def test_bad_prime_checklist_and_level_lowering_generation(self) -> None:
        bad_rows = build_bad_prime_tate_checklist_545()
        self.assertEqual({row.prime for row in bad_rows}, {2, 5, 11})
        self.assertTrue(all(row.audit_label == "blocks_conductor_claim" for row in bad_rows))
        self.assertTrue({row.audit_label for row in bad_rows} <= SAFE_BAD_PRIME_TATE_LABELS)
        level_rows = build_level_lowering_obligations_545()
        self.assertIn("Exact target level 220", {row.obligation_name for row in level_rows})
        self.assertIn("Residual representation irreducible", {row.obligation_name for row in level_rows})
        self.assertTrue({row.current_status for row in level_rows} <= SAFE_LEVEL_LOWERING_STATUS_LABELS)
        self.assertTrue(all(row.route_ceiling_label == "worth_human_modular_review" for row in level_rows))

    def test_conditional_route_validity_score_is_safe_and_not_overpromoted(self) -> None:
        frey_rows = build_frey_curve_derivation_545()
        conductor_rows = build_conductor_support_audit_545()
        bad_rows = build_bad_prime_tate_checklist_545()
        level_rows = build_level_lowering_obligations_545()
        score = build_conditional_route_validity_score_545(
            _quantifier_rows(),
            frey_rows,
            conductor_rows,
            bad_rows,
            level_rows,
        )[0]
        self.assertEqual(score.validity_label, "conductor_gap_blocks_upgrade")
        self.assertIn(score.validity_label, SAFE_CONDITIONAL_ROUTE_VALIDITY_LABELS)
        self.assertNotIn(score.validity_label, FORBIDDEN_LABELS)
        self.assertEqual(score.route_ceiling_label, "worth_human_modular_review")

    def test_focused_generation_writes_frey_conductor_sidecars_and_keeps_calibration_clean(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)
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
            (run_dir / "level_220_newform_coefficients.json").write_text(
                json.dumps(
                    {
                        "signature": [5, 4, 5],
                        "level": 220,
                        "weight": 2,
                        "sage_status": "completed",
                        "selected_good_primes": [3, 13, 17, 41, 61],
                        "newform_count": 2,
                        "coefficient_rows": [row.to_flat_dict() for row in _coefficient_rows()],
                        "contradiction_claim_allowed": False,
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
            artifacts = generate_focused_545_review(run_dir)
            for path_text in [
                artifacts.frey_curve_derivation_path,
                artifacts.frey_curve_derivation_report_path,
                artifacts.conductor_support_audit_path,
                artifacts.conductor_support_audit_report_path,
                artifacts.bad_prime_tate_checklist_path,
                artifacts.bad_prime_tate_checklist_report_path,
                artifacts.level_lowering_obligations_path,
                artifacts.level_lowering_obligations_report_path,
                artifacts.conditional_route_validity_score_path,
                artifacts.conditional_route_validity_score_report_path,
            ]:
                self.assertTrue(Path(path_text).exists(), path_text)
            focused = Path(artifacts.focused_report_path).read_text(encoding="utf-8")
            self.assertIn("Frey-Conductor Proof Audit", focused)
            self.assertIn("Known-case mismatches: `0`", focused)
            self.assertIn("Known-case overpromotions: `0`", focused)
            packet = Path(artifacts.conditional_theorem_packet_path).read_text(encoding="utf-8")
            self.assertIn("Exact Theorem A Human Must Prove", packet)
            self.assertIn("conductor_gap_blocks_upgrade", packet)


if __name__ == "__main__":
    unittest.main()
