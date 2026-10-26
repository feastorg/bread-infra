# Slice Firmware Conventions

What every BREADS Slice's firmware does the same way, whatever its function.
[`bread-slice-core`](https://github.com/feastorg/bread-slice-core) implements
it. Wire semantics (opcodes, refusals, the command watchdog) live in
[`bread-crumbs-contracts`](https://github.com/feastorg/bread-crumbs-contracts),
not here. How the firmware pieces depend on each other is in
[Firmware Layering](../firmware-layering.md).

Each rule below is what Slice_DCMT and Slice_RLHT do today, unless it is
marked **Not yet met**, which names the boards and libraries that fall short.

## Status LED

A Slice with the BREADS status LED (one WS2812B on D5) shows:

| State | Colour |
| --- | --- |
| Booting, through the boot wait | blue |
| Running | green |
| E-stop held | red |
| A firmware hold: a command-watchdog trip, or a latched fault such as an over-temperature | amber |

Red wins over amber: with the e-stop held and a trip latched, the LED is red.
Red means the hardware line needs attention; amber means the Slice is holding
on its own, and is cleared at the console or by the controller
(`CLEAR_WATCHDOG_TRIP`, `CLEAR_FAULTS`).

The LED is written only from the main loop, and only when its colour changes.

**Not yet met:** `bread-slice-core` 0.1 has no amber state, so a trip or a
fault shows green today
([feastorg/bread-slice-core#3](https://github.com/feastorg/bread-slice-core/issues/3)).

## E-stop Input

- **Sampling.** Sampled once per main-loop pass, not by interrupt. A single
  asserted sample asserts the stop. Release needs the line released
  continuously for the debounce time. The press count increments once per stop.
- **Boot.** For the first second after reset, the firmware samples the e-stop
  continuously. A line held at power-up is asserted before the first loop pass.
- **Loop bound.** No loop pass may block. The e-stop latency is one pass.
- **What a stop does** is defined per family and published in the contracts'
  `docs/capabilities.md`.

## E-stop Polarity

[Design Constraints](design-constraints.md) requires the interlock chain to be
wired so that "open state" means e-stop: a broken wire, an unplugged
connector or an unseated Slice must stop, not run. The e-stop line is bus
pin 6. To meet the rule:

- The chain sources the run level. +5V feeds the line through the chain's
  normally closed contacts in series; a pull-down on the Loaf holds the line
  LOW when any contact opens or the chain is unplugged.
- A Slice asserts e-stop on LOW, as today, and reads the line with no
  internal pull-up. With several Slices on the bus, their pull-ups in
  parallel (20 to 50 kOhm each on the ATmega328P and ATmega4809) would hold an
  open line HIGH against the pull-down.
- Anything else that stops the system, such as a controller, pulls the line
  LOW, as the contracts' `controller-compatibility.md` describes.

**Not yet met.** From the schematics (netlists exported from each repo's
`hardware/` on 2026-10-25), today's boards read an open line as released:

| Board | E-stop line |
| --- | --- |
| Loaf_x004 | `E_STOP_5V` passes bus pin 6 between the chain connectors (J2, J7) and the four Slice sockets, with no pull resistor |
| Loaf_ESPT | `E_STOP_5V` has a 10 kOhm pull-up to +5V (R4), and a BSS138 level shifter (Q1) lets the ThingPlus pull it LOW |
| Slice_DCMT, Slice_RLHT | bus pin 6 goes straight to the Nano's D2; the firmware enables the internal pull-up |

So the line idles HIGH and stops only when driven LOW; an open chain reads as
released on every Slice
([#20](https://github.com/feastorg/bread-infra/issues/20); the Slice side is
[feastorg/bread-slice-core#3](https://github.com/feastorg/bread-slice-core/issues/3)).

## Boot

- Outputs are driven to their safe state before the main loop starts.
- The hardware watchdog (WDT) is enabled after the boot wait.

Through reset and the bootloader, before firmware runs, every pin is a
high-impedance input. So every output that can actuate a load has a defined
safe level from reset without firmware: an external resistor to the level
that leaves the load off, or a load that is off when its pin is
high-impedance.

Slice_RLHT meets this: each relay output drives an optocoupler LED (TCMT1100)
through 180 Ohm, and an undriven pin lights nothing. Slice_DCMT does not yet:
the PWM, DIRECTION and BRAKE inputs of both LMD18200 drivers connect only to
Nano pins, with no resistor, so they float until the firmware drives them
([feastorg/Slice_DCMT#83](https://github.com/feastorg/Slice_DCMT/issues/83)).

## Command Watchdog

The timer and trip latch behave the same in every Slice: a trip latches until
cleared, and clearing resumes nothing. What refreshes the watchdog is defined
in the contracts (`bread_watchdog.h`). The trip action is per family.

## Serial Console

- Numeric arguments are parsed strictly. The whole token must parse, values
  must be finite and in range, and anything else is refused with no change.
- A serial command never bypasses a check that the CRUMBS path applies.
- Each main-loop pass handles at most one serial line.

Strict parsing and one line per pass are true in both Slices
(Slice_DCMT#60 and #49, Slice_RLHT#51 and #39). The second rule is not yet:
some commands are still implemented separately for serial and CRUMBS
([feastorg/.github#3](https://github.com/feastorg/.github/issues/3)).
