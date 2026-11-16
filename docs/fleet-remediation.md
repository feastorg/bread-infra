# Fleet remediation worklist

The detailed critical path for bringing the BREAD Slice fleet to a releasable
state: KiCad 10 format, library references that resolve, and ERC/DRC/Fab clean
under [`validate_board.py`](../scripts/validate_board.py).

Live status, the per-board checklist, and the open remediation PRs are tracked in
the epic, **#16**. This document holds the detailed tier breakdown and the
measurement method — the analysis that is too long for the epic body.

> **Re-measured 2026-11-15** with KiCad 10.0.8 ERC and DRC (`--schematic-parity`)
> at `error` severity plus `validate_board.py` (bread-infra tip), each board at the
> committed tip of its `chore/mechanical-remediation` branch. Since 2026-10-19 the
> library re-points (Tier 3) landed on 11 boards; every other board's counts are
> unchanged.

**25 of 42 boards are green**, up from 14. Mechanical remediation — KiCad 10
format, DRC parity gate, Makefile targets, `.gitignore`, symbol sub-units, KiBot
layer coverage — is complete on all 42; no board fails a structural check for
those any more. Everything left is a board defect: unresolved library references,
ERC, or DRC.

Green: `Loaf_ESPT`, `Loaf_x004`, `Slice_AQDO`, `Slice_AQEC`, `Slice_AQOR`,
`Slice_BUCK`, `Slice_DCMT`, `Slice_IOAC`, `Slice_LVAI`, `Slice_PRTO_CONN_S2L`,
`Slice_PRTO_THTA_S2L`, `Slice_PRTO_THT_S2L`, `Slice_RLAY`, `Slice_RLHT`,
`Slice_RTDM`, `Slice_TEMP_NANO_S2L-r1`, `Slice_TEMP_NANO_S2L-r2`,
`Slice_TEMP_NUCL_L4L-r1`, `Slice_TEMP_NUCL_S4L-r1`, `Slice_TEMP_PICO_L4L-r1`,
`Slice_TEMP_PICO_S2L-r1`, `Slice_THRM_31855`, `Slice_THRM_31856`, `Slice_USBP`,
`Slice_VCAC`.

## Critical path

Ordered by what it costs to get wrong, then by throughput.

### Tier 0 — real copper defects (6 boards)

The only items here that can ruin a fabrication run: shorts, mask bridges across
pads, clearance violations, drills out of range. They sat in boards whose CI
reported green for months.

DRC errors (violations + unconnected + parity), measured 2026-11-15, with the
error types behind each count.

| Board | DRC | Types |
| --- | --- | --- |
| `Slice_IOCT` | 20 | shorting_items 6, solder_mask_bridge 6, courtyards_overlap 1, unconnected 7 |
| `Slice_STEP` | 11 | footprint_type_mismatch 3, starved_thermal 3, parity 5 |
| `Slice_LOAD` | 7 | parity 7 |
| `Slice_GDHB` | 6 | zones_intersect 6 |
| `Slice_AOEM` | 5 | parity 5 |
| `Slice_AQPH` | 4 | starved_thermal 3, unconnected 1 |
| `Slice_FPSG` | 4 | shorting_items 2, solder_mask_bridge 2 |
| `Slice_IAQM` | 4 | parity 4 |
| `Slice_SOLR` | 4 | unconnected 4 |
| `Slice_STPC` | 3 | clearance 3 |
| `Slice_LEPD` | 2 | clearance 2 |
| `Slice_PRTO_SMT_S2L` | 1 | parity 1 |

71 DRC errors across 12 boards. Every parity error is
`footprint_symbol_mismatch`. The fab-fatal ones are shorts, mask bridges and
clearance: `Slice_IOCT` (12), `Slice_FPSG` (4), `Slice_STPC` (3) and
`Slice_LEPD` (2). `Slice_IOCT` holds the most by a wide margin — start there.
`Slice_SOLR` was the worst (14 copper defects) until its BQ24650 redesign dropped
it to 4 unconnected items.

### Tier 1 — schematic/PCB parity (22 errors)

Not fab-fatal, but the BOM, pick-and-place, or fab output disagrees with the
design. Each needs a decision about which side is right.

| Count | Issue | Board | Decision |
| --- | --- | --- | --- |
| 5 | `'Exclude from BOM' settings differ` (H1–H4, Logo1) | `Slice_STEP` | Should the part be in the BOM? |
| 4 | `KMLib_IC_SMD:RS_20_ADI-L` vs symbol's `RS_20_ADI` | `Slice_AOEM` | Which footprint is correct? |
| 1 | `Package_TO_SOT_SMD:TSOT-23-6` vs symbol's `SOIC_05WU-7_DIO` | `Slice_AOEM` | Which footprint is correct? |
| 7 | values on C6, C14, R9, R10; footprints on C14, R9, R10 | `Slice_LOAD` | Which value and footprint is correct? |
| 4 | values on C2, U1, R10, R16 | `Slice_IAQM` | Which value is correct? |
| 1 | `KMLib_Boards_Modules:Arduino_Nano_Headers` vs symbol's `Module:Arduino_Nano` | `Slice_PRTO_SMT_S2L` | Which footprint is correct? |

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

### Tier 3 — library re-points

The eleven boards that needed only re-points are green as of 2026-11-15: `AQDO`,
`AQEC`, `AQOR`, `BUCK`, `LVAI`, `TEMP_PICO_L4L-r1`, `TEMP_PICO_S2L-r1`,
`THRM_31855`, `THRM_31856`, `USBP`, `VCAC`. Each points at a stock KiCad or
KiCad-Master-Lib symbol or footprint with the same pin numbers or the same pads.
The schematic netlist is identical before and after, and ERC and DRC change only
by the findings on the re-pointed parts. Each part's drawing is kept, so KiCad
reports a `lib_symbol_mismatch` or `lib_footprint_mismatch` warning on it.
The custom logo art on `BUCK` and `USBP` was removed; both keep the stock OSHW
mark.

`Slice_IAQM` was listed here as library-only but also carries 4 parity errors.
Unresolved references remain on 11 boards that also have ERC or DRC errors:

| Board | Refs |
| --- | --- |
| `Slice_AQPH` | 1 |
| `Slice_LEPD` | 1 |
| `Slice_PHDO` | 1 |
| `Slice_GDHB` | 2 |
| `Slice_THMX` | 2 |
| `Slice_VCDC` | 2 |
| `Slice_IAQM` | 3 |
| `Slice_STEP` | 3 |
| `Slice_STPC` | 3 |
| `Slice_SERV` | 6 |
| `Slice_HEAT` | 7 |

## Suggested sequence

1. `Slice_IOCT` — the copper defects, highest cost of being wrong.
2. The other copper boards — `FPSG`, `STPC`, `LEPD`; then `SOLR`'s unconnected
   items.
3. The remaining library references above.
4. ERC `pin_to_pin` (8) — real electrical conflicts.
5. `PWR_FLAG`s and no-connects (24) — mechanical, fast.
6. Tier 1 parity decisions — BOM flags and footprint choices.

Copper, ERC and parity fixes are design decisions, made in the KiCad UI on each
board's branch. A library re-point can be scripted
(`boardwright sch DIR repoint`) when its pin numbers match and the netlist is
compared before and after.

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
