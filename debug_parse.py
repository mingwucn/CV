import sys
sys.path.insert(0, '.')
from backend import parse_bib_text, TARGET_ALIASES, CITATION_FIELD

with open('MyPaper.bib', 'r', encoding='utf-8') as f:
    content = f.read()
papers = parse_bib_text(content, TARGET_ALIASES, CITATION_FIELD)
print('Parsed papers:', len(papers))
if papers:
    for p in papers[:3]:
        print(f'  - {p.title[:50]}... cites={p.citations} role={p.role}')
else:
    print('No papers parsed. Check regex.')
    # Let's see the first few lines of the bib file
    lines = content.split('\n')[:10]
    for i, line in enumerate(lines):
        print(f'{i}: {line}')
