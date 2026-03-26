"""
FastAPI backend for C‑Score Calculator.
Serves static files and provides API to load/save citation data.
"""
import json
import os
from pathlib import Path
from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Configuration
BIB_FILES = ["MyPaper.bib", "MyConference.bib"]
CITATIONS_JSON = "citations.json"  # stores manual citation overrides
TARGET_ALIASES = ["Wu, M", "M. Wu", "Wu, M.", "Wu, M*", "M. Wu*", "Ming Wu"]
CITATION_FIELD = "citationthisyear"

app = FastAPI(title="C‑Score Calculator API")

# Serve static files (HTML, CSS, JS) from current directory
app.mount("/static", StaticFiles(directory="."), name="static")

# --------------------------------------------------------------------
# Data models
# --------------------------------------------------------------------
class Paper(BaseModel):
    title: str
    year: int
    authors: str
    role: str
    citations: int
    num_authors: int
    ncs: int = 0
    ncsf: int = 0
    ncsfl: int = 0
    source_file: str = ""  # which .bib file this paper came from
    journal: str = ""      # journal or conference name

class CitationUpdate(BaseModel):
    title: str
    citations: int

# --------------------------------------------------------------------
# Helper functions (copied from c‑score.py)
# --------------------------------------------------------------------
def normalize_name(name: str) -> str:
    import re
    # Remove all punctuation characters (non-alphanumeric, non-space)
    return re.sub(r'[^\w\s]', '', name).lower().strip()

def parse_bib_text(content: str, aliases: List[str], citation_key: str, source_file: str = "") -> List[Paper]:
    target_aliases_clean = {normalize_name(a) for a in aliases}
    import re
    
    # Find all @Article entries
    article_pattern = r'@Article\s*\{[^@]+'
    articles = re.findall(article_pattern, content, re.DOTALL)
    papers = []

    for article in articles:
        # Extract fields
        field_pattern = r'(\w+)\s*=\s*[\{"](.*?)(?<!\\)[\}"]'
        fields = {}
        for match in re.finditer(field_pattern, article, re.DOTALL):
            key = match.group(1).lower()
            val = match.group(2).replace('\n', ' ').strip()
            fields[key] = val

        if 'author' not in fields:
            continue

        # Title
        title = fields.get('title', 'Unknown Title')
        title = re.sub(r'\s+', ' ', title)

        # Citations
        cites = 0
        if citation_key.lower() in fields:
            try:
                cites = int(fields[citation_key.lower()])
            except ValueError:
                cites = 0

        # Authors
        raw_authors = fields['author']
        author_list = re.split(r'\s+and\s+', raw_authors, flags=re.IGNORECASE)
        author_list = [a.strip() for a in author_list]
        num_authors = len(author_list)

        # Find author position
        match_index = -1
        for idx, author in enumerate(author_list):
            if normalize_name(author) in target_aliases_clean:
                match_index = idx
                break
        if match_index == -1:
            continue

        # Determine role
        if num_authors == 1:
            role = 'single'
        elif match_index == 0:
            role = 'first'
        elif match_index == num_authors - 1:
            role = 'last'
        else:
            role = 'middle'

        # Year
        year = int(fields.get('year', 0)) if fields.get('year', '').isdigit() else 0

        # Journal
        journal = fields.get('journal', '')

        papers.append(Paper(
            title=title,
            year=year,
            authors=fields['author'],
            role=role,
            citations=cites,
            num_authors=num_authors,
            source_file=source_file,
            journal=journal
        ))
    return papers

def load_all_papers() -> List[Paper]:
    """Load papers from .bib files and apply manual overrides."""
    all_papers = []
    for fname in BIB_FILES:
        if not os.path.exists(fname):
            continue
        with open(fname, 'r', encoding='utf-8') as f:
            content = f.read()
        papers = parse_bib_text(content, TARGET_ALIASES, CITATION_FIELD, source_file=fname)
        all_papers.extend(papers)

    # Apply manual overrides
    if os.path.exists(CITATIONS_JSON):
        with open(CITATIONS_JSON, 'r', encoding='utf-8') as f:
            overrides = json.load(f)
        override_dict = {o['title']: o['citations'] for o in overrides}
        for paper in all_papers:
            if paper.title in override_dict:
                paper.citations = override_dict[paper.title]

    return all_papers

def save_citation_overrides(papers: List[Paper]):
    """Save current citation values to JSON (only those different from original?)."""
    overrides = [{"title": p.title, "citations": p.citations} for p in papers]
    with open(CITATIONS_JSON, 'w', encoding='utf-8') as f:
        json.dump(overrides, f, indent=2)

def update_bib_files(papers: List[Paper]):
    """Update citationthisyear field in the original .bib files."""
    # Group papers by source file
    by_source = {}
    for paper in papers:
        if not paper.source_file:
            continue
        by_source.setdefault(paper.source_file, []).append(paper)
    
    for source_file, paper_list in by_source.items():
        if not os.path.exists(source_file):
            continue
        with open(source_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Build mapping from title to new citation count
        title_to_cite = {p.title: p.citations for p in paper_list}
        
        # Process lines to find entries and update citationthisyear
        i = 0
        while i < len(lines):
            line = lines[i]
            # Look for start of an entry
            if line.strip().startswith('@'):
                # Find the end of this entry (next line that starts with '}' at same indentation? We'll assume entry ends with a line containing '}' alone)
                # Simpler: we'll just look for the title field within the next ~30 lines.
                for j in range(i, min(i + 30, len(lines))):
                    if 'title' in lines[j] and '=' in lines[j]:
                        # Extract title value
                        import re
                        match = re.search(r'title\s*=\s*\{([^}]+)\}', lines[j])
                        if not match:
                            # Could be multi-line title, skip for simplicity
                            break
                        title = match.group(1).strip()
                        # Check if this title matches any paper
                        matched = False
                        for paper_title, new_cite in title_to_cite.items():
                            # Simple substring match (title in paper_title or vice versa)
                            if paper_title in title or title in paper_title:
                                # Found matching entry, now find citationthisyear line
                                for k in range(i, min(i + 50, len(lines))):
                                    if 'citationthisyear' in lines[k] and '=' in lines[k]:
                                        # Replace the number inside braces
                                        lines[k] = re.sub(r'(citationthisyear\s*=\s*\{)[^}]+(\})', rf'\g<1>{new_cite}\2', lines[k])
                                        matched = True
                                        break
                                if matched:
                                    break
                        if matched:
                            break
                # Skip forward
                i += 1
            else:
                i += 1
        
        # Write back
        with open(source_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        print(f"Updated {source_file}")

# --------------------------------------------------------------------
# API endpoints
# --------------------------------------------------------------------
@app.get("/")
def serve_index():
    """Serve the main HTML page."""
    return FileResponse("c-score-app.html")

@app.get("/api/papers", response_model=List[Paper])
def get_papers():
    """Return all papers with current citation counts."""
    return load_all_papers()

@app.post("/api/citations")
def update_citations(updates: List[CitationUpdate]):
    """Update citation counts for specific papers."""
    papers = load_all_papers()
    paper_dict = {p.title: p for p in papers}
    for update in updates:
        if update.title in paper_dict:
            paper_dict[update.title].citations = update.citations
    save_citation_overrides(list(paper_dict.values()))
    # Also write back to .bib files
    update_bib_files(list(paper_dict.values()))
    return {"message": "Citations updated (saved to .bib files)"}

@app.post("/api/reset")
def reset_citations():
    """Reset all citations to original values from .bib files (delete overrides)."""
    if os.path.exists(CITATIONS_JSON):
        os.remove(CITATIONS_JSON)
    return {"message": "Citations reset to original"}

# --------------------------------------------------------------------
# Run with: uvicorn backend:app --reload
# --------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
