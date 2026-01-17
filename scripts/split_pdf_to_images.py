"""
Split PDF documents into individual page images
"""
from pathlib import Path
from PIL import Image
import sys

# Requires: pip install pdf2image poppler
try:
    from pdf2image import convert_from_path
except ImportError:
    print("Please install: pip install pdf2image")
    print("Also requires poppler: https://github.com/oschwartz10612/poppler-windows/releases/")
    sys.exit(1)


def split_pdf(pdf_path: Path, output_dir: Path, dpi: int = 300):
    """Convert PDF pages to images"""
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    images = convert_from_path(pdf_path, dpi=dpi)
    
    for i, image in enumerate(images, start=1):
        output_path = output_dir / f"{pdf_path.stem}_page_{i:03d}.png"
        image.save(output_path, "PNG")
        print(f"Saved: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python split_pdf_to_images.py <pdf_file>")
        sys.exit(1)
    
    pdf_file = Path(sys.argv[1])
    output_directory = Path("data/raw_uploads") / pdf_file.stem
    
    split_pdf(pdf_file, output_directory)
