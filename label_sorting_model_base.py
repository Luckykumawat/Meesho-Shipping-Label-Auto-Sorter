import pypdf
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


# -------------------------------------------------
# MODEL PRIORITY (SORT ORDER)
# -------------------------------------------------
MODEL_PRIORITY = {

    # ================= MOTO =================
    "MOTO G67 5G": 1,
    "MOTO G57 5G": 2,
    "MOTO G57 POWER 5G": 3,
    "MOTO G67 POWER 5G": 4,
    "MOTO EDGE 60 FUSION 5G": 5,
    "MOTO G31": 6,
    "MOTO G35 5G": 7,
    "MOTO G45 5G": 8,
    "MOTO G54 5G": 9,
    "MOTO G62 5G": 10,
    "MOTO E40": 11,
    "MOTO E30": 12,

    # ================= REDMI =================
    "REDMI A4 5G": 13,
    "REDMI A5": 14,
    "REDMI 9 POWER": 15,
    "REDMI 12 4G": 16,
    "REDMI 14C 5G": 17,
    "REDMI NOTE 6 PRO": 18,
    "REDMI NOTE 14 5G": 19,
    "REDMI NOTE 14 PRO 5G": 20,

    # ================= POCO =================
    "POCO F1": 21,
    "POCO C75 5G": 22,
    "POCO M7 5G": 23,
    "POCO M7 PRO 5G": 24,

    # ================= OPPO =================
    "OPPO F11": 25,
    "OPPO F31 5G": 26,
    "OPPO F31 PRO 5G": 27,
    "OPPO RENO 2Z": 28,
    "OPPO K10 5G": 29,
    "OPPO K13X 5G": 30,
    "OPPO A3S": 31,
    "OPPO A3 5G": 32,
    "OPPO A3 PRO 5G": 33,
    "OPPO A3X 5G": 34,
    "OPPO A5 5G": 35,
    "OPPO A5X 5G": 36,
    "OPPO A17": 37,
    "OPPO A31": 38,
    "OPPO A57": 39,
    "OPPO A57E": 40,
    "OPPO A57 5G": 41,
    "OPPO A59 5G": 42,
    "OPPO A76": 43,
    "OPPO A77": 44,
    "OPPO A77S": 45,
    "OPPO A78 5G": 46,
    "OPPO A93 4G": 47,

    # ================= REALME =================
    "REALME 11": 48,
    "REALME 11X 5G": 49,
    "REALME 14X 5G": 50,
    "REALME C30": 51,
    "REALME C30S": 52,
    "REALME C31": 53,
    "REALME NARZO 30A": 54,
    "REALME NARZO 50I": 55,
    "REALME NARZO 50I PRIME": 56,
    "REALME NARZO 60X 5G": 57,
    "REALME NARZO 80 LITE 5G": 58,
    "REALME NARZO 80X 5G": 59,
    "REALME NARZO 80 PRO 5G": 60,
    "REALME P3 5G": 61,
    "REALME P3X 5G": 62,
    "REALME GT 7T 5G": 63,

    # ================= SAMSUNG =================
    "SAMSUNG GALAXY A31": 64,
    "SAMSUNG F13": 65,
    "SAMSUNG M13": 66,
    "SAMSUNG GALAXY J8": 67,
    "SAMSUNG GALAXY M31S": 68,
    "SAMSUNG M36 5G": 69,
    "SAMSUNG GALAXY S20 FE": 70,

    # ================= VIVO =================
    "VIVO Y16": 71,
    "VIVO Y19 5G": 72,
    "VIVO T1 PRO": 73,
    "VIVO T4X 5G": 74,
    "VIVO V40 PRO 5G": 75,
    "VIVO V50E 5G": 76,
    "VIVO V60E 5G": 77,

    # ================= UNKNOWN =================
    "UNKNOWN MODEL": 999
}


# -------------------------------------------------
# MODEL DETECTION
# -------------------------------------------------
def detect_model(text):
    text = text.upper()
    for model in MODEL_PRIORITY:
        if model != "UNKNOWN MODEL" and model in text:
            return model
    return "UNKNOWN MODEL"


# -------------------------------------------------
# MAIN SORT FUNCTION
# -------------------------------------------------
def sort_shipping_labels(input_pdf_path, output_pdf_path, progress_label):

    doc = fitz.open(input_pdf_path)
    pdf_reader = pypdf.PdfReader(input_pdf_path)

    model_pages = []
    total_pages = doc.page_count

    for i in range(total_pages):
        page_num = i + 1
        progress_label.config(text=f"Processing Page {page_num}/{total_pages}...")
        progress_label.update()

        page = doc[i]
        text = page.get_text("text")  # FAST extraction

        model = detect_model(text)
        priority = MODEL_PRIORITY.get(model, 999)

        model_pages.append((priority, page_num, model, pdf_reader.pages[i]))

    model_pages.sort(key=lambda x: x[0])

    writer = pypdf.PdfWriter()
    for _, _, _, page in model_pages:
        writer.add_page(page)

    with open(output_pdf_path, "wb") as f:
        writer.write(f)

    progress_label.config(text=f"Completed! Saved to: {output_pdf_path}")


# -------------------------------------------------
# UI FUNCTIONS
# -------------------------------------------------
def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if filepath:
        input_path_var.set(filepath)


def run_sorting():
    input_pdf = input_path_var.get().strip()
    if not input_pdf:
        messagebox.showerror("Error", "Please select an input PDF file!")
        return

    output_pdf = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")],
        title="Save Sorted PDF As"
    )

    if not output_pdf:
        return

    progress_label.config(text="Sorting pages...")
    progress_label.update()

    try:
        sort_shipping_labels(input_pdf, output_pdf, progress_label)
        messagebox.showinfo("Success", "PDF sorted successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# -------------------------------------------------
# TKINTER UI
# -------------------------------------------------
root = tk.Tk()
root.title("📦 Meesho Shipping Label Sorter (Model Based)")
root.geometry("600x300")
root.resizable(False, False)

title = tk.Label(root, text="📦 Meesho Shipping Label Sorting Automation",
                 font=("Arial", 16, "bold"))
title.pack(pady=10)

instruction = tk.Label(
    root,
    text="Upload Meesho shipping label PDF to auto-sort by Mobile Model (SKU)."
)
instruction.pack(pady=5)

input_path_var = tk.StringVar()

path_frame = tk.Frame(root)
path_frame.pack(pady=10)

path_entry = tk.Entry(path_frame, textvariable=input_path_var, width=50)
path_entry.pack(side="left", padx=5)

browse_btn = ttk.Button(path_frame, text="Browse", command=open_file)
browse_btn.pack(side="left")

run_btn = ttk.Button(root, text="Sort Labels", command=run_sorting)
run_btn.pack(pady=15)

progress_label = tk.Label(root, text="", fg="blue")
progress_label.pack(pady=10)

root.mainloop()
