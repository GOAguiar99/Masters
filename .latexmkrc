# Kept minimal so Overleaf can apply its own output handling.
# Local builds go through ./compile.sh, which passes -outdir=build.
$pdf_mode = 1;
$pdflatex = 'pdflatex -interaction=nonstopmode -file-line-error %O %S';
