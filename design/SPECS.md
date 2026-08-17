# Spec List

Work is done when this list empties, documents match reality, and the blind comparison
against the Shape Up anchor passes. Each spec closes in one commit with documents updated.

- [x] **S0 — Anchor study + transcript.** design/ANCHOR-NOTES.md distilled from the real
  Shape Up pitches; real transcript selected (Mixergy: Brady Lewis, Allmoxy — cabinet-shop
  operations) and `examples/fetch_transcript.sh` fetches it.
- [ ] **S1 — Skeleton + checks.** Package layout per blueprint; `schema.py`; `checks.py`
  (verbatim with canonical fold, lexicon exempting quotes, ref integrity) with unit tests
  covering the fold table (curly quotes, em-dash, ellipsis, nbsp, case); `groundwork check`.
- [ ] **S2 — Renderer.** `render.py`: proposal.json → proposal.md; code assignment in
  document order; `{ref:slug}` substitution; page one (compressed read) then the five
  sections. Golden-file test on a handwritten fixture.
- [ ] **S3 — Judgment core.** `prompt.py` (contract + anchor register from ANCHOR-NOTES)
  and `engine.py` (provider call → parse → checks → one corrective retry covering both
  check-reds and parse failures). Anthropic provider only.
- [ ] **S4 — First real run.** Fetch transcript, `groundwork generate`, checks green,
  commit `examples/proposal.md` + `proposal.json`. Honest verdict in design/NOTES.md:
  startlingly better than slop, or a finding — if a finding, stop and report.
- [ ] **S5 — Provider switch.** `codex_provider.py` + `openrouter_provider.py` (default
  model resolved against the live catalog); `GROUNDWORK_PROVIDER`; graceful errors when
  credentials are missing.
- [ ] **S6 — README, blind comparison, publish.** README quickstart for all three
  connection paths. Blind comparison: a fresh-context examiner receives the proposal and
  the anchor mechanics (not the build history) and scores each mechanic; result recorded
  in design/CLOSING.md. Create public repo `5000Stadia/groundwork`, push.
