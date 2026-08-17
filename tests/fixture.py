"""A small handwritten proposal + matching transcript for tests."""

from groundwork.schema import (
    HonestNo, OpenQuestion, Opportunity, Pain, Proposal, RecommendedPath,
)

TRANSCRIPT = """\
Dana: So walk me through a typical week.

Sam: Honestly? We’re probably losing — I don’t know — forty hours a month just on invoicing. \
My office manager types every fax into Excel by hand. It takes forever.

Dana: And collections?

Sam: We’d find out an invoice was past due two months later. We got taken for $40,000 last year. \
I asked about one of those big ERP systems but the quote was $150k and eighteen months.
"""


def make_proposal() -> Proposal:
    return Proposal(
        client_name="Sam's Cabinet Shop",
        business="A family cabinet shop taking orders by fax and phone.",
        page_one=(
            "You are paying twice for every order: once to make it and once to type it. "
            "We'd start with {ref:opp-invoicing} and hold off on {ref:no-erp}."
        ),
        pains=[
            Pain(
                id="pain-retyping",
                headline="Every order is typed in twice",
                quotes=["My office manager types every fax into Excel by hand."],
                why_it_hurts="A full-time person's week disappears into copying, not making.",
            ),
        ],
        opportunities=[
            Opportunity(
                id="opp-invoicing",
                title="Invoices that send themselves",
                moment="When Dana asked about a typical week, the first thing named was invoicing.",
                quotes=["We’re probably losing — I don’t know — forty hours a month just on invoicing."],
                effort="S",
                impact="Roughly forty hours a month back, by your own count.",
                impact_basis="Sam's own estimate on the call; worth confirming against a week's timesheets.",
                confidence="high",
                confidence_reason="The pain was named unprompted and the fix is well-trodden.",
                first_slice="Auto-generate invoices from the existing Excel sheet for two weeks, in parallel with the current process.",
            ),
        ],
        honest_nos=[
            HonestNo(
                id="no-erp",
                title="A full ERP system",
                what_they_raised="You asked about the big system a vendor quoted.",
                quotes=["I asked about one of those big ERP systems but the quote was $150k and eighteen months."],
                why_not=(
                    "An ERP would eventually cover invoicing too, and a good one is genuinely "
                    "impressive. But eighteen months is longer than this problem deserves, and "
                    "most of what it fixes you don't have."
                ),
            ),
        ],
        recommended_path=RecommendedPath(
            first_move="Two weeks on {ref:opp-invoicing}, run beside the current process so nothing breaks.",
            then_layers=["Collections alerts once invoices are structured data."],
        ),
        open_questions=[
            OpenQuestion(
                id="q-order-volume",
                question="How many orders arrive in a normal month?",
                assumption="We assumed 150–300 based on one person spending full days typing.",
                quotes=["It takes forever."],
            ),
        ],
    )
