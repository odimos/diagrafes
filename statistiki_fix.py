from pathlib import Path

file_path = Path("tables/STATISTIKI.csv")  # change if needed

lines = file_path.read_text(encoding="utf-8").splitlines()

cleaned = [
    line.split("-", 1)[0].strip()
    for line in lines
    if line.strip()
]

file_path.write_text("\n".join(cleaned), encoding="utf-8")
