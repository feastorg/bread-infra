# Slice Interface 1

Slice Interface 1 (SI1) is the contract between a BREADS Slice and the Loaf
slot it plugs into: the 10-pin bus, the signals on it, and where the bus and
mounting holes sit on the board. Every Slice and Loaf built so far uses it.
Its slot pin map has not changed since the first boards of 2021
([Origins](#origins)).

This page records SI1 as built. Each rule is what the fleet's board files
show at each repo's `main` on 2026-11-27, unless it is marked **Not yet
met**, which names the boards that differ. RFC 0001
([#23](https://github.com/feastorg/bread-infra/pull/23)) proposes its
successor, Slice Interface 2.

## Slot connector

- A Slice carries a 1x10 female socket at 2.54 mm pitch, right-angle
  (KiCad `PinSocket_1x10_P2.54mm_Horizontal`), on its bus edge.
- A Loaf carries a 1x10 male header, vertical, at each slot (LOAF_X08 uses
  KiCad's `PinHeader_1x10_P2.54mm_Vertical`; bread-mechanical's slot
  datums model the same header for Loaf_x004).
- Pin 1 is toward the Slice's top edge.

| Pin | Signal | Driven by | Use |
| --- | --- | --- | --- |
| 1 | GND | — | ground |
| 2 | +12V | Loaf | supply |
| 3 | SCL | bus controller | I²C clock |
| 4 | SDA | bus controller, Slices | I²C data |
| 5 | GND | — | ground |
| 6 | E_STOP | Loaf (the interlock chain), controller | the Slice stops on LOW ([E-stop](#e-stop)) |
| 7 | INT | Slice | interrupt toward the controller |
| 8 | SYNC | Loaf | synchronisation toward the Slices |
| 9 | +12V | Loaf | supply |
| 10 | GND | — | ground |

The pin numbers are the interface; net names are not. The fleet calls the
grounds `GND` or `GNDPWR`, the I²C lines `I2C_CLK`/`I2C_DAT` or
`SCL`/`SDA`, and the stop `E_STOP`, `ESTOP` or `ESTOP_BUS`; Loaf_x004 adds a
`_5V` suffix. Who drives pins 6–8 follows the HardwareX paper's Table 2;
the controller's pull on pin 6 is in
[Slice Firmware Conventions](firmware.md#e-stop-polarity). SI1 does not
define the timing of INT or SYNC.

## Power

- +12V on pins 2 and 9, ground on pins 1, 5 and 10.
- There is no logic supply on the bus. Each Slice makes its own from +12V.
- **Not defined:** the current a slot may draw, the supply's tolerance, and
  whether Slices may be inserted with the Loaf powered.

## Logic level and pull-ups

- The bus signals run at the Arduino Nano's 5 V. Loaf_x004 names its bus
  nets `SCL_5V`, `SDA_5V`, `E_STOP_5V`, `INT_5V`, `SYNC_5V`.
- No board in the fleet carries I²C pull-up resistors: not Loaf_x004, not
  the Slice templates, not Slice_DCMT or Slice_RLHT. The bus is pulled up by
  whatever the controller and the Slices' microcontrollers provide, so its
  high level and rise time depend on what is in the stack.
- **Not defined:** a 3.3 V microcontroller on the bus.
  `Slice_TEMP_PICO_S2L-r1` joins the RP2040's GPIO to the bus lines through
  solder jumpers, with no level translation. `Loaf_ESPT` names its bus I²C
  nets `SCL_3.3V`, `SDA_3.3V`. SI1 does not say what level a mixed bus runs
  at.

## E-stop

Pin 6 carries the e-stop. A Slice asserts the stop on LOW, and an open
line (a broken wire, an unplugged chain, an unseated Slice) must also stop.
The polarity, sampling and boot rules are in
[Slice Firmware Conventions](firmware.md#e-stop-polarity).

**Not yet met:** today's Loafs and Slices pull the line HIGH, so an open
line reads as released
([#20](https://github.com/feastorg/bread-infra/issues/20)).

## Addressing

Each Slice's I²C address is fixed in its firmware at build time, and every
Slice on one bus needs its own. SI1 has no hardware addressing: the
position of a Slice in a Loaf does not set its address.

## Chain connector

Loafs chain through a second 1x10 at each end. On
[Loaf_x004](https://github.com/feastorg/Loaf_x004) these are J2, a
right-angle male header, and J7, a right-angle female socket. Both carry
the slot pin map pin for pin, so every slot on every chained Loaf shares
one bus. Loaf_x004's slots are 30.4 mm apart.

## Mechanical

Coordinates are in the board's own frame as a designer sees it in KiCad:
bus edge on the left, x from the bus edge, y up from the bottom edge.

| Format | Board | Bus pin row (row centre) | Mounting holes |
| --- | --- | --- | --- |
| S | 70 × 100 mm | x 3.6, y 50.0 | 4 × Ø5.0 NPTH at (5, 5), (5, 95), (65, 5), (65, 95) |
| L | 100 × 145 mm | x 3.6, y 50.0 | 4 × Ø5.0 NPTH at (5, 5), (5, 140), (95, 5), (95, 140) |

- Board corners are R5.
- The template boards put the row centre at y 50.02; every board that
  meets the format sits there.
- The mounting holes locate the Slice's case, not the Loaf. The case and
  the printed backplane part that holds it are defined in
  [bread-mechanical](https://github.com/feastorg/bread-mechanical)
  (`slice-case/design/synth/slot-interface-v1.1.json` and `formats.yaml`).

**Not yet met:**

| Board | Measured | Differs in |
| --- | --- | --- |
| [Slice_STEP](https://github.com/feastorg/Slice_STEP) | row x 7.00, y 49.57 | bus position: 3.4 mm in from the edge |
| [Slice_STPC](https://github.com/feastorg/Slice_STPC), [Slice_TEMP_PICO_L4L-r1](https://github.com/feastorg/Slice_TEMP_PICO_L4L-r1) | 100 × 145; row x 3.80, y 50.43; three holes 0.2 mm in | bus position and holes |
| [Slice_AOEM](https://github.com/feastorg/Slice_AOEM), [Slice_THMX](https://github.com/feastorg/Slice_THMX), [Slice_TEMP_NUCL_L4L-r1](https://github.com/feastorg/Slice_TEMP_NUCL_L4L-r1) | 100.12 × 144.89; holes up to 0.13 mm off in x or y | outline and holes |
| [Slice_FPSG](https://github.com/feastorg/Slice_FPSG) | 100.12 × 99.95 | neither format |

## Manifests

A Slice or Loaf manifest names SI1 by its bus connector type,
`slice-bus-10pin` ([Slice manifest](slice-manifest-spec.md)).

## Origins

The slot pin map above is the one the first published description gives
(Oberloier's 2021 dissertation, Table 3.2; the HardwareX paper, Table 2),
and the board files agree:

- G1: Slice_CR10 "R0 2021" and Slice_DCMT "R0 2021", the LOAF_X08
  backplane "R0 2022".
- G2: Slice_DCMT "R1 2024" and Slice_RLHT "R2 2024".
- Today: every Slice and Loaf in the fleet.

A 2021 Slice and a Slice designed today fit the same slot. What changed is
around the slot:

| | 2021–2023 | 2024 | Today |
| --- | --- | --- | --- |
| Loaf | LOAF_X08: 8 slots and its own Arduino Nano | LOAF_x04: 4 slots, chainable | Loaf_x004 |
| Loaf to Loaf | RJ45 daisy chain in the 2021 draft; a 3-pin connector on LOAF_X08 | a right-angle 1x10 at each end | 1x10 header and socket, slot order |
| Addressing | assigned by the Loaf at start-up in the 2021 draft; fixed in firmware by 2023 | fixed in firmware | fixed in firmware |
| Bus controller | LOAF_X08's Nano; then a Raspberry Pi or BeagleBone running OpenReactor | an ESP32 Loaf controller running Butter | a Raspberry Pi or similar single-board computer on the Loaf's I²C |
| Board rules | single-layer, millable, 1206 or larger, through-hole preferred | not recorded | boards made by a PCB fab; [Design Constraints](design-constraints.md) still describes milled boards |

The publications are listed in [CITATION.md](../../CITATION.md).
