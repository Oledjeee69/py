# Student CSV Reports

Мини‑проект: CLI‑скрипт, который читает один или несколько CSV‑файлов с данными подготовки студентов к экзаменам и формирует отчёты в консоль.

## Требования

- Python 3.11+ (проверено на 3.13)

## Установка

```bash
python -m pip install -r requirements.txt
```

Для запуска тестов:

```bash
python -m pip install -r requirements.txt -r requirements-dev.txt
```

## Запуск

Отчёт `median-coffee` — медианная сумма трат на кофе (`coffee_spent`) по каждому студенту **по всем переданным файлам суммарно**.

```bash
python student_reports.py --report median-coffee --files data/demo.csv
```

Можно передать несколько файлов:

```bash
python student_reports.py --report median-coffee --files data/a.csv data/b.csv
```

## Тесты

```bash
python -m pytest -q
```

## Архитектура отчётов

Отчёты регистрируются в словаре `REPORTS` в `student_reports.py`.
Чтобы добавить новый отчёт:

1. Реализуйте функцию вида `def report_x(rows: Sequence[Row]) -> list[tuple[str, float]]`
2. Добавьте её в `REPORTS` под новым ключом и запускайте через `--report`.

