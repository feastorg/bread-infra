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

To use in other repos, call the workflow like this:

```yaml
name: Docs Pipeline

on:
  push:
    branches: [main]
    paths:
      - "hardware/**"
      - "docs/**"
      - "scripts/**"
      - ".github/workflows/**"
  workflow_dispatch:

jobs:
  kibot:
    uses: feastorg/bread-infra/.github/workflows/kibot-ci.yml@main

  gen-kibot-index:
    uses: feastorg/bread-infra/.github/workflows/publish-kibot.yml@main
    needs: [kibot]
    with:
      kibot_run_id: ${{ needs.kibot.outputs.kibot_run_id }}

  deploy-pages:
    uses: feastorg/bread-infra/.github/workflows/deploy-pages.yml@main
    needs: [gen-kibot-index]
    with:
      kibot_run_id: ${{ needs.kibot.outputs.kibot_run_id }}
      commit_sha: ${{ needs.gen-kibot-index.outputs.kibot_index_sha }}
```
