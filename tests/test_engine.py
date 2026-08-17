import json

import pytest

from groundwork.engine import ParseError, generate, parse_document

from fixture import TRANSCRIPT, make_proposal


class FakeProvider:
    def __init__(self, *responses: str):
        self.responses = list(responses)
        self.calls: list[tuple[str, str]] = []

    def complete(self, system: str, user: str) -> str:
        self.calls.append((system, user))
        return self.responses.pop(0)


def good_json() -> str:
    return json.dumps(make_proposal().to_dict())


def test_green_first_try():
    provider = FakeProvider(good_json())
    result = generate(TRANSCRIPT, provider=provider)
    assert result.failures == []
    assert "O1" in result.markdown
    assert len(provider.calls) == 1


def test_fenced_output_is_parsed():
    provider = FakeProvider("```json\n" + good_json() + "\n```")
    assert generate(TRANSCRIPT, provider=provider).failures == []


def test_red_then_corrected_retry():
    bad = make_proposal()
    bad.pains[0].quotes = ["We are hemorrhaging money on manual data entry."]  # fabricated
    provider = FakeProvider(json.dumps(bad.to_dict()), good_json())
    result = generate(TRANSCRIPT, provider=provider)
    assert result.failures == []
    assert len(provider.calls) == 2
    # the retry carries the specific failure and the previous output
    retry_user = provider.calls[1][1]
    assert "does not appear verbatim" in retry_user
    assert "hemorrhaging" in retry_user


def test_still_red_after_retry_is_reported_not_hidden():
    bad = make_proposal()
    bad.page_one = "We will streamline everything."
    provider = FakeProvider(json.dumps(bad.to_dict()), json.dumps(bad.to_dict()))
    result = generate(TRANSCRIPT, provider=provider)
    assert result.failures and result.failures[0].check == "lexicon"


def test_unparseable_twice_raises():
    provider = FakeProvider("not json at all", "still not json")
    with pytest.raises(ParseError):
        generate(TRANSCRIPT, provider=provider)


def test_parse_document_rejects_missing_fields():
    with pytest.raises(ParseError):
        parse_document('{"client_name": "x"}')
