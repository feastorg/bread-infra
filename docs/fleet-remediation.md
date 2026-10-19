# Fleet remediation worklist

The detailed critical path for bringing the BREAD Slice fleet to a releasable
state: KiCad 10 format, library references that resolve, and ERC/DRC/Fab clean
under [`validate_board.py`](../scripts/validate_board.py).

Live status, the per-board checklist, and the open remediation PRs are tracked in
the epic, **#16**. This document holds the detailed tier breakdown and the
measurement method — the analysis that is too long for the epic body.

> **Re-measured 2026-10-19** with KiCad 10 ERC and DRC at `error` severity plus
> `validate_board.py` (bread-infra tip), each board on its
> `chore/mechanical-remediation` branch. This reproduced the 2026-07-13
> measurement: the same 14 green boards, 39 ERC errors, and DRC within two of the
> earlier count. Nothing has merged since July. The one change is `Slice_SOLR`,
> whose BQ24650 redesign dropped it from 17 DRC to 4.

**14 of 42 boards are green.** Mechanical remediation — KiCad 10 format, DRC
parity gate, Makefile targets, `.gitignore`, symbol sub-units, KiBot layer
coverage — is complete on all 42; no board fails a structural check for those
any more. Everything left is a board defect: unresolved library references, ERC,
or DRC.

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

DRC errors (violations + unconnected + parity), measured 2026-10-19. The right
column flags the six boards the 2026-07-13 pass identified as holding real copper
defects — the fab-fatal subset.

| Board | DRC | July copper defects |
| --- | --- | --- |
| `Slice_IOCT` | 20 | 12 |
| `Slice_STEP` | 11 | — |
| `Slice_LOAD` | 7 | — |
| `Slice_GDHB` | 6 | — |
| `Slice_AOEM` | 5 | — |
| `Slice_AQPH` | 4 | — |
| `Slice_FPSG` | 4 | 4 |
| `Slice_IAQM` | 4 | — |
| `Slice_SOLR` | 4 | was 14, pre-redesign |
| `Slice_STPC` | 3 | 3 |
| `Slice_LEPD` | 2 | 2 |
| `Slice_PRTO_SMT_S2L` | 1 | 1 |

71 DRC errors across 12 boards. `Slice_IOCT` holds the most by a wide margin —
start there. `Slice_SOLR` was the worst (14 copper defects) until its BQ24650
redesign dropped it to 4. These counts are totals; run the DRC command below to
separate real copper defects from unconnected-item and parity noise per board.

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
