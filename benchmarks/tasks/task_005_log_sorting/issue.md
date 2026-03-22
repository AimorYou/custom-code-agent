# Logs from different regions sort out of order after aggregation

We use logmerge to aggregate logs from services running in multiple AWS regions (us-east-1 and eu-west-1). After merging, the entries are supposed to be in chronological order, but they're clearly not.

Here's a minimal example:

```python
from src.aggregator import aggregate_logs

us_logs = [
    "2024-06-01T10:00:00-04:00 service-a Starting up",
    "2024-06-01T11:00:00-04:00 service-a Ready",
]

eu_logs = [
    "2024-06-01T14:30:00+02:00 service-b Starting up",
]

merged = aggregate_logs([us_logs, eu_logs])
for entry in merged:
    print(entry)
```

The EU entry (`14:30:00+02:00`) is actually `12:30 UTC`, so it should appear before the US `11:00:00-04:00` entry (`15:00 UTC`). But in the output it ends up last, as if the tool is just comparing the time portion without accounting for the timezone offset.

This is causing confusion during incident reviews because the timeline doesn't match what actually happened. Logs from our EU services look like they happened later than they did.

We need the merged output sorted by absolute time regardless of what timezone each source is in.
