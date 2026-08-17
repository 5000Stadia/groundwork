"""The proposal document: dataclasses, JSON (de)serialization, field traversal.

Slug ids are chosen by the LLM (`opp-invoicing`, `no-full-erp`, `q-order-volume`).
Prose fields cross-reference items with `{ref:<slug>}` placeholders; display codes
(O1, N2, Q3) are assigned by the renderer, never by the LLM.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Iterator

EFFORTS = ("S", "M", "L")
CONFIDENCES = ("high", "medium", "low")


@dataclass
class Pain:
    id: str
    headline: str          # in plain words, close to the client's own
    quotes: list[str]      # verbatim, contiguous, single-speaker spans
    why_it_hurts: str      # prose: consequence in the client's terms


@dataclass
class Opportunity:
    id: str
    title: str
    moment: str            # the specific moment in the call this came from
    quotes: list[str]
    effort: str            # S | M | L — appetite, not estimate
    impact: str            # in the client's own currency (hours, dollars, headaches)
    impact_basis: str      # where the number/claim comes from: a quote or a named assumption
    confidence: str        # high | medium | low
    confidence_reason: str
    first_slice: str       # the smallest concrete piece that proves value


@dataclass
class HonestNo:
    id: str
    title: str
    what_they_raised: str  # what the client asked about or implied wanting
    quotes: list[str]
    why_not: str           # the argument against, made honestly — concede upside where real


@dataclass
class OpenQuestion:
    id: str
    question: str
    assumption: str        # our best guess, named as an assumption
    quotes: list[str] = field(default_factory=list)


@dataclass
class RecommendedPath:
    first_move: str        # smallest thing that proves value in weeks; may use {ref:...}
    then_layers: list[str] # each layer as prose; may use {ref:...}


@dataclass
class Proposal:
    client_name: str
    business: str          # one line: what the business is
    page_one: str          # the compressed read for a busy owner; may use {ref:...}
    pains: list[Pain]
    opportunities: list[Opportunity]
    honest_nos: list[HonestNo]
    recommended_path: RecommendedPath
    open_questions: list[OpenQuestion]

    # -- construction ------------------------------------------------------

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Proposal":
        return cls(
            client_name=d["client_name"],
            business=d["business"],
            page_one=d["page_one"],
            pains=[Pain(**p) for p in d["pains"]],
            opportunities=[Opportunity(**o) for o in d["opportunities"]],
            honest_nos=[HonestNo(**n) for n in d["honest_nos"]],
            recommended_path=RecommendedPath(**d["recommended_path"]),
            open_questions=[OpenQuestion(**q) for q in d["open_questions"]],
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def validate(self) -> list[str]:
        """Structural problems (not check failures): bad enums, duplicate ids."""
        problems = []
        ids = [x.id for x in (*self.pains, *self.opportunities, *self.honest_nos, *self.open_questions)]
        dupes = {i for i in ids if ids.count(i) > 1}
        if dupes:
            problems.append(f"duplicate ids: {sorted(dupes)}")
        for o in self.opportunities:
            if o.effort not in EFFORTS:
                problems.append(f"{o.id}: effort must be one of {EFFORTS}, got {o.effort!r}")
            if o.confidence not in CONFIDENCES:
                problems.append(f"{o.id}: confidence must be one of {CONFIDENCES}, got {o.confidence!r}")
        return problems

    # -- traversal (what the checks walk) ----------------------------------

    def iter_quotes(self) -> Iterator[tuple[str, str]]:
        """(path, quote) for every verbatim quote in the document."""
        for p in self.pains:
            for i, q in enumerate(p.quotes):
                yield f"pains.{p.id}.quotes[{i}]", q
        for o in self.opportunities:
            for i, q in enumerate(o.quotes):
                yield f"opportunities.{o.id}.quotes[{i}]", q
        for n in self.honest_nos:
            for i, q in enumerate(n.quotes):
                yield f"honest_nos.{n.id}.quotes[{i}]", q
        for oq in self.open_questions:
            for i, q in enumerate(oq.quotes):
                yield f"open_questions.{oq.id}.quotes[{i}]", q

    def iter_prose(self) -> Iterator[tuple[str, str]]:
        """(path, text) for every LLM-authored non-quote field.

        This is the surface the lexicon and ref checks scan. Quotes are exempt:
        the client's vocabulary always wins.
        """
        yield "page_one", self.page_one
        yield "business", self.business
        for p in self.pains:
            yield f"pains.{p.id}.headline", p.headline
            yield f"pains.{p.id}.why_it_hurts", p.why_it_hurts
        for o in self.opportunities:
            yield f"opportunities.{o.id}.title", o.title
            yield f"opportunities.{o.id}.moment", o.moment
            yield f"opportunities.{o.id}.impact", o.impact
            yield f"opportunities.{o.id}.impact_basis", o.impact_basis
            yield f"opportunities.{o.id}.confidence_reason", o.confidence_reason
            yield f"opportunities.{o.id}.first_slice", o.first_slice
        for n in self.honest_nos:
            yield f"honest_nos.{n.id}.title", n.title
            yield f"honest_nos.{n.id}.what_they_raised", n.what_they_raised
            yield f"honest_nos.{n.id}.why_not", n.why_not
        yield "recommended_path.first_move", self.recommended_path.first_move
        for i, layer in enumerate(self.recommended_path.then_layers):
            yield f"recommended_path.then_layers[{i}]", layer
        for q in self.open_questions:
            yield f"open_questions.{q.id}.question", q.question
            yield f"open_questions.{q.id}.assumption", q.assumption

    def all_ids(self) -> set[str]:
        return {x.id for x in (*self.pains, *self.opportunities, *self.honest_nos, *self.open_questions)}
