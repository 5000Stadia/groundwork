"""groundwork — turns a raw discovery conversation into the document a client
would actually pay for.

    groundwork generate <transcript.txt> [-o proposal.md]
    groundwork check <proposal.json> <transcript.txt>
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _cmd_check(args: argparse.Namespace) -> int:
    from .checks import report, run_all
    from .schema import Proposal

    doc = Proposal.from_dict(json.loads(Path(args.proposal).read_text(encoding="utf-8")))
    transcript = Path(args.transcript).read_text(encoding="utf-8")
    failures = run_all(doc, transcript)
    print(report(failures))
    return 1 if failures else 0


def _cmd_generate(args: argparse.Namespace) -> int:
    from .engine import generate

    transcript = Path(args.transcript).read_text(encoding="utf-8")
    out_md = Path(args.output)
    out_json = out_md.with_suffix(".json")

    result = generate(transcript)
    out_json.write_text(
        json.dumps(result.document.to_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    out_md.write_text(result.markdown, encoding="utf-8")
    print(f"wrote {out_md} and {out_json}")
    if result.failures:
        from .checks import report

        print("\nCHECKS RED after retry — do not hand this to a client:", file=sys.stderr)
        print(report(result.failures), file=sys.stderr)
        return 1
    print("all checks green")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="groundwork", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    g = sub.add_parser("generate", help="transcript -> proposal.md + proposal.json")
    g.add_argument("transcript")
    g.add_argument("-o", "--output", default="proposal.md")
    g.set_defaults(func=_cmd_generate)

    c = sub.add_parser("check", help="re-run the mechanical checks on a proposal")
    c.add_argument("proposal", help="proposal.json (written by generate)")
    c.add_argument("transcript")
    c.set_defaults(func=_cmd_check)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
