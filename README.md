# Meesho-Shipping-Label-Auto-Sorter
This script automatically reads, detects, and rearranges Meesho shipping labels based on their carrier partners using OCR. It works for PDFs containing multiple labels, extracts text from each page, identifies the courier partner, and sorts the pages into a clean, ordered PDF.
📦 Supports automatic sorting for:

Valmo Pickup

Shadowfax Pickup

Delhivery Pickup

XpressBees

Unknown Carrier (fallback)

This tool is ideal for Meesho sellers who receive shipping labels in bulk and want them arranged courier-wise for faster packaging & dispatch.

⭐ Why This Tool Exists

Meesho sellers often download 100–500 shipping labels at once.
These labels come mixed, which makes sorting them manually extremely time-consuming.

Manually sorting:

❌ Takes 30–60 minutes per batch

❌ High chance of mistakes

❌ Difficult during high-volume orders

This script:

✔ Automatically detects the courier partner using OCR

✔ Sorts labels in this order: VALMO → SHADOWFAX → DELHIVERY → XPRESSBEES → UNKNOWN

✔ Generates a new clean PDF ready for printing

✔ Saves 90% time during packaging

🔥 Key Features
🧠 Smart Carrier Detection (OCR-based)

Uses EasyOCR to recognize text even with spelling mistakes:

SHADOWFAX

SHADOW FAX

SHADOFAX

DELHIVERY

DELHIVRY

XPRESS BEES

XPRESSBEES

🖥 Works on CPU & GPU

CPU: Works well

GPU: ⚡ Runs 10x faster if you have a supported NVIDIA GPU

📄 PDF Sorting

Opens PDF → Reads each page → Detects carrier → Reorders → Saves new PDF

📦 Extremely Helpful for Meesho Sellers

Perfect for:

Warehouse teams

Packaging boys

Resellers handling bulk orders

Automated pickup arrangement

🛠️ Installation
1️⃣ Clone the Repository
git clone https://github.com/YOUR_USERNAME/meesho-label-sorter.git
cd meesho-label-sorter

2️⃣ Create Virtual Environment
python3 -m venv .venv
source .venv/bin/activate

3️⃣ Install Required Libraries
pip install pymupdf pypdf pillow easyocr numpy


👉 macOS users also need Poppler only if using pdf2image (not required here).

▶️ Usage

Place your Meesho label PDF inside your project folder.

Example:

meesho_lables/
   |— input_labels.pdf


Run the script:

python meesho_label_sorter.py

GPU Advantage (Important)

EasyOCR supports CUDA (NVIDIA GPUs).

If running on GPU:

OCR becomes 10–15x faster

Sorting 500 labels takes seconds, not minutes

Major speed improvement for warehouse automation workflows

To enable GPU:

reader = easyocr.Reader(['en'], gpu=True)

💡 Example: Why This Saves Time
Labels Count	Manual Sorting	Script Sorting
50 labels	15–20 min	8 seconds
150 labels	40–60 min	20 seconds
300+ labels	1–2 hours	< 1 minute
📚 File Structure Example
📁 meesho-label-sorter
│
├── meesho_label_sorter.py
├── quicklabelcrop-xxxxxxxxx.pdf   # Input
└── Sorted_Labels_By_Carrier.pdf   # Output

The output will be created as:

Sorted_Labels_By_Carrier.pdf
