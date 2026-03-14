# custom-code-agent

Кастомный агент для написания кода, построенный на [OpenHands SDK](https://github.com/All-Hands-AI/OpenHands).

Цель дипломной работы — исследовать, как кастомные инструменты сокращают количество
API-вызовов и расход токенов при работе на бенчмарке [SWE-bench](https://www.swebench.com/).

---

## Архитектура

```
run.py                          ← entry point
  └── LocalConversation (OpenHands SDK)
        ├── Agent + system_prompt.j2   ← кастомный системный промпт
        │     └── LLM (litellm → Anthropic / OpenAI / любой провайдер)
        ├── TerminalTool    ← OpenHands built-in (персистентная bash-сессия)
        ├── BashTool        ← кастомный: stateless subprocess
        ├── GrepTool        ← кастомный: regex-поиск с контекстом
        ├── SmartReadTool   ← кастомный: чтение файла с диапазоном строк
        └── SubmitTool      ← кастомный: сигнал завершения задачи
```

```
custom-code-agent/
├── agent/
│   ├── agent_config.yaml      # Поведение: промпты, step_limit
│   ├── config.py              # Загрузка конфига (.env + YAML + CLI)
│   ├── token_tracker.py       # Трекинг токенов и стоимости
│   ├── prompts/
│   │   └── system_prompt.j2   # Jinja2 системный промпт
│   └── tools/
│       ├── bash.py            # Stateless subprocess bash
│       ├── grep.py            # Regex-поиск по файлам с контекстом
│       ├── smart_read.py      # Чтение файла с диапазоном строк
│       └── submit.py          # Сигнал завершения задачи
├── benchmarks/
│   ├── run_benchmark.py       # SWE-Bench-style раннер
│   └── tasks/                 # 5 задач с багами и тестами
├── tests/
│   └── test_tools.py          # Юнит-тесты инструментов
├── run.py                     # Entry point
├── .env                       # Секреты (не в git)
└── .env.example
```

---

## Установка

Требуется [uv](https://github.com/astral-sh/uv).

```bash
git clone <repo-url>
cd custom-code-agent

uv sync
cp .env.example .env
# Вставьте API ключ в .env
```

---

## Использование

```bash
# Запустить агента
uv run run.py "Fix the failing tests in tests/"

# Тихий режим
uv run run.py --quiet "задача"

# Другая модель
uv run run.py --model anthropic/claude-opus-4-6 "задача"

# Другой конфиг поведения
uv run run.py --prompt-config path/to/config.yaml "задача"

# Указать рабочую директорию
uv run run.py --working-dir /path/to/project "задача"

# Отключить инструмент
uv run run.py --disable bash "задача"

# Список зарегистрированных инструментов
uv run run.py --list-tools
```

---

## Конфигурация

Три источника конфигурации с чётким разделением:

### `.env` — секреты и подключение

| Переменная | Описание |
|---|---|
| `AGENT_API_KEY` | API ключ |
| `AGENT_BASE_URL` | Кастомный API endpoint (для OpenAI-совместимых сервисов) |
| `AGENT_MODEL` | litellm model ID (по умолчанию `anthropic/claude-sonnet-4-6`) |

### `agent/agent_config.yaml` — поведение агента

```yaml
agent:
  system_template: "system_prompt.j2"   # Jinja2 шаблон системного промпта
  instance_template: |                  # Шаблон задачи ({{task}} заменяется)
    <issue_description>
    {{task}}
    </issue_description>
    ...
  step_limit: 30                        # Макс. шагов агента
  cost_limit: 0                         # Лимит стоимости в USD (0 = без лимита)
```

### CLI аргументы — рантайм-оверрайды

| Аргумент | Описание |
|---|---|
| `--model` | Переопределить модель из `.env` |
| `--max-steps` | Переопределить `step_limit` из YAML |
| `--working-dir` | Рабочая директория (по умолчанию `.`) |
| `--quiet` | Подавить вывод агента |
| `--disable TOOL` | Отключить инструмент |
| `--prompt-config` | Путь к альтернативному YAML конфигу |

---

## Инструменты

| Имя | Источник | Описание |
|-----|----------|----------|
| `terminal` | OpenHands built-in | Персистентная bash-сессия (состояние между вызовами) |
| `bash` | Кастомный | Stateless subprocess — каждый вызов независим |
| `grep` | Кастомный | Regex-поиск по файлам с N строками контекста |
| `smart_read` | Кастомный | Чтение файла целиком или диапазона строк |
| `submit` | Кастомный | Сигнал завершения — агент вызывает когда починил баг |

---

## Бенчмарк

5 SWE-Bench-style задач для тестирования агента. Подробности — в [benchmarks/README.md](benchmarks/README.md).

```bash
# Все задачи
uv run python benchmarks/run_benchmark.py

# Одна задача
uv run python benchmarks/run_benchmark.py task_001

# С логами агента
uv run python benchmarks/run_benchmark.py --verbose task_001

# Сохранить результаты
uv run python benchmarks/run_benchmark.py --save results.json
```

---

## Трекинг токенов

После каждого запуска выводится таблица:

```
         Token Usage Summary
┌───────────────────────┬────────────────────┐
│ Metric                │              Value │
├───────────────────────┼────────────────────┤
│ Model                 │  openai/qwen/...   │
│ Steps                 │                  5 │
│ Input tokens          │             12,430 │
│ Output tokens         │              1,820 │
│ Estimated cost        │            $0.0521 │
└───────────────────────┴────────────────────┘
```

---

## Добавление нового инструмента

1. Создай файл в `agent/tools/` (шаблон — `smart_read.py`)
2. Добавь импорт в `agent/tools/__init__.py`
3. Добавь `Tool(name="...")` в `build_tools()` в `run.py`

---

## Тесты

```bash
uv run pytest tests/ -v
```
