\NeedsTeXFormat{LaTeX2e}

\ProvidesClass{ResearchStatement}[2015/05/25 An elegant Résumé class]
\LoadClass[9pt]{article}
% \RequirePackage[
%   a4paper,
% %   total={6in, 8in},
%   left=3cm,
%   right=2.5cm
%   top=0.20in,
%   bottom=0.25in,
% %   nohead
% ]{geometry}
\RequirePackage{amsmath}
\RequirePackage{upgreek}
% \newcommand{\subsubsection}[1]{\paragraph{\textbf{#1}}\mbox{}\\}
% \setcounter{secnumdepth}{3}
% \setcounter{tocdepth}{3}
\newcommand{\subsubsubsection}[1]{\paragraph{\textbf{#1}}\mbox{}\\}
\setcounter{secnumdepth}{4}
\setcounter{tocdepth}{4}

\newcommand{\subsubsubsubsection}[1]{\paragraph{\textbf{#1}}\mbox{}\\}
\setcounter{secnumdepth}{5}
\setcounter{tocdepth}{5}
% \RequirePackage{outline}
\RequirePackage[svgnames,x11names,table]{xcolor}
% \RequirePackage{soul}

% ORCID
\RequirePackage{orcidlink}
% disable indent globally
% \setlength{\parindent}{0pt}
% some general improvements, defines the XeTeX logo
% \RequirePackage{xltxtra}
% use xifthen
% \RequirePackage{xifthen}
% use progress bar for skill
% \RequirePackage{progressbar}
% use hyperlink for email and url
\RequirePackage{hyperref}
\RequirePackage{xparse}

% natbib
% \RequirePackage{natbib}
% \RequirePackage{bibentry} % For including full citations inline
% \bibliographystyle{IEEETran}
% \setcitestyle{numbers,sort&compress,square}

% BIB[backend=biber, sorting=ydnt, style=ieee, maxbibnames=999,maxcitenames=999,url=true,eprint=false,date=year]{biblatex}
\RequirePackage[backend=biber, sorting=none, style=ieee, maxbibnames=999,maxcitenames=999,url=true,eprint=false,date=year]{biblatex}

\DeclareFieldFormat[article]{title}{#1} % Remove quotes around titles
\DeclareFieldFormat[article]{journaltitle}{#1} % Journal title in plain text
\DeclareFieldFormat[article]{volume}{#1}
\DeclareFieldFormat{date}{\mkbibparens{#1}} % Date in parentheses
\renewbibmacro*{date}{\printdate} % Remove month from date
\DeclareFieldFormat{pages}{#1} % Remove "pp." from pages
\DeclareFieldFormat{groups}{#1} 

% Customize the bibliography driver for articles
\DeclareBibliographyDriver{article}{%
  \usebibmacro{bibindex}%
  \usebibmacro{author}%
  \setunit{\addcomma\space}\newblock
  \usebibmacro{title}%
  \newunit\newblock
  \usebibmacro{journal+issuetitle}%
  \newunit\newblock
  \usebibmacro{date}%
  \newunit\newblock
  \usebibmacro{pages}%
  \newunit\newblock
  \printfield{doi}%
  \newunit\newblock
  \printfield{note}%
  \newunit\newblock
  \finentry
}
\newcommand\SLASH{\texttt{\char`\~}}
% Customize the journal+issuetitle macro
\renewbibmacro*{journal+issuetitle}{%
  \usebibmacro{journal}%
  \setunit{\addspace}%
  \printfield{volume}%
  \setunit{\addspace}%
  \printfield{number}%
  \setunit{\addspace}%
  \printfield{eid}%
  \newunit
}

% If using custom fields, map them first:
\DeclareSourcemap{
  \maps[datatype=bibtex]{
    \map{
      \step[fieldset=comment,fieldsource=comment]
    }
  }
}

% citation
\newcommand{\fcite}[1]{\fullcite{#1}\label{#1}}

\NewDocumentCommand{\ecite}{mm}{%
  \hyperref[#1]{#1}%
}

\DeclareCiteCommand{\justnumber}
  {}
  {\printfield{labelnumber}}
  {\multicitedelim}
  {}

% Definition for paper citations (\jcite)
\NewDocumentCommand{\jcite}{om}{%
  \mkbibbrackets{J - \justnumber{#2}}%
  \IfNoValueTF{[\textcolor{RoyalBlue4}{#1}]}{}{(\textit{\unexpanded{#1}})}}


% Definition for conference citations (\ccite)
\NewDocumentCommand{\ccite}{om}{%
  \mkbibbrackets{C - \justnumber{#2}}%
  \IfNoValueTF{#1}{}{ (\unexpanded{#1})}%
}

% Definition for patent citations (\pcite)
\NewDocumentCommand{\pcite}{om}{%
  \mkbibbrackets{P - \justnumber{#2}}%
  \IfNoValueTF{#1}{}{ (\unexpanded{#1})}%
}

% \NewDocumentCommand{\jcite}{om}{%
%   \IfNoValueTF{#1}
%     {J\cite{#2}}
%     {J\cite[#1]{#2}}%
% }


\NewDocumentCommand{\projectcite}{mm}{%
  \hyperref[project:#1]{#1}%
}

\NewDocumentCommand{\projectcitec}{mm}{%
  \hyperref[project:#1]{#1}%
}

% Custom citation macros
\DeclareCiteCommand{\paper}[\mkbibparens]
  {\usebibmacro{prenote}}
  {\mkbibemph{#1}~\printfield{year}}
  {\multicitedelim}
  {\usebibmacro{postnote}}

\DeclareCiteCommand{\conference}[\mkbibparens]
  {\usebibmacro{prenote}}
  {\printfield{year}}
  {\multicitedelim}
  {\usebibmacro{postnote}}

% Smart citation formatter
\NewDocumentCommand{\myCite}{m}{
  \IfBibliography{\cite{#1}}{
    \ifentrytype{article}{\paper{#1}}
    {\ifentrytype{inproceedings}{\conference{#1}}
    {\cite{#1}}}
  }
}

% highlight
\RequirePackage[normalem]{ulem}
\newcommand\hl{\bgroup\markoverwith
    {\textcolor{yellow}{\rule[-.5ex]{.1pt}{2.5ex}}}\ULon}
  
\definecolor{OliveGreen}{rgb}{0,0.6,0}

\RequirePackage{graphicx}
\RequirePackage{caption}
\RequirePackage{svg}
\RequirePackage[off]{svg-extract}
\svgsetup{inkscapeversion=2,inkscape=force, inkscapepath=./figures/, inkscapedpi=600, inkscapearea=page, inkscapelatex=false, inkscapeformat=png, extractformat={pdf},clean=true, extractpath=./fig}



% \RequirePackage{enumitem}

\hypersetup{
  colorlinks=true,
  % linkcolor=MidnightBlue,
  % urlcolor=MidnightBlue,
  allcolors=RoyalBlue4
}