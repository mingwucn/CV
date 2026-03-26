\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{resume}[2015/05/25 An elegant Résumé class]
\LoadClass[11pt]{article}

\RequirePackage{amsmath}
\RequirePackage{academicons}
\RequirePackage{outline}
% \RequirePackage{soul}

% ORCID
\RequirePackage{orcidlink}
% disable indent globally
\setlength{\parindent}{0pt}
% some general improvements, defines the XeTeX logo
\RequirePackage{xltxtra}
% use xifthen
\RequirePackage{xifthen}
% use progress bar for skill
\RequirePackage{progressbar}
% use hyperlink for email and url
\RequirePackage{hyperref}
\RequirePackage{xparse}
\RequirePackage{url}

% natbib
% \RequirePackage{natbib}
% \RequirePackage{bibentry} % For including full citations inline
% \bibliographystyle{IEEETran}
% \setcitestyle{numbers,sort&compress,square}

% BIB
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

\RequirePackage{svg}
\RequirePackage[off]{svg-extract}
\svgsetup{inkscapeversion=2,inkscapepath=./figures/, inkscapedpi=300, inkscapearea=page, inkscapelatex=true, extractformat={pdf,eps},clean=true}

% URL style
\urlstyle{tt}
% use fontawesome
\RequirePackage{fontawesome}
% use xcolor for customizing color
%\RequirePackage[usenames,dvipsnames]{xcolor}
\RequirePackage[svgnames,x11names,table]{xcolor}
% loading fonts
\RequirePackage{fontspec}
% Main document font
\setmainfont[
  Path = fonts/Main/ ,
  Extension = .otf ,
  UprightFont = *-regular ,
  BoldFont = *-bold ,
  ItalicFont = *-italic ,
  BoldItalicFont = *-bolditalic ,
  SmallCapsFont = Fontin-SmallCaps
]{texgyretermes}

\RequirePackage[
  a4paper,
  total={6in, 8in},
  left=0.55in,
  right=0.55in,
  top=0.70in,
  bottom=0.55in,
  nohead
]{geometry}

\RequirePackage{titlesec}
\RequirePackage{enumitem}
\setlist{noitemsep} % removes spacing from items but leaves space around the whole list
%\setlist{nosep} % removes all vertical spacing within and around the list
\setlist[itemize]{topsep=0.25em, leftmargin=1.5pc}
\setlist[enumerate]{topsep=0.25em, leftmargin=1.5pc}
\RequirePackage[super]{nth}

\titleformat{\section}         % Customise the \section command 
{\Large\scshape\raggedright} % Make the \section headers large (\Large),
% small capitals (\scshape) and left aligned (\raggedright)
{}{0em}                      % Can be used to give a prefix to all sections, like 'Section ...'
{}                           % Can be used to insert code before the heading
[\titlerule]                 % Inserts a horizontal line after the heading
\titlespacing*{\section}{0cm}{*1.8}{*1.8}

\titleformat{\subsection}
{\large\raggedright}
{}{0em}
{}
\titlespacing*{\subsection}{0cm}{*1.8}{*0.6}

\newcommand{\datedsection}[2]{%
  \section[#1]{#1 \hfill #2}%
}
\newcommand{\datedsubsection}[2]{%
  \subsection[#1]{#1 \hfill #2}%
}
\newcommand{\datedsubsubsection}[2]{%
  \subsubsection[#1]{#1 \hfill #2}%
}
\newcommand{\datedline}[2]{%
  {\par #1 \hfill #2 \par}%
}

\newcommand{\name}[1]{
  \centerline{\Huge\scshape{#1}}
  \vspace{1.25ex}
}

% defines one's name
% usage: \name{<name>}
\newcommand{\nameTest}[1]{
  {\large\scshape{#1}}
}

% defines one's email
% usage: \email{<email>}
\newcommand{\email}[1]{\faEnvelope\ \href{mailto:#1}{#1}}
% defines one's phone
% usage: \phone{<phone>}
\newcommand{\phone}[1]{\faPhone\ {#1}}
% defines one's linkedin
% usage: \linkedin{<linkedin>}
\newcommand{\linkedin}[2][]{\faLinkedin\
  \ifthenelse{\isempty{#1}}%
  {\href{#2}{#2}}
  {\href{#2}{#1}}}
% defines one's GitHub
% usage: \github{<github>}
\newcommand{\github}[2][]{\faGithub\
  \ifthenelse{\isempty{#1}}%
  {\href{#2}{#2}}
  {\href{#2}{#1}}}
% defines one's homepage
% usage: \homepage{<homepage>}
\newcommand{\homepage}[2][]{\faLink\
  \ifthenelse{\isempty{#1}}%
  {\href{#2}{#2}}
  {\href{#2}{#1}}}

% defines progress bar with text
% usage: \pbar[3][width]{Text}{percentage}
\newcommand{\pbar}[3][10em]{{#2}\
  \progressbar[heightr=1, width=#1, borderwidth=0pt, roundnessr=0.45, filledcolor=green!40, subdivisions=1]{#3}
}

\newcommand{\basicInfo}[1]{
  \centerline{\sffamily\large{#1}}
  \vspace{1.5ex}
}

\newcommand{\role}[2]{
  {\par \textit{#1} ~ #2 \par}
  \vspace{0.85ex}
}

\newcommand{\yourphoto}[1]{
  \hfill \smash{\includegraphics[width={#1}\paperwidth]{profile.jpg}}
}

\newcommand{\info}[4]{
\centerline{\sffamily\large{\ {#1}}
\ifthenelse{\isempty{#2}}%
{ } % if {#2} is empty
{\textperiodcentered\ \ {#2} } % homepage, no space before \text...
\ifthenelse{\isempty{#3}}%
{ } % if {#3} is empty
{\textperiodcentered\ \ {#3} } % homepage, no space before \text...
\ifthenelse{\isempty{#4}}%
{ } % if {#3} is empty
{\textperiodcentered\ \ {#4} }
}
\vspace{0.7ex}
}

\hypersetup{
  colorlinks=true,
  % linkcolor=MidnightBlue,
  % urlcolor=MidnightBlue,
  allcolors=RoyalBlue4
}

\setcounter{secnumdepth}{0}