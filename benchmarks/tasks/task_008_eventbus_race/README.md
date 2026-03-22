# eventbus

A lightweight in-process event bus for Python with middleware support and priority-based handler ordering.

## Features

- Subscribe and emit events with payload data
- Priority-based handler execution (lower number = higher priority)
- Middleware chain for cross-cutting concerns (logging, retries, timeouts)
- Async event emission support
- Event serialization/deserialization
- Event history tracking

## Installation

```bash
pip install -e .
```

## Quick start

```python
from src import EventBus, Event

bus = EventBus()

# Subscribe a handler
bus.subscribe("user.created", lambda e: print(f"Welcome, {e.payload['name']}!"))

# Emit an event
bus.emit(Event(name="user.created", payload={"name": "Alice"}))
```

## Priority handlers

Handlers with a lower priority number run first:

```python
bus.subscribe("order.placed", send_confirmation_email, priority=10)
bus.subscribe("order.placed", update_inventory, priority=1)   # runs first
bus.subscribe("order.placed", notify_warehouse, priority=20)   # runs last
```

## Middleware

Add middleware to intercept all events before they reach handlers:

```python
from src import LoggingMiddleware, RetryMiddleware, TimeoutMiddleware

bus.use(LoggingMiddleware())
bus.use(RetryMiddleware(max_retries=3))
bus.use(TimeoutMiddleware(timeout=5.0))
```

You can write custom middleware as any callable that accepts `(event, next_fn)`:

```python
def auth_middleware(event, next_fn):
    if not event.payload.get("auth_token"):
        raise PermissionError("Missing auth token")
    return next_fn(event)

bus.use(auth_middleware)
```

## Async support

```python
import asyncio
from src import EventBus, Event

bus = EventBus()

async def async_handler(event):
    await asyncio.sleep(0.1)
    return f"processed {event.name}"

bus.subscribe("task", async_handler)
results = asyncio.run(bus.emit_async(Event(name="task")))
```

## Running tests

```bash
python -m pytest tests/ -v
```
