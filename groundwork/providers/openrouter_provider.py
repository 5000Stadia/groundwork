"""OpenRouter path: OPENROUTER_API_KEY, OpenAI-compatible chat completions."""

from __future__ import annotations

import os

DEFAULT_MODEL = "anthropic/claude-opus-5"


class OpenRouterProvider:
    name = "openrouter"

    def __init__(self) -> None:
        self._key = os.getenv("OPENROUTER_API_KEY", "")
        if not self._key:
            raise RuntimeError(
                "OPENROUTER_API_KEY is not set — add it to .env (see .env.example)"
            )
        self._model = os.getenv("GROUNDWORK_OPENROUTER_MODEL", DEFAULT_MODEL)

    def complete(self, system: str, user: str) -> str:
        import httpx

        resp = httpx.post(
            "https://openrouter.ai/api/v1/chat/completions",
            timeout=httpx.Timeout(300.0, connect=15.0),
            headers={
                "Authorization": f"Bearer {self._key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/5000Stadia/groundwork",
                "X-Title": "Groundwork",
            },
            json={
                "model": self._model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                "max_tokens": 32000,
            },
        )
        if resp.status_code != 200:
            raise RuntimeError(f"openrouter HTTP {resp.status_code}: {resp.text[:500]}")
        data = resp.json()
        try:
            choice = data["choices"][0]
            content = choice["message"]["content"]
        except (KeyError, IndexError) as exc:
            raise RuntimeError(f"openrouter: unexpected response shape: {str(data)[:500]}") from exc
        if not isinstance(content, str) or not content:
            raise RuntimeError(f"openrouter: empty/non-text content: {str(data)[:500]}")
        if choice.get("finish_reason") == "length":
            raise RuntimeError("openrouter: output truncated at max_tokens — transcript may be too large")
        return content
