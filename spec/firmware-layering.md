# Firmware Layering

Where the shared firmware for BREADS Slices lives, what each piece may depend
on, and how code moves between them. "Core" below is
[`bread-slice-core`](https://github.com/feastorg/bread-slice-core), the shared
Slice firmware library. What every Slice's firmware must do is in
[`slice/firmware.md`](slice/firmware.md).

## Layers

Dependencies point down only. A layer never includes a header from a layer
above it.

| Layer | Repo | Owns | Never contains |
| --- | --- | --- | --- |
| Slice firmware | `Slice_*` | Pin maps and board profiles; handler registration; validating and applying commands; control loops; what the safe state *is* for this family | Code copied from another Slice |
| Core | [`bread-slice-core`](https://github.com/feastorg/bread-slice-core) | Board mechanisms every Slice implements the same way: status LED, e-stop sampling and release debounce, the boot wait, the watchdog timer and trip latch, strict number parsing, and later the persistence record and writer | Protocol knowledge (no CRUMBS or contracts includes); family policy; control algorithms; device drivers |
| Contracts | [`bread-crumbs-contracts`](https://github.com/feastorg/bread-crumbs-contracts) | What a frame means on the wire: opcodes, payload layouts, units, capability bits, refusal reasons, documented semantics (for example what refreshes the watchdog) | Runtime behaviour beyond pack/unpack |
| Transport | [`CRUMBS`](https://github.com/feastorg/CRUMBS) | Framing, CRC, dispatch, GET_ACK, the I2C HALs | BREAD opcodes or semantics |
| Device and algorithm libraries | `LMD18200`, `DCMotorServo`, third party | One device or one algorithm, no BREAD knowledge | Slice or protocol policy |
| Standard | `bread-infra` (this repo) | What every Slice must do, in prose (`spec/`), plus schemas and hardware CI | Code that is compiled into firmware |

Core and contracts are siblings: neither includes the other. The Slice firmware
is where a wire command meets a mechanism. For example, the SET_WATCHDOG handler
decodes the contracts payload and calls the core's arm function.

## What May Enter Core

All of these must hold:

1. **BREADS requires it, or two Slices need it identically.** One Slice's need
   stays in that Slice until a second one needs the same thing.
2. **Mechanism, not policy.** Where families differ, core calls a hook the Slice
   provides. Core never decides what a safe state is.
3. **No protocol dependency.** It takes times, pins and values as arguments.
   Opcodes, payloads and refusal reasons stay above it.
4. **Non-blocking and bounded.** No call may hold the loop, since the e-stop is
   sampled there. No `delay()`, no dynamic allocation, and no serial output
   unless the caller asks for it.
5. **Host-tested in the core repo.** Every module has host tests, and
   hardware-specific code sits behind architecture guards that `#error` on
   unsupported MCUs. Nothing silently compiles to nothing.
6. **Small and explicit.** Plain functions and one state struct per module. No
   base classes, scheduler or framework. Each function documents whether it is
   ISR-safe.
7. **It names the clause.** Each module cites the section of this spec, or the
   contracts semantics, that it implements.

## How Changes Flow

- **Behaviour every Slice must show** (LED meanings, e-stop polarity and
  latching): spec first, here; then core; then each Slice adopts it.
- **Wire semantics** (a watchdog lease, setpoint selectors): contracts first,
  then each Slice's handlers. Core changes only if a mechanism changes.
- **Moving code into core:** add it to core with tests and release it. Each Slice
  then switches to it in its own PR, which the Slice's host tests must pass
  unchanged. The Slice copy is deleted in that same PR.
- **Versions:** core follows semver; 0.x minors may break and say so in its
  changelog. Slices pin `^0.minor`. A Slice may lag a core release, but two
  Slices on different core minors is a known state, listed in the core README.

## Examples That Test the Boundary

| Item | Placement |
| --- | --- |
| Status LED | Driver and the standard state colours in core; the state meanings in this spec |
| E-stop | Sampling, debounce, count and boot wait in core; what "stopped" does is a Slice hook |
| Watchdog | Timer and latch in core; what refreshes it is a contracts decision, wired in the Slice; the trip action is a Slice hook |
| Opcode is a command (`is_command_op()`) | A has-handler query in CRUMBS (transport), not core |
| Strict number parsing | Core, written once with tests |
| Validate-and-apply per operation | Each Slice |
| Persistent configuration | Record format, integrity check and non-blocking writer in core; which fields per family; the opcodes in contracts |
| Speed and position control | DCMotorServo |
