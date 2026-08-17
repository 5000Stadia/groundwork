"""Default path: the Anthropic API via the official SDK.

Credentials resolve the standard way (ANTHROPIC_API_KEY from .env or the
environment, ANTHROPIC_AUTH_TOKEN, or an `ant auth login` profile). Adaptive
thinking is the model default — no thinking parameter is sent.
"""

from __future__ import annotations

import os


class AnthropicProvider:
    name = "anthropic"

    def __init__(self) -> None:
        import anthropic

        self._client = anthropic.Anthropic()
        self._model = os.getenv("GROUNDWORK_ANTHROPIC_MODEL", "claude-opus-5")

    def complete(self, system: str, user: str) -> str:
        with self._client.messages.stream(
            model=self._model,
            max_tokens=32000,
            system=system,
            messages=[{"role": "user", "content": user}],
        ) as stream:
            message = stream.get_final_message()

        if message.stop_reason == "refusal":
            raise RuntimeError(
                "the model declined this request (stop_reason=refusal); "
                "nothing in a discovery transcript should normally trigger this — retry or "
                "inspect the transcript"
            )
        text = "".join(b.text for b in message.content if b.type == "text")
        if message.stop_reason == "max_tokens":
            raise RuntimeError(
                "output truncated at max_tokens — transcript may be too large; "
                f"got {len(text)} chars"
            )
        return text
