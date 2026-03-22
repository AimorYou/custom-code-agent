# logmerge

A log aggregation utility that merges log streams from multiple services into a single, chronologically sorted output.

## Installation

```bash
pip install logmerge
```

## Usage

### Command line

```bash
# Merge logs from multiple files
logmerge service-a.log service-b.log service-c.log > merged.log

# Merge all log files in a directory
logmerge ./logs/*.log > merged.log
```

### Python API

```python
from logmerge.aggregator import aggregate_logs

logs_a = [
    "2024-06-01T10:00:00-04:00 service-a Starting up",
    "2024-06-01T10:05:00-04:00 service-a Connected to DB",
]

logs_b = [
    "2024-06-01T14:02:00+02:00 service-b Health check OK",
]

merged = aggregate_logs([logs_a, logs_b])
for line in merged:
    print(line)
```

## Log format

Each log line must begin with an ISO-8601 timestamp, followed by a space and the message:

```
2024-06-01T10:00:00-04:00 service-a Starting up
```

Supported timestamp formats:
- `2024-06-01T10:00:00-04:00` (with UTC offset)
- `2024-06-01T10:00:00+02:00` (with UTC offset)
- `2024-06-01T10:00:00Z` (UTC)

## Architecture

- **aggregator** — merges multiple log streams and sorts by timestamp
- **log_parser** — parses individual log lines into structured records
- **time_utils** — timestamp parsing helpers

## Development

```bash
git clone https://github.com/yourorg/logmerge.git
cd logmerge
pip install -e ".[dev]"
python -m pytest tests/ -v
```

## License

MIT
