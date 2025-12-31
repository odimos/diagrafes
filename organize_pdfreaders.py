import pdfplumber
import pandas as pd
import sys
from pathlib import Path

from pdfreader import extract_third_column


out_dir = Path("tables")
out_dir.mkdir(exist_ok=True)

pdfs_dir = Path("pdfs")

for input_path in pdfs_dir.glob("*.pdf"):
    print("Processing:", input_path)
    try:
        output_path = out_dir / f"{input_path.stem}.csv"
        extract_third_column(str(input_path), str(output_path))
    except Exception as e:
        print("Failed to create .csv for", input_path, "due to", e)

