import sys
sys.path.insert(0, '.')
from backend import load_all_papers

papers = load_all_papers()
print('Total papers:', len(papers))
if papers:
    for p in papers[:3]:
        print(f'  - {p.title[:50]}... cites={p.citations} role={p.role}')
else:
    print('No papers loaded')
    # Check if files exist
    import os
    for f in ['MyPaper.bib', 'MyConference.bib']:
        print(f'{f} exists:', os.path.exists(f))
