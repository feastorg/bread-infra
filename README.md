# bread-infra

BREADS definitions, specifications, schemas, templates, and reusable CI
infrastructure for BREADS-compatible hardware repos.

- **`spec/`** — Human-readable specifications and BREADS terminology
- **`schemas/`** — JSON Schemas for manifest validation (machine-readable)
- **`templates/`** — Copy-paste manifest templates for new repos
- **`.github/workflows/`** — Reusable CI workflows (KiBot, docs deployment, manifest validation)
- **`scripts/`** — Build and validation helper scripts

Start with [`spec/terminology.md`](spec/terminology.md) for the active
definitions of BREAD, BREADS, Slices, Loaves, and Grains.

See [Slice_TEMP_NANO_S2L-r2](https://github.com/feastorg/Slice_TEMP_NANO_S2L-r2) for an example of the required auxiliary and template files.

## Usage

This repo contains reusable workflows, specifications, and scripts for
BREADS-compatible hardware repos.
It is not meant to be triggered directly.

To use in other repos, copy [`templates/docs-pipeline.yml`](templates/docs-pipeline.yml)
to `.github/workflows/docs-pipeline.yml`. It wires up board validation, KiBot ERC/DRC,
and the docs site, and it runs on **pull requests** as well as pushes — hardware checks
that only run after merge cannot stop anything from breaking.

Board repos also need [`templates/hardware.Makefile`](templates/hardware.Makefile) at
`hardware/Makefile`.

### Board validation

[`validate-board.yml`](.github/workflows/validate-board.yml) checks that a board is
actually aligned with BREADS, not merely that it opens in KiCad:

| Check | Why |
| --- | --- |
| KiCad 10 file format | A board saved by KiCad 9 opens fine; the version stamp is the only signal. |
| `footprint_symbol_mismatch` severity is `error` | KiCad's **default is `warning`**, and KiBot's DRC preflight only fails on errors — so `schematic_parity: true` runs the check and can never fail it. |
| Every library reference resolves | KiCad embeds footprint geometry in the `.kicad_pcb`, so a board renders and fabricates long after its library reference has rotted. |
| `hardware/Makefile` targets not swapped | KiBot's `-s` **skips** the named preflight, so `drc: kibot -s drc` skips DRC. |

Run it locally:

```sh
python3 scripts/validate_board.py <repo> --master-lib <KiCad-Master-Lib>
```

A green **Validate Board** is the definition of "this board is done".
