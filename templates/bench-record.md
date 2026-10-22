---
title: "YYYY-MM-DD: short description"
parent: Bench Records
---

<!-- Copy to docs/bench/YYYY-MM-DD-<short-slug>.md and add a row to
     docs/bench/README.md. Guide: bread-infra spec/slice/bench-records.md.
     Delete these comments and any section that does not apply. -->

# YYYY-MM-DD: short description

**Verifies:** <issue or PR links>
**By:** <name>

## Setup

| | |
| --- | --- |
| Firmware | `<commit>`, env `<pio env>` <!-- note any uncommitted changes --> |
| Board | <generation or revision>, <MCU> <!-- and anything unusual about this board --> |
| Controller | <what sends commands, and over what: serial, I2C> |
| Outputs | <what is connected: motors, encoders, heaters, nothing> |

## Steps and Results

| Step | Expected | Observed | Result |
| --- | --- | --- | --- |
| <command or action> | <what should happen> | <what you saw> | pass / fail / skipped |

## Raw Output

```text
<paste output here, or link docs/bench/assets/<record>/...>
```

## Not Checked

- <steps skipped, things not observable on this rig, limits of the result>

## Notes

<!-- Anything odd. Later corrections go here as dated notes; don't rewrite
     the results above. -->
