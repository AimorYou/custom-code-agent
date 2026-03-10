"""Unit tests for custom tools (no API calls needed)."""

import os
import tempfile

import pytest

# Ensure tools are registered
import agent.tools  # noqa: F401
from openhands.sdk.tool import list_registered_tools


# ---------------------------------------------------------------------------
# BashTool
# ---------------------------------------------------------------------------

from agent.tools.bash import BashAction, BashTool


def _run_bash(command: str, timeout: int | None = None):
    tool = BashTool.create()[0]
    return tool(BashAction(command=command, timeout=timeout))


def test_bash_success():
    obs = _run_bash("echo hello")
    assert not obs.is_error
    assert "hello" in obs.text
    assert obs.exit_code == 0


def test_bash_exit_code():
    obs = _run_bash("exit 42")
    assert obs.is_error
    assert obs.exit_code == 42


def test_bash_stderr_included():
    obs = _run_bash("echo err >&2; exit 0")
    assert "err" in obs.text


def test_bash_timeout():
    obs = _run_bash("sleep 60", timeout=1)
    assert obs.is_error
    assert "timed out" in obs.text.lower()


# ---------------------------------------------------------------------------
# GrepTool
# ---------------------------------------------------------------------------

from agent.tools.grep import GrepAction, GrepTool


@pytest.fixture
def repo_dir():
    """Create a tiny fake repo for grep tests."""
    with tempfile.TemporaryDirectory() as d:
        (open(os.path.join(d, "a.py"), "w")).write(
            "def foo():\n    return 42\n\ndef bar():\n    pass\n"
        )
        (open(os.path.join(d, "b.py"), "w")).write(
            "# This file calls foo\nresult = foo()\n"
        )
        (open(os.path.join(d, "notes.txt"), "w")).write("foo is a function\n")
        yield d


def _run_grep(path, pattern, **kwargs):
    tool = GrepTool.create()[0]
    return tool(GrepAction(path=path, pattern=pattern, **kwargs))


def test_grep_finds_matches(repo_dir):
    obs = _run_grep(repo_dir, "def foo")
    assert not obs.is_error
    assert "def foo" in obs.text
    assert "a.py" in obs.text


def test_grep_include_filter(repo_dir):
    obs = _run_grep(repo_dir, "foo", include="*.py")
    assert not obs.is_error
    assert "a.py" in obs.text
    # notes.txt is excluded by filter
    assert "notes.txt" not in obs.text


def test_grep_context_lines(repo_dir):
    obs = _run_grep(repo_dir, "return 42", context_lines=1)
    # Should include the line before (def foo():)
    assert "def foo" in obs.text


def test_grep_no_matches(repo_dir):
    obs = _run_grep(repo_dir, "nonexistent_xyz_pattern")
    assert "No matches found" in obs.text


def test_grep_invalid_regex(repo_dir):
    obs = _run_grep(repo_dir, "[invalid(regex")
    assert obs.is_error


def test_grep_ignore_case(repo_dir):
    obs = _run_grep(repo_dir, "DEF FOO", ignore_case=True)
    assert "def foo" in obs.text


# ---------------------------------------------------------------------------
# SmartReadTool
# ---------------------------------------------------------------------------

from agent.tools.smart_read import SmartReadAction, SmartReadTool


@pytest.fixture
def sample_file():
    """Create a temporary file with 10 numbered lines."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        for i in range(1, 11):
            f.write(f"line {i}\n")
        path = f.name
    yield path
    os.unlink(path)


def _run_smart_read(**kwargs):
    tool = SmartReadTool.create()[0]
    action = SmartReadAction(**kwargs)
    return tool(action)


def test_smart_read_full_file(sample_file):
    obs = _run_smart_read(path=sample_file)
    assert not obs.is_error
    for i in range(1, 11):
        assert f"line {i}" in obs.text


def test_smart_read_line_range(sample_file):
    obs = _run_smart_read(path=sample_file, start_line=3, end_line=5)
    assert not obs.is_error
    assert "line 3" in obs.text
    assert "line 5" in obs.text
    assert "line 1" not in obs.text
    assert "line 6" not in obs.text


def test_smart_read_start_only(sample_file):
    obs = _run_smart_read(path=sample_file, start_line=8)
    assert not obs.is_error
    assert "line 8" in obs.text
    assert "line 10" in obs.text
    assert "line 7" not in obs.text


def test_smart_read_missing_file():
    obs = _run_smart_read(path="/nonexistent/file.py")
    assert obs.is_error
    assert "not found" in obs.text.lower()


def test_smart_read_includes_line_numbers(sample_file):
    obs = _run_smart_read(path=sample_file, start_line=1, end_line=3)
    assert " | " in obs.text


# ---------------------------------------------------------------------------
# Tool registry
# ---------------------------------------------------------------------------

def test_custom_tools_registered():
    registered = list_registered_tools()
    assert "smart_read" in registered
    assert "bash" in registered
    assert "grep" in registered


def test_terminal_tool_registered():
    from openhands.tools.terminal.definition import TerminalTool  # noqa: F401
    registered = list_registered_tools()
    assert "terminal" in registered


# ---------------------------------------------------------------------------
# TokenTracker
# ---------------------------------------------------------------------------

from agent.token_tracker import TokenTracker, make_token_callback


def test_token_tracker_record():
    tracker = TokenTracker(model="anthropic/claude-sonnet-4-6")
    tracker.record(step=1, input_tokens=100, output_tokens=50)
    tracker.record(step=2, input_tokens=200, output_tokens=80)

    assert tracker.total_input == 300
    assert tracker.total_output == 130
    assert len(tracker.steps) == 2


def test_token_tracker_cost():
    tracker = TokenTracker(model="anthropic/claude-sonnet-4-6")
    tracker.record(step=1, input_tokens=1_000_000, output_tokens=0)
    # 1M input tokens at $3.00/M
    assert abs(tracker.total_cost - 3.0) < 0.01


def test_token_tracker_model_prefix_stripped():
    """Cost lookup should work with 'anthropic/model' and 'model' alike."""
    t1 = TokenTracker(model="anthropic/claude-sonnet-4-6")
    t2 = TokenTracker(model="claude-sonnet-4-6")
    t1.record(step=1, input_tokens=1000, output_tokens=500)
    t2.record(step=1, input_tokens=1000, output_tokens=500)
    assert abs(t1.total_cost - t2.total_cost) < 1e-9


def test_make_token_callback():
    tracker = TokenTracker(model="anthropic/claude-sonnet-4-6")
    cb = make_token_callback(tracker)

    class FakeUsage:
        prompt_tokens = 100
        completion_tokens = 40

    class FakeChunk:
        usage = FakeUsage()

    cb(FakeChunk())
    assert tracker.total_input == 100
    assert tracker.total_output == 40
