# confloader

A lightweight configuration file loader for Python applications. Reads YAML and JSON config files, applies sensible defaults, and validates the result.

## Installation

```bash
pip install confloader
```

## Quick start

```python
from confloader import load_config

config = load_config("config/app.yaml")
print(config["database"]["host"])
```

## Supported formats

| Format | Extensions        |
|--------|-------------------|
| YAML   | `.yaml`, `.yml`   |
| JSON   | `.json`           |

## API

### `load_config(path: str) -> dict`

Loads a configuration file from the given path. The format is detected automatically based on the file extension.

The returned dictionary has default values merged in and is validated against the expected schema. Raises `ValueError` for unsupported file extensions and `FileNotFoundError` if the path does not exist.

```python
# YAML config
config = load_config("settings.yaml")

# JSON config
config = load_config("settings.json")
```

## Default values

If your config file omits certain keys, `confloader` fills them in from a built-in defaults template. This means you only need to specify the values you want to override.

## Validation

After merging defaults, the configuration is validated to ensure required fields are present and values have the correct types. Invalid configs raise a `ValueError` with a descriptive message.

## Development

```bash
git clone https://github.com/yourorg/confloader.git
cd confloader
pip install -e ".[dev]"
python -m pytest tests/ -v
```

## License

MIT
