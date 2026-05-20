# Schema Changelog

All notable changes to `schemas/slice.schema.json`.

Format: [Keep a Changelog](https://keepachangelog.com/)

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
