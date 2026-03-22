# litemap

A lightweight Python ORM for SQLite with a Django-inspired query API.

## Features

- Declarative model definitions with typed fields
- Lazy `QuerySet` with chained `filter()`, `exclude()`, `order_by()`
- Foreign key relationships and `join()` support
- Automatic table creation from model definitions
- Environment-friendly: uses SQLite with in-memory or file-based databases

## Installation

```bash
pip install -e .
```

## Defining models

```python
from src import IntField, StringField, BoolField, ForeignKey
from src.model import Model

class Department(Model):
    name = StringField()

class Employee(Model):
    name = StringField()
    age = IntField()
    active = BoolField(default=True)
    department_id = ForeignKey(to="department")
```

## Creating tables

```python
from src import ConnectionManager

ConnectionManager.get(":memory:")  # or "mydb.sqlite"
Department.create_table()
Employee.create_table()
```

## Inserting data

```python
eng = Department.insert(name="Engineering")
Employee.insert(name="Alice", age=30, active=True, department_id=eng.id)
```

## Querying

```python
# Basic filter
seniors = Employee.objects.filter(age__gt=25).all()

# Exclude
non_bobs = Employee.objects.exclude(name="Bob").all()

# Chained filters
active_seniors = Employee.objects.filter(age__gt=25).filter(active=True).all()

# Ordering
by_age = Employee.objects.order_by("age").all()
by_age_desc = Employee.objects.order_by("-age").all()

# Count and first
total = Employee.objects.count()
youngest = Employee.objects.order_by("age").first()
```

## Joins

```python
# Join with another model via ForeignKey
rows = (
    Employee.objects
    .join(Department)
    .filter(department__name="Engineering")
    .order_by("name")
    .all()
)
```

## Running tests

```bash
python -m pytest tests/ -v
```
