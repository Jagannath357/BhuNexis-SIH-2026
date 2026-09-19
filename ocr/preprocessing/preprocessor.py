import cv2
import numpy as np
from typing import Tuple, Dict, Any, Union
from pathlib import Path


class ImagePreprocessor:
    """
    OpenCV-based image preprocessing pipeline specifically tuned for
    aged, handwritten English land-record documents.
    """

    def __init__(self, target_dpi_scale: float = 1.5):
        self.target_dpi_scale = target_dpi_scale

    @staticmethod
    def load_image(image_input: Union[str, Path, np.ndarray]) -> np.ndarray:
        """Loads an image from file path or validates an existing numpy array."""
        if isinstance(image_input, (str, Path)):
            path_str = str(image_input)
            img = cv2.imread(path_str)
            if img is None:
                # Handle non-ascii Windows paths
                img = cv2.imdecode(np.fromfile(path_str, dtype=np.uint8), cv2.IMREAD_COLOR)
            if img is None:
                raise FileNotFoundError(f"Failed to load image from path: {path_str}")
            return img
        elif isinstance(image_input, np.ndarray):
            return image_input.copy()
        else:
            raise TypeError("Expected image path (str/Path) or numpy array")

    @staticmethod
    def resize(image: np.ndarray, min_width: int = 1200, max_width: int = 2400) -> np.ndarray:
        """
        Resize image ensuring sufficient resolution for stroke recognition
        without exceeding GPU/CPU memory bounds.
        """
        h, w = image.shape[:2]
        if w < min_width:
            scale = min_width / float(w)
            new_w = int(w * scale)
            new_h = int(h * scale)
            return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
        elif w > max_width:
            scale = max_width / float(w)
            new_w = int(w * scale)
            new_h = int(h * scale)
            return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
        return image

    @staticmethod
    def to_grayscale(image: np.ndarray) -> np.ndarray:
        """Converts BGR image to single-channel 8-bit grayscale."""
        if len(image.shape) == 2:
            return image
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def denoise_bilateral(gray: np.ndarray, diameter: int = 9, sigma_color: int = 75, sigma_space: int = 75) -> np.ndarray:
        """
        Bilateral filter smooths paper grain and background stains while keeping
        handwritten stroke boundaries crisp.
        """
        return cv2.bilateralFilter(gray, diameter, sigma_color, sigma_space)

    @staticmethod
    def denoise_gaussian(gray: np.ndarray, ksize: Tuple[int, int] = (3, 3)) -> np.ndarray:
        """Soft Gaussian blur to suppress fine speckle noise."""
        return cv2.GaussianBlur(gray, ksize, 0)

    @staticmethod
    def apply_clahe(gray: np.ndarray, clip_limit: float = 2.5, tile_grid_size: Tuple[int, int] = (8, 8)) -> np.ndarray:
        """
        Contrast Limited Adaptive Histogram Equalization (CLAHE).
        Crucial for aged documents where ink is unevenly faded or paper is discolored.
        """
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
        return clahe.apply(gray)

    @staticmethod
    def deskew(gray: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Detects image skew angle and rotates the image horizontally.
        Returns the deskewed image and detected angle in degrees.
        """
        # Invert colors so text is foreground white, paper is black
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        
        # Find all foreground pixels
        coords = np.column_stack(np.where(thresh > 0))
        if len(coords) < 100:
            return gray, 0.0

        angle = cv2.minAreaRect(coords)[-1]
        # In OpenCV minAreaRect, angle ranges between [-90, 0)
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        # Cap unrealistic angles (> 45 deg usually means landscape / wrong axis)
        if abs(angle) > 45 or abs(angle) < 0.2:
            return gray, 0.0

        h, w = gray.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        deskewed = cv2.warpAffine(
            gray,
            rotation_matrix,
            (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE
        )
        return deskewed, float(angle)

    @staticmethod
    def binarize_adaptive(gray: np.ndarray, block_size: int = 15, c: int = 8) -> np.ndarray:
        """Adaptive Gaussian thresholding for varying illumination and local shadows."""
        # Ensure block_size is odd and >= 3
        if block_size % 2 == 0:
            block_size += 1
        return cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, c
        )

    @staticmethod
    def binarize_otsu(gray: np.ndarray) -> np.ndarray:
        """Global Otsu binarization."""
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        return thresh

    def process(self, image_input: Union[str, Path, np.ndarray], preset: str = "standard") -> Dict[str, Any]:
        """
        Executes preprocessing pipeline according to selected preset.
        Returns a dictionary containing:
          - 'processed': Final preprocessed image (ready for OCR)
          - 'deskew_angle': Estimated skew correction angle
          - 'stages': Intermediate numpy arrays for inspection/visualization
        """
        raw_bgr = self.load_image(image_input)
        stages: Dict[str, np.ndarray] = {"raw": raw_bgr}

        if preset == "raw":
            return {"processed": raw_bgr, "deskew_angle": 0.0, "stages": stages}

        # 1. Resize/Upscale for consistent stroke width
        resized_bgr = self.resize(raw_bgr)
        stages["resized"] = resized_bgr

        # 2. Grayscale
        gray = self.to_grayscale(resized_bgr)
        stages["grayscale"] = gray

        # 3. Deskew
        deskewed_gray, angle = self.deskew(gray)
        stages["deskewed"] = deskewed_gray

        if preset == "deskew_only":
            # Return deskewed color or gray
            final_img = cv2.cvtColor(deskewed_gray, cv2.COLOR_GRAY2BGR)
            return {"processed": final_img, "deskew_angle": angle, "stages": stages}

        # 4. Denoise (Bilateral preserves stroke edges)
        denoised = self.denoise_bilateral(deskewed_gray)
        stages["denoised"] = denoised

        # 5. Contrast Enhancement (CLAHE)
        clahe_enhanced = self.apply_clahe(denoised, clip_limit=2.5)
        stages["clahe"] = clahe_enhanced

        if preset == "clahe_enhanced" or preset == "standard":
            # Modern deep learning OCR engines (PaddleOCR & TrOCR) work best on
            # high-contrast grayscale/color rather than harsh binary bitmasks.
            final_img = cv2.cvtColor(clahe_enhanced, cv2.COLOR_GRAY2BGR)
            return {"processed": final_img, "deskew_angle": angle, "stages": stages}

        elif preset == "denoise_adaptive":
            binary = self.binarize_adaptive(clahe_enhanced)
            stages["binary_adaptive"] = binary
            final_img = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
            return {"processed": final_img, "deskew_angle": angle, "stages": stages}

        elif preset == "otsu_binarized":
            binary = self.binarize_otsu(clahe_enhanced)
            stages["binary_otsu"] = binary
            final_img = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
            return {"processed": final_img, "deskew_angle": angle, "stages": stages}

        else:
            # Fallback to standard
            final_img = cv2.cvtColor(clahe_enhanced, cv2.COLOR_GRAY2BGR)
            return {"processed": final_img, "deskew_angle": angle, "stages": stages}
