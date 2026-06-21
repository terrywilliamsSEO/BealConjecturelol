from __future__ import annotations

import csv
import json
from pathlib import Path
import tempfile
import unittest

from beal_rsg_lab.focused_candidate_audit_545 import generate_focused_545_review
from beal_rsg_lab.good_prime_selector import select_good_primes_545
from beal_rsg_lab.nonunit_elimination_545 import build_nonunit_eliminations_545
from beal_rsg_lab.nonunit_newform_filter_545 import (
    SAFE_NONUNIT_FILTER_LABELS,
    build_nonunit_newform_filters_545,
    local_case_decision_tree_545_markdown,
)
from beal_rsg_lab.singular_reduction_trace_545 import build_singular_reduction_traces_545
from beal_rsg_lab.trace_congruence_filter_545 import TraceCongruenceFilterRecord


FORBIDDEN_LABELS = {"proof", "proven", "solved", "contradiction", "disproof", "disproven"}
FOCUSED_PRIMES = {3, 13, 17, 41, 61}


def _filter_row(prime: int, newform_index: int, classification: str) -> TraceCongruenceFilterRecord:
    return TraceCongruenceFilterRecord(
        signature="5-4-5",
        level=220,
        prime=prime,
        newform_index=newform_index,
        newform_label=f"f{newform_index}",
        coefficient_field="Rational Field",
        coefficient_field_kind="rational_integer",
        frey_trace_values=(0,),
        newform_coefficient="1",
        coefficient_mod_5="1",
        prime_above_5_metadata="",
        comparison_mode="mod_5",
        filter_classification=classification,
        reason="synthetic route audit",
        contradiction_claim_allowed=False,
    )


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


class NonunitElimination545Tests(unittest.TestCase):
    def test_focused_primes_are_included_in_focused_nonunit_audit(self) -> None:
        good_rows = select_good_primes_545(level=220, bound=61)
        rows = build_nonunit_eliminations_545(good_rows)
        self.assertEqual({row.prime for row in rows}, FOCUSED_PRIMES)
        self.assertEqual({row.valuation_mask for row in rows}, {"A_only", "B_only", "C_only", "AB", "AC", "BC", "ABC"})

    def test_pairwise_masks_are_primitive_forbidden(self) -> None:
        good_rows = select_good_primes_545(level=220, bound=61)
        rows = build_nonunit_eliminations_545(good_rows)
        by_key = {(row.prime, row.valuation_mask): row for row in rows}
        for prime in FOCUSED_PRIMES:
            for mask in ("AB", "AC", "BC", "ABC"):
                self.assertTrue(by_key[(prime, mask)].primitive_forbidden)
                self.assertEqual(by_key[(prime, mask)].branch_label, "primitive_forbidden")

    def test_single_nonunit_branches_force_reduction_argument_label(self) -> None:
        good_rows = select_good_primes_545(level=220, bound=61)
        nonunit_rows = build_nonunit_eliminations_545(good_rows)
        reduction_rows = build_singular_reduction_traces_545(nonunit_rows)
        filter_rows = [
            _filter_row(13, 0, "eliminated"),
            _filter_row(13, 1, "survives"),
            _filter_row(17, 0, "survives"),
            _filter_row(17, 1, "eliminated"),
        ]
        decision_rows = build_nonunit_newform_filters_545(filter_rows, nonunit_rows, reduction_rows)
        self.assertEqual({row.prime for row in decision_rows}, FOCUSED_PRIMES)
        self.assertTrue(all(row.safe_label in SAFE_NONUNIT_FILTER_LABELS for row in decision_rows))
        self.assertTrue(all(row.safe_label == "reduction_argument_required" for row in decision_rows))
        self.assertTrue(all(not row.full_nonunit_resolution for row in decision_rows))
        self.assertTrue(all(row.safe_label != "local_case_elimination_candidate" for row in decision_rows))

    def test_singular_reduction_labels_are_safe(self) -> None:
        good_rows = select_good_primes_545(level=220, bound=61)
        nonunit_rows = build_nonunit_eliminations_545(good_rows)
        reduction_rows = build_singular_reduction_traces_545(nonunit_rows)
        labels = {row.frey_reduction_classification for row in reduction_rows}
        self.assertTrue(labels <= {"multiplicative", "additive", "potentially_good", "template_unknown", "needs_human_reduction_argument"})
        self.assertTrue(labels.isdisjoint(FORBIDDEN_LABELS))

    def test_decision_tree_keeps_local_coverage_gap(self) -> None:
        good_rows = select_good_primes_545(level=220, bound=61)
        nonunit_rows = build_nonunit_eliminations_545(good_rows)
        reduction_rows = build_singular_reduction_traces_545(nonunit_rows)
        filter_rows = [_filter_row(13, 0, "eliminated"), _filter_row(17, 1, "eliminated")]
        decision_rows = build_nonunit_newform_filters_545(filter_rows, nonunit_rows, reduction_rows)
        text = local_case_decision_tree_545_markdown(
            filter_rows=filter_rows,
            nonunit_rows=nonunit_rows,
            reduction_rows=reduction_rows,
            newform_filter_rows=decision_rows,
        )
        self.assertIn("q=13", text)
        self.assertIn("q=17", text)
        self.assertIn("q=41", text)
        self.assertIn("q=61", text)
        self.assertIn("local_coverage_gap", text)
        self.assertIn("unit_only_trace_mismatch_candidate", text)

    def test_focused_generation_writes_nonunit_sidecars_without_overpromotion(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)
            (run_dir / "sage_results").mkdir()
            (run_dir / "sage_results" / "sage_5_4_5.json").write_text(
                json.dumps(
                    {
                        "checked_levels": [220],
                        "contradiction_claim_allowed": False,
                        "newform_count": 2,
                        "sage_status": "completed",
                        "signature": [5, 4, 5],
                        "trace_match_status": "narrow",
                    }
                ),
                encoding="utf-8",
            )
            _write_csv(
                run_dir / "sage_known_case_calibration.csv",
                [
                    {
                        "signature": "5-4-5",
                        "post_sage_label": "modular_followup_candidate",
                        "overpromoted": "False",
                        "calibration_status": "calibrated",
                    }
                ],
            )
            artifacts = generate_focused_545_review(run_dir)
            self.assertTrue(Path(artifacts.nonunit_eliminations_path).exists())
            self.assertTrue(Path(artifacts.singular_reduction_traces_path).exists())
            self.assertTrue(Path(artifacts.nonunit_newform_filter_path).exists())
            self.assertTrue(Path(artifacts.local_case_decision_tree_path).exists())
            report = Path(artifacts.focused_report_path).read_text(encoding="utf-8")
            self.assertIn("Known-case mismatches: `0`", report)
            self.assertIn("Known-case overpromotions: `0`", report)
            self.assertIn("Focused Eliminating-Prime Nonunit Branch Audit", report)
            self.assertIn("local_coverage_gap", report)


if __name__ == "__main__":
    unittest.main()
