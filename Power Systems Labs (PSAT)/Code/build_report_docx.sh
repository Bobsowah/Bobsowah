#!/usr/bin/env bash
# Build the PSAT Technical Report DOCX from the master .tex.
# Usage: build_report_docx.sh <outdir>
# The master .tex keeps \allowbreak (useful in PDF line breaking); texmath cannot
# parse it, so a pandoc-only copy has it stripped.
set -euo pipefail
OUT="${1:?output dir}"
HERE="$(cd "$(dirname "$0")/.." && pwd)"
REF="$HERE/../Code/pandoc_style/lab_reference.docx"
mkdir -p "$OUT"
python3 "$HERE/Code/prep_report_for_pandoc.py" "$HERE/PSAT Toolbox Extensions - Technical Report.tex" "$HERE/_pandoc_input.tex"
trap 'rm -f "$HERE/_pandoc_input.tex"' EXIT
cd "$HERE"
pandoc _pandoc_input.tex -f latex -t docx --reference-doc="$REF" --toc --number-sections \
  -o "$OUT/PSAT Toolbox Extensions - Technical Report.docx" 2> "$OUT/pandoc.err"
cat "$OUT/pandoc.err"
