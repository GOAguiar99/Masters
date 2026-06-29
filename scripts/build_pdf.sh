#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PROJECT_DIR=$(cd "$SCRIPT_DIR/.." && pwd)

MAIN_TEX=${1:-text.tex}

cd "$PROJECT_DIR"

mkdir -p build

latexmk \
  -pdf \
  -interaction=nonstopmode \
  -file-line-error \
  -auxdir=build \
  -outdir=build \
  "$MAIN_TEX"
