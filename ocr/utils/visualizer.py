import cv2
import numpy as np
from typing import List, Tuple, Optional
from pathlib import Path
from engines.base_engine import OCRResult, OCRBox


class OCRVisualizer:
    """Utility to render OCR detection bounding boxes and confidence overlays."""

    @staticmethod
    def draw_bounding_boxes(
        image: np.ndarray,
        boxes: List[OCRBox],
        box_color: Tuple[int, int, int] = (0, 180, 255),       # Amber / Orange
        text_color: Tuple[int, int, int] = (255, 255, 255),    # White
        bg_color: Tuple[int, int, int] = (30, 30, 30),         # Dark Gray
        thickness: int = 2
    ) -> np.ndarray:
        """
        Draws bounding polygons and confidence tags over the image.
        """
        vis_img = image.copy()
        if len(vis_img.shape) == 2:
            vis_img = cv2.cvtColor(vis_img, cv2.COLOR_GRAY2BGR)

        for item in boxes:
            pts = np.array(item.box, np.int32)
            pts = pts.reshape((-1, 1, 2))
            # Draw polygon box
            cv2.polylines(vis_img, [pts], isClosed=True, color=box_color, thickness=thickness)

            # Draw text label with confidence
            label = f"{item.text} ({item.confidence:.2f})"
            x, y = pts[0][0]
            # Background badge for legibility
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
            y_badge = max(th + 5, y - 4)
            cv2.rectangle(vis_img, (x, y_badge - th - 3), (x + tw + 6, y_badge + 2), bg_color, -1)
            cv2.putText(vis_img, label, (x + 3, y_badge - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.45, text_color, 1, cv2.LINE_AA)

        return vis_img

    @staticmethod
    def create_comparison_grid(
        original: np.ndarray,
        preprocessed: np.ndarray,
        annotated: np.ndarray,
        target_height: int = 700
    ) -> np.ndarray:
        """
        Concatenates Original, Preprocessed, and Annotated images side-by-side
        with clean title headers.
        """
        def format_panel(img: np.ndarray, title: str) -> np.ndarray:
            if len(img.shape) == 2:
                panel = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            else:
                panel = img.copy()

            # Resize keeping aspect ratio
            h, w = panel.shape[:2]
            scale = target_height / float(h)
            new_w = int(w * scale)
            resized = cv2.resize(panel, (new_w, target_height), interpolation=cv2.INTER_AREA)

            # Add header banner
            header = np.zeros((45, new_w, 3), dtype=np.uint8)
            header[:] = (24, 24, 27)  # Dark slate
            cv2.putText(header, title, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 220, 180), 2, cv2.LINE_AA)

            return np.vstack([header, resized])

        p1 = format_panel(original, "1. Raw Land Record")
        p2 = format_panel(preprocessed, "2. Preprocessed (CLAHE + Denoise)")
        p3 = format_panel(annotated, "3. OCR Detection & Recognition")

        # Combine horizontally
        divider = np.zeros((p1.shape[0], 6, 3), dtype=np.uint8)
        divider[:] = (50, 50, 60)
        return np.hstack([p1, divider, p2, divider, p3])

    @staticmethod
    def save_annotated_image(image: np.ndarray, output_path: Path) -> None:
        """Saves image safely handling Windows file paths."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imencode(".jpg", image)[1].tofile(str(output_path))
