"""
SmartReadTool — читает файл с опциональным диапазоном строк.

Зачем это нужно (суть кастомного тула):
  Без него агент вынужден делать `cat file.py` и получать весь файл целиком,
  тратя токены на контекст. SmartReadTool позволяет запросить только нужный
  фрагмент — например, строки 50-80 — сокращая расход токенов на больших файлах.
"""

import os
from collections.abc import Sequence
from typing import TYPE_CHECKING

from pydantic import Field

from openhands.sdk.tool import Action, Observation, register_tool
from openhands.sdk.tool.tool import ToolAnnotations, ToolDefinition, ToolExecutor

TOOL_DESCRIPTION = """\
Read a file and return its contents with line numbers.
Supports reading only a specific range of lines to avoid returning large files in full.

Prefer this over `terminal` + `cat` when you need a specific section of a file,
as it reduces token usage by returning only the relevant lines.
"""


class SmartReadObservation(Observation):
    """Concrete observation returned by SmartReadTool."""

if TYPE_CHECKING:
    from openhands.sdk.conversation import LocalConversation


class SmartReadAction(Action):
    """Read a file, optionally limited to a line range."""

    path: str = Field(description="Absolute or relative path to the file to read.")
    start_line: int | None = Field(
        default=None,
        description="First line to read (1-indexed, inclusive). Omit to start from the beginning.",
    )
    end_line: int | None = Field(
        default=None,
        description="Last line to read (1-indexed, inclusive). Omit to read until the end.",
    )


class _SmartReadExecutor(ToolExecutor):
    def __call__(
        self,
        action: SmartReadAction,
        conversation: "LocalConversation | None" = None,
    ) -> Observation:
        # Resolve relative paths against workspace (like bash/grep/submit do)
        path = action.path
        if not os.path.isabs(path) and conversation is not None:
            working_dir = getattr(
                getattr(conversation, "workspace", None), "working_dir", None
            )
            if working_dir:
                path = os.path.join(working_dir, path)

        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
        except FileNotFoundError:
            return SmartReadObservation.from_text(f"File not found: {action.path}", is_error=True)
        except OSError as e:
            return SmartReadObservation.from_text(str(e), is_error=True)

        total = len(lines)
        start = max(0, (action.start_line or 1) - 1)
        end = min(total, action.end_line or total)
        selected = lines[start:end]

        # Format with line numbers (makes it easier for the model to reference)
        numbered = "".join(
            f"{start + i + 1:>6} | {line}" for i, line in enumerate(selected)
        )
        header = f"[{action.path}  lines {start+1}-{end} of {total}]\n"
        return SmartReadObservation.from_text(header + numbered)


TOOL_DESCRIPTION = """\
Read a file and return its contents with line numbers.
Supports reading only a specific range of lines to avoid returning large files in full.

Prefer this over `terminal` + `cat` when you need a specific section of a file,
as it reduces token usage by returning only the relevant lines.
"""


class SmartReadTool(ToolDefinition[SmartReadAction, SmartReadObservation]):
    @classmethod
    def create(cls, conv_state=None, **_) -> Sequence["SmartReadTool"]:
        return [
            cls(
                action_type=SmartReadAction,
                observation_type=SmartReadObservation,
                description=TOOL_DESCRIPTION,
                annotations=ToolAnnotations(readOnlyHint=True, destructiveHint=False),
                executor=_SmartReadExecutor(),
            )
        ]


register_tool(SmartReadTool.name, SmartReadTool)
