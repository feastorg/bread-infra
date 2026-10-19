# Fleet remediation worklist

The detailed critical path for bringing the BREAD Slice fleet to a releasable
state: KiCad 10 format, library references that resolve, and ERC/DRC/Fab clean
under [`validate_board.py`](../scripts/validate_board.py).

Live status, the per-board checklist, and the open remediation PRs are tracked in
the epic, **#16**. This document holds the detailed tier breakdown and the
measurement method — the analysis that is too long for the epic body.

> **Last measured 2026-07-13** with KiCad 10's own ERC and DRC at `error`
> severity plus `validate_board.py` (bread-infra v1.2.0), each board on its
> `chore/mechanical-remediation` branch. The counts below are that measurement,
> not current state. Re-measure (see [Measuring](#measuring)) before relying on
> any number here.

At that measurement, **14 of 42 boards were green**. Mechanical remediation —
KiCad 10 format, DRC parity gate, Makefile targets, `.gitignore`, symbol
sub-units, KiBot layer coverage — was complete on all 42. Everything left is a
board defect.

Green: `Loaf_ESPT`, `Loaf_x004`, `Slice_DCMT`, `Slice_IOAC`,
`Slice_PRTO_CONN_S2L`, `Slice_PRTO_THTA_S2L`, `Slice_PRTO_THT_S2L`,
`Slice_RLAY`, `Slice_RTDM`, `Slice_TEMP_NANO_S2L-r1`, `Slice_TEMP_NANO_S2L-r2`,
`Slice_TEMP_NUCL_L4L-r1`, `Slice_TEMP_NUCL_S4L-r1`.

## Critical path

Ordered by what it costs to get wrong, then by throughput.

### Tier 0 — real copper defects (6 boards)

The only items here that can ruin a fabrication run: shorts, mask bridges across
pads, clearance violations, drills out of range. They sat in boards whose CI
reported green for months.

| Board | Copper defects | Total DRC |
| --- | --- | --- |
| `Slice_SOLR` | 14 | 17 |
| `Slice_IOCT` | 12 | 20 |
| `Slice_FPSG` | 4 | 4 |
| `Slice_STPC` | 3 | 3 |
| `Slice_LEPD` | 2 | 2 |
| `Slice_PRTO_SMT_S2L` | 1 | 1 |

Types across the fleet: `solder_mask_bridge` x12, `clearance` x11,
`shorting_items` x8, `drill_out_of_range` x4, `courtyards_overlap` x1. Start with
`Slice_SOLR` and `Slice_IOCT` — they hold 26 of the 73 DRC errors between them.
`Slice_SOLR` has since become a BQ24650 charger redesign.

### Tier 1 — schematic/PCB parity (11 errors)

Not fab-fatal, but the BOM, pick-and-place, or fab output disagrees with the
design. Each needs a decision about which side is right.

| Count | Issue | Board | Decision |
| --- | --- | --- | --- |
| 5 | `'Exclude from BOM' settings differ` | `Slice_STEP` | Should the part be in the BOM? |
| 4 | `KMLib_IC_SMD:RS_20_ADI-L` vs symbol | `Slice_AOEM` | Which footprint is correct? |
| 1 | `Package_TO_SOT_SMD:TSOT-23-6` vs symbol | | |
| 1 | `KMLib_Boards_Modules:Arduino_Nano_Headers` vs symbol | | |

Where the PCB is right, **Tools -> Update PCB from Schematic** with *re-link
footprints* enabled resolves it.

### Tier 2 — ERC (39 errors, 10 boards)

| Count | Type | Fix |
| --- | --- | --- |
| 14 | `power_pin_not_driven` | Add `PWR_FLAG` — mechanical |
| 10 | `pin_not_connected` | No-connect flag on intentionally unused pins — mechanical |
| 8 | `pin_to_pin` | Two outputs driving each other — a real electrical conflict |
| 4 | `pin_not_driven` | |
| 3 | `label_dangling` | |

`Slice_STPC` (12) and `Slice_VCDC` (9) are the bulk. The 8 `pin_to_pin` are
design errors, not flags you can add — look at those properly.

### Tier 3 — library re-points (62 refs, quick throughput)

Twelve boards need nothing but library re-points to go green — the cheapest way
to move the count.

| Board | Refs |
| --- | --- |
| `Slice_AQDO` | 1 |
| `Slice_AQEC` | 1 |
| `Slice_AQOR` | 1 |
| `Slice_TEMP_PICO_L4L-r1` | 1 |
| `Slice_TEMP_PICO_S2L-r1` | 1 |
| `Slice_THRM_31856` | 1 |
| `Slice_VCAC` | 1 |
| `Slice_BUCK` | 2 |
| `Slice_THRM_31855` | 2 |
| `Slice_IAQM` | 3 |
| `Slice_USBP` | 4 |
| `Slice_LVAI` | 5 |

Best done in the KiCad UI, where the symbol and its value are visible —
fingerprint matching cannot tell a 2-pin resistor from a 2-pin capacitor.

## Suggested sequence

1. `Slice_SOLR`, `Slice_IOCT` — the copper defects, highest cost of being wrong.
2. The other four copper boards — `FPSG`, `STPC`, `LEPD`, `PRTO_SMT_S2L`.
3. The twelve library-only boards — pure re-pointing.
4. ERC `pin_to_pin` (8) — real electrical conflicts.
5. `PWR_FLAG`s and no-connects (24) — mechanical, fast.
6. Tier 1 parity decisions — BOM flags and footprint choices.

Board edits are done by hand in the KiCad UI on each board's branch. Automation
measures, reads CI, and prepares changes; it does not edit board art.

## Syncing the branches

The boards are on branch `chore/mechanical-remediation`. Fetch and check out each
board's branch before measuring:

```sh
for d in ~/repos_feast/Slice_* ~/repos_feast/Loaf_*; do
  git -C "$d" fetch origin && git -C "$d" switch chore/mechanical-remediation 2>/dev/null
done
```

## Measuring

Re-check a board (needs KiCad 10 as a flatpak and KiCad-Master-Lib):

```sh
KICAD_CLI='flatpak run --command=kicad-cli org.kicad.KiCad' \
KICAD_MASTER_LIB=~/repos_feast/KiCad-Master-Lib \
  python3 ~/repos_feast/bread-infra/scripts/validate_board.py <repo>
```

DRC counts three categories — violations, unconnected items, and schematic
parity. Read all three lines, not just the first:

```sh
flatpak run --command=kicad-cli org.kicad.KiCad \
  pcb drc --schematic-parity --severity-error -o /dev/null <board>.kicad_pcb
```

After a re-measure, update the counts above and the status in #16.
