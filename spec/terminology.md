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

| Label | Answers | Form | Where it is recorded |
| --- | --- | --- | --- |
| Generation | which release of BREADS-compatible hardware the board is built for | G1, G2, G3… | the manifest's `hw_gen_current`; on a released board, its release tag and silkscreen |
| Revision | which respin of the board within its generation | r1, r2…, from r1 | on a released board, its release tag and silkscreen |
| Interface | the slot a Slice plugs into and a Loaf provides | Slice Interface 1, 2… | today only by the manifest's bus connector type (`slice-bus-10pin` is Slice Interface 1) |

The generations so far:

| Generation | Boards | Interface |
| --- | --- | --- |
| G1 | the boards built for BREAD v1, 2021–2023 | [Slice Interface 1](slice/slice-interface-1.md) |
| G2 | the boards built for BREAD v2, 2024 | Slice Interface 1 |
| G3 | the next release, not built yet; most repos' `hardware/` designs are heading for it | Slice Interface 1 |
| G4 (proposed) | the first boards built to Slice Interface 2, proposed in RFC 0001 | Slice Interface 2 |

- A generation is a release of BREADS-compatible hardware: the boards built
  for it. A design in `hardware/` carries the generation it is heading for
  and is in development until it is built and released. A design changed
  only by moving it to a newer KiCad, with no change to its circuit or
  copper, keeps the generation it was built for. So does a board that is not
  carried into the next release.
- Generation numbers are fleet-wide whole numbers. A Slice whose first design
  is in today's `hardware/` is heading for G3; it has no G1 or G2 board.
- A revision counts respins within one generation, starting at r1. A board
  is named by both: "DCMT G3 r1". A G3 board's silkscreen reads, for example,
  "BREAD Slice / DC Motor Controller / SLC_DCMT / G3 r1 11-2026".
- Earlier labels are quoted as they are, not renamed: silkscreen such as
  "R0 2021" or "rev.A", the `-r1`/`-r2` suffix the template repo names had until 2026-11,
  and the manifest's `version.hardware`. None of them is a revision in this
  scheme. Each built historical board is mapped to its generation and
  revision once, in a table (DCMT "R0 2021" is G1 r1).
- A hardware release is a git tag on the board's repo, one per fabricated
  revision, such as `g3-r1`, with the fabrication outputs attached to a
  GitHub release built from that tag. A generation's release is a list in
  bread-infra of the board tags that make it up. Loaf_x008 (`g1-r1`) and
  Ctrl_ESPT (`g2-r1`) have release tags; no G3 board has one yet.
- Built earlier designs are kept under `archive/hw_archive/` and tagged as
  well. Today only Slice_DCMT and Slice_RLHT keep designs there. Loaf_x008
  holds LOAF_X08's OSF history; the other G1 designs are on OSF
  ([CITATION.md](../CITATION.md)).
- A new generation can keep its interface: G1 to G3 all use Slice
  Interface 1. Slice Interface 2 is proposed to start at G4.
- "BREAD v1" and "BREAD v2" are the papers' names for G1 and G2 (Hafting et
  al., *Technologies* 2025, Table 2). Manifests, tags and silkscreen use the
  G number.
- Say "a G3 board", "DCMT G3 r1", "a Slice Interface 2 Loaf". Do not use a
  generation to name an interface, or an interface to name a generation.

## Usage Notes

- Say `BREAD`, not `BREADS device`.
- Say `BREADS-compatible`, not `BREAD-compatible`, when referring to standard
  compliance.
- Avoid using `BREAD ecosystem` when a narrower term is available.
- Avoid using `Loaf` for the complete device; that meaning belongs to `BREAD`.
