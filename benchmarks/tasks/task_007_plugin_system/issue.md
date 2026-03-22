# New plugin not being picked up by the system

## What's going on

I added a new plugin (`math_plugin.py`) to the `src/plugins/` directory following the same pattern as `example_plugin.py` -- class with `execute()`, decorated with `@register_plugin`. But when I start the app, only the example plugin shows up. My new plugin is completely invisible.

I double-checked the file is in the right directory and the decorator is applied correctly. Ran `list_plugins()` after init and it only returns `["example"]`.

## Steps to reproduce

1. Drop a new plugin file into `src/plugins/` (e.g. `math_plugin.py`)
2. Use `@register_plugin("math")` decorator on the class
3. Call `discover_plugins()` followed by `list_plugins()`
4. Only `"example"` is listed -- `"math"` is missing

## Additional weirdness

Even the example plugin that IS discovered seems broken at runtime. When I do:

```python
plugin = get_plugin("example")
plugin.execute(text="hello")
```

I get a `TypeError`. Haven't dug into that yet but it might be related, or a separate issue.

## Expected behavior

Any `.py` file placed in the `plugins/` directory should be automatically discovered and importable by name via `get_plugin()`. Once retrieved, calling `.execute()` on the plugin should work.

## Failing tests

`tests/test_plugin_discovery.py`
