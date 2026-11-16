# Fleet remediation worklist

The detailed critical path for bringing the BREAD Slice fleet to a releasable
state: KiCad 10 format, library references that resolve, and ERC/DRC/Fab clean
under [`validate_board.py`](../scripts/validate_board.py).

Live status, the per-board checklist, and the open remediation PRs are tracked in
the epic, **#16**. This document holds the detailed tier breakdown and the
measurement method — the analysis that is too long for the epic body.

> **Re-measured 2026-11-15** with KiCad 10.0.8 ERC and DRC (`--schematic-parity`)
> at `error` severity, each board at the committed tip of its
> `chore/mechanical-remediation` branch. The library check is `validate_board.py`
> with the stock-name check from #26: a reference into a stock KiCad library must
> name a symbol or footprint that KiCad 10 ships. Without that check, 25 boards
> passed while their bus connector pointed at `Connector:Conn_01x10_Female`, which
> KiCad 10 no longer has. KiCad reports a missing library symbol only as an ERC
> warning. CI on the 26 board PRs pushed on 2026-11-15 agrees with their counts
> below.

**29 of 42 boards are green**, up from 14 on 2026-10-19. Mechanical remediation —
KiCad 10 format, DRC parity gate, Makefile targets, `.gitignore`, symbol
sub-units, KiBot layer coverage — is complete on all 42; no board fails a
structural check for those any more. Everything left is a board defect:
unresolved library references, ERC, or DRC.

Green: `Loaf_ESPT`, `Loaf_x004`, `Slice_AQDO`, `Slice_AQEC`, `Slice_AQOR`,
`Slice_BUCK`, `Slice_DCMT`, `Slice_GDHB`, `Slice_IOAC`, `Slice_LVAI`,
`Slice_PHDO`, `Slice_PRTO_CONN_S2L`, `Slice_PRTO_THTA_S2L`, `Slice_PRTO_THT_S2L`,
`Slice_RLAY`, `Slice_RLHT`, `Slice_RTDM`, `Slice_SERV`, `Slice_TEMP_NANO_S2L-r1`,
`Slice_TEMP_NANO_S2L-r2`, `Slice_TEMP_NUCL_L4L-r1`, `Slice_TEMP_NUCL_S4L-r1`,
`Slice_TEMP_PICO_L4L-r1`, `Slice_TEMP_PICO_S2L-r1`, `Slice_THMX`,
`Slice_THRM_31855`, `Slice_THRM_31856`, `Slice_USBP`, `Slice_VCAC`.

## What changed on 2026-11-15

- **Library references:** re-pointed to stock KiCad or KiCad-Master-Lib
  entries with the same pin numbers and roles, or the same pads.
  This includes the bus connector (`Conn_01x10_Female` → `Conn_01x10_Socket`)
  on 25 boards. The schematic netlist is identical before and after each
  re-point. Each part's drawing is kept, so KiCad reports a
  `lib_symbol_mismatch` or `lib_footprint_mismatch` warning on it.
- **Power flags:** `PWR_FLAG`s added on power nets that enter through a
  connector or a net tie (HEAT, SERV, PHDO, STEP, STPC, GDHB, THMX, LOAD). The
  redundant flag on STPC's GND removed.
- **No-connects:** no-connect flags on STPC's unused card-edge and sheet pins.
- **STEP:** the tantalum capacitors' footprint type set to SMD, matching their
  pads.
- **GDHB:** distinct priorities on overlapping same-net GND zones; the copper
  Gerbers are unchanged.
- **Logo art:** custom art removed on BUCK, USBP, SERV, STEP and IAQM; each
  keeps the stock OSHW mark.

## Critical path

Ordered by what it costs to get wrong, then by throughput.

### Tier 0 — DRC (62 errors, 11 boards)

DRC errors (violations + unconnected + parity) with the error types behind each
count.

| Board | DRC | Types |
| --- | --- | --- |
| `Slice_IOCT` | 20 | shorting_items 6, solder_mask_bridge 6, courtyards_overlap 1, unconnected 7 |
| `Slice_STEP` | 8 | starved_thermal 3, parity 5 |
| `Slice_LOAD` | 7 | parity 7 |
| `Slice_AOEM` | 5 | parity 5 |
| `Slice_AQPH` | 4 | starved_thermal 3, unconnected 1 |
| `Slice_FPSG` | 4 | shorting_items 2, solder_mask_bridge 2 |
| `Slice_IAQM` | 4 | parity 4 |
| `Slice_SOLR` | 4 | unconnected 4 |
| `Slice_STPC` | 3 | clearance 3 |
| `Slice_LEPD` | 2 | clearance 2 |
| `Slice_PRTO_SMT_S2L` | 1 | parity 1 |

Every parity error is `footprint_symbol_mismatch`. The fab-fatal ones are shorts,
mask bridges and clearance: `Slice_IOCT` (12), `Slice_FPSG` (4), `Slice_STPC`
(3) and `Slice_LEPD` (2).

- **IOCT's shorts come from two parts changed after the board was routed.**
  SW1's schematic symbol moved the common off the footprint's middle pad. D1
  was swapped from SOD-123F to DO-41 at the same anchor. A fix is drafted on
  the board's branch, not yet pushed: the common back on the middle pad, and D1
  re-placed as through-hole. It takes IOCT to 0 DRC violations and 3
  pre-existing unconnected GND-zone items. It waits for a datasheet check of the
  WS-SLTV pinout and a visual review.
- **FPSG's I2C tracks cross U2's unconnected pad CN3_3.**
- **STPC's VM tracks pass about 0.2 mm too close to the GND pad B16 of J3, J5
  and J6.**
- **LEPD's GNDA pour is about 0.02 mm short of its 0.5 mm clearance at J4.**
- **SOLR has a BQ24650 redesign in progress.**

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

### Tier 2 — ERC (15 errors, 3 boards)

| Board | Count | Type |
| --- | --- | --- |
| `Slice_VCDC` | 7 | `pin_to_pin` between U4's own ground pins |
| `Slice_VCDC` | 1 | `power_pin_not_driven` on U3 VDD1 |
| `Slice_VCDC` | 1 | `label_dangling` (IC_CURR1) |
| `Slice_STEP` | 4 | `pin_not_driven` on A1–A4 ~RESET |
| `Slice_IOCT` | 2 | `label_dangling` (I2C_CLK, I2C_DAT) |

VCDC's 8 power errors come from the KiCad-Master-Lib ADuM5010 symbol, which
types its ground pins as power outputs and VISO as unspecified
(feastorg/KiCad-Master-Lib#12). With that fixed, VCDC needs a `PWR_FLAG` on the
isolated ground and keeps only the dangling label.

### Tier 3 — library references (5 refs, 4 boards)

Every other reference resolves. These name parts that no library has yet:

| Board | Reference |
| --- | --- |
| `Slice_HEAT` | `BREAD_Slice-rescue:MAX31855KASA-Sensor_Temperature` (stock `MAX31855KASA` adds an NC pin 8) |
| `Slice_IAQM` | `KML-Custom:MicroSD_5025700893` (KMLib's `5025700893` differs: signal pads shifted 2.176 mm, shield pads mirrored) |
| `Slice_STEP` | `OCI_UPL_FOOTPRINTS:C_2312` (no library footprint has the same pads) |
| `Slice_STPC` | `KMLib_Connectors:PCIE-036-02-X-D-TH`, symbol and footprint |

## Suggested sequence

1. `Slice_IOCT` — review and push the drafted fix (shorts and mask bridges).
2. The other copper boards — `FPSG`, `STPC`, `LEPD`; then `SOLR`'s unconnected
   items.
3. KiCad-Master-Lib#12, then VCDC's isolated-ground flag.
4. The four parts no library has (Tier 3).
5. STEP's RESET inputs and starved thermals, AQPH's starved thermals.
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
