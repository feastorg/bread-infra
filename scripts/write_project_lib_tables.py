#!/usr/bin/env python3
"""Write project-level KiCad library tables pointing at a KiCad-Master-Lib checkout.

Usage:
    python write_project_lib_tables.py <hardware-dir> --master-lib <path>

KiCad merges a project's `fp-lib-table` / `sym-lib-table` with the global ones, so
this makes every KMLib_* and vendored nickname resolve without disturbing the
stock libraries that ship with KiCad.

Board repos deliberately do NOT commit these files -- they hold absolute paths,
which differ per machine. Generate them at build time instead, from the tables
that KiCad-Master-Lib does commit.

Paths are written absolute rather than as ${KICAD_MASTER_LIB}: KiCad only expands
variables it knows about, and depending on it being configured in the environment
is exactly the fragility this is meant to remove.
"""

import argparse
import re
import sys
from pathlib import Path

LIB_RE = re.compile(r'\(name "([^"]+)"\)\(type "KiCad"\)\(uri "([^"]+)"\)')

TABLES = [
    # (source in KiCad-Master-Lib, project filename, s-expression tag)
    ("kmlib.fp-lib-table", "fp-lib-table", "fp_lib_table"),
    ("kmlib.sym-lib-table", "sym-lib-table", "sym_lib_table"),
    ("kmlib.design-block-lib-table", "design-block-lib-table", "design_block_lib_table"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("hardware", type=Path)
    ap.add_argument("--master-lib", type=Path, required=True)
    args = ap.parse_args()

    master = args.master_lib.expanduser().resolve()
    if not master.is_dir():
        sys.exit(f"error: master lib not found: {master}")
    if not args.hardware.is_dir():
        sys.exit(f"error: hardware dir not found: {args.hardware}")

    for src_name, dest_name, tag in TABLES:
        src = master / src_name
        if not src.is_file():
            sys.exit(f"error: {src_name} missing from {master}")

        lines = [f"({tag}", "  (version 7)"]
        count = 0
        for nickname, uri in LIB_RE.findall(src.read_text()):
            path = uri.replace("${KICAD_MASTER_LIB}", str(master))
            lines.append(
                f'  (lib (name "{nickname}")(type "KiCad")(uri "{path}")(options "")(descr ""))'
            )
            count += 1
        lines.append(")\n")

        (args.hardware / dest_name).write_text("\n".join(lines))
        print(f"wrote {args.hardware / dest_name}  ({count} libraries)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
