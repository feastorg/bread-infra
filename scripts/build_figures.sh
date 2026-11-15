#!/usr/bin/env bash
# Builds every rfcs/*/figures/src/*.tex into rfcs/*/figures/<name>.svg:
# pdflatex, then pdftocairo -svg. Needs a TeX Live with tikz and circuitikz,
# and poppler-utils. Build intermediates go to a temporary directory.
#
#   scripts/build_figures.sh                       build every figure
#   scripts/build_figures.sh rfcs/0001-slice-interface-2 stop-circuit   build one figure
set -euo pipefail
cd "$(dirname "$0")/.."

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

build() { # build <figures dir> <name>
    local dir=$1 name=$2 src=$1/src
    if [ -z "$name" ] || [[ $name == */* ]] || [ ! -f "$src/$name.tex" ]; then
        echo "build_figures: no $src/$name.tex (give a name such as stop-circuit, not a path)" >&2
        exit 1
    fi
    if ! TEXINPUTS="$src:" pdflatex -interaction=nonstopmode -halt-on-error \
        -output-directory "$tmp" "$src/$name.tex" >"$tmp/$name.stdout"; then
        cat "$tmp/$name.stdout" >&2
        echo "build_figures: $name.tex failed" >&2
        exit 1
    fi
    pdftocairo -svg "$tmp/$name.pdf" "$tmp/$name.svg"
    # The SVG's viewBox is the figure in points. pdftocairo versions write
    # the root's width and height differently, so set both to twice the
    # viewBox, in px; a page narrower than the figure scales it down.
    python3 -I - "$tmp/$name.svg" "$dir/$name.svg" <<'EOF'
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
svg = open(src, encoding="utf-8").read()
root = re.search(r"<svg\b[^>]*>", svg)
box = re.search(r'\bviewBox="[-0-9.]+ [-0-9.]+ ([0-9.]+) ([0-9.]+)"', root.group(0))
if box is None:
    sys.exit(f"build_figures: no viewBox in {src}: {root.group(0)}")
size = {"width": float(box.group(1)) * 2, "height": float(box.group(2)) * 2}
new_root, n = re.subn(
    r'\b(width|height)="[^"]*"', lambda m: f'{m.group(1)}="{size[m.group(1)]:g}"', root.group(0)
)
if n != 2:
    sys.exit(f"build_figures: no width and height in {src}: {root.group(0)}")
open(dst, "w", encoding="utf-8").write(svg[: root.start()] + new_root + svg[root.end() :])
EOF
    echo "build_figures: $dir/$name.svg"
}

if [ $# -eq 2 ]; then
    build "$1/figures" "$2"
elif [ $# -eq 0 ]; then
    shopt -s nullglob
    for f in rfcs/*/figures/src/*.tex; do
        build "$(dirname "$(dirname "$f")")" "$(basename "$f" .tex)"
    done
else
    echo "usage: scripts/build_figures.sh [rfcs/<rfc> <figure>]" >&2
    exit 1
fi
