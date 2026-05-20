# Slice Manifest Field Reference

This document describes every field in `slice.yaml` with its type, constraints, and rationale.

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
| `hardware` | semver string | PCB revision |
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
| `hw_gen_current` | integer | Current HW generation number |
| `hw_gen_supported` | integer[] | All gens firmware supports |
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

The primary communication interface to the LOAF controller.

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
- `hardware` — other BREAD modules required
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
