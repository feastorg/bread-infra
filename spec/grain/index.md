# GRAIN Spec

A **GRAIN** is a FEAST-adjacent PCB hardware module that is not a Slice and
not a Loaf. Grains complement the BREAD ecosystem without conforming to the
Slice bus topology.

## What qualifies as a GRAIN?

A board is a GRAIN if:

- It is a designed PCB (not a commercial off-the-shelf part)
- It is used alongside FEAST hardware (as a shield, carrier, adapter, or
  driver card)
- It does not implement the BREAD Slice bus (no CRUMBS protocol, no ADPP)
- It is intended to be produced or reproduced (not purely a development jig)

## Categories

| Category | Description | Examples |
|---|---|---|
| `shield` | Plugs onto or wraps a dev board; Arduino Nano form factor or similar | `can-nano-shield` |
| `card` | Edge-connector card; plugs into a carrier Slice | `stepper_card` |
| `adapter` | Signal or connector adapter board | — |
| `module` | Self-contained module that connects externally | — |

## Manifest

Each GRAIN repo must contain a `grain.yaml` at the repository root.
This file is the machine-readable manifest that enables discovery, validation,
and indexing.

See the [manifest spec](grain-manifest-spec.md) for the full field reference
and the [template](../../templates/grain.yaml.template) to copy into a new repo.

Validate locally:

```sh
python bread-infra/scripts/validate_manifest.py grain.yaml
```

## Discovery

The site index generator (`generate_grain_index.py`) scans all `feastorg` repos
for the presence of `grain.yaml` at the repo root. There is no required repo
naming prefix — the manifest signals membership.

## Relationship to other BREAD hardware classes

```
Loaf    — full BREAD host controller (runs the bus)
Slice   — BREAD bus module (CRUMBS protocol, ADPP capability model)
GRAIN   — ecosystem-adjacent hardware (no bus, complements Slices/Loaves)
```
