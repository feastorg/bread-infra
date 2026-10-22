# Bench Records

A bench record is the write-up of one session of testing real hardware: what
was run, on what, and what happened. Each Slice keeps its records in
`docs/bench/`, one file per session, with a table of them in
`docs/bench/README.md`.

A good record lets someone who wasn't there tell what was tested, on what
hardware and firmware, and how far to trust the result. That is the whole
standard. Everything below serves it.

Start from [`templates/bench-record.md`](../../templates/bench-record.md).

## What to Include

- **When and who.** The date, and who ran it.
- **What firmware.** The commit hash it was built from, and the PlatformIO env.
  If the tree had uncommitted changes, say so and say what they were.
- **What hardware.** The board, its revision or generation, and the MCU. Note
  anything unusual about this particular board, such as a rework or a swapped
  part.
- **The rig.** The controller and how it talks to the board (serial, I2C and
  from what), and what is connected to the outputs (motors, heaters, nothing).
- **What you did.** The steps or commands, in order. If you followed a plan
  written elsewhere, link it and note where you departed from it.
- **What happened, per step.** Pass, fail or skipped, with what you actually
  saw: the reading, the reply, the motor's behaviour. "Works" on its own tells
  the next reader nothing.
- **Raw output.** Paste it in a fenced block, or attach the log under
  `docs/bench/assets/<record>/`. The summary is your reading of it, and a
  later reader may need to check that reading.
- **What wasn't checked.** Steps you skipped, things you couldn't observe, and
  anything a passing result here does not show.

## Keeping Records Useful

- **Failures and skips belong in the record.** A record that lists only the
  passes reads as complete when it may not be.
- **A number comes with its source:** the command, instrument or log line that
  produced it. Label an estimate as one.
- **Don't rewrite a past record's results.** If something turns out to be
  wrong, add a dated note at the end of that record, or write a new record and
  link back. Records are a lab notebook, not a wiki page.
- **One session, one record.** Testing several boards in one sitting is still
  one session. Testing the same board on another day is a new record.

## Mechanics

- **File name:** `YYYY-MM-DD-<short-slug>.md`, for example
  `2026-10-22-applied-pwm-and-serial-burst.md`.
- **Photos and logs:** go in `docs/bench/assets/<file name without .md>/`.
- **The table:** add the record's row to the table in `docs/bench/README.md`
  in the same PR as the record.
- **Links:** link the record from the issue or PR it verifies, and link that
  issue or PR from the record.
- **These repos are public.** Leave out network addresses, hostnames on private
  networks, credentials and personal details. Photos are fine when nothing
  sensitive is in frame.
- **Site navigation:** the `docs/` folder is published as the Slice's site. Keep
  the front matter from the template so the record appears under Bench Records.
