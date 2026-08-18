# Spec List

Work is done when this list empties, documents match reality, and the blind comparison
against the Shape Up anchor passes. Each spec closes in one commit with documents updated.

- [x] **S0 — Anchor study + transcript.** design/ANCHOR-NOTES.md distilled from the real
  Shape Up pitches; real transcript selected (Mixergy: Brady Lewis, Allmoxy — cabinet-shop
  operations) and `examples/fetch_transcript.sh` fetches it.
- [x] **S1 — Skeleton + checks.** Package layout per blueprint; `schema.py`; `checks.py`
  (verbatim with canonical fold, lexicon exempting quotes, ref integrity) with unit tests
  covering the fold table (curly quotes, em-dash, ellipsis, nbsp, case); `groundwork check`.
- [x] **S2 — Renderer.** `render.py`: proposal.json → proposal.md; code assignment in
  document order; `{ref:slug}` substitution; page one (compressed read) then the five
  sections. Golden-file test on a handwritten fixture.
- [x] **S3 — Judgment core.** `prompt.py` (contract + anchor register from ANCHOR-NOTES)
  and `engine.py` (provider call → parse → checks → one corrective retry covering both
  check-reds and parse failures). Anthropic provider only.
- [x] **S4 — First real run.** Fetch transcript, `groundwork generate`, checks green,
  commit `examples/proposal.md` + `proposal.json`. Honest verdict in design/NOTES.md:
  startlingly better than slop, or a finding — if a finding, stop and report.
- [x] **S5 — Provider switch.** `codex_provider.py` + `openrouter_provider.py` (default
  model resolved against the live catalog); `GROUNDWORK_PROVIDER`; graceful errors when
  credentials are missing.
- [x] **S6 — README, blind comparison, publish.** README quickstart for all three
  connection paths. Blind comparison: a fresh-context examiner receives the proposal and
  the anchor mechanics (not the build history) and scores each mechanic; result recorded
  in design/CLOSING.md. Create public repo `5000Stadia/groundwork`, push.
- [x] **S7 — `--client` flag.** `groundwork generate transcript.txt --client "..."` names
  the intended client, removing the ambiguity found in S4. Plan (as reviewed):
  `prompt.user_prompt(transcript, client=None)` — when client is given, the default
  "treat the operator as the client" sentence is REPLACED (not appended to) by a steer
  that draws every pain, opportunity, and quote solely from moments about that client,
  allows other ventures only as context or honest no's, and takes `client_name` from the
  transcript rather than the flag string. `engine.generate` threads `client` through both
  the first attempt AND the corrective retry (pinned by a test where attempt 1 fails and
  the second captured input still carries the steer). Checks, renderer, schema, and
  `groundwork check` stay client-agnostic — no mismatch check, no schema field.
  Proof: second real run on the same transcript targeting the cabinet-shop era,
  committed as `examples/proposal-lewis-cabinet.*` (checks green), blind-compared
  against the anchor like the first example (score appended to CLOSING.md), README
  updated with the two-clients-one-transcript contrast.
