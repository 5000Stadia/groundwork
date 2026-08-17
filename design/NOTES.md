# Notes

## S4 verdict — first real run (2026-08-17)

Input: Mixergy's Brady Lewis / Allmoxy interview (11,868 words), via the ChatGPT OAuth
provider (`gpt-5.6-sol`, effort medium). All checks green on the first attempt.

**Verdict: better than slop, honestly so.** The parts generic tools structurally can't
write came out real: N1 argues against the sales organization Brady himself once
planned (quoting his own abandonment of it), N3 declines the marketplace using the
risk Brady flagged, N4 kills the $4.99 support plan with his own "no one buys it."
Impact claims carry their bases and admit single-customer evidence ("one customer's
result, not yet a fleet-wide benchmark"). Assumptions are named. Zero lexicon hits
on the first pass — the register held without the check having to bite.

**Finding worth recording:** the model proposed for *Allmoxy* (Brady's current SaaS)
rather than the cabinet shop of the story's first half. That is the defensible reading
— the operator being interviewed runs Allmoxy today — but a consultant using this tool
on an ambiguous transcript should state the intended client; a future flag
(`--client "..."`) would remove the ambiguity.

**Seam bug caught by the real run, not the tests:** the model cross-referenced a pain
(`{ref:pain-...}`), which the check accepted (the id existed) but the renderer could
not substitute (pains carry no codes). Fixed: refs may only target coded items; the
check now rejects pain refs and the prompt says so. The committed example is the
regenerated, fully-green document.

## Provider status

- **openai-codex**: exercised live end-to-end (this run), including credential resync
  from `~/.codex/auth.json`.
- **anthropic**: implemented per SDK docs; not exercised locally (no ANTHROPIC_API_KEY
  on this machine). First user with a key exercises it; the provider surface is three
  calls and mirrors the documented streaming pattern.
- **openrouter**: implemented; default model verified against the live catalog
  (`anthropic/claude-opus-5`); not exercised locally (no key).
