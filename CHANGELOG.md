# Changelog

Notable changes to bread-infra workflows, scripts, and infrastructure.

Format: [Keep a Changelog](https://keepachangelog.com/)

For schema-specific changes, see [SCHEMA_CHANGELOG.md](SCHEMA_CHANGELOG.md).

---

## 2026-07-12

### Added
- `validate-board.yml` + `scripts/validate_board.py` — fails a board that is not
  aligned with BREADS: KiCad 10 file format, `footprint_symbol_mismatch` severity
  of `error`, all library references resolving against KiCad-Master-Lib, and
  un-swapped Makefile targets.
- `scripts/write_project_lib_tables.py` — generates project-level KiCad library
  tables from KiCad-Master-Lib's committed tables, so CI resolves `KMLib_*` and
  vendored nicknames without any global KiCad config.
- `templates/docs-pipeline.yml` and `templates/hardware.Makefile`.

### Changed
- **KiBot CI now runs KiCad 10**, not KiCad 9, against what are now KiCad 10
  projects. Images are pinned by tag *and* digest instead of `:latest`.
- KiBot CI checks out KiCad-Master-Lib and resolves libraries before running.
  Previously `KMLib_*` did not resolve in the container, producing ~100
  `lib_footprint_issues` warnings per board — noise that concealed real defects.

### Fixed
- `hardware/Makefile` ERC and DRC targets were inverted fleet-wide: KiBot's
  `-s`/`--skip-pre` *skips* the named preflight, so the `erc` target ran DRC and
  vice versa. Both checks still ran, but every violation was reported under the
  wrong job name. Corrected in `templates/hardware.Makefile`.
- `templates/docs-pipeline.yml` adds a `pull_request` trigger. Hardware checks
  previously ran only on `push: main`, i.e. only *after* a bad change had merged.

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
