# RFC 0001: Slice Interface 2

| | |
| --- | --- |
| Status | **Draft** |
| Created | 2026-11-15 |
| Replaces | Slice Interface 1, the 1×10 bus of every G1–G3 board ([design constraints](../../spec/slice/design-constraints.md)) |
| Acceptance | the bench tests in [09 Bench plan](09-bench-plan.md) pass, including runs of real slice firmware under load, or this RFC changes to match what they measure |

Slice Interface 2 (SI2) is the second interface between a BREADS Slice and the
Loaf it plugs into. Every board so far, G1 to G3, uses Slice Interface 1, the
1×10 bus. The first boards built to SI2 are generation G4. Generations,
revisions and interfaces are separate labels; [terminology](../../spec/terminology.md#generations-revisions-and-interfaces) defines
them. SI2 defines:

- **Connector:** a keyed 2×12 at 2.54 mm, with a card guide on the loaf at
  every slot.
- **Power:** 12 V or 24 V per loaf, with a voltage key, and one ground net.
- **Bus:** an idle-connect bus interface block (BIB) on every slice, between
  its MCU and a 3.3 V I²C bus at 50 kHz.
- **Stop:** a relay start/stop circuit at the head, whose loop runs out and
  back through every loaf; a relay on each loaf cuts actuator power. It is a
  **non-safety-rated interlock**.
- **Addressing:** automatic, from the slice's slot and its loaf's position in
  the chain, read as one analog level.
- **MCU site:** a Nano-format socket with a per-board pin and power table, plus
  a Pico variant.
- **Manufacturing:** fab-first.

SI2 is not backward compatible with Slice Interface 1: G1–G3 boards don't
plug into an SI2 loaf.

## Documents

| | Covers |
| --- | --- |
| [01 System](01-system.md) | controller, head, loafs, slices; what each one carries; capacity |
| [02 Connectors](02-connectors.md) | the slot connector, card guide and keys; the chain connector |
| [03 Bus and MCU site](03-bus.md) | the bus interface block, bus signals, the MCU pin and board tables, the sensor-carrier pattern |
| [04 Addressing](04-addressing.md) | addresses, the SLOT_ID network and its table, reserved addresses |
| [05 Stop and interlock](05-stop.md) | the stop circuit, its fault behaviour and known limits, the outputs rule |
| [06 Power and ground](06-power.md) | rails, loaf input protection, the supply window, ground and earth, mains and isolation |
| [07 Mechanical](07-mechanical.md) | formats, datums, zones, envelope; generations and versions |
| [08 Migration and open work](08-migration.md) | what SI2 changes elsewhere; spec work still to do |
| [09 Bench plan](09-bench-plan.md) | the tests that gate acceptance, and the parts they need |
| [10 Rationale](10-rationale.md) | why each main choice was made, and what was considered instead |

## Conventions

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be interpreted
as described in BCP 14 ([RFC 2119](https://www.rfc-editor.org/rfc/rfc2119),
[RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)) when, and only when, they
appear in all capitals.

Requirements carry an ID (such as **STOP-3**) so a conformance checklist can
cite them. A figure marked *estimate* is a calculation, not a measurement. An
item marked *verify* has not yet been checked against a datasheet or a bench.
Nothing in this RFC has been measured on a bench yet.

## Terms

| Term | Meaning |
| --- | --- |
| Slice | a function board that plugs into one slot |
| Loaf | a backplane with up to four slots |
| Head | the chained board that joins the controller to the loafs and holds the stop circuit |
| Stack | one head, its loafs and their slices |
| Chain | the ribbon connection head → loaf → loaf → terminator |
| BIB | the bus interface block on each slice |
| V_ACT | the stop-switched actuator rail |
| V_LOGIC | the always-on logic supply to each slot |
| VIO | the 3.3 V bus rail, from the head |
| IOREF | a slice's MCU-side logic voltage, 3.3 V or 5 V |

## Decisions

| ID | Decision | See |
| --- | --- | --- |
| C1 | Keyed 2×12 slot connector at 2.54 mm; a card guide on the loaf at every slot; row keys, a voltage key, 2 reserved pins | [02](02-connectors.md) |
| C2 | Chain: a shrouded, polarised 2×12 box header and ribbon carrying the bus, VIO, INT_N, SYNC, RESET, four position lines, the stop loop out and back, RUN_FEED and ground; no supply rail; keyed OUT to IN | [02](02-connectors.md#chain-connector) |
| E1 | Bus at 3.3 V on VIO, 50 kHz provisional; an LTC4313-3 on every slice; replies carry an integrity check a truncated frame can't pass; the controller must tolerate clock stretching, shown on the bench with real slice firmware | [03](03-bus.md) |
| E2 | One 2.2 k pull-up pair per bus, on the head, removed when the controller has its own | [03](03-bus.md) |
| E3 | Stop: relay start/stop circuit with two force-guided relays and a capacitor start; the loop runs through a window-held relay on every loaf; RUN_FEED from the loop drives a relay per loaf that cuts V_ACT | [05](05-stop.md) |
| E4 | SLOT_ID carries slot and loaf; SYNC and INT_N optional per slice; RESET shared | [03](03-bus.md), [04](04-addressing.md) |
| E5 | Every actuator slice senses V_ACT, goes safe and stays disarmed when it drops, and boots disarmed; back-drivable loads need a brake | [05](05-stop.md#outputs) |
| P1 | 12 V or 24 V per loaf, with a voltage key; V_LOGIC 9–30 V, 0.5 A per slot; V_ACT 3 A per slot through a 4 A fuse | [06](06-power.md) |
| P2 | One ground net; one floating-output supply per loaf, feeding only that loaf; at most one earth reference per stack | [06](06-power.md#ground) |
| U1 | Nano-format socket plus a Pico variant, with a fixed pin map and a per-board power-entry table | [03](03-bus.md#mcu-site) |
| S1 | Sensor-carrier pattern: direct or proxy, chosen by jumpers | [03](03-bus.md#sensor-carrier-pattern) |
| F1 | Fab-first, with PCBA outputs in CI; variant BOMs fix IOREF | [07](07-mechanical.md) |

## Sources

- The KiCad board files of the 40 existing slices and the existing loafs.
- This repository's [`spec/`](../../spec/), including
  [`slice/firmware.md`](../../spec/slice/firmware.md) and
  [`slice/design-constraints.md`](../../spec/slice/design-constraints.md); the
  slot interface and case model in
  [bread-mechanical](https://github.com/feastorg/bread-mechanical).
- [CRUMBS](https://github.com/feastorg/CRUMBS), including the clock-stretch
  measurements in its `docs/protocol.md`; the
  [Slice_DCMT](https://github.com/feastorg/Slice_DCMT) and
  [Slice_RLHT](https://github.com/feastorg/Slice_RLHT) firmware and docs.
- The BREAD HardwareX paper (2023), Table 2; see [CITATION.md](../../CITATION.md).
- Datasheets: ADI LTC4313 (Rev F), ATmega4809, STM32L432KC, Arduino Nano R4
  (ABX00142) and Nano ESP32 (ABX00083), and the Arduino Nano family.
- Adafruit's I²C address list.
