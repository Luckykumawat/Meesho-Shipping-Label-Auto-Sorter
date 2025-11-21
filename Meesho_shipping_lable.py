import os
import pypdf
import fitz  # PyMuPDF
from PIL import Image
import numpy as np
import easyocr

# ---- Strong Carrier Matching ----
CARRIER_KEYWORDS = {
    "VALMO PICKUP": ["VALMO", "VALMO PICK", "VALMO PICKUP"],
    "SHADOWFAX PICKUP": ["SHADOWFAX", "SHADOW FAX", "SHADOFAX", "SHADOWFAX PICKUP"],
    "DELHIVERY PICKUP": ["DELHIVERY", "DELHIVRY", "DELHVERY", "DELHIVERY PICKUP"],
    "XPRESS BEES": ["XPRESS", "XPRESSBEES", "XPRESS BEES", "XPRESS-BEES", "XPRESSBEE"]
}

def detect_carrier(text):
    text = text.upper()
    for carrier, keywords in CARRIER_KEYWORDS.items():
        for word in keywords:
            if word in text:
                return carrier
    return "UNKNOWN"


def sort_shipping_labels(input_pdf_path, output_pdf_path, use_easyocr=True):
    CARRIER_PRIORITY = {
        "VALMO PICKUP": 1,# Change the Delivery sevice according to your repuirement
        "SHADOWFAX PICKUP": 2,
        "DELHIVERY PICKUP": 3,
        "XPRESS BEES": 4,
        "UNKNOWN": 99
    }

    # Init EasyOCR
    reader = None
    if use_easyocr:
        reader = easyocr.Reader(['en'], gpu=False)

    # Load PDF
    doc = fitz.open(input_pdf_path)
    pdf_reader = pypdf.PdfReader(input_pdf_path)

    print(f"Total Pages: {doc.page_count}")

    carrier_pages = []
    unknown_count = 0

    # Loop each page
    for i in range(doc.page_count):
        page_number = i + 1
        page = doc[i]

        # Convert PDF page to image
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # OCR text extraction
        if use_easyocr:
            ocr_result = reader.readtext(np.array(img))
            text = " ".join([item[1] for item in ocr_result]) if ocr_result else ""
        else:
            import pytesseract
            text = pytesseract.image_to_string(img)

        # Detect courier partner
        found_carrier = detect_carrier(text)
        priority = CARRIER_PRIORITY.get(found_carrier, 99)

        print(f"[Page {page_number}] Carrier Detected: {found_carrier}")

        if found_carrier == "UNKNOWN":
            unknown_count += 1

        carrier_pages.append((priority, page_number, found_carrier, pdf_reader.pages[i]))

    # Sort by assigned priority
    carrier_pages.sort(key=lambda x: x[0])

    # Write new sorted PDF
    writer = pypdf.PdfWriter()
    for _, _, _, page in carrier_pages:
        writer.add_page(page)

    with open(output_pdf_path, "wb") as f:
        writer.write(f)

    print("\n✓ Sorting Complete!")
    print(f"✓ Saved at: {output_pdf_path}")
    print(f"⚠ Unknown Pages: {unknown_count}")


# Run
INPUT_FILENAME = "INPUT_FILE_PATH.pdf"
OUTPUT_FILENAME = "OUTPUT_FILE_PATH.pdf"

sort_shipping_labels(INPUT_FILENAME, OUTPUT_FILENAME)
