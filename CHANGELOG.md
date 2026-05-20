# Changelog

Notable changes to bread-infra workflows, scripts, and infrastructure.

Format: [Keep a Changelog](https://keepachangelog.com/)

For schema-specific changes, see [SCHEMA_CHANGELOG.md](SCHEMA_CHANGELOG.md).

---

## 2026-05-19

### Added

- `spec/slice/` — Slice specification documents migrated from BREADS repo
- `spec/loaf/index.md` — Loaf spec stub
- `LICENSES/LICENSE_HW` and `LICENSES/LICENSE_SW` — canonical license files
- `scripts/validate_manifest.py` — local manifest validation tool
- `templates/slice.yaml.template` — copy-paste manifest starting point
- `.gitignore` and `.gitattributes` for cross-platform consistency

### Removed

- `LICENSE` (MIT) — superseded by dual-license model in `LICENSES/`

### Changed

- `README.md` — updated to describe expanded role (spec + infra)
