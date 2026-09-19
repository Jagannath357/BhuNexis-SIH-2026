import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
SAMPLES_DIR = BASE_DIR / "samples"
OUTPUT_DIR = BASE_DIR / "output"

# Ensure output and sample directories exist
SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Preprocessing Settings
DEFAULT_PREPROCESS_PRESET = "standard"
PREPROCESS_PRESETS = [
    "raw",                 # Original image untouched
    "standard",            # Resize + Grayscale + Bilateral Filter + CLAHE
    "clahe_enhanced",      # Grayscale + Strong CLAHE for faint ink
    "denoise_adaptive",    # Bilateral Denoising + Adaptive Gaussian Threshold
    "otsu_binarized",      # Bilateral Denoising + Otsu Binarization
    "deskew_only"          # Orientation/Skew correction only
]

# Primary Engine (PaddleOCR) Settings
# PP-OCRv5 / PP-OCRv4 English mobile recognition
PADDLE_LANG = "en"
PADDLE_USE_ANGLE_CLS = True
PADDLE_CONFIDENCE_THRESHOLD = 0.60

# Fallback Engine (Microsoft TrOCR) Settings
TROCR_BASE_MODEL = "microsoft/trocr-base-handwritten"
TROCR_SMALL_MODEL = "microsoft/trocr-small-handwritten"
DEFAULT_TROCR_MODEL = TROCR_BASE_MODEL

# Confidence Fallback Threshold
# If Primary engine average confidence < FALLBACK_THRESHOLD, switch to TrOCR
AUTO_FALLBACK_CONFIDENCE = 0.60

# Default Standard JSON Output Language
DEFAULT_LANGUAGE = "English"
