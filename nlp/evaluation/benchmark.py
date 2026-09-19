"""
evaluation/benchmark.py - Benchmark Execution Runner for BhuNexis NLP Pipeline.

Executes ground-truth validation across test suites and produces comprehensive
performance, latency, and safety compliance reports.
"""

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Union
from pathlib import Path

try:
    from ..schemas.ocr_contract import OCRDocument
    from ..schemas.canonical_record import CanonicalRecord
    from ..schemas.field_result import FieldTier
    from ..pipeline import MasterNLPPipeline
    from .metrics import (
        FieldMetric,
        SafetyMetrics,
        EvaluationReport,
        character_error_rate,
    )
except (ImportError, ValueError):
    from schemas.ocr_contract import OCRDocument
    from schemas.canonical_record import CanonicalRecord
    from schemas.field_result import FieldTier
    from pipeline import MasterNLPPipeline
    from evaluation.metrics import (
        FieldMetric,
        SafetyMetrics,
        EvaluationReport,
        character_error_rate,
    )


# Standard canonical fields mapped to their risk tiers
CANONICAL_FIELD_TIERS = {
    "khata_number": FieldTier.TIER_1_IMMUTABLE,
    "plot_number": FieldTier.TIER_1_IMMUTABLE,
    "owner_name": FieldTier.TIER_3_ENTITY_LINGUISTIC,
    "father_or_guardian_name": FieldTier.TIER_3_ENTITY_LINGUISTIC,
    "area_value": FieldTier.TIER_2_SAFE_NORMALIZABLE,
    "village": FieldTier.TIER_3_ENTITY_LINGUISTIC,
    "tehsil": FieldTier.TIER_3_ENTITY_LINGUISTIC,
    "district": FieldTier.TIER_3_ENTITY_LINGUISTIC,
    "date_of_record": FieldTier.TIER_2_SAFE_NORMALIZABLE,
    "land_classification": FieldTier.TIER_3_ENTITY_LINGUISTIC,
}


@dataclass
class GroundTruthRecord:
    """Ground truth annotations for evaluating an OCR document."""
    document_id: str
    expected_fields: Dict[str, str] = field(default_factory=dict)
    is_corrupted_or_ambiguous: bool = False
    expected_needs_review: bool = False


class BenchmarkRunner:
    """
    Executes end-to-end benchmarking against ground truth datasets.
    Calculates field-level P/R/F1, CER, FAR, FRR, and latency.
    """

    def __init__(self, pipeline: Optional[MasterNLPPipeline] = None):
        self.pipeline = pipeline or MasterNLPPipeline()

    def run_benchmark(
        self,
        test_dataset: List[Tuple[Union[OCRDocument, Dict[str, Any], Path, str], GroundTruthRecord]]
    ) -> EvaluationReport:
        """
        Runs the benchmark over a collection of (OCRInput, GroundTruthRecord) pairs.
        """
        # Initialize FieldMetrics
        field_metrics: Dict[str, FieldMetric] = {
            name: FieldMetric(field_name=name, tier=tier)
            for name, tier in CANONICAL_FIELD_TIERS.items()
        }

        safety_metrics = SafetyMetrics()
        total_latency_ms = 0.0

        for ocr_input, gt in test_dataset:
            # Measure processing latency
            t0 = time.perf_counter()
            record: CanonicalRecord = self.pipeline.process_document(ocr_input)
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            total_latency_ms += elapsed_ms

            # 1. Update Safety Metrics (FAR / FRR / Rule 5)
            if gt.is_corrupted_or_ambiguous or gt.expected_needs_review:
                safety_metrics.corrupted_docs_total += 1
                if not record.needs_human_review:
                    # Catastrophic: corrupted/ambiguous record slipped past without review
                    safety_metrics.corrupted_docs_auto_approved += 1
            else:
                safety_metrics.clean_docs_total += 1
                if record.needs_human_review:
                    # Clean record sent to review unnecessarily
                    safety_metrics.clean_docs_routed_to_review += 1

            # Check Rule 5 compliance on Tier 1 fields:
            # Tier 1 field must NEVER alter normalized_value from raw_value without human verification
            for t1_field in ["plot_number", "khata_number"]:
                f_res = getattr(record, t1_field, None)
                if f_res and f_res.normalized_value is not None:
                    if str(f_res.normalized_value).strip() != str(f_res.raw_value).strip():
                        if f_res.status != FieldStatus.VERIFIED_BY_HUMAN:
                            safety_metrics.rule_5_violations += 1

            # 2. Update Field-Level Extraction Metrics
            for field_name, expected_val in gt.expected_fields.items():
                if field_name not in field_metrics:
                    tier = CANONICAL_FIELD_TIERS.get(field_name, FieldTier.TIER_3_ENTITY_LINGUISTIC)
                    field_metrics[field_name] = FieldMetric(field_name=field_name, tier=tier)

                f_res = getattr(record, field_name, None)
                # If field was extracted, choose value (normalized or raw)
                pred_val = None
                if f_res:
                    pred_val = f_res.normalized_value or f_res.raw_value

                field_metrics[field_name].record_match(expected_val, pred_val)

        total_docs = len(test_dataset)
        mean_latency = (total_latency_ms / total_docs) if total_docs > 0 else 0.0

        return EvaluationReport(
            total_documents=total_docs,
            field_metrics=field_metrics,
            safety_metrics=safety_metrics,
            mean_latency_ms=mean_latency,
        )
