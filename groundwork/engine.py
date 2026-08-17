"""Orchestration: prompt -> provider -> parse -> checks -> one corrective retry."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

from .checks import Failure, report, run_all
from .prompt import SYSTEM_PROMPT, retry_prompt, user_prompt
from .render import render
from .schema import Proposal


@dataclass
class Result:
    document: Proposal
    markdown: str
    failures: list[Failure] = field(default_factory=list)  # non-empty = red after retry


class ParseError(Exception):
    pass


_FENCE_RE = re.compile(r"^\s*```(?:json)?\s*|\s*```\s*$", re.MULTILINE)


def parse_document(text: str) -> Proposal:
    cleaned = _FENCE_RE.sub("", text).strip()
    # Tolerate leading/trailing prose by slicing to the outermost braces.
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start == -1 or end == -1:
        raise ParseError("no JSON object in model output")
    try:
        data = json.loads(cleaned[start : end + 1])
    except json.JSONDecodeError as exc:
        raise ParseError(f"invalid JSON: {exc}") from exc
    try:
        return Proposal.from_dict(data)
    except (KeyError, TypeError) as exc:
        raise ParseError(f"JSON does not match the document contract: {exc}") from exc


def generate(transcript: str, provider=None) -> Result:
    if provider is None:
        from .providers import resolve_provider

        provider = resolve_provider()

    attempt_input = user_prompt(transcript)
    doc: Proposal | None = None
    failures: list[Failure] = []

    for attempt in (1, 2):
        raw = provider.complete(SYSTEM_PROMPT, attempt_input)
        try:
            doc = parse_document(raw)
        except ParseError as exc:
            failures = [Failure("structure", "output", str(exc))]
            doc = None
        else:
            failures = run_all(doc, transcript)

        if not failures:
            break
        if attempt == 1:
            # One corrective pass, carrying the specific failures. The retry sees
            # the transcript again plus its own previous output.
            attempt_input = (
                user_prompt(transcript)
                + "\n\nYour previous attempt:\n" + raw
                + "\n\n" + retry_prompt(report(failures))
            )

    if doc is None:
        raise ParseError(
            "model output was not a valid document after retry:\n" + report(failures)
        )
    return Result(document=doc, markdown=render(doc), failures=failures)
