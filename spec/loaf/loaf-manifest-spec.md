# Loaf Manifest Field Reference

Every field in `loaf.yaml`, with its type, constraints, and rationale.

Schema: [`schemas/loaf.schema.json`](../../schemas/loaf.schema.json)
Template: [`templates/loaf.yaml.template`](../../templates/loaf.yaml.template)

A Loaf is the attachment and interconnect layer that lets Slices operate together as one
BREAD. See [Loaf](index.md) for the concept.

---

## Top-Level Required Fields

| Field | Type | Description |
| --- | --- | --- |
| `schema_version` | string (`M.m`) | Schema version this file conforms to |
| `id` | string | Unique ID: `loaf-{name}`, pattern `^loaf-[a-z0-9-]+$` |
| `name` | string | Human-readable display name |
| `status` | enum | `concept` · `prototype` · `validated` · `released` · `deprecated` |
| `role` | enum | `backplane` · `controller` · `hybrid` |
| `summary` | string | One-line purpose |
| `version` | object | `hardware`, `firmware` (nullable), `manifest` |
| `compatibility` | object | `loaf_spec`, `slice_spec`, `crumbs_protocol` |
| `hardware` | object | Physical description |
| `electrical` | object | Power in, rails out |
| `interconnect` | object | Slice attachment and bus |
| `artifacts` | object | Paths to schematic, PCB, docs |
| `license` | object | Per-domain licences |
| `repository` | object | Repo URL |
| `metadata` | object | `created`, `updated`, `tags` |

`id` is derived from the repo name: `Loaf_x004` → `loaf-x004`.

---

## `role`

The field that distinguishes the two kinds of Loaf.

| Value | Meaning |
| --- | --- |
| `backplane` | Provides Slice attachment. `interconnect.slice_slots` > 0. |
| `controller` | Provides the controller interface and chains onto a backplane. **No Slice slots of its own** — `interconnect.slice_slots` is `0`. |
| `hybrid` | Both: hosts a controller *and* provides Slice slots. |

A controller alone is not a Loaf. It qualifies only because it also provides the
attachment/interconnect role — in the `controller` case, by chaining onto a backplane and
carrying the bus.

Worked examples:

- `Loaf_x004` — `backplane`, 4 slots, no controller, barrel-jack power in.
- `Loaf_ESPT` — `controller`, **0 slots**, hosts an ESP32 Thing Plus, chains onto x004.

---

## `interconnect`

**This is what makes a board a Loaf** rather than a carrier or a power board. Required.

| Field | Type | Description |
| --- | --- | --- |
| `slice_slots` | integer ≥ 0 | Slice attachment positions. `0` for a controller Loaf. |
| `bus.type` | string | e.g. `i2c` |
| `bus.connector` | string | e.g. `slice-bus-10pin` |
| `bus.signals` | string[] | Signals carried, e.g. `+12V`, `GND`, `SDA`, `SCL`, `E_STOP` |
| `chaining.supported` | boolean | Whether this Loaf connects to another Loaf |
| `chaining.connector` | string \| null | e.g. `1x10-2.54mm` |

`slice_slots: 0` with `chaining.supported: true` is the controller-Loaf shape: it carries
the bus but does not terminate it in a Slice.

---

## `hardware`

| Field | Type | Description |
| --- | --- | --- |
| `controller` | object \| null | `null` for a passive backplane |
| `controller.type` | string | `dev-board-socket` · `embedded` · `external` |
| `controller.form_factor` | string \| null | e.g. `thing-plus` |
| `primary_ic` | object \| null | Manufacturer and part number of the defining IC |
| `hw_gen_current` | integer | Current hardware generation |
| `hw_gen_supported` | integer[] | Generations this board interoperates with |
| `pcb.layers` | integer | Copper layers. Must match the board; the KiBot config is chosen from it. |
| `pcb.dimensions` | string | e.g. `180mm x 162mm` |
| `connectors` | object[] | `ref`, `type`, `purpose` |
| `mounting` | object | `pattern`, `hole_size`, `inset` |
| `enclosure` | object \| null | `supported`, `path` |

---

## `electrical`

| Field | Type | Description |
| --- | --- | --- |
| `input_voltage` | string | Required |
| `logic_voltage` | string \| null | |
| `rails` | object[] | Rails the Loaf distributes: `name`, `voltage`, `max_current`, `source` |
| `protection` | object | `reverse_polarity`, `input_esd`, `fuse` |

`rails` is the Loaf's distinguishing electrical duty: a Slice consumes power, a Loaf
distributes it. Record where each rail comes from (`source`), because that is what fails.

---

## Remaining sections

`firmware`, `artifacts`, `manufacturing`, `validation`, `safety`, `related`, `maintainers`,
`license`, `repository`, `metadata` mirror
[`slice-manifest-spec.md`](../slice/slice-manifest-spec.md), except:

- `firmware` is nullable — a passive backplane has none.
- `related.compatible_loaves` records which Loaves chain together.

---

## Validation

```sh
python3 scripts/validate_manifest.py loaf.yaml
```

The schema is auto-detected from the filename. CI runs this via
[`validate-manifest.yml`](../../.github/workflows/validate-manifest.yml).
