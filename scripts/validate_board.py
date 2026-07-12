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

  5. .gitignore ignores .history/ and *.kicad_prl.
     KiCad 10's Local History runs git_repository_init() on <project>/.history,
     so it is a nested git repo. The .gitignore KiCad writes inside it governs
     KiCad's history repo, not the board repo -- which still sees an embedded
     repository. Committing it adds a broken gitlink.

  6. Every schematic actually LOADS, and its symbol sub-units are well-formed.
     `kicad-cli` prints "Failed to load schematic" and still EXITS 0, so a
     completely unloadable schematic reads as "zero ERC violations" to any script
     that trusts the exit code. A board can therefore look perfectly clean while
     KiCad refuses to open it. Never trust kicad-cli's exit status to tell you a
     schematic is well-formed.

Requires: KiCad-Master-Lib, via --master-lib or $KICAD_MASTER_LIB.
"""

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
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


def check_symbol_units(hw: Path, problems: list[str]) -> None:
    """Every symbol sub-unit must be named "<parent item>_<unit>_<style>".

    In a schematic's lib_symbols block:

        (symbol "LIB:ITEM"
            (symbol "ITEM_0_1" ...)

    The sub-units carry the BARE item name. Rename a symbol's item without also
    renaming its sub-units and KiCad refuses to open the schematic:

        Invalid symbol unit name prefix AP63205_0_1

    Checked structurally, in pure Python, so it works with no KiCad present --
    and because kicad-cli cannot be trusted to report a load failure (see
    check_schematics_load).
    """
    parent = re.compile(r'^(\t\t)\(symbol "([^"]+)"', re.M)
    child = re.compile(r'^(\t\t\t)\(symbol "([^"]+)"', re.M)

    for sch in sorted(hw.glob("*.kicad_sch")):
        src = sch.read_text(errors="ignore")
        for m in parent.finditer(src):
            if ":" not in m.group(2):
                continue
            item = m.group(2).split(":", 1)[1]
            depth, end = 0, len(src)
            for j in range(m.start(), len(src)):
                if src[j] == "(":
                    depth += 1
                elif src[j] == ")":
                    depth -= 1
                    if depth == 0:
                        end = j + 1
                        break
            for c in child.finditer(src[m.start() : end]):
                um = re.match(r"^(.*)_(\d+)_(\d+)$", c.group(2))
                if um and um.group(1) != item:
                    problems.append(
                        f"{sch.name}: symbol unit '{c.group(2)}' does not match its parent "
                        f"'{m.group(2)}' — KiCad will refuse to open this schematic "
                        f"(expected '{item}_{um.group(2)}_{um.group(3)}')"
                    )


def check_schematics_load(hw: Path, problems: list[str]) -> None:
    """Actually open every schematic with KiCad.

    kicad-cli EXITS 0 when it fails to load a schematic, so its exit status is
    useless here -- the output has to be read. A scripted ERC sweep that trusts
    the exit code will score an unloadable schematic as "zero violations".
    """
    cli = shlex.split(os.environ.get("KICAD_CLI", "kicad-cli"))
    try:
        subprocess.run([*cli, "version"], capture_output=True, timeout=60, check=True)
    except (OSError, subprocess.SubprocessError):
        print("  note: kicad-cli unavailable — skipping the schematic load check")
        return

    with tempfile.TemporaryDirectory() as tmp:
        for sch in sorted(hw.glob("*.kicad_sch")):
            r = subprocess.run(
                [*cli, "sch", "erc", "-o", str(Path(tmp) / "erc.rpt"), str(sch)],
                capture_output=True,
                text=True,
                timeout=300,
            )
            if "failed to load" in (r.stdout + r.stderr).lower():
                problems.append(f"{sch.name}: KiCad cannot load this schematic")


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


def check_gitignore(repo: Path, problems: list[str]) -> None:
    """.history/ must be ignored.

    KiCad 10's Local History feature runs git_repository_init() on <project>/.history,
    making it a nested git repository. KiCad writes a .gitignore *inside* it, but that
    governs KiCad's own history repo -- the board repo still sees an embedded repository
    and reports it untracked. Committing it puts a broken gitlink in the repo.
    """
    gitignore = repo / ".gitignore"
    if not gitignore.is_file():
        problems.append(".gitignore: missing")
        return
    rules = {line.strip() for line in gitignore.read_text().splitlines()}
    if not rules & {".history/", ".history"}:
        problems.append(
            ".gitignore: does not ignore '.history/' — KiCad 10 creates it as a nested "
            "git repo; committing it would add a broken gitlink"
        )
    if not rules & {"*.kicad_prl", "*.kicad_prl "}:
        problems.append(
            ".gitignore: does not ignore '*.kicad_prl' — KiCad rewrites it on every open, "
            "so tracking it dirties the tree constantly (it is per-developer local state, "
            "not design intent)"
        )


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
    check_symbol_units(hw, problems)
    check_schematics_load(hw, problems)
    check_drc_severity(hw, problems)
    check_libraries(hw, fp, sym, problems)
    check_makefile(hw, problems)
    check_gitignore(args.repo, problems)

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
