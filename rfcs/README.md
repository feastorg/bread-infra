# BREADS RFCs

An RFC proposes a change to a BREADS standard before it lands in
[`spec/`](../spec/). It holds the normative text, the reasons for it, and the
tests that have to pass before it is accepted.

| RFC | Title | Status |
| --- | --- | --- |
| [0001](0001-g3/README.md) | G3 slice and backplane standard | Draft |

## Status

- **Draft**: open for review. Nothing in `spec/`, the templates or the boards
  changes yet.
- **Accepted**: the RFC's acceptance tests have passed, or the RFC has been
  changed to match what they measured. Its text then moves into `spec/`, and
  the migration list in the RFC becomes tracked issues.
- **Withdrawn**: not going ahead; the RFC stays for the record.

An RFC is changed by pull request like anything else in this repository.
Review happens on those pull requests and on issues that link the RFC.

## Layout

Each RFC is a directory `NNNN-name/` with a `README.md` that gives its status,
summary and document map. Figures are either Mermaid, inline in the Markdown,
or TikZ and CircuiTikZ sources in `figures/src/`, built to the SVGs in
`figures/` by [`scripts/build_figures.sh`](../scripts/build_figures.sh):

```sh
scripts/build_figures.sh                          # every figure in every RFC
scripts/build_figures.sh rfcs/0001-g3 stop-circuit # one figure
```

It needs a TeX Live with TikZ and CircuiTikZ, and `pdftocairo` from
poppler-utils. Commit the rebuilt SVG with its source.

## Keywords

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be interpreted
as described in BCP 14 ([RFC 2119](https://www.rfc-editor.org/rfc/rfc2119),
[RFC 8174](https://www.rfc-editor.org/rfc/rfc8174)) when, and only when, they
appear in all capitals.
