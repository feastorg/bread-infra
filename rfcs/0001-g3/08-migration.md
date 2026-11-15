# 08 Migration and Open Work

[RFC 0001](README.md) · previous: [07 Mechanical](07-mechanical.md) · next:
[09 Bench plan](09-bench-plan.md)

## What G3 changes elsewhere

When this RFC is accepted, each of these becomes a tracked issue:

- [`spec/slice/firmware.md`](../../spec/slice/firmware.md): the status LED
  moves from D5 to D9; the e-stop input becomes V_ACT sense; addresses come
  from SLOT_ID.
- [`spec/slice/design-constraints.md`](../../spec/slice/design-constraints.md):
  fab-first replaces "manufacturable on commonly available circuit milling
  machines", the through-hole preference and the 0805 minimum; the 2×12
  replaces the "Standard 10-pin female header".
- The manifest schema and all 40 `slice.yaml` files: `type: "slice-bus-10pin"`,
  and `hw_gen` and `address_default` get G3 meanings.
- The six `Slice_TEMP_*` templates and `slice.yaml.template`.
- Slice_DCMT and Slice_RLHT firmware: `LED_PIN 5`. DCMT also uses A3 and D9 for
  its encoder and motor, which G3 takes, and it needs 14 free pins: on an Every
  it fits by leaving out SYNC or INT_N; otherwise it moves to the Pico variant
  or adds an I/O expander on its private bus.
- CRUMBS: discovery from SLOT_ID, the 50 kHz bus, and the 30 ms clock-stretch
  contract.
- Slice_DCMT's docs: rename its "G1–G3" generations to revisions r1–r3.

## Spec work still to do

- Connector part numbers, including a socket with a real hole-blocking option,
  for the slot and for the chain ribbon.
- The head schematic: the stop circuit, the stop supply, VIO, and the chain
  pin map.
- Part requirements and candidates for K0 and K1 (force-guided), the loaf RUN
  and supply-held relays, the loaf window detector, and the 20 A loaf input
  connector.
- The buffer's price and second source: the LTC4313-3 is single-source.
- The firmware contract: the proxy family, outputs off at boot, V_ACT sense.
- The motor-slice regeneration clamp (PWR-8).
- The mains creepage distance (ISO-1).
- A conformance checklist and a KiCad template (the 2×12 footprint and the BIB
  as a sheet), so another builder can check a design.

## Items marked *verify*

- RP2350 erratum E9 against the 4.7 k BUS_EN pull-down (BUS-3).
- The WS2812 on D9 clear of D7/D8 on the Nucleo-32 (MCU-1).
- The Nano R4's 5V-pin entry and its I²C target mode (MCU-2).
- The Nucleo-32 G431KB's +5V range (MCU-2).
- D0/D1 on the Nucleo-32 (MCU-2).
