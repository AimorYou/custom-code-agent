# Data loss when merging configs with different-length lists and deeply nested keys

## What's happening

We use confmerge in our deployment pipeline to layer environment-specific overrides on top of a base config. Recently we hit two separate data loss issues.

### 1. Plugin list gets truncated during merge

Our base config has one plugin defined, and the production override adds two more. After merging with the `"merge"` strategy, only the first plugin survives -- the rest vanish silently.

```python
base = {"plugins": [{"name": "auth", "enabled": True}]}
override = {"plugins": [
    {"name": "auth", "enabled": True},
    {"name": "metrics", "enabled": True},
    {"name": "cache", "enabled": True},
]}

result = deep_merge(base, override, strategy="merge")
# Expected: 3 plugins
# Actual: only 1 plugin -- "metrics" and "cache" are gone
```

The same thing happens the other way around: if the base list is longer than the override, the extra base items disappear too.

### 2. Config diff collapses deeply nested changes

When computing a diff between two configs that differ three or more levels deep, the diff engine returns a single "changed" entry for the entire subtree instead of a granular per-leaf diff.

```python
old = {"infra": {"cluster": {"nodes": {"count": 3, "type": "m5.large"}, "region": "us-east-1"}}}
new = {"infra": {"cluster": {"nodes": {"count": 5, "type": "m5.large"}, "region": "us-east-1"}}}

diff = compute_diff(old, new)
# Expected: one entry at path "infra.cluster.nodes.count"
# Actual: one entry at path "infra.cluster" replacing the entire subtree
```

This also breaks `apply_patch()` -- when you apply the collapsed diff back, it overwrites sibling keys that didn't change (like `nodes.type` and `region`), effectively losing data.

## Expected behavior

1. `deep_merge(..., strategy="merge")` should keep all items from the longer list when lists have different lengths. Overlapping indices get merged element-wise, remaining items get appended.
2. `compute_diff()` should recurse to any depth and produce leaf-level entries.
3. `apply_patch(old, compute_diff(old, new))` should produce a result equal to `new` without destroying unchanged keys.
