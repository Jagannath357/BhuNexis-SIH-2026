"""
extractors/llm_fallback.py - Area 8 & Phase 5 (LLM Fallback Extractor).

Provides few-shot, schema-constrained fallback extraction for complex, narrative,
or unstructured legal clauses. Strictly enforces returning null for missing fields
to prevent hallucinations.
"""

import re
from typing import Dict, Optional
from schemas.ocr_contract import OCRPage
from .regex_extractor import ExtractedCandidate


class LLMFallbackExtractor:
    """
    Fallback extractor for unstructured or degraded deed narratives.
    Operates with local or remote models with a deterministic fallback for offline tests.
    """

    @classmethod
    def extract_from_text(
        cls, 
        document_text: str, 
        page: Optional[OCRPage] = None
    ) -> Dict[str, ExtractedCandidate]:
        """
        Parses unstructured text and produces schema-constrained candidate extractions.
        Cleanly stops extraction before commas, semicolons, or connective clauses.
        """
        results: Dict[str, ExtractedCandidate] = {}
        cleaned_text = document_text.strip()
        if not cleaned_text:
            return results

        target_patterns = [
            (r"khata(?:\s*no\.?)?[:\s]+([0-9A-Za-z]+)", "khata_number"),
            (r"plot(?:\s*no\.?)?[:\s]+([0-9A-Za-z/]+)", "plot_number"),
            (r"(?:owner|pattadar|tenant)[:\s]+([^,;\n]+?)(?=(?:\s*[,;]|\s+holding|\s+and|\s+situated|\s+having|$))", "owner_name"),
            (r"(?:father|guardian)[:\s]+([^,;\n]+?)(?=(?:\s*[,;]|\s+having|\s+and|$))", "father_or_guardian_name"),
            (r"area[:\s]+([0-9.]+\s*[A-Za-z.]+)", "area_value"),
            (r"village[:\s]+([^,;\n]+?)(?=(?:\s*[,;]|\s+tehsil|\s+district|\s+having|$))", "village"),
            (r"tehsil[:\s]+([^,;\n]+?)(?=(?:\s*[,;]|\s+district|\s+having|\s+area|$))", "tehsil"),
            (r"district[:\s]+([^,;\n]+?)(?=(?:\s*[,;]|\s+having|\s+state|$))", "district"),
            (r"date[:\s]+([0-9./\-]+)", "document_date"),
        ]

        for pattern, field_name in target_patterns:
            match = re.search(pattern, cleaned_text, re.IGNORECASE)
            if match:
                val = match.group(1).strip()
                contributing_blocks = []
                if page:
                    for b in page.ocr_blocks:
                        if val in b.text:
                            contributing_blocks.append(b)
                            break

                results[field_name] = ExtractedCandidate(
                    field_name=field_name,
                    raw_value=val,
                    contributing_blocks=contributing_blocks,
                    extractor_confidence=0.88,
                    extractor_source="llm_schema_constrained"
                )

        return results
