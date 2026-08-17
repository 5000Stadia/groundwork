# Blueprint

## Shape

A Python CLI (`groundwork`), package layout:

```
groundwork/
  cli.py            # argparse: groundwork generate <transcript> [-o out.md]; groundwork check <proposal.json> <transcript>
  engine.py         # builds the prompt, calls the provider, parses JSON, runs checks, one corrective retry
  prompt.py         # the judgment core: system prompt + document contract (one home)
  schema.py         # dataclasses for the proposal document + JSON (de)serialization
  checks.py         # mechanical checks: verbatim quotes, banned lexicon, ref integrity — each can go red
  render.py         # proposal.json -> proposal.md (page one first, depth behind); assigns O/N/Q codes
  providers/
    __init__.py     # resolve_provider(): GROUNDWORK_PROVIDER = anthropic | openai-codex | openrouter
    anthropic_provider.py   # official SDK, claude-opus-5, streaming; checks stop_reason
    codex_provider.py       # ChatGPT OAuth via chatgpt.com/backend-api/codex/responses (Kernos wire contract, simplified)
    openrouter_provider.py  # OPENROUTER_API_KEY, OpenAI-compatible chat completions
  credentials.py    # .env loading; Codex OAuth: .credentials/openai-codex.json + ~/.codex/auth.json resync + refresh
examples/
  fetch_transcript.sh   # downloads the real test transcript (not committed — copyright)
  proposal.md           # generated output on the real transcript (committed; quotes are fair-use excerpts)
  proposal.json         # the structured document behind it (what `check` verifies)
design/               # the AgentBridge documents
```

## Decisions

1. **Python 3.11+, minimal deps**: `anthropic`, `httpx`, `python-dotenv`. No framework.
2. **The engine returns structured JSON, not prose.** Every item carries a stable slug `id`
   chosen by the LLM (`opp-invoicing`, `no-full-erp`, `q-order-volume`). Prose fields
   cross-reference items with `{ref:<slug>}` placeholders — the LLM never writes `O1`/`N2`
   literals. `render.py` assigns codes (O1..., N1..., Q1...) in document order and
   substitutes placeholders. `generate` writes `proposal.json` alongside `proposal.md`.
3. **Quotes are contiguous, single-speaker, verbatim spans.** No elision, no `...`, no
   speaker labels inside a quote. A claim that needs two moments cites two quotes
   (`quotes: [str, ...]`), each checked independently.
4. **Checks (each can go red; `groundwork check proposal.json transcript` runs them standalone):**
   - **Verbatim**: every quote must appear in the transcript after canonical folding of
     BOTH sides — NFKC, curly quotes/apostrophes → straight, en/em-dash → `-`,
     `…` → `...`, non-breaking space → space, casefold, collapse whitespace. The fold
     table is data in `checks.py`, auditable. No other forgiveness.
   - **Lexicon**: banned-terms scan (case-insensitive regex) over all LLM-authored
     non-quote fields. Client quotes are exempt by design — their vocabulary wins.
   - **Refs**: every `{ref:...}` resolves to an existing item; no bare `O\d+/N\d+/Q\d+`
     literals in LLM-authored fields; every stated number in an impact carries a `basis`.
5. **One retry loop**: a red check OR a JSON parse failure triggers one re-prompt carrying
   the specific failures. Still red after retry → the tool fails loudly with the report.
   It never silently drops claims.
6. **Transcript not committed** (copyright); `examples/fetch_transcript.sh` retrieves it.
   The generated proposal (short fair-use excerpts) is committed as the showcase.
7. **Provider contract**: `complete(system: str, user: str) -> str` (the JSON text).
   Selection via `GROUNDWORK_PROVIDER` (default `anthropic`). Providers own auth.
8. **Anchor style rules** live in `prompt.py`, sourced from design/ANCHOR-NOTES.md.

## Provider notes

- **anthropic**: `Anthropic()` client (resolves `ANTHROPIC_API_KEY` / auth token / `ant`
  profile), model `claude-opus-5` (override `GROUNDWORK_ANTHROPIC_MODEL`),
  `client.messages.stream(...)` + `get_final_message()`, `max_tokens=32000`, no
  `thinking` param (adaptive by default), no temperature. Check `stop_reason` before
  reading content (`refusal` → clear error; `max_tokens` → treated as parse failure).
- **openai-codex**: NOT api.openai.com — the ChatGPT consumer backend. Credentials file
  `.credentials/openai-codex.json` (`{access, refresh, expires, accountId}`), auto-resync
  from `~/.codex/auth.json` when newer, refresh via `auth.openai.com/oauth/token` with
  client id `app_EMoamEEZ73f0CkXaXp7hrann`, recover from refresh-401 via the CLI file.
  Request: POST `{base}/codex/responses`, SSE only, body `{model, instructions, input,
  store:false, stream:true, reasoning:{effort,summary}, text:{verbosity}}`, headers
  `Authorization: Bearer`, `chatgpt-account-id`, `originator: pi`, OS-style UA,
  `OpenAI-Beta: responses=experimental`, `session_id`/`prompt_cache_key` per run.
  (No tools are sent, so Kernos's ~40KB tool-schema failure mode doesn't apply; the
  load-bearing headers are kept anyway.)
- **openrouter**: `OPENROUTER_API_KEY`, POST `https://openrouter.ai/api/v1/chat/completions`.
  Default model `anthropic/claude-opus-5` (verified in the live catalog; same tier as
  the Anthropic provider); override `GROUNDWORK_OPENROUTER_MODEL`.
