import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
from typing import List, Dict, Any


def create_parchment_background(width: int, height: int) -> Image.Image:
    """Generates an aged, slightly textured yellowish paper background."""
    # Base aged paper tone (RGB: ~245, 238, 220)
    base = np.full((height, width, 3), [220, 238, 245], dtype=np.uint8)

    # Add subtle random grain/noise
    noise = np.random.normal(0, 8, (height, width, 3)).astype(np.int16)
    textured = np.clip(base.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    # Add faint vignette (darker edges)
    y, x = np.ogrid[:height, :width]
    cx, cy = width / 2, height / 2
    dist_from_center = np.sqrt((x - cx)**2 + (y - cy)**2)
    max_dist = np.sqrt(cx**2 + cy**2)
    vignette = 1.0 - 0.15 * (dist_from_center / max_dist) ** 2
    vignette = np.stack([vignette] * 3, axis=-1)
    textured = (textured * vignette).astype(np.uint8)

    # Convert BGR back to RGB PIL Image
    return Image.fromarray(cv2.cvtColor(textured, cv2.COLOR_BGR2RGB))


def get_handwriting_font(size: int = 28) -> ImageFont.ImageFont:
    """Finds a cursive/handwriting font on Windows or falls back to system font."""
    candidates = [
        "C:\\Windows\\Fonts\\segoesc.ttf",   # Segoe Script
        "C:\\Windows\\Fonts\\Inkfree.ttf",   # Ink Free
        "C:\\Windows\\Fonts\\BRUSHSCI.TTF",  # Brush Script
        "C:\\Windows\\Fonts\\comic.ttf",     # Comic Sans (handwriting look)
        "C:\\Windows\\Fonts\\calibri.ttf",   # Calibri fallback
        "C:\\Windows\\Fonts\\arial.ttf"      # Arial fallback
    ]
    for font_path in candidates:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size=size)
            except Exception:
                continue
    return ImageFont.load_default()


def get_bold_font(size: int = 32) -> ImageFont.ImageFont:
    candidates = [
        "C:\\Windows\\Fonts\\segoescb.ttf",
        "C:\\Windows\\Fonts\\calibrib.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf"
    ]
    for font_path in candidates:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size=size)
            except Exception:
                continue
    return ImageFont.load_default()


def generate_sample_documents(output_dir: Path) -> List[Path]:
    """
    Generates 3 realistic synthetic handwritten English land-record documents
    for immediate prototype testing and benchmarking.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_files = []

    samples_data = [
        {
            "filename": "DOC_001.jpg",
            "doc_id": "DOC_001",
            "title": "GOVERNMENT OF ODISHA - REVENUE & DISASTER MANAGEMENT",
            "subtitle": "RECORD OF RIGHTS (ROR) / KHATIAN",
            "lines": [
                "Name of Pattadar: Ramesh Chandra Sahu",
                "Father's Name: Late Kailash Chandra Sahu",
                "Khata No: 45",
                "Plot No: 128/3",
                "Area: 0.240 Acre",
                "Village: Khandagiri",
                "Tehsil: Bhubaneswar",
                "District: Khordha"
            ],
            "skew_angle": 0.0
        },
        {
            "filename": "sample_land_record_1.jpg",
            "doc_id": "LR_001",
            "title": "RECORD OF RIGHTS (KHATIYAN EXTRACT)",
            "lines": [
                "Document ID: LR_001",
                "District: Angul       Tahasil: Banarpal",
                "Village: Nuahata      Khata No: 342",
                "Plot No: 124/3",
                "Owner: Ramesh Kumar Mohapatra",
                "Father: Jagannath Mohapatra",
                "Land Classification: Sarada-II",
                "Area: 0.85 Acre",
                "Annual Rent: Rs 18.50",
                "Date of Entry: 14-04-1992",
                "Signature of Tahasildar: R.K. Das"
            ],
            "skew_angle": 1.2
        },
        {
            "filename": "sample_land_record_2.jpg",
            "doc_id": "LR_002",
            "title": "LAND MUTATION ORDER CERTIFICATE",
            "lines": [
                "Document ID: LR_002",
                "Mutation Case No: 412/2005",
                "District: Cuttack     Tahasil: Salipur",
                "Village: Rampur       Khata No: 88",
                "Plot No: 405/2",
                "Owner: Sunita Devi",
                "Vendor: Birendra Singh",
                "Land Type: Homestead / Gharabari",
                "Area: 0.42 Acre",
                "Mutation Fee Paid: Rs 150",
                "Date: 22-09-2005",
                "Verified by: Revenue Inspector"
            ],
            "skew_angle": -1.5
        },
        {
            "filename": "sample_land_record_3.jpg",
            "doc_id": "LR_003",
            "title": "LAND POSSESSION & BOUNDARY SLIP",
            "lines": [
                "Document ID: LR_003",
                "Certificate No: POS-7891",
                "Village: Madhuban     Khata No: 115",
                "Plot No: 890/1",
                "Possessor: Arvind Narayan",
                "Area: 1.60 Acre",
                "North Boundary: Public Village Road",
                "South Boundary: Irrigation Canal",
                "East Boundary: Land of K. Sharma",
                "Date of Inspection: 05-11-2012",
                "Officer: Assistant Settlement Officer"
            ],
            "skew_angle": 1.8
        }
    ]

    for data in samples_data:
        width, height = 1200, 1500
        img = create_parchment_background(width, height)
        draw = ImageDraw.Draw(img)

        title_font = get_bold_font(28 if len(data["title"]) > 35 else 34)
        body_font = get_handwriting_font(30)

        # Draw Header Border
        draw.rectangle([(50, 50), (width - 50, height - 50)], outline=(110, 95, 75), width=3)
        draw.rectangle([(56, 56), (width - 56, height - 56)], outline=(140, 125, 105), width=1)

        # Draw Title
        draw.text((80 if len(data["title"]) > 40 else 120, 85), data["title"], fill=(35, 25, 15), font=title_font)
        
        if "subtitle" in data:
            draw.text((120, 130), data["subtitle"], fill=(45, 35, 25), font=get_bold_font(26))
            draw.line([(80, 170), (width - 80, 170)], fill=(120, 90, 60), width=2)
            y_pos = 205
        else:
            draw.line([(120, 135), (width - 120, 135)], fill=(120, 90, 60), width=2)
            y_pos = 180
        for line in data["lines"]:
            jitter = np.random.randint(-2, 3)
            # Ink color variations (faded blue-black or blackish fountain pen)
            ink_tone = (
                np.random.randint(20, 45),
                np.random.randint(25, 50),
                np.random.randint(40, 75)
            )
            draw.text((120, y_pos + jitter), line, fill=ink_tone, font=body_font)
            y_pos += 80

        # Draw an official simulated circular stamp watermark
        stamp_x, stamp_y = width - 260, height - 280
        draw.ellipse([(stamp_x, stamp_y), (stamp_x + 180, stamp_y + 180)], outline=(140, 40, 40, 160), width=3)
        draw.text((stamp_x + 35, stamp_y + 75), "SEAL & VERIFIED", fill=(140, 40, 40), font=get_bold_font(16))

        # Apply slight blur to simulate real scanner optics
        img = img.filter(ImageFilter.GaussianBlur(radius=0.4))

        # Apply Skew / Tilt
        if abs(data["skew_angle"]) > 0.1:
            img = img.rotate(data["skew_angle"], resample=Image.BICUBIC, expand=False, fillcolor=(235, 230, 215))

        out_path = output_dir / data["filename"]
        img.save(str(out_path), "JPEG", quality=92)
        generated_files.append(out_path)

    return generated_files


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from config import SAMPLES_DIR
    files = generate_sample_documents(SAMPLES_DIR)
    print(f"Generated {len(files)} sample land records:")
    for f in files:
        print(f"  - {f}")

