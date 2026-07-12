#!/usr/bin/env bash
# Migrate a BREAD board's KiCad files to the KiCad 10 format.
#
#   scripts/upgrade_kicad10.sh <repo-or-hardware-dir> [...]
#   KICAD_CLI="kicad-cli" scripts/upgrade_kicad10.sh Slice_RLAY     # native install
#
# Uses KiCad's own `kicad-cli sch upgrade` / `pcb upgrade`. Verified lossless on
# a real board (Slice_RLAY): identical netlist, identical footprint refs,
# positions and pad counts, identical routing. And idempotent -- re-running on an
# already-migrated file reports "not updated" and leaves it byte-for-byte alone,
# so it is safe to run across the fleet including boards already done.
#
# THE TRAP: `sch upgrade` does NOT cascade into hierarchical sub-sheets. Running
# it on the root sheet alone leaves every sub-sheet on the old format, which
# looks migrated and is not. This script upgrades every .kicad_sch it finds.
#
# What this does NOT do:
#   - fix broken library references (format migration only)
#   - re-link footprints from the schematic
#   - fix pre-existing annotation errors
# Run scripts/validate_board.py afterwards to see what is still wrong.

set -euo pipefail

KICAD_CLI="${KICAD_CLI:-flatpak run --command=kicad-cli org.kicad.KiCad}"

if [ $# -eq 0 ]; then
    echo "usage: $0 <repo-or-hardware-dir> [...]" >&2
    exit 1
fi

version_of() { grep -m1 -oE '\(version [0-9]+\)' "$1" | grep -oE '[0-9]+'; }

for target in "$@"; do
    hw="$target"
    [ -d "$target/hardware" ] && hw="$target/hardware"

    if [ ! -d "$hw" ]; then
        echo "skip  $target (no hardware dir)"
        continue
    fi

    echo "=== $target"
    changed=0

    # Every schematic, not just the root: sub-sheets are not upgraded for us.
    while IFS= read -r -d '' f; do
        before=$(version_of "$f")
        $KICAD_CLI sch upgrade "$f" >/dev/null 2>&1 || {
            echo "  FAIL  $(basename "$f")" >&2
            continue
        }
        after=$(version_of "$f")
        if [ "$before" != "$after" ]; then
            echo "  sch   $(basename "$f")  $before -> $after"
            changed=$((changed + 1))
        fi
    done < <(find "$hw" -maxdepth 1 -name '*.kicad_sch' -print0)

    while IFS= read -r -d '' f; do
        before=$(version_of "$f")
        $KICAD_CLI pcb upgrade "$f" >/dev/null 2>&1 || {
            echo "  FAIL  $(basename "$f")" >&2
            continue
        }
        after=$(version_of "$f")
        if [ "$before" != "$after" ]; then
            echo "  pcb   $(basename "$f")  $before -> $after"
            changed=$((changed + 1))
        fi
    done < <(find "$hw" -maxdepth 1 -name '*.kicad_pcb' -print0)

    if [ "$changed" -eq 0 ]; then
        echo "  already on KiCad 10"
    fi
done
