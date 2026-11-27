# Terminology

This page defines the active terminology for BREADS-compatible hardware.

## Active Terms

| Term   | Meaning                                                          |
| ------ | ---------------------------------------------------------------- |
| BREAD  | Broadly Reconfigurable and Expandable Automation Device          |
| BREADS | Broadly Reconfigurable and Expandable Automation Device Standard |
| Slice  | Standardized Logic Interface and Capability Element              |
| Loaf   | Local Operations Attachment Frame                                |
| Grain  | Adjacent support hardware; not an acronym                        |

Use the terms as shown here in prose.

## Standard, Specifications, And Support Artifacts

`BREADS` names the overall compatibility standard. Individual documents in
`spec/` are specifications within BREADS. Schemas, templates, workflows, and
scripts are support artifacts that help apply the standard.

In short:

- **BREADS**: the standard
- **specification**: a human-readable document defining part of BREADS
- **schema**: a machine-readable validation artifact
- **template**: a starter file or project pattern
- **workflow/script**: reusable implementation or CI support

## BREAD

**Broadly Reconfigurable and Expandable Automation Device**

A BREAD is a complete automation device assembled from BREADS-compatible parts.
It is the deployable thing someone builds, documents, tests, and uses.

A BREAD can include:

- a Loaf
- one or more Slices
- a controller or supervisor connection
- optional Grains
- external hardware
- power distribution
- firmware, software, and documentation

Use `BREAD` for a physical or deployed device. Do not use `BREAD` when the
intended meaning is the standard.

## BREADS

**Broadly Reconfigurable and Expandable Automation Device Standard**

BREADS defines the compatibility model that makes BREAD implementations
possible: how compatible parts fit together mechanically, electrically, and
logically.

BREADS covers:

- mechanical envelope and mounting conventions
- Slice bus connector and pinout expectations
- power distribution expectations
- communication bus conventions
- manifest structure and validation
- artifact and documentation expectations
- compatibility language between Slices, Loaves, Grains, firmware, and
  controllers

Use `BREADS` for the standard, schemas, specs, compliance language, validation,
and reusable infrastructure.

## Slice

**Standardized Logic Interface and Capability Element**

A Slice is a BREADS-compatible capability module. It adds functionality to a
BREAD, such as sensing, actuation, power, interface, integrated behavior,
template support, or prototyping support.

A Slice generally has:

- a PCB in the Slice mechanical format
- Slice bus connector/pinout compatibility
- local circuitry for its capability
- local MCU or logic when needed
- a `slice.yaml` manifest
- design artifacts and documentation

Use `Slice` for modules that participate in the BREADS Slice interface and
carry a `slice.yaml` manifest.

## Loaf

**Local Operations Attachment Frame**

A Loaf is the attachment and interconnect layer that lets multiple Slices
operate together as one BREAD.

A Loaf can provide:

- physical attachment for Slices
- backplane, carrier, chassis, or wiring structure
- shared power distribution
- communication paths between Slices and the controller
- controller interface circuitry, headers, or cabling
- enclosure, mounting, service, or safety interfaces

The controller may be an SBC, MCU, PC, or another compute element that can
speak the required BREADS communication interface and has sufficient resources
to operate the BREAD. The controller may be integrated into the Loaf or
connected through it, but a controller alone is not a Loaf unless it also
provides the Loaf attachment/interconnect role.

## Controller / Supervisor

A controller is the compute element that issues commands, reads data, and runs
local device logic.

A supervisor is higher-level orchestration software or compute that coordinates
devices, logs data, exposes a user interface, or manages broader workflows.

The controller or supervisor is not the whole BREAD and is not automatically
the whole Loaf.

## Grain

Grain is a plain class name rather than an acronym.

A Grain is designed adjacent hardware that may be used in or alongside a BREAD,
but is not a Slice and not a Loaf. Grains do not carry the compatibility
obligations of Slices.

Examples include:

- shields
- cards
- adapters
- support modules

Use `Grain` for reusable adjacent hardware that should be indexed and validated
with `grain.yaml`.

## Generations, Revisions And Interfaces

Three labels describe a board. Each answers one question, and none stands in
for another.

| Label | Answers | Form | Recorded in |
| --- | --- | --- | --- |
| Generation | which release of BREADS hardware the board was built for | G1, G2, G3… | `hw_gen_current` in the manifest, the release tag, the silkscreen |
| Revision | which respin of the board within its generation | r1, r2…, from r1 | the release tag, the silkscreen |
| Interface | what the board must do to plug into a Loaf | Slice Interface 1, 2… | the bus connector's `type` in the manifest (`slice-bus-10pin` is Slice Interface 1) |

The generations so far:

| Generation | Boards | Interface |
| --- | --- | --- |
| G1 | the original OSF project's boards, 2021–2023 ("BREAD v1" in the papers) | [Slice Interface 1](slice/slice-interface-1.md) |
| G2 | the 2024 boards ("BREAD v2" in the papers) | Slice Interface 1 |
| G3 | the next release: the designs in each repo's `hardware/`, not yet built | Slice Interface 1 |
| G4 | the first boards built to Slice Interface 2 | Slice Interface 2, proposed in RFC 0001 |

- A generation is a release of BREADS hardware: the boards built for it. A
  design in `hardware/` carries the generation it is heading for and is in
  development until it is built and released. A design moved to a newer
  KiCad without being redesigned and released keeps its generation.
- Generation numbers are fleet-wide whole numbers. A Slice whose first design
  is in today's `hardware/` is G3; it has no G1 or G2 board. There is no G2.5.
- A revision counts respins within one generation, starting at r1. A board is
  named by both: "DCMT G3 r1". Its silkscreen reads, for example,
  "SLC_DCMT G3 r1 2026". Older silkscreen labels such as "R0 2021" or
  "rev.A" are quoted as they are, not renamed. The `-r1`/`-r2` suffix on the
  template repo names predates this scheme.
- A hardware release is a git tag on the board's repo, such as `g3-r1`, with
  the fabrication outputs attached to a GitHub release built from that tag.
  Earlier built designs stay on `main` under `archive/hw_archive/` and are
  tagged the same way. No board has a release tag yet.
- A new generation can keep its interface. A board built to a new interface
  starts a new generation.
- "BREAD v1" and "BREAD v2", as the papers say, are other names for G1 and
  G2. Manifests, tags and silkscreen use the G number.
- Say "a G3 board", "DCMT G3 r1", "a Slice Interface 2 Loaf". Do not use a
  generation to name an interface, or an interface to name a generation.

## Usage Notes

- Say `BREAD`, not `BREADS device`.
- Say `BREADS-compatible`, not `BREAD-compatible`, when referring to standard
  compliance.
- Avoid using `BREAD ecosystem` when a narrower term is available.
- Avoid using `Loaf` for the complete device; that meaning belongs to `BREAD`.
