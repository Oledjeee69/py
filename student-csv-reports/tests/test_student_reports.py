import textwrap
from pathlib import Path

import pytest

from student_reports import Row, _read_rows, build_table, report_median_coffee


def _write_csv(tmp_path: Path, name: str, content: str) -> Path:
    p = tmp_path / name
    p.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    return p


def test_report_median_coffee_across_multiple_files(tmp_path: Path) -> None:
    f1 = _write_csv(
        tmp_path,
        "a.csv",
        """
        student,date,coffee_spent,sleep_hours,study_hours,mood,exam
        Алексей Смирнов,2024-06-01,450,4.5,12,норм,Математика
        Алексей Смирнов,2024-06-02,500,4.0,14,устал,Математика
        Дарья Петрова,2024-06-01,200,7.0,6,отл,Математика
        """,
    )
    f2 = _write_csv(
        tmp_path,
        "b.csv",
        """
        student,date,coffee_spent,sleep_hours,study_hours,mood,exam
        Алексей Смирнов,2024-06-03,550,3.5,16,зомби,Математика
        Дарья Петрова,2024-06-02,250,6.5,8,норм,Математика
        Дарья Петрова,2024-06-03,300,6.0,9,норм,Математика
        """,
    )

    rows = _read_rows([f1, f2])
    report = report_median_coffee(rows)

    assert report == [
        ("Алексей Смирнов", 500.0),
        ("Дарья Петрова", 250.0),
    ]


def test_sorting_descending_then_name() -> None:
    rows = [
        Row(student="B", coffee_spent=10),
        Row(student="A", coffee_spent=10),
        Row(student="C", coffee_spent=5),
    ]
    report = report_median_coffee(rows)
    assert report == [("A", 10.0), ("B", 10.0), ("C", 5.0)]


def test_build_table_contains_headers_and_students() -> None:
    table = build_table([("Alice", 12.5), ("Bob", 10.0)])
    assert "student" in table
    assert "median_coffee_spent" in table
    assert "Alice" in table
    assert "Bob" in table


def test_read_rows_raises_on_missing_required_columns(tmp_path: Path) -> None:
    f = _write_csv(
        tmp_path,
        "bad.csv",
        """
        student,date,sleep_hours
        Alice,2024-06-01,7
        """,
    )
    with pytest.raises(ValueError, match="Missing columns"):
        _read_rows([f])


def test_read_rows_raises_on_invalid_coffee_spent(tmp_path: Path) -> None:
    f = _write_csv(
        tmp_path,
        "bad.csv",
        """
        student,date,coffee_spent
        Alice,2024-06-01,not-a-number
        """,
    )
    with pytest.raises(ValueError, match="Invalid coffee_spent"):
        _read_rows([f])

