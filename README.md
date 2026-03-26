# Academic CV Website

This repository contains both LaTeX source files for academic CVs and a dynamic GitHub Pages website that automatically parses and displays the content.

## Features

- **Dual Language Support**: English (`resume.tex`) and Chinese (`resume-zh_CN.tex`) versions
- **Dynamic Parsing**: The website automatically parses LaTeX files at runtime using JavaScript
- **Publication Management**: Publications are parsed from BibTeX files (`MyPaper.bib`, `MyPatent.bib`, `MyConference.bib`)
- **GitHub Pages Ready**: Deploy directly to GitHub Pages with automatic updates when you modify source files
- **Responsive Design**: Mobile-friendly, professional academic layout

### LaTeX Template Features

- Extremely customizable and extensible
- Full Unicode font support with XeLaTeX
- Perfect Chinese support using Adobe fonts
- FontAwesome 4.3.0 support

## Usage

### For GitHub Pages Website

1. **Update Source Files**: Modify `resume.tex` (English) or `resume-zh_CN.tex` (Chinese) with your content
2. **Update Publications**: Modify the BibTeX files:
   - `MyPaper.bib` - Journal publications
   - `MyConference.bib` - Conference papers  
   - `MyPatent.bib` - Patents
3. **Deploy to GitHub Pages**: Push to your repository's main branch and enable GitHub Pages
4. **Automatic Updates**: The website dynamically parses your source files on each page load

### For LaTeX Compilation

1. Compile locally with XeLaTeX:
   ```bash
   xelatex resume.tex
   ```
2. Or use online compilers like Overleaf/ShareLaTeX

## Website Structure

- `index.html` - Main website structure
- `styles.css` - Professional styling
- `parser.js` - LaTeX and BibTeX parsing logic
- `app.js` - Main application logic with language switching

## Deployment

To deploy to GitHub Pages:

1. Ensure your repository is public
2. Go to Settings → Pages
3. Select source: "Deploy from a branch"
4. Choose branch: `main` (or `master`)
5. Select folder: `/ (root)`
6. Save and wait for deployment

Your website will be available at: `https://yourusername.github.io/repository-name/`

## License

[The MIT License (MIT)](http://opensource.org/licenses/MIT)

Copyrighted fonts are not subjected to this License.
