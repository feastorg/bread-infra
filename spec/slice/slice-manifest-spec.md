# Slice Manifest Field Reference

This document describes every field in `slice.yaml`. Schema 2.0 is first;
the 1.0 reference follows it and holds until each manifest moves to 2.0.

## Schema 2.0

Schema: [`schemas/slice.schema.v2.json`](../../schemas/slice.schema.v2.json)

2.0 keeps what a tool reads or a reader needs, under the same paths as 1.0.
Every other 1.0 field is removed. A field is added back when something reads
it. The validator picks 2.0 for a manifest whose `schema_version` is `2.x`;
CI picks it with `schema_ref: schema-v2.0`.

```yaml
schema_version: "2.0"
id: "slice-dcmt"
name: "DC Motor Controller"
summary: "One line."
category: "actuation"
status: "development"
hardware:
  hw_gen_current: 3
  interface: "SI1"
  pcb:
    layers: 2
    dimensions: "70mm x 100mm"
    thickness: "1.6mm"
  mounting:
    pattern: "slice-S-v0"
  mcu:
    form_factor: "nano"
interfaces:
  host:
    address_default: 18
metadata:
  tags: ["motor"]
```

| Field | Required | Meaning | Read by |
|---|---|---|---|
| `schema_version` | yes | `2.x` | validator, site index |
| `id`, `name`, `summary`, `category` | yes | as in 1.0 | site index |
| `status` | yes | lifecycle of the board in `hardware/`: `concept` (not designed), `development` (designed, not fabricated), `built` (fabricated, under test), `released` (has a `g<N>-r<n>` tag), `retired` | site index |
| `hardware.hw_gen_current` | yes | generation the board is built for, or heading for while in development ([terminology](../terminology.md)) | site index |
| `hardware.interface` | yes | slot interface the board meets: `SI1` ([Slice Interface 1](slice-interface-1.md)) | SI2 migration |
| `hardware.pcb.layers`, `.dimensions`, `.thickness` | yes | as in 1.0 | bread-mechanical (`dimensions`, `thickness`) |
| `hardware.mounting.pattern` | yes | board format: `slice-S-v0` (70 x 100) or `slice-L-v0` (100 x 145), per Slice Interface 1; `null` if the board meets neither | bread-mechanical |
| `hardware.mcu.form_factor` | no | `nano`, `nucleo32` or `pico`; `mcu: null` for none | bread-mechanical (USB port) |
| `interfaces.host.address_default` | no | default 7-bit I2C address, decimal; `null` if set at run time | whoever sets up the bus |
| `metadata.tags` | no | free tags | site index |

The facts 1.0 also held live elsewhere: a revision in its release tag,
license in `LICENSE`, the repository URL and dates in GitHub, and
electrical, firmware, protocol and safety detail in the README, board files
and bench records.

## Schema 1.0 (legacy)

Schema: [`schemas/slice.schema.json`](../../schemas/slice.schema.json)  
Template: [`templates/slice.yaml.template`](../../templates/slice.yaml.template)

---

## Top-Level Required Fields

| Field | Type | Description |
|---|---|---|
| `schema_version` | string (`M.m`) | Schema version this file conforms to |
| `id` | string | Unique ID: `slice-{name}` (lowercased, hyphens) |
| `name` | string | Human-readable display name |
| `status` | enum | `concept` · `prototype` · `validated` · `released` · `deprecated` |
| `category` | enum | `actuation` · `sensing` · `integrated` · `power` · `interface` · `template` · `prototype` |
| `summary` | string | One-line purpose description |
| `description` | string \| null | Extended description |

### `id` Convention

Derived from the repo name: `Slice_DCMT` → `slice-dcmt`. Must match pattern `^slice-[a-z0-9-]+$`.

### `status` Lifecycle

```
concept → prototype → validated → released
                                      ↓
                                 deprecated
```

---

## `version`

| Field | Type | Notes |
|---|---|---|
| `hardware` | semver string | Legacy; not the board's revision, which is its G and r label ([terminology](../terminology.md#generations-revisions-and-interfaces)) |
| `firmware` | semver string \| null | Firmware version; null for hardware-only |
| `manifest` | semver string | Version of this manifest file's content |

---

## `compatibility`

| Field | Type | Notes |
|---|---|---|
| `slice_spec` | semver range | e.g. `>=0.1.0 <0.2.0` |
| `crumbs_protocol` | semver range \| null | CRUMBS library compatibility |
| `anolis_provider_api` | semver range \| null | Forward-signal for Anolis integration |

---

## `hardware`

### `hardware.mcu`

Object or null (for passive boards without MCU).

| Field | Type | Notes |
|---|---|---|
| `type` | enum | `dev-board-socket` (pluggable) or `embedded` (soldered) |
| `form_factor` | enum \| null | `nano` · `nucleo32` · `pico` · null (if embedded) |
| `primary` | string | Default MCU chip name |
| `supported` | string[] | All MCUs firmware supports on this PCB |

### `hardware.primary_ic`

Object or null. The main functional IC on the board (not the MCU).

| Field | Type |
|---|---|
| `manufacturer` | string |
| `part_number` | string |

### `hardware.pcb`

| Field | Type | Notes |
|---|---|---|
| `layers` | integer | Number of copper layers |
| `thickness` | string \| null | e.g. `"1.6mm"` |
| `copper_weight` | string \| null | e.g. `"1oz"` |
| `dimensions` | string | Board dimensions e.g. `"70mm x 100mm"` |

### `hardware.connectors[]`

| Field | Type | Notes |
|---|---|---|
| `ref` | string | Schematic reference designator |
| `type` | string | Connector standard (e.g. `slice-bus-10pin`) |
| `purpose` | string | What it carries (e.g. `power-and-i2c`) |

### `hardware.mounting`

| Field | Type | Notes |
|---|---|---|
| `pattern` | string | Mounting pattern ID |
| `hole_size` | string | Bolt size (e.g. `M3`) |
| `inset` | string | Distance from edge |

### Other Hardware Fields

| Field | Type | Notes |
|---|---|---|
| `hw_gen_current` | integer | Generation (G number) the board in `hardware/` is built for, or heading for while in development; see [terminology](../terminology.md#generations-revisions-and-interfaces) |
| `hw_gen_supported` | integer[] | Generations the firmware supports |
| `pcb_color_prototype` | string \| null | Solder mask color for prototypes |
| `pcb_color_production` | string \| null | Solder mask color for production |
| `enclosure` | object \| null | `{supported: bool, path: string|null}` |

---

## `electrical`

| Field | Type | Notes |
|---|---|---|
| `input_voltage` | string \| null | Nominal input voltage |
| `logic_voltage` | string \| null | Logic level voltage |
| `max_current` | string \| null | Maximum current draw |
| `protection` | object \| null | `{reverse_polarity, input_esd, fuse}` (booleans) |
| `isolation` | object \| null | `{present: bool}` |

---

## `interfaces`

### `interfaces.host` (required)

The primary communication interface exposed through the Loaf to the controller.

| Field | Type | Notes |
|---|---|---|
| `type` | string | Protocol type (e.g. `i2c`) |
| `address_default` | integer \| null | Default bus address (decimal) |
| `address_configurable` | boolean | Whether address can be changed |

### `interfaces.data`

Object or null. Describes physical I/O channels.

| Field | Type |
|---|---|
| `inputs[]` | `{name, type}` |
| `outputs[]` | `{name, type}` |

---

## `capabilities`

Array or null. Each entry describes a functional capability.

| Field | Type | Notes |
|---|---|---|
| `id` | string | Capability identifier |
| `channels` | integer | Number of channels (optional) |
| `control_modes` | string[] | Supported control modes (optional) |

---

## `firmware`

Object or null (null for hardware-only slices).

| Field | Type | Notes |
|---|---|---|
| `required` | boolean | Whether firmware is needed to operate |
| `path` | string | Relative path to firmware directory |
| `language` | string | e.g. `c++` |
| `framework` | string | e.g. `arduino` |
| `targets` | string[] | PlatformIO environment names |
| `lib_deps` | string[] | PlatformIO library dependencies |

---

## `protocol`

Object or null. Describes the communication protocol implementation.

| Field | Type | Notes |
|---|---|---|
| `type` | string | e.g. `crumbs-i2c` |
| `discovery.supported` | boolean | Whether auto-discovery is implemented |
| `commands` | object[] | Command definitions (future expansion) |

---

## `software`

Object or null. Host-side software support.

- `drivers.python` — path or null
- `drivers.arduino` — path or null
- `provider.supported` — boolean
- `provider.path` — path or null

---

## `artifacts`

Paths to key project files (relative to repo root).

| Field | Required | Notes |
|---|---|---|
| `schematic` | yes | KiCad schematic path |
| `pcb` | yes | KiCad PCB path |
| `firmware` | no | Firmware directory |
| `docs` | no | Docs directory |
| `bom` | no | Bill of materials |
| `gerbers` | no | Gerber output directory |
| `pick_and_place` | no | PnP file |
| `datasheets` | no | Array of datasheet paths/URLs |

---

## `manufacturing`, `validation`, `safety`

All nullable objects for tracking production readiness. See schema for full structure.

---

## `dependencies`

Object or null. Lists external dependencies by category:
- `hardware` — other BREADS-compatible hardware required
- `firmware_libraries` — library dependencies
- `software_packages` — host software dependencies

---

## `related`

Object or null. Tracks relationships between slices:
- `supersedes` — ID of slice this replaces
- `superseded_by` — ID of slice that replaces this
- `variants` — IDs of variant slices
- `compatible_slices` — IDs of slices commonly used together

---

## `maintainers`

Array of `{name, role}` objects. At least one entry expected.

---

## `license`

| Field | Required | Notes |
|---|---|---|
| `hardware` | yes | SPDX identifier for hardware (default: `CERN-OHL-S-2.0`) |
| `firmware` | yes | SPDX identifier or null |
| `software` | no | SPDX identifier or null |
| `docs` | yes | SPDX identifier (default: `CC-BY-4.0`) |

---

## `repository`

| Field | Type |
|---|---|
| `url` | URI — GitHub repo URL |

---

## `metadata`

| Field | Type | Notes |
|---|---|---|
| `created` | date string | ISO 8601 date manifest was created |
| `updated` | date string | ISO 8601 date of last manifest update |
| `tags` | string[] | Searchable keywords |
