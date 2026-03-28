// app.js - Main application logic for dynamic CV parsing
class CVWebsite {
    constructor() {
        this.currentLanguage = 'en';
        this.latexParser = new LatexParser();
        this.bibtexParser = new BibTeXParser();
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.loadContent();
    }
    
    setupEventListeners() {
        const langToggle = document.getElementById('langToggle');
        if (langToggle) {
            langToggle.addEventListener('click', () => this.toggleLanguage());
        }
    }
    
    toggleLanguage() {
        this.currentLanguage = this.currentLanguage === 'en' ? 'zh' : 'en';
        this.updateLanguageDisplay();
        this.loadContent();
    }
    
    updateLanguageDisplay() {
        const langToggle = document.getElementById('langToggle');
        const footerText = document.getElementById('footerText');
        
        if (this.currentLanguage === 'en') {
            langToggle.textContent = '中文';
            if (footerText) footerText.innerHTML = footerText.dataset.en;
        } else {
            langToggle.textContent = 'English';
            if (footerText) footerText.innerHTML = footerText.dataset.zh;
        }
        
        // Update all section titles
        const sectionTitles = document.querySelectorAll('.section-title');
        sectionTitles.forEach(title => {
            if (this.currentLanguage === 'en') {
                title.textContent = title.dataset.en || title.textContent;
            } else {
                title.textContent = title.dataset.zh || title.textContent;
            }
        });
        
        // Update publication section titles
        const pubTitles = document.querySelectorAll('.pub-section h3');
        const pubSectionMap = {
            'Journal Papers': '期刊论文',
            'Conference Papers': '会议论文', 
            'Patents': '专利'
        };
        
        pubTitles.forEach(title => {
            const enText = Object.keys(pubSectionMap).find(key => pubSectionMap[key] === title.textContent) || title.textContent;
            if (this.currentLanguage === 'en') {
                title.textContent = enText;
            } else {
                title.textContent = pubSectionMap[enText] || title.textContent;
            }
        });
    }
    
    async loadContent() {
        try {
            // Load and parse LaTeX file based on language
            const latexFile = this.currentLanguage === 'en' ? 'resume.tex' : 'resume-zh_CN.tex';
            const latexResponse = await fetch(latexFile);
            if (!latexResponse.ok) {
                throw new Error(`Failed to load ${latexFile}`);
            }
            const latexContent = await latexResponse.text();
            const parsedData = this.latexParser.parseLatex(latexContent);
            
            // Load and parse BibTeX files
            const paperResponse = await fetch('MyPaper.bib');
            const patentResponse = await fetch('MyPatent.bib'); 
            const conferenceResponse = await fetch('MyConference.bib');
            
            let papers = [], patents = [], conferences = [];
            
            if (paperResponse.ok) {
                const paperContent = await paperResponse.text();
                papers = this.bibtexParser.parseBibTeX(paperContent).map(entry => 
                    this.bibtexParser.formatPublication(entry)
                );
            }
            
            if (patentResponse.ok) {
                const patentContent = await patentResponse.text();
                patents = this.bibtexParser.parseBibTeX(patentContent).map(entry => 
                    this.bibtexParser.formatPublication(entry)
                );
            }
            
            if (conferenceResponse.ok) {
                const conferenceContent = await conferenceResponse.text();
                conferences = this.bibtexParser.parseBibTeX(conferenceContent).map(entry => 
                    this.bibtexParser.formatPublication(entry)
                );
            }
            
            // Render content
            this.renderContent(parsedData, papers, patents, conferences);
            
        } catch (error) {
            console.error('Error loading content:', error);
            this.showError('Failed to load CV content. Please ensure all source files are available.');
        }
    }
    
    renderContent(parsedData, papers, patents, conferences) {
        // Render personal info
        if (parsedData.personalInfo && parsedData.personalInfo.name) {
            document.getElementById('fullName').textContent = parsedData.personalInfo.name;
        }
        
        // Render contact info
        if (parsedData.contactInfo && parsedData.contactInfo.length > 0) {
            const contactContainer = document.getElementById('contactInfo');
            contactContainer.innerHTML = '';
            parsedData.contactInfo.forEach(contact => {
                const contactItem = document.createElement('div');
                contactItem.className = 'contact-item';
                contactItem.innerHTML = contact;
                contactContainer.appendChild(contactItem);
            });
        }
        
        // Render sections
        this.renderSection('researchVision', ['Research Vision', '研究愿景'], parsedData);
        this.renderSection('education', ['Education', '教育背景'], parsedData);
        this.renderSection('appointments', ['Academic Appointments', '职业经历'], parsedData);
        this.renderSection('grants', ['Research Grants & Secured Funding', '研究资助与项目经历'], parsedData);
        this.renderSection('teaching', ['Teaching & Mentorship Competencies', '教学活动'], parsedData);
        this.renderSection('innovation', ['Innovation & Technology Transfer', '专利及成果转化'], parsedData);
        this.renderSection('miscellaneous', ['Miscellaneous', '其他信息'], parsedData);
        
        // Render publications
        this.renderPublications(papers, patents, conferences);
    }
    
    renderSection(sectionId, sectionKeys, parsedData) {
        const sectionKey = this.currentLanguage === 'en' ? sectionKeys[0] : sectionKeys[1];
        const sectionData = parsedData[sectionKey];
        const container = document.getElementById(`${sectionId}Content`);
        
        if (container && sectionData) {
            if (sectionData.content && sectionData.content.trim()) {
                // Simple text content (like Research Vision)
                container.innerHTML = `<p>${sectionData.content.trim()}</p>`;
            } else if (sectionData.items && sectionData.items.length > 0) {
                // List of items with dates and content
                container.innerHTML = '';
                sectionData.items.forEach(item => {
                    if (item.type === 'dated_entry' || item.type === 'dated_subentry') {
                        const entryDiv = document.createElement('div');
                        entryDiv.className = 'dated-entry';
                        
                        const titleEl = document.createElement('div');
                        titleEl.className = 'entry-title';
                        titleEl.innerHTML = item.title || '';
                        
                        const dateEl = document.createElement('span');
                        dateEl.className = 'entry-date';
                        dateEl.textContent = item.date || '';
                        
                        entryDiv.appendChild(titleEl);
                        if (dateEl.textContent) {
                            entryDiv.appendChild(dateEl);
                        }
                        
                        if (item.content && item.content.length > 0) {
                            const contentEl = document.createElement('div');
                            contentEl.className = 'entry-content';
                            const ul = document.createElement('ul');
                            item.content.forEach(contentItem => {
                                if (contentItem.trim()) {
                                    const li = document.createElement('li');
                                    li.innerHTML = contentItem;
                                    ul.appendChild(li);
                                }
                            });
                            if (ul.children.length > 0) {
                                contentEl.appendChild(ul);
                                entryDiv.appendChild(contentEl);
                            }
                        }
                        
                        container.appendChild(entryDiv);
                    }
                });
            }
        }
    }
    
    renderPublications(papers, patents, conferences) {
        // Render journal papers
        const journalContainer = document.getElementById('journalPapersContent');
        if (journalContainer) {
            if (papers.length > 0) {
                journalContainer.innerHTML = '';
                papers.forEach(pub => {
                    if (pub.title) {
                        const pubDiv = document.createElement('div');
                        pubDiv.className = 'publication-item';
                        pubDiv.innerHTML = `
                            <div class="pub-authors">${pub.authors || ''}</div>
                            <div class="pub-title">${pub.title}</div>
                            <div class="pub-journal">${pub.journal || ''}</div>
                            <div class="pub-year">${pub.year || ''}</div>
                        `;
                        journalContainer.appendChild(pubDiv);
                    }
                });
            } else {
                journalContainer.innerHTML = '<p>No journal publications available.</p>';
            }
        }
        
        // Render conferences
        const confContainer = document.getElementById('conferencesContent');
        if (confContainer) {
            if (conferences.length > 0) {
                confContainer.innerHTML = '';
                conferences.forEach(pub => {
                    if (pub.title) {
                        const pubDiv = document.createElement('div');
                        pubDiv.className = 'publication-item';
                        pubDiv.innerHTML = `
                            <div class="pub-authors">${pub.authors || ''}</div>
                            <div class="pub-title">${pub.title}</div>
                            <div class="pub-journal">${pub.journal || ''}</div>
                            <div class="pub-year">${pub.year || ''}</div>
                        `;
                        confContainer.appendChild(pubDiv);
                    }
                });
            } else {
                confContainer.innerHTML = '<p>No conference publications available.</p>';
            }
        }
        
        // Render patents
        const patentContainer = document.getElementById('patentsContent');
        if (patentContainer) {
            if (patents.length > 0) {
                patentContainer.innerHTML = '';
                patents.forEach(pub => {
                    if (pub.title) {
                        const pubDiv = document.createElement('div');
                        pubDiv.className = 'publication-item';
                        pubDiv.innerHTML = `
                            <div class="pub-authors">${pub.authors || ''}</div>
                            <div class="pub-title">${pub.title}</div>
                            <div class="pub-journal">${pub.journal || ''}</div>
                            <div class="pub-year">${pub.year || ''}</div>
                        `;
                        patentContainer.appendChild(pubDiv);
                    }
                });
            } else {
                patentContainer.innerHTML = '<p>No patents available.</p>';
            }
        }
    }
    
    showError(message) {
        const mainContent = document.querySelector('.main-content');
        mainContent.innerHTML = `<div style="text-align: center; padding: 2rem; color: #e74c3c;">${message}</div>`;
    }
}

// Initialize the website when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Check if required files exist by attempting to create the website
    try {
        new CVWebsite();
    } catch (error) {
        console.error('Failed to initialize CV website:', error);
        document.body.innerHTML = '<div style="padding: 2rem; text-align: center;">Error loading website. Please check browser console for details.</div>';
    }
});
