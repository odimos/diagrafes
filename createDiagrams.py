import sys
from pathlib import Path
from diagrams import createDiagram


tables_dir = Path("tables")

for input_path in tables_dir.glob("*.csv"):
    print("Processing:", input_path)
    try:
        createDiagram(str(input_path), str(input_path.stem))
    except Exception as e:
        print("Failed to create diagram for", input_path, "due to", e)
