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


def test_structurally_broken_twice_raises_not_renders():
    bad = make_proposal()
    bad.opportunities[0].effort = "XL"
    provider = FakeProvider(json.dumps(bad.to_dict()), json.dumps(bad.to_dict()))
    with pytest.raises(ParseError) as exc:
        generate(TRANSCRIPT, provider=provider)
    assert "effort" in str(exc.value)


# --- S7: --client steer ------------------------------------------------------

def test_client_steer_replaces_operator_sentence():
    from groundwork.prompt import user_prompt

    default = user_prompt(TRANSCRIPT)
    steered = user_prompt(TRANSCRIPT, "Lewis Cabinet Company")
    assert "operator being interviewed" in default
    assert "operator being interviewed" not in steered
    assert "Lewis Cabinet Company" in steered
    assert "never borrow their moments" in steered


def test_client_steer_survives_the_corrective_retry():
    bad = make_proposal()
    bad.page_one = "We will streamline everything."  # planted lexicon red
    provider = FakeProvider(json.dumps(bad.to_dict()), good_json())
    result = generate(TRANSCRIPT, provider=provider, client="Lewis Cabinet Company")
    assert result.failures == []
    assert len(provider.calls) == 2
    for _, user in provider.calls:  # steer present on BOTH attempts
        assert "Lewis Cabinet Company" in user
        assert "operator being interviewed" not in user
