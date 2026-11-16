# 10 Rationale

[RFC 0001](README.md) · previous: [09 Bench plan](09-bench-plan.md)

Why each main choice was made, and what was considered instead.

## A 2×12 connector with a guide on the loaf

Slice Interface 1's 1×10 has no room for separate actuator and logic rails,
the position and interrupt lines, or grounds between the hazards. A 2×10 was
too small once each supply pin needed ground around it. Keys alone can't make
an unshrouded header safe: some offset and row-shifted insertions seat with a
key hanging off the end, and an exhaustive search found no key placement that
blocks them all.
The guide fixes position and row, and the keys then only have to block a
reversed board.

## A relay stop circuit, not an electronic latch

An earlier draft used an electronic RUN loop (a latch, a continuity probe and a
receiver on every slice) and an eFuse to cut V_ACT. The eFuse needed three
added parts before it would fail off, and the receivers cost every slice a pin
and parts. The relay start/stop circuit is the textbook stop-category-0
circuit: it powers up stopped, can't start into an open loop, needs no probe,
and frees D2 on every slice for the buffer enable.

The details each answer a single fault:

- **RUN_FEED from the loop's return**, not from the stop supply, so any open
  in the loop removes loaf coil power whatever K0 is doing.
- **Two force-guided relays in series**, because with one relay a welded
  contact restarts the stack as soon as the loop closes again.
- **A capacitor start**, because with the monitor contacts in a plain START
  path, each relay's monitor contact opens before its seal-in contacts close,
  and the latch would depend on armature momentum. It also means a stuck START
  starts nothing.
- **A supply-held relay on every loaf**, because firmware can't stop a
  controller re-sending its last command after a loaf's power returns.
- **A window detector driving it**, because a relay alone holds in down to
  about 10 % of its coil voltage, so a brownout would reset slices with V_ACT
  live. The window also replaces an input crowbar, which could latch on a
  current-limited supply without blowing its fuse.
- **A mandatory stop contact opened by RESET**, because a controller-driven
  RESET otherwise reboots every slice with V_ACT live.

A certified safety relay was not chosen for now; it can replace K0 and K1
later without changing the loafs or slices.

## One ground net

An earlier draft split the actuator return (GND_PWR) from logic ground, with a
link on every loaf and a Schottky tie on every slice. The split is what made a
lost return contact dangerous. Floating supplies, one per loaf, already keep
load current local, so one net is simpler and safer.

## An LTC4313-3 on every slice

One loaf can power up while another's bus is live, so a slice has to join a
busy bus cleanly. The LTC4313-3 connects only at bus idle, translates 3.3↔5 V,
goes high-impedance unpowered, and cuts a stuck slice off after 35–55 ms. It
doesn't help with clock-stretch losses, which it passes through, but its
cut-off isolates a slice whose firmware holds SCL low, which has happened on
the bench. Its cost is a few dollars per slice and a single source, which is
listed as open work.

## Automatic addressing

Compile-time addresses and DIP switches both let two slices end up at one
address. Encoding slot and chain position into one analog level costs one ADC
pin and a resistor network, and a misplaced slice can't pick the wrong address.
The E96 table is what gives the margin; the best E24 set left only 1.51 % of
full scale.

## 12 V and 24 V loafs

Common actuators come in 12 V and 24 V versions. One loaf design with two BOMs
keeps a single layout, and the voltage key keeps 12 V-only slices off 24 V
loafs.

## 50 kHz, provisionally, with an integrity check

A Pi 4 lost replies across clock stretch at 66 and 79 kHz and none at
49.7 kHz, but only with near-idle targets: masking interrupts brought the
failures back at 49.7 kHz, and the fleet's real firmware fails 3–22 % of
replies at 50 kHz under load ([03](03-bus.md#bus-integrity)). Lowering the
rate doesn't fix that, and neither does the buffer. SI2 therefore asks for two
things: a reply check that a truncated frame can't pass, so a bad reply is
never acted on, and a controller shown on the bench to tolerate the
stretching, so bad replies are rare. The bench runs real firmware because the
synthetic sketch passes where the fleet fails.

## Slices that know V_ACT is gone

Dropping the stop receiver freed D2 for the buffer enable, but it also left a
closed-loop slice blind to the stop: its loop winds up, it latches false
stalls, and START sends it to a stale setpoint. Sensing V_ACT costs an analog
pin and a divider, and booting disarmed with an explicit arm also covers a
slice that resets on its own and gets its last command re-sent. The stop
stays category 0, a cut rather than a controlled ramp-down, so holding loads
need their own brake; a category 1 option would need a timed cut on the head
and more to test.

## Two plain reserved pins

An earlier draft routed a matched differential pair through loafs and chain.
Nothing in SI2 uses it, so the standard that does can define the routing.

## Reference boards

The Nano Every, Nucleo-32 L432KC and Pico 2 are the boards the fleet already
runs or the Pico variant is built for. The Nano R4 is the cheapest 5 V Nano,
but its I²C target mode has an open core issue, so it stays a candidate until
the bench passes it.
