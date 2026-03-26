import requests
import json

r = requests.get('http://localhost:8000/api/papers')
if r.status_code == 200:
    papers = r.json()
    print('Total papers:', len(papers))
    for p in papers:
        if 'Flexible Adaptive Fixture' in p['title']:
            print('Found:', p['title'])
            print('Citations:', p['citations'])
            print('Role:', p['role'])
            print('Authors:', p['authors'])
else:
    print('Error:', r.status_code)
