#!/usr/bin/env bash
set -euo pipefail

# Requires: texlive-publishers biber texlive-bibtex-extra texlive-science
# Install on Debian/Ubuntu:
#   sudo apt-get install texlive-publishers biber texlive-bibtex-extra texlive-science

root="$(cd "$(dirname "$0")" && pwd)"
cd "$root"

# Avoid stale overrides from earlier local biber/texmf experiments.
unset TEXINPUTS PERL5LIB

cleanup() {
  latexmk -c >/dev/null 2>&1 || true
  rm -f chapters/*.aux
  rm -f main.{bcf,run.xml,fdb_latexmk,fls,bbl,blg}
  rm -rf build
}

trap cleanup EXIT

# -f: keep going through biber and reruns even when refs/cites are not yet resolved.
latexmk -pdf -f -interaction=nonstopmode -file-line-error "$@"

# Fail if the PDF was not produced.
test -f main.pdf
