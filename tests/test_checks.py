from groundwork.checks import (
    check_lexicon, check_refs, check_verbatim, fold, run_all,
)

from fixture import TRANSCRIPT, make_proposal


# --- fold table -------------------------------------------------------------

def test_fold_curly_apostrophe():
    assert fold("we’re") == fold("we're")

def test_fold_curly_double_quotes():
    assert fold("“hello”") == fold('"hello"')

def test_fold_em_dash():
    assert fold("losing — forty hours") == fold("losing - forty hours")

def test_fold_ellipsis_char():
    assert fold("well…") == fold("well...")

def test_fold_nbsp_and_case():
    assert fold("Forty Hours") == fold("forty hours")

def test_fold_collapses_whitespace():
    assert fold("a  b\n\tc") == "a b c"


# --- verbatim ---------------------------------------------------------------

def test_ascii_folded_copy_of_curly_source_passes():
    doc = make_proposal()
    # Model copied the curly-quote transcript in plain ASCII:
    doc.opportunities[0].quotes = [
        "We're probably losing - I don't know - forty hours a month just on invoicing."
    ]
    assert check_verbatim(doc, TRANSCRIPT) == []

def test_fabricated_quote_goes_red():
    doc = make_proposal()
    doc.pains[0].quotes = ["We are hemorrhaging money on manual data entry."]
    failures = check_verbatim(doc, TRANSCRIPT)
    assert len(failures) == 1 and failures[0].check == "verbatim"

def test_elided_quote_goes_red():
    doc = make_proposal()
    doc.pains[0].quotes = ["My office manager ... by hand."]
    failures = check_verbatim(doc, TRANSCRIPT)
    assert failures and "ellipsis" in failures[0].detail

def test_near_miss_paraphrase_goes_red():
    doc = make_proposal()
    doc.pains[0].quotes = ["My office manager types every fax into a spreadsheet by hand."]
    assert check_verbatim(doc, TRANSCRIPT)


# --- lexicon ----------------------------------------------------------------

def test_slop_in_authored_prose_goes_red():
    doc = make_proposal()
    doc.page_one = "We will leverage AI-powered solutions to streamline your workflow."
    failures = check_lexicon(doc)
    terms = {f.detail.split("'")[1] for f in failures}
    assert "leverage" in terms and "streamline" in terms

def test_slop_inside_client_quote_is_exempt():
    doc = make_proposal()
    doc.pains[0].quotes = ["My office manager types every fax into Excel by hand."]
    # Client's own words containing a banned term must not trip the check:
    doc.honest_nos[0].quotes = [
        "I asked about one of those big ERP systems but the quote was $150k and eighteen months."
    ]
    doc.honest_nos[0].what_they_raised = "You asked about the big system a vendor pitched as a way to streamline everything."
    failures = check_lexicon(doc)
    # the authored field trips; add a quote-only variant:
    assert any(f.path.endswith("what_they_raised") for f in failures)
    doc.honest_nos[0].what_they_raised = "You asked about the big system a vendor quoted."
    assert check_lexicon(doc) == []


# --- refs -------------------------------------------------------------------

def test_unresolved_ref_goes_red():
    doc = make_proposal()
    doc.page_one = "We'd start with {ref:opp-nonexistent}."
    failures = check_refs(doc)
    assert failures and "does not resolve" in failures[0].detail

def test_bare_code_in_prose_goes_red():
    doc = make_proposal()
    doc.recommended_path.first_move = "Start with O1 immediately."
    failures = check_refs(doc)
    assert failures and "bare code" in failures[0].detail

def test_number_without_basis_goes_red():
    doc = make_proposal()
    doc.opportunities[0].impact = "Save $4,000 a month."
    doc.opportunities[0].impact_basis = "  "
    failures = check_refs(doc)
    assert failures and "basis" in failures[0].detail


# --- integration ------------------------------------------------------------

def test_fixture_is_fully_green():
    assert run_all(make_proposal(), TRANSCRIPT) == []


def test_ref_to_pain_goes_red():
    doc = make_proposal()
    doc.page_one = "The core problem is {ref:pain-retyping}."
    failures = check_refs(doc)
    assert failures and "pains have no codes" in failures[0].detail
