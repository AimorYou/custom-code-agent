# SWE-Bench-style Benchmark Tasks

5 задач для тестирования code-агентов. Каждая задача — мини-репозиторий с:
- `issue.md` — описание бага (как GitHub issue)
- `src/` — исходный код с багом
- `tests/` — тесты, которые падают из-за бага

## Задачи

| # | Задача | Баг | Файл | Сложность |
|---|--------|-----|------|-----------|
| 1 | `task_001_data_merger` | `pd.merge` использует `how="inner"` вместо `how="left"` | `src/merger.py` | Easy |
| 2 | `task_002_array_stats` | `np.std()` без `ddof=1` (population вместо sample std) | `src/stats.py` | Easy |
| 3 | `task_003_timeseries` | Off-by-one в `rolling_mean` — `i - window` вместо `i - window + 1` | `src/timeseries.py` | Medium |
| 4 | `task_004_outlier_detector` | IQR bounds от `mean` вместо `Q1`/`Q3` | `src/detector.py` | Medium |
| 5 | `task_005_data_cleaner` | `median(axis=1)` вместо `median(axis=0)` | `src/cleaner.py` | Easy-Medium |

## Зависимости

Только `numpy` и `pandas` (в dev-зависимостях проекта).

## Запуск

```bash
# Все задачи (логи агента по умолчанию)
uv run python benchmarks/run_benchmark.py

# Одна задача
uv run python benchmarks/run_benchmark.py task_001

# Без логов
uv run python benchmarks/run_benchmark.py --quiet task_001

# Другая модель
uv run python benchmarks/run_benchmark.py --model anthropic/claude-opus-4-6 task_001

# Другой конфиг
uv run python benchmarks/run_benchmark.py --agent-config custom.yaml task_001

# Сохранить результаты в JSON
uv run python benchmarks/run_benchmark.py --save results.json
```

## Как это работает

```
run_benchmark.py
  │
  ├── 1. Копирует задачу во /tmp БЕЗ tests/
  │      (агент физически не видит тесты)
  │
  ├── 2. Читает issue.md → передаёт агенту как task
  │      (агент оборачивает через instance_template из agent_config.yaml)
  │
  ├── 3. Запускает агента: run.py --working-dir /tmp/... <issue>
  │
  ├── 4. Проверяет SUBMISSION.json (создаёт submit tool)
  │      → агент явно сигнализирует завершение
  │
  ├── 5. Читает METRICS.json (steps, tokens, cost)
  │
  └── 6. Копирует tests/ → pytest
         → PASS/FAIL
```

## Метрики для сбора

- Потраченные токены (input/output)
- Количество API-вызовов (steps)
- Время до решения
- Submitted / Not submitted
- Pass / Fail
