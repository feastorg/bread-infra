# Schema Changelog

All notable changes to BREAD manifest schemas.

Format: [Keep a Changelog](https://keepachangelog.com/)

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
