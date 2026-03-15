"""
BashSessionTool — persistent bash session (wraps OpenHands TerminalTool).

Переименовывает `terminal` → `bash_session`, чтобы агенту было понятно
отличие от stateless `bash`:

  - bash_session: persistent tmux/shell session, состояние сохраняется между вызовами
  - bash: каждый вызов — новый subprocess, без состояния
"""

from openhands.sdk.tool import register_tool
from openhands.tools.terminal.definition import TerminalTool


class BashSessionTool(TerminalTool):
    """Persistent bash session (TerminalTool with a clearer name)."""

    pass


# BashSessionTool → auto-name "bash_session"
register_tool(BashSessionTool.name, BashSessionTool)
