import sys
sys.path.insert(0, '.')
from backend import parse_bib_text, TARGET_ALIASES, CITATION_FIELD
import re

with open('MyPaper.bib', 'r', encoding='utf-8') as f:
    content = f.read()

# Use the same splitting as in parse_bib_text
entries = re.split(r'@\w+\s*\{', content)[1:]
print('Total entries:', len(entries))
if entries:
    entry = entries[0]
    print('Entry snippet:', entry[:300])
    print('\n---\n')
    # Manually run parse_bib_text logic
    target_aliases_clean = {a.replace("*", "").replace(".", "").lower().strip() for a in TARGET_ALIASES}
    field_pattern = r'(\w+)\s*=\s*[\{"](.*?)(?<!\\)[\}"]'
    fields = {}
    for match in re.finditer(field_pattern, entry, re.DOTALL):
        key = match.group(1).lower()
        val = match.group(2).replace('\n', ' ').strip()
        fields[key] = val
    print('Fields found:', list(fields.keys()))
    if 'author' in fields:
        print('Author:', fields['author'])
        # Split authors
        raw_authors = fields['author']
        author_list = re.split(r'\s+and\s+', raw_authors, flags=re.IGNORECASE)
        author_list = [a.strip() for a in author_list]
        print('Author list:', author_list)
        # Find match
        match_index = -1
        for idx, author in enumerate(author_list):
            clean = author.replace("*", "").replace(".", "").lower().strip()
            if clean in target_aliases_clean:
                match_index = idx
                break
        print('Match index:', match_index)
        if match_index != -1:
            num_authors = len(author_list)
            if num_authors == 1:
                role = 'single'
            elif match_index == 0:
                role = 'first'
            elif match_index == num_authors - 1:
                role = 'last'
            else:
                role = 'middle'
            print('Role:', role)
            # Citations
            cites = 0
            if CITATION_FIELD.lower() in fields:
                cites = int(fields[CITATION_FIELD.lower()]) if fields[CITATION_FIELD.lower()].isdigit() else 0
            print('Citations:', cites)
            print('PAPER WOULD BE PARSED')
        else:
            print('No alias match')
    else:
        print('No author field')
    # Now call parse_bib_text on the same content
    papers = parse_bib_text(content, TARGET_ALIASES, CITATION_FIELD)
    print('\nparse_bib_text returned:', len(papers), 'papers')
