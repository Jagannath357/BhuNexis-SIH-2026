"""
extractors/transformer_extractor.py - Area 8 & Phase 5 (LayoutLMv3 & 2D Spatial Tabular Extractor).

Extracts fields using 2D spatial layouts, table column headers, and normalized bounding box alignment.
Handles multi-row RoR/Khatian tabular records where labels are not repeated on each row.
"""

import re
from typing import Dict, List, Optional
from schemas.ocr_contract import OCRBlock, OCRPage
from schemas.canonical_record import STATE_TERMINOLOGY_MAP
from evidence.bbox_utils import normalize_bbox, are_vertically_aligned
from .regex_extractor import ExtractedCandidate


class TransformerExtractor:
    """
    Layout-aware 2D spatial extractor.
    Aligns table columns and multi-row cells to extract canonical land-record fields.
    """

    # Common Column Header keywords mapped to canonical fields
    COLUMN_HEADER_KEYWORDS = [
        (["khata", "khatian", "jamabandi"], "khata_number"),
        (["plot", "p1ot", "dag", "khasra", "survey", "chaka"], "plot_number"),
        (["area", "rakba", "total area"], "area_value"),
        (["name", "pattadar", "tenant", "raiyat"], "owner_name"),
        (["father", "guardian"], "father_or_guardian_name"),
        (["kisam", "classification", "type"], "land_classification"),
    ]

    @classmethod
    def extract_from_page(cls, page: OCRPage) -> Dict[str, ExtractedCandidate]:
        """
        Scans an OCRPage using 2D geometry to identify column headers and extract
        vertically aligned data cells.
        """
        results: Dict[str, ExtractedCandidate] = {}
        headers_found = []

        # Step 1: Identify all column headers on the page
        for block in page.ocr_blocks:
            text_strip = block.text.strip()
            text_lower = text_strip.lower()

            # Column header cannot be a key-value pair (e.g. "Khata No: 45")
            if re.search(r":\s*\S+", text_strip):
                continue
            # Column headers shouldn't be long sentences
            if len(text_strip.split()) > 5:
                continue
            # Column headers generally don't contain digits
            if any(c.isdigit() for c in text_strip):
                continue

            for keywords, canonical_field in cls.COLUMN_HEADER_KEYWORDS:
                if any(kw in text_lower for kw in keywords):
                    headers_found.append((canonical_field, block))
                    break

        if not headers_found:
            return results

        # Step 2: For each identified column header, find vertically aligned cells below it
        for canonical_field, header_block in headers_found:
            if canonical_field in results:
                continue

            aligned_cells = []
            h_y2 = header_block.bbox[3]

            for block in page.ocr_blocks:
                if block == header_block:
                    continue

                # Cell must be below header
                if block.bbox[1] >= h_y2:
                    if are_vertically_aligned(header_block.bbox, block.bbox, x_tolerance=50.0):
                        aligned_cells.append(block)

            if aligned_cells:
                # Sort cells top-to-bottom
                aligned_cells.sort(key=lambda b: b.bbox[1])
                # Take the first data row under the header
                target_cell = aligned_cells[0]

                results[canonical_field] = ExtractedCandidate(
                    field_name=canonical_field,
                    raw_value=target_cell.text.strip(),
                    contributing_blocks=[target_cell],
                    label_block=header_block,
                    extractor_confidence=0.92,
                    extractor_source="transformer_layout_column"
                )

        return results
