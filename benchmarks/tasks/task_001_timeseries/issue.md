## rolling_mean returns wrong values

I was comparing our `rolling_mean` output against pandas and the numbers don't match.

With `window=3` on `[1, 2, 3, 4, 5]`, position 3 should give `mean([2, 3, 4]) = 3.0` but we get `2.5`. Looks like the window is grabbing one extra element somehow?

```python
import numpy as np
from src.timeseries import rolling_mean

data = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
result = rolling_mean(data, window=3)
print(result)
# Expected: [nan, nan, 2.0, 3.0, 4.0]
# Actual:   [nan, nan, 1.5, 2.0, 3.0]
```

This is causing drift in our daily aggregation pipeline. Would be great to get a fix in soon.
