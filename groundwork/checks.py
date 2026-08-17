"""Mechanical checks. Each returns a list of Failure — empty means green.

These are the credibility floor of the whole tool: every claim traceable, no
consulting slop, every cross-reference resolving. A red check fails the build.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from .schema import Proposal

# ---------------------------------------------------------------------------
# Canonical fold — applied to BOTH sides before verbatim comparison.
#
# Transcripts arrive with typographic punctuation (curly quotes, em-dashes)
# and models ASCII-fold when copying. The fold below is the complete list of
# forgiveness this check grants; anything beyond it is a red.
# ---------------------------------------------------------------------------

_FOLD_TABLE = {
    "‘": "'", "’": "'", "‚": "'", "′": "'",  # curly/prime apostrophes
    "“": '"', "”": '"', "„": '"', "″": '"',  # curly double quotes
    "–": "-", "—": "-", "―": "-", "−": "-",  # dashes/minus
    "…": "...",                                             # ellipsis
    "\u00a0": " ", "\u202f": " ", "\u2009": " ",  # nbsp / narrow nbsp / thin space
}
_FOLD_RE = re.compile("|".join(map(re.escape, _FOLD_TABLE)))


def fold(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = _FOLD_RE.sub(lambda m: _FOLD_TABLE[m.group()], text)
    text = text.casefold()
    return re.sub(r"\s+", " ", text).strip()


@dataclass
class Failure:
    check: str   # "verbatim" | "lexicon" | "refs" | "structure"
    path: str    # where in the document
    detail: str  # human-readable, specific enough for the corrective retry


# ---------------------------------------------------------------------------
# Check 1: every quote appears verbatim in the transcript
# ---------------------------------------------------------------------------

_SPEAKER_LINE_RE = re.compile(r"^([A-Z][\w .'-]{0,30}):", re.MULTILINE)


def transcript_speakers(transcript: str) -> set[str]:
    """Names appearing as 'Name:' speaker labels at line starts."""
    return {m.group(1).strip() for m in _SPEAKER_LINE_RE.finditer(transcript)}


def check_verbatim(doc: Proposal, transcript: str) -> list[Failure]:
    haystack = fold(transcript)
    speakers = transcript_speakers(transcript)
    failures = []
    for path, quote in doc.iter_quotes():
        if not quote.strip():
            failures.append(Failure("verbatim", path, "empty quote"))
            continue
        hit = next((s for s in speakers if f"{s}:" in quote), None)
        if hit is not None:
            failures.append(Failure(
                "verbatim", path,
                f"quote contains the speaker label {hit + ':'!r} — a quote must be one "
                f"contiguous span by one speaker, with no labels inside: {quote!r}",
            ))
            continue
        if "..." in quote or "…" in quote:
            failures.append(Failure(
                "verbatim", path,
                f"quote contains an ellipsis — quotes must be contiguous spans, no elision: {quote!r}",
            ))
            continue
        if fold(quote) not in haystack:
            failures.append(Failure(
                "verbatim", path,
                f"quote does not appear verbatim in the source: {quote!r}",
            ))
    return failures


# ---------------------------------------------------------------------------
# Check 2: banned lexicon (LLM-authored fields only; client quotes exempt)
# ---------------------------------------------------------------------------

BANNED_LEXICON: list[str] = [
    r"leverag(?:e|ed|es|ing)",
    r"streamlin(?:e|ed|es|ing)",
    r"unlock(?:ing|s|ed)?\s+(?:value|potential|growth|efficienc)",
    r"synerg(?:y|ies|istic|ize)",
    r"AI-powered",
    r"AI[- ]driven",
    r"transformation(?:al)?\s+journey",
    r"digital\s+transformation",
    r"game[- ]chang(?:er|ing)",
    r"cutting[- ]edge",
    r"state[- ]of[- ]the[- ]art",
    r"best[- ]in[- ]class",
    r"world[- ]class",
    r"seamless(?:ly)?",
    r"robust(?:ly|ness)?",
    r"holistic(?:ally)?",
    r"paradigm",
    r"empower(?:s|ed|ing|ment)?",
    r"revolutioniz(?:e|es|ed|ing)",
    r"supercharg(?:e|es|ed|ing)",
    r"turnkey",
    r"low[- ]hanging\s+fruit",
    r"value[- ]add(?:ed)?",
    r"drive\s+(?:value|growth|efficiency|innovation)",
    r"harness(?:es|ed|ing)?\s+the\s+power",
    r"next[- ]level",
    r"end[- ]to[- ]end\s+solution",
    r"solutioning",
    r"deep[- ]dive",
    r"boil\s+the\s+ocean",
    r"move\s+the\s+needle",
    r"circle\s+back",
    r"double[- ]click",
    r"utiliz(?:e|es|ed|ing|ation)",
]
_BANNED_RES = [re.compile(p, re.IGNORECASE) for p in BANNED_LEXICON]


def check_lexicon(doc: Proposal) -> list[Failure]:
    failures = []
    for path, text in doc.iter_prose():
        for rx in _BANNED_RES:
            m = rx.search(text)
            if m:
                failures.append(Failure(
                    "lexicon", path,
                    f"banned term {m.group()!r} — say what you mean in the client's vocabulary",
                ))
    return failures


# ---------------------------------------------------------------------------
# Check 3: reference integrity + numbers carry a basis
# ---------------------------------------------------------------------------

_ANY_REF_RE = re.compile(r"\{ref:([^}]*)\}")
_SLUG_RE = re.compile(r"^[a-z0-9-]+$")
# O/N codes are always renderer-owned; Q1-Q4 followed by quarter vocabulary is
# ordinary business speech ("the Q4 rush"), not a display code.
_BARE_CODE_RE = re.compile(
    r"\b(?:[ON]\d+|Q(?:[5-9]|\d{2,})|Q[1-4](?!\s+(?:rush|quarter|sales|revenue|earnings|results|numbers|season)))\b")


def check_refs(doc: Proposal) -> list[Failure]:
    failures = []
    # Only coded items are referenceable: pains carry no display code, so a
    # {ref:} to a pain could never render.
    codeable = {x.id for x in (*doc.opportunities, *doc.honest_nos, *doc.open_questions)}
    for path, text in doc.iter_prose():
        for m in _ANY_REF_RE.finditer(text):
            slug = m.group(1)
            if not _SLUG_RE.match(slug):
                failures.append(Failure(
                    "refs", path,
                    f"malformed reference {m.group(0)!r} — slugs are lowercase letters, "
                    "digits, and hyphens only",
                ))
            elif slug not in codeable:
                failures.append(Failure(
                    "refs", path,
                    f"{{ref:{slug}}} does not resolve to a codeable item "
                    "(an opportunity, honest no, or open question — pains have no codes; "
                    "name the pain in words instead)",
                ))
        if _BARE_CODE_RE.search(text):
            failures.append(Failure(
                "refs", path,
                "bare code (O1/N2/Q3-style) in authored text — use {ref:<slug>}; codes are assigned by the renderer",
            ))
    return failures


# ---------------------------------------------------------------------------

def run_all(doc: Proposal, transcript: str) -> list[Failure]:
    structural = [Failure("structure", "document", p) for p in doc.validate()]
    if structural:
        return structural
    return check_verbatim(doc, transcript) + check_lexicon(doc) + check_refs(doc)


def report(failures: list[Failure]) -> str:
    if not failures:
        return "all checks green"
    lines = [f"{len(failures)} check failure(s):"]
    for f in failures:
        lines.append(f"  [{f.check}] {f.path}: {f.detail}")
    return "\n".join(lines)
