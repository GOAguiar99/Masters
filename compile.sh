#!/usr/bin/env bash
set -euo pipefail

# Builds the dissertation into build/main.pdf.
#
# Requires: texlive-publishers biber texlive-bibtex-extra texlive-science
# Install on Debian/Ubuntu:
#   sudo apt-get install texlive-publishers biber texlive-bibtex-extra texlive-science
#
# Usage:
#   ./compile.sh          # incremental build into build/
#   ./compile.sh clean    # remove build/ and stray root artifacts

root="$(cd "$(dirname "$0")" && pwd)"
cd "$root"

# Avoid stale overrides from earlier local biber/texmf experiments.
unset TEXINPUTS PERL5LIB

if [[ "${1:-}" == "clean" ]]; then
  rm -rf build
  rm -f chapters/*.aux
  rm -f main.{aux,bcf,run.xml,fdb_latexmk,fls,bbl,blg,log,out,toc,lof,lot,idx,glo,acn,slo}
  exit 0
fi

# pdflatex needs the aux subdirectories to exist for \include'd files.
mkdir -p build/chapters build/beforetext build/aftertext

# -f: keep going through biber and reruns even when refs/cites are not yet resolved.
latexmk -pdf -outdir=build -f -interaction=nonstopmode -file-line-error "$@" main.tex

# Fail if the PDF was not produced.
test -f build/main.pdf
echo "OK: build/main.pdf"
