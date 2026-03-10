# custom-code-agent

Кастомный агент для написания кода, построенный на [OpenHands SDK](https://github.com/All-Hands-AI/OpenHands).

Цель дипломной работы — исследовать, как кастомные инструменты сокращают количество
API-вызовов и расход токенов при работе на бенчмарке [SWE-bench](https://www.swebench.com/).

---

## Архитектура

```
run.py
  └── LocalConversation (OpenHands SDK)
        ├── Agent (openhands.sdk.Agent)
        │     └── LLM (litellm → Anthropic / OpenAI / любой провайдер)
        ├── TerminalTool    ← OpenHands built-in (персистентная bash-сессия)
        ├── BashTool        ← кастомный: stateless subprocess, один вызов — один процесс
        ├── GrepTool        ← кастомный: regex-поиск с контекстом вокруг совпадений
        └── SmartReadTool   ← кастомный: читает файл с диапазоном строк
```

```
custom-code-agent/
├── agent/
│   ├── config.py           # Конфигурация через env-переменные
│   ├── token_tracker.py    # Трекинг токенов + make_token_callback()
│   └── tools/
│       ├── __init__.py     # Регистрация всех кастомных тулзов
│       ├── bash.py         # Stateless subprocess bash
│       ├── grep.py         # Regex-поиск по файлам с контекстом
│       └── smart_read.py   # Чтение файла с диапазоном строк
├── tests/
│   └── test_tools.py       # Юнит-тесты (без API-вызовов)
├── run.py                  # Единственный entry point
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
# Вставьте нужный API ключ в .env
```

---

## Использование

```bash
# Запустить агента (Anthropic по умолчанию)
uv run run.py "Fix the failing tests in tests/"

# Список зарегистрированных инструментов
uv run run.py --list-tools

# Отключить инструмент
uv run run.py --disable bash "задача"

# Другая модель Anthropic
uv run run.py --model anthropic/claude-opus-4-6 "задача"

# OpenAI
uv run run.py --model openai/gpt-4o "задача"

# OpenAI-совместимый сервис (Ollama, vLLM, и т.д.)
uv run run.py --model openai/llama3 --base-url http://localhost:11434/v1 "задача"

# Передать API ключ напрямую
uv run run.py --api-key sk-... "задача"

# Тихий режим (только итоговый ответ)
uv run run.py --quiet "задача"
```

---

## Конфигурация

| Переменная | По умолчанию | Описание |
|------------|-------------|----------|
| `ANTHROPIC_API_KEY` | — | API ключ для Anthropic моделей |
| `OPENAI_API_KEY` | — | API ключ для OpenAI и совместимых сервисов |
| `AGENT_API_KEY` | — | Универсальный ключ (приоритет над остальными) |
| `AGENT_MODEL` | `anthropic/claude-sonnet-4-6` | litellm model ID |
| `AGENT_BASE_URL` | — | Кастомный базовый URL (для OpenAI-совместимых сервисов) |
| `AGENT_MAX_STEPS` | `50` | Максимум шагов агента |
| `AGENT_WORKING_DIR` | `.` | Рабочая директория |
| `AGENT_VERBOSE` | `true` | Подробный вывод |
| `AGENT_DISABLED_TOOLS` | — | Отключённые тулзы через запятую |

Ключ выбирается автоматически по провайдеру из model ID:
- `anthropic/...` → `ANTHROPIC_API_KEY`
- `openai/...` → `OPENAI_API_KEY`
- Любой → `AGENT_API_KEY` (наивысший приоритет)

---

## Инструменты

| Имя | Источник | Описание |
|-----|----------|----------|
| `terminal` | OpenHands built-in | Персистентная bash-сессия через tmux (состояние сохраняется между вызовами) |
| `bash` | Кастомный | Stateless subprocess — каждый вызов независим, удобен для тестов и скриптов |
| `grep` | Кастомный | Regex-поиск по файлам с N строками контекста вокруг совпадений |
| `smart_read` | Кастомный | Читает файл целиком или диапазон строк с номерами строк |

**Когда что использовать:**
- `terminal` — когда нужно сохранить состояние (активировать virtualenv, cd и дальше работать)
- `bash` — короткие одиночные команды (запуск тестов, ls, diff, установка пакетов)
- `grep` — найти определение функции/класса без лишнего чтения файлов
- `smart_read` — прочитать конкретный фрагмент большого файла по номерам строк

---

## Добавление нового инструмента

Скопируй [agent/tools/smart_read.py](agent/tools/smart_read.py) как шаблон:

```python
# agent/tools/my_tool.py
from openhands.sdk.tool import Action, Observation, register_tool
from openhands.sdk.tool.tool import ToolDefinition, ToolExecutor
from pydantic import Field

class MyAction(Action):
    param: str = Field(description="Параметр инструмента")

class MyObservation(Observation):
    """Результат работы инструмента."""

class _MyExecutor(ToolExecutor):
    def __call__(self, action: MyAction, conversation=None) -> MyObservation:
        result = do_something(action.param)
        return MyObservation.from_text(result)

class MyTool(ToolDefinition[MyAction, MyObservation]):
    @classmethod
    def create(cls, conv_state=None, **_):
        return [cls(action_type=MyAction, observation_type=MyObservation,
                    description="...", executor=_MyExecutor())]

register_tool(MyTool.name, MyTool)
```

Добавь импорт в [agent/tools/__init__.py](agent/tools/__init__.py):

```python
from agent.tools import my_tool  # noqa: F401
```

Добавь в список в [run.py](run.py):

```python
Tool(name="my_tool"),
```

Имя тула = snake_case имени класса без суффикса `_tool` (например, `MyTool` → `my_tool`).

---

## Трекинг токенов

После каждого запуска выводится таблица:

```
         Token Usage Summary
┌───────────────────────┬────────────────────────────┐
│ Metric                │                      Value │
├───────────────────────┼────────────────────────────┤
│ Model                 │  anthropic/claude-sonnet-4-6│
│ Steps                 │                          5 │
│ Input tokens          │                     12,430 │
│ Output tokens         │                      1,820 │
│ Cache write tokens    │                      8,200 │
│ Cache read tokens     │                      4,100 │
│ Estimated cost        │                     $0.0521│
└───────────────────────┴────────────────────────────┘
```

Доступно программно:

```python
tracker.steps        # список StepUsage по шагам
tracker.summary()    # dict с агрегированными данными
tracker.total_cost   # float, USD
```

---

## Тесты

```bash
uv run pytest tests/ -v
```
