import re

content = open('MyPaper.bib', 'r', encoding='utf-8').read()
article_pattern = r'@Article\s*\{[^@]+'
articles = re.findall(article_pattern, content, re.DOTALL)
for art in articles:
    if 'Design and Manufacture of a Flexible Adaptive Fixture' in art:
        field_pattern = r'(\w+)\s*=\s*[\{"](.*?)(?<!\\)[\}"]'
        fields = {}
        for match in re.finditer(field_pattern, art, re.DOTALL):
            key = match.group(1).lower()
            val = match.group(2).replace('\n', ' ').strip()
            fields[key] = val
        print('Fields:', list(fields.keys()))
        print('title:', fields.get('title'))
        print('citationthisyear:', fields.get('citationthisyear'))
        break
