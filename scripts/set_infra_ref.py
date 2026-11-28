#!/usr/bin/env python3
"""Set, or check, the default `infra_ref` of every reusable workflow.

Usage:
    python scripts/set_infra_ref.py <ref>           # rewrite the defaults to <ref>
    python scripts/set_infra_ref.py --check <ref>   # exit 1 unless every default is <ref>

The reusable workflows check bread-infra out a second time, at `inputs.infra_ref`, for the
scripts they run. On main the default is `main`; a release tag's commit sets it to the tag,
so a board pinned at `@vX.Y.Z` runs vX.Y.Z's scripts. See README.md, "Releasing".
"""

import argparse
import re
import sys
from pathlib import Path

WORKFLOWS = Path(__file__).resolve().parent.parent / ".github" / "workflows"
# The default line inside an `infra_ref:` input block (6-space key, 8-space fields).
DEFAULT = re.compile(r'(^      infra_ref:\n(?:^        .*\n)*?^        default: )"?([^"\n]*)"?$', re.M)


def defaults(text: str) -> list[str]:
    return [m.group(2) for m in DEFAULT.finditer(text)]


def set_ref(text: str, ref: str) -> str:
    return DEFAULT.sub(lambda m: f'{m.group(1)}"{ref}"', text)


def main() -> int:
    parser = argparse.ArgumentParser(description="Set or check the reusable workflows' infra_ref default.")
    parser.add_argument("ref")
    parser.add_argument("--check", action="store_true", help="only check; exit 1 on any mismatch")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9._/-]+", args.ref):
        sys.exit(f"not a git ref name: {args.ref!r}")

    files = sorted(WORKFLOWS.glob("*.yml"))
    found, wrong = 0, []
    for path in files:
        text = path.read_text(encoding="utf-8")
        refs = defaults(text)
        if re.search(r"^      infra_ref:$", text, re.M) and not refs:
            sys.exit(f"{path.name}: has an infra_ref input but no default this script can read")
        found += len(refs)
        wrong += [f"{path.name}: {r}" for r in refs if r != args.ref]
        if refs and not args.check:
            path.write_text(set_ref(text, args.ref), encoding="utf-8")
    if not found:
        sys.exit("no infra_ref defaults found")
    if args.check:
        if wrong:
            print(f"infra_ref defaults that are not {args.ref!r}:", *wrong, sep="\n  ")
            return 1
        print(f"OK: {found} infra_ref defaults are {args.ref!r}")
    else:
        print(f"set {found} infra_ref defaults to {args.ref!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
