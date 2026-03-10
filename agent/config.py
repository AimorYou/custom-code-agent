"""
Agent configuration loaded from environment variables / .env file.

Model ID format:  <provider>/<model-name>
  The provider is always the FIRST segment; model name is everything after it.

  Anthropic:          anthropic/claude-sonnet-4-6
  OpenAI:             openai/gpt-4o
  OpenAI-compatible:  openai/qwen/qwen3-coder-next  +  AGENT_BASE_URL=https://api.example.com/v1
                      openai/llama3                  +  AGENT_BASE_URL=http://localhost:11434/v1

  With a custom base URL, litellm strips "openai/" and sends the rest as the model name
  to the API (e.g. "qwen/qwen3-coder-next" → sent as-is to AGENT_BASE_URL).

API key resolution order:
    1. AGENT_API_KEY  (universal override)
    2. ANTHROPIC_API_KEY  (if provider == "anthropic")
    3. OPENAI_API_KEY     (if provider == "openai")
"""

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


def _resolve_api_key(model: str) -> str | None:
    if key := os.getenv("AGENT_API_KEY"):
        return key
    provider = model.split("/")[0].lower() if "/" in model else ""
    if provider == "anthropic":
        return os.getenv("ANTHROPIC_API_KEY")
    if provider == "openai":
        return os.getenv("OPENAI_API_KEY")
    return os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")


@dataclass
class AgentConfig:
    # litellm model ID: "anthropic/claude-sonnet-4-6", "openai/gpt-4o", etc.
    model: str = field(
        default_factory=lambda: os.getenv("AGENT_MODEL", "anthropic/claude-sonnet-4-6")
    )
    # Optional custom base URL — for OpenAI-compatible APIs (Ollama, vLLM, Groq, etc.)
    # Example: AGENT_BASE_URL=http://localhost:11434/v1
    base_url: str | None = field(
        default_factory=lambda: os.getenv("AGENT_BASE_URL") or None
    )
    max_steps: int = field(
        default_factory=lambda: int(os.getenv("AGENT_MAX_STEPS", "50"))
    )
    working_dir: str = field(
        default_factory=lambda: os.path.abspath(os.getenv("AGENT_WORKING_DIR", "."))
    )
    verbose: bool = field(
        default_factory=lambda: os.getenv("AGENT_VERBOSE", "true").lower() == "true"
    )
    # Comma-separated tool names to disable (e.g. "bash,grep")
    disabled_tools: list[str] = field(
        default_factory=lambda: [
            t.strip()
            for t in os.getenv("AGENT_DISABLED_TOOLS", "").split(",")
            if t.strip()
        ]
    )

    @property
    def api_key(self) -> str | None:
        return _resolve_api_key(self.model)
