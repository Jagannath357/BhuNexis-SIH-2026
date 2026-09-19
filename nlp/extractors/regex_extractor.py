"""
extractors/regex_extractor.py - Area 8 & Phase 5 (Deterministic Pattern & Key-Value Extractor).

High-speed deterministic extraction for structured land records using tolerant anchor patterns.
Handles:
1. Single-block key-values ("Khata No: 45").
2. Horizontally split blocks ("Khata No:" -> "45").
3. Vertically split blocks ("P1ot Number" -> next line "128/3-A").
"""

import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

from schemas.ocr_contract import OCRBlock, OCRPage
from evidence.bbox_utils import are_horizontally_aligned, are_vertically_aligned


@dataclass
class ExtractedCandidate:
    """Represents a raw candidate extracted by an extractor before normalization & gating."""
    field_name: str
    raw_value: str
    contributing_blocks: List[OCRBlock]
    label_block: Optional[OCRBlock] = None
    extractor_confidence: float = 0.95
    extractor_source: str = "regex"


class RegexExtractor:
    """
    Extracts canonical land-record fields from OCR pages using tolerant regex anchors.
    Tolerant capture ensures values like '382/l' are captured rather than dropped.
    """

    # Single-block Anchor Patterns (must not capture label words like 'Number' as values)
    ANCHOR_PATTERNS: List[Tuple[str, str, int]] = [
        (r"(?:Father(?:'s)?\s*Name|Guardian(?:'s)?\s*Name)[:.\s-]+([^\n,;]+)", "father_or_guardian_name", 1),
        (r"(?:Name\s*of\s*Pattadar|Pattadar\s*Name|Recorded\s*Tenant|Tenant\s*Name|Owner\s*Name|(?<!Father's\s)(?<!Father\s)\bName\b)[:.\s-]+([^\n,;]+)", "owner_name", 1),
        (r"(?:Khata\s*(?:No|N0|Number)?|Khatian\s*(?:No)?|Jamabandi)(?:[:.\s]*[:.-]\s*|\s+)(?!No\b|N0\b|Number\b)([A-Za-z0-9@#/\-]+)", "khata_number", 1),
        (r"(?:Plot\s*(?:No|N0|Number)?|P1ot\s*(?:No|Number)?|Dag\s*(?:No)?|Khasra\s*(?:No)?|Survey\s*(?:No)?)(?:[:.\s]*[:.-]\s*|\s+)(?!No\b|N0\b|Number\b)([A-Za-z0-9/\-]+)", "plot_number", 1),
        (r"(?:Area|Land\s*Area|Total\s*Area|Rakba)[:.\s-]+([0-9.]+\s*[A-Za-z.]+)", "area_value", 1),
        (r"(?:Village|Vil1age|Mouza|Mauza|Gram)[:.\s-]+([A-Za-z\s]+)", "village", 1),
        (r"(?:Tehsil|Tehsi1|Tahasil|Taluk|Mandal)[:.\s-]+([A-Za-z\s]+)", "tehsil", 1),
        (r"(?:District|Distt\.?|Dist\.?|Zilla|Jilla)[:.\s-]+([A-Za-z\s]+)", "district", 1),
        (r"(?:Mutation\s*No\.?|Case\s*No\.?)[:.\s-]+([A-Za-z0-9/\-]+)", "mutation_number", 1),
        (r"(?:Date|Order\s*Date|Registration\s*Date|Date\s*of\s*Record)[:.\s-]+([0-9]{1,2}(?:st|nd|rd|th)?[-/\s]+[A-Za-z]+[-/\s]+[0-9]{4}|[0-9]{1,4}[-/.][0-9]{1,2}[-/.][0-9]{1,4})", "document_date", 1),
    ]

    # Standalone label patterns for adjacent split blocks
    LABEL_SPLIT_PATTERNS: List[Tuple[str, str]] = [
        (r"^(?:Name\s*of\s*Pattadar|Pattadar\s*Name|Recorded\s*Tenant|Owner\s*Name)[:.\s-]*$", "owner_name"),
        (r"^(?:Father(?:'s)?\s*Name|Guardian(?:'s)?\s*Name)[:.\s-]*$", "father_or_guardian_name"),
        (r"^(?:Khata\s*(?:No|N0|Number)?|Khatian\s*(?:No)?|Khata\s+N0\.)[:.\s-]*$", "khata_number"),
        (r"^(?:Plot\s*(?:No|N0|Number)?|P1ot\s*(?:Number|No)?|Dag\s*(?:No)?|Khasra\s*(?:No)?|Survey\s*(?:No)?|Chaka)[:.\s-]*$", "plot_number"),
        (r"^(?:Area|Land\s*Area|Total\s*Area|Rakba)[:.\s-]*$", "area_value"),
        (r"^(?:Village|Vil1age|Mouza|Mauza|Gram)[:.\s-]*$", "village"),
        (r"^(?:Tehsil|Tehsi1|Tahasil|Taluk)[:.\s-]*$", "tehsil"),
        (r"^(?:District|Distt\.?|Dist\.?|Zilla)[:.\s-]*$", "district"),
        (r"^(?:Mutation\s*No\.?|Case\s*No\.?)[:.\s-]*$", "mutation_number"),
        (r"^(?:Date|Order\s*Date|Registration\s*Date)[:.\s-]*$", "document_date"),
    ]

    @classmethod
    def extract_from_page(cls, page: OCRPage) -> Dict[str, ExtractedCandidate]:
        """
        Scans an OCRPage and extracts land record fields.
        Returns a mapping from canonical_field_name -> ExtractedCandidate.
        """
        results: Dict[str, ExtractedCandidate] = {}
        processed_blocks = set()

        # Strategy 1: Single-block key-value pairs (e.g. "Khata No: 45")
        for block in page.ocr_blocks:
            text = block.text.strip()
            for pattern, canonical_field, group_idx in cls.ANCHOR_PATTERNS:
                if canonical_field in results:
                    continue
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    raw_val = match.group(group_idx).strip()
                    if raw_val and raw_val.lower() not in ("no", "number", "name"):
                        results[canonical_field] = ExtractedCandidate(
                            field_name=canonical_field,
                            raw_value=raw_val,
                            contributing_blocks=[block],
                            label_block=block,
                            extractor_confidence=0.96,
                            extractor_source="regex_single_block"
                        )
                        processed_blocks.add(id(block))
                        break

        # Strategy 2: Adjacent split blocks (horizontally to the right OR directly below)
        for block in page.ocr_blocks:
            if id(block) in processed_blocks:
                continue
            text = block.text.strip()

            for label_pattern, canonical_field in cls.LABEL_SPLIT_PATTERNS:
                if canonical_field in results:
                    continue
                if re.match(label_pattern, text, re.IGNORECASE):
                    # Check horizontally adjacent or directly below
                    val_block = cls._find_adjacent_block(block, page.ocr_blocks)
                    if val_block and id(val_block) not in processed_blocks:
                        raw_val = val_block.text.strip()
                        # Ensure candidate value is not itself another field label or generic word
                        is_another_label = any(re.match(lp, raw_val, re.IGNORECASE) for lp, _ in cls.LABEL_SPLIT_PATTERNS)
                        if is_another_label or raw_val.lower() in ("no", "number", "name", "plot", "khata", "area"):
                            continue

                        # For numeric fields, value must contain digits or valid identifiers
                        if canonical_field in ("khata_number", "plot_number") and not any(c.isdigit() for c in raw_val):
                            continue

                        results[canonical_field] = ExtractedCandidate(
                            field_name=canonical_field,
                            raw_value=raw_val,
                            contributing_blocks=[val_block],
                            label_block=block,
                            extractor_confidence=0.93,
                            extractor_source="regex_adjacent_block"
                        )
                        processed_blocks.add(id(block))
                        processed_blocks.add(id(val_block))
                        break

        return results

    @staticmethod
    def _find_adjacent_block(label_block: OCRBlock, all_blocks: List[OCRBlock], max_dist: float = 450.0) -> Optional[OCRBlock]:
        """
        Finds the associated value block:
        1. Closest block horizontally to the right on the same line.
        2. OR closest block situated vertically directly underneath.
        """
        l_x1, l_y1, l_x2, l_y2 = label_block.bbox

        # Try Option 1: Horizontally to the right
        h_candidates = []
        for b in all_blocks:
            if b == label_block:
                continue
            b_x1 = b.bbox[0]
            if b_x1 >= (l_x2 - 10.0) and (b_x1 - l_x2) <= max_dist:
                if are_horizontally_aligned(label_block.bbox, b.bbox, y_tolerance=35.0):
                    dist = abs(b_x1 - l_x2)
                    h_candidates.append((dist, b))

        if h_candidates:
            h_candidates.sort(key=lambda x: x[0])
            return h_candidates[0][1]

        # Try Option 2: Vertically directly below (within 120px)
        v_candidates = []
        for b in all_blocks:
            if b == label_block:
                continue
            b_y1 = b.bbox[1]
            if b_y1 >= (l_y2 - 10.0) and (b_y1 - l_y2) <= 120.0:
                if are_vertically_aligned(label_block.bbox, b.bbox, x_tolerance=100.0):
                    dist = abs(b_y1 - l_y2)
                    v_candidates.append((dist, b))

        if v_candidates:
            v_candidates.sort(key=lambda x: x[0])
            return v_candidates[0][1]

        return None
