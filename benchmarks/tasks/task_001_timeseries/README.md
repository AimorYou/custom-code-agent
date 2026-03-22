# tskit

Lightweight timeseries utilities for NumPy arrays. No heavy dependencies, just the basics done right.

## Installation

```bash
pip install numpy
```

Then copy the `src/` directory into your project, or add it to your `PYTHONPATH`.

## Quick start

```python
import numpy as np
from src.timeseries import rolling_mean, exponential_moving_average

data = np.array([1.0, 3.0, 5.0, 7.0, 9.0, 11.0])

# Rolling (moving) mean with a window of 3
rm = rolling_mean(data, window=3)
print(rm)  # [nan, nan, 3.0, 5.0, 7.0, 9.0]

# Exponential moving average
ema = exponential_moving_average(data, alpha=0.3)
print(ema)  # smoothed series
```

## API reference

### `rolling_mean(data, window)`

Compute the rolling mean over a 1-D NumPy array.

| Parameter | Type | Description |
|-----------|------|-------------|
| `data` | `np.ndarray` | 1-D numeric array |
| `window` | `int` | Number of elements in each window (>= 1) |

Returns an array of the same length. The first `window - 1` positions are `NaN`.

### `exponential_moving_average(data, alpha)`

Compute the exponential moving average (EMA).

| Parameter | Type | Description |
|-----------|------|-------------|
| `data` | `np.ndarray` | 1-D numeric array |
| `alpha` | `float` | Smoothing factor in (0, 1] |

Returns an array of the same length as the input.

## Running tests

```bash
python -m pytest tests/ -v
```

## License

MIT
