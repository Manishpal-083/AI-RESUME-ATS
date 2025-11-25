import pdfplumber
import pytesseract
from PIL import Image, UnidentifiedImageError
import tempfile
import fitz  # PyMuPDF
import os

def extract_text(file_path: str) -> str:
    text = ""

    ext = os.path.splitext(file_path)[1].lower()

    # 1️⃣ Try PDF path
    if ext == ".pdf":
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    text += page_text
        except Exception:
            pass

        # if PDF seems scanned / empty
        if len(text.strip()) < 20:
            text += extract_text_from_image_pdf(file_path)
        return text

    # 2️⃣ Otherwise, treat as image (png/jpg/jpeg)
    try:
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
    except UnidentifiedImageError:
        # not a valid image
        return ""

    return text


def extract_text_from_image_pdf(file_path: str) -> str:
    """Render each page of PDF as image, then run OCR."""
    out_text = ""
    doc = fitz.open(file_path)
    for page in doc:
        pix = page.get_pixmap()
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            pix.save(tmp.name)
            img = Image.open(tmp.name)
            out_text += pytesseract.image_to_string(img)
    return out_text
