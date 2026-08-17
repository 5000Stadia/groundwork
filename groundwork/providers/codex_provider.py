"""ChatGPT OAuth path — NOT api.openai.com.

Talks to OpenAI's consumer backend (chatgpt.com/backend-api/codex/responses),
the same endpoint the Codex CLI uses, authenticated with the ChatGPT OAuth
tokens from `codex login`. The wire shape mirrors the contract Kernos
established for this backend; Groundwork sends no tools, so the payload is a
small subset, but the load-bearing headers are kept.
"""

from __future__ import annotations

import json
import os
import platform
import time
import uuid

from ..credentials import (
    CodexCredential, refresh_codex_credential, resolve_codex_credential,
)


class CodexProvider:
    name = "openai-codex"

    def __init__(self) -> None:
        self._creds: CodexCredential = resolve_codex_credential()
        self._model = os.getenv("GROUNDWORK_CODEX_MODEL", "gpt-5.6-sol")
        self._base = os.getenv("GROUNDWORK_CODEX_BASE_URL", "https://chatgpt.com/backend-api")

    # -- auth --------------------------------------------------------------

    def _ensure_fresh(self) -> None:
        if self._creds["expires"] and self._creds["expires"] > (time.time() + 300) * 1000:
            return
        self._creds = refresh_codex_credential(self._creds)

    def _headers(self, session_id: str) -> dict[str, str]:
        ua = f"pi ({platform.system()} {platform.release()}; {platform.machine()})"
        return {
            # OAuth bearer — the consumer backend rejects API keys here.
            "Authorization": f"Bearer {self._creds['access']}",
            "chatgpt-account-id": self._creds["accountId"],
            # Known-transport identity; other values get rate-limited.
            "originator": "pi",
            "User-Agent": ua,
            "Content-Type": "application/json",
            "OpenAI-Beta": "responses=experimental",
            "accept": "text/event-stream",
            "session_id": session_id,
            "x-client-request-id": session_id,
        }

    # -- request -----------------------------------------------------------

    def complete(self, system: str, user: str) -> str:
        import httpx

        self._ensure_fresh()
        session_id = str(uuid.uuid4())
        body = {
            "model": self._model,
            # System prompt goes in `instructions` — this endpoint rejects
            # system roles inside `input`.
            "instructions": system,
            "input": [
                {"role": "user", "content": [{"type": "input_text", "text": user}]},
            ],
            "store": False,      # required: no backend persistence
            "stream": True,      # required: endpoint is SSE-only
            "reasoning": {"effort": os.getenv("GROUNDWORK_CODEX_EFFORT", "medium"),
                          "summary": "auto"},
            "text": {"verbosity": "medium"},
            "include": ["reasoning.encrypted_content"],
            "prompt_cache_key": session_id,
        }
        url = f"{self._base}/codex/responses"

        with httpx.Client(timeout=httpx.Timeout(300.0, connect=15.0)) as client:
            for attempt in (1, 2):
                with client.stream("POST", url, json=body,
                                   headers=self._headers(session_id)) as resp:
                    if resp.status_code == 401 and attempt == 1:
                        self._creds = refresh_codex_credential(self._creds)
                        continue
                    if resp.status_code != 200:
                        detail = resp.read().decode(errors="replace")[:500]
                        raise RuntimeError(f"codex backend HTTP {resp.status_code}: {detail}")
                    return self._read_sse(resp)
        raise RuntimeError("codex backend: unreachable after token refresh")

    @staticmethod
    def _read_sse(resp) -> str:
        chunks: list[str] = []
        final: str | None = None
        for line in resp.iter_lines():
            if not line.startswith("data:"):
                continue
            payload = line[5:].strip()
            if payload == "[DONE]":
                break
            try:
                event = json.loads(payload)
            except json.JSONDecodeError:
                continue
            etype = event.get("type", "")
            if etype == "response.output_text.delta":
                chunks.append(event.get("delta", ""))
            elif etype == "response.completed":
                out = []
                for item in event.get("response", {}).get("output", []):
                    if item.get("type") == "message":
                        for part in item.get("content", []):
                            if part.get("type") == "output_text":
                                out.append(part.get("text", ""))
                final = "".join(out)
            elif etype in ("response.failed", "error"):
                raise RuntimeError(f"codex backend stream error: {json.dumps(event)[:500]}")
        if final is not None and final:
            return final
        return "".join(chunks)
