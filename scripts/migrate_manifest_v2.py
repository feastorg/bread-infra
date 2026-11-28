#!/usr/bin/env python3
"""Convert a schema 1.0 slice.yaml or loaf.yaml to schema 2.0.

Usage:
    python migrate_manifest_v2.py <repo-dir> --gen N [--no-format] [--write]

Reads <repo-dir>/slice.yaml or loaf.yaml and prints the 2.0 manifest; --write replaces the file.
2.0 keeps the 1.0 fields a tool reads, under the same paths (spec/slice/slice-manifest-spec.md):

- status: concept stays concept, deprecated becomes retired, and prototype, validated and
  released become development. 1.0's released never meant a release tag. Set by hand a
  fabricated board to built, and a 1.0 concept whose board is already designed to development.
- hardware.hw_gen_current: --gen, the generation the board in hardware/ is heading for.
- hardware.interface: SI1.
- Slices: mounting.pattern from the board outline in hardware/BREAD_Slice.kicad_pcb, slice-S-v0
  for 70 x 100 and slice-L-v0 for 100 x 145 (within 0.02 mm, Slice Interface 1's tolerance),
  with pcb.dimensions set to match; null, with the measured dimensions, for any other
  outline, or with --no-format for a board whose bus or holes do not meet its outline's
  format. A board file with no Edge.Cuts outline stops the run unless
  --no-format is given. Edge.Cuts drawn inside footprints is not read.

Prints each value it changes to stderr, and hw_gen_supported when it is dropped with more
than the current generation in it; the other 1.0 fields that 2.0 removes are dropped without
a note. It validates the result against the 2.0
schema before printing or writing it; an invalid result is neither printed nor written.
"""

import argparse
import importlib.util
import re
import sys
from pathlib import Path

import yaml

_spec = importlib.util.spec_from_file_location("validate_manifest", Path(__file__).with_name("validate_manifest.py"))
assert _spec is not None and _spec.loader is not None
validate_manifest = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate_manifest)

STATUS = {
    "concept": "concept",
    "prototype": "development",
    "validated": "development",
    "released": "development",
    "deprecated": "retired",
}
FORMATS = {"slice-S-v0": (70.0, 100.0), "slice-L-v0": (100.0, 145.0)}
TOLERANCE = 0.02  # Slice Interface 1: a board meets a format to 0.02 mm
HEADER = "# {kind}.yaml: BREAD {Kind} manifest, schema 2.0 (bread-infra spec/{kind}/{kind}-manifest-spec.md)\n"


def outline(pcb: Path) -> tuple[float, float] | None:
    """Width and height of the Edge.Cuts bounding box, or None if the board has no outline."""
    text = pcb.read_text(encoding="utf-8")
    xs, ys = [], []
    for m in re.finditer(r"\(gr_(?:line|arc|rect|poly)\s", text):
        depth, i = 0, m.start()
        for i in range(m.start(), len(text)):
            depth += {"(": 1, ")": -1}.get(text[i], 0)
            if depth == 0:
                break
        item = text[m.start() : i + 1]
        if not re.search(r'\(layer "?Edge\.Cuts"?\)', item):
            continue
        for x, y in re.findall(r"\((?:start|mid|end|xy) (-?[\d.]+) (-?[\d.]+)\)", item):
            xs.append(float(x))
            ys.append(float(y))
    if not xs:
        return None
    return round(max(xs) - min(xs), 3), round(max(ys) - min(ys), 3)


def board_format(size: tuple[float, float] | None) -> str | None:
    if size is None:
        return None
    for name, (w, h) in FORMATS.items():
        # 1e-9 absorbs float error, so 145.02 is inside like 70.02 (145.02 - 145 > 0.02 in floats).
        if abs(size[0] - w) <= TOLERANCE + 1e-9 and abs(size[1] - h) <= TOLERANCE + 1e-9:
            return name
    return None


def dims(w: float, h: float) -> str:
    return f"{w:g}mm x {h:g}mm"


def migrate(
    kind: str, v1: dict, gen: int, size: tuple[float, float] | None, use_format: bool
) -> tuple[dict, list[str]]:
    notes = []
    hw1 = v1.get("hardware") or {}
    if v1.get("status") not in STATUS:
        raise SystemExit(f"unknown 1.0 status {v1.get('status')!r}")
    out: dict = {"schema_version": "2.0"}
    for key in ("id", "name", "summary", "category" if kind == "slice" else "role"):
        out[key] = v1[key]
    out["status"] = STATUS[v1["status"]]
    if out["status"] != v1["status"]:
        notes.append(f"status {v1['status']!r} -> {out['status']!r}")
    if hw1.get("hw_gen_current") != gen:
        notes.append(f"hw_gen_current {hw1.get('hw_gen_current')} -> {gen}")
    hw = {"hw_gen_current": gen, "interface": "SI1"}
    pcb1 = hw1.get("pcb") or {}
    if kind == "slice":
        fmt = board_format(size) if use_format else None
        if fmt:
            stated = dims(*FORMATS[fmt])
        elif size:
            stated = dims(*size)
        else:
            stated = pcb1["dimensions"]
        if stated.replace(" ", "") != str(pcb1.get("dimensions", "")).replace(" ", ""):
            notes.append(f"pcb.dimensions {pcb1.get('dimensions')!r} -> {stated!r} (board outline {size})")
        hw["pcb"] = {"layers": pcb1["layers"], "dimensions": stated, "thickness": pcb1["thickness"]}
        hw["mounting"] = {"pattern": fmt}
        mcu = hw1.get("mcu")
        hw["mcu"] = {"form_factor": mcu["form_factor"]} if mcu and mcu.get("form_factor") else None
    else:
        hw["pcb"] = {"layers": pcb1["layers"]}
    out["hardware"] = hw
    if kind == "slice":
        addr = ((v1.get("interfaces") or {}).get("host") or {}).get("address_default")
        fw_addr = (((v1.get("firmware") or {}).get("i2c")) or {}).get("address_default")
        if addr is None and fw_addr is not None:
            addr = fw_addr
            notes.append(f"address_default {fw_addr} taken from firmware.i2c")
        elif fw_addr is not None and fw_addr != addr:
            notes.append(f"firmware.i2c.address_default {fw_addr} differs from interfaces.host {addr}; kept {addr}")
        out["interfaces"] = {"host": {"address_default": addr}}
    else:
        ic = v1["interconnect"]
        out["interconnect"] = {"slice_slots": ic["slice_slots"], "bus": {"type": ic["bus"]["type"]}}
    out["metadata"] = {"tags": list((v1.get("metadata") or {}).get("tags") or [])}
    if hw1.get("hw_gen_supported") not in (None, [], [hw1.get("hw_gen_current")]):
        notes.append(f"hw_gen_supported {hw1['hw_gen_supported']} dropped")
    return out, notes


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert a 1.0 slice.yaml or loaf.yaml to schema 2.0.")
    parser.add_argument("repo", type=Path)
    parser.add_argument("--gen", type=int, required=True, help="generation the board in hardware/ is heading for")
    parser.add_argument("--no-format", action="store_true", help="board meets no format: mounting.pattern null")
    parser.add_argument("--write", action="store_true", help="replace the manifest instead of printing it")
    args = parser.parse_args()
    if args.gen < 1:
        sys.exit("--gen must be 1 or more")

    for kind in ("slice", "loaf"):
        path = args.repo / f"{kind}.yaml"
        if path.exists():
            break
    else:
        sys.exit(f"no slice.yaml or loaf.yaml in {args.repo}")
    v1 = yaml.safe_load(path.read_text(encoding="utf-8"))
    if str(v1.get("schema_version", "")).startswith("2."):
        sys.exit(f"{path} is already schema 2.x")
    size = None
    if kind == "slice":
        pcb = args.repo / "hardware" / "BREAD_Slice.kicad_pcb"
        if not pcb.exists():
            sys.exit(f"no board file at {pcb}")
        size = outline(pcb)
        if size is None and not args.no_format:
            sys.exit(f"no Edge.Cuts outline found in {pcb}; pass --no-format if the board meets no format")
    out, notes = migrate(kind, v1, args.gen, size, not args.no_format)
    text = HEADER.format(kind=kind, Kind=kind.capitalize()) + yaml.safe_dump(
        out, sort_keys=False, allow_unicode=True, width=100
    )
    for note in notes:
        print(f"{path}: {note}", file=sys.stderr)
    schema = Path(__file__).resolve().parent.parent / "schemas" / f"{kind}.schema.v2.json"
    errors = validate_manifest.validate_data(yaml.safe_load(text), schema)
    if errors:
        print(f"{path}: the 2.0 result is invalid, nothing written:", file=sys.stderr)
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    if args.write:
        path.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
