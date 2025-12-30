import pdfplumber
import pandas as pd
import sys
from pathlib import Path

from pdfreader import extract_third_column

pdfs = [
    "PLIROFORIKI.pdf",
    "STATISTIKI.pdf",
    "DET.pdf",
    "DEOS.pdf",
    "LOXRI.pdf",
    "MARKETING.pdf",
    "OIKONOMIKIS_EPISTIMIS.pdf",   
    "ODE.pdf"
]

out_dir = Path("tables")
out_dir.mkdir(exist_ok=True)

for pdf in pdfs:
    input_path = Path(pdf)

    if input_path.exists():
        output_path = out_dir / f"{input_path.stem}_output.csv"
        extract_third_column(str(input_path), str(output_path))
