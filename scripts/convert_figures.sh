#!/usr/bin/env bash
# Convert publication SVGs under Figs/ to PDF for pdflatex.
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
FIGS_DIR=$(cd "$SCRIPT_DIR/../Figs" && pwd)

if ! command -v rsvg-convert >/dev/null 2>&1; then
  echo "Install librsvg2-bin to convert SVG figures (rsvg-convert)." >&2
  exit 1
fi

shopt -s nullglob
for svg in "$FIGS_DIR"/*.svg; do
  out="${svg%.svg}.pdf"
  rsvg-convert -f pdf1.4 -o "$out" "$svg"
  echo "Wrote $out"
done
