import pdfplumber
import sys
from pathlib import Path

TARGET_COL = 3  # 4th column (0-based)

def extract_third_column(pdf_path, output_txt):
    out_lines = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for table in (page.extract_tables() or []):
                if not table or len(table) < 2:
                    continue  # no data rows

                # skip header row
                for row in table[1:]:
                    if not row or len(row) <= TARGET_COL:
                        continue

                    val = (row[TARGET_COL] or "").strip()
                    if val:
                        out_lines.append(val)

    Path(output_txt).write_text("\n".join(out_lines), encoding="utf-8")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: py conv.py <input.pdf>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    output_path = input_path.with_name(f"{input_path.stem}_col4.csv")
    extract_third_column(str(input_path), str(output_path))
