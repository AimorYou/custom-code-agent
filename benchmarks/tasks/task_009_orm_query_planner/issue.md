# Chained queries break after adding join()

## What's happening

Everything works fine with basic `filter()`, `exclude()`, and `order_by()` on a single table. But as soon as I add a `join()` call, things start falling apart.

### 1. `order_by()` after `join()` gives "ambiguous column name"

```python
purchases = (
    Purchase.objects
    .join(Customer)
    .order_by("name")
    .all()
)
# sqlite3.OperationalError: ambiguous column name: name
```

Both `Purchase` and `Customer` have a `name` column. The generated SQL has `ORDER BY name ASC` with no table qualifier, so SQLite doesn't know which table's `name` to sort by.

### 2. `exclude()` after `join()` targets the wrong table

```python
rows = (
    Purchase.objects
    .join(Customer)
    .filter(purchase__status="paid")
    .exclude(total__lt=100)
    .all()
)
```

The `exclude(total__lt=100)` should apply to `Purchase.total`, but because the generated SQL uses bare `total` instead of `purchase.total`, it either errors out or resolves against the wrong table when column names overlap.

### 3. Filter lookups with `__` operators don't get table prefix after join

Using something like `filter(age__gt=20)` after a `join()` generates `age > ?` without qualifying which table `age` belongs to. On a single table this is fine, but with a join it becomes ambiguous.

## Expected behavior

When a join is active, column references in `exclude()`, `order_by()`, and `filter()` operator lookups should be qualified with the primary model's table name to avoid ambiguity.

Simple queries without joins should continue to work exactly as before.
