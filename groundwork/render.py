"""proposal.json -> proposal.md.

The renderer owns display codes: opportunities become O1..., honest no's N1...,
open questions Q1..., in document order. `{ref:<slug>}` placeholders in prose
are substituted with the assigned code. Pains carry no codes — they are heard,
not negotiated.
"""

from __future__ import annotations

import re

from .schema import Proposal

_REF_RE = re.compile(r"\{ref:([a-z0-9-]+)\}")


def assign_codes(doc: Proposal) -> dict[str, str]:
    codes: dict[str, str] = {}
    for i, o in enumerate(doc.opportunities, 1):
        codes[o.id] = f"O{i}"
    for i, n in enumerate(doc.honest_nos, 1):
        codes[n.id] = f"N{i}"
    for i, q in enumerate(doc.open_questions, 1):
        codes[q.id] = f"Q{i}"
    return codes


def _sub(text: str, codes: dict[str, str]) -> str:
    return _REF_RE.sub(lambda m: codes.get(m.group(1), m.group(0)), text)


_EFFORT_WORDS = {"S": "Small", "M": "Medium", "L": "Large"}


def render(doc: Proposal) -> str:
    codes = assign_codes(doc)
    s = lambda t: _sub(t, codes)  # noqa: E731
    out: list[str] = []

    # ---- Page one: the compressed read -----------------------------------
    out.append(f"# {doc.client_name} — What we heard, and what we'd do about it\n")
    out.append(f"*{s(doc.business)}*\n")
    out.append(s(doc.page_one).strip())
    out.append("")
    out.append(
        "*Everything below carries a code (O = opportunity, N = not worth doing, "
        "Q = open question). Reply with the codes — \"O2 yes, but N1 worries me\" "
        "is a complete answer.*")
    out.append("\n---\n")

    # ---- What we heard ----------------------------------------------------
    out.append("## What we heard\n")
    out.append("In your words, ranked by how much they seem to cost you:\n")
    for i, p in enumerate(doc.pains, 1):
        out.append(f"### {i}. {s(p.headline)}\n")
        for q in p.quotes:
            out.append(f"> “{q}”\n")
        out.append(s(p.why_it_hurts) + "\n")

    # ---- Opportunity map ---------------------------------------------------
    out.append("## Opportunity map\n")
    for o in doc.opportunities:
        code = codes[o.id]
        out.append(f"### {code} — {s(o.title)}\n")
        out.append(f"**Where this comes from:** {s(o.moment)}\n")
        for q in o.quotes:
            out.append(f"> “{q}”\n")
        out.append(f"**Effort:** {_EFFORT_WORDS.get(o.effort, o.effort)} · **Confidence:** {o.confidence} — {s(o.confidence_reason)}\n")
        out.append(f"**What it's worth:** {s(o.impact)}")
        out.append(f"  \n*Basis: {s(o.impact_basis)}*\n")
        out.append(f"**First slice:** {s(o.first_slice)}\n")

    # ---- The honest no's ---------------------------------------------------
    out.append("## What we'd say no to\n")
    out.append("Things that came up that we don't think are worth your money right now:\n")
    for n in doc.honest_nos:
        code = codes[n.id]
        out.append(f"### {code} — {s(n.title)}\n")
        out.append(f"{s(n.what_they_raised)}\n")
        for q in n.quotes:
            out.append(f"> “{q}”\n")
        out.append(f"{s(n.why_not)}\n")

    # ---- Recommended path --------------------------------------------------
    out.append("## Recommended path\n")
    out.append(f"**Start here:** {s(doc.recommended_path.first_move)}\n")
    if doc.recommended_path.then_layers:
        out.append("Then, in order:\n")
        for i, layer in enumerate(doc.recommended_path.then_layers, 1):
            out.append(f"{i}. {s(layer)}")
        out.append("")

    # ---- Open questions ----------------------------------------------------
    out.append("## Open questions\n")
    for q in doc.open_questions:
        code = codes[q.id]
        out.append(f"**{code} — {s(q.question)}**\n")
        for quote in q.quotes:
            out.append(f"> “{quote}”\n")
        out.append(f"*Our working assumption: {s(q.assumption)}*\n")

    return "\n".join(out).rstrip() + "\n"
