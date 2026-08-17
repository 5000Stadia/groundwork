"""Provider selection: GROUNDWORK_PROVIDER = anthropic (default) | openai-codex | openrouter.

Each provider exposes `complete(system: str, user: str) -> str`.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

PROVIDERS = ("anthropic", "openai-codex", "openrouter")


def resolve_provider():
    name = os.getenv("GROUNDWORK_PROVIDER", "anthropic").strip().lower()
    if name == "anthropic":
        from .anthropic_provider import AnthropicProvider

        return AnthropicProvider()
    if name == "openai-codex":
        from .codex_provider import CodexProvider

        return CodexProvider()
    if name == "openrouter":
        from .openrouter_provider import OpenRouterProvider

        return OpenRouterProvider()
    raise ValueError(f"GROUNDWORK_PROVIDER must be one of {PROVIDERS}, got {name!r}")
