# Intention

## What we are building

**Groundwork**: a local CLI tool that turns a raw discovery conversation into the document a client would actually pay for. A consultant pastes in a discovery-call transcript or messy notes; Groundwork produces one proposal document with five sections:

1. **What we heard** — the client's pains, ranked, quoted in their own words.
2. **Opportunity map** — each opportunity grounded in a specific moment from the call, with effort (S/M/L), impact stated in the client's own currency, and confidence.
3. **The honest no's** — what the client asked about that is *not* worth doing, and why. The credibility section; generic tools structurally cannot write it.
4. **Recommended path** — the smallest thing that proves value in weeks, then layers.
5. **Open questions** — with assumptions named.

Every opportunity, no, and question carries a short code (O1, N2, Q3) so a client can reply "O3 yes but N2 worries me" — the document is conversationally addressable. The first page is the compressed read for a busy owner; depth sits behind it.

**For whom:** AI consultants walking into client conversations — and the author, as a portfolio piece showing understanding of the business problem, not just the API.

## What "good" means

The bar: *I would hand this across a table to a real client without editing it.* A reader should think "these people actually listened."

- **Traceability, mechanically checked.** Every opportunity must cite a quote that appears **verbatim** in the input text. The check is automated and can go red.
- **Client vocabulary over consulting jargon.** No number without its stated basis.
- **Zero consulting slop**, enforced by a banned lexicon check (grep-class): leverage, streamline, unlock value, AI-powered transformation, synergy, and their cousins.
- **Addressability**: stable O/N/Q codes throughout.
- **Compression**: page one stands alone for a busy owner.

## Anchor

Basecamp's **Shape Up pitches** (the book is free online, with real pitch examples). Adjacent shape, not identical: problem stated from evidence, appetite instead of estimates, rabbit holes named, and explicit no-gos — which are exactly the honest no's. The finished document is blind-compared against this register.

## First proof

Build the judgment core **first**, on one genuinely real published conversation — a business owner walking through their operations (a podcast interview transcript), not a synthetic one, so the tool cannot cheat by matching anyone's imagination. If the first output does not already feel startlingly better than slop, that is a **finding, not a polish item**.

## Runtime connections

The engine calls an LLM at runtime. Connection config lives in `.env` per standard practice:

1. **Anthropic** — `ANTHROPIC_API_KEY`, the default path.
2. **ChatGPT OAuth** — the way Kernos does it: credentials file with access/refresh tokens, `.credentials/openai-codex.json` style, resynced from `~/.codex/auth.json`.
3. **OpenRouter** — third option.

The README quickstart documents each connection path.

## Publishing authority

**Stand-by authority granted.** Create the GitHub repo under `5000Stadia` (public — portfolio piece); push on pass per the method; no per-push asks.
