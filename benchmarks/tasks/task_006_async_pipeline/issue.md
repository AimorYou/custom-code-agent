# Pipeline output order is scrambled after async loader migration

## What happened

We recently migrated the file loading stage from synchronous to async to improve throughput. Since the change, the pipeline output no longer matches the order of the input files.

For example, if I pass `["a.txt", "b.txt", "c.txt"]`, the final report has the entries jumbled -- usually smaller files appear first in the output regardless of their position in the input list. This is breaking downstream consumers that rely on positional correspondence between input and output.

## Reproduction

```python
import asyncio
from src.pipeline import run_pipeline

# a.txt is ~500 chars, b.txt is ~50 chars, c.txt is ~200 chars
result = asyncio.run(run_pipeline(["a.txt", "b.txt", "c.txt"]))
print(result)

# Expected: entries for a, b, c in that order
# Actual:   entries come back as b, c, a (shortest file first)
```

It's consistent -- the ordering always seems to correlate with file size, with smaller files appearing earlier in the result.

## Expected behavior

Pipeline output should preserve the same order as the input file list. We still want concurrent loading for performance, just need the results to come back in the right order.

## Environment

- Python 3.11
- Running on macOS, but same behavior on Linux CI

## Failing tests

`tests/test_pipeline_order.py` catches this -- the order assertions fail.
