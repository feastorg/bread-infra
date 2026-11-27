# 02 Connectors

[RFC 0001](README.md) · previous: [01 System](01-system.md) · next:
[03 Bus and MCU site](03-bus.md)

## Slot connector

![The SI2 slot connector, 2×12 at 2.54 mm, rows A (next to the board) and B, positions 1 to 12 from the top. Row A: GND, V_ACT, KEY_A, V_LOGIC, GND, GND, GND, INT_N, VKEY, SCL, SDA, RSV1. Row B: GND, V_ACT, GND, GND, KEY_B, GND, RESET, SYNC, SLOT_ID, GND, VIO, RSV2.](figures/slot-pinmap.svg)

**CON-1** The slot connector MUST be a 2×12 at 2.54 mm with the map above:
vertical male on the loaf, right-angle female on the slice. The slice's bus
connector is J1.

| Pos | Row A | Row B |
| --- | --- | --- |
| 1 | GND | GND |
| 2 | V_ACT | V_ACT |
| 3 | KEY_A | GND |
| 4 | V_LOGIC | GND |
| 5 | GND | KEY_B |
| 6 | GND | GND |
| 7 | GND | RESET |
| 8 | INT_N | SYNC |
| 9 | VKEY | SLOT_ID |
| 10 | SCL | GND |
| 11 | SDA | VIO |
| 12 | RSV1 | RSV2 |

What each signal is and who drives it: [Signals](#signals).

### Card guide and keys

An unshrouded header can't locate the board it mates with. Every offset and
row shift that leaves a key hanging off the end of the header seats, and some
of those put V_ACT, V_LOGIC or VIO on the wrong pin. No key placement fixes
that, so the guide is part of the loaf.

**CON-2** Every SI2 slot MUST carry a card guide on the loaf: a U-guide closed
on both sides (the bread-mechanical backplane part's U-guides become part of
the loaf standard). The guide MUST engage before the pins touch. A printed
bench guide does the same for bare-board work.

**CON-3** Row keys: at KEY_A and KEY_B the loaf omits the post and the slice
blocks the socket hole. With position and row fixed by the guide, the keys
block the one misinsertion left, a reversed board.

**CON-4** Voltage key: a 24 V loaf fits a post at 9A (VKEY) and a 12 V loaf
leaves it out. A slice whose V_ACT loads are 12 V only MUST block hole 9A, so
it seats only on a 12 V loaf; every other slice MUST leave 9A open. VKEY is a
key, not a net: the loaf and the slice MUST leave 9A unconnected.

### Contacts

The two V_ACT pins carry 1.5 A each at the full 3 A, against a contact rating
of about 3 A. Return current goes through the two ground pins beside them, 1A
and 1B, and the slice's other ground pins share it if one opens.

**CON-5** Slices and loafs MUST leave RSV1 and RSV2 (12A, 12B) unconnected. A
later standard that uses them, for example for CAN, defines their routing, and
it MUST keep fault voltages off SDA and VIO beside them, which the buffer can't
take above 6 V. CAN on an SI2 slice goes on the slice's own connector, for
example an MCP2515 over SPI as
[can-nano-shield](https://github.com/feastorg/can-nano-shield) does, never
through the SI2 bus.

**CON-6** Slices MUST be inserted and removed with the loaf powered off.

### Mechanical checks still open

- The 2×12 body is ±15.24 mm. The case window grows to about ±17.9 mm,
  leaving about 0.45 mm to the loaf's locating holes. The next version of
  bread-mechanical's slot interface (`slot-interface-v1.1.json` today)
  confirms that or moves the holes.
- The second row moves the fin out 2.54 mm.
- The guide's lead-in length is set against the header post height.
- A socket with a real hole-blocking option still has to be found.

## Chain connector

![The chain header, 2×12 with odd pins on one row and even pins on the other. 12 V stop-circuit pins 1 (RUN_FEED), 12 (LOOP_OUT) and 24 (LOOP_RET) each have ground on every neighbour. An IN header has no post at pin 16, an OUT header none at pin 21.](figures/chain-pinmap.svg)

**CON-7** The chain MUST use a shrouded, polarised 2×12 box header and a short
IDC ribbon, with this map in ribbon order:

| Pin | Signal | Pin | Signal |
| --- | --- | --- | --- |
| 1 | RUN_FEED (12 V) | 13 | GND |
| 2 | GND | 14 | GND |
| 3 | GND | 15 | INT_N |
| 4 | POS1 | 16 | GND (IN key) |
| 5 | POS2 | 17 | SCL |
| 6 | POS3 | 18 | GND |
| 7 | POS4 | 19 | SDA |
| 8 | RESET | 20 | VIO |
| 9 | SYNC | 21 | GND (OUT key) |
| 10 | GND | 22 | GND |
| 11 | GND | 23 | GND |
| 12 | LOOP_OUT (12 V) | 24 | LOOP_RET (12 V) |

What each signal is and who drives it: [Signals](#signals).

On the header, pin *n* faces *n*±1 across the rows and *n*±2 along its row.
Each 12 V pin (1, 12, 24) has ground on every one of those, so no single bridge
joins two 12 V lines or puts 12 V on a signal. The bus sits away from all
three, because 12 V on a bus line would exceed the buffer's 6 V absolute
maximum. Ten signals and three 12 V lines with grounds around them don't fit a
2×10.

The chain carries no supply rail: VIO, the stop loop and RUN_FEED, with their
ground returns, are its only currents.

**CON-8** Each loaf MUST have a CHAIN IN header, toward the head, and a CHAIN
OUT header, both marked on the silkscreen. The head MUST have one CHAIN OUT
header. The chain MUST only go OUT to IN:

- an OUT header leaves out the post at pin 21, and an IN header the post at
  pin 16;
- each ribbon blocks hole 21 at its upstream end and hole 16 at its
  downstream end;
- the terminator plug blocks hole 21, so it fits only an OUT, and joins
  LOOP_OUT to LOOP_RET.

Pins 16 and 21 are grounds that guard no 12 V pin.

The keys stop a loaf being chained backwards, which nothing else catches.
Every pin meets its own signal across a ribbon, so a reversed loaf with the
terminator on its IN header closes the stop loop through its supply-held
contact and gets RUN_FEED. With the position lines wired as in CON-9, a
reversed loaf after the first sees at its IN header the line the loaf before
it sees and takes that loaf's addresses. Two slices then answer at each of
them, and a write meant for one reaches both.

### Position lines

**CON-9** The head grounds POS1 on its CHAIN OUT header. Each loaf senses the
position lines at its CHAIN IN header and wires IN POS*n* to OUT POS*n*+1 for
*n* = 1–3, so loaf *k* (*k* = 1–4 along the chain) sees ground on line *k*. IN
POS4 goes no further, and the loaf leaves OUT POS1 unconnected. Lines that
aren't grounded sit at VIO through a 100 k pull-up on each loaf. A loaf that
sees no grounded line leaves its SLOT_ID network open, so its slices don't join
([04](04-addressing.md)).

```mermaid
flowchart LR
    H["Head<br/>POS1 = GND"] -- "POS1" --> A["Loaf 1<br/>sees POS1"]
    A -- "POS1 → POS2" --> B["Loaf 2<br/>sees POS2"]
    B -- "POS2 → POS3" --> C["Loaf 3<br/>sees POS3"]
    C -- "POS3 → POS4" --> D["Loaf 4<br/>sees POS4"]
    D --> T["Terminator"]
```

## Controller cable

**CON-10** The head's controller header MUST carry SCL, SDA, INT_N, the SYNC
and RESET drive inputs, the stop contact's enable (STOP-6) and ground, all at
3.3 V. It carries no supply. Its connector and pin map are still open
([08](08-migration.md#spec-work-still-to-do)).

## Signals

| Signal | Pins | Driven by | What it is | See |
| --- | --- | --- | --- | --- |
| GND | slot 1A, 1B, 3B, 4B, 5A, 6A, 6B, 7A, 10B; chain 2, 3, 10, 11, 13, 14, 16, 18, 21, 22, 23 | — | The stack's one ground net. | GND-1 |
| V_LOGIC | slot 4A | loaf | The always-on logic supply, 12 or 24 V, 0.5 A per slot through a PTC. | PWR-1, PWR-3 |
| V_ACT | slot 2A, 2B | loaf | The actuator rail, 12 or 24 V, 3 A per slot through a 4 A fuse. The loaf's RUN relay cuts it when the stack stops. | PWR-3, OUT-1, OUT-7 |
| VIO | slot 11B; chain 20 | head | The 3.3 V bus rail. The bus, INT_N and SYNC levels, the position-line pull-ups and the SLOT_ID network run from it. | BUS-1, ADR-3 |
| SCL, SDA | slot 10A, 11A; chain 17, 19 | controller; slices answer and stretch SCL | I²C at 3.3 V, 50 kHz provisional, with one 2.2 k pull-up pair on the head. A slice connects only through its LTC4313-3. | BUS-1 to BUS-5 |
| INT_N | slot 8A; chain 15 | slices | Open-drain, active low, 10 k to VIO on the head. Optional per slice. | BUS-6, BUS-10 |
| SYNC | slot 8B; chain 9 | head | Push-pull at VIO; a rising edge means sample, high for at least 10 µs. Optional per slice; 100 k pull-down on the slice. | BUS-7, BUS-9 |
| RESET | slot 7B; chain 8 | head | Push-pull, active high, for at least 10 ms. Resets every slice and opens the stop contact. 100 k pull-down on the slice. | BUS-8, BUS-9, STOP-6 |
| SLOT_ID | slot 9B | loaf (resistor to ground) and slice (12.7 k pull-up) | One analog level giving the slice's loaf and slot. | ADR-2 to ADR-4 |
| POS1–POS4 | chain 4–7 | head grounds POS1; each loaf shifts it one line | Open or grounded, 100 k to VIO on each loaf. Tells each loaf its position. | CON-9 |
| RUN_FEED | chain 1 | head | 12 V from the stop loop through K0 and K1. Drives each loaf's RUN relay coil. | STOP-3 |
| LOOP_OUT, LOOP_RET | chain 12, 24 | head | The 12 V stop loop, out through each loaf's supply-held contact to the terminator and back. | STOP-1 |
| KEY_A, KEY_B | slot 3A, 5B | — | Row keys: no post on the loaf, a blocked hole on the slice. | CON-3 |
| VKEY | slot 9A | — | Voltage key: a post on a 24 V loaf, a blocked hole on a 12 V-only slice. No net. | CON-4 |
| RSV1, RSV2 | slot 12A, 12B | — | Reserved, unconnected. | CON-5 |
