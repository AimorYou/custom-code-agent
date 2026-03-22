# fileproc

A simple command-line tool for processing text files. Reads a file, applies a standard transformation pipeline, and outputs the result.

## Installation

```bash
pip install fileproc
```

## Usage

```bash
# Process a single file
fileproc report.txt

# Process a CSV file
fileproc data.csv
```

## Supported file types

- `.txt` — plain text files
- `.csv` — comma-separated value files

## Python API

You can also use `fileproc` as a library:

```python
from fileproc.processor import process_file

result = process_file("report.txt")
print(result)
```

### Listing files in a directory

```python
from fileproc.file_utils import list_supported_files

files = list_supported_files("./data/")
for f in files:
    print(f)
```

## Development

```bash
git clone https://github.com/yourorg/fileproc.git
cd fileproc
pip install -e ".[dev]"
python -m pytest tests/ -v
```

## License

MIT
