"""
evidence/evidence_linker.py - Evidence Grounding & Provenance Binding.

Binds extracted fields to their physical source tokens on the scanned document.
Generates EvidenceSnippet objects with unified bounding boxes for the Officer UI.
"""

from typing import List, Optional, Tuple
from schemas.ocr_contract import OCRBlock, OCRPage
from schemas.field_result import EvidenceSnippet
from .bbox_utils import merge_bboxes, are_horizontally_aligned, are_vertically_aligned


class EvidenceLinker:
    """Manages spatial evidence grounding between extracted entities and OCR blocks."""

    @staticmethod
    def create_evidence(
        source_blocks: List[OCRBlock], 
        page_number: int = 1, 
        explicit_text: Optional[str] = None
    ) -> EvidenceSnippet:
        """
        Creates an EvidenceSnippet by merging bounding boxes and calculating
        weighted average confidence across the contributing OCR blocks.
        """
        if not source_blocks:
            raise ValueError("Cannot create evidence without at least one source OCRBlock")

        merged_bbox = merge_bboxes([b.bbox for b in source_blocks])
        combined_text = explicit_text if explicit_text is not None else " ".join(b.text for b in source_blocks)
        
        # Weighted average confidence based on token width
        total_width = sum(b.width for b in source_blocks)
        if total_width > 0:
            avg_conf = sum(b.confidence * b.width for b in source_blocks) / total_width
        else:
            avg_conf = sum(b.confidence for b in source_blocks) / len(source_blocks)

        return EvidenceSnippet(
            page_number=page_number,
            bbox=merged_bbox,
            source_text=combined_text.strip(),
            ocr_confidence=round(avg_conf, 3)
        )

    @staticmethod
    def find_associated_blocks(
        label_text: str, 
        page: OCRPage, 
        y_tolerance: float = 30.0,
        max_search_dist: float = 400.0
    ) -> Tuple[Optional[OCRBlock], List[OCRBlock]]:
        """
        Finds a label block (e.g. 'Plot No:') and returns the label block along with
        all value blocks positioned immediately to its right on the same line.
        """
        label_lower = label_text.lower().strip()
        matched_label_block: Optional[OCRBlock] = None

        # Step 1: Identify the label block
        for block in page.ocr_blocks:
            if label_lower in block.text.lower():
                matched_label_block = block
                break

        if not matched_label_block:
            return None, []

        # Step 2: Find all value blocks horizontally aligned to the right
        value_blocks = []
        l_x2 = matched_label_block.bbox[2]

        for block in page.ocr_blocks:
            if block == matched_label_block:
                continue
            
            # Check horizontal direction and maximum search distance
            v_x1 = block.bbox[0]
            if v_x1 >= l_x2 and (v_x1 - l_x2) <= max_search_dist:
                if are_horizontally_aligned(matched_label_block.bbox, block.bbox, y_tolerance=y_tolerance):
                    value_blocks.append(block)

        # Sort left-to-right
        value_blocks.sort(key=lambda b: b.bbox[0])
        return matched_label_block, value_blocks

    @staticmethod
    def find_column_blocks(
        header_text: str,
        page: OCRPage,
        x_tolerance: float = 60.0
    ) -> Tuple[Optional[OCRBlock], List[OCRBlock]]:
        """
        In tabular land records, finds the column header block and returns all cell
        blocks positioned directly beneath it.
        """
        header_lower = header_text.lower().strip()
        matched_header: Optional[OCRBlock] = None

        for block in page.ocr_blocks:
            if header_lower in block.text.lower():
                matched_header = block
                break

        if not matched_header:
            return None, []

        cell_blocks = []
        for block in page.ocr_blocks:
            if block == matched_header:
                continue
            if are_vertically_aligned(matched_header.bbox, block.bbox, x_tolerance=x_tolerance):
                cell_blocks.append(block)

        # Sort top-to-bottom
        cell_blocks.sort(key=lambda b: b.bbox[1])
        return matched_header, cell_blocks
