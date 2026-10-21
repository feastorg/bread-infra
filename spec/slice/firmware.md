# Slice Firmware Conventions

What every BREADS Slice's firmware does the same way, whatever its function.
[`bread-slice-core`](https://github.com/feastorg/bread-slice-core) implements
it. Wire semantics (opcodes, refusals, the command watchdog) live in
[`bread-crumbs-contracts`](https://github.com/feastorg/bread-crumbs-contracts),
not here. How the firmware pieces depend on each other is in
[Firmware Layering](../firmware-layering.md).

Each rule below is what Slice_DCMT and Slice_RLHT do today, unless it is
marked **open**.

## Status LED

A Slice with the BREADS status LED (one WS2812B on D5) shows:

| State | Colour |
| --- | --- |
| Booting, through the boot wait | blue |
| Running | green |
| E-stop held | red |

The LED is written only from the main loop, and only when its colour changes.

**Open:** whether a command-watchdog trip, or a latched fault such as an
over-temperature, gets its own colour or shares red.

## E-stop Input

- **Sampling.** Sampled once per main-loop pass, not by interrupt. A single
  asserted sample asserts the stop. Release needs the line released
  continuously for the debounce time. The press count increments once per stop.
- **Boot.** For the first second after reset, the firmware samples the e-stop
  continuously. A line held at power-up is asserted before the first loop pass.
- **Loop bound.** No loop pass may block. The e-stop latency is one pass.
- **What a stop does** is defined per family and published in the contracts'
  `docs/capabilities.md`.

**Open: polarity.** [Design Constraints](design-constraints.md) requires the
interlock chain to be wired so that "open state" means e-stop. The firmware
uses the internal pull-up and asserts on LOW, and the contracts'
`controller-compatibility.md` says "the e-stop pulls the slice's e-stop input
low". So an open or disconnected e-stop line reads as released. If the open
chain is turned into a LOW on the Slice's input upstream, on the Loaf, then both
statements hold, and this page should say where that happens. If not, the
firmware and the standard disagree.

## Boot

- Outputs are driven to their safe state before the main loop starts.
- The hardware watchdog (WDT) is enabled after the boot wait.

**Open:** which output pins must have defined levels from reset, before
firmware runs. A driver input left floating through reset and the bootloader
has no defined state.

## Command Watchdog

The timer and trip latch behave the same in every Slice: a trip latches until
cleared, and clearing resumes nothing. What refreshes the watchdog is defined
in the contracts (`bread_watchdog.h`). The trip action is per family.

## Serial Console

- Numeric arguments are parsed strictly. The whole token must parse, values
  must be finite and in range, and anything else is refused with no change.
- A serial command never bypasses a check that the CRUMBS path applies.
- Each main-loop pass handles at most one serial line.

These are the target, not yet true in either Slice
([feastorg/.github#3](https://github.com/feastorg/.github/issues/3)).
