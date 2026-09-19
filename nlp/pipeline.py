"""
pipeline.py - Master Orchestrator for BhuNexis Document Understanding Pipeline.

Chains together the complete 10-Area lifecycle:
OCR Ingestion -> Multi-Tier Extraction -> Evidence Grounding -> Ambiguity Firewall ->
Composite Confidence Scoring -> Quality Gate -> Canonical Record Packaging -> Notification Hook.
"""

import json
from typing import Dict, Optional, Any, Callable, Union
from pathlib import Path

try:
    from .schemas.ocr_contract import OCRDocument, OCRPage
    from .schemas.canonical_record import CanonicalRecord
    from .schemas.field_result import FieldResult, FieldTier, FieldStatus
    from .extractors.regex_extractor import RegexExtractor, ExtractedCandidate
    from .extractors.spacy_extractor import SpacyExtractor
    from .extractors.transformer_extractor import TransformerExtractor
    from .normalizers.safe_normalizer import SafeNormalizer
    from .evidence.evidence_linker import EvidenceLinker
    from .confidence.quality_gate import QualityGate
except (ImportError, ValueError):
    from schemas.ocr_contract import OCRDocument, OCRPage
    from schemas.canonical_record import CanonicalRecord
    from schemas.field_result import FieldResult, FieldTier, FieldStatus
    from extractors.regex_extractor import RegexExtractor, ExtractedCandidate
    from extractors.spacy_extractor import SpacyExtractor
    from extractors.transformer_extractor import TransformerExtractor
    from normalizers.safe_normalizer import SafeNormalizer
    from evidence.evidence_linker import EvidenceLinker
    from confidence.quality_gate import QualityGate


class MasterNLPPipeline:
    """
    Master orchestrator converting raw OCR JSON into validated, auditable Canonical Records.
    Enforces Rule 1 (Tiering), Rule 2 (Two-Track), Rule 3 (Ambiguity Firewall), and Rule 4 (Audit).
    """

    def __init__(self, on_review_required: Optional[Callable[[Dict[str, Any]], None]] = None):
        """
        Args:
            on_review_required: Optional callback hook triggered when a document requires human review.
                               Receives record.to_officer_payload() for backend WebSocket notifications.
        """
        self.on_review_required = on_review_required

    def process_document(
        self, 
        ocr_input: Union[Dict[str, Any], str, Path, OCRDocument],
        state: str = "ODISHA",
        output_path: Optional[Union[str, Path]] = None
    ) -> CanonicalRecord:
        """
        Runs the complete end-to-end understanding pipeline on an OCR document.

        Args:
            ocr_input: Dict from OCR teammate, file path to JSON, or validated OCRDocument.
            state: State context for terminology resolution (default: "ODISHA").
            output_path: Optional file path to save the normalized JSON result for verification.

        Returns:
            CanonicalRecord with all fields, confidences, evidence bboxes, and review status.
        """
        # Step 1: Ingest & Validate Input Contract (Phase 1)
        doc: OCRDocument = self._load_ocr_document(ocr_input)
        
        record = CanonicalRecord(
            document_id=doc.document_id,
            state=state,
            language=doc.language or "en"
        )

        if not doc.pages:
            record.overall_status = FieldStatus.NOT_FOUND
            record.needs_human_review = True
            record.review_reasons = ["OCR document contains no pages."]
            return record

        # Process primary page (or iterate across pages)
        page = doc.pages[0]

        # Step 2: Multi-Tier Extraction (Phase 5)
        # Combine candidates across Regex, SpaCy, and Transformer extractors
        candidates: Dict[str, ExtractedCandidate] = {}

        # 2a. Regex Anchor Extraction (High precision for structured key-values)
        regex_candidates = RegexExtractor.extract_from_page(page)
        candidates.update(regex_candidates)

        # 2b. Transformer / Table Column Extraction (Tabular column-row alignment)
        transformer_candidates = TransformerExtractor.extract_from_page(page)
        for k, v in transformer_candidates.items():
            if k not in candidates:
                candidates[k] = v

        # 2c. SpaCy NER Extraction (Specialized for person & location names)
        ner_candidates = SpacyExtractor.extract_from_page(page)
        for k, v in ner_candidates.items():
            if k not in candidates:
                candidates[k] = v

        # Step 3: Evidence Grounding & Confidence Evaluation (Phases 2, 3, 4)
        for field_name, cand in candidates.items():
            # 3a. Ground Evidence BBox
            evidence_snippet = None
            c_ocr = 0.90
            bbox_val = None
            bbox_lbl = cand.label_block.bbox if cand.label_block else None

            if cand.contributing_blocks:
                evidence_snippet = EvidenceLinker.create_evidence(
                    source_blocks=cand.contributing_blocks,
                    page_number=page.page_number,
                    explicit_text=cand.raw_value
                )
                c_ocr = evidence_snippet.ocr_confidence
                bbox_val = evidence_snippet.bbox

            # 3b. Quality Gate & Ambiguity Firewall Evaluation
            field_result: FieldResult = QualityGate.evaluate_field(
                field_name=field_name,
                raw_value=cand.raw_value,
                c_ocr=c_ocr,
                c_model=cand.extractor_confidence,
                bbox_value=bbox_val,
                bbox_label=bbox_lbl,
                evidence=evidence_snippet
            )

            record.set_field(field_name, field_result)

        # Step 4: Handle Derived Safe Normalizations (e.g. Area sq. meters)
        if record.area_value and record.area_value.raw_value:
            area_norm = SafeNormalizer.normalize_area(record.area_value.raw_value)
            if area_norm:
                record.normalized_area_sqm = FieldResult(
                    field_name="normalized_area_sqm",
                    tier=FieldTier.TIER_2_SAFE_NORMALIZABLE,
                    raw_value=str(area_norm["sqm"]),
                    normalized_value=area_norm["sqm"],
                    status=FieldStatus.NORMALIZED,
                    confidence=record.area_value.confidence,
                    evidence=record.area_value.evidence
                )
                if not record.area_unit:
                    record.area_unit = FieldResult(
                        field_name="area_unit",
                        tier=FieldTier.TIER_2_SAFE_NORMALIZABLE,
                        raw_value=area_norm["unit"],
                        normalized_value=area_norm["unit"],
                        status=FieldStatus.NORMALIZED,
                        confidence=record.area_value.confidence
                    )

        # Step 5: Document-Level Quality Gating (Phase 4)
        record = QualityGate.evaluate_document(record)

        # Step 6: Trigger Backend Notification Hook if Review is Required
        if record.needs_human_review and self.on_review_required:
            try:
                self.on_review_required(record.to_officer_payload())
            except Exception:
                pass  # Do not block processing if external callback fails

        # Step 7: Export to JSON if output_path is requested
        if output_path:
            record.save_to_file(output_path)

        return record

    @staticmethod
    def _load_ocr_document(ocr_input: Union[Dict[str, Any], str, Path, OCRDocument]) -> OCRDocument:
        """Parses various input formats into a validated OCRDocument."""
        if isinstance(ocr_input, OCRDocument):
            return ocr_input
        elif isinstance(ocr_input, (str, Path)):
            path = Path(ocr_input)
            if path.exists() and path.is_file():
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return OCRDocument.model_validate(data)
            else:
                # Treat as raw JSON string
                data = json.loads(str(ocr_input))
                return OCRDocument.model_validate(data)
        elif isinstance(ocr_input, dict):
            return OCRDocument.model_validate(ocr_input)
        else:
            raise ValueError(f"Unsupported OCR input type: {type(ocr_input)}")
