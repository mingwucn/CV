#!/bin/bash

# This script translates the provided Windows batch file into a Linux shell script.
# It ensures that the script exits immediately if a command fails, enhancing robustness.
set -e

# Run HilightAuthor.py
echo "Running HilightAuthor.py..."
python HilightAuthor.py || { 
    echo "Failed to run HilightAuthor.py" >&2
    exit 1
}

echo "=== Compiling resume-zh_CN.tex with XeLaTeX ==="

# Step 1: First XeLaTeX run
# This run is permitted to fail (e.g., due to missing citations), so a warning is issued instead of exiting.
echo "Step 1: First XeLaTeX run..."
xelatex -interaction=nonstopmode resume-zh_CN.tex || echo "[WARNING] First XeLaTeX run finished with errors, but proceeding as it may be due to missing citations..."

# Step 2: Check for Biber requirement and run if necessary
echo "Checking for Biber requirement..."
if [ -f resume-zh_CN.bcf ]; then
    echo "Step 2: Running Biber..."
    biber resume-zh_CN || {
        echo "Biber processing failed" >&2
        exit 1
    }
else
    echo "No BCF file found. Skipping Biber."
fi

# Step 3: Second XeLaTeX run
echo "Step 3: Second XeLaTeX run..."
xelatex -interaction=nonstopmode -halt-on-error resume-zh_CN.tex || {
    echo "Second XeLaTeX run failed" >&2
    exit 1
}

# Step 4: Third XeLaTeX run
echo "Step 4: Third XeLaTeX run..."
xelatex -interaction=nonstopmode -halt-on-error resume-zh_CN.tex || {
    echo "Third XeLaTeX run failed" >&2
    exit 1
}

# Clean up intermediate files for resume-zh_CN
echo "Cleaning intermediate files for resume-zh_CN..."
rm -f resume-zh_CN.aux resume-zh_CN.log resume-zh_CN.out resume-zh_CN.toc \
      resume-zh_CN.lof resume-zh_CN.lot resume-zh_CN.bbl resume-zh_CN.blg \
      resume-zh_CN.synctex.gz resume-zh_CN.fls resume-zh_CN.fdb_latexmk \
      resume-zh_CN.bcf resume-zh_CN.run.xml

echo "=== resume-zh_CN compilation successful! ==="

# Compile CV_achieve_CN.tex with pdflatex
echo "Compiling CV_achieve_CN.tex with pdflatex..."
pdflatex -interaction=nonstopmode -halt-on-error "CV_achieve_CN.tex" || {
    echo "pdfLaTeX compilation failed for CV_achieve_CN.tex" >&2
    exit 1
}

# Clean up remaining intermediate files
echo "Cleaning all remaining intermediate files..."
rm -f *.aux *.log *.out *.toc *.lof *.lot *.bbl *.blg *.synctex.gz *.fls *.fdb_latexmk

echo "All operations completed successfully."