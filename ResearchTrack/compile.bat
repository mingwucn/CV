@echo off
:: ==================================================================
::           LaTeX Compilation Script for Windows Batch
:: ==================================================================
:: This script automates a multi-step LaTeX compilation process.
:: It was converted from a Linux shell command sequence.

TITLE Compiling LaTeX Project...

:: --- Initial Setup ---
ECHO [INFO] Navigating to parent directory to run helper script...
cd ..
python HilightAuthor.py

ECHO [INFO] Entering the main project directory...
cd ResearchTrack

:: --- Part 1: Compile 'raw_contribution.tex' and Generate SVG ---

ECHO [INFO] Cleaning up previous 'raw_contribution' build files...
del /F /Q raw_contribution*.svg
del /F /Q *.aux *.log *.gz *.out *.bbl *.lof *.lot *.blg *.upa *.upb

ECHO [INFO] Starting pdflatex->biber->pdflatex->pdflatex cycle for raw_contribution.tex...
pdflatex --shell-escape -interaction=nonstopmode -synctex=1 raw_contribution.tex
biber raw_contribution
pdflatex --shell-escape -interaction=nonstopmode -synctex=1 raw_contribution.tex
pdflatex --shell-escape -interaction=nonstopmode -synctex=1 raw_contribution.tex

ECHO [INFO] Cleaning up intermediate files from 'raw_contribution' build...
del /F /Q *.aux *.log *.gz *.out *.bbl *.lof *.lot *.blg *.upa *.upb raw_contribution.spl raw_contribution.abs raw_contribution.run.xml raw_contribution.bcf raw_contribution-blx.bib

ECHO [INFO] Regenerating SVG files from raw_contribution.pdf...
del /F /Q raw_contribution*.svg
:: Note the use of %% to escape the % character in the --output parameter.
dvisvgm --pdf --no-fonts --bbox=min raw_contribution.pdf -p 1,2,3 --output="%%f-%%p"

:: --- Part 2: Compile the Main 'ResearchTrack.tex' Document ---

ECHO [INFO] Cleaning up previous 'ResearchTrack' build files...
del /F /Q *.aux *.log *.gz *.out *.bbl *.lof *.lot *.blg *.upa *.upb

ECHO [INFO] Starting pdflatex->biber->pdflatex->pdflatex cycle for ResearchTrack.tex...
pdflatex --shell-escape -interaction=nonstopmode -synctex=1 ResearchTrack.tex
biber ResearchTrack
pdflatex --shell-escape -interaction=nonstopmode -synctex=1 ResearchTrack.tex
pdflatex --shell-escape -interaction=nonstopmode -synctex=1 ResearchTrack.tex

ECHO [INFO] Performing final cleanup of all intermediate files...
del /F /Q *.aux *.log *.gz *.out *.bbl *.lof *.lot *.blg *.upa *.upb ResearchTrack.spl ResearchTrack.abs ResearchTrack.run.xml ResearchTrack.bcf ResearchTrack-blx.bib

ECHO [SUCCESS] Build process completed.