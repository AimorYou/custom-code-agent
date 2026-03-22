## Stale values returned after updating through DataService

After calling `svc.set("x", new_value)`, subsequent `svc.get("x")` still returns the old value. It works correctly the first time a key is written, but updates don't seem to take effect until the service is restarted.

```python
from src.service import DataService

svc = DataService()
svc.set("x", 1)
print(svc.get("x"))  # 1  -- correct

svc.set("x", 2)
print(svc.get("x"))  # 1  -- still returns old value, expected 2
```

This is causing issues in production where config updates are silently ignored. Restarting the process fixes it temporarily, which makes me think something is being held in memory when it shouldn't be.
