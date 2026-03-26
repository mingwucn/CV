import re

with open('MyPaper.bib', 'r', encoding='utf-8') as f:
    content = f.read()

# Split as Node does
import re
entries = re.split(r'@\w+\s*\{', content)[1:]
print('Number of entries:', len(entries))
if entries:
    entry = entries[0]
    print('First 500 chars of first entry:')
    print(entry[:500])
    print('\n---\n')
    # Apply regex
    field_pattern = r'(\w+)\s*=\s*[\{"](.*?)(?<!\\)[\}"]'
    matches = list(re.finditer(field_pattern, entry, re.DOTALL))
    print('Number of matches:', len(matches))
    for m in matches[:5]:
        print(f'  {m.group(1)} = {m.group(2)[:50]}...')
    # Check author field
    for m in matches:
        if m.group(1).lower() == 'author':
            print('Author found:', m.group(2))
            break
