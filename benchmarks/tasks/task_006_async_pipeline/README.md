# asyncpipe

A lightweight async data processing pipeline for Python.

## Overview

asyncpipe loads files concurrently, processes them through a configurable pipeline, and produces structured reports. It's designed for I/O-bound workloads where you want to maximize throughput without sacrificing simplicity.

## Architecture

The pipeline has three stages:

1. **Loader** (`src/loader.py`) -- Reads input files concurrently using `asyncio` tasks. Handles variable I/O latency gracefully.
2. **Processor** (`src/processor.py`) -- Transforms raw file contents into structured records with sequence numbers and metadata.
3. **Report generator** (`src/utils.py`) -- Combines processed records into a final output report.

The orchestration logic lives in `src/pipeline.py`, which chains the stages together.

## Quick start

```python
import asyncio
from src.pipeline import run_pipeline

result = asyncio.run(run_pipeline(["data/input1.txt", "data/input2.txt"]))
print(result)
```

## Project structure

```
src/
  loader.py        # Async file loading
  processor.py     # Data transformation
  pipeline.py      # Pipeline orchestration
  utils.py         # Report generation
tests/
  test_pipeline_order.py
```

## Running tests

```bash
python -m pytest tests/ -v
```

## Requirements

- Python 3.10+
- No external dependencies (stdlib only)
