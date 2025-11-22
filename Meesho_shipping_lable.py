import os
import pypdf
import fitz  # PyMuPDF
from PIL import Image
import numpy as np
import easyocr
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


# ----------------------------
# Strong Carrier Keyword Detection
# ----------------------------
CARRIER_KEYWORDS = {
    "VALMO PICKUP": ["VALMO", "VALMO PICK", "VALMO PICKUP"],
    "SHADOWFAX PICKUP": ["SHADOWFAX", "SHADOW FAX", "SHADOFAX", "SHADOWFAX PICKUP"],
    "DELHIVERY PICKUP": ["DELHIVERY", "DELHIVRY", "DELHVERY", "DELHIVERY PICKUP"],
    "XPRESS BEES": ["XPRESS", "XPRESSBEES", "XPRESS BEES", "XPRESS-BEES", "XPRESSBEE"]
}

def detect_carrier(text):
    text = text.upper()
    for carrier, words in CARRIER_KEYWORDS.items():
        for w in words:
            if w in text:
                return carrier
    return "UNKNOWN"


# ----------------------------
# Main Sorting Function
# ----------------------------
def sort_shipping_labels(input_pdf_path, output_pdf_path, progress_label):

    CARRIER_PRIORITY = {
        "VALMO PICKUP": 1,
        "SHADOWFAX PICKUP": 2,
        "DELHIVERY PICKUP": 3,
        "XPRESS BEES": 4,
        "UNKNOWN": 99
    }

    # Init OCR
    reader = easyocr.Reader(['en'], gpu=False)

    # Load PDF
    doc = fitz.open(input_pdf_path)
    pdf_reader = pypdf.PdfReader(input_pdf_path)

    carrier_pages = []
    unknown_count = 0

    total_pages = doc.page_count

    # Loop pages
    for i in range(total_pages):
        page_num = i + 1
        progress_label.config(text=f"Processing Page {page_num}/{total_pages}...")
        progress_label.update()

        page = doc[i]

        # Convert to image
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # OCR
        ocr_result = reader.readtext(np.array(img))
        text = " ".join([item[1] for item in ocr_result]) if ocr_result else ""

        # Carrier detection
        carrier = detect_carrier(text)
        priority = CARRIER_PRIORITY.get(carrier, 99)

        carrier_pages.append((priority, page_num, carrier, pdf_reader.pages[i]))

    # Sort pages
    carrier_pages.sort(key=lambda x: x[0])

    # Write output
    writer = pypdf.PdfWriter()
    for _, _, _, page in carrier_pages:
        writer.add_page(page)

    with open(output_pdf_path, "wb") as f:
        writer.write(f)

    progress_label.config(text=f"Completed! Saved to: {output_pdf_path}")


# ----------------------------
# GUI Application
# ----------------------------
def open_file():
    filepath = filedialog.askopenfilename(
        filetypes=[("PDF Files", "*.pdf")]
    )
    if filepath:
        input_path_var.set(filepath)


def run_sorting():
    input_pdf = input_path_var.get().strip()

    if input_pdf == "":
        messagebox.showerror("Error", "Please select an input PDF file!")
        return

    output_pdf = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title="Save Sorted PDF As"
    )

    if output_pdf == "":
        return

    progress_label.config(text="Starting OCR...")
    progress_label.update()

    try:
        sort_shipping_labels(input_pdf, output_pdf, progress_label)
        messagebox.showinfo("Success", f"Sorted PDF saved successfully:\n{output_pdf}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# ----------------------------
# Tkinter UI
# ----------------------------
root = tk.Tk()
root.title("Shipping Label Sorter - Meesho Automation")
root.geometry("600x300")
root.resizable(False, False)

title = tk.Label(root, text="📦 Shipping Label Sorting Automation", font=("Arial", 16, "bold"))
title.pack(pady=10)

instruction = tk.Label(root, text="Upload a Meesho shipping label PDF to auto-sort by courier partner.")
instruction.pack(pady=5)

# PDF Path Input
input_path_var = tk.StringVar()

path_frame = tk.Frame(root)
path_frame.pack(pady=10)

path_entry = tk.Entry(path_frame, textvariable=input_path_var, width=50)
path_entry.pack(side="left", padx=5)

browse_btn = ttk.Button(path_frame, text="Browse", command=open_file)
browse_btn.pack(side="left")

# Run Button
run_btn = ttk.Button(root, text="Sort Labels", command=run_sorting)
run_btn.pack(pady=15)

# Progress Label
progress_label = tk.Label(root, text="", fg="blue")
progress_label.pack(pady=10)

root.mainloop()
