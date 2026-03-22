"""Apply a diff as a patch to a config."""

from __future__ import annotations

import copy
from typing import Any, Dict, List

from .diff import DiffEntry


def apply_patch(
    config: Dict[str, Any],
    diff: List[DiffEntry],
) -> Dict[str, Any]:
    """Apply *diff* entries to a copy of *config* and return the result.

    Supports ``added``, ``removed``, and ``changed`` operations.
    Paths use dot-notation (e.g. ``"database.host"``).

    """
    result = copy.deepcopy(config)
    for entry in diff:
        op = entry["op"]
        path_parts = entry["path"].split(".")

        if op == "added":
            _set_nested(result, path_parts, entry["value"])
        elif op == "removed":
            _del_nested(result, path_parts)
        elif op == "changed":
            _set_nested(result, path_parts, entry["value"])
    return result


def _set_nested(d: dict, parts: list[str], value: Any) -> None:
    for part in parts[:-1]:
        if part not in d or not isinstance(d[part], dict):
            d[part] = {}
        d = d[part]
    d[parts[-1]] = copy.deepcopy(value)


def _del_nested(d: dict, parts: list[str]) -> None:
    for part in parts[:-1]:
        if part not in d:
            return
        d = d[part]
    d.pop(parts[-1], None)
