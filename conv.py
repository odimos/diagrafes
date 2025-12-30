from docx import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph
from pathlib import Path
import sys

TARGET_COL = 3  # 0-based index

def iter_blocks(parent):
    for child in parent.element.body.iterchildren():
        if isinstance(child, CT_P):
            continue
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

def cell_text(cell):
    txt = " ".join(p.text.strip() for p in cell.paragraphs if p.text.strip())
    return " ".join(txt.split())

def docx_to_txt(docx_path, txt_path):
    doc = Document(docx_path)
    out = []

    for table in iter_blocks(doc):
        for row in table.rows:
            if TARGET_COL < len(row.cells):
                value = cell_text(row.cells[TARGET_COL])
                if value:
                    out.append(value)

    Path(txt_path).write_text("\n".join(out), encoding="utf-8")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: py conv.py <input.docx>")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    output_path = input_path.with_name(
        f"{input_path.stem}_output.txt"
    )

    docx_to_txt(str(input_path), str(output_path))