import re

def normalize_name(name: str) -> str:
    return name.replace("*", "").replace(".", "").lower().strip()

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
        raw_authors = fields['author']
        author_list = re.split(r'\s+and\s+', raw_authors, flags=re.IGNORECASE)
        author_list = [a.strip() for a in author_list]
        print('Author list:', author_list)
        target_aliases = ["Wu, M", "M. Wu", "Wu, M.", "Wu, M*", "M. Wu*", "Ming Wu"]
        target_aliases_clean = {normalize_name(a) for a in target_aliases}
        print('Target aliases cleaned:', target_aliases_clean)
        for idx, author in enumerate(author_list):
            print(f'  {idx}: {author} -> {normalize_name(author)}')
            if normalize_name(author) in target_aliases_clean:
                print('    MATCH')
        break
