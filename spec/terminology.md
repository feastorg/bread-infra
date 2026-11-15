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
| Generation | which round of BREADS hardware the board belongs to | G1, G2, G3… | `hw_gen_current` in the manifest; `hw_gen_supported` lists the generations the firmware supports |
| Revision | which respin of the board within its generation | r1, r2… | the board's title block and release tag; a template repo's name suffix (`-r2`) |
| Interface | what the board must do to plug into a Loaf | Slice Interface 1, 2… | the bus connector's `type` in the manifest (`slice-bus-10pin` is Slice Interface 1) |

The generations so far:

| Generation | Boards | Interface |
| --- | --- | --- |
| G1 | 2021–2023 boards from the original OSF project | Slice Interface 1 |
| G2 | 2024 boards | Slice Interface 1 |
| G3 | the current designs in each repo's `hardware/` | Slice Interface 1 |
| G4 | the first boards built to Slice Interface 2 | Slice Interface 2, proposed in [RFC 0001](../rfcs/0001-slice-interface-2/README.md) |

- A generation number is fleet-wide. A Slice whose first design is in today's
  `hardware/` is G3, not G1; it simply has no G1 or G2 board.
- Generations are whole numbers. `hw_gen` is an integer, so there is no G2.5.
- A new generation can keep its interface. Boards built to a new interface
  start a new generation.
- An interface is versioned on its own: a change that keeps every board on it
  working is a minor version (Slice Interface 2.1); a change that breaks one,
  such as a pin-map change, is the next interface.
- Say "a G3 board", "DCMT G3 r2", "a Slice Interface 2 Loaf". Do not use a
  generation to name an interface, or an interface to name a board generation.

## Usage Notes

- Say `BREAD`, not `BREADS device`.
- Say `BREADS-compatible`, not `BREAD-compatible`, when referring to standard
  compliance.
- Avoid using `BREAD ecosystem` when a narrower term is available.
- Avoid using `Loaf` for the complete device; that meaning belongs to `BREAD`.
