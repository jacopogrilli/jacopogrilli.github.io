#!/bin/bash
# Regenerate the data-backed partials from ../_data, then build the CV.
set -e
cd "$(dirname "$0")"

python3 script/generate_cv.py

pdflatex jgrilli_cv.tex
pdflatex jgrilli_cv.tex
pdflatex jgrilli_cv.tex

rm -f *.aux *.log *.blg *.bbl *.toc *.out

# Publish the freshly built CV as the copy the website links to
cp jgrilli_cv.pdf ../images/teamcv/jgrilli_cv.pdf
