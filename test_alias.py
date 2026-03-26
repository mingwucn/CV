import sys
sys.path.insert(0, '.')
from backend import normalize_name, TARGET_ALIASES

target_aliases_clean = {normalize_name(a) for a in TARGET_ALIASES}
print('Target aliases cleaned:', target_aliases_clean)

# Example author string
author_str = "Wu, M and Liu, J and He, J and Chen, X and Guo*, Z"
author_list = [a.strip() for a in author_str.split(' and ')]
print('Author list:', author_list)
for idx, author in enumerate(author_list):
    clean = normalize_name(author)
    print(f'  {idx}: {author} -> {clean}')
    if clean in target_aliases_clean:
        print(f'    MATCH at index {idx}')
        break
