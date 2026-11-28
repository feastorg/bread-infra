# Slice Interface 1

Slice Interface 1 (SI1) is what a BREADS Slice must do to plug into a Loaf
slot: the connector, the pin map and the signals on it. Every Slice and Loaf
in the fleet uses it. Apart from two early designs that swapped INT and SYNC,
the slot has not changed since the first boards of 2021 ([Origins](#origins)).

Where the bus socket and the mounting holes sit on a Slice board is recorded
separately, under [Slice board formats](#slice-board-formats). It changed in
2024 without changing the slot: a board in either format plugs into the same
Loaf header.

This page records SI1 as built. Each statement is what the board files show
at each repo's `main` on 2026-11-27, unless it is marked **Not yet met**
(it names the boards that differ) or **Not defined** (no board settles it).
Who drives pins 6–8 also draws on the papers' pin table. RFC 0001
([#23](https://github.com/feastorg/bread-infra/pull/23)) proposes the
successor, Slice Interface 2.

Generations: G1 is the boards of the original OSF project (2021–2023), G2 the
2024 boards, and the designs in each repo's `hardware/` today are the next
round, not yet built. Labels such as "R0 2021" are quoted from board
silkscreen.

## Slot connector

- A Slice carries a 1x10 female socket at 2.54 mm pitch, right-angle (KiCad
  `PinSocket_1x10_P2.54mm_Horizontal`), on its bus edge. Its reference is
  not fixed: J1 on 28 Slices, J2 on 10, J4 on Slice_IOCT, J12 on
  Slice_PRTO_THTA_S2L.
- A Loaf carries a vertical 1x10 male header at each slot. Loaf_x004 uses
  KiCad-Master-Lib's `KMLib_Connectors:BREAD_Slice_Bus_10Pin`: the 1x10 row
  plus two Ø3.3 mm NPTH on the row's axis, 20 mm either side of the row
  centre, which locate the printed slot guide (below). LOAF_X08 (G1) used
  KiCad's `PinHeader_1x10_P2.54mm_Vertical`.
- Pin 1 is toward the Slice's top edge.

| Pin | Signal | Driven by | Use |
| --- | --- | --- | --- |
| 1 | GND | — | ground |
| 2 | +12V | the Loaf's supply input | supply |
| 3 | SCL | controller | I²C clock |
| 4 | SDA | controller, Slices | I²C data |
| 5 | GND | — | ground |
| 6 | E_STOP | the interlock chain (off the board), controller | the Slice stops on LOW ([E-stop](#e-stop)) |
| 7 | INT | Slices | interrupt toward the controller |
| 8 | SYNC | controller | synchronisation of the Slices |
| 9 | +12V | the Loaf's supply input | supply |
| 10 | GND | — | ground |

The papers' pin table (Oberloier 2021, Table 3.2; HardwareX 2023, Table 2)
says E_STOP and SYNC are "driven by loaf" and INT "driven by slice". In 2021
the controller sat on the Loaf, as LOAF_X08's own Arduino Nano. Today
Loaf_x004 is passive: its only parts are the supply jack and the 1x10
connectors. Ctrl_ESPT, an ESP32 controller, drives pins 6 and 8 and pulls
pin 7 up ([Logic levels](#logic-levels-and-pull-ups)).

The pin numbers are the interface; net names are not. The fleet calls the
grounds `GND` or `GNDPWR`, the I²C lines `I2C_CLK`/`I2C_DAT` (Slice_RLHT:
`I2C_TC_CLK` for pin 3) or `SCL`/`SDA`, and the stop `E_STOP`, `ESTOP` or
`ESTOP_BUS`. Loaf_x004 adds `_5V` to pins 3–8; Ctrl_ESPT uses `_3.3V` on
pins 3–4 and `_5V` on 6–8. Where a Slice calls the bus ground `GNDPWR`, its
logic ground is a separate net joined to it at one net tie, NT1.

A Slice's microcontroller joins pins 3, 4, 7 and 8 directly, through solder
"bus link" jumpers bridged by default (Slice_TEMP_NANO_S2L,
Slice_TEMP_PICO_S2L, Slice_TEMP_PICO_L4L, Slice_TEMP_NUCL_S4L,
Slice_TEMP_NUCL_L4L, Slice_IOCT, Slice_STPC), or through a 4-way DIP
switch (Slice_IOAC, Slice_PRTO_THTA_S2L).

- Slice_THMX leaves pin 7 unconnected: its Nano's `INT` net does not reach
  the socket.
- **Not defined:** which of pins 6–8 a Slice must connect, and the timing of
  INT and SYNC.

## Power

- +12V on pins 2 and 9, ground on pins 1, 5 and 10. There is no logic supply
  on the bus: each Slice makes its own from +12V.
- Loaf_x004 takes +12V from a barrel jack (J1) straight onto pins 2 and 9 of
  every slot and chain connector, with no fuse or reverse-polarity
  protection.
- **Not defined:** the current a slot may draw (no bus connector in the
  fleet records a part number, so no pin rating is on record), the supply's
  tolerance, and whether a Slice may be inserted with the Loaf powered.

## Logic levels and pull-ups

- E_STOP, INT and SYNC are 5 V signals, the Arduino Nano's level. Loaf_x004
  names them `E_STOP_5V`, `INT_5V`, `SYNC_5V`. Ctrl_ESPT joins its ESP32 to
  them through BSS138 level shifters (Q1–Q3) with 10 kΩ pull-ups to +5V (R4,
  R5, R6).
- **Not defined:** the I²C level. What pulls SDA and SCL up depends on the
  stack:
  - Ctrl_ESPT pulls them to +3.3V through 2.2 kΩ (R8, R9, behind solder
    jumpers JP3 and JP4, bridged by default) and adds an LTC4311 rise-time
    accelerator (U2). Its ESP32 drives pins 3–4 with no level translation.
  - Slice_IAQM ties the bus by default (JP1, JP2) to its BME280 and ENS160
    lines, which carry 4.7 kΩ to +3V3.
  - Slice_AOEM has four 4.7 kΩ pull-ups to +5V on each line, reaching the
    bus only when its open jumpers JP1 and JP2 are bridged to the bus side.
  - No other board carries I²C pull-ups: not Loaf_x004, not the Slice
    templates, not Slice_DCMT or Slice_RLHT.
- Seven Slices put 3.3 V parts on the bus lines with no level translation:
  - an RP2040 through bus link jumpers on Slice_TEMP_PICO_S2L,
    Slice_TEMP_PICO_L4L and Slice_STPC;
  - an STM32L432 Nucleo through jumpers on Slice_TEMP_NUCL_S4L and
    Slice_TEMP_NUCL_L4L, and directly on Slice_FPSG;
  - Slice_IAQM's sensors, as above.
- Ten Slices bring the bus SDA and SCL out on a 4-pin JST-SH connector with
  +5V and ground: Slice_HEAT, Slice_IAQM, Slice_LVAI, Slice_ACAR_S2L, Slice_RLAY,
  Slice_SERV, Slice_SOLR, Slice_THRM_31855, Slice_THRM_31856 and Slice_USBP.
  A device plugged in there is on the slot bus. **Not defined:** what may be
  connected there.
- **Not defined:** the I²C clock rate. The bench records in
  [Slice_DCMT](https://github.com/feastorg/Slice_DCMT) and
  [Slice_RLHT](https://github.com/feastorg/Slice_RLHT) `docs/bench/` run
  the bus at 50 kHz from a Raspberry Pi 4.

## E-stop

Pin 6 carries the e-stop. A Slice asserts the stop on LOW, and an open line
(a broken wire, an unplugged chain, an unseated Slice) must also stop. The
polarity rule is in
[Slice Firmware Conventions](firmware.md#e-stop-polarity), and the sampling
and boot rules in [E-stop Input](firmware.md#e-stop-input).

**Not yet met:** an open line reads as released
([#20](https://github.com/feastorg/bread-infra/issues/20)).

- Loaf_x004 has no pull on pin 6.
- Ctrl_ESPT pulls it up to +5V through 10 kΩ (R4).
- The Slice_DCMT and Slice_RLHT firmware enables the Nano's internal
  pull-up.
- Three Slices also load the line to ground through a series resistor and
  a pull-down: Slice_HEAT (1 kΩ and 1 MΩ, into a buffer), Slice_IOCT
  (1 kΩ and 100 kΩ, into a FET gate) and Slice_STPC (10 kΩ and 47 kΩ, into
  the motor supply's shutdown).

## Addressing

Each Slice's I²C address is fixed in its firmware at build time, and every
Slice on one bus needs its own. The published Slice firmware has done this
since 2021 (`#define I2C_ADR` in SLC_CR10's and SLC_DCMT R0's firmware on
OSF). No board has hardware addressing: a Slice's position in a Loaf does
not set its address. Oberloier's 2021 dissertation describes Slices
receiving their address from the Loaf at start-up (printed p. 32); no
published board or firmware does that.

## Chain connector

Loaves chain through 1x10 connectors that carry the slot pin map, numbered
pin for pin with the slot, so every slot on every chained Loaf shares one
bus.

- Loaf_x004 has one at each end: J2, a right-angle male header, and J7, a
  right-angle female socket. Its slots are 30.4 mm apart.
- Ctrl_ESPT has no slots. Its only 1x10 is J3, a right-angle female socket
  (the same part as Loaf_x004's J7) on its back side.
- The manifests record the chain connector as `1x10-2.54mm`.
- Loaf_CANPB has no board file and is not covered here.

## Slice board formats

A format fixes a Slice board's outline, where its bus socket sits, and its
mounting holes. It is not part of the slot: it sets how a board fits its
case and the printed slot guide that holds the case on the Loaf.

Coordinates are in millimetres, in the board's own frame as a designer sees
it in KiCad: the bus edge (the edge the socket faces) on the left, x from
the bus edge, y up from the bottom edge. The row centre is the midpoint of
the ten pin centres, between pins 5 and 6. Hole positions are measured from
the board's own edges.

| | G1 (2021–2023) | G2 (2024) and today |
| --- | --- | --- |
| Bus row centre | x 7.00, y 49.57 | x 3.60, y 50.02 |
| Mounting holes | 4 × Ø3.2 plated (M3), centres 5 from each edge | 4 × Ø5.0 NPTH, centres 5 from each edge |
| Boards | every G1 Slice on OSF (SLC_PHDO: x 7.05) | the G2 boards and every Slice in the fleet except those below |

Two outline sizes are in use with the G2 placement:

| Format | Board | Mounting holes |
| --- | --- | --- |
| S | 70 × 100 | (5, 5), (5, 95), (65, 5), (65, 95) |
| L | 100 × 145 | (5, 5), (5, 140), (95, 5), (95, 140) |

- Every G1 board is S-sized. No L board meets every L value: Slice_STPC and
  Slice_TEMP_PICO_L4L meet the outline, Slice_AOEM, Slice_THMX and
  Slice_TEMP_NUCL_L4L the bus row, and none the hole pattern.
- Slice board corners are R5.
- The mounting holes locate the case, not the Loaf. The case and the
  printed slot guide (bread-mechanical calls it the backplane part) are
  defined in [bread-mechanical](https://github.com/feastorg/bread-mechanical),
  `slice-case/design/synth/slot-interface-v1.1.json` and `formats.yaml`.
  `formats.yaml` gives the row as y 50.0 and records exceptions that predate
  Slice_STEP's 2026-11-27 hole change.
- **Not defined:** a tolerance (boards that meet a format match its values
  to 0.02 mm; those listed below differ by 0.1 mm or more), and board
  thickness (1.6 to 1.85 mm in the board files; Slice_DCMT is 1.85).

**Not yet met:**

| Board, `main` | Measured | Differs in |
| --- | --- | --- |
| [Slice_STEP](https://github.com/feastorg/Slice_STEP) `b9fdc8e` | row x 7.00, y 49.57; Ø5.0 NPTH holes | bus row still in the G1 place |
| [Slice_STPC](https://github.com/feastorg/Slice_STPC) `14c9c50`, [Slice_TEMP_PICO_L4L](https://github.com/feastorg/Slice_TEMP_PICO_L4L) `0776a39` | 100 × 145; row x 3.80, y 50.43; three holes 0.2 in | bus row and holes |
| [Slice_AOEM](https://github.com/feastorg/Slice_AOEM) `309f9a4`, [Slice_THMX](https://github.com/feastorg/Slice_THMX) `205785a`, [Slice_TEMP_NUCL_L4L](https://github.com/feastorg/Slice_TEMP_NUCL_L4L) `1aa59ff` | 100.12 × 144.89; holes up to 0.13 off in x or y | outline and holes |
| [Slice_FPSG](https://github.com/feastorg/Slice_FPSG) `8ffa8e3` | 100.12 × 99.95 | neither size |

Other records disagree with the boards:
[Design Constraints](design-constraints.md) says the header is "centered on
the left side" (true for S only) and gives "M3 bolts". Every manifest gives
`hole_size: "M3"` and `pattern: "slice-standard-v0"`. The manifests of
Slice_AOEM, Slice_THMX and Slice_STPC give `70mm x 100mm` for L-sized
boards.

## Manifests

A Slice manifest names SI1 as `slice-bus-10pin` in
`hardware.connectors[].type`, and a Loaf manifest names it in
`interconnect.bus.connector`
([Slice manifest](slice-manifest-spec.md),
[Loaf manifest](../loaf/loaf-manifest-spec.md)). The schemas accept any
string there.

## Origins

The slot pin map is the one in the first published description:
Oberloier's 2021 dissertation (Table 3.2, printed p. 29) and the HardwareX
paper (Table 2, p. 10). The board files agree:

- G1:
  - SLC_CR10 "R0 2021" (OSF ajmbe).
  - SLC_DCMT "R0 2021" (Slice_DCMT `archive/hw_archive/g1-2021-06-08-mtu`).
  - The LOAF_X08 backplane, silkscreen "LOAF R0 2022" (OSF x4yqj; [Loaf_x008](https://github.com/feastorg/Loaf_x008)).
- G2:
  - SLC_DCMT "R1 2024" (Slice_DCMT `archive/hw_archive/g2-2024-02-13-finn`).
  - SLC_RLHT "R2 2024" (Slice_RLHT `archive/hw_archive/finn_recent`).
- Today: every Slice and Loaf in the fleet.

**Exception:** SLC_LVAI "R0 2021" (OSF 742ez) and the 2020 Slice template
(kept as a KiCad backup in SLC_PUMP's OSF files) put SYNC on pin 7 and INT
on pin 8. Slice_LVAI's current design uses the order above.

What changed around the slot:

| | G1 (2021–2023) | G2 (2024) | Today |
| --- | --- | --- | --- |
| Loaf | LOAF_X08: 8 slots and its own Arduino Nano | LOAF_x04: 4 slots, chainable; LOAF_ESPTP, an ESP32 controller | Loaf_x004; Ctrl_ESPT |
| Loaf to Loaf | the dissertation: two RJ45 jacks, "amplified" (printed pp. 32, 65); LOAF_X08 as published: a 3-pin connector carrying I²C (HardwareX pp. 3, 8) | a right-angle 1x10 at each end, signals in slot order (the male header's footprint numbers its pins in reverse) | 1x10 header and socket, numbered pin for pin with the slot |
| Addressing | fixed in firmware | fixed in firmware | fixed in firmware |
| Controller | LOAF_X08's Nano; then a Raspberry Pi or BeagleBone running OpenReactor (Electronics 2023) | the ESP32 Loaf controller running Butter (Technologies 2025) | Ctrl_ESPT's ESP32; a Raspberry Pi 4 on the bench |
| Slice board format | G1 placement | G2 placement | G2 placement (Slice_STEP's bus row still G1) |
| Board rules | one or two layers, millable, 1206 or larger, through-hole preferred ([design-constraints-legacy](design-constraints-legacy.md)) | not recorded | boards made by a PCB fab, up to four layers; [Design Constraints](design-constraints.md) mixes the milling rules with fab colour conventions |

The publications are listed in [CITATION.md](../../CITATION.md).
