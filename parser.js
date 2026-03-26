// LaTeX and BibTeX Parser for Academic CV
class LatexParser {
    constructor() {
        this.currentLanguage = 'en';
    }

    // Parse LaTeX file content
    parseLatex(content) {
        const sections = {};
        let currentSection = '';
        
        // Split into lines and process
        const lines = content.split('\n');
        let inItemize = false;
        let currentItemContent = [];
        let currentItem = null;
        
        for (let i = 0; i < lines.length; i++) {
            const line = lines[i].trim();
            
            // Skip empty lines and comments
            if (line === '' || line.startsWith('%')) continue;
            
            // Handle section commands
            if (line.startsWith('\\section{')) {
                currentSection = this.extractBraceContent(line, '\\section{');
                sections[currentSection] = { items: [], raw: line };
                continue;
            }
            
            // Handle subsection commands  
            if (line.startsWith('\\subsection{')) {
                const subsection = this.extractBraceContent(line, '\\subsection{');
                if (!sections[currentSection]) {
                    sections[currentSection] = { items: [], raw: '' };
                }
                sections[currentSection].items.push({
                    type: 'subsection',
                    content: subsection
                });
                continue;
            }
            
            // Handle dated subsections
            if (line.startsWith('\\datedsubsection{')) {
                const match = line.match(/\\datedsubsection\{([^}]+)\}\{([^}]+)\}/);
                if (match) {
                    const title = match[1];
                    const date = match[2];
                    const item = {
                        type: 'dated_entry',
                        title: this.cleanLatex(title),
                        date: this.cleanLatex(date),
                        content: []
                    };
                    
                    // Look ahead for itemize content
                    let j = i + 1;
                    while (j < lines.length && !lines[j].trim().startsWith('\\') && 
                           !lines[j].trim().startsWith('%') && lines[j].trim() !== '') {
                        j++;
                    }
                    
                    // Check if next non-empty line is \begin{itemize}
                    if (j < lines.length && lines[j].includes('\\begin{itemize}')) {
                        i = j;
                        inItemize = true;
                        currentItem = item;
                        currentItemContent = [];
                        continue;
                    }
                    
                    if (!sections[currentSection]) {
                        sections[currentSection] = { items: [], raw: '' };
                    }
                    sections[currentSection].items.push(item);
                }
                continue;
            }
            
            // Handle dated subsubsections
            if (line.startsWith('\\datedsubsubsection{')) {
                const match = line.match(/\\datedsubsubsection\{([^}]+)\}\{([^}]+)\}/);
                if (match) {
                    const title = match[1];
                    const date = match[2];
                    const item = {
                        type: 'dated_subentry',
                        title: this.cleanLatex(title),
                        date: this.cleanLatex(date),
                        content: []
                    };
                    
                    if (!sections[currentSection]) {
                        sections[currentSection] = { items: [], raw: '' };
                    }
                    sections[currentSection].items.push(item);
                }
                continue;
            }
            
            // Handle itemize environment
            if (line.includes('\\begin{itemize}')) {
                inItemize = true;
                currentItemContent = [];
                continue;
            }
            
            if (line.includes('\\end{itemize}')) {
                inItemize = false;
                if (currentItem) {
                    currentItem.content = currentItemContent.map(item => this.cleanLatex(item));
                    if (!sections[currentSection]) {
                        sections[currentSection] = { items: [], raw: '' };
                    }
                    sections[currentSection].items.push(currentItem);
                    currentItem = null;
                }
                continue;
            }
            
            // Handle item content
            if (inItemize && line.startsWith('\\item')) {
                let itemContent = line.substring(5).trim();
                // Check if item continues on next lines
                let j = i + 1;
                while (j < lines.length && 
                       !lines[j].trim().startsWith('\\') && 
                       !lines[j].trim().startsWith('%') && 
                       lines[j].trim() !== '' &&
                       !lines[j].includes('\\end{itemize}')) {
                    itemContent += ' ' + lines[j].trim();
                    j++;
                }
                currentItemContent.push(itemContent);
                i = j - 1; // Adjust loop counter
                continue;
            }
            
            // Handle personal info commands
            if (line.startsWith('\\name{')) {
                sections.personalInfo = sections.personalInfo || {};
                sections.personalInfo.name = this.extractBraceContent(line, '\\name{');
                continue;
            }
            
            if (line.startsWith('\\info{')) {
                sections.contactInfo = sections.contactInfo || [];
                const contactItems = this.parseContactInfo(line);
                sections.contactInfo.push(...contactItems);
                continue;
            }
            
            // Handle research vision (special case)
            if (currentSection === 'Research Vision' || currentSection === '研究愿景') {
                if (!line.startsWith('\\section{') && !line.startsWith('\\')) {
                    if (!sections[currentSection]) {
                        sections[currentSection] = { content: '' };
                    }
                    sections[currentSection].content += line + ' ';
                }
            }
        }
        
        return sections;
    }
    
    parseContactInfo(line) {
        const contacts = [];
        // Extract all \\href or email/phone links
        const regex = /\\(?:email|phone|linkedin|github|orcidlink|homepage|aiGoogleScholar)\{[^}]*\}(?:\{[^}]*\})?|\\href\{[^}]+\}\{[^}]+\}/g;
        let match;
        while ((match = regex.exec(line)) !== null) {
            contacts.push(this.cleanLatex(match[0]));
        }
        return contacts;
    }
    
    extractBraceContent(line, prefix) {
        const startIndex = line.indexOf('{');
        if (startIndex === -1) return '';
        let braceCount = 1;
        let endIndex = startIndex + 1;
        while (endIndex < line.length && braceCount > 0) {
            if (line[endIndex] === '{') braceCount++;
            else if (line[endIndex] === '}') braceCount--;
            endIndex++;
        }
        return line.substring(startIndex + 1, endIndex - 1);
    }
    
    cleanLatex(text) {
        if (!text) return '';
        
        // Remove LaTeX commands
        let cleaned = text
            .replace(/\\textbf\{([^}]+)\}/g, '$1')
            .replace(/\\textit\{([^}]+)\}/g, '$1')
            .replace(/\\underline\{([^}]+)\}/g, '$1')
            .replace(/\\SLASH/g, '/')
            .replace(/\\%/g, '%')
            .replace(/\\&/g, '&')
            .replace(/\\#/g, '#')
            .replace(/\\$/g, '$')
            .replace(/\\\{/g, '{')
            .replace(/\\\}/g, '}')
            .replace(/\\textbackslash/g, '\\')
            .replace(/~+/g, ' ')
            .replace(/\s+/g, ' ')
            .trim();
            
        // Handle href links
        cleaned = cleaned.replace(/\\href\{([^}]+)\}\{([^}]+)\}/g, '<a href="$1" target="_blank">$2</a>');
        
        return cleaned;
    }
}

class BibTeXParser {
    parseBibTeX(content) {
        const entries = [];
        const lines = content.split('\n');
        let currentEntry = null;
        let inEntry = false;
        
        for (const line of lines) {
            const trimmed = line.trim();
            if (trimmed === '') continue;
            if (trimmed.startsWith('%')) continue;
            
            // Start of new entry
            if (trimmed.startsWith('@')) {
                if (currentEntry) {
                    entries.push(currentEntry);
                }
                const match = trimmed.match(/@(\w+)\{([^,]+),/);
                if (match) {
                    currentEntry = {
                        type: match[1].toLowerCase(),
                        id: match[2],
                        fields: {}
                    };
                    inEntry = true;
                }
                continue;
            }
            
            // End of entry
            if (trimmed === '}' && inEntry) {
                if (currentEntry) {
                    entries.push(currentEntry);
                    currentEntry = null;
                }
                inEntry = false;
                continue;
            }
            
            // Field assignment
            if (inEntry && trimmed.includes('=')) {
                const equalIndex = trimmed.indexOf('=');
                const key = trimmed.substring(0, equalIndex).trim().toLowerCase();
                let value = trimmed.substring(equalIndex + 1).trim();
                
                // Remove trailing comma if present
                if (value.endsWith(',')) {
                    value = value.substring(0, value.length - 1);
                }
                
                // Remove surrounding braces or quotes
                if (value.startsWith('{') && value.endsWith('}')) {
                    value = value.substring(1, value.length - 1);
                } else if (value.startsWith('"') && value.endsWith('"')) {
                    value = value.substring(1, value.length - 1);
                }
                
                currentEntry.fields[key] = value;
            }
        }
        
        return entries;
    }
    
    formatPublication(entry) {
        const fields = entry.fields;
        return {
            id: entry.id,
            authors: fields.author || '',
            title: fields.title || '',
            journal: fields.journal || fields.booktitle || '',
            year: fields.year || '',
            type: entry.type
        };
    }
}
