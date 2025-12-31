from collections import Counter
from pathlib import Path
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import info.years as years

from pathlib import Path
from collections import Counter
import matplotlib.pyplot as plt

import datas

def createAbsoluteDiagram(input_file: str, name: str):
    print("Creating diagram for:", input_file, "as", name)
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

    tmima = datas.data.get(name, name)

    plt.xlabel("Ετος Εισαγωγής")
    plt.ylabel("Αιώνιοι Φοιτητές")
    plt.title(f"Αιώνιοι Φοιτητές ανά Έτος Εισαγωγής - {tmima}")
    plt.subplots_adjust(bottom=bottom)

    img_dir = Path("images")
    img_dir.mkdir(exist_ok=True)
    out_path = img_dir / f"{Path(input_file).stem}_absolute_chart.png"

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


BASE_BY_YEAR = {
    2015: years.year_2015,
    2016: years.year_2016,
    2017: years.year_2017,
    2018: years.year_2018,
}


def createPercentageDiagramFromFile(input_file: str, name: str, dept_key: str):
    """
    Self-contained:
    - reads extracted years from input_file (one per line: '2015' or '2015-16')
    - compares counts to BASE_BY_YEAR totals for dept_key for 2015-2018
    - creates and saves a percentage chart image
    Output file: images/<dept>_percentage_chart.png
    """
    print("Creating percentage diagram for:", input_file, "as", name, "dept:", dept_key)

    lines = [
        ln.strip()
        for ln in Path(input_file).read_text(encoding="utf-8").splitlines()
        if ln.strip()
    ]

    # Normalize: keep only the part before "-" (e.g. "2015-16" -> "2015")
    years = [ln.split("-", 1)[0].strip() for ln in lines]
    counts = Counter(years)

    year_labels = [2015, 2016, 2017, 2018]
    abs_counts = [int(counts.get(str(y), 0)) for y in year_labels]
    base_totals = [int(BASE_BY_YEAR[y].get(dept_key, 0)) for y in year_labels]

    # Percentages (skip years with base_total == 0)
    pct_values = [
        (abs_counts[i] / base_totals[i] * 100) if base_totals[i] > 0 else 0.0
        for i in range(len(year_labels))
    ]

    # If there is no available base data at all, skip image
    if sum(base_totals) == 0:
        print("No base totals available for dept_key:", dept_key, "- skipping percentage chart")
        return

    # layout decision
    n = len(year_labels)
    if n < 30:
        plt.figure(figsize=(16, 6))
        plt.xticks(fontsize=10)
        bottom = 0.15
    else:
        plt.figure(figsize=(20, 6))
        plt.margins(x=0)
        plt.xticks(rotation=90, fontsize=7)
        bottom = 0.35

    # plot
    x = [str(y) for y in year_labels]
    plt.bar(x, pct_values)

    tmima = datas.data.get(name, name)

    plt.xlabel("Ακαδημαϊκό Έτος (βάση: 2015-2018)")
    plt.ylabel("Ποσοστό (%)")
    plt.title(f"Ποσοστό Αιώνιων Φοιτητών ανά Έτος Εισαγωγής - {tmima}")
    plt.subplots_adjust(bottom=bottom)

    # annotation (totals)
    total_abs = sum(abs_counts)
    total_base = sum(base_totals)
    overall_pct = (total_abs / total_base * 100) if total_base > 0 else 0.0

    # plt.text(
    #     0.99, 0.95,
    #     f"Σύνολο: {total_abs}/{total_base} ({overall_pct:.2f}%)",
    #     transform=plt.gca().transAxes,
    #     ha="right",
    #     va="top",
    #     fontsize=10,
    #     bbox=dict(facecolor="white", alpha=0.8, edgecolor="black")
    # )

    # save
    img_dir = Path("images")
    img_dir.mkdir(exist_ok=True)

    out_path = img_dir / f"{dept_key.lower()}_percentage_chart.png"
    plt.savefig(out_path, dpi=200)
    plt.close()

def createDiagram(input_file: str, name: str):
    createAbsoluteDiagram(input_file, name)
    createPercentageDiagramFromFile(input_file, name, name)

if __name__ == "__main__":
    pass

    print("Diagrams module called directly")
    if len(sys.argv) != 3:
        print("Usage: py conv.py <input.pdf> <tmima>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    createDiagram(str(input_path), str(input_path.stem))