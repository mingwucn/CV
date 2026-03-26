@echo off
setlocal enabledelayedexpansion

:: Run HilightAuthor.py
echo Running HilightAuthor.py...
python HilightAuthor.py || (
    echo Failed to run HilightAuthor.py && exit /b 1
)

echo "=== Compiling resume.tex with XeLaTeX ==="

echo Step 1: First XeLaTeX run...
xelatex -interaction=nonstopmode resume.tex
if %errorlevel% neq 0 (
  echo [WARNING] First XeLaTeX run finished with errors, but proceeding as it may be due to missing citations...
)

echo Checking for Biber requirement...
if exist resume.bcf (
  echo Step 2: Running Biber...
  biber resume
  if %errorlevel% neq 0 (
    echo Biber processing failed && exit /b 1
  )
) else (
  echo No BCF file found. Skipping Biber.
)

echo Step 3: Second XeLaTeX run...
xelatex -interaction=nonstopmode -halt-on-error resume.tex || (
  echo Second XeLaTeX run failed && exit /b 1
)

echo Step 4: Third XeLaTeX run...
xelatex -interaction=nonstopmode -halt-on-error resume.tex || (
  echo Third XeLaTeX run failed && exit /b 1
)

:: Clean up intermediate files
echo Cleaning intermediate files...
del /Q resume.aux resume.log resume.out resume.toc 2>nul
del /Q resume.lof resume.lot resume.bbl resume.blg 2>nul
del /Q resume.synctex.gz resume.fls resume.fdb_latexmk resume.bcf resume.run.xml 2>nul

echo "=== Compiling resume-zh_CN.tex with XeLaTeX ==="

echo Step 1: First XeLaTeX run...
xelatex -interaction=nonstopmode resume-zh_CN.tex
if %errorlevel% neq 0 (
  echo [WARNING] First XeLaTeX run finished with errors, but proceeding as it may be due to missing citations...
)

echo Checking for Biber requirement...
if exist resume-zh_CN.bcf (
  echo Step 2: Running Biber...
  biber resume-zh_CN
  if %errorlevel% neq 0 (
    echo Biber processing failed && exit /b 1
  )
) else (
  echo No BCF file found. Skipping Biber.
)

echo Step 3: Second XeLaTeX run...
xelatex -interaction=nonstopmode -halt-on-error resume-zh_CN.tex || (
  echo Second XeLaTeX run failed && exit /b 1
)

echo Step 4: Third XeLaTeX run...
xelatex -interaction=nonstopmode -halt-on-error resume-zh_CN.tex || (
  echo Third XeLaTeX run failed && exit /b 1
)

:: Clean up intermediate files
echo Cleaning intermediate files...
del /Q resume-zh_CN.aux resume-zh_CN.log resume-zh_CN.out resume-zh_CN.toc 2>nul
del /Q resume-zh_CN.lof resume-zh_CN.lot resume-zh_CN.bbl resume-zh_CN.blg 2>nul
del /Q resume-zh_CN.synctex.gz resume-zh_CN.fls resume-zh_CN.fdb_latexmk resume-zh_CN.bcf resume-zh_CN.run.xml 2>nul


echo "=== resume-zh_CN compilation successful! ==="

:: Compile CV_个人业绩.tex with pdflatex
echo Compiling CV_achieve_CN.tex with pdflatex...
pdflatex -interaction=nonstopmode -halt-on-error "CV_achieve_CN.tex" || (
    echo pdfLaTeX compilation failed for CV_achieve_CN.tex && exit /b 1
)

:: Clean up intermediate files
echo Cleaning intermediate files...
del /Q *.aux *.log *.out *.toc *.lof *.lot *.bbl *.blg *.synctex.gz *.fls *.fdb_latexmk 2>nul

echo All operations completed successfully.
endlocal