# Groundwork

Turns a raw discovery conversation into the document a client would actually pay for.

Paste in a discovery-call transcript or messy notes; Groundwork produces one proposal
document:

- **What we heard** — the client's pains, ranked, quoted in their own words
- **Opportunity map** — each opportunity grounded in a specific moment from the call,
  with effort (S/M/L as appetite, not estimate), impact in the client's own currency
  with its stated basis, and confidence
- **What we'd say no to** — the things the client asked about that aren't worth doing,
  argued honestly. This is the credibility section; generic tools structurally can't
  write it
- **Recommended path** — the smallest thing that proves value in weeks, then layers
- **Open questions** — with our working assumptions named

Every opportunity, no, and question carries a code (O1, N2, Q3), so a client can reply
**"O3 yes, but N2 worries me"** — the document is conversationally addressable.

The register is modeled on Basecamp's [Shape Up pitches](https://basecamp.com/shapeup):
problems shown as evidence, alternatives killed on the page, no-gos stated plainly.

## The checks can go red

Trust is mechanical here, not aspirational. Every generation is verified:

1. **Verbatim** — every quote must appear character-for-character in the input
   (punctuation style, case, and whitespace are the only forgiveness — the exact fold
   table is data in [`groundwork/checks.py`](groundwork/checks.py)). No elision,
   no stitched-together quotes.
2. **Lexicon** — a banned list of consulting slop (leverage, streamline, synergy,
   seamless, AI-powered, and their cousins) enforced over everything Groundwork writes.
   Client quotes are exempt: their vocabulary always wins.
3. **References** — every cross-reference resolves; every number carries its stated basis.

A red check triggers one corrective retry with the specific failures; still red means
`generate` exits nonzero and tells you not to hand the document to a client. Re-verify
any proposal later with:

```
groundwork check proposal.json transcript.txt
```

## Example, on a real conversation

[`examples/proposal.md`](examples/proposal.md) was generated from a real published
conversation: Mixergy's interview with Brady Lewis, a cabinet-shop operator describing
faxes retyped into Excel eight hours a day, invoices discovered past due months later,
and $40k bad-debt hits. Run `examples/fetch_transcript.sh` to pull the transcript
(it isn't committed — it's Mixergy's) and reproduce it:

```
./examples/fetch_transcript.sh
groundwork generate examples/transcript.txt -o examples/proposal.md
```

## Install

```
git clone https://github.com/5000Stadia/groundwork && cd groundwork
python3 -m venv .venv && .venv/bin/pip install -e .
cp .env.example .env   # then pick a connection path below
```

## Connection paths

Groundwork calls an LLM at runtime. Pick one of three paths via `GROUNDWORK_PROVIDER`
in `.env`:

### 1. Anthropic (default)

```
GROUNDWORK_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
```

Uses the official SDK with `claude-opus-5` (override with `GROUNDWORK_ANTHROPIC_MODEL`).
Any credential source the SDK understands works — an `ant auth login` profile also
resolves without a key in `.env`.

### 2. ChatGPT OAuth (`openai-codex`)

```
GROUNDWORK_PROVIDER=openai-codex
```

No API key. If you use the Codex CLI, `codex login` is all you need: Groundwork reads
`~/.codex/auth.json`, keeps its own copy in `.credentials/openai-codex.json`
(gitignored), refreshes expired access tokens via OAuth, and re-syncs automatically
when a fresh `codex login` rotates them. This talks to the ChatGPT consumer backend
(`chatgpt.com/backend-api/codex/responses`), not the OpenAI platform API — usage
draws on your ChatGPT plan. Model override: `GROUNDWORK_CODEX_MODEL`.

### 3. OpenRouter

```
GROUNDWORK_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-...
```

Model override: `GROUNDWORK_OPENROUTER_MODEL` (default `anthropic/claude-opus-5`).

## Usage

```
groundwork generate transcript.txt -o proposal.md   # writes proposal.md + proposal.json
groundwork check proposal.json transcript.txt        # re-run the mechanical checks
```

## Development

```
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest
```

The `design/` directory contains the working documents this project was built against
(intention, blueprint, spec list, anchor study) — the build process is part of the
portfolio.
