# Changelog

Notable changes to bread-infra workflows, scripts, and infrastructure.

Format: [Keep a Changelog](https://keepachangelog.com/)

For schema-specific changes, see [SCHEMA_CHANGELOG.md](SCHEMA_CHANGELOG.md).

---

## v1.0.0 — 2026-07-12

First tagged release of the workflows and scripts. Board repos should pin this
tag rather than `@main`: an unpinned reusable workflow means a bread-infra commit
can silently change what every board's CI is gated on, which is the same class of
drift this repo exists to eliminate.

### Added
- `scripts/upgrade_kicad10.sh` — migrate a board's KiCad files to the KiCad 10
  format via `kicad-cli sch upgrade` / `pcb upgrade`. Note `sch upgrade` does
  NOT cascade into hierarchical sub-sheets, so upgrading only the root sheet
  leaves sub-sheets on the old format — a board that looks migrated and is not.
  This upgrades every sheet. Verified lossless on Slice_RLAY (identical netlist,
  footprint positions and routing) and idempotent on already-migrated boards.
- `templates/gitignore` — board `.gitignore`, including `.history/` and
  `*.kicad_prl`. KiCad rewrites `.kicad_prl` on every project open (open sheet,
  zoom, selection filter), so tracking it dirties the working tree constantly.
  It is per-developer local state, not design intent. Already-tracked files need
  `git rm --cached hardware/*.kicad_prl`. KiCad 10's
  Local History creates `<project>/.history` and runs `git_repository_init()` on
  it, so it is a nested git repository. The `.gitignore` KiCad writes inside it
  governs KiCad's own history repo, not the board repo — which still reports the
  directory untracked. Committing it would add a broken gitlink. No board
  `.gitignore` in the fleet covered this; all 42 will hit it on KiCad 10.
- `validate-board.yml` + `scripts/validate_board.py` — fails a board that is not
  aligned with BREADS: KiCad 10 file format, `footprint_symbol_mismatch` severity
  of `error`, all library references resolving against KiCad-Master-Lib,
  un-swapped Makefile targets, and `.history/` gitignored.
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
