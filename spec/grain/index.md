# Grain Spec

Grain is a plain class name rather than an acronym.

A **Grain** is designed adjacent hardware that may be used in or alongside a
BREAD, but is not a Slice and not a Loaf. Grains do not carry the full
compatibility obligations of Slices.

For the full terminology reference, see [Terminology](../terminology.md).

## What qualifies as a Grain?

A board is a Grain if:

- it is a designed PCB, not a commercial off-the-shelf part
- it is used alongside BREADS-compatible hardware
- it does not implement the BREADS Slice interface
- it is intended to be produced or reproduced, not purely a development jig

## Categories

| Category | Description | Examples |
|---|---|---|
| `shield` | Plugs onto or wraps a development board | `can-nano-shield` |
| `card` | Plugs into a carrier or host board | `stepper_card` |
| `adapter` | Signal or connector adapter board | - |
| `module` | Self-contained support module that connects externally | - |

## Manifest

Each indexed Grain repo must contain a `grain.yaml` at the repository root.
This file is the machine-readable manifest that enables discovery, validation,
and indexing.

See the [manifest spec](grain-manifest-spec.md) for the full field reference
and the [template](../../templates/grain.yaml.template) to copy into a new repo.

Validate locally:

```sh
python bread-infra/scripts/validate_manifest.py grain.yaml
```

## Discovery

The site index generator (`generate_grain_index.py`) scans `feastorg` repos for
the presence of `grain.yaml` at the repo root. There is no required repo naming
prefix; the manifest signals membership.

## Relationship To Other Hardware

```text
Loaf  = attachment/interconnect layer for a BREAD
Slice = BREADS-compatible capability module
Grain = adjacent support hardware
```
