"""
test/test_phase7_evaluation.py - Unit & Benchmark Tests for Phase 7 Evaluation Suite.

Validates:
1. Levenshtein edit distance and Character Error Rate (CER) calculations.
2. FieldMetric precision, recall, F1, exact match accuracy, and error tracking.
3. SafetyMetrics: False Acceptance Rate (FAR) and False Rejection Rate (FRR).
4. EvaluationReport serialization to dict and Markdown table output.
5. End-to-end BenchmarkRunner execution across clean and ambiguous fixtures.
6. Zero-tolerance safety: 0.0% FAR on corrupted land record parcels and 100% Rule 5 compliance.
"""

import sys
import json
from pathlib import Path
import pytest

NLP_ROOT = Path(__file__).resolve().parent.parent
if str(NLP_ROOT) not in sys.path:
    sys.path.insert(0, str(NLP_ROOT))

from schemas.ocr_contract import OCRDocument, OCRPage, OCRBlock
from schemas.field_result import FieldTier
from evaluation.metrics import (
    levenshtein_distance,
    character_error_rate,
    FieldMetric,
    SafetyMetrics,
    EvaluationReport,
)
from evaluation.benchmark import (
    GroundTruthRecord,
    BenchmarkRunner,
)

FIXTURES_DIR = NLP_ROOT / "fixtures"


class TestEvaluationMetricsMath:
    """Tests unit calculation of NLP and distance metrics."""

    def test_levenshtein_distance(self):
        assert levenshtein_distance("128/3", "128/3") == 0
        assert levenshtein_distance("128/3", "128/l") == 1
        assert levenshtein_distance("", "hello") == 5
        assert levenshtein_distance("Khandagiri", "Khandgiri") == 1

    def test_character_error_rate(self):
        assert character_error_rate("128/3", "128/3") == 0.0
        # 1 error in 5 characters = 0.20
        assert character_error_rate("128/3", "128/l") == 0.20
        assert character_error_rate("", "") == 0.0

    def test_field_metric_tallies(self):
        m = FieldMetric(field_name="plot_number", tier=FieldTier.TIER_1_IMMUTABLE)

        # 1 Exact Match
        m.record_match("128/3", "128/3")
        # 1 Close Match (dist <= 2) -> counts as true positive
        m.record_match("128/3-A", "128/3A")
        # 1 False Positive / Error
        m.record_match("500", "999")
        # 1 False Negative (missed)
        m.record_match("220", None)

        assert m.total_evaluated == 4
        assert m.exact_matches == 1
        assert m.true_positives == 2
        assert m.false_positives == 1
        assert m.false_negatives == 1

        assert m.precision == round(2 / (2 + 1), 4)
        assert m.recall == round(2 / (2 + 1), 4)
        assert m.exact_match_accuracy == 0.25


class TestSafetyMetrics:
    """Tests legal safety compliance and ambiguity metrics."""

    def test_far_and_frr_calculations(self):
        safety = SafetyMetrics()

        # 10 clean docs: 9 auto-approved, 1 mistakenly sent to review (FRR = 1/10 = 10%)
        safety.clean_docs_total = 10
        safety.clean_docs_routed_to_review = 1

        # 5 corrupted docs: 5 correctly sent to review, 0 auto-approved (FAR = 0.0%)
        safety.corrupted_docs_total = 5
        safety.corrupted_docs_auto_approved = 0

        assert safety.false_acceptance_rate == 0.0
        assert safety.false_rejection_rate == 0.10
        assert safety.is_rule_5_compliant is True

    def test_far_critical_failure_flag(self):
        safety = SafetyMetrics()
        safety.corrupted_docs_total = 4
        safety.corrupted_docs_auto_approved = 1  # 1 corrupted slipped past!

        assert safety.false_acceptance_rate == 0.25

    def test_rule_5_violation_flag(self):
        safety = SafetyMetrics()
        safety.rule_5_violations = 1
        assert safety.is_rule_5_compliant is False


class TestEvaluationReportSerialization:
    """Tests report formatting to dictionary and Markdown."""

    def test_report_to_markdown_and_dict(self):
        m1 = FieldMetric(field_name="khata_number", tier=FieldTier.TIER_1_IMMUTABLE)
        m1.record_match("45", "45")

        m2 = FieldMetric(field_name="village", tier=FieldTier.TIER_3_ENTITY_LINGUISTIC)
        m2.record_match("Khandagiri", "Khandagiri")

        report = EvaluationReport(
            total_documents=1,
            field_metrics={"khata_number": m1, "village": m2},
            safety_metrics=SafetyMetrics(clean_docs_total=1),
            mean_latency_ms=42.5
        )

        d = report.to_dict()
        assert d["total_documents"] == 1
        assert d["mean_latency_ms"] == 42.5
        assert d["safety_metrics"]["rule_5_compliant"] is True
        assert "khata_number" in d["field_details"]

        md = report.to_markdown()
        assert "# BhuNexis NLP Document Understanding - Benchmark Report" in md
        assert "`khata_number`" in md
        assert "42.50 ms" in md
        assert "False Acceptance Rate (FAR):** 0.00%" in md


class TestBenchmarkRunnerEndToEnd:
    """Runs BenchmarkRunner on realistic clean and corrupted land record datasets."""

    def test_benchmark_runner_execution(self):
        runner = BenchmarkRunner()

        # 1. Clean English fixture
        clean_gt = GroundTruthRecord(
            document_id="DOC_001",
            expected_fields={
                "khata_number": "45",
                "plot_number": "128/3",
                "owner_name": "Ramesh Chandra Sahu",
                "village": "Khandagiri",
                "tehsil": "Bhubaneswar",
                "district": "Khordha",
            },
            is_corrupted_or_ambiguous=False,
            expected_needs_review=False
        )

        # 2. Corrupted / Ambiguous document ("382/l" instead of "382/1")
        corrupted_doc = OCRDocument(
            document_id="DOC_AMBIGUOUS_TEST",
            language="en",
            pages=[
                OCRPage(
                    page_number=1,
                    image_width=1000.0,
                    image_height=1400.0,
                    ocr_blocks=[
                        OCRBlock(text="Khata No: 124", bbox=[100.0, 300.0, 400.0, 340.0], confidence=0.98),
                        OCRBlock(text="Plot No: 382/l", bbox=[100.0, 400.0, 400.0, 440.0], confidence=0.76),
                    ]
                )
            ]
        )
        corrupted_gt = GroundTruthRecord(
            document_id="DOC_AMBIGUOUS_TEST",
            expected_fields={
                "khata_number": "124",
                "plot_number": "382/l",
            },
            is_corrupted_or_ambiguous=True,
            expected_needs_review=True
        )

        dataset = [
            (FIXTURES_DIR / "english_sample.json", clean_gt),
            (corrupted_doc, corrupted_gt),
        ]

        report = runner.run_benchmark(dataset)

        assert report.total_documents == 2
        assert report.mean_latency_ms > 0.0

        # CRITICAL SAFETY REQUIREMENT:
        # The corrupted scan MUST NOT be auto-accepted. FAR must be 0.0%.
        assert report.safety_metrics.false_acceptance_rate == 0.0
        # The clean scan was not rejected
        assert report.safety_metrics.false_rejection_rate == 0.0
        # Rule 5 must be 100% compliant (no auto-normalization of Tier 1 without officer)
        assert report.safety_metrics.is_rule_5_compliant is True

        # Field metrics check
        assert "plot_number" in report.field_metrics
        assert "khata_number" in report.field_metrics
        assert report.field_metrics["plot_number"].true_positives > 0
