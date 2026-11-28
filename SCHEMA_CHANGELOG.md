# Schema Changelog

All notable changes to BREAD manifest schemas.

Format: [Keep a Changelog](https://keepachangelog.com/)

---

## [Unreleased]

---

## schema-v2.0 — 2026-11-27

### Added

- Slice and loaf schema 2.0: `schemas/slice.schema.v2.json` and
  `schemas/loaf.schema.v2.json`. 2.0 keeps the 1.0 fields a tool reads or a
  reader needs, under the same paths, and removes the rest. It adds
  `hardware.interface` (`SI1`), gives `status` the lifecycle values
  `concept · development · built · released · retired`, and limits
  `mounting.pattern` to `slice-S-v0`, `slice-L-v0` or null. Loaf 2.0 has no
  `hw_gen_supported`. 1.0 is unchanged; the validator picks 2.0 when
  `schema_version` is `2.x`.

### Changed

- `hw_gen_current` and `hw_gen_supported` in the slice and loaf schemas are
  defined as the fleet-wide generation (G1, G2, G3…), not a per-board design
  counter. A design in `hardware/` carries the generation it is heading for.
  The types are unchanged; the values in existing manifests are updated
  separately (#24). Definitions in `spec/terminology.md`.

---

## grain-v1.0 — 2026-06-12

Initial GRAIN manifest schema.

### Added

- `schemas/grain.schema.json` — new schema for `grain.yaml` GRAIN manifests
- Required fields: `grain_schema_version`, `id`, `name`, `category`, `status`,
  `summary`, `license.hardware`, `repository.url`
- Optional fields: `version.hardware`, `compatibility`, `related_slices`,
  `hardware.form_factor`, `hardware.pcb_layers`, `firmware.language`,
  `firmware.framework`, `license.firmware`, `license.documentation`,
  `metadata.tags`, `metadata.updated`
- Category enum: `shield | card | adapter | module`
- Status enum: `concept | prototype | released | deprecated`
- Separate from `slice.schema.json` — no shared base (see grain-decisions.md D6)

---

## [1.0] — 2026-05-19

Initial stable schema release.

### Added

- All top-level sections: identity, version, compatibility, hardware, electrical, interfaces, capabilities, firmware, protocol, software, artifacts, manufacturing, validation, safety, dependencies, related, maintainers, license, repository, metadata
- MCU expanded object model (`type`, `form_factor`, `primary`, `supported[]`)
- Bus address exclusively under `interfaces.host` (not duplicated in electrical)
- Category enum aligned with BREADS taxonomy
- Status lifecycle enum
- Nullable pattern for optional/unknown fields
