# Closing

## Blind comparison (2026-08-17)

Procedure: a fresh-context examiner received only `examples/proposal.md` and
`design/ANCHOR-NOTES.md` — no build history — and scored the proposal against the
eight honesty mechanics distilled from the real Shape Up pitches.

**Result: MEETS ANCHOR — 8/8 PASS.**

- "Would a reader plausibly think 'these people actually listened'?" — *"Yes,
  unambiguously. The proposal quotes Brady roughly two dozen times... and references
  specifics no template contains — the cabin retreat, the eight-hour order-entry job,
  the failed paid chat add-on, 'ChapStick to hamburgers.'"*
- Generic-consulting-output scan: *"Almost nothing... Nothing else on the page could
  be pasted into another client's deck without breaking."* Closest candidate: the O3
  first slice's trade-show follow-up shape (still anchored to Brady's own numbers).
- Only cosmetic shortfall noted: no literal timestamps on quotes (the transcript
  itself carries none).

## Artifact examination

A fresh-context examiner reviewed the implementation against the intention and
blueprint (having not seen the build), running the suite and demonstrating claims
with concrete inputs. Findings: 5 MAJOR, 5 MINOR — all ten fixed in one round,
each with a regression test where testable:

- Structural failures (bad enums, string-typed lists, malformed slugs) now
  short-circuit the checks and share the parse-retry path instead of crashing the
  renderer or passing as "char-soup" quotes.
- Malformed `{ref:}` slugs can no longer leak raw placeholders into a client
  document while checks report green.
- Quotes containing speaker labels (or spanning speaker turns) go red.
- `impact_basis` is required non-empty for every opportunity (stricter than the
  original number-pattern scan, which missed most realistic formats).
- Q1–Q4 quarter vocabulary no longer false-positives the bare-code scan.
- CLI, OpenRouter, and Codex error paths fail with actionable messages instead of
  tracebacks (`codex login` hint, truncation hints, friendly `check` errors).

Suite at close: 35 tests green. The committed example re-verified green under the
stricter checks without modification.

## Spec list at close

S0–S5 closed; S6 closed except the physical push, which was blocked on GitHub
re-authentication (`gh` keyring token invalid, no SSH keys) at the time of writing.
The repo is fully commit-ready: run `gh auth login -h github.com`, then
`gh repo create 5000Stadia/groundwork --public --source . --push`.
