#!/usr/bin/env python3
"""Validate a BREAD board's hardware against the fleet conventions.

Usage:
    python validate_board.py <repo-root> [--master-lib <path>] [--strict]

Checks that a board repo is actually aligned with BREADS, not merely that it
opens in KiCad. Each check exists because the defect it catches is invisible
from inside KiCad and silently passes CI:

  1. KiCad file format is version 10.
     A board saved by KiCad 9 still opens fine; the version stamp is the only
     signal. Note the converse is not true -- being on 10 does not mean a board
     was migrated properly (see check 3).

  2. `footprint_symbol_mismatch` DRC severity is `error`.
     KiCad's stock DEFAULT is `warning`, and KiBot's DRC preflight only fails on
     errors. So `schematic_parity: true` runs the check and can never fail it.
     Until this is `error`, the parity gate is decorative.

  3. Every symbol and footprint reference resolves against KiCad-Master-Lib.
     KiCad embeds footprint geometry in the .kicad_pcb, so a board renders and
     fabricates perfectly long after its library reference has rotted. The rot
     only surfaces on update-from-library -- or when a generator tries to resolve
     a nickname.

  4. hardware/Makefile does not have its ERC and DRC targets swapped.
     KiBot's `-s`/`--skip-pre` SKIPS the named preflight, so `drc: kibot -s drc`
     skips DRC. Both checks still run, but under each other's names.

Requires: KiCad-Master-Lib, via --master-lib or $KICAD_MASTER_LIB.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

KICAD10_PCB = 20260206
KICAD10_SCH = 20260306

# Libraries that ship with KiCad. Anything else must come from KiCad-Master-Lib.
STOCK = re.compile(
    r"^(Amplifier|Analog|Audio|Battery|Button|Buzzer|Calibration|Capacitor|Choke|Comparator"
    r"|Connector|Converter|Crystal|Device|Diode|Display|Driver|Fiducial|Filter|Fuse|Graphic"
    r"|Heatsink|Inductor|Interface|Isolator|Jumper|LED_|Logic|MCU|Mechanical|Memory|Module"
    r"|Motor|Mounting|NetTie|OptoDevice|Oscillator|Package|Pin|Potentiometer|Power|RF|Reference"
    r"|Regulator|Relay|Resistor|Sensor|Simulation|Socket|Switch|Symbol|TerminalBlock|TestPoint"
    r"|Timer|Transformer|Transistor|Triac|Valve|Varistor|Video|power)"
)

LIB_RE = re.compile(r'\(name "([^"]+)"\)\(type "KiCad"\)\(uri "([^"]+)"\)')


def load_tables(master_lib: Path) -> tuple[dict, dict]:
    def parse(name: str) -> dict:
        f = master_lib / name
        if not f.is_file():
            sys.exit(f"error: {name} not found in {master_lib}")
        return {
            n: Path(u.replace("${KICAD_MASTER_LIB}", str(master_lib)))
            for n, u in LIB_RE.findall(f.read_text())
        }

    return parse("kmlib.fp-lib-table"), parse("kmlib.sym-lib-table")


def check_versions(hw: Path, problems: list[str]) -> None:
    for pcb in hw.glob("*.kicad_pcb"):
        m = re.search(r"\(version (\d+)\)", pcb.read_text(errors="ignore"))
        if m and int(m.group(1)) < KICAD10_PCB:
            problems.append(f"{pcb.name}: KiCad file format {m.group(1)}, expected {KICAD10_PCB} (v10)")
    for sch in hw.glob("*.kicad_sch"):
        m = re.search(r"\(version (\d+)\)", sch.read_text(errors="ignore"))
        if m and int(m.group(1)) < KICAD10_SCH:
            problems.append(f"{sch.name}: KiCad file format {m.group(1)}, expected {KICAD10_SCH} (v10)")


def check_drc_severity(hw: Path, problems: list[str]) -> None:
    for pro in hw.glob("*.kicad_pro"):
        try:
            sev = (
                json.loads(pro.read_text())
                .get("board", {})
                .get("design_settings", {})
                .get("rule_severities", {})
            )
        except json.JSONDecodeError as e:
            problems.append(f"{pro.name}: not valid JSON ({e})")
            continue
        got = sev.get("footprint_symbol_mismatch", "absent")
        if got != "error":
            problems.append(
                f"{pro.name}: rule_severities.footprint_symbol_mismatch is '{got}', must be "
                "'error' — otherwise the schematic-parity gate can never fail"
            )


def check_libraries(hw: Path, fp: dict, sym: dict, problems: list[str]) -> None:
    refs: set[tuple[str, str]] = set()
    for f in hw.glob("*.kicad_pcb"):
        refs |= {
            (r, "fp")
            for r in re.findall(r'^\s*\(footprint "([^"]+)"', f.read_text(errors="ignore"), re.M)
        }
    for f in hw.glob("*.kicad_sch"):
        refs |= {(r, "sym") for r in re.findall(r'\(lib_id "([^"]+)"\)', f.read_text(errors="ignore"))}

    for ref, kind in sorted(refs):
        lib, _, item = ref.partition(":")
        if not lib or STOCK.match(lib):
            continue
        table = fp if kind == "fp" else sym
        if lib not in table:
            problems.append(f"unresolvable {kind}: {ref} — no such library '{lib}'")
            continue
        path = table[lib]
        found = (
            (path / f"{item}.kicad_mod").is_file()
            if kind == "fp"
            else path.is_file() and f'"{item}"' in path.read_text(errors="ignore")
        )
        if not found:
            problems.append(f"unresolvable {kind}: {ref} — '{item}' not in library '{lib}'")


def check_makefile(hw: Path, problems: list[str]) -> None:
    mk = hw / "Makefile"
    if not mk.is_file():
        return
    text = mk.read_text()
    for target, skip_of_other in (("erc", "drc"), ("drc", "erc")):
        m = re.search(rf"^{target}:.*?\n((?:\t.*\n)+)", text, re.M)
        if m and f"-s {target}" in m.group(1):
            problems.append(
                f"Makefile: target '{target}' passes '-s {target}', which SKIPS {target.upper()} "
                f"and runs {skip_of_other.upper()} instead — the targets are swapped"
            )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", type=Path, nargs="?", default=Path("."))
    ap.add_argument("--master-lib", type=Path, default=os.environ.get("KICAD_MASTER_LIB"))
    args = ap.parse_args()

    if not args.master_lib:
        sys.exit("error: pass --master-lib or set $KICAD_MASTER_LIB")
    master_lib = Path(args.master_lib).expanduser().resolve()

    hw = args.repo / "hardware"
    if not hw.is_dir():
        print(f"{args.repo}: no hardware/ directory — skipping")
        return 0

    fp, sym = load_tables(master_lib)
    problems: list[str] = []
    check_versions(hw, problems)
    check_drc_severity(hw, problems)
    check_libraries(hw, fp, sym, problems)
    check_makefile(hw, problems)

    name = args.repo.resolve().name
    if problems:
        print(f"FAIL  {name} — {len(problems)} problem(s)")
        for p in problems:
            print(f"        {p}")
        return 1
    print(f"PASS  {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
