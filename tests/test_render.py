import json

from groundwork.render import assign_codes, render
from groundwork.schema import Proposal

from fixture import make_proposal


def test_codes_assigned_in_document_order():
    codes = assign_codes(make_proposal())
    assert codes == {"opp-invoicing": "O1", "no-erp": "N1", "q-order-volume": "Q1"}


def test_refs_substituted_and_no_placeholders_remain():
    md = render(make_proposal())
    assert "{ref:" not in md
    assert "O1" in md and "N1" in md and "Q1" in md


def test_page_one_comes_first_and_sections_in_order():
    md = render(make_proposal())
    order = [
        md.index("## What we heard"),
        md.index("## Opportunity map"),
        md.index("## What we'd say no to"),
        md.index("## Recommended path"),
        md.index("## Open questions"),
    ]
    assert order == sorted(order)
    assert md.index("O2 yes, but N1 worries me") < order[0]  # addressability note on page one


def test_quotes_render_as_blockquotes():
    md = render(make_proposal())
    assert "> “We’re probably losing — I don’t know — forty hours a month just on invoicing.”" in md


def test_roundtrip_through_json():
    doc = make_proposal()
    again = Proposal.from_dict(json.loads(json.dumps(doc.to_dict())))
    assert render(again) == render(doc)


def test_render_survives_unknown_effort():
    doc = make_proposal()
    doc.opportunities[0].effort = "XL"
    assert "XL" in render(doc)  # no KeyError; engine blocks this upstream anyway
