import sys
from pathlib import Path
from diagrams import createDiagram


tables_dir = Path("tables")

for input_path in tables_dir.glob("*_output.csv"):
    print("Processing:", input_path)
    try:
        createDiagram(str(input_path))
    except Exception as e:
        print("Failed to create diagram for", input_path, "due to", e)
