from pathlib import Path


import csv

tables_dir = Path("tables")
merged = []

for input_path in tables_dir.glob("*.csv"):
    try:
        with input_path.open(encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0].strip():
                    merged.append(row[0].strip())

        print(f"OK: {input_path.name}")

    except Exception as e:
        print(f"SKIPPED: {input_path.name} -> {e}")
        


# write merged file
# write merged file inside tables/
out_file = tables_dir / "merged.csv"

with out_file.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for value in merged:
        writer.writerow([value])

print("Total values merged:", len(merged))
