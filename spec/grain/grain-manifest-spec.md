# grain.yaml — Manifest Spec

The `grain.yaml` file at the root of a GRAIN repo is the machine-readable
manifest that enables discovery, validation, and indexing on the FEAST site.

Validate with:

```sh
python bread-infra/scripts/validate_manifest.py grain.yaml
```

Schema: [`schemas/grain.schema.json`](../../schemas/grain.schema.json) (JSON Schema Draft 2020-12)  
Template: [`templates/grain.yaml.template`](../../templates/grain.yaml.template)

---

## Required fields

| Field | Type | Description |
|---|---|---|
| `grain_schema_version` | string | Schema version. Must be `"1.0"`. |
| `id` | string | Repo name slug — lowercase, underscores → hyphens (e.g. `can-nano-shield`) |
| `name` | string | Human display name |
| `category` | enum | `shield` \| `card` \| `adapter` \| `module` |
| `status` | enum | `concept` \| `prototype` \| `released` \| `deprecated` |
| `summary` | string | One-line description (≤ 120 chars) |
| `license.hardware` | string | SPDX expression (e.g. `CERN-OHL-S-2.0`) |
| `repository.url` | string | HTTPS URL of the GitHub repo |

## Optional fields

| Field | Type | Description |
|---|---|---|
| `version.hardware` | string \| null | Hardware version string |
| `compatibility` | list[string] \| null | What this grain connects to or is designed for |
| `related_slices` | list[string] \| null | Slice repo names this grain works with (e.g. `Slice_STPC`) |
| `hardware.form_factor` | string \| null | Physical form descriptor (e.g. `arduino-nano-shield`, `pcie-edge`) |
| `hardware.pcb_layers` | integer \| null | Number of copper layers |
| `firmware.language` | string \| null | Firmware language (e.g. `C++`) — omit section if no firmware |
| `firmware.framework` | string \| null | Firmware framework (e.g. `arduino`, `platformio`) |
| `license.firmware` | string \| null | SPDX expression for firmware license |
| `license.documentation` | string \| null | SPDX expression for documentation license |
| `metadata.tags` | list[string] \| null | Searchable tags |
| `metadata.updated` | string \| null | ISO 8601 date of last manifest update (e.g. `2026-06-12`) |

## Fields intentionally absent (vs slice.yaml)

The following fields from the Slice manifest are not present in grain.yaml
because grains do not participate in the BREAD bus:

- `interfaces.host` — no I2C address or bus role
- `capabilities` — no ADPP capability model
- `protocol` — no CRUMBS/ADPP
- `electrical.power_consumption` — grains don't sit on the BREAD bus power rail
- `hw_gen_current` / `hw_gen_supported` — generation model is Slice-specific
- `compatibility.slice_spec` / `crumbs_protocol` / `anolis_provider_api`

---

## Example

```yaml
grain_schema_version: "1.0"

id: "can-nano-shield"
name: "CAN Nano Shield"
status: "released"
category: "shield"
summary: "Arduino Nano-form-factor CAN bus shield for the FEAST ecosystem."

version:
  hardware: "1.0.0"

license:
  hardware: "CERN-OHL-S-2.0"
  firmware: "MIT"
  documentation: "CC-BY-SA-4.0"

repository:
  url: "https://github.com/feastorg/can-nano-shield"

compatibility:
  - "Arduino Nano"
  - "Arduino Nano Every"

related_slices: null

hardware:
  form_factor: "arduino-nano-shield"
  pcb_layers: 2

firmware:
  language: "C++"
  framework: "arduino"

metadata:
  tags: ["can", "shield", "nano"]
  updated: "2026-06-12"
```
