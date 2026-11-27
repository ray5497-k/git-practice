import csv
from pathlib import Path


def revenue_from_csv(path: str | Path) -> int:
    with open(path, encoding="utf-8", newline="") as file:
        total = 0
        for row in csv.DictReader(file):
            total += int(row["price"]) * int(row["quantity"])
        return total
