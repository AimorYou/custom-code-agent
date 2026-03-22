# confmerge

A Python library for deep merging, diffing, and patching configuration files with schema validation and environment variable interpolation.

## Features

- Deep merge with configurable list strategies (`override`, `append`, `merge`)
- Structured diff between two config trees
- Patch application from diff output
- Schema validation (required fields, type checking)
- Environment variable interpolation with fallback defaults
- YAML and JSON support

## Installation

```bash
pip install -e .
```

## Quick start

### Loading configs

```python
from src import load_config, dump_config

config = load_config("config.yaml")
dump_config(config, "output.json")
```

Environment variables are interpolated automatically:

```yaml
# config.yaml
database:
  host: ${DB_HOST:localhost}
  port: ${DB_PORT:5432}
```

### Deep merge

```python
from src import deep_merge

base = {"database": {"host": "localhost", "port": 3306}}
production = {"database": {"port": 5432, "ssl": True}}

result = deep_merge(base, production)
# {"database": {"host": "localhost", "port": 5432, "ssl": True}}
```

List merge strategies:

```python
# override (default) -- replace the list entirely
deep_merge({"plugins": ["a"]}, {"plugins": ["b"]}, strategy="override")
# {"plugins": ["b"]}

# append -- concatenate lists
deep_merge({"plugins": ["a"]}, {"plugins": ["b"]}, strategy="append")
# {"plugins": ["a", "b"]}

# merge -- element-wise merge (dicts merged, scalars replaced)
deep_merge(
    {"servers": [{"host": "a", "port": 80}]},
    {"servers": [{"port": 443}]},
    strategy="merge"
)
# {"servers": [{"host": "a", "port": 443}]}
```

### Diff and patch

```python
from src import compute_diff, apply_patch

old = {"db": {"host": "localhost", "port": 3306}}
new = {"db": {"host": "prod.example.com", "port": 3306}}

diff = compute_diff(old, new)
# [{"op": "changed", "path": "db.host", "old": "localhost", "value": "prod.example.com"}]

restored = apply_patch(old, diff)
assert restored == new
```

### Schema validation

```python
from src import validate

schema = {
    "host": {"type": "str", "required": True},
    "port": {"type": "int", "required": True},
}

errors = validate({"host": "localhost"}, schema)
# ["port: required field missing"]
```

## Running tests

```bash
python -m pytest tests/ -v
```
