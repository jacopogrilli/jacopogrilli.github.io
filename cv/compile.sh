#!/bin/bash
# Regenerate the data-backed partials from ../_data, then build the CV.
set -e
cd "$(dirname "$0")"

python3 script/generate_cv.py

pdflatex jgrilli_cv.tex
pdflatex jgrilli_cv.tex
pdflatex jgrilli_cv.tex

rm -f *.aux *.log *.blg *.bbl *.toc *.out
