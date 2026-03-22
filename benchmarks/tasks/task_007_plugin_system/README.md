# plugkit

A minimal plugin system framework for Python applications.

## Overview

plugkit provides automatic plugin discovery, registration, and retrieval. Drop a Python module into the plugins directory, decorate your class, and it's ready to use.

## Writing a plugin

Create a new `.py` file in `src/plugins/`:

```python
# src/plugins/my_plugin.py
from src.plugin_registry import register_plugin

@register_plugin("my_plugin")
class MyPlugin:
    def execute(self, **kwargs):
        # Your plugin logic here
        return {"result": "done"}
```

That's it. The framework handles discovery and registration automatically.

## Using plugins

```python
from src.plugin_loader import discover_plugins
from src.plugin_registry import get_plugin, list_plugins

# Discover all plugins in the directory
discover_plugins("src/plugins")

# See what's available
print(list_plugins())  # ["example", "my_plugin"]

# Get and run a plugin
plugin = get_plugin("my_plugin")
result = plugin.execute(text="hello")
```

## Architecture

- **Plugin registry** (`src/plugin_registry.py`) -- Global registry powered by the `@register_plugin` decorator. Stores plugins by name and provides lookup via `get_plugin()`.
- **Plugin loader** (`src/plugin_loader.py`) -- Scans the plugins directory and imports all modules, triggering decorator-based registration.
- **App** (`src/app.py`) -- Example application that uses the plugin system.

## Project structure

```
src/
  plugin_loader.py       # Plugin discovery
  plugin_registry.py     # Registration and retrieval
  app.py                 # Application entry point
  plugins/
    __init__.py
    example_plugin.py    # Built-in example plugin
    math_plugin.py       # Math operations plugin
tests/
  test_plugin_discovery.py
```

## Running tests

```bash
python -m pytest tests/ -v
```

## Requirements

- Python 3.10+
- No external dependencies
