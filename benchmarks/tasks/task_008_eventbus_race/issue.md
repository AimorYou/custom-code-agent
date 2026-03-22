# RuntimeError and missed handlers when using EventBus from multiple threads

## What's happening

We started using the event bus from worker threads in our job processing pipeline (one thread subscribes handlers dynamically, others emit events), and we're seeing intermittent crashes in production.

The most common error is:

```
RuntimeError: dictionary changed size during iteration
```

This happens somewhere in the handler dispatch path. We've also seen `IndexError` a few times, which seems related to the middleware chain, and occasionally handlers just silently don't fire even though they were definitely subscribed before the emit call.

## How to reproduce

It's timing-dependent, but this reliably triggers it within a few runs:

```python
import threading
from src import EventBus, Event

bus = EventBus()
results = []
bus.subscribe("task", lambda e: results.append(1))

barrier = threading.Barrier(200)

def subscribe_loop():
    barrier.wait()
    bus.subscribe("task", lambda e: None)

def emit_loop():
    barrier.wait()
    bus.emit(Event(name="task"))

threads = [threading.Thread(target=subscribe_loop) for _ in range(100)]
threads += [threading.Thread(target=emit_loop) for _ in range(100)]
for t in threads:
    t.start()
for t in threads:
    t.join()

# Expected: len(results) == 100
# Actual: sometimes fewer, sometimes RuntimeError
```

Adding middleware at runtime (e.g., enabling a logging middleware via an admin endpoint) also causes crashes if events are being processed at the same time.

## Expected behavior

- `subscribe()`, `emit()`, and `use()` should be safe to call concurrently from different threads.
- A handler that was subscribed before an `emit()` call should always be invoked.
- Adding middleware while events are being processed should not crash.
