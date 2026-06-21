from __future__ import annotations

import csv
import json
from pathlib import Path
import tempfile
import unittest

from beal_rsg_lab.candidate_level_generator_545 import (
    SAFE_CANDIDATE_LEVEL_LABELS_545,
    build_candidate_levels_545,
)
from beal_rsg_lab.candidate_level_importer_545 import (
    SAFE_COEFFICIENT_FIELD_STATUS_545,
    CandidateLevelCoefficientRow545,
    CandidateLevelImportRecord545,
    import_candidate_level_newforms_545,
)
from beal_rsg_lab.focused_candidate_audit_545 import generate_focused_545_review
from beal_rsg_lab.frey_reduction_diagnostics_545 import build_frey_reduction_diagnostics_545
from beal_rsg_lab.frey_trace_possibility_545 import build_frey_trace_possibilities_545
from beal_rsg_lab.good_prime_selector import select_good_primes_545
from beal_rsg_lab.level_route_ranking_545 import (
    SAFE_LEVEL_ROUTE_LABELS_545,
    build_level_route_ranking_545,
)
from beal_rsg_lab.trace_filter_across_levels_545 import (
    SAFE_TRACE_FILTER_ACROSS_LEVELS_LABELS,
    build_trace_filter_across_levels_545,
)


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


class CandidateLevelDiscovery545Tests(unittest.TestCase):
    def test_level_generation_includes_220_and_without_11_variants(self) -> None:
        rows = build_candidate_levels_545()
        levels = {row.level for row in rows}
        self.assertEqual(len(rows), 24)
        self.assertIn(220, levels)
        self.assertTrue(any(not row.includes_11 for row in rows))
        self.assertIn(20, levels)
        labels = {row.conductor_plausibility_label for row in rows}
        self.assertTrue(labels <= SAFE_CANDIDATE_LEVEL_LABELS_545)
        self.assertTrue(labels.isdisjoint(FORBIDDEN_LABELS))

    def test_candidate_level_importer_missing_and_invalid_are_safe(self) -> None:
        candidates = build_candidate_levels_545()
        with tempfile.TemporaryDirectory() as temp_dir:
            missing_path = Path(temp_dir) / "missing.json"
            summary, coeffs = import_candidate_level_newforms_545(missing_path, candidates)
            self.assertEqual(len(summary), len(candidates))
            self.assertEqual(coeffs, [])
            self.assertTrue(all(row.import_status == "missing" for row in summary))
            self.assertTrue({row.coefficient_field_status for row in summary} <= SAFE_COEFFICIENT_FIELD_STATUS_545)
            bad_path = Path(temp_dir) / "bad.json"
            bad_path.write_text("{not json", encoding="utf-8")
            bad_summary, bad_coeffs = import_candidate_level_newforms_545(bad_path, candidates)
            self.assertEqual(bad_coeffs, [])
            self.assertTrue(all(not row.schema_valid for row in bad_summary))

    def test_candidate_level_importer_completed_partial_timeout_failed_statuses(self) -> None:
        candidates = [row for row in build_candidate_levels_545() if row.level in {20, 220}]
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            completed_payload = {
                "signature": [5, 4, 5],
                "weight": 2,
                "sage_status": "completed",
                "contradiction_claim_allowed": False,
                "levels": [
                    {
                        "level": 20,
                        "newform_count": 1,
                        "selected_good_primes": [3],
                        "level_status": "completed",
                        "errors": [],
                    }
                ],
                "coefficient_rows": [
                    {
                        "level": 20,
                        "weight": 2,
                        "newform_index": 0,
                        "newform_label": "f0",
                        "prime": 3,
                        "coefficient": "2",
                        "coefficient_field": "Rational Field",
                        "coefficient_field_kind": "rational_integer",
                        "is_rational_integer": True,
                        "reduction_mod_5_available": True,
                        "coefficient_mod_5": "2",
                        "prime_above_5_metadata": "",
                        "row_status": "completed",
                    }
                ],
            }
            completed_path = root / "completed.json"
            completed_path.write_text(json.dumps(completed_payload), encoding="utf-8")
            summary, coeffs = import_candidate_level_newforms_545(completed_path, candidates)
            by_level = {row.level: row for row in summary}
            self.assertEqual(by_level[20].import_status, "completed")
            self.assertEqual(by_level[20].coefficient_field_status, "all_clear")
            self.assertEqual(len(coeffs), 1)
            for status in ("partial", "timeout", "failed"):
                path = root / f"{status}.json"
                path.write_text(
                    json.dumps(
                        {
                            "signature": [5, 4, 5],
                            "weight": 2,
                            "sage_status": status,
                            "contradiction_claim_allowed": False,
                            "levels": [],
                            "coefficient_rows": [],
                        }
                    ),
                    encoding="utf-8",
                )
                rows, coefficient_rows = import_candidate_level_newforms_545(path, candidates)
                self.assertEqual(coefficient_rows, [])
                self.assertTrue(all(row.import_status == status for row in rows))

    def test_trace_filter_safe_labels_for_missing_data(self) -> None:
        candidates = build_candidate_levels_545()
        import_rows, coefficient_rows = import_candidate_level_newforms_545(Path("definitely_missing_candidate_level.json"), candidates)
        rows = build_trace_filter_across_levels_545(candidates, import_rows, coefficient_rows)
        labels = {row.level_trace_label for row in rows}
        self.assertEqual(labels, {"level_data_insufficient"})
        self.assertTrue(labels <= SAFE_TRACE_FILTER_ACROSS_LEVELS_LABELS)

    def test_synthetic_cross_level_ranking_detects_level_sensitivity(self) -> None:
        candidates = [row for row in build_candidate_levels_545() if row.level in {20, 220}]
        import_rows = [
            CandidateLevelImportRecord545(
                signature="5-4-5",
                level=20,
                weight=2,
                sage_status="completed",
                level_status="completed",
                schema_valid=True,
                newform_count=1,
                selected_good_primes="3",
                coefficient_row_count=1,
                rational_integer_coefficient_count=1,
                nonrational_coefficient_count=0,
                unclear_coefficient_count=0,
                coefficient_field_status="all_clear",
                import_status="completed",
                error_message="",
                source_path="synthetic",
                route_ceiling_label="worth_human_modular_review",
            ),
            CandidateLevelImportRecord545(
                signature="5-4-5",
                level=220,
                weight=2,
                sage_status="completed",
                level_status="completed",
                schema_valid=True,
                newform_count=1,
                selected_good_primes="3",
                coefficient_row_count=1,
                rational_integer_coefficient_count=1,
                nonrational_coefficient_count=0,
                unclear_coefficient_count=0,
                coefficient_field_status="all_clear",
                import_status="completed",
                error_message="",
                source_path="synthetic",
                route_ceiling_label="worth_human_modular_review",
            ),
        ]
        coefficient_rows = [
            CandidateLevelCoefficientRow545(
                signature="5-4-5",
                level=20,
                weight=2,
                newform_index=0,
                newform_label="f0",
                prime=3,
                coefficient="2",
                coefficient_field="Rational Field",
                coefficient_field_kind="rational_integer",
                is_rational_integer=True,
                reduction_mod_5_available=True,
                coefficient_mod_5="2",
                prime_above_5_metadata="",
                row_status="completed",
            ),
            CandidateLevelCoefficientRow545(
                signature="5-4-5",
                level=220,
                weight=2,
                newform_index=0,
                newform_label="f0",
                prime=3,
                coefficient="0",
                coefficient_field="Rational Field",
                coefficient_field_kind="rational_integer",
                is_rational_integer=True,
                reduction_mod_5_available=True,
                coefficient_mod_5="0",
                prime_above_5_metadata="",
                row_status="completed",
            ),
        ]
        good_primes = select_good_primes_545(level=220, bound=3, allow_residual_prime=False)
        frey_rows = build_frey_trace_possibilities_545(good_primes)
        diagnostic_rows = build_frey_reduction_diagnostics_545(good_primes)
        trace_rows = build_trace_filter_across_levels_545(
            candidates,
            import_rows,
            coefficient_rows,
            frey_rows,
            diagnostic_rows,
            target_primes=(3,),
        )
        by_level = {row.level: row for row in trace_rows}
        self.assertEqual(by_level[20].level_trace_label, "level_trace_mismatch_candidate")
        self.assertEqual(by_level[220].level_trace_label, "level_survivor_exists")
        ranking = build_level_route_ranking_545(candidates, trace_rows)
        self.assertEqual(ranking[0].aggregate_route_label, "level_sensitive_route")
        self.assertIn(ranking[0].aggregate_route_label, SAFE_LEVEL_ROUTE_LABELS_545)

    def test_focused_generation_writes_level_search_sidecars_and_keeps_calibration_clean(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir)
            _seed_minimal_focused_run(run_dir)
            artifacts = generate_focused_545_review(run_dir)
            for path_text in [
                artifacts.candidate_levels_path,
                artifacts.candidate_levels_report_path,
                artifacts.sage_candidate_level_expander_path,
                artifacts.candidate_level_import_summary_path,
                artifacts.candidate_level_coefficient_rows_path,
                artifacts.trace_filter_across_levels_path,
                artifacts.level_route_ranking_path,
                artifacts.level_route_ranking_report_path,
            ]:
                self.assertTrue(Path(path_text).exists(), path_text)
            focused = Path(artifacts.focused_report_path).read_text(encoding="utf-8")
            self.assertIn("Candidate Level Discovery", focused)
            self.assertIn("level_data_insufficient", focused)
            self.assertIn("Known-case mismatches: `0`", focused)
            self.assertIn("Known-case overpromotions: `0`", focused)


if __name__ == "__main__":
    unittest.main()
