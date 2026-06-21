from __future__ import annotations

import csv
import json
from pathlib import Path
import tempfile
import unittest

from beal_rsg_lab.assumption_dependency_graph_545 import build_assumption_dependency_graph_545
from beal_rsg_lab.cross_prime_branch_compatibility_545 import (
    CrossPrimeBranchCompatibilityRecord,
    build_cross_prime_branch_compatibility_545,
)
from beal_rsg_lab.focused_candidate_audit_545 import generate_focused_545_review
from beal_rsg_lab.frey_reduction_diagnostics_545 import build_frey_reduction_diagnostics_545
from beal_rsg_lab.good_prime_selector import select_good_primes_545
from beal_rsg_lab.multiplicative_reduction_congruence_545 import (
    build_multiplicative_reduction_congruences_545,
)
from beal_rsg_lab.newform_coefficient_importer import NewformCoefficientRow
from beal_rsg_lab.nonunit_elimination_545 import build_nonunit_eliminations_545
from beal_rsg_lab.quantifier_safety_audit_545 import (
    SAFE_QUANTIFIER_SAFETY_LABELS,
    build_quantifier_safety_audit_545,
)
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
        reason="synthetic quantifier-safety row",
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


def _audit_inputs(
    *,
    coefficient_rows: list[NewformCoefficientRow] | None = None,
    unit_rows: list[TraceCongruenceFilterRecord] | None = None,
):
    coefficients = coefficient_rows if coefficient_rows is not None else _coefficient_rows()
    filters = unit_rows if unit_rows is not None else _unit_rows()
    diagnostics = build_frey_reduction_diagnostics_545()
    multiplicative = build_multiplicative_reduction_congruences_545(
        coefficients,
        diagnostics,
        newform_count=2,
    )
    nonunit = build_nonunit_eliminations_545(select_good_primes_545(level=220, bound=61))
    cross = build_cross_prime_branch_compatibility_545(filters, multiplicative, nonunit, newform_count=2)
    quantifier = build_quantifier_safety_audit_545(
        filters,
        multiplicative,
        nonunit,
        cross,
        newform_count=2,
    )
    return filters, multiplicative, nonunit, cross, quantifier


def _cross_claim(index: int) -> CrossPrimeBranchCompatibilityRecord:
    return CrossPrimeBranchCompatibilityRecord(
        signature="5-4-5",
        prime_set="13;17;41;61",
        newform_index=index,
        newform_label=f"f{index}",
        allowed_branch_sets="synthetic_invalid_fixed_branch_claim",
        eliminated_at_primes="",
        pairwise_primitive_forbidden_status="all_pairwise_primitive_forbidden",
        compatible_prime_count=0,
        incompatible_prime_count=4,
        data_gap_count=0,
        level_lowering_assumption_required_count=0,
        compatible_branch_assignment_exists=False,
        compatibility_label="cross_prime_elimination_candidate",
        route_ceiling_label="worth_human_modular_review",
        reason="synthetic cross-prime elimination claim",
    )


class QuantifierSafetyAudit545Tests(unittest.TestCase):
    def test_valid_exists_prime_per_newform_elimination(self) -> None:
        _, _, _, _, rows = _audit_inputs()
        by_index = {row.newform_index: row for row in rows}
        self.assertEqual(by_index[0].quantifier_classification, "valid_exists_prime_elimination")
        self.assertEqual(by_index[0].eliminated_primes, "17;41")
        self.assertEqual(by_index[1].quantifier_classification, "valid_exists_prime_elimination")
        self.assertEqual(by_index[1].eliminated_primes, "13")
        self.assertEqual(by_index[-1].quantifier_classification, "quantifier_safe_cross_prime_candidate")
        self.assertFalse(by_index[-1].fixed_branch_dependency_detected)

    def test_invalid_fixed_branch_dependency_detection(self) -> None:
        survivor_units = [
            _filter_row(13, 0, "survives", "-4"),
            _filter_row(13, 1, "survives", "0"),
            _filter_row(17, 0, "survives", "0"),
            _filter_row(17, 1, "survives", "-4"),
            _filter_row(41, 0, "survives", "6"),
            _filter_row(41, 1, "survives", "-10"),
            _filter_row(61, 0, "eliminated", "2"),
            _filter_row(61, 1, "survives", "-14"),
        ]
        filters, multiplicative, nonunit, _, _ = _audit_inputs(unit_rows=survivor_units)
        rows = build_quantifier_safety_audit_545(
            filters,
            multiplicative,
            nonunit,
            [_cross_claim(0), _cross_claim(1)],
            newform_count=2,
        )
        by_index = {row.newform_index: row for row in rows}
        self.assertEqual(by_index[0].quantifier_classification, "invalid_cross_prime_branch_dependency")
        self.assertTrue(by_index[0].fixed_branch_dependency_detected)
        self.assertEqual(by_index[-1].quantifier_classification, "invalid_cross_prime_branch_dependency")

    def test_complete_branch_coverage_required_per_eliminating_prime(self) -> None:
        diagnostics = build_frey_reduction_diagnostics_545(target_primes=(17,))
        multiplicative = build_multiplicative_reduction_congruences_545(
            [_coefficient(17, 0, "0")],
            diagnostics,
            newform_count=1,
            target_primes=(17,),
        )
        missing_c_only = [row for row in multiplicative if row.valuation_mask != "C_only"]
        rows = build_quantifier_safety_audit_545(
            [_filter_row(17, 0, "eliminated", "0")],
            missing_c_only,
            build_nonunit_eliminations_545(select_good_primes_545(level=220, bound=17)),
            [_cross_claim(0)],
            newform_count=1,
            target_primes=(17,),
        )
        by_index = {row.newform_index: row for row in rows}
        self.assertEqual(by_index[0].quantifier_classification, "data_insufficient")
        self.assertEqual(by_index[0].eliminated_primes, "")

    def test_safe_labels_and_dependency_graph_do_not_overpromote(self) -> None:
        _, _, _, _, rows = _audit_inputs()
        labels = {row.quantifier_classification for row in rows}
        self.assertTrue(labels <= SAFE_QUANTIFIER_SAFETY_LABELS)
        self.assertTrue(labels.isdisjoint(FORBIDDEN_LABELS))
        self.assertTrue(all(row.route_ceiling_label == "worth_human_modular_review" for row in rows))
        dependency_rows = build_assumption_dependency_graph_545(rows)
        dependency_statuses = {row.current_status for row in dependency_rows}
        self.assertIn("quantifier_safe_cross_prime_candidate", dependency_statuses)
        self.assertTrue(all(row.route_ceiling_label == "worth_human_modular_review" for row in dependency_rows))
        self.assertTrue(dependency_statuses.isdisjoint(FORBIDDEN_LABELS))

    def test_focused_generation_writes_quantifier_packet_sidecars(self) -> None:
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
            self.assertTrue(Path(artifacts.quantifier_safety_audit_path).exists())
            self.assertTrue(Path(artifacts.quantifier_safety_audit_report_path).exists())
            self.assertTrue(Path(artifacts.conditional_theorem_packet_path).exists())
            self.assertTrue(Path(artifacts.assumption_dependency_graph_path).exists())
            self.assertTrue(Path(artifacts.assumption_dependency_graph_report_path).exists())
            self.assertTrue(Path(artifacts.adversarial_review_checklist_path).exists())
            with Path(artifacts.quantifier_safety_audit_path).open(newline="", encoding="utf-8") as handle:
                quantifier_rows = list(csv.DictReader(handle))
            aggregate = next(row for row in quantifier_rows if row["newform_index"] == "-1")
            self.assertEqual(aggregate["quantifier_classification"], "quantifier_safe_cross_prime_candidate")
            focused = Path(artifacts.focused_report_path).read_text(encoding="utf-8")
            self.assertIn("Quantifier Safety Audit", focused)
            self.assertIn("Conditional Theorem Packet", focused)
            self.assertIn("Assumption Dependency Graph", focused)
            packet = Path(artifacts.conditional_theorem_packet_path).read_text(encoding="utf-8")
            self.assertIn("newform 0 as eliminated at q=17 and q=41", packet)
            self.assertIn("worth_human_modular_review", packet)


if __name__ == "__main__":
    unittest.main()
