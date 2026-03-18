from __future__ import annotations

import argparse
import csv
import statistics
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence

from tabulate import tabulate


@dataclass(frozen=True)
class Row:
    student: str
    coffee_spent: float


def _read_rows(paths: Iterable[Path]) -> list[Row]:
    rows: list[Row] = []
    for path in paths:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                continue
            required = {"student", "coffee_spent"}
            missing = required.difference({h.strip() for h in reader.fieldnames})
            if missing:
                raise ValueError(f"Missing columns in {path}: {sorted(missing)}")

            for r in reader:
                student = (r.get("student") or "").strip()
                if not student:
                    continue
                coffee_raw = (r.get("coffee_spent") or "").strip()
                if coffee_raw == "":
                    continue
                try:
                    coffee = float(coffee_raw)
                except ValueError as e:
                    raise ValueError(f"Invalid coffee_spent value {coffee_raw!r} in {path}") from e
                rows.append(Row(student=student, coffee_spent=coffee))
    return rows


def report_median_coffee(rows: Sequence[Row]) -> list[tuple[str, float]]:
    by_student: dict[str, list[float]] = defaultdict(list)
    for r in rows:
        by_student[r.student].append(r.coffee_spent)

    result: list[tuple[str, float]] = [
        (student, float(statistics.median(values))) for student, values in by_student.items() if values
    ]
    result.sort(key=lambda x: (-x[1], x[0]))
    return result


ReportFn = Callable[[Sequence[Row]], list[tuple[str, float]]]


REPORTS: dict[str, ReportFn] = {
    "median-coffee": report_median_coffee,
}


def build_table(report_rows: Sequence[tuple[str, float]]) -> str:
    table_data = [(student, median) for student, median in report_rows]
    return tabulate(table_data, headers=["student", "median_coffee_spent"], tablefmt="github")


def parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CSV exam preparation reports")
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Paths to CSV files",
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=sorted(REPORTS.keys()),
        help="Report name",
    )
    return parser.parse_args(list(argv) if argv is not None else None)


def main(argv: Sequence[str] | None = None) -> int:
    if sys.platform.startswith("win"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    args = parse_args(argv)
    paths = [Path(p) for p in args.files]
    rows = _read_rows(paths)
    report_fn = REPORTS[args.report]
    report_rows = report_fn(rows)
    print(build_table(report_rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

