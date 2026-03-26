\NeedsTeXFormat{LaTeX2e}

\ProvidesClass{myCitation}[Powered by Ming Wu]
\LoadClass[11pt]{article}

% \RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
% \RequirePackage[sfdefault]{carlito}
\RequirePackage{helvet}
\renewcommand{\familydefault}{\sfdefault}
\RequirePackage{xparse}
\RequirePackage{textcomp}
% \RequirePackage{url}



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
% \RequirePackage{firasans}
% \RequirePackage{cmbright}
\RequirePackage{amsmath}
\RequirePackage{outline}
\RequirePackage{graphicx}
\RequirePackage[svgnames,x11names,table]{xcolor}
\definecolor{OliveGreen}{rgb}{0,0.6,0}
\definecolor{citeRed}{HTML}{aa3377}
\RequirePackage{svg}
\RequirePackage[off]{svg-extract}
\svgsetup{inkscapeversion=2,inkscape=force, inkscapepath=./figures/, inkscapedpi=600, inkscapearea=page, inkscapelatex=true, inkscapeformat=pdf, extractformat={pdf},clean=true, extractpath=./fig}
\RequirePackage[
  a4paper,
%   total={6in, 8in},
  left=3cm,
  right=2.5cm
%   top=0.70in,
%   bottom=0.55in,
%   nohead
]{geometry}
\RequirePackage[normalem]{ulem}
\RequirePackage{orcidlink}
\RequirePackage{hyperref}
% citation
\newcommand{\fcite}[1]{\fullcite{#1}\label{#1}}

\NewDocumentCommand{\ecite}{mm}{%
  \hyperref[#1]{#1}%
}



% Just return the citation number
% \DeclareCiteCommand{\jn}
%   {}
%   {\printfield{labelnumber}}
%   {\multicitedelim}
%   {}

% Definition for paper citations (\jcite)
\NewDocumentCommand{\jcite}{om}{%
  {\textcolor{RoyalBlue4}{[J: \justnumber{#2}]}}%
  \IfNoValueTF{#1}
  {}
  {(\textit{\unexpanded{#1}})}
}
\NewDocumentCommand{\ccite}{om}{%
  {{[C}&: {\justnumber{#2}]}}%
  \IfNoValueTF{#1}
  {}
  {(\textit{\unexpanded{#1}})}
}
\NewDocumentCommand{\Pcite}{om}{%
  {\textcolor{RoyalBlue4}{[P: \justnumber{#2}]}}%
  \IfNoValueTF{#1}
  {}
  {(\textit{\unexpanded{#1}})}
}
% \newbibmacro*{jcitecheck}{
%   \ifkeyword{paper}
%     {\usebibmacro{citeindex}\usebibmacro{cite}}
%     {\PackageWarning{biblatex}{Citation '\thefield{entrykey}' is not a journal paper.}}%
% }

% \DeclareCiteCommand{\jcite}
%   {\usebibmacro{prenote}}
%   {\usebibmacro{jcitecheck}}
%   {\multicitedelim}
%   {\usebibmacro{postnote}}

% \DeclareCiteCommand{\ccite}
%   {\usebibmacro{prenote}}
%   {\ifkeyword{conference}
%      {\usebibmacro{citeindex}\usebibmacro{cite}}
%      {\PackageWarning{biblatex}{Citation '#1' is not a conference.}}}
%   {\multicitedelim}
%   {\usebibmacro{postnote}}

% \NewDocumentCommand{\ccite}{om}{%
%   {\textcolor{RoyalBlue4}{[C - \justnumber{#2}]}}%
%   \IfNoValueTF{#1}
%   {}
%   {(\textit{\unexpanded{#1}})}
% }


% \NewDocumentCommand{\pcite}{om}{%
%   {\textcolor{RoyalBlue4}{[P - \justnumber{#2}]}}%
%   \IfNoValueTF{#1}
%   {}
%   {(\textit{\unexpanded{#1}})}
% }

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
\newcommand\hl{\bgroup\markoverwith
    {\textcolor{yellow}{\rule[-.5ex]{.1pt}{2.5ex}}}\ULon}
  




% \RequirePackage{enumitem}

\hypersetup{
  colorlinks=true,
  % linkcolor=MidnightBlue,
  % urlcolor=MidnightBlue,
  allcolors=RoyalBlue4
}