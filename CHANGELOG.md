# Changelog

Notable changes to bread-infra workflows, scripts, and infrastructure.

Format: [Keep a Changelog](https://keepachangelog.com/)

For schema-specific changes, see [SCHEMA_CHANGELOG.md](SCHEMA_CHANGELOG.md).

---

## 2026-06-12

### Added

- `schemas/grain.schema.json` — GRAIN manifest schema v1.0 (JSON Schema Draft 2020-12)
- `templates/grain.yaml.template` — copy-paste manifest starting point for GRAIN repos
- `spec/grain/index.md` — GRAIN hardware class spec
- `spec/grain/grain-manifest-spec.md` — field-by-field grain.yaml reference
- `TODO.md` — tracked open questions (GRAIN acronym, CRUST class definition)

### Changed

- `scripts/validate_manifest.py` — now auto-detects schema from manifest filename
  (`grain.yaml` → `grain.schema.json`, `slice.yaml` → `slice.schema.json`); `--schema`
  flag still overrides. Updated description strings.
- `.github/workflows/validate-manifest.yml` — removed hardcoded `--schema` flag
  (auto-detect in script handles it); updated `manifest_path` description to
  reflect support for both manifest types.

### Renamed

- `spec/crust/` → `spec/grain/` (directory was empty; GRAIN is the adopted name)

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
