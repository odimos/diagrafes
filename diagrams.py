from collections import Counter
from pathlib import Path
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from pathlib import Path
from collections import Counter
import matplotlib.pyplot as plt

def createDiagram(input_file: str):
    numbers = [
        line.strip()
        for line in Path(input_file).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    counts = Counter(numbers)
    labels = sorted(counts.keys(), key=lambda x: float(x))
    values = [counts[k] for k in labels]

    n = len(labels)

    # layout decision
    if n < 30:
        plt.figure(figsize=(16, 6))
        plt.bar(labels, values)
        plt.xticks(fontsize=10)
        bottom = 0.15
    else:
        plt.figure(figsize=(20, 6))
        plt.bar(labels, values)
        plt.margins(x=0)
        plt.xticks(rotation=90, fontsize=7)
        bottom = 0.35

    plt.xlabel("Ετος Εισαγωγής")
    plt.ylabel("Αιώνιοι Φοιτητές")
    plt.title("Αιώνιοι Φοιτητές ανά Έτος Εισαγωγής")
    plt.subplots_adjust(bottom=bottom)

    img_dir = Path("images")
    img_dir.mkdir(exist_ok=True)
    out_path = img_dir / f"{Path(input_file).stem}_frequency_chart.png"

    total = sum(values)

    plt.text(
        0.99, 0.95,
        f"Σύνολο: {total}",
        transform=plt.gca().transAxes,
        ha="right",
        va="top",
        fontsize=10,
        bbox=dict(facecolor="white", alpha=0.8, edgecolor="black")
    )


    plt.savefig(out_path, dpi=200)
    plt.close()

if __name__ == "__main__":

    print("Diagrams module called directly")
    if len(sys.argv) != 2:
        print("Usage: py conv.py <input.pdf>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    createDiagram(str(input_path))